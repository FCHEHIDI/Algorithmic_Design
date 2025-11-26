/**
 * kernel_scheduler.h
 * 
 * Kernel-inspired scheduler for medical laboratory - C implementation
 * Designed for CentOS RT / RHEL RT with PREEMPT_RT patch
 * 
 * Performance targets:
 * - Latency: <100µs worst-case
 * - Throughput: 50000+ samples/second
 * - Memory: <5MB resident
 * - Jitter: <10µs (99.99th percentile)
 */

#ifndef KERNEL_SCHEDULER_H
#define KERNEL_SCHEDULER_H

#include <stdint.h>
#include <stdbool.h>
#include <pthread.h>
#include <time.h>

/* ============================================================================
 * CONSTANTS
 * ============================================================================ */

#define MAX_SAMPLES         10000
#define MAX_TECHNICIANS     100
#define MAX_EQUIPMENT       200
#define MAX_SCHEDULE_ENTRIES 10000

/* Priority levels (compatible with Linux SCHED_FIFO) */
#define PRIORITY_STAT       3  /* RT priority 99 */
#define PRIORITY_URGENT     2  /* RT priority 50 */
#define PRIORITY_ROUTINE    1  /* SCHED_OTHER nice=0 */

/* Sample types */
typedef enum {
    SAMPLE_TYPE_BLOOD = 0,
    SAMPLE_TYPE_URINE = 1,
    SAMPLE_TYPE_TISSUE = 2,
    SAMPLE_TYPE_MAX = 3
} sample_type_t;

/* Technician specialities */
typedef enum {
    SPECIALITY_BLOOD = 0,
    SPECIALITY_URINE = 1,
    SPECIALITY_TISSUE = 2,
    SPECIALITY_GENERAL = 3,
    SPECIALITY_MAX = 4
} speciality_t;

/* ============================================================================
 * DATA STRUCTURES (Cache-aligned for performance)
 * ============================================================================ */

/**
 * Sample structure (64 bytes, fits in single cache line)
 */
typedef struct __attribute__((aligned(64))) {
    char id[16];                /* Sample ID (e.g., "S001") */
    sample_type_t type;         /* BLOOD, URINE, TISSUE */
    uint8_t priority;           /* STAT=3, URGENT=2, ROUTINE=1 */
    uint32_t ready_time;        /* Minutes since midnight */
    uint32_t processing_time;   /* Duration in minutes */
    
    /* Aging fields */
    uint32_t wait_start;        /* When sample entered queue */
    uint8_t priority_boosted;   /* Has aging increased priority? */
    
    /* Scheduling state */
    uint8_t scheduled;          /* 0=waiting, 1=scheduled, 2=preempted */
    uint32_t assigned_tech_id;  /* Technician ID */
    uint32_t assigned_equip_id; /* Equipment ID */
    
    /* Padding to 64 bytes */
    uint8_t _padding[19];
} sample_t;

/**
 * Technician structure (64 bytes, cache-aligned)
 */
typedef struct __attribute__((aligned(64))) {
    uint32_t id;                /* Technician ID */
    speciality_t speciality;    /* Specialization */
    uint32_t available_from;    /* Next available time (minutes) */
    
    /* Load balancing */
    uint32_t total_duration;    /* Total work assigned (minutes) */
    uint16_t sample_count;      /* Number of samples assigned */
    
    /* Lock-free synchronization */
    volatile uint32_t lock;     /* Spinlock for CAS operations */
    
    uint8_t _padding[40];
} technician_t;

/**
 * Equipment structure (64 bytes, cache-aligned)
 */
typedef struct __attribute__((aligned(64))) {
    uint32_t id;                /* Equipment ID */
    sample_type_t type;         /* Compatible sample type */
    uint32_t available_from;    /* Next available time (minutes) */
    
    volatile uint32_t lock;     /* Spinlock */
    
    uint8_t _padding[48];
} equipment_t;

/**
 * Schedule entry (32 bytes, compact)
 */
typedef struct {
    uint32_t sample_id;
    uint32_t technician_id;
    uint32_t equipment_id;
    uint32_t start_time;
    uint32_t end_time;
    uint8_t priority;
    uint8_t _padding[11];
} schedule_entry_t;

/* ============================================================================
 * KERNEL FEATURES
 * ============================================================================ */

/**
 * Preemption Manager
 * Uses bitmap for O(1) preemption checks (like Linux runqueue bitmap)
 */
typedef struct {
    uint64_t preemptible_bitmap;    /* Bit per priority level */
    uint32_t total_preemptions;
    uint16_t pending_resumptions;
    uint8_t policy;                 /* 0=NONE, 1=STAT_ONLY, 2=PRIORITY_BASED */
    
    /* Queue of preempted samples (circular buffer) */
    uint32_t preempted_queue[256];
    uint8_t queue_head;
    uint8_t queue_tail;
} preemption_mgr_t;

/**
 * Aging System
 * Uses Red-Black Tree for O(log n) age-sorted lookups (like Linux CFS)
 */
typedef struct {
    uint32_t routine_to_urgent_threshold;  /* Minutes */
    uint32_t urgent_to_stat_threshold;     /* Minutes */
    uint32_t aging_events;
    uint32_t total_aged_samples;
} aging_system_t;

/**
 * Deadlock Detector
 * Lock-free wait-for graph using atomic operations
 */
typedef struct {
    /* Adjacency list representation (wait-for graph) */
    uint32_t wait_edges[MAX_SAMPLES][4];  /* Max 4 resource dependencies */
    uint8_t edge_count[MAX_SAMPLES];
    
    uint32_t total_deadlocks_detected;
    uint32_t deadlocks_resolved;
} deadlock_detector_t;

/**
 * Load Balancer
 * Per-CPU load tracking (like Linux SMP scheduler)
 */
typedef struct {
    /* Load per technician */
    struct {
        uint32_t total_duration;
        uint16_t sample_count;
        float utilization_rate;
    } loads[MAX_TECHNICIANS];
    
    /* Balance metrics */
    float coefficient_variation;
    float avg_load;
    float std_deviation;
} load_balancer_t;

/* ============================================================================
 * MAIN SCHEDULER CONTEXT
 * ============================================================================ */

typedef struct {
    /* Input data */
    sample_t samples[MAX_SAMPLES];
    technician_t technicians[MAX_TECHNICIANS];
    equipment_t equipment[MAX_EQUIPMENT];
    
    uint32_t sample_count;
    uint32_t technician_count;
    uint32_t equipment_count;
    
    /* Output schedule */
    schedule_entry_t schedule[MAX_SCHEDULE_ENTRIES];
    uint32_t schedule_size;
    
    /* Kernel features */
    preemption_mgr_t preemption;
    aging_system_t aging;
    deadlock_detector_t deadlock;
    load_balancer_t load_balancer;
    
    /* Configuration */
    struct {
        bool enable_preemption;
        bool enable_aging;
        bool enable_deadlock_detection;
        bool enable_load_balancing;
        uint8_t deadlock_check_interval;
    } config;
    
    /* Performance metrics */
    struct timespec start_time;
    struct timespec end_time;
    uint64_t cycles_elapsed;  /* CPU cycles via RDTSC */
    
} kernel_scheduler_t;

/* ============================================================================
 * PUBLIC API
 * ============================================================================ */

/**
 * Initialize kernel scheduler
 * Returns 0 on success, -1 on error
 */
int kernel_scheduler_init(kernel_scheduler_t *sched);

/**
 * Add sample to scheduler
 * Thread-safe, uses atomic operations
 */
int kernel_scheduler_add_sample(
    kernel_scheduler_t *sched,
    const char *id,
    sample_type_t type,
    uint8_t priority,
    uint32_t ready_time,
    uint32_t processing_time
);

/**
 * Add technician to scheduler
 */
int kernel_scheduler_add_technician(
    kernel_scheduler_t *sched,
    uint32_t id,
    speciality_t speciality,
    uint32_t available_from
);

/**
 * Add equipment to scheduler
 */
int kernel_scheduler_add_equipment(
    kernel_scheduler_t *sched,
    uint32_t id,
    sample_type_t type,
    uint32_t available_from
);

/**
 * Run scheduling algorithm
 * This is the HOT PATH - optimized for latency
 * 
 * Returns number of scheduled samples, or -1 on error
 */
int kernel_scheduler_schedule(kernel_scheduler_t *sched);

/**
 * Get schedule entry
 */
const schedule_entry_t* kernel_scheduler_get_entry(
    const kernel_scheduler_t *sched,
    uint32_t index
);

/**
 * Get performance metrics
 */
void kernel_scheduler_get_metrics(
    const kernel_scheduler_t *sched,
    uint64_t *latency_ns,
    uint64_t *throughput_samples_per_sec,
    uint32_t *memory_kb
);

/**
 * Print schedule (for debugging)
 */
void kernel_scheduler_print_schedule(const kernel_scheduler_t *sched);

/**
 * Cleanup and free resources
 */
void kernel_scheduler_destroy(kernel_scheduler_t *sched);

/* ============================================================================
 * INLINE PERFORMANCE HELPERS
 * ============================================================================ */

/**
 * Read CPU timestamp counter (RDTSC) for cycle-accurate timing
 */
static inline uint64_t rdtsc(void) {
    uint32_t lo, hi;
    __asm__ __volatile__ ("rdtsc" : "=a"(lo), "=d"(hi));
    return ((uint64_t)hi << 32) | lo;
}

/**
 * Compiler memory barrier
 */
static inline void barrier(void) {
    __asm__ __volatile__("" ::: "memory");
}

/**
 * Atomic compare-and-swap (CAS) for lock-free operations
 */
static inline bool cas_u32(volatile uint32_t *ptr, uint32_t old_val, uint32_t new_val) {
    return __sync_bool_compare_and_swap(ptr, old_val, new_val);
}

/**
 * Prefetch cache line (for predictable samples array access)
 */
static inline void prefetch(const void *addr) {
    __builtin_prefetch(addr, 0, 3);  /* Read, high temporal locality */
}

#endif /* KERNEL_SCHEDULER_H */
