import hashlib
import random
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json
import logging
from datetime import datetime, timedelta
import numpy as np
from scipy import stats
import pandas as pd
from collections import defaultdict

logger = logging.getLogger(__name__)

class ExperimentStatus(Enum):
    DRAFT = "draft"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    STOPPED = "stopped"

@dataclass
class ExperimentConfig:
    """A/B test experiment configuration"""
    experiment_id: str
    name: str
    description: str
    variants: List[Dict[str, Any]]
    traffic_allocation: Dict[str, float]
    start_date: datetime
    end_date: datetime
    success_metrics: List[str]
    minimum_sample_size: int
    confidence_level: float = 0.95
    status: ExperimentStatus = ExperimentStatus.DRAFT

class ABTestingFramework:
    """Advanced A/B testing framework for recommendations"""
    
    def __init__(self, redis_client, config: Dict[str, Any]):
        self.redis_client = redis_client
        self.config = config
        self.experiments = {}
        self.experiment_assignments = defaultdict(dict)
        
    def create_experiment(self, config: ExperimentConfig) -> Dict[str, Any]:
        """Create a new A/B test experiment"""
        
        # Validate configuration
        validation_result = self._validate_experiment_config(config)
        if not validation_result['valid']:
            return validation_result
        
        # Store experiment configuration
        self.experiments[config.experiment_id] = config
        
        # Store in Redis
        experiment_key = f"experiment:{config.experiment_id}"
        self.redis_client.hset(experiment_key, mapping={
            'config': json.dumps(config.__dict__, default=str),
            'status': config.status.value,
            'created_at': datetime.now().isoformat()
        })
        
        logger.info(f"Created experiment: {config.experiment_id}")
        
        return {
            'success': True,
            'experiment_id': config.experiment_id,
            'message': 'Experiment created successfully'
        }
    
    def _validate_experiment_config(self, config: ExperimentConfig) -> Dict[str, Any]:
        """Validate experiment configuration"""
        
        errors = []
        
        # Check variant allocation sums to 1.0
        total_allocation = sum(config.traffic_allocation.values())
        if abs(total_allocation - 1.0) > 0.001:
            errors.append(f"Traffic allocation must sum to 1.0, got {total_allocation}")
        
        # Check variants are defined
        variant_names = set(config.traffic_allocation.keys())
        config_variants = set(v['name'] for v in config.variants)
        if variant_names != config_variants:
            errors.append("Variant names in allocation don't match variant definitions")
        
        # Check dates
        if config.start_date >= config.end_date:
            errors.append("Start date must be before end date")
        
        if errors:
            return {
                'valid': False,
                'errors': errors
            }
        
        return {'valid': True}
    
    def assign_user_to_variant(self, user_id: str, experiment_id: str) -> str:
        """Assign user to experiment variant"""
        
        # Check if user already assigned
        if user_id in self.experiment_assignments.get(experiment_id, {}):
            return self.experiment_assignments[experiment_id][user_id]
        
        experiment = self.experiments.get(experiment_id)
        if not experiment or experiment.status != ExperimentStatus.RUNNING:
            return 'control'  # Default variant
        
        # Check if experiment is active
        now = datetime.now()
        if now < experiment.start_date or now > experiment.end_date:
            return 'control'
        
        # Hash-based assignment for consistency
        hash_input = f"{user_id}:{experiment_id}:{experiment.start_date}"
        hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
        assignment_value = (hash_value % 10000) / 10000.0
        
        # Determine variant based on traffic allocation
        cumulative_allocation = 0.0
        for variant_name, allocation in experiment.traffic_allocation.items():
            cumulative_allocation += allocation
            if assignment_value <= cumulative_allocation:
                # Cache assignment
                if experiment_id not in self.experiment_assignments:
                    self.experiment_assignments[experiment_id] = {}
                self.experiment_assignments[experiment_id][user_id] = variant_name
                
                # Store in Redis
                assignment_key = f"assignment:{experiment_id}:{user_id}"
                self.redis_client.setex(assignment_key, 86400, variant_name)
                
                return variant_name
        
        return 'control'  # Fallback
    
    def get_variant_config(self, experiment_id: str, variant_name: str) -> Dict[str, Any]:
        """Get configuration for a specific variant"""
        
        experiment = self.experiments.get(experiment_id)
        if not experiment:
            return {}
        
        for variant in experiment.variants:
            if variant['name'] == variant_name:
                return variant.get('config', {})
        
        return {}
    
    def track_experiment_event(self, user_id: str, experiment_id: str, 
                              event_type: str, value: float = 1.0) -> bool:
        """Track an event for experiment analysis"""
        
        variant = self.assign_user_to_variant(user_id, experiment_id)
        
        # Store event
        event_key = f"experiment_events:{experiment_id}:{variant}:{event_type}"
        
        event_data = {
            'user_id': user_id,
            'variant': variant,
            'event_type': event_type,
            'value': value,
            'timestamp': datetime.now().isoformat()
        }
        
        # Add to Redis list
        self.redis_client.lpush(event_key, json.dumps(event_data))
        
        # Keep only recent events (last 10000)
        self.redis_client.ltrim(event_key, 0, 9999)
        
        return True
    
    def analyze_experiment(self, experiment_id: str) -> Dict[str, Any]:
        """Analyze experiment results"""
        
        experiment = self.experiments.get(experiment_id)
        if not experiment:
            return {'error': 'Experiment not found'}
        
        results = {}
        
        for metric in experiment.success_metrics:
            metric_results = self._analyze_metric(experiment_id, metric)
            results[metric] = metric_results
        
        # Calculate overall experiment results
        overall_results = self._calculate_overall_results(results)
        
        return {
            'experiment_id': experiment_id,
            'status': experiment.status.value,
            'results': results,
            'overall': overall_results,
            'analyzed_at': datetime.now().isoformat()
        }
    
    def _analyze_metric(self, experiment_id: str, metric: str) -> Dict[str, Any]:
        """Analyze a specific metric for the experiment"""
        
        experiment = self.experiments.get(experiment_id)
        variant_results = {}
        
        for variant in experiment.variants:
            variant_name = variant['name']
            
            # Get events for this variant and metric
            event_key = f"experiment_events:{experiment_id}:{variant_name}:{metric}"
            events = self.redis_client.lrange(event_key, 0, -1)
            
            values = []
            for event_json in events:
                try:
                    event = json.loads(event_json)
                    values.append(event['value'])
                except:
                    continue
            
            if values:
                variant_results[variant_name] = {
                    'sample_size': len(values),
                    'mean': np.mean(values),
                    'std': np.std(values),
                    'sum': sum(values),
                    'values': values
                }
            else:
                variant_results[variant_name] = {
                    'sample_size': 0,
                    'mean': 0,
                    'std': 0,
                    'sum': 0,
                    'values': []
                }
        
        # Statistical analysis
        statistical_results = self._perform_statistical_analysis(variant_results)
        
        return {
            'metric': metric,
            'variants': variant_results,
            'statistics': statistical_results
        }
    
    def _perform_statistical_analysis(self, variant_results: Dict[str, Any]) -> Dict[str, Any]:
        """Perform statistical analysis on variant results"""
        
        if len(variant_results) < 2:
            return {'error': 'Need at least 2 variants for comparison'}
        
        # Get control and treatment groups
        variant_names = list(variant_results.keys())
        control_name = 'control' if 'control' in variant_names else variant_names[0]
        
        control_data = variant_results[control_name]
        
        statistical_results = {}
        
        for variant_name, variant_data in variant_results.items():
            if variant_name == control_name:
                continue
            
            # Perform t-test
            if (control_data['sample_size'] > 0 and variant_data['sample_size'] > 0 and
                control_data['values'] and variant_data['values']):
                
                t_stat, p_value = stats.ttest_ind(
                    control_data['values'],
                    variant_data['values']
                )
                
                # Calculate confidence interval for difference in means
                control_mean = control_data['mean']
                variant_mean = variant_data['mean']
                
                # Calculate lift
                lift = (variant_mean - control_mean) / control_mean if control_mean > 0 else 0
                
                # Determine significance
                is_significant = p_value < (1 - 0.95)  # 95% confidence
                
                statistical_results[variant_name] = {
                    't_statistic': t_stat,
                    'p_value': p_value,
                    'is_significant': is_significant,
                    'lift': lift,
                    'control_mean': control_mean,
                    'variant_mean': variant_mean,
                    'difference': variant_mean - control_mean
                }
            else:
                statistical_results[variant_name] = {
                    'error': 'Insufficient data for statistical analysis'
                }
        
        return statistical_results
    
    def _calculate_overall_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall experiment results"""
        
        total_significant = 0
        total_metrics = len(results)
        best_variant = None
        best_lift = 0
        
        for metric, metric_results in results.items():
            stats_results = metric_results.get('statistics', {})
            
            for variant, stats in stats_results.items():
                if isinstance(stats, dict) and stats.get('is_significant', False):
                    total_significant += 1
                    
                    lift = stats.get('lift', 0)
                    if abs(lift) > abs(best_lift):
                        best_lift = lift
                        best_variant = variant
        
        return {
            'significant_metrics': total_significant,
            'total_metrics': total_metrics,
            'significance_rate': total_significant / total_metrics if total_metrics > 0 else 0,
            'best_variant': best_variant,
            'best_lift': best_lift,
            'recommendation': self._get_experiment_recommendation(results)
        }
    
    def _get_experiment_recommendation(self, results: Dict[str, Any]) -> str:
        """Get recommendation based on experiment results"""
        
        significant_improvements = 0
        total_comparisons = 0
        
        for metric_results in results.values():
            stats_results = metric_results.get('statistics', {})
            
            for variant_stats in stats_results.values():
                if isinstance(variant_stats, dict):
                    total_comparisons += 1
                    if (variant_stats.get('is_significant', False) and 
                        variant_stats.get('lift', 0) > 0):
                        significant_improvements += 1
        
        if significant_improvements > total_comparisons * 0.5:
            return "IMPLEMENT - Significant positive results"
        elif significant_improvements > 0:
            return "CONTINUE - Some positive results, need more data"
        else:
            return "STOP - No significant improvements detected"
    
    def start_experiment(self, experiment_id: str) -> Dict[str, Any]:
        """Start an experiment"""
        
        experiment = self.experiments.get(experiment_id)
        if not experiment:
            return {'success': False, 'error': 'Experiment not found'}
        
        experiment.status = ExperimentStatus.RUNNING
        
        # Update in Redis
        experiment_key = f"experiment:{experiment_id}"
        self.redis_client.hset(experiment_key, 'status', experiment.status.value)
        
        logger.info(f"Started experiment: {experiment_id}")
        
        return {'success': True, 'message': 'Experiment started'}
    
    def stop_experiment(self, experiment_id: str) -> Dict[str, Any]:
        """Stop an experiment"""
        
        experiment = self.experiments.get(experiment_id)
        if not experiment:
            return {'success': False, 'error': 'Experiment not found'}
        
        experiment.status = ExperimentStatus.COMPLETED
        
        # Update in Redis
        experiment_key = f"experiment:{experiment_id}"
        self.redis_client.hset(experiment_key, 'status', experiment.status.value)
        
        # Generate final analysis
        final_results = self.analyze_experiment(experiment_id)
        
        logger.info(f"Stopped experiment: {experiment_id}")
        
        return {
            'success': True,
            'message': 'Experiment stopped',
            'final_results': final_results
        }