"""
Forensic Analysis Module - OpenCV-based evidence processing
"""

import cv2
import numpy as np
import pygame
from typing import Dict, List, Tuple, Optional

class ForensicAnalyzer:
    def __init__(self):
        self.evidence_cache = {}
        self.analysis_results = {}
    
    def enhance_image(self, image_path: str) -> Dict:
        """
        Enhance a blurry security camera image
        Returns analysis results and enhanced image
        """
        try:
            # Load image
            img = cv2.imread(image_path)
            if img is None:
                return {"error": "Could not load image"}
            
            # Store original
            original = img.copy()
            
            # Enhancement pipeline
            enhanced = self._apply_enhancement_pipeline(img)
            
            # Face detection
            faces = self._detect_faces(enhanced)
            
            # Fingerprint analysis (simulated)
            fingerprints = self._analyze_fingerprints(enhanced)
            
            return {
                "original": original,
                "enhanced": enhanced,
                "faces_detected": len(faces),
                "face_locations": faces,
                "fingerprints": fingerprints,
                "enhancement_score": self._calculate_enhancement_score(original, enhanced)
            }
        
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _apply_enhancement_pipeline(self, img: np.ndarray) -> np.ndarray:
        """Apply image enhancement techniques"""
        # Convert to grayscale for processing
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Noise reduction
        denoised = cv2.fastNlMeansDenoising(gray)
        
        # Contrast enhancement using CLAHE
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        enhanced = clahe.apply(denoised)
        
        # Sharpening kernel
        kernel = np.array([[-1,-1,-1],
                          [-1, 9,-1],
                          [-1,-1,-1]])
        sharpened = cv2.filter2D(enhanced, -1, kernel)
        
        # Convert back to BGR for display
        result = cv2.cvtColor(sharpened, cv2.COLOR_GRAY2BGR)
        
        return result
    
    def _detect_faces(self, img: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """Detect faces in the enhanced image"""
        try:
            # Load face cascade (you'll need to download this)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            return [(x, y, w, h) for (x, y, w, h) in faces]
        
        except Exception:
            # Fallback: simulate face detection
            return [(100, 100, 80, 80)] if np.random.random() > 0.3 else []
    
    def _analyze_fingerprints(self, img: np.ndarray) -> Dict:
        """Simulate fingerprint analysis"""
        # This is a simulation - real fingerprint analysis would be much more complex
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Look for ridge-like patterns
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Simulate fingerprint quality based on contour analysis
        quality_score = min(len(contours) / 100.0, 1.0)
        
        return {
            "quality_score": quality_score,
            "ridge_count": len(contours),
            "match_probability": quality_score * 0.8 if quality_score > 0.3 else 0.0
        }
    
    def _calculate_enhancement_score(self, original: np.ndarray, enhanced: np.ndarray) -> float:
        """Calculate how much the image was improved"""
        # Simple metric based on contrast improvement
        orig_std = np.std(cv2.cvtColor(original, cv2.COLOR_BGR2GRAY))
        enh_std = np.std(cv2.cvtColor(enhanced, cv2.COLOR_BGR2GRAY))
        
        improvement = (enh_std - orig_std) / orig_std if orig_std > 0 else 0
        return max(0.0, min(1.0, improvement))
    
    def pygame_surface_from_cv2(self, cv2_image: np.ndarray) -> pygame.Surface:
        """Convert OpenCV image to Pygame surface"""
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
        # Rotate for pygame
        rgb_image = np.rot90(rgb_image)
        rgb_image = np.flipud(rgb_image)
        
        return pygame.surfarray.make_surface(rgb_image)

class EvidenceGraph:
    """Manages the logical connections between evidence pieces"""
    
    def __init__(self):
        self.evidence_nodes = {}
        self.connections = []
        self.deduction_score = 0
    
    def add_evidence(self, evidence_id: str, evidence_type: str, description: str, location: str):
        """Add a piece of evidence to the graph"""
        self.evidence_nodes[evidence_id] = {
            "type": evidence_type,
            "description": description,
            "location": location,
            "connected_to": [],
            "analyzed": False
        }
    
    def connect_evidence(self, evidence1_id: str, evidence2_id: str, connection_type: str) -> bool:
        """Connect two pieces of evidence with a logical relationship"""
        if evidence1_id in self.evidence_nodes and evidence2_id in self.evidence_nodes:
            connection = {
                "from": evidence1_id,
                "to": evidence2_id,
                "type": connection_type,
                "strength": self._calculate_connection_strength(evidence1_id, evidence2_id, connection_type)
            }
            
            self.connections.append(connection)
            self.evidence_nodes[evidence1_id]["connected_to"].append(evidence2_id)
            self.evidence_nodes[evidence2_id]["connected_to"].append(evidence1_id)
            
            self._update_deduction_score()
            return True
        
        return False
    
    def _calculate_connection_strength(self, ev1_id: str, ev2_id: str, connection_type: str) -> float:
        """Calculate how strong the logical connection is"""
        ev1 = self.evidence_nodes[ev1_id]
        ev2 = self.evidence_nodes[ev2_id]
        
        # Base strength based on connection type
        type_strengths = {
            "location_match": 0.8,
            "time_correlation": 0.7,
            "physical_match": 0.9,
            "witness_testimony": 0.6,
            "forensic_match": 0.95
        }
        
        base_strength = type_strengths.get(connection_type, 0.5)
        
        # Modify based on evidence types
        if ev1["type"] == "forensic" or ev2["type"] == "forensic":
            base_strength *= 1.2
        
        return min(1.0, base_strength)
    
    def _update_deduction_score(self):
        """Update the overall deduction score based on evidence connections"""
        if not self.connections:
            self.deduction_score = 0
            return
        
        total_strength = sum(conn["strength"] for conn in self.connections)
        connection_bonus = len(self.connections) * 0.1
        
        self.deduction_score = min(100, (total_strength * 10) + connection_bonus)
    
    def get_deduction_paths(self) -> List[List[str]]:
        """Find logical paths through the evidence"""
        paths = []
        visited = set()
        
        for evidence_id in self.evidence_nodes:
            if evidence_id not in visited:
                path = self._dfs_path(evidence_id, visited.copy())
                if len(path) > 1:
                    paths.append(path)
        
        return paths
    
    def _dfs_path(self, start_id: str, visited: set) -> List[str]:
        """Depth-first search to find evidence paths"""
        if start_id in visited:
            return []
        
        visited.add(start_id)
        path = [start_id]
        
        for connected_id in self.evidence_nodes[start_id]["connected_to"]:
            if connected_id not in visited:
                sub_path = self._dfs_path(connected_id, visited.copy())
                if sub_path:
                    path.extend(sub_path)
                    break
        
        return path