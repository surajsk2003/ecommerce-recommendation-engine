import cv2
import numpy as np
import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50
from sklearn.metrics.pairwise import cosine_similarity
import tensorflow as tf
from PIL import Image
import logging
from dataclasses import dataclass
from typing import List, Dict, Tuple, Any, Optional
import asyncio

logger = logging.getLogger(__name__)

@dataclass
class DetectedObject:
    label: str
    confidence: float
    bbox: Tuple[int, int, int, int]
    features: np.ndarray
    color_palette: List[str]

class AdvancedComputerVisionEngine:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.resnet_model = resnet50(pretrained=True).to(self.device)
        self.resnet_model.eval()
        self.color_detector = ColorAnalyzer()
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        self.product_embeddings = {}

    async def analyze_image(self, image_data: bytes) -> Dict[str, Any]:
        try:
            image = Image.open(io.BytesIO(image_data)).convert('RGB')
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            features = await self._extract_features(image)
            colors = await self._analyze_colors(cv_image)
            
            return {
                'features': features,
                'colors': colors,
                'embedding': features,
                'search_tags': self._generate_search_tags([colors])
            }
        except Exception as e:
            logger.error(f"Error analyzing image: {e}")
            return {}

    async def _extract_features(self, image: Image.Image) -> np.ndarray:
        try:
            image_tensor = self.transform(image).unsqueeze(0).to(self.device)
            with torch.no_grad():
                features = self.resnet_model.features(image_tensor)
                features = torch.nn.functional.adaptive_avg_pool2d(features, (1, 1))
                features = features.view(features.size(0), -1)
                return features.cpu().numpy().flatten()
        except Exception as e:
            logger.error(f"Error extracting features: {e}")
            return np.zeros(2048)

    async def _analyze_colors(self, image: np.ndarray) -> Dict[str, Any]:
        return self.color_detector.analyze_colors(image)

    def _generate_search_tags(self, analysis_results: List[Any]) -> List[str]:
        tags = set()
        if analysis_results and analysis_results[0]:
            if 'dominant_colors' in analysis_results[0]:
                tags.update(analysis_results[0]['dominant_colors'])
        return list(tags)

    async def find_similar_products(self, query_embedding: np.ndarray, top_k: int = 10) -> List[Dict[str, Any]]:
        try:
            if not self.product_embeddings:
                return []
            
            similarities = []
            for product_id, embedding in self.product_embeddings.items():
                similarity = cosine_similarity(
                    query_embedding.reshape(1, -1), 
                    embedding.reshape(1, -1)
                )[0][0]
                similarities.append((product_id, similarity))
            
            similarities.sort(key=lambda x: x[1], reverse=True)
            return [{'product_id': product_id, 'similarity_score': score} for product_id, score in similarities[:top_k]]
        except Exception as e:
            logger.error(f"Error finding similar products: {e}")
            return []

class ColorAnalyzer:
    def __init__(self):
        self.color_names = {
            (255, 0, 0): 'red', (0, 255, 0): 'green', (0, 0, 255): 'blue',
            (255, 255, 0): 'yellow', (255, 0, 255): 'magenta', (0, 255, 255): 'cyan',
            (255, 255, 255): 'white', (0, 0, 0): 'black', (128, 128, 128): 'gray'
        }

    def analyze_colors(self, image: np.ndarray) -> Dict[str, Any]:
        try:
            dominant_colors = self.extract_dominant_colors(image, k=5)
            return {'dominant_colors': dominant_colors}
        except Exception as e:
            logger.error(f"Error in color analysis: {e}")
            return {}

    def extract_dominant_colors(self, image: np.ndarray, k: int = 5) -> List[str]:
        try:
            from sklearn.cluster import KMeans
            pixels = image.reshape(-1, 3)
            kmeans = KMeans(n_clusters=min(k, len(pixels)), random_state=42, n_init=10)
            kmeans.fit(pixels)
            colors = kmeans.cluster_centers_.astype(int)
            return [self._rgb_to_color_name(tuple(color)) for color in colors]
        except Exception as e:
            logger.error(f"Error extracting dominant colors: {e}")
            return ['unknown']

    def _rgb_to_color_name(self, rgb: Tuple[int, int, int]) -> str:
        min_distance = float('inf')
        closest_color = 'unknown'
        for known_rgb, color_name in self.color_names.items():
            distance = sum((a - b) ** 2 for a, b in zip(rgb, known_rgb)) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_color = color_name
        return closest_color