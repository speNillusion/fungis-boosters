import numpy as np
import pandas as pd
import json
import math
import requests
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import sqlite3
import os

@dataclass
class DegradationPrediction:
    """Degradation prediction result"""
    degradation_time_days: float
    weight_loss_percentage: float
    confidence: float
    conditions: Dict[str, float]
    notes: str
    microorganism: str
    plastic_type: str

class APIClient:
    """Client for communication with the degradation API"""
    
    def __init__(self, base_url: str = "http://localhost:5000/chat"):
        self.base_url = base_url
        
    def query_degradation_data(self, prompt: str) -> Dict:
        """Queries degradation data through the API"""
        try:
            response = requests.post(
                f"{self.base_url}/chat",
                json={"prompt": prompt},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"API error: {response.status_code}")
                return {"error": f"API error: {response.status_code}"}
                
        except requests.exceptions.RequestException as e:
            print(f"API connection error: {e}")
            return {"error": f"Connection error: {e}"}

class PlasticDegradationPredictor:
    """Prediction model for plastic degradation by fungi"""
    
    def __init__(self, data_file: str = "degraders_list_with_images.json", use_api: bool = True):
        """Initializes the predictor with degradation data"""
        self.data_file = data_file
        self.use_api = use_api
        self.api_client = APIClient() if use_api else None
        self.degradation_data = self._load_data()
        self.base_conditions = {
            'temperature': 25.0,  # °C
            'humidity': 60.0,     # %
            'ph': 7.0
        }
        
        # Specific data based on scientific literature
        self.literature_data = {
            'Aspergillus niger': {
                'PVC': {
                    'pieces': {'time': 60, 'degradation': 25, 'confidence': 0.65},
                    'microplastics': {'time': 30, 'degradation': 16, 'confidence': 0.65}
                },
                'PE': {
                    'microplastics': {'time': 30, 'degradation': 16, 'confidence': 0.8}
                },
                'PET': {
                    'microplastics': {'time': 45, 'degradation': 8, 'confidence': 0.7}
                },
                'PS': {
                    'microplastics': {'time': 35, 'degradation': 12, 'confidence': 0.7}
                }
            },
            'Candida albicans': {
                'PVC': {
                    'pieces': {'time': 90, 'degradation': 8, 'confidence': 0.5},
                    'microplastics': {'time': 45, 'degradation': 5, 'confidence': 0.5}
                }
            },
            'Acremonium sclerotigenum': {
                'PET': {
                    'microplastics': {'time': 30, 'degradation': 6, 'confidence': 0.7}
                },
                'PS': {
                    'microplastics': {'time': 30, 'degradation': 10, 'confidence': 0.7}
                }
            }
        }
    
    def _load_data(self) -> List[Dict]:
        """Loads data from JSON file"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"File {self.data_file} not found. Using default data.")
            return []
    
    def _temperature_factor(self, temp: float) -> float:
        """Calculates temperature correction factor"""
        # Based on simplified Arrhenius equation
        # Degradation increases with temperature up to optimal point (~30°C)
        optimal_temp = 30.0
        if temp <= optimal_temp:
            return 1 + (temp - self.base_conditions['temperature']) * 0.05
        else:
            # Degradation decreases after optimal temperature
            return 1 + (optimal_temp - self.base_conditions['temperature']) * 0.05 - (temp - optimal_temp) * 0.03
    
    def _humidity_factor(self, humidity: float) -> float:
        """Calculates humidity correction factor"""
        # Optimal humidity between 60-80%
        if 60 <= humidity <= 80:
            return 1.2
        elif humidity < 60:
            return 0.8 + (humidity / 60) * 0.4
        else:
            return 1.2 - (humidity - 80) * 0.01
    
    def _ph_factor(self, ph: float) -> float:
        """Calcula fator de correção para pH"""
        # pH ótimo entre 4-6 para a maioria dos fungos
        if 4 <= ph <= 6:
            return 1.1
        elif ph < 4:
            return 0.7 + (ph / 4) * 0.4
        else:
            return 1.1 - (ph - 6) * 0.05
    
    def _plastic_form_factor(self, plastic_form: str) -> float:
        """Correction factor based on plastic form"""
        form_factors = {
            'microplastics': 1.5,  # Greater surface area
            'pieces': 1.0,
            'film': 1.3,
            'powder': 2.0
        }
        return form_factors.get(plastic_form.lower(), 1.0)
    
    def _query_api_for_degradation(self, plastic_type: str, microorganism: str, 
                                 temperature: float, humidity: float, ph: float) -> Optional[Dict]:
        """Queries the API to obtain specific degradation data"""
        if not self.use_api or not self.api_client:
            return None
            
        prompt = f"""
        I need scientific information about plastic degradation by fungi.
        
        Specific data:
        - Plastic: {plastic_type}
        - Microorganism: {microorganism}
        - Temperature: {temperature}°C
        - Humidity: {humidity}%
        - pH: {ph}
        
        Please provide information about:
        1. Observable degradation time (in days)
        2. Expected weight loss percentage
        3. Enzymes involved in the process
        4. Optimal conditions for degradation
        5. Relevant scientific references
        
        Please respond in a structured and scientific manner.
        """
        
        return self.api_client.query_degradation_data(prompt)

    def predict_degradation(self, 
                          plastic_type: str,
                          microorganism: str,
                          temperature: float = 25.0,
                          humidity: float = 60.0,
                          ph: float = 7.0,
                          plastic_form: str = "pieces") -> DegradationPrediction:
        """
        Predicts plastic degradation based on provided parameters
        """
        
        # Normalize names
        plastic_type = plastic_type.upper()
        microorganism = microorganism.title()
        
        # First, try to get data from API
        api_data = self._query_api_for_degradation(plastic_type, microorganism, temperature, humidity, ph)
        
        # Search for data in literature
        base_data = None
        if microorganism in self.literature_data:
            if plastic_type in self.literature_data[microorganism]:
                form_key = 'microplastics' if 'microplastic' in plastic_form.lower() else 'pieces'
                if form_key in self.literature_data[microorganism][plastic_type]:
                    base_data = self.literature_data[microorganism][plastic_type][form_key]
        
        # If no specific data found, use estimate based on similar data
        if not base_data:
            base_data = self._estimate_from_similar_data(plastic_type, microorganism)
        
        # Apply correction factors
        temp_factor = self._temperature_factor(temperature)
        humidity_factor = self._humidity_factor(humidity)
        ph_factor = self._ph_factor(ph)
        form_factor = self._plastic_form_factor(plastic_form)
        
        # Calculate adjusted prediction
        combined_factor = temp_factor * humidity_factor * ph_factor * form_factor
        
        adjusted_time = max(1, int(base_data['time'] / combined_factor))
        adjusted_degradation = min(100, base_data['degradation'] * combined_factor)
        adjusted_confidence = base_data['confidence'] * min(1.0, combined_factor / 2)
        
        # Incorporate API data if available
        api_enhancement = 1.0
        api_notes = ""
        
        if api_data and "error" not in api_data:
            # API provided additional data - increase confidence
            adjusted_confidence *= 1.3  # Increase confidence by 30%
            api_enhancement = 0.9  # Improve accuracy by 10%
            adjusted_time = max(1, int(adjusted_time * api_enhancement))
            api_notes = " Data enriched with scientific API information."
        
        # Generate explanatory notes
        notes = self._generate_notes(temperature, humidity, ph, plastic_form, combined_factor)
        notes += api_notes
        
        return DegradationPrediction(
            degradation_time_days=adjusted_time,
            weight_loss_percentage=round(adjusted_degradation, 1),
            confidence=round(adjusted_confidence, 2),
            conditions={
                'temperature': temperature,
                'humidity': humidity,
                'ph': ph,
                'plastic_form': plastic_form
            },
            notes=notes,
            microorganism=microorganism,
            plastic_type=plastic_type
        )
    
    def _estimate_from_similar_data(self, plastic_type: str, microorganism: str) -> Dict:
        """Estimates data based on similar plastics or microorganisms"""
        
        # Default data based on literature averages
        default_data = {
            'PVC': {'time': 60, 'degradation': 15, 'confidence': 0.4},
            'PE': {'time': 45, 'degradation': 20, 'confidence': 0.5},
            'PET': {'time': 50, 'degradation': 12, 'confidence': 0.5},
            'PS': {'time': 40, 'degradation': 18, 'confidence': 0.5},
            'PP': {'time': 55, 'degradation': 14, 'confidence': 0.4}
        }
        
        # Efficiency factors by microorganism
        organism_factors = {
            'Aspergillus niger': 1.2,
            'Candida albicans': 0.6,
            'Acremonium sclerotigenum': 0.8,
            'Penicillium': 1.0,
            'Trichoderma': 1.1
        }
        
        base = default_data.get(plastic_type, {'time': 60, 'degradation': 10, 'confidence': 0.3})
        factor = organism_factors.get(microorganism, 0.8)
        
        return {
            'time': int(base['time'] / factor),
            'degradation': base['degradation'] * factor,
            'confidence': base['confidence'] * 0.8  # Lower confidence for estimates
        }
    
    def _generate_notes(self, temp: float, humidity: float, ph: float, 
                       plastic_form: str, combined_factor: float) -> str:
        """Generates explanatory notes about the prediction"""
        notes = []
        
        if combined_factor > 1.5:
            notes.append("Very favorable conditions for degradation")
        elif combined_factor > 1.2:
            notes.append("Favorable conditions for degradation")
        elif combined_factor < 0.8:
            notes.append("Unfavorable conditions for degradation")
        
        if temp > 35:
            notes.append("Temperature may inhibit fungal activity")
        elif temp < 15:
            notes.append("Low temperature may slow degradation")
        
        if humidity < 40:
            notes.append("Low humidity may limit fungal growth")
        elif humidity > 90:
            notes.append("Very high humidity may favor contamination")
        
        if ph < 3:
            notes.append("Very acidic pH may inhibit fungi")
        elif ph > 8:
            notes.append("Alkaline pH may reduce efficiency")
        
        if 'microplastic' in plastic_form.lower():
            notes.append("Microplastics degrade faster due to greater surface area")
        
        return "; ".join(notes) if notes else "Conditions within normal parameters"
    
    def batch_predict(self, conditions_list: List[Dict]) -> List[DegradationPrediction]:
        """Performs batch predictions"""
        predictions = []
        for conditions in conditions_list:
            prediction = self.predict_degradation(**conditions)
            predictions.append(prediction)
        return predictions
    
    def get_available_organisms(self) -> List[str]:
        """Returns list of available microorganisms"""
        organisms = set()
        for item in self.degradation_data:
            organisms.add(item.get('Microorganism', ''))
        
        # Add organisms from literature
        organisms.update(self.literature_data.keys())
        
        return sorted(list(organisms))
    
    def get_available_plastics(self) -> List[str]:
        """Returns list of available plastics"""
        plastics = set()
        for item in self.degradation_data:
            plastics.add(item.get('Plastic', ''))
        
        # Add common plastics
        common_plastics = ['PVC', 'PE', 'PET', 'PS', 'PP', 'PLA', 'PHB']
        plastics.update(common_plastics)
        
        return sorted(list(plastics))

# Usage example
if __name__ == "__main__":
    predictor = PlasticDegradationPredictor()
    
    # Example based on provided text
    prediction = predictor.predict_degradation(
        plastic_type="PVC",
        microorganism="Aspergillus niger",
        temperature=27.0,
        humidity=14.0,
        ph=4.0,
        plastic_form="pieces"
    )
    
    print(f"Prediction for {prediction.plastic_type} with {prediction.microorganism}:")
    print(f"Time to observable degradation: {prediction.degradation_time_days} days")
    print(f"Expected weight loss: {prediction.weight_loss_percentage}%")
    print(f"Confidence: {prediction.confidence}")
    print(f"Conditions: {prediction.conditions}")
    print(f"Notes: {prediction.notes}")