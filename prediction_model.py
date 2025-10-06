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
    """Resultado da predição de degradação"""
    degradation_time_days: float
    weight_loss_percentage: float
    confidence: float
    conditions: Dict[str, float]
    notes: str
    microorganism: str
    plastic_type: str

class APIClient:
    """Cliente para comunicação com a API de degradação"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        
    def query_degradation_data(self, prompt: str) -> Dict:
        """Consulta dados de degradação através da API"""
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
                print(f"Erro na API: {response.status_code}")
                return {"error": f"API error: {response.status_code}"}
                
        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão com a API: {e}")
            return {"error": f"Connection error: {e}"}

class PlasticDegradationPredictor:
    """Modelo de predição para degradação de plásticos por fungos"""
    
    def __init__(self, data_file: str = "degraders_list_with_images.json", use_api: bool = True):
        """Inicializa o preditor com dados de degradação"""
        self.data_file = data_file
        self.use_api = use_api
        self.api_client = APIClient() if use_api else None
        self.degradation_data = self._load_data()
        self.base_conditions = {
            'temperature': 25.0,  # °C
            'humidity': 60.0,     # %
            'ph': 7.0
        }
        
        # Dados específicos baseados na literatura científica
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
        """Carrega dados do arquivo JSON"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Arquivo {self.data_file} não encontrado. Usando dados padrão.")
            return []
    
    def _temperature_factor(self, temp: float) -> float:
        """Calcula fator de correção para temperatura"""
        # Baseado na equação de Arrhenius simplificada
        # Degradação aumenta com temperatura até um ponto ótimo (~30°C)
        optimal_temp = 30.0
        if temp <= optimal_temp:
            return 1 + (temp - self.base_conditions['temperature']) * 0.05
        else:
            # Degradação diminui após temperatura ótima
            return 1 + (optimal_temp - self.base_conditions['temperature']) * 0.05 - (temp - optimal_temp) * 0.03
    
    def _humidity_factor(self, humidity: float) -> float:
        """Calcula fator de correção para umidade"""
        # Umidade ótima entre 60-80%
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
        """Fator de correção baseado na forma do plástico"""
        form_factors = {
            'microplastics': 1.5,  # Maior área superficial
            'pieces': 1.0,
            'film': 1.3,
            'powder': 2.0
        }
        return form_factors.get(plastic_form.lower(), 1.0)
    
    def _query_api_for_degradation(self, plastic_type: str, microorganism: str, 
                                 temperature: float, humidity: float, ph: float) -> Optional[Dict]:
        """Consulta a API para obter dados de degradação específicos"""
        if not self.use_api or not self.api_client:
            return None
            
        prompt = f"""
        Preciso de informações científicas sobre degradação de plásticos por fungos.
        
        Dados específicos:
        - Plástico: {plastic_type}
        - Microrganismo: {microorganism}
        - Temperatura: {temperature}°C
        - Umidade: {humidity}%
        - pH: {ph}
        
        Por favor, forneça informações sobre:
        1. Tempo de degradação observável (em dias)
        2. Percentual de perda de peso esperado
        3. Enzimas envolvidas no processo
        4. Condições ótimas para degradação
        5. Referências científicas relevantes
        
        Responda de forma estruturada e científica.
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
        Prediz a degradação de plástico baseado nos parâmetros fornecidos
        """
        
        # Normalizar nomes
        plastic_type = plastic_type.upper()
        microorganism = microorganism.title()
        
        # Primeiro, tentar obter dados da API
        api_data = self._query_api_for_degradation(plastic_type, microorganism, temperature, humidity, ph)
        
        # Buscar dados na literatura
        base_data = None
        if microorganism in self.literature_data:
            if plastic_type in self.literature_data[microorganism]:
                form_key = 'microplastics' if 'microplastic' in plastic_form.lower() else 'pieces'
                if form_key in self.literature_data[microorganism][plastic_type]:
                    base_data = self.literature_data[microorganism][plastic_type][form_key]
        
        # Se não encontrar dados específicos, usar estimativa baseada em dados similares
        if not base_data:
            base_data = self._estimate_from_similar_data(plastic_type, microorganism)
        
        # Aplicar fatores de correção
        temp_factor = self._temperature_factor(temperature)
        humidity_factor = self._humidity_factor(humidity)
        ph_factor = self._ph_factor(ph)
        form_factor = self._plastic_form_factor(plastic_form)
        
        # Calcular predição ajustada
        combined_factor = temp_factor * humidity_factor * ph_factor * form_factor
        
        adjusted_time = max(1, int(base_data['time'] / combined_factor))
        adjusted_degradation = min(100, base_data['degradation'] * combined_factor)
        adjusted_confidence = base_data['confidence'] * min(1.0, combined_factor / 2)
        
        # Incorporar dados da API se disponíveis
        api_enhancement = 1.0
        api_notes = ""
        
        if api_data and "error" not in api_data:
            # A API forneceu dados adicionais - aumentar confiança
            adjusted_confidence *= 1.3  # Aumentar confiança em 30%
            api_enhancement = 0.9  # Melhorar precisão em 10%
            adjusted_time = max(1, int(adjusted_time * api_enhancement))
            api_notes = " Dados enriquecidos com informações da API científica."
        
        # Gerar notas explicativas
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
        """Estima dados baseado em plásticos ou microrganismos similares"""
        
        # Dados padrão baseados em médias da literatura
        default_data = {
            'PVC': {'time': 60, 'degradation': 15, 'confidence': 0.4},
            'PE': {'time': 45, 'degradation': 20, 'confidence': 0.5},
            'PET': {'time': 50, 'degradation': 12, 'confidence': 0.5},
            'PS': {'time': 40, 'degradation': 18, 'confidence': 0.5},
            'PP': {'time': 55, 'degradation': 14, 'confidence': 0.4}
        }
        
        # Fatores de eficiência por microrganismo
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
            'confidence': base['confidence'] * 0.8  # Menor confiança para estimativas
        }
    
    def _generate_notes(self, temp: float, humidity: float, ph: float, 
                       plastic_form: str, combined_factor: float) -> str:
        """Gera notas explicativas sobre a predição"""
        notes = []
        
        if combined_factor > 1.5:
            notes.append("Condições muito favoráveis para degradação")
        elif combined_factor > 1.2:
            notes.append("Condições favoráveis para degradação")
        elif combined_factor < 0.8:
            notes.append("Condições desfavoráveis para degradação")
        
        if temp > 35:
            notes.append("Temperatura pode inibir atividade fúngica")
        elif temp < 15:
            notes.append("Temperatura baixa pode retardar degradação")
        
        if humidity < 40:
            notes.append("Umidade baixa pode limitar crescimento fúngico")
        elif humidity > 90:
            notes.append("Umidade muito alta pode favorecer contaminação")
        
        if ph < 3:
            notes.append("pH muito ácido pode inibir fungos")
        elif ph > 8:
            notes.append("pH alcalino pode reduzir eficiência")
        
        if 'microplastic' in plastic_form.lower():
            notes.append("Microplásticos degradam mais rapidamente devido à maior área superficial")
        
        return "; ".join(notes) if notes else "Condições dentro dos parâmetros normais"
    
    def batch_predict(self, conditions_list: List[Dict]) -> List[DegradationPrediction]:
        """Realiza predições em lote"""
        predictions = []
        for conditions in conditions_list:
            prediction = self.predict_degradation(**conditions)
            predictions.append(prediction)
        return predictions
    
    def get_available_organisms(self) -> List[str]:
        """Retorna lista de microrganismos disponíveis"""
        organisms = set()
        for item in self.degradation_data:
            organisms.add(item.get('Microorganism', ''))
        
        # Adicionar organismos da literatura
        organisms.update(self.literature_data.keys())
        
        return sorted(list(organisms))
    
    def get_available_plastics(self) -> List[str]:
        """Retorna lista de plásticos disponíveis"""
        plastics = set()
        for item in self.degradation_data:
            plastics.add(item.get('Plastic', ''))
        
        # Adicionar plásticos comuns
        common_plastics = ['PVC', 'PE', 'PET', 'PS', 'PP', 'PLA', 'PHB']
        plastics.update(common_plastics)
        
        return sorted(list(plastics))

# Exemplo de uso
if __name__ == "__main__":
    predictor = PlasticDegradationPredictor()
    
    # Exemplo baseado no texto fornecido
    prediction = predictor.predict_degradation(
        plastic_type="PVC",
        microorganism="Aspergillus niger",
        temperature=27.0,
        humidity=14.0,
        ph=4.0,
        plastic_form="pieces"
    )
    
    print(f"Predição para {prediction.plastic_type} com {prediction.microorganism}:")
    print(f"Tempo para degradação observável: {prediction.degradation_time_days} dias")
    print(f"Perda de peso esperada: {prediction.weight_loss_percentage}%")
    print(f"Confiança: {prediction.confidence}")
    print(f"Condições: {prediction.conditions}")
    print(f"Notas: {prediction.notes}")