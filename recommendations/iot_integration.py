import asyncio
import json
import paho.mqtt.client as mqtt
from typing import Dict, List, Any, Callable, Optional
import logging
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class IoTDevice:
    device_id: str
    device_type: str
    location: str
    status: str
    last_seen: datetime
    battery_level: Optional[float] = None

@dataclass
class IoTEvent:
    device_id: str
    event_type: str
    timestamp: datetime
    data: Dict[str, Any]
    user_id: Optional[str] = None
    product_id: Optional[str] = None

class IoTIntegrationManager:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.devices = {}
        self.event_handlers = {}
        
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self._on_mqtt_connect
        self.mqtt_client.on_message = self._on_mqtt_message
        self._initialize_mqtt()

    def _initialize_mqtt(self):
        try:
            mqtt_host = self.config.get('mqtt_host', 'localhost')
            mqtt_port = self.config.get('mqtt_port', 1883)
            self.mqtt_client.connect(mqtt_host, mqtt_port, 60)
            self.mqtt_client.loop_start()
            logger.info(f"Connected to MQTT broker at {mqtt_host}:{mqtt_port}")
        except Exception as e:
            logger.error(f"Failed to connect to MQTT broker: {e}")

    def _on_mqtt_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("Successfully connected to MQTT broker")
            client.subscribe("smartcommerce/devices/+/events")
            client.subscribe("smartcommerce/beacons/+/proximity")
        else:
            logger.error(f"Failed to connect to MQTT broker: {rc}")

    def _on_mqtt_message(self, client, userdata, msg):
        try:
            topic_parts = msg.topic.split('/')
            device_id = topic_parts[2]
            event_type = topic_parts[3]
            data = json.loads(msg.payload.decode())
            
            event = IoTEvent(
                device_id=device_id,
                event_type=event_type,
                timestamp=datetime.now(),
                data=data,
                user_id=data.get('user_id'),
                product_id=data.get('product_id')
            )
            
            asyncio.create_task(self._process_iot_event(event))
        except Exception as e:
            logger.error(f"Error processing MQTT message: {e}")

    async def _process_iot_event(self, event: IoTEvent):
        try:
            if event.device_id in self.devices:
                self.devices[event.device_id].last_seen = event.timestamp
            
            if event.event_type in self.event_handlers:
                await self.event_handlers[event.event_type](event)
            else:
                logger.info(f"IoT Event: {event.device_id} - {event.event_type}")
        except Exception as e:
            logger.error(f"Error processing IoT event: {e}")

    def register_device(self, device: IoTDevice):
        self.devices[device.device_id] = device
        logger.info(f"Registered IoT device: {device.device_id} ({device.device_type})")

    def register_event_handler(self, event_type: str, handler: Callable):
        self.event_handlers[event_type] = handler

    async def handle_beacon_proximity(self, event: IoTEvent):
        try:
            user_id = event.user_id
            beacon_data = event.data
            distance = beacon_data.get('distance', 0)
            location = beacon_data.get('location', '')
            
            if user_id and distance < 2.0:
                await self._send_proximity_recommendations(user_id, location, event.device_id)
        except Exception as e:
            logger.error(f"Error handling beacon proximity: {e}")

    async def _send_proximity_recommendations(self, user_id: str, location: str, beacon_id: str):
        try:
            notification_data = {
                'user_id': user_id,
                'type': 'proximity_recommendation',
                'location': location,
                'beacon_id': beacon_id,
                'message': f"Check out great deals near you in {location}!"
            }
            logger.info(f"Proximity notification sent: {notification_data}")
        except Exception as e:
            logger.error(f"Error sending proximity recommendations: {e}")

    def get_device_status(self, device_id: str) -> Optional[IoTDevice]:
        return self.devices.get(device_id)

    async def send_command_to_device(self, device_id: str, command: Dict[str, Any]) -> bool:
        try:
            topic = f"smartcommerce/devices/{device_id}/commands"
            payload = json.dumps(command)
            result = self.mqtt_client.publish(topic, payload)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logger.info(f"Command sent to device {device_id}: {command}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error sending command to device: {e}")
            return False