"""
Advanced Kernel-Inspired Scheduler

Scheduler avancé intégrant :
- Préemption (interruption haute priorité)
- Aging (anti-starvation)
- Deadlock Detection
- Load Balancing
"""

from typing import List, Optional, Dict
import logging
from dataclasses import dataclass

from .strategies import SchedulingStrategy
from .schedule import Schedule
from .kernel_features import (
    PreemptionManager, PreemptionPolicy,
    AgingSystem, AgingConfig,
    DeadlockDetector,
    LoadBalancer
)
from ..domain.models import Sample, Priority, ScheduleEntry
from ..resources.manager import ResourceManager

logger = logging.getLogger(__name__)


@dataclass
class KernelSchedulerConfig:
    """Configuration du scheduler kernel-inspired"""
    
    # Préemption
    enable_preemption: bool = True
    preemption_policy: PreemptionPolicy = PreemptionPolicy.STAT_ONLY
    
    # Aging
    enable_aging: bool = True
    aging_config: Optional[AgingConfig] = None
    
    # Deadlock Detection
    enable_deadlock_detection: bool = True
    deadlock_check_interval: int = 5  # Vérifier tous les N échantillons
    
    # Load Balancing
    enable_load_balancing: bool = True
    
    # Concurrence
    enable_concurrent: bool = True
    max_workers: int = 4


class KernelScheduler(SchedulingStrategy):
    """
    Scheduler Avancé inspiré des kernels OS modernes
    
    Combine :
    - Ordonnancement par priorité (comme SCHED_FIFO)
    - Préemption (comme IRQ handlers)
    - Aging (comme CFS)
    - Deadlock detection (comme resource allocation graphs)
    - Load balancing (comme SMP scheduler)
    
    Architecture :
    ┌────────────────────────────────────┐
    │  KernelScheduler (Orchestrateur)  │
    └────────────┬───────────────────────┘
                 │
    ┌────────────┴───────────────────────┐
    │  PreemptionManager                 │  ← IRQ-like
    │  AgingSystem                       │  ← CFS-like
    │  DeadlockDetector                  │  ← Banker's algorithm
    │  LoadBalancer                      │  ← SMP-like
    └────────────────────────────────────┘
    """
    
    def __init__(self, config: Optional[KernelSchedulerConfig] = None):
        self.config = config or KernelSchedulerConfig()
        
        # Initialiser composants kernel
        self.preemption_manager = PreemptionManager(
            policy=self.config.preemption_policy
        ) if self.config.enable_preemption else None
        
        self.aging_system = AgingSystem(
            config=self.config.aging_config
        ) if self.config.enable_aging else None
        
        self.deadlock_detector = DeadlockDetector() \
            if self.config.enable_deadlock_detection else None
        
        self.load_balancer = LoadBalancer() \
            if self.config.enable_load_balancing else None
        
        self.stats = {
            "preemptions": 0,
            "aging_boosts": 0,
            "deadlocks_detected": 0,
            "load_balancing_decisions": 0
        }
    
    def name(self) -> str:
        return "Kernel-Inspired Scheduler (Preemption+Aging+Deadlock+LoadBalance)"
    
    def schedule(
        self,
        samples: List[Sample],
        resource_manager: ResourceManager,
        start_time: int = 480
    ) -> Schedule:
        """
        Ordonnancement avec features kernel avancées
        
        Algorithme :
        1. Appliquer aging aux échantillons en attente
        2. Trier par priorité (boostée par aging)
        3. Pour chaque échantillon :
           a. Load balancing : Choisir ressources optimales
           b. Vérifier préemption possible
           c. Assigner ou préempter
        4. Détecter deadlocks périodiquement
        5. Reprendre analyses interrompues
        """
        schedule = Schedule()
        current_time = start_time
        
        # Initialiser load balancer avec tous les techniciens
        if self.load_balancer:
            all_technicians = resource_manager.get_all_technicians()
            self.load_balancer.initialize_loads(all_technicians)
        
        # Phase 1 : Appliquer aging
        if self.aging_system:
            samples = self.aging_system.apply_aging(samples, current_time)
            logger.info(f"✓ Aging appliqué à {len(samples)} échantillons")
        
        # Phase 2 : Trier par priorité (STAT > URGENT > ROUTINE)
        priority_order = {Priority.STAT: 3, Priority.URGENT: 2, Priority.ROUTINE: 1}
        samples_sorted = sorted(
            samples,
            key=lambda s: (priority_order.get(s.priority, 0), s.ready_time),
            reverse=True
        )
        
        waiting_samples: List[Sample] = []
        processed_count = 0
        
        # Phase 3 : Ordonnancement principal
        for i, sample in enumerate(samples_sorted):
            logger.debug(f"\n--- Traitement échantillon {sample.id} ({sample.priority.value}) ---")
            
            # Vérifier deadlock périodiquement
            if (self.deadlock_detector and 
                processed_count % self.config.deadlock_check_interval == 0 and
                waiting_samples):
                
                self._check_deadlock(waiting_samples, schedule.entries, current_time)
            
            # Phase 3a : Load Balancing - Trouver ressources optimales
            resources = self._find_resources_with_load_balancing(
                sample, resource_manager, current_time
            )
            
            if not resources:
                logger.warning(f"⏳ Aucune ressource pour {sample.id}, ajout à la file d'attente")
                waiting_samples.append(sample)
                continue
            
            tech, equip, actual_start = resources
            
            # Phase 3b : Vérifier préemption
            preemption_occurred = False
            if self.preemption_manager and sample.priority == Priority.STAT:
                preemption_occurred = self._check_and_preempt(
                    sample, schedule, actual_start
                )
            
            # Phase 3c : Créer entrée de planning
            entry = ScheduleEntry(
                sample_id=sample.id,
                priority=sample.priority,
                technician_id=tech.id,
                equipment_id=equip.id,
                start_time=actual_start,
                end_time=actual_start + sample.processing_time
            )
            
            schedule.add_entry(entry)
            
            # Réserver ressources
            tech.reserve(actual_start, sample.processing_time, sample.id)
            equip.reserve(actual_start, sample.processing_time, sample.id)
            
            # Mettre à jour load balancer
            if self.load_balancer:
                self.load_balancer.update_load(
                    tech.id,
                    sample.processing_time,
                    actual_start,
                    entry.end_time
                )
            
            current_time = max(current_time, entry.end_time)
            processed_count += 1
            
            logger.info(
                f"✓ {sample.id} planifié : {tech.id} + {equip.id} "
                f"@ {actual_start}-{entry.end_time} "
                f"{'[PREEMPTION]' if preemption_occurred else ''}"
            )
        
        # Phase 4 : Reprendre analyses interrompues
        if self.preemption_manager:
            self._resume_preempted_analyses(schedule, resource_manager, current_time)
        
        # Phase 5 : Calculer métriques kernel
        self._calculate_final_metrics(schedule, current_time)
        
        # Ajouter échantillons non planifiés comme conflits
        for sample in waiting_samples:
            schedule.add_conflict(sample.id)
        
        logger.info(f"\n{'='*60}")
        logger.info(f"📊 RÉSUMÉ KERNEL SCHEDULER")
        logger.info(f"{'='*60}")
        logger.info(f"✓ Échantillons planifiés : {len(schedule.entries)}")
        logger.info(f"✗ Conflits : {len(schedule.conflicts)}")
        
        if self.preemption_manager:
            preempt_stats = self.preemption_manager.get_stats()
            logger.info(f"⚠️ Préemptions : {preempt_stats['total_preemptions']}")
        
        if self.aging_system:
            aging_stats = self.aging_system.get_stats()
            logger.info(f"🔼 Aging events : {aging_stats['aging_events']}")
        
        if self.deadlock_detector:
            deadlock_stats = self.deadlock_detector.get_stats()
            logger.info(f"💀 Deadlocks détectés : {deadlock_stats['total_deadlocks_detected']}")
        
        if self.load_balancer:
            balance_stats = self.load_balancer.get_stats()
            if balance_stats.get("current_balance"):
                cv = balance_stats["current_balance"]["coefficient_variation"]
                status = balance_stats["current_balance"]["status"]
                logger.info(f"⚖️ Load Balance : CV={cv:.1f}% ({status})")
        
        logger.info(f"{'='*60}\n")
        
        return schedule
    
    def _find_resources_with_load_balancing(
        self,
        sample: Sample,
        resource_manager: ResourceManager,
        current_time: int
    ) -> Optional[tuple]:
        """
        Trouve ressources en utilisant load balancing pour techniciens.
        Utilise l'API publique du ResourceManager.
        """
        if not self.config.enable_load_balancing:
            # Utiliser méthode standard du ResourceManager
            tech, equip, start = resource_manager.find_resources_for(sample)
            if tech and equip:
                return (tech, equip, max(start, current_time))
            return None
        
        # Trouver tous les techniciens compatibles via API publique
        compatible_techs = resource_manager._get_compatible_technicians(sample.type)
        if not compatible_techs:
            return None
        
        # Load Balancing : Sélectionner technicien le moins chargé
        selected_tech = self.load_balancer.get_least_loaded_technician(
            compatible_techs, current_time
        )
        if not selected_tech:
            return None
        
        # Trouver équipement compatible via API publique
        compatible_equips = resource_manager._get_compatible_equipment(sample.type)
        if not compatible_equips:
            return None
        
        # Prendre premier équipement disponible
        selected_equip = None
        for equip in compatible_equips:
            if equip.available_from <= current_time:
                selected_equip = equip
                break
        
        if not selected_equip:
            # Prendre équipement avec la plus petite available_from
            selected_equip = min(compatible_equips, key=lambda e: e.available_from)
        
        # Calculer heure de début
        start_time = max(
            sample.ready_time,
            selected_tech.available_from,
            selected_equip.available_from,
            current_time
        )
        
        return (selected_tech, selected_equip, start_time)
    
    def _check_and_preempt(
        self,
        incoming_sample: Sample,
        schedule: Schedule,
        current_time: int
    ) -> bool:
        """
        Vérifie si une analyse en cours peut être interrompue
        
        Retourne True si préemption effectuée
        """
        if not self.preemption_manager:
            return False
        
        # Trouver analyses en cours à current_time
        ongoing_entries = [
            entry for entry in schedule.entries
            if entry.start_time <= current_time < entry.end_time
        ]
        
        for entry in ongoing_entries:
            if self.preemption_manager.can_preempt(entry, incoming_sample):
                # PRÉEMPTION !
                preempted = self.preemption_manager.preempt_analysis(
                    entry, current_time, incoming_sample.id
                )
                
                # Retirer entrée préemptée du schedule (sera reprise plus tard)
                schedule.entries.remove(entry)
                
                self.stats["preemptions"] += 1
                return True
        
        return False
    
    def _resume_preempted_analyses(
        self,
        schedule: Schedule,
        resource_manager: ResourceManager,
        current_time: int
    ):
        """
        Reprend les analyses interrompues par préemption
        
        Équivalent kernel : Restaurer le contexte après IRQ
        """
        if not self.preemption_manager:
            return
        
        resumed_count = 0
        
        while True:
            preempted = self.preemption_manager.get_next_preempted()
            if not preempted:
                break
            
            # Trouver ressources pour reprendre
            original_entry = preempted.entry
            
            # Recréer Sample pour recherche ressources
            sample = Sample(
                id=original_entry.sample_id,
                type=original_entry.sample_priority,  # Approximation
                priority=original_entry.sample_priority,
                ready_time=current_time,
                processing_time=preempted.remaining_time
            )
            
            resources = self._find_resources_with_load_balancing(
                sample, resource_manager, current_time
            )
            
            if resources:
                tech, equip = resources
                actual_start = max(current_time, tech.available_from, equip.available_from)
                
                # Créer nouvelle entrée pour le reste de l'analyse
                resumed_entry = ScheduleEntry(
                    sample_id=original_entry.sample_id,
                    sample_priority=original_entry.sample_priority,
                    technician_id=tech.id,
                    equipment_id=equip.id,
                    start_time=actual_start,
                    duration=preempted.remaining_time
                )
                
                schedule.add_entry(resumed_entry)
                
                # Réserver ressources
                tech.reserve(actual_start, preempted.remaining_time)
                equip.reserve(actual_start, preempted.remaining_time)
                
                current_time = max(current_time, resumed_entry.end_time)
                resumed_count += 1
                
                logger.info(
                    f"♻️ REPRISE: {original_entry.sample_id} reprend "
                    f"@ {actual_start} (reste: {preempted.remaining_time} min)"
                )
            else:
                logger.warning(
                    f"⚠️ Impossible de reprendre {original_entry.sample_id} "
                    f"(aucune ressource)"
                )
        
        if resumed_count > 0:
            logger.info(f"✓ {resumed_count} analyses interrompues reprises")
    
    def _check_deadlock(
        self,
        waiting_samples: List[Sample],
        schedule_entries: List[ScheduleEntry],
        current_time: int
    ):
        """Vérifie et résout les deadlocks"""
        if not self.deadlock_detector:
            return
        
        # Construire wait-for graph
        wait_graph = self.deadlock_detector.build_wait_graph(
            waiting_samples, schedule_entries
        )
        
        if not wait_graph:
            return
        
        # Détecter cycles
        cycles = self.deadlock_detector.detect_cycles()
        
        if cycles:
            self.stats["deadlocks_detected"] += len(cycles)
            
            for cycle in cycles:
                # Résoudre deadlock
                deadlock_info = self.deadlock_detector.resolve_deadlock(
                    cycle, current_time
                )
                
                logger.error(
                    f"💀 DEADLOCK: {' → '.join(cycle)} "
                    f"(résolution: {deadlock_info.resolution_strategy})"
                )
    
    def _calculate_final_metrics(self, schedule: Schedule, total_time: int):
        """Calcule et attache métriques finales kernel-inspired"""
        
        # Métriques kernel avancées
        kernel_metrics = {
            "kernel_features": {}
        }
        
        if self.preemption_manager:
            kernel_metrics["kernel_features"]["preemption"] = \
                self.preemption_manager.get_stats()
        
        if self.aging_system:
            kernel_metrics["kernel_features"]["aging"] = \
                self.aging_system.get_stats()
        
        if self.deadlock_detector:
            kernel_metrics["kernel_features"]["deadlock_detection"] = \
                self.deadlock_detector.get_stats()
        
        if self.load_balancer:
            balance_metrics = self.load_balancer.calculate_balance_metrics(total_time)
            kernel_metrics["kernel_features"]["load_balancing"] = balance_metrics
        
        # Stocker pour récupération ultérieure (sera ajouté au dict dans planner.py)
        self.kernel_metrics = kernel_metrics
    
    def get_comprehensive_stats(self) -> Dict:
        """Statistiques complètes du scheduler kernel"""
        stats = {
            "scheduler": self.name(),
            "config": {
                "preemption": self.config.enable_preemption,
                "aging": self.config.enable_aging,
                "deadlock_detection": self.config.enable_deadlock_detection,
                "load_balancing": self.config.enable_load_balancing
            },
            "runtime_stats": self.stats
        }
        
        if self.preemption_manager:
            stats["preemption_details"] = self.preemption_manager.get_stats()
        
        if self.aging_system:
            stats["aging_details"] = self.aging_system.get_stats()
        
        if self.deadlock_detector:
            stats["deadlock_details"] = self.deadlock_detector.get_stats()
        
        if self.load_balancer:
            stats["load_balancing_details"] = self.load_balancer.get_stats()
        
        return stats
