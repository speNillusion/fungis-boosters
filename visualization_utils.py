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
    """Utilities for creating advanced visualizations"""
    
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
        Creates degradation heatmap based on predictions matrix
        
        Args:
            predictions_matrix: Predictions matrix
            x_labels: X-axis labels
            y_labels: Y-axis labels
            metric: Metric to visualize ('degradation', 'time', 'confidence')
        """
        
        # Extract values from matrix based on metric
        if metric == 'degradation':
            values = [[pred.weight_loss_percentage for pred in row] for row in predictions_matrix]
            title = "Heat Map - Expected Degradation (%)"
            colorscale = 'Reds'
        elif metric == 'time':
            values = [[pred.degradation_time_days for pred in row] for row in predictions_matrix]
            title = "Heat Map - Time to Degradation (days)"
            colorscale = 'Blues_r'
        elif metric == 'confidence':
            values = [[pred.confidence for pred in row] for row in predictions_matrix]
            title = "Heat Map - Prediction Confidence"
            colorscale = 'Greens'
        else:
            raise ValueError("Metric must be 'degradation', 'time' or 'confidence'")
        
        fig = go.Figure(data=go.Heatmap(
            z=values,
            x=x_labels,
            y=y_labels,
            colorscale=colorscale,
            hoverongaps=False,
            hovertemplate='<b>%{y}</b><br>%{x}<br>Value: %{z}<extra></extra>'
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Conditions/Parameters",
            yaxis_title="Microorganisms/Plastics",
            template='plotly_white'
        )
        
        return fig
    
    def create_3d_surface_plot(self, temp_range: np.ndarray, humidity_range: np.ndarray,
                              degradation_surface: np.ndarray, plastic_type: str, 
                              microorganism: str) -> go.Figure:
        """
        Creates 3D surface plot showing temperature and humidity effects
        """
        
        fig = go.Figure(data=[go.Surface(
            z=degradation_surface,
            x=temp_range,
            y=humidity_range,
            colorscale='Viridis',
            hovertemplate='Temp: %{x}°C<br>Humidity: %{y}%<br>Degradation: %{z}%<extra></extra>'
        )])
        
        fig.update_layout(
            title=f'3D Degradation Surface - {plastic_type} with {microorganism}',
            scene=dict(
                xaxis_title='Temperature (°C)',
                yaxis_title='Humidity (%)',
                zaxis_title='Degradation (%)',
                camera=dict(eye=dict(x=1.2, y=1.2, z=1.2))
            ),
            template='plotly_white'
        )
        
        return fig
    
    def create_sensitivity_analysis(self, base_prediction: DegradationPrediction,
                                  parameter_variations: Dict[str, List[float]]) -> go.Figure:
        """
        Creates parameter sensitivity analysis
        """
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Temperature', 'Humidity', 'pH', 'Summary'),
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
                    # Simulate prediction with varied parameter
                    # (here you would integrate with the real model)
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
                
                # Degradation
                fig.add_trace(
                    go.Scatter(x=values, y=degradations, name=f'Degradation ({param})',
                              line=dict(color=colors[i]), mode='lines+markers'),
                    row=row, col=col
                )
                
                # Time (secondary axis)
                fig.add_trace(
                    go.Scatter(x=values, y=times, name=f'Time ({param})',
                              line=dict(color=colors[i], dash='dash'), mode='lines+markers',
                              yaxis='y2'),
                    row=row, col=col, secondary_y=True
                )
                
                # Calculate sensitivity
                deg_sensitivity = np.std(degradations) / np.mean(degradations)
                time_sensitivity = np.std(times) / np.mean(times)
                sensitivity_data.append({
                    'Parameter': param.title(),
                    'Sensitivity': (deg_sensitivity + time_sensitivity) / 2
                })
        
        # Sensitivity bar chart
        if sensitivity_data:
            sens_df = pd.DataFrame(sensitivity_data)
            fig.add_trace(
                go.Bar(x=sens_df['Parameter'], y=sens_df['Sensitivity'],
                      name='Sensitivity', marker_color='orange'),
                row=2, col=2
            )
        
        fig.update_layout(
            height=800,
            title_text="Parameter Sensitivity Analysis",
            template='plotly_white'
        )
        
        return fig
    
    def create_uncertainty_bands(self, predictions: List[DegradationPrediction]) -> go.Figure:
        """
        Creates chart with uncertainty bands based on confidence
        """
        
        # Sort by time
        sorted_preds = sorted(predictions, key=lambda x: x.degradation_time_days)
        
        times = [p.degradation_time_days for p in sorted_preds]
        degradations = [p.weight_loss_percentage for p in sorted_preds]
        confidences = [p.confidence for p in sorted_preds]
        
        # Calcular bandas de incerteza
        upper_bounds = [d * (1 + (1 - c) * 0.5) for d, c in zip(degradations, confidences)]
        lower_bounds = [d * (1 - (1 - c) * 0.5) for d, c in zip(degradations, confidences)]
        
        fig = go.Figure()
        
        # Uncertainty band
        fig.add_trace(go.Scatter(
            x=times + times[::-1],
            y=upper_bounds + lower_bounds[::-1],
            fill='toself',
            fillcolor='rgba(31, 119, 180, 0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name='Uncertainty Band',
            hoverinfo="skip"
        ))
        
        # Central line
        fig.add_trace(go.Scatter(
            x=times,
            y=degradations,
            mode='lines+markers',
            name='Central Prediction',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=8, color=confidences, colorscale='Viridis',
                       showscale=True, colorbar=dict(title="Confidence"))
        ))
        
        fig.update_layout(
            title="Predictions with Uncertainty Bands",
            xaxis_title="Time to Degradation (days)",
            yaxis_title="Expected Degradation (%)",
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
        Creates distribution plot of predictions
        """
        
        if metric == 'degradation':
            values = [p.weight_loss_percentage for p in predictions]
            title = "Expected Degradation Distribution"
            x_title = "Degradation (%)"
        elif metric == 'time':
            values = [p.degradation_time_days for p in predictions]
            title = "Time to Degradation Distribution"
            x_title = "Time (days)"
        elif metric == 'confidence':
            values = [p.confidence for p in predictions]
            title = "Confidence Distribution"
            x_title = "Confidence"
        else:
            raise ValueError("Metric must be 'degradation', 'time' or 'confidence'")
        
        fig = go.Figure()
        
        # Histograma
        fig.add_trace(go.Histogram(
            x=values,
            nbinsx=20,
            name='Distribution',
            opacity=0.7,
            marker_color=self.color_palette['primary']
        ))
        
        # Density line (approximated)
        hist, bin_edges = np.histogram(values, bins=20, density=True)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        
        # Simple smoothing
        from scipy.ndimage import gaussian_filter1d
        smoothed_hist = gaussian_filter1d(hist, sigma=1)
        
        fig.add_trace(go.Scatter(
            x=bin_centers,
            y=smoothed_hist * len(values) * (bin_edges[1] - bin_edges[0]),
            mode='lines',
            name='Density',
            line=dict(color=self.color_palette['secondary'], width=3)
        ))
        
        # Statistics
        mean_val = np.mean(values)
        median_val = np.median(values)
        
        fig.add_vline(x=mean_val, line_dash="dash", line_color="red",
                     annotation_text=f"Mean: {mean_val:.1f}")
        fig.add_vline(x=median_val, line_dash="dot", line_color="green",
                     annotation_text=f"Median: {median_val:.1f}")
        
        fig.update_layout(
            title=title,
            xaxis_title=x_title,
            yaxis_title="Frequency",
            template='plotly_white',
            showlegend=True
        )
        
        return fig
    
    def create_performance_dashboard(self, predictions: List[DegradationPrediction]) -> go.Figure:
        """
        Creates model performance dashboard
        """
        
        fig = make_subplots(
            rows=2, cols=3,
            subplot_titles=('Confidence vs Degradation', 'Time vs Degradation', 
                           'Confidence Distribution', 'Efficiency by Organism',
                           'Efficiency by Plastic', 'Statistical Summary'),
            specs=[[{"type": "scatter"}, {"type": "scatter"}, {"type": "histogram"}],
                   [{"type": "bar"}, {"type": "bar"}, {"type": "table"}]]
        )
        
        # Data for analysis
        confidences = [p.confidence for p in predictions]
        degradations = [p.weight_loss_percentage for p in predictions]
        times = [p.degradation_time_days for p in predictions]
        organisms = [p.microorganism for p in predictions]
        plastics = [p.plastic_type for p in predictions]
        
        # Chart 1: Confidence vs Degradation
        fig.add_trace(
            go.Scatter(x=confidences, y=degradations, mode='markers',
                      name='Confidence vs Degradation',
                      marker=dict(size=8, color=times, colorscale='Viridis')),
            row=1, col=1
        )
        
        # Chart 2: Time vs Degradation
        fig.add_trace(
            go.Scatter(x=times, y=degradations, mode='markers',
                      name='Time vs Degradation',
                      marker=dict(size=8, color=confidences, colorscale='Reds')),
            row=1, col=2
        )
        
        # Chart 3: Confidence Distribution
        fig.add_trace(
            go.Histogram(x=confidences, name='Confidence Distribution',
                        marker_color=self.color_palette['info']),
            row=1, col=3
        )
        
        # Chart 4: Efficiency by Organism
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
                  name='Average Degradation by Organism',
                  marker_color=self.color_palette['success']),
            row=2, col=1
        )
        
        # Chart 5: Efficiency by Plastic
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
                  name='Average Degradation by Plastic',
                  marker_color=self.color_palette['warning']),
            row=2, col=2
        )
        
        # Statistical summary table
        stats_data = [
            ['Metric', 'Value'],
            ['Average Degradation', f"{np.mean(degradations):.1f}%"],
            ['Average Time', f"{np.mean(times):.0f} days"],
            ['Average Confidence', f"{np.mean(confidences):.2f}"],
            ['Degradation Std Dev', f"{np.std(degradations):.1f}%"],
            ['Time Std Dev', f"{np.std(times):.0f} days"]
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
            title_text="Model Performance Dashboard",
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