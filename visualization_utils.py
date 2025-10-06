import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import List, Dict, Optional
import seaborn as sns
import matplotlib.pyplot as plt
from prediction_model import DegradationPrediction

class VisualizationUtils:
    """Utilitários para criação de visualizações avançadas"""
    
    def __init__(self):
        self.color_palette = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e',
            'success': '#2ca02c',
            'warning': '#d62728',
            'info': '#9467bd',
            'light': '#8c564b',
            'dark': '#e377c2'
        }
    
    def create_degradation_heatmap(self, predictions_matrix: List[List[DegradationPrediction]], 
                                 x_labels: List[str], y_labels: List[str], 
                                 metric: str = 'degradation') -> go.Figure:
        """
        Cria heatmap de degradação baseado em matriz de predições
        
        Args:
            predictions_matrix: Matriz de predições
            x_labels: Rótulos do eixo X
            y_labels: Rótulos do eixo Y
            metric: Métrica a ser visualizada ('degradation', 'time', 'confidence')
        """
        
        # Extrair valores da matriz baseado na métrica
        if metric == 'degradation':
            values = [[pred.weight_loss_percentage for pred in row] for row in predictions_matrix]
            title = "Mapa de Calor - Degradação Esperada (%)"
            colorscale = 'Reds'
        elif metric == 'time':
            values = [[pred.degradation_time_days for pred in row] for row in predictions_matrix]
            title = "Mapa de Calor - Tempo para Degradação (dias)"
            colorscale = 'Blues_r'
        elif metric == 'confidence':
            values = [[pred.confidence for pred in row] for row in predictions_matrix]
            title = "Mapa de Calor - Confiança da Predição"
            colorscale = 'Greens'
        else:
            raise ValueError("Métrica deve ser 'degradation', 'time' ou 'confidence'")
        
        fig = go.Figure(data=go.Heatmap(
            z=values,
            x=x_labels,
            y=y_labels,
            colorscale=colorscale,
            hoverongaps=False,
            hovertemplate='<b>%{y}</b><br>%{x}<br>Valor: %{z}<extra></extra>'
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Condições/Parâmetros",
            yaxis_title="Microrganismos/Plásticos",
            template='plotly_white'
        )
        
        return fig
    
    def create_3d_surface_plot(self, temp_range: np.ndarray, humidity_range: np.ndarray,
                              degradation_surface: np.ndarray, plastic_type: str, 
                              microorganism: str) -> go.Figure:
        """
        Cria gráfico 3D de superfície mostrando efeito de temperatura e umidade
        """
        
        fig = go.Figure(data=[go.Surface(
            z=degradation_surface,
            x=temp_range,
            y=humidity_range,
            colorscale='Viridis',
            hovertemplate='Temp: %{x}°C<br>Umidade: %{y}%<br>Degradação: %{z}%<extra></extra>'
        )])
        
        fig.update_layout(
            title=f'Superfície de Degradação 3D - {plastic_type} com {microorganism}',
            scene=dict(
                xaxis_title='Temperatura (°C)',
                yaxis_title='Umidade (%)',
                zaxis_title='Degradação (%)',
                camera=dict(eye=dict(x=1.2, y=1.2, z=1.2))
            ),
            template='plotly_white'
        )
        
        return fig
    
    def create_sensitivity_analysis(self, base_prediction: DegradationPrediction,
                                  parameter_variations: Dict[str, List[float]]) -> go.Figure:
        """
        Cria análise de sensibilidade dos parâmetros
        """
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Temperatura', 'Umidade', 'pH', 'Resumo'),
            specs=[[{"secondary_y": True}, {"secondary_y": True}],
                   [{"secondary_y": True}, {"type": "bar"}]]
        )
        
        colors = ['red', 'blue', 'green']
        parameters = ['temperature', 'humidity', 'ph']
        
        sensitivity_data = []
        
        for i, param in enumerate(parameters):
            if param in parameter_variations:
                values = parameter_variations[param]
                degradations = []
                times = []
                
                for val in values:
                    # Simular predição com parâmetro variado
                    # (aqui você integraria com o modelo real)
                    base_deg = base_prediction.expected_weight_loss
                    base_time = base_prediction.time_to_observable_degradation
                    
                    if param == 'temperature':
                        factor = 1 + (val - base_prediction.temperature) * 0.02
                    elif param == 'humidity':
                        factor = 1 + (val - base_prediction.humidity) * 0.01
                    else:  # pH
                        factor = 1 + abs(val - base_prediction.ph) * -0.05
                    
                    degradations.append(base_deg * factor)
                    times.append(base_time / factor)
                
                row = (i // 2) + 1
                col = (i % 2) + 1
                
                # Degradação
                fig.add_trace(
                    go.Scatter(x=values, y=degradations, name=f'Degradação ({param})',
                              line=dict(color=colors[i]), mode='lines+markers'),
                    row=row, col=col
                )
                
                # Tempo (eixo secundário)
                fig.add_trace(
                    go.Scatter(x=values, y=times, name=f'Tempo ({param})',
                              line=dict(color=colors[i], dash='dash'), mode='lines+markers',
                              yaxis='y2'),
                    row=row, col=col, secondary_y=True
                )
                
                # Calcular sensibilidade
                deg_sensitivity = np.std(degradations) / np.mean(degradations)
                time_sensitivity = np.std(times) / np.mean(times)
                sensitivity_data.append({
                    'Parâmetro': param.title(),
                    'Sensibilidade': (deg_sensitivity + time_sensitivity) / 2
                })
        
        # Gráfico de barras de sensibilidade
        if sensitivity_data:
            sens_df = pd.DataFrame(sensitivity_data)
            fig.add_trace(
                go.Bar(x=sens_df['Parâmetro'], y=sens_df['Sensibilidade'],
                      name='Sensibilidade', marker_color='orange'),
                row=2, col=2
            )
        
        fig.update_layout(
            height=800,
            title_text="Análise de Sensibilidade dos Parâmetros",
            template='plotly_white'
        )
        
        return fig
    
    def create_uncertainty_bands(self, predictions: List[DegradationPrediction]) -> go.Figure:
        """
        Cria gráfico com bandas de incerteza baseadas na confiança
        """
        
        # Ordenar por tempo
        sorted_preds = sorted(predictions, key=lambda x: x.degradation_time_days)
        
        times = [p.degradation_time_days for p in sorted_preds]
        degradations = [p.weight_loss_percentage for p in sorted_preds]
        confidences = [p.confidence for p in sorted_preds]
        
        # Calcular bandas de incerteza
        upper_bounds = [d * (1 + (1 - c) * 0.5) for d, c in zip(degradations, confidences)]
        lower_bounds = [d * (1 - (1 - c) * 0.5) for d, c in zip(degradations, confidences)]
        
        fig = go.Figure()
        
        # Banda de incerteza
        fig.add_trace(go.Scatter(
            x=times + times[::-1],
            y=upper_bounds + lower_bounds[::-1],
            fill='toself',
            fillcolor='rgba(31, 119, 180, 0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name='Banda de Incerteza',
            hoverinfo="skip"
        ))
        
        # Linha central
        fig.add_trace(go.Scatter(
            x=times,
            y=degradations,
            mode='lines+markers',
            name='Predição Central',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=8, color=confidences, colorscale='Viridis',
                       showscale=True, colorbar=dict(title="Confiança"))
        ))
        
        fig.update_layout(
            title="Predições com Bandas de Incerteza",
            xaxis_title="Tempo para Degradação (dias)",
            yaxis_title="Degradação Esperada (%)",
            template='plotly_white',
            hovermode='x unified'
        )
        
        return fig
    
    def create_correlation_matrix(self, data: pd.DataFrame) -> go.Figure:
        """
        Cria matriz de correlação entre variáveis
        """
        
        # Selecionar apenas colunas numéricas
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        corr_matrix = data[numeric_cols].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            hoverongaps=False,
            hovertemplate='<b>%{y}</b> vs <b>%{x}</b><br>Correlação: %{z:.3f}<extra></extra>'
        ))
        
        fig.update_layout(
            title="Matriz de Correlação entre Variáveis",
            template='plotly_white',
            width=600,
            height=600
        )
        
        return fig
    
    def create_distribution_plot(self, predictions: List[DegradationPrediction],
                               metric: str = 'degradation') -> go.Figure:
        """
        Cria gráfico de distribuição das predições
        """
        
        if metric == 'degradation':
            values = [p.weight_loss_percentage for p in predictions]
            title = "Distribuição da Degradação Esperada"
            x_title = "Degradação (%)"
        elif metric == 'time':
            values = [p.degradation_time_days for p in predictions]
            title = "Distribuição do Tempo para Degradação"
            x_title = "Tempo (dias)"
        elif metric == 'confidence':
            values = [p.confidence for p in predictions]
            title = "Distribuição da Confiança"
            x_title = "Confiança"
        else:
            raise ValueError("Métrica deve ser 'degradation', 'time' ou 'confidence'")
        
        fig = go.Figure()
        
        # Histograma
        fig.add_trace(go.Histogram(
            x=values,
            nbinsx=20,
            name='Distribuição',
            opacity=0.7,
            marker_color=self.color_palette['primary']
        ))
        
        # Linha de densidade (aproximada)
        hist, bin_edges = np.histogram(values, bins=20, density=True)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        
        # Suavização simples
        from scipy.ndimage import gaussian_filter1d
        smoothed_hist = gaussian_filter1d(hist, sigma=1)
        
        fig.add_trace(go.Scatter(
            x=bin_centers,
            y=smoothed_hist * len(values) * (bin_edges[1] - bin_edges[0]),
            mode='lines',
            name='Densidade',
            line=dict(color=self.color_palette['secondary'], width=3)
        ))
        
        # Estatísticas
        mean_val = np.mean(values)
        median_val = np.median(values)
        
        fig.add_vline(x=mean_val, line_dash="dash", line_color="red",
                     annotation_text=f"Média: {mean_val:.1f}")
        fig.add_vline(x=median_val, line_dash="dot", line_color="green",
                     annotation_text=f"Mediana: {median_val:.1f}")
        
        fig.update_layout(
            title=title,
            xaxis_title=x_title,
            yaxis_title="Frequência",
            template='plotly_white',
            showlegend=True
        )
        
        return fig
    
    def create_performance_dashboard(self, predictions: List[DegradationPrediction]) -> go.Figure:
        """
        Cria dashboard de performance do modelo
        """
        
        fig = make_subplots(
            rows=2, cols=3,
            subplot_titles=('Confiança vs Degradação', 'Tempo vs Degradação', 
                           'Distribuição de Confiança', 'Eficiência por Organismo',
                           'Eficiência por Plástico', 'Resumo Estatístico'),
            specs=[[{"type": "scatter"}, {"type": "scatter"}, {"type": "histogram"}],
                   [{"type": "bar"}, {"type": "bar"}, {"type": "table"}]]
        )
        
        # Dados para análise
        confidences = [p.confidence for p in predictions]
        degradations = [p.weight_loss_percentage for p in predictions]
        times = [p.degradation_time_days for p in predictions]
        organisms = [p.microorganism for p in predictions]
        plastics = [p.plastic_type for p in predictions]
        
        # Gráfico 1: Confiança vs Degradação
        fig.add_trace(
            go.Scatter(x=confidences, y=degradations, mode='markers',
                      name='Confiança vs Degradação',
                      marker=dict(size=8, color=times, colorscale='Viridis')),
            row=1, col=1
        )
        
        # Gráfico 2: Tempo vs Degradação
        fig.add_trace(
            go.Scatter(x=times, y=degradations, mode='markers',
                      name='Tempo vs Degradação',
                      marker=dict(size=8, color=confidences, colorscale='Reds')),
            row=1, col=2
        )
        
        # Gráfico 3: Distribuição de Confiança
        fig.add_trace(
            go.Histogram(x=confidences, name='Distribuição Confiança',
                        marker_color=self.color_palette['info']),
            row=1, col=3
        )
        
        # Gráfico 4: Eficiência por Organismo
        organism_stats = pd.DataFrame({
            'organism': organisms,
            'degradation': degradations,
            'time': times
        }).groupby('organism').agg({
            'degradation': 'mean',
            'time': 'mean'
        }).reset_index()
        
        fig.add_trace(
            go.Bar(x=organism_stats['organism'], y=organism_stats['degradation'],
                  name='Degradação Média por Organismo',
                  marker_color=self.color_palette['success']),
            row=2, col=1
        )
        
        # Gráfico 5: Eficiência por Plástico
        plastic_stats = pd.DataFrame({
            'plastic': plastics,
            'degradation': degradations,
            'time': times
        }).groupby('plastic').agg({
            'degradation': 'mean',
            'time': 'mean'
        }).reset_index()
        
        fig.add_trace(
            go.Bar(x=plastic_stats['plastic'], y=plastic_stats['degradation'],
                  name='Degradação Média por Plástico',
                  marker_color=self.color_palette['warning']),
            row=2, col=2
        )
        
        # Tabela de resumo estatístico
        stats_data = [
            ['Métrica', 'Valor'],
            ['Degradação Média', f"{np.mean(degradations):.1f}%"],
            ['Tempo Médio', f"{np.mean(times):.0f} dias"],
            ['Confiança Média', f"{np.mean(confidences):.2f}"],
            ['Desvio Padrão Degradação', f"{np.std(degradations):.1f}%"],
            ['Desvio Padrão Tempo', f"{np.std(times):.0f} dias"]
        ]
        
        fig.add_trace(
            go.Table(
                header=dict(values=stats_data[0], fill_color='lightblue'),
                cells=dict(values=list(zip(*stats_data[1:])), fill_color='white')
            ),
            row=2, col=3
        )
        
        fig.update_layout(
            height=800,
            title_text="Dashboard de Performance do Modelo",
            template='plotly_white',
            showlegend=False
        )
        
        return fig

# Função auxiliar para importação condicional do scipy
def safe_import_scipy():
    """Importa scipy de forma segura"""
    try:
        from scipy.ndimage import gaussian_filter1d
        return gaussian_filter1d
    except ImportError:
        # Fallback simples se scipy não estiver disponível
        def simple_smooth(data, sigma=1):
            return data
        return simple_smooth

# Substituir a importação do scipy no código acima
gaussian_filter1d = safe_import_scipy()