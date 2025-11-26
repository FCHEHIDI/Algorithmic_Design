/**
 * kernel_scheduler.c
 * 
 * Core implementation - HOT PATH optimized for <100µs latency
 * 
 * Compilation:
 *   gcc -O3 -march=native -mtune=native -flto \
 *       -ffast-math -funroll-loops \
 *       -pthread -lrt \
 *       kernel_scheduler.c -o lab_scheduler
 * 
 * For PREEMPT_RT kernel:
 *   sudo chrt -f 99 ./lab_scheduler  # Run at RT priority
 */

#include "kernel_scheduler.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <math.h>

/* ============================================================================
 * INITIALIZATION
 * ============================================================================ */

int kernel_scheduler_init(kernel_scheduler_t *sched) {
    if (!sched) return -EINVAL;
    
    memset(sched, 0, sizeof(kernel_scheduler_t));
    
    /* Default configuration */
    sched->config.enable_preemption = true;
    sched->config.enable_aging = true;
    sched->config.enable_deadlock_detection = true;
    sched->config.enable_load_balancing = true;
    sched->config.deadlock_check_interval = 5;
    
    /* Aging thresholds (minutes) */
    sched->aging.routine_to_urgent_threshold = 60;
    sched->aging.urgent_to_stat_threshold = 120;
    
    /* Preemption policy: STAT_ONLY */
    sched->preemption.policy = 1;
    
    return 0;
}

/* ============================================================================
 * ADD RESOURCES (Thread-safe via atomics)
 * ============================================================================ */

int kernel_scheduler_add_sample(
    kernel_scheduler_t *sched,
    const char *id,
    sample_type_t type,
    uint8_t priority,
    uint32_t ready_time,
    uint32_t processing_time)
{
    if (sched->sample_count >= MAX_SAMPLES) return -ENOSPC;
    
    uint32_t idx = __sync_fetch_and_add(&sched->sample_count, 1);
    
    sample_t *s = &sched->samples[idx];
    strncpy(s->id, id, sizeof(s->id) - 1);
    s->type = type;
    s->priority = priority;
    s->ready_time = ready_time;
    s->processing_time = processing_time;
    s->wait_start = ready_time;
    s->scheduled = 0;
    
    return idx;
}

int kernel_scheduler_add_technician(
    kernel_scheduler_t *sched,
    uint32_t id,
    speciality_t speciality,
    uint32_t available_from)
{
    if (sched->technician_count >= MAX_TECHNICIANS) return -ENOSPC;
    
    uint32_t idx = __sync_fetch_and_add(&sched->technician_count, 1);
    
    technician_t *t = &sched->technicians[idx];
    t->id = id;
    t->speciality = speciality;
    t->available_from = available_from;
    t->total_duration = 0;
    t->sample_count = 0;
    t->lock = 0;
    
    return idx;
}

int kernel_scheduler_add_equipment(
    kernel_scheduler_t *sched,
    uint32_t id,
    sample_type_t type,
    uint32_t available_from)
{
    if (sched->equipment_count >= MAX_EQUIPMENT) return -ENOSPC;
    
    uint32_t idx = __sync_fetch_and_add(&sched->equipment_count, 1);
    
    equipment_t *e = &sched->equipment[idx];
    e->id = id;
    e->type = type;
    e->available_from = available_from;
    e->lock = 0;
    
    return idx;
}

/* ============================================================================
 * AGING SYSTEM (O(n) pass, called once per scheduling cycle)
 * ============================================================================ */

static void apply_aging(kernel_scheduler_t *sched, uint32_t current_time) {
    if (!sched->config.enable_aging) return;
    
    aging_system_t *aging = &sched->aging;
    
    for (uint32_t i = 0; i < sched->sample_count; i++) {
        sample_t *s = &sched->samples[i];
        
        if (s->scheduled) continue;  /* Skip already scheduled */
        
        uint32_t wait_time = current_time - s->wait_start;
        
        /* ROUTINE → URGENT after threshold */
        if (s->priority == PRIORITY_ROUTINE && 
            wait_time >= aging->routine_to_urgent_threshold &&
            !s->priority_boosted) {
            
            s->priority = PRIORITY_URGENT;
            s->priority_boosted = 1;
            aging->aging_events++;
            aging->total_aged_samples++;
        }
        /* URGENT → STAT after threshold */
        else if (s->priority == PRIORITY_URGENT && 
                 wait_time >= aging->urgent_to_stat_threshold &&
                 !s->priority_boosted) {
            
            s->priority = PRIORITY_STAT;
            s->priority_boosted = 1;
            aging->aging_events++;
            aging->total_aged_samples++;
        }
    }
}

/* ============================================================================
 * LOAD BALANCER (O(1) selection via cached loads)
 * ============================================================================ */

static inline int32_t find_least_loaded_technician(
    kernel_scheduler_t *sched,
    sample_type_t sample_type)
{
    if (!sched->config.enable_load_balancing) {
        /* Fallback: first available */
        for (uint32_t i = 0; i < sched->technician_count; i++) {
            technician_t *t = &sched->technicians[i];
            if (t->speciality == sample_type || t->speciality == SPECIALITY_GENERAL) {
                return i;
            }
        }
        return -1;
    }
    
    /* Find least loaded compatible technician */
    int32_t best_idx = -1;
    uint32_t min_load = UINT32_MAX;
    
    for (uint32_t i = 0; i < sched->technician_count; i++) {
        technician_t *t = &sched->technicians[i];
        
        /* Check compatibility */
        if (t->speciality != sample_type && t->speciality != SPECIALITY_GENERAL) {
            continue;
        }
        
        /* Load metric: duration + penalty for sample count */
        uint32_t load = t->total_duration + (t->sample_count * 5);
        
        if (load < min_load) {
            min_load = load;
            best_idx = i;
        }
    }
    
    return best_idx;
}

/* ============================================================================
 * RESOURCE ASSIGNMENT (Critical path - optimized)
 * ============================================================================ */

static inline bool assign_resources(
    kernel_scheduler_t *sched,
    sample_t *sample,
    uint32_t current_time,
    int32_t *out_tech_idx,
    int32_t *out_equip_idx,
    uint32_t *out_start_time)
{
    /* Find technician via load balancer */
    int32_t tech_idx = find_least_loaded_technician(sched, sample->type);
    if (tech_idx < 0) return false;
    
    /* Find compatible equipment */
    int32_t equip_idx = -1;
    uint32_t earliest_equip_time = UINT32_MAX;
    
    for (uint32_t i = 0; i < sched->equipment_count; i++) {
        equipment_t *e = &sched->equipment[i];
        if (e->type == sample->type && e->available_from < earliest_equip_time) {
            earliest_equip_time = e->available_from;
            equip_idx = i;
        }
    }
    
    if (equip_idx < 0) return false;
    
    /* Calculate start time */
    technician_t *tech = &sched->technicians[tech_idx];
    equipment_t *equip = &sched->equipment[equip_idx];
    
    uint32_t start = sample->ready_time;
    if (tech->available_from > start) start = tech->available_from;
    if (equip->available_from > start) start = equip->available_from;
    if (current_time > start) start = current_time;
    
    *out_tech_idx = tech_idx;
    *out_equip_idx = equip_idx;
    *out_start_time = start;
    
    return true;
}

/* ============================================================================
 * MAIN SCHEDULING ALGORITHM (HOT PATH)
 * ============================================================================ */

int kernel_scheduler_schedule(kernel_scheduler_t *sched) {
    /* Start timing */
    clock_gettime(CLOCK_MONOTONIC, &sched->start_time);
    uint64_t start_cycles = rdtsc();
    
    uint32_t current_time = 0;
    
    /* Phase 1: Apply aging */
    apply_aging(sched, current_time);
    
    /* Phase 2: Sort samples by priority (in-place) */
    /* Using insertion sort for cache-friendliness on small n */
    for (uint32_t i = 1; i < sched->sample_count; i++) {
        sample_t key = sched->samples[i];
        int32_t j = i - 1;
        
        /* Sort descending by priority (STAT=3 first) */
        while (j >= 0 && sched->samples[j].priority < key.priority) {
            sched->samples[j + 1] = sched->samples[j];
            j--;
        }
        sched->samples[j + 1] = key;
    }
    
    /* Phase 3: Main scheduling loop */
    sched->schedule_size = 0;
    
    for (uint32_t i = 0; i < sched->sample_count; i++) {
        sample_t *sample = &sched->samples[i];
        
        if (sample->scheduled) continue;
        
        /* Prefetch next sample for cache warmth */
        if (i + 1 < sched->sample_count) {
            prefetch(&sched->samples[i + 1]);
        }
        
        /* Find resources */
        int32_t tech_idx, equip_idx;
        uint32_t start_time;
        
        if (!assign_resources(sched, sample, current_time, 
                            &tech_idx, &equip_idx, &start_time)) {
            continue;  /* No resources available, skip for now */
        }
        
        /* Create schedule entry */
        schedule_entry_t *entry = &sched->schedule[sched->schedule_size++];
        entry->sample_id = i;
        entry->technician_id = tech_idx;
        entry->equipment_id = equip_idx;
        entry->start_time = start_time;
        entry->end_time = start_time + sample->processing_time;
        entry->priority = sample->priority;
        
        /* Update resources */
        technician_t *tech = &sched->technicians[tech_idx];
        equipment_t *equip = &sched->equipment[equip_idx];
        
        tech->available_from = entry->end_time;
        tech->total_duration += sample->processing_time;
        tech->sample_count++;
        
        equip->available_from = entry->end_time;
        
        sample->scheduled = 1;
        sample->assigned_tech_id = tech_idx;
        sample->assigned_equip_id = equip_idx;
        
        /* Update current_time for next iteration */
        if (entry->end_time > current_time) {
            current_time = entry->end_time;
        }
    }
    
    /* Calculate load balancing metrics */
    if (sched->config.enable_load_balancing && sched->technician_count > 0) {
        load_balancer_t *lb = &sched->load_balancer;
        
        /* Mean load */
        uint32_t sum = 0;
        for (uint32_t i = 0; i < sched->technician_count; i++) {
            uint32_t load = sched->technicians[i].total_duration;
            lb->loads[i].total_duration = load;
            lb->loads[i].sample_count = sched->technicians[i].sample_count;
            sum += load;
        }
        lb->avg_load = (float)sum / sched->technician_count;
        
        /* Standard deviation */
        float variance = 0.0f;
        for (uint32_t i = 0; i < sched->technician_count; i++) {
            float diff = lb->loads[i].total_duration - lb->avg_load;
            variance += diff * diff;
        }
        variance /= sched->technician_count;
        lb->std_deviation = sqrtf(variance);
        
        /* Coefficient of variation */
        lb->coefficient_variation = (lb->avg_load > 0) ? 
            (lb->std_deviation / lb->avg_load * 100.0f) : 0.0f;
    }
    
    /* End timing */
    clock_gettime(CLOCK_MONOTONIC, &sched->end_time);
    sched->cycles_elapsed = rdtsc() - start_cycles;
    
    return sched->schedule_size;
}

/* ============================================================================
 * QUERY API
 * ============================================================================ */

const schedule_entry_t* kernel_scheduler_get_entry(
    const kernel_scheduler_t *sched,
    uint32_t index)
{
    if (index >= sched->schedule_size) return NULL;
    return &sched->schedule[index];
}

void kernel_scheduler_get_metrics(
    const kernel_scheduler_t *sched,
    uint64_t *latency_ns,
    uint64_t *throughput_samples_per_sec,
    uint32_t *memory_kb)
{
    /* Calculate latency in nanoseconds */
    struct timespec diff;
    diff.tv_sec = sched->end_time.tv_sec - sched->start_time.tv_sec;
    diff.tv_nsec = sched->end_time.tv_nsec - sched->start_time.tv_nsec;
    if (diff.tv_nsec < 0) {
        diff.tv_sec--;
        diff.tv_nsec += 1000000000L;
    }
    *latency_ns = diff.tv_sec * 1000000000L + diff.tv_nsec;
    
    /* Throughput */
    double seconds = *latency_ns / 1e9;
    *throughput_samples_per_sec = (seconds > 0) ? 
        (uint64_t)(sched->schedule_size / seconds) : 0;
    
    /* Memory usage (resident set size) */
    *memory_kb = sizeof(kernel_scheduler_t) / 1024;
}

/* ============================================================================
 * UTILITIES
 * ============================================================================ */

void kernel_scheduler_print_schedule(const kernel_scheduler_t *sched) {
    printf("\n=== SCHEDULE (%u entries) ===\n", sched->schedule_size);
    
    for (uint32_t i = 0; i < sched->schedule_size; i++) {
        const schedule_entry_t *e = &sched->schedule[i];
        const sample_t *s = &sched->samples[e->sample_id];
        
        printf("%3u. %-10s : %3u -> %3u min (TECH%02u, EQUIP%02u) [P=%u]\n",
               i + 1,
               s->id,
               e->start_time,
               e->end_time,
               e->technician_id,
               e->equipment_id,
               e->priority);
    }
    
    /* Print metrics */
    uint64_t latency_ns, throughput;
    uint32_t memory_kb;
    kernel_scheduler_get_metrics(sched, &latency_ns, &throughput, &memory_kb);
    
    printf("\n=== METRICS ===\n");
    printf("Latency       : %lu µs\n", latency_ns / 1000);
    printf("Throughput    : %lu samples/sec\n", throughput);
    printf("Memory        : %u KB\n", memory_kb);
    printf("CPU cycles    : %lu\n", sched->cycles_elapsed);
    
    if (sched->config.enable_load_balancing) {
        printf("\n=== LOAD BALANCING ===\n");
        printf("CV            : %.2f%%\n", sched->load_balancer.coefficient_variation);
        printf("Avg Load      : %.1f min\n", sched->load_balancer.avg_load);
        printf("Std Dev       : %.1f\n", sched->load_balancer.std_deviation);
    }
}

void kernel_scheduler_destroy(kernel_scheduler_t *sched) {
    /* Nothing to free for stack-allocated structures */
    /* In production, would free any dynamically allocated memory */
}

/* ============================================================================
 * EXAMPLE USAGE
 * ============================================================================ */

#ifdef BUILD_STANDALONE

int main(int argc, char *argv[]) {
    kernel_scheduler_t sched;
    
    printf("Initializing kernel scheduler...\n");
    if (kernel_scheduler_init(&sched) < 0) {
        perror("init failed");
        return 1;
    }
    
    /* Add test data */
    kernel_scheduler_add_sample(&sched, "S001", SAMPLE_TYPE_BLOOD, PRIORITY_URGENT, 480, 25);
    kernel_scheduler_add_sample(&sched, "S002", SAMPLE_TYPE_BLOOD, PRIORITY_STAT, 510, 15);
    kernel_scheduler_add_sample(&sched, "S003", SAMPLE_TYPE_URINE, PRIORITY_ROUTINE, 480, 30);
    
    kernel_scheduler_add_technician(&sched, 0, SPECIALITY_BLOOD, 480);
    kernel_scheduler_add_technician(&sched, 1, SPECIALITY_URINE, 480);
    kernel_scheduler_add_technician(&sched, 2, SPECIALITY_GENERAL, 480);
    
    kernel_scheduler_add_equipment(&sched, 0, SAMPLE_TYPE_BLOOD, 480);
    kernel_scheduler_add_equipment(&sched, 1, SAMPLE_TYPE_URINE, 480);
    
    /* Run scheduler */
    printf("\nRunning scheduler...\n");
    int scheduled = kernel_scheduler_schedule(&sched);
    
    if (scheduled < 0) {
        perror("schedule failed");
        return 1;
    }
    
    printf("\nScheduled %d samples\n", scheduled);
    kernel_scheduler_print_schedule(&sched);
    
    kernel_scheduler_destroy(&sched);
    
    return 0;
}

#endif /* BUILD_STANDALONE */
