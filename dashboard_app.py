import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import json
from prediction_model import PlasticDegradationPredictor, DegradationPrediction

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Degradação de Plásticos",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .prediction-result {
        background-color: #e8f4fd;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #1f77b4;
        margin: 1rem 0;
    }
    .confidence-high { color: #28a745; }
    .confidence-medium { color: #ffc107; }
    .confidence-low { color: #dc3545; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_predictor():
    """Carrega o modelo de predição com cache"""
    return PlasticDegradationPredictor()

@st.cache_data
def load_degradation_data():
    """Carrega dados de degradação do arquivo JSON"""
    try:
        with open('degraders_list_with_images.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return pd.DataFrame(data)
    except FileNotFoundError:
        st.warning("Arquivo de dados não encontrado. Usando dados de exemplo.")
        return pd.DataFrame()

def create_degradation_timeline(prediction: DegradationPrediction):
    """Cria gráfico de timeline de degradação"""
    days = list(range(0, int(prediction.degradation_time_days) + 30, 5))
    
    degradation_values = []
    for day in days:
        if day <= prediction.degradation_time_days:
            # Degradação progressiva até o ponto observável
            progress = (day / prediction.degradation_time_days) ** 0.7
            degradation = prediction.weight_loss_percentage * progress
        else:
            # Degradação adicional após ponto observável
            extra_days = day - prediction.degradation_time_days
            additional_degradation = prediction.weight_loss_percentage * 0.3 * (1 - np.exp(-extra_days/20))
            degradation = prediction.weight_loss_percentage + additional_degradation
        
        degradation_values.append(min(degradation, 95))  # Máximo 95% de degradação
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=days,
        y=degradation_values,
        mode='lines+markers',
        name='Degradação Prevista',
        line=dict(color='#FF6B6B', width=3),
        marker=dict(size=6)
    ))
    
    # Adicionar linha vertical para ponto de degradação observável
    fig.add_vline(
        x=prediction.degradation_time_days,
        line_dash="dash",
        line_color="orange",
        annotation_text=f"Degradação Observável<br>({prediction.degradation_time_days} dias)"
    )
    
    fig.update_layout(
        title=f"Timeline de Degradação - {prediction.plastic_type} com {prediction.microorganism}",
        xaxis_title="Dias",
        yaxis_title="Perda de Peso (%)",
        hovermode='x unified',
        template='plotly_white'
    )
    
    return fig

def create_conditions_radar(temperature, humidity, ph):
    """Cria gráfico radar das condições ambientais"""
    categories = ['Temperatura', 'Umidade', 'pH']
    
    # Normalizar valores para escala 0-100
    temp_norm = min(100, (temperature / 40) * 100)  # 40°C como máximo
    humidity_norm = humidity  # Já em porcentagem
    ph_norm = (ph / 14) * 100  # pH 14 como máximo
    
    values = [temp_norm, humidity_norm, ph_norm]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Condições Atuais',
        line_color='#1f77b4'
    ))
    
    # Adicionar zona ótima
    optimal_values = [75, 70, 35]  # Valores ótimos normalizados
    fig.add_trace(go.Scatterpolar(
        r=optimal_values,
        theta=categories,
        fill='toself',
        name='Zona Ótima',
        line_color='#28a745',
        opacity=0.3
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Condições Ambientais vs Zona Ótima"
    )
    
    return fig

def create_comparison_chart(predictions_list):
    """Cria gráfico de comparação entre diferentes predições"""
    if not predictions_list:
        return None
    
    df = pd.DataFrame([
        {
            'Cenário': f"{p.plastic_type} + {p.microorganism}",
            'Tempo (dias)': p.degradation_time_days,
            'Degradação (%)': p.weight_loss_percentage,
            'Confiança': p.confidence,
            'Temperatura': p.conditions['temperature'],
            'Umidade': p.conditions['humidity'],
            'pH': p.conditions['ph']
        }
        for p in predictions_list
    ])
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Tempo vs Degradação', 'Confiança por Cenário', 
                       'Efeito da Temperatura', 'Efeito da Umidade'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Gráfico 1: Tempo vs Degradação
    fig.add_trace(
        go.Scatter(x=df['Tempo (dias)'], y=df['Degradação (%)'], 
                  mode='markers+text', text=df['Cenário'],
                  textposition="top center", name='Predições',
                  marker=dict(size=df['Confiança']*20, color=df['Confiança'],
                            colorscale='Viridis', showscale=True)),
        row=1, col=1
    )
    
    # Gráfico 2: Confiança
    fig.add_trace(
        go.Bar(x=df['Cenário'], y=df['Confiança'], name='Confiança',
               marker_color=df['Confiança'], 
               marker_colorscale='RdYlGn'),
        row=1, col=2
    )
    
    # Gráfico 3: Temperatura
    fig.add_trace(
        go.Scatter(x=df['Temperatura'], y=df['Degradação (%)'],
                  mode='markers', name='Temp vs Degradação',
                  marker=dict(color='red', size=8)),
        row=2, col=1
    )
    
    # Gráfico 4: Umidade
    fig.add_trace(
        go.Scatter(x=df['Umidade'], y=df['Degradação (%)'],
                  mode='markers', name='Umidade vs Degradação',
                  marker=dict(color='blue', size=8)),
        row=2, col=2
    )
    
    fig.update_layout(height=800, showlegend=False, title_text="Análise Comparativa de Predições")
    
    return fig

def main():
    """Função principal da aplicação"""
    
    # Header
    st.markdown('<h1 class="main-header">🧪 Dashboard de Degradação de Plásticos por Fungos</h1>', 
                unsafe_allow_html=True)
    
    # Carregar modelo
    predictor = load_predictor()
    
    # Definir fonte baseada no tipo de preditor
    source = "Literatura científica + Modelo de predição local"
    
    # Sidebar para parâmetros
    st.sidebar.header("⚙️ Parâmetros de Predição")
    
    # Seleção de plástico e microrganismo
    plastic_type = st.sidebar.selectbox(
        "Tipo de Plástico",
        options=['PVC', 'PE', 'PET', 'PS', 'PP', 'PLA', 'PHB'],
        index=0
    )
    
    microorganism = st.sidebar.selectbox(
        "Microrganismo",
        options=['Aspergillus niger', 'Candida albicans', 'Acremonium sclerotigenum', 
                'Penicillium', 'Trichoderma'],
        index=0
    )
    
    # Parâmetros ambientais
    st.sidebar.subheader("🌡️ Condições Ambientais")
    
    temperature = st.sidebar.slider(
        "Temperatura (°C)",
        min_value=10.0,
        max_value=45.0,
        value=27.0,
        step=0.5
    )
    
    humidity = st.sidebar.slider(
        "Umidade Relativa (%)",
        min_value=10.0,
        max_value=95.0,
        value=14.0,
        step=1.0
    )
    
    ph = st.sidebar.slider(
        "pH",
        min_value=2.0,
        max_value=12.0,
        value=4.0,
        step=0.1
    )
    
    plastic_form = st.sidebar.selectbox(
        "Forma do Plástico",
        options=['pieces', 'microplastics', 'film', 'powder'],
        index=0
    )
    
    # Botão de predição
    if st.sidebar.button("🔮 Fazer Predição", type="primary"):
        with st.spinner("Calculando predição..."):
            prediction = predictor.predict_degradation(
                plastic_type=plastic_type,
                microorganism=microorganism,
                temperature=temperature,
                humidity=humidity,
                ph=ph,
                plastic_form=plastic_form
            )
            
            st.session_state['current_prediction'] = prediction
    
    # Layout principal
    if 'current_prediction' in st.session_state:
        prediction = st.session_state['current_prediction']
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="⏱️ Tempo para Degradação",
                value=f"{prediction.degradation_time_days} dias"
            )
        
        with col2:
            st.metric(
                label="📉 Perda de Peso Esperada",
                value=f"{prediction.weight_loss_percentage}%"
            )
        
        with col3:
            confidence_color = ("confidence-high" if prediction.confidence > 0.7 
                              else "confidence-medium" if prediction.confidence > 0.4 
                              else "confidence-low")
            st.metric(
                label="🎯 Confiança",
                value=f"{prediction.confidence:.2f}"
            )
        
        with col4:
            st.metric(
                label="🌡️ Condições",
                value=f"{temperature}°C, {humidity}%, pH {ph}"
            )
        
        # Resultado detalhado
        st.markdown(f"""
        <div class="prediction-result">
            <h3>📊 Resultado da Predição</h3>
            <p><strong>Plástico:</strong> {prediction.plastic_type}</p>
            <p><strong>Microrganismo:</strong> {prediction.microorganism}</p>
            <p><strong>Forma:</strong> {plastic_form}</p>
            <p><strong>Notas:</strong> {prediction.notes}</p>
            <p><strong>Fonte:</strong> {source}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Detalhes da predição
        st.subheader("📊 Detalhes da Predição")
        
        details_col1, details_col2 = st.columns(2)
        
        with details_col1:
            st.write("**Condições Ambientais:**")
            st.write(f"🌡️ Temperatura: {prediction.conditions['temperature']}°C")
            st.write(f"💧 Umidade: {prediction.conditions['humidity']}%")
            st.write(f"⚗️ pH: {prediction.conditions['ph']}")
            st.write(f"📦 Forma: {prediction.conditions['plastic_form']}")
        
        with details_col2:
            st.write("**Parâmetros:**")
            st.write(f"🧪 Plástico: {prediction.plastic_type}")
            st.write(f"🦠 Microrganismo: {prediction.microorganism}")
            st.write(f"📋 Fonte: Literatura científica + API")
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(
                create_degradation_timeline(prediction),
                use_container_width=True
            )
        
        with col2:
            st.plotly_chart(
                create_conditions_radar(temperature, humidity, ph),
                use_container_width=True
            )
    
    # Seção de análise comparativa
    st.header("📈 Análise Comparativa")
    
    if st.button("🔄 Gerar Cenários de Comparação"):
        scenarios = [
            {'plastic_type': 'PVC', 'microorganism': 'Aspergillus niger', 
             'temperature': 25, 'humidity': 60, 'ph': 5, 'plastic_form': 'pieces'},
            {'plastic_type': 'PVC', 'microorganism': 'Aspergillus niger', 
             'temperature': 30, 'humidity': 70, 'ph': 4, 'plastic_form': 'microplastics'},
            {'plastic_type': 'PE', 'microorganism': 'Aspergillus niger', 
             'temperature': 27, 'humidity': 65, 'ph': 5, 'plastic_form': 'microplastics'},
            {'plastic_type': 'PET', 'microorganism': 'Acremonium sclerotigenum', 
             'temperature': 25, 'humidity': 60, 'ph': 6, 'plastic_form': 'microplastics'}
        ]
        
        predictions_list = predictor.batch_predict(scenarios)
        
        comparison_chart = create_comparison_chart(predictions_list)
        if comparison_chart:
            st.plotly_chart(comparison_chart, use_container_width=True)
        
        # Tabela de comparação
        comparison_df = pd.DataFrame([
            {
                'Plástico': p.plastic_type,
                'Microrganismo': p.microorganism,
                'Temperatura (°C)': p.conditions['temperature'],
                'Umidade (%)': p.conditions['humidity'],
                'pH': p.conditions['ph'],
                'Tempo (dias)': p.degradation_time_days,
                'Degradação (%)': p.weight_loss_percentage,
                'Confiança': f"{p.confidence:.2f}"
            }
            for p in predictions_list
        ])
        
        st.subheader("📋 Tabela Comparativa")
        st.dataframe(comparison_df, use_container_width=True)
    
    # Seção de dados históricos
    st.header("📚 Dados da Literatura")
    
    df = load_degradation_data()
    if not df.empty:
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            selected_plastic = st.selectbox(
                "Filtrar por Plástico",
                options=['Todos'] + list(df['Plastic'].unique()) if 'Plastic' in df.columns else ['Todos']
            )
        
        with col2:
            selected_organism = st.selectbox(
                "Filtrar por Microrganismo",
                options=['Todos'] + list(df['Microorganism'].unique()) if 'Microorganism' in df.columns else ['Todos']
            )
        
        # Aplicar filtros
        filtered_df = df.copy()
        if selected_plastic != 'Todos' and 'Plastic' in df.columns:
            filtered_df = filtered_df[filtered_df['Plastic'] == selected_plastic]
        if selected_organism != 'Todos' and 'Microorganism' in df.columns:
            filtered_df = filtered_df[filtered_df['Microorganism'] == selected_organism]
        
        # Mostrar dados filtrados
        if not filtered_df.empty:
            st.dataframe(
                filtered_df[['Microorganism', 'Plastic', 'Enzyme', 'Year', 'Isolation_location']].head(20)
                if all(col in filtered_df.columns for col in ['Microorganism', 'Plastic', 'Enzyme', 'Year', 'Isolation_location'])
                else filtered_df.head(20),
                use_container_width=True
            )
        else:
            st.info("Nenhum dado encontrado com os filtros selecionados.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Dashboard de Degradação de Plásticos por Fungos | 
        Baseado em literatura científica e modelos preditivos</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()