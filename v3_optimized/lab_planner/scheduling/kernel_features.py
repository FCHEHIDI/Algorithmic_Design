"""
Kernel-Inspired Advanced Scheduling Features

Ce module implémente des concepts avancés inspirés des kernels OS :
- Préemption (interruption de tâches pour haute priorité)
- Aging (éviter la starvation)
- Deadlock Detection (détection de blocages)
- Load Balancing (distribution équitable des charges)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple
from enum import Enum
import time
import logging
from ..domain.models import Sample, Technician, Equipment, Priority, ScheduleEntry

logger = logging.getLogger(__name__)


class PreemptionPolicy(Enum):
    """Politique de préemption"""
    NONE = "none"                    # Pas de préemption
    STAT_ONLY = "stat_only"          # Seulement pour STAT
    PRIORITY_BASED = "priority_based"  # Basé sur différence de priorité


@dataclass
class PreemptedAnalysis:
    """Analyse interrompue en attente de reprise"""
    entry: ScheduleEntry
    paused_at: int          # Minute où l'analyse a été pausée
    remaining_time: int     # Temps restant
    resume_priority: int    # Priorité pour reprise (peut être boostée)
    preempted_by: str      # ID de l'échantillon préempteur


@dataclass
class AgingConfig:
    """Configuration du système d'aging"""
    enabled: bool = True
    threshold_minutes: int = 60      # Seuil avant boost
    routine_to_urgent: int = 60      # ROUTINE → URGENT après 60 min
    urgent_to_stat: int = 120        # URGENT → STAT après 120 min (exceptionnel)
    boost_factor: float = 1.5        # Facteur de boost de priorité


@dataclass
class ResourceWaitEdge:
    """Arête dans le graphe d'attente (wait-for graph)"""
    from_sample: str        # Échantillon qui attend
    to_sample: str          # Échantillon qui bloque la ressource
    resource_type: str      # 'technician' ou 'equipment'
    resource_id: str        # ID de la ressource


@dataclass
class DeadlockInfo:
    """Information sur un deadlock détecté"""
    cycle: List[str]                    # Cycle d'échantillons
    involved_resources: List[str]       # Ressources impliquées
    detection_time: int                 # Quand détecté
    resolution_strategy: str            # Comment résolu


@dataclass
class TechnicianLoad:
    """Charge de travail d'un technicien"""
    technician_id: str
    total_duration: int = 0             # Durée totale assignée
    sample_count: int = 0               # Nombre d'échantillons
    idle_time: int = 0                  # Temps d'inactivité
    last_end_time: int = 0              # Fin de dernière tâche
    
    def utilization_rate(self, total_time: int) -> float:
        """Taux d'utilisation du technicien"""
        if total_time == 0:
            return 0.0
        return (self.total_duration / total_time) * 100
    
    def average_gap(self) -> float:
        """Temps moyen entre tâches"""
        if self.sample_count == 0:
            return 0.0
        return self.idle_time / self.sample_count


class PreemptionManager:
    """
    Gestionnaire de préemption inspiré des IRQ handlers kernel
    
    Permet d'interrompre une analyse en cours pour traiter une haute priorité.
    Équivalent à : interrupt handler qui sauvegarde le contexte et schedule une tâche prioritaire.
    """
    
    def __init__(self, policy: PreemptionPolicy = PreemptionPolicy.STAT_ONLY):
        self.policy = policy
        self.preempted_queue: List[PreemptedAnalysis] = []
        self.preemption_count = 0
        
    def can_preempt(self, current_entry: ScheduleEntry, incoming_sample: Sample) -> bool:
        """
        Détermine si l'analyse actuelle peut être interrompue.
        
        Règles :
        - STAT_ONLY : Seulement si incoming est STAT et current n'est pas STAT
        - PRIORITY_BASED : Si incoming a priorité strictement supérieure
        """
        if self.policy == PreemptionPolicy.NONE:
            return False
        
        current_priority = self._get_priority_value(current_entry.sample_priority)
        incoming_priority = self._get_priority_value(incoming_sample.priority)
        
        if self.policy == PreemptionPolicy.STAT_ONLY:
            return (incoming_sample.priority == Priority.STAT and 
                    current_entry.sample_priority != Priority.STAT)
        
        # PRIORITY_BASED
        return incoming_priority > current_priority
    
    def preempt_analysis(
        self, 
        current_entry: ScheduleEntry, 
        current_time: int,
        preemptor_id: str
    ) -> PreemptedAnalysis:
        """
        Interrompt une analyse et la met en file d'attente.
        
        Équivalent kernel : save_context() lors d'une IRQ
        """
        elapsed_time = current_time - current_entry.start_time
        remaining_time = current_entry.duration - elapsed_time
        
        preempted = PreemptedAnalysis(
            entry=current_entry,
            paused_at=current_time,
            remaining_time=max(0, remaining_time),
            resume_priority=self._get_priority_value(current_entry.sample_priority) + 1,  # Boost
            preempted_by=preemptor_id
        )
        
        self.preempted_queue.append(preempted)
        self.preemption_count += 1
        
        logger.warning(
            f"⚠️ PRÉEMPTION: {current_entry.sample_id} interrompu par {preemptor_id} "
            f"(reste {remaining_time} min)"
        )
        
        return preempted
    
    def get_next_preempted(self) -> Optional[PreemptedAnalysis]:
        """Récupère la prochaine analyse à reprendre (plus haute priorité)"""
        if not self.preempted_queue:
            return None
        
        # Trier par priorité de reprise (boostée)
        self.preempted_queue.sort(key=lambda p: p.resume_priority, reverse=True)
        return self.preempted_queue.pop(0)
    
    def _get_priority_value(self, priority: Priority) -> int:
        """Convertit Priority en valeur numérique"""
        priority_map = {
            Priority.STAT: 3,
            Priority.URGENT: 2,
            Priority.ROUTINE: 1
        }
        return priority_map.get(priority, 0)
    
    def get_stats(self) -> Dict:
        """Statistiques de préemption"""
        return {
            "total_preemptions": self.preemption_count,
            "pending_resumptions": len(self.preempted_queue),
            "policy": self.policy.value
        }


class AgingSystem:
    """
    Système d'aging inspiré de Linux CFS (Completely Fair Scheduler)
    
    Augmente progressivement la priorité des tâches qui attendent trop longtemps
    pour éviter la starvation (famine).
    """
    
    def __init__(self, config: Optional[AgingConfig] = None):
        self.config = config or AgingConfig()
        self.aging_history: Dict[str, int] = {}  # sample_id → aged_count
        
    def apply_aging(
        self, 
        samples: List[Sample], 
        current_time: int
    ) -> List[Sample]:
        """
        Applique l'aging aux échantillons en attente.
        
        Équivalent kernel : Augmenter la priorité d'un process qui attend
        """
        if not self.config.enabled:
            return samples
        
        aged_samples = []
        
        for sample in samples:
            wait_time = current_time - sample.ready_time
            original_priority = sample.priority
            
            # ROUTINE → URGENT après seuil
            if (sample.priority == Priority.ROUTINE and 
                wait_time >= self.config.routine_to_urgent):
                
                # Créer copie avec priorité boostée
                aged_sample = Sample(
                    id=sample.id,
                    type=sample.type,
                    priority=Priority.URGENT,  # BOOST !
                    ready_time=sample.ready_time,
                    processing_time=sample.processing_time
                )
                
                self.aging_history[sample.id] = self.aging_history.get(sample.id, 0) + 1
                
                logger.info(
                    f"🔼 AGING: {sample.id} ROUTINE→URGENT "
                    f"(attente: {wait_time} min, seuil: {self.config.routine_to_urgent})"
                )
                
                aged_samples.append(aged_sample)
                continue
            
            # URGENT → STAT (exceptionnel, situations critiques)
            if (sample.priority == Priority.URGENT and 
                wait_time >= self.config.urgent_to_stat):
                
                aged_sample = Sample(
                    id=sample.id,
                    type=sample.type,
                    priority=Priority.STAT,  # BOOST EXCEPTIONNEL !
                    ready_time=sample.ready_time,
                    processing_time=sample.processing_time
                )
                
                self.aging_history[sample.id] = self.aging_history.get(sample.id, 0) + 1
                
                logger.warning(
                    f"🔼🔼 AGING CRITIQUE: {sample.id} URGENT→STAT "
                    f"(attente: {wait_time} min, seuil: {self.config.urgent_to_stat})"
                )
                
                aged_samples.append(aged_sample)
                continue
            
            # Pas d'aging nécessaire
            aged_samples.append(sample)
        
        return aged_samples
    
    def get_stats(self) -> Dict:
        """Statistiques d'aging"""
        return {
            "total_aged_samples": len(self.aging_history),
            "aging_events": sum(self.aging_history.values()),
            "config": {
                "enabled": self.config.enabled,
                "routine_to_urgent_threshold": self.config.routine_to_urgent,
                "urgent_to_stat_threshold": self.config.urgent_to_stat
            }
        }


class DeadlockDetector:
    """
    Détecteur de deadlocks inspiré de l'algorithme de détection de cycles
    
    Construit un wait-for graph et détecte les cycles (deadlocks).
    Équivalent kernel : Banker's algorithm ou cycle detection dans resource allocation graph.
    """
    
    def __init__(self):
        self.detected_deadlocks: List[DeadlockInfo] = []
        self.wait_graph: Dict[str, List[ResourceWaitEdge]] = {}
        
    def build_wait_graph(
        self,
        waiting_samples: List[Sample],
        schedule_entries: List[ScheduleEntry]
    ) -> Dict[str, List[ResourceWaitEdge]]:
        """
        Construit le graphe d'attente (wait-for graph).
        
        Nœuds = échantillons
        Arêtes = S1 → S2 si S1 attend une ressource occupée par S2
        """
        graph: Dict[str, List[ResourceWaitEdge]] = {}
        
        # Map ressource → échantillon qui l'occupe
        resource_owners: Dict[str, str] = {}
        for entry in schedule_entries:
            resource_owners[f"tech_{entry.technician_id}"] = entry.sample_id
            resource_owners[f"equip_{entry.equipment_id}"] = entry.sample_id
        
        # Construire arêtes
        for sample in waiting_samples:
            edges = []
            
            # Chercher ressources nécessaires occupées
            # (Simplification : on suppose qu'on connaît les besoins)
            tech_key = f"tech_{sample.type.value}"
            equip_key = f"equip_{sample.type.value}"
            
            if tech_key in resource_owners:
                edges.append(ResourceWaitEdge(
                    from_sample=sample.id,
                    to_sample=resource_owners[tech_key],
                    resource_type="technician",
                    resource_id=tech_key
                ))
            
            if equip_key in resource_owners:
                edges.append(ResourceWaitEdge(
                    from_sample=sample.id,
                    to_sample=resource_owners[equip_key],
                    resource_type="equipment",
                    resource_id=equip_key
                ))
            
            if edges:
                graph[sample.id] = edges
        
        self.wait_graph = graph
        return graph
    
    def detect_cycles(self) -> List[List[str]]:
        """
        Détecte les cycles dans le wait-for graph (algorithme DFS).
        
        Un cycle = deadlock !
        """
        visited: Set[str] = set()
        rec_stack: Set[str] = set()
        cycles: List[List[str]] = []
        
        def dfs(node: str, path: List[str]) -> bool:
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            if node in self.wait_graph:
                for edge in self.wait_graph[node]:
                    neighbor = edge.to_sample
                    
                    if neighbor not in visited:
                        if dfs(neighbor, path.copy()):
                            return True
                    elif neighbor in rec_stack:
                        # Cycle détecté !
                        cycle_start = path.index(neighbor)
                        cycle = path[cycle_start:] + [neighbor]
                        cycles.append(cycle)
                        logger.error(f"💀 DEADLOCK DÉTECTÉ: {' → '.join(cycle)}")
                        return True
            
            path.pop()
            rec_stack.remove(node)
            return False
        
        for node in self.wait_graph:
            if node not in visited:
                dfs(node, [])
        
        return cycles
    
    def resolve_deadlock(
        self,
        cycle: List[str],
        current_time: int
    ) -> DeadlockInfo:
        """
        Résout un deadlock en libérant une ressource (victim selection).
        
        Stratégie : Tuer l'échantillon ROUTINE avec le moins de temps écoulé.
        """
        # Sélectionner victime (sample à interrompre)
        victim = cycle[0]  # Simplification : premier du cycle
        
        resources_involved = [
            edge.resource_id 
            for edges in self.wait_graph.values() 
            for edge in edges 
            if edge.from_sample in cycle or edge.to_sample in cycle
        ]
        
        deadlock_info = DeadlockInfo(
            cycle=cycle,
            involved_resources=list(set(resources_involved)),
            detection_time=current_time,
            resolution_strategy=f"abort_{victim}"
        )
        
        self.detected_deadlocks.append(deadlock_info)
        
        logger.warning(
            f"🔓 RÉSOLUTION DEADLOCK: Victime={victim}, "
            f"Cycle={' → '.join(cycle)}"
        )
        
        return deadlock_info
    
    def get_stats(self) -> Dict:
        """Statistiques de détection"""
        return {
            "total_deadlocks_detected": len(self.detected_deadlocks),
            "current_wait_graph_size": len(self.wait_graph),
            "deadlocks": [
                {
                    "cycle": dl.cycle,
                    "time": dl.detection_time,
                    "strategy": dl.resolution_strategy
                }
                for dl in self.detected_deadlocks
            ]
        }


class LoadBalancer:
    """
    Load Balancer inspiré du scheduler multi-CPU Linux (SMP)
    
    Distribue équitablement les échantillons entre techniciens pour minimiser
    le déséquilibre de charge (load imbalance).
    """
    
    def __init__(self):
        self.technician_loads: Dict[str, TechnicianLoad] = {}
        self.balance_history: List[Dict] = []
        
    def initialize_loads(self, technicians: List[Technician]):
        """Initialise les structures de tracking de charge"""
        for tech in technicians:
            self.technician_loads[tech.id] = TechnicianLoad(
                technician_id=tech.id
            )
    
    def get_least_loaded_technician(
        self,
        compatible_technicians: List[Technician],
        current_time: int
    ) -> Optional[Technician]:
        """
        Trouve le technicien compatible avec la charge la plus faible.
        
        Équivalent kernel : Trouver le CPU avec le runqueue le plus court.
        """
        if not compatible_technicians:
            return None
        
        # Calculer score de charge pour chaque technicien
        scores = []
        for tech in compatible_technicians:
            load = self.technician_loads.get(tech.id)
            if not load:
                load = TechnicianLoad(technician_id=tech.id)
                self.technician_loads[tech.id] = load
            
            # Score = charge totale + pénalité si indisponible
            availability_penalty = max(0, tech.available_from - current_time) * 2
            score = load.total_duration + availability_penalty
            
            scores.append((tech, score))
        
        # Trier par score croissant
        scores.sort(key=lambda x: x[1])
        
        selected_tech = scores[0][0]
        
        logger.debug(
            f"⚖️ LOAD BALANCING: Sélectionné {selected_tech.id} "
            f"(charge: {scores[0][1]} min, alternatives: {len(scores)-1})"
        )
        
        return selected_tech
    
    def update_load(
        self,
        technician_id: str,
        sample_duration: int,
        start_time: int,
        end_time: int
    ):
        """Met à jour la charge après assignation"""
        load = self.technician_loads.get(technician_id)
        if not load:
            load = TechnicianLoad(technician_id=technician_id)
            self.technician_loads[technician_id] = load
        
        # Calculer idle time
        if load.last_end_time > 0:
            idle = max(0, start_time - load.last_end_time)
            load.idle_time += idle
        
        load.total_duration += sample_duration
        load.sample_count += 1
        load.last_end_time = end_time
    
    def calculate_balance_metrics(self, total_time: int) -> Dict:
        """
        Calcule métriques d'équilibrage de charge.
        
        - Standard deviation : Mesure du déséquilibre
        - Min/Max : Extrêmes de charge
        - Coefficient de variation : Déséquilibre normalisé
        """
        if not self.technician_loads:
            return {}
        
        loads = [load.total_duration for load in self.technician_loads.values()]
        
        avg_load = sum(loads) / len(loads)
        variance = sum((l - avg_load) ** 2 for l in loads) / len(loads)
        std_dev = variance ** 0.5
        
        cv = (std_dev / avg_load * 100) if avg_load > 0 else 0
        
        metrics = {
            "average_load": avg_load,
            "std_deviation": std_dev,
            "min_load": min(loads),
            "max_load": max(loads),
            "load_imbalance": max(loads) - min(loads),
            "coefficient_variation": cv,  # < 15% = excellent balance
            "technician_details": {
                tech_id: {
                    "total_duration": load.total_duration,
                    "sample_count": load.sample_count,
                    "utilization_rate": load.utilization_rate(total_time),
                    "idle_time": load.idle_time,
                    "avg_gap": load.average_gap()
                }
                for tech_id, load in self.technician_loads.items()
            }
        }
        
        self.balance_history.append(metrics)
        
        return metrics
    
    def get_stats(self) -> Dict:
        """Statistiques de load balancing"""
        if not self.balance_history:
            return {"status": "no_data"}
        
        latest = self.balance_history[-1]
        
        return {
            "current_balance": {
                "coefficient_variation": latest["coefficient_variation"],
                "load_imbalance": latest["load_imbalance"],
                "status": "excellent" if latest["coefficient_variation"] < 15 else 
                         "good" if latest["coefficient_variation"] < 30 else "poor"
            },
            "history_size": len(self.balance_history),
            "latest_metrics": latest
        }
