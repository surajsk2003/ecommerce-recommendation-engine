import hashlib
import json
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@dataclass
class SupplyChainEvent:
    event_id: str
    product_id: str
    event_type: str
    timestamp: datetime
    location: str
    actor: str
    metadata: Dict[str, Any]
    hash: Optional[str] = None

@dataclass
class ProductAuthenticity:
    product_id: str
    authentic: bool
    confidence_score: float
    verification_method: str
    blockchain_hash: str
    verification_timestamp: datetime

class BlockchainSupplyChain:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.supply_chain_events = {}
        self.product_authenticity = {}

    async def track_product_event(self, event: SupplyChainEvent) -> bool:
        try:
            event.hash = self._calculate_event_hash(event)
            
            if event.product_id not in self.supply_chain_events:
                self.supply_chain_events[event.product_id] = []
            
            self.supply_chain_events[event.product_id].append(event)
            logger.info(f"Supply chain event tracked: {event.event_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to track supply chain event: {e}")
            return False

    def _calculate_event_hash(self, event: SupplyChainEvent) -> str:
        event_data = {
            'event_id': event.event_id,
            'product_id': event.product_id,
            'event_type': event.event_type,
            'timestamp': event.timestamp.isoformat(),
            'location': event.location,
            'actor': event.actor,
            'metadata': event.metadata
        }
        event_json = json.dumps(event_data, sort_keys=True)
        return hashlib.sha256(event_json.encode()).hexdigest()

    async def verify_product_authenticity(self, product_id: str) -> ProductAuthenticity:
        try:
            events = self.supply_chain_events.get(product_id, [])
            
            if not events:
                return ProductAuthenticity(
                    product_id=product_id,
                    authentic=False,
                    confidence_score=0.0,
                    verification_method='no_data',
                    blockchain_hash='',
                    verification_timestamp=datetime.now()
                )

            chain_valid = self._verify_hash_chain(events)
            confidence_score = 0.8 if chain_valid else 0.2
            latest_hash = events[-1].hash if events else ''

            authenticity = ProductAuthenticity(
                product_id=product_id,
                authentic=chain_valid and confidence_score > 0.7,
                confidence_score=confidence_score,
                verification_method='blockchain_supply_chain',
                blockchain_hash=latest_hash,
                verification_timestamp=datetime.now()
            )

            self.product_authenticity[product_id] = authenticity
            return authenticity
        except Exception as e:
            logger.error(f"Failed to verify product authenticity: {e}")
            return ProductAuthenticity(
                product_id=product_id,
                authentic=False,
                confidence_score=0.0,
                verification_method='error',
                blockchain_hash='',
                verification_timestamp=datetime.now()
            )

    def _verify_hash_chain(self, events: List[SupplyChainEvent]) -> bool:
        try:
            for event in events:
                calculated_hash = self._calculate_event_hash(event)
                if calculated_hash != event.hash:
                    return False
            return True
        except Exception as e:
            logger.error(f"Error verifying hash chain: {e}")
            return False

    async def get_supply_chain_history(self, product_id: str) -> List[Dict[str, Any]]:
        try:
            events = self.supply_chain_events.get(product_id, [])
            return [{
                'event_id': event.event_id,
                'event_type': event.event_type,
                'timestamp': event.timestamp.isoformat(),
                'location': event.location,
                'actor': event.actor,
                'hash': event.hash
            } for event in sorted(events, key=lambda x: x.timestamp)]
        except Exception as e:
            logger.error(f"Error getting supply chain history: {e}")
            return []