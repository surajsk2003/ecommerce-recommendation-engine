from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import logging
import asyncio
from .computer_vision_engine import AdvancedComputerVisionEngine
from .blockchain_integration import BlockchainSupplyChain, SupplyChainEvent
from .iot_integration import IoTIntegrationManager, IoTDevice
from datetime import datetime
import json

logger = logging.getLogger(__name__)

# Initialize services
cv_engine = AdvancedComputerVisionEngine()
blockchain_config = {'blockchain_provider_url': 'http://localhost:8545'}
blockchain_service = BlockchainSupplyChain(blockchain_config)
iot_config = {'mqtt_host': 'localhost', 'mqtt_port': 1883}
iot_manager = IoTIntegrationManager(iot_config)

@api_view(['POST'])
def visual_search(request):
    """Visual search using computer vision"""
    try:
        if 'image' not in request.FILES:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        image_file = request.FILES['image']
        image_data = image_file.read()
        
        # Analyze image
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        analysis_result = loop.run_until_complete(cv_engine.analyze_image(image_data))
        
        # Find similar products
        if 'embedding' in analysis_result:
            similar_products = loop.run_until_complete(
                cv_engine.find_similar_products(analysis_result['embedding'])
            )
            analysis_result['similar_products'] = similar_products
        
        return Response(analysis_result)
    except Exception as e:
        logger.error(f"Error in visual search: {e}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def track_supply_chain(request):
    """Track supply chain event on blockchain"""
    try:
        data = request.data
        event = SupplyChainEvent(
            event_id=data['event_id'],
            product_id=data['product_id'],
            event_type=data['event_type'],
            timestamp=datetime.fromisoformat(data['timestamp']),
            location=data['location'],
            actor=data['actor'],
            metadata=data.get('metadata', {})
        )
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        success = loop.run_until_complete(blockchain_service.track_product_event(event))
        
        return Response({'success': success, 'event_hash': event.hash})
    except Exception as e:
        logger.error(f"Error tracking supply chain: {e}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def verify_authenticity(request, product_id):
    """Verify product authenticity using blockchain"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        authenticity = loop.run_until_complete(
            blockchain_service.verify_product_authenticity(product_id)
        )
        
        return Response({
            'product_id': authenticity.product_id,
            'authentic': authenticity.authentic,
            'confidence_score': authenticity.confidence_score,
            'verification_method': authenticity.verification_method,
            'blockchain_hash': authenticity.blockchain_hash,
            'verification_timestamp': authenticity.verification_timestamp.isoformat()
        })
    except Exception as e:
        logger.error(f"Error verifying authenticity: {e}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def register_iot_device(request):
    """Register IoT device"""
    try:
        data = request.data
        device = IoTDevice(
            device_id=data['device_id'],
            device_type=data['device_type'],
            location=data['location'],
            status=data.get('status', 'active'),
            last_seen=datetime.now(),
            battery_level=data.get('battery_level')
        )
        
        iot_manager.register_device(device)
        return Response({'success': True, 'message': 'Device registered successfully'})
    except Exception as e:
        logger.error(f"Error registering IoT device: {e}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def iot_device_status(request, device_id):
    """Get IoT device status"""
    try:
        device = iot_manager.get_device_status(device_id)
        if device:
            return Response({
                'device_id': device.device_id,
                'device_type': device.device_type,
                'location': device.location,
                'status': device.status,
                'last_seen': device.last_seen.isoformat(),
                'battery_level': device.battery_level
            })
        else:
            return Response({'error': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error getting device status: {e}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def supply_chain_history(request, product_id):
    """Get supply chain history"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        history = loop.run_until_complete(
            blockchain_service.get_supply_chain_history(product_id)
        )
        return Response({'product_id': product_id, 'history': history})
    except Exception as e:
        logger.error(f"Error getting supply chain history: {e}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)