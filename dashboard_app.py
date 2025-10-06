import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import json
from prediction_model import PlasticDegradationPredictor, DegradationPrediction

# Page configuration
st.set_page_config(
    page_title="Plastic Degradation Dashboard",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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
    """Loads the prediction model with cache"""
    return PlasticDegradationPredictor()

@st.cache_data
def load_degradation_data():
    """Loads degradation data from JSON file"""
    try:
        with open('degraders_list_with_images.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return pd.DataFrame(data)
    except FileNotFoundError:
        st.warning("Data file not found. Using example data.")
        return pd.DataFrame()

def create_degradation_timeline(prediction: DegradationPrediction):
    """Creates degradation timeline chart"""
    days = list(range(0, int(prediction.degradation_time_days) + 30, 5))
    
    degradation_values = []
    for day in days:
        if day <= prediction.degradation_time_days:
            # Progressive degradation until observable point
            progress = (day / prediction.degradation_time_days) ** 0.7
            degradation = prediction.weight_loss_percentage * progress
        else:
            # Additional degradation after observable point
            extra_days = day - prediction.degradation_time_days
            additional_degradation = prediction.weight_loss_percentage * 0.3 * (1 - np.exp(-extra_days/20))
            degradation = prediction.weight_loss_percentage + additional_degradation
        
        degradation_values.append(min(degradation, 95))  # Maximum 95% degradation
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=days,
        y=degradation_values,
        mode='lines+markers',
        name='Predicted Degradation',
        line=dict(color='#FF6B6B', width=3),
        marker=dict(size=6)
    ))
    
    # Add vertical line for observable degradation point
    fig.add_vline(
        x=prediction.degradation_time_days,
        line_dash="dash",
        line_color="orange",
        annotation_text=f"Observable Degradation<br>({prediction.degradation_time_days} days)"
    )
    
    fig.update_layout(
        title=f"Degradation Timeline - {prediction.plastic_type} com {prediction.microorganism}",
        xaxis_title="Days",
        yaxis_title="Weight Loss (%)",
        hovermode='x unified',
        template='plotly_white'
    )
    
    return fig

def create_conditions_radar(temperature, humidity, ph):
    """Creates radar chart of environmental conditions"""
    categories = ['Temperature', 'Humidity', 'pH']
    
    # Normalize values to 0-100 scale
    temp_norm = (temperature - 10) / (45 - 10) * 100
    humidity_norm = humidity
    ph_norm = (ph - 2) / (12 - 2) * 100
    
    values = [temp_norm, humidity_norm, ph_norm]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Current Conditions',
        line_color='#1f77b4'
    ))
    
    # Add optimal zone
    optimal_values = [75, 70, 35]  # Normalized optimal values
    fig.add_trace(go.Scatterpolar(
        r=optimal_values,
        theta=categories,
        fill='toself',
        name='Optimal Zone',
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
        title="Environmental Conditions",
        template='plotly_white'
    )
    
    return fig

def create_comparison_chart(predictions_list):
    """Creates comparison chart between different predictions"""
    if not predictions_list:
        return None
    
    df = pd.DataFrame([
        {
            'Scenario': f"{p.plastic_type} + {p.microorganism}",
            'Time (days)': p.degradation_time_days,
            'Degradation (%)': p.weight_loss_percentage,
            'Confidence': p.confidence,
            'Temperature': p.conditions['temperature'],
            'Humidity': p.conditions['humidity'],
            'pH': p.conditions['ph']
        }
        for p in predictions_list
    ])
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Time vs Degradation', 'Confidence by Scenario', 
                       'Temperature Effect', 'Humidity Effect'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Chart 1: Time vs Degradation
    fig.add_trace(
        go.Scatter(x=df['Time (days)'], y=df['Degradation (%)'], 
                  mode='markers+text', text=df['Scenario'],
                  textposition="top center", name='Predictions',
                  marker=dict(size=df['Confidence']*20, color=df['Confidence'],
                            colorscale='Viridis', showscale=True)),
        row=1, col=1
    )
    
    # Chart 2: Confidence
    fig.add_trace(
        go.Bar(x=df['Scenario'], y=df['Confidence'], name='Confidence',
               marker_color=df['Confidence'], 
               marker_colorscale='RdYlGn'),
        row=1, col=2
    )
    
    # Chart 3: Temperature
    fig.add_trace(
        go.Scatter(x=df['Temperature'], y=df['Degradation (%)'],
                  mode='markers', name='Temp vs Degradation',
                  marker=dict(color='red', size=8)),
        row=2, col=1
    )
    
    # Chart 4: Humidity
    fig.add_trace(
        go.Scatter(x=df['Humidity'], y=df['Degradation (%)'],
                  mode='markers', name='Humidity vs Degradation',
                  marker=dict(color='blue', size=8)),
        row=2, col=2
    )
    
    fig.update_layout(height=800, showlegend=False, title_text="Comparative Analysis of Predictions")
    
    return fig

def main():
    """Main function of the application"""
    
    # Header
    st.markdown('<h1 class="main-header">🧪 Plastic Degradation Dashboard by Fungi</h1>', 
                unsafe_allow_html=True)
    
    # Load model
    predictor = load_predictor()
    
    # Define source based on predictor type
    source = "Scientific literature + Local prediction model"
    
    # Sidebar for parameters
    st.sidebar.header("⚙️ Prediction Parameters")
    
    # Parameter selection
    plastic_type = st.sidebar.selectbox(
        "Plastic Type",
        options=['PVC', 'PE', 'PET', 'PS', 'PP'],
        index=0
    )
    
    microorganism = st.sidebar.selectbox(
        "Microorganism",
        options=[
            'Aspergillus niger',
            'Acremonium sclerotigenum',
            'Penicillium chrysogenum',
            'Trichoderma viride',
            'Fusarium oxysporum'
        ],
        index=0
    )
    
    # Environmental conditions
    st.sidebar.subheader("🌡️ Environmental Conditions")
    
    temperature = st.sidebar.slider(
        "Temperature (°C)",
        min_value=10.0,
        max_value=45.0,
        value=27.0,
        step=0.5
    )
    
    humidity = st.sidebar.slider(
        "Relative Humidity (%)",
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
        "Plastic Form",
        options=['pieces', 'microplastics', 'film', 'powder'],
        index=0
    )
    
    # Prediction button
    if st.sidebar.button("🔮 Make Prediction", type="primary"):
        with st.spinner("Calculating prediction..."):
            prediction = predictor.predict_degradation(
                plastic_type=plastic_type,
                microorganism=microorganism,
                temperature=temperature,
                humidity=humidity,
                ph=ph,
                plastic_form=plastic_form
            )
            
            st.session_state['current_prediction'] = prediction
    
    # Main layout
    if 'current_prediction' in st.session_state:
        prediction = st.session_state['current_prediction']
        
        # Main metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="⏱️ Time to Degradation",
                value=f"{prediction.degradation_time_days} days"
            )
        
        with col2:
            st.metric(
                label="📉 Expected Weight Loss",
                value=f"{prediction.weight_loss_percentage}%"
            )
        
        with col3:
            confidence_color = ("confidence-high" if prediction.confidence > 0.7 
                              else "confidence-medium" if prediction.confidence > 0.4 
                              else "confidence-low")
            st.metric(
                label="🎯 Confidence",
                value=f"{prediction.confidence:.2f}"
            )
        
        with col4:
            st.metric(
                label="🌡️ Conditions",
                value=f"{temperature}°C, {humidity}%, pH {ph}"
            )
        
        # Detailed result
        st.markdown(f"""
        <div class="prediction-result">
            <h3>📊 Prediction Result</h3>
            <p><strong>Plastic:</strong> {prediction.plastic_type}</p>
            <p><strong>Microorganism:</strong> {prediction.microorganism}</p>
            <p><strong>Form:</strong> {plastic_form}</p>
            <p><strong>Notes:</strong> {prediction.notes}</p>
            <p><strong>Source:</strong> {source}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Prediction details
        st.subheader("📊 Prediction Details")
        
        details_col1, details_col2 = st.columns(2)
        
        with details_col1:
            st.write("**Environmental Conditions:**")
            st.write(f"🌡️ Temperature: {prediction.conditions['temperature']}°C")
            st.write(f"💧 Humidity: {prediction.conditions['humidity']}%")
            st.write(f"⚗️ pH: {prediction.conditions['ph']}")
            st.write(f"📦 Form: {prediction.conditions['plastic_form']}")
        
        with details_col2:
            st.write("**Parameters:**")
            st.write(f"🧪 Plastic: {prediction.plastic_type}")
            st.write(f"🦠 Microorganism: {prediction.microorganism}")
            st.write(f"📋 Source: Scientific literature + API")
        
        # Charts
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
    
    # Comparative analysis section
    st.header("📈 Comparative Analysis")
    
    if st.button("🔄 Generate Comparison Scenarios"):
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
        
        # Comparison table
        comparison_df = pd.DataFrame([
            {
                'Plastic': p.plastic_type,
                'Microorganism': p.microorganism,
                'Temperature (°C)': p.conditions['temperature'],
                'Humidity (%)': p.conditions['humidity'],
                'pH': p.conditions['ph'],
                'Time (days)': p.degradation_time_days,
                'Degradation (%)': p.weight_loss_percentage,
                'Confidence': f"{p.confidence:.2f}"
            }
            for p in predictions_list
        ])
        
        st.subheader("📋 Comparative Table")
        st.dataframe(comparison_df, use_container_width=True)
    
    # Literature data section
    st.header("📚 Literature Data")
    
    df = load_degradation_data()
    if not df.empty:
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            selected_plastic = st.selectbox(
                "Filter by Plastic",
                options=['All'] + list(df['Plastic'].unique()) if 'Plastic' in df.columns else ['All']
            )
        
        with col2:
            selected_organism = st.selectbox(
                "Filter by Microorganism",
                options=['All'] + list(df['Microorganism'].unique()) if 'Microorganism' in df.columns else ['All']
            )
        
        # Apply filters
        filtered_df = df.copy()
        if selected_plastic != 'All' and 'Plastic' in df.columns:
            filtered_df = filtered_df[filtered_df['Plastic'] == selected_plastic]
        if selected_organism != 'All' and 'Microorganism' in df.columns:
            filtered_df = filtered_df[filtered_df['Microorganism'] == selected_organism]
        
        # Show filtered data
        if not filtered_df.empty:
            st.dataframe(
                filtered_df[['Microorganism', 'Plastic', 'Enzyme', 'Year', 'Isolation_location']].head(20)
                if all(col in filtered_df.columns for col in ['Microorganism', 'Plastic', 'Enzyme', 'Year', 'Isolation_location'])
                else filtered_df.head(20),
                use_container_width=True
            )
        else:
            st.info("No data found with the selected filters.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Plastic Degradation Dashboard by Fungi | 
        Based on scientific literature and predictive models</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()