# 🧪 Python Interface for Plastic Degradation by Fungi Prediction

This application provides a complete interface for prediction and analysis of plastic degradation by fungal microorganisms, based on scientific literature and advanced predictive models.

## 📋 Main Features

### 🔮 Prediction Model
- **Scientific literature-based prediction**: Uses data from studies such as Aspergillus niger, Candida albicans and Acremonium sclerotigenum
- **Environmental factors**: Considers temperature, relative humidity and pH
- **Plastic types**: Support for PVC, PE, PET, PS, PP, PLA, PHB
- **Plastic forms**: Pieces, microplastics, films and powder
- **Statistical confidence**: Each prediction includes confidence level

### 📊 Interactive Dashboard
- **Modern web interface**: Developed with Streamlit
- **Advanced visualizations**: 3D charts, heat maps, sensitivity analysis
- **Comparative analysis**: Compare different scenarios simultaneously
- **Historical data**: Access to scientific literature database

### 📈 Available Visualizations
- Degradation timeline
- Environmental conditions radar charts
- Efficiency heat maps
- 3D response surfaces
- Sensitivity analysis
- Uncertainty bands
- Statistical distributions

## 🚀 How to Use

### Quick Installation

1. **Run the main script**:
   ```bash
   python run_app.py
   ```
   
   The script automatically:
   - Checks dependencies
   - Installs necessary packages
   - Starts the web application

2. **Access the application**:
   - Open your browser at: `http://localhost:8501`

### Manual Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   streamlit run dashboard_app.py
   ```

## 📁 File Structure

```
📦 Python Interface
├── 🔮 prediction_model.py      # Main prediction model
├── 📊 dashboard_app.py         # Streamlit web interface
├── 📈 visualization_utils.py   # Visualization utilities
├── 🚀 run_app.py              # Execution script
├── 📋 requirements.txt        # Python dependencies
└── 📖 README_PYTHON.md        # This documentation
```

## 🔬 Model Usage Example

### Basic Prediction

```python
from prediction_model import PlasticDegradationPredictor

# Initialize the model
predictor = PlasticDegradationPredictor()

# Make prediction (based on provided example)
prediction = predictor.predict_degradation(
    plastic_type="PVC",
    microorganism="Aspergillus niger",
    temperature=27.0,
    humidity=14.0,
    ph=4.0,
    plastic_form="pieces"
)

print(f"Time to degradation: {prediction.time_to_observable_degradation} days")
print(f"Expected weight loss: {prediction.expected_weight_loss}%")
print(f"Confidence: {prediction.confidence}")
```

### Batch Analysis

```python
# Define multiple scenarios
scenarios = [
    {'plastic_type': 'PVC', 'microorganism': 'Aspergillus niger', 
     'temperature': 25, 'humidity': 60, 'ph': 5},
    {'plastic_type': 'PE', 'microorganism': 'Aspergillus niger', 
     'temperature': 30, 'humidity': 70, 'ph': 4},
    # ... more scenarios
]

# Execute batch predictions
predictions = predictor.batch_predict(scenarios)
```

## 📊 Dashboard Features

### 1. **Prediction Panel**
- Parameter selection via intuitive interface
- Sliders for environmental conditions
- Real-time results

### 2. **Interactive Visualizations**
- **Degradation Timeline**: Shows temporal evolution
- **Conditions Radar**: Compares current vs optimal conditions
- **Comparative Analysis**: Multiple scenarios simultaneously

### 3. **Advanced Analysis**
- **Heat Maps**: Efficiency by parameter combination
- **3D Surfaces**: Effect of temperature and humidity
- **Sensitivity Analysis**: Impact of each parameter

### 4. **Historical Data**
- Access to scientific database
- Filters by plastic and microorganism
- Enzyme and gene information

## 🧬 Scientific Basis

### Integrated Literature Data

The model incorporates specific data from scientific studies:

- **Aspergillus niger + PVC**: 
  - Pieces: ~60 days, 25% degradation
  - Microplastics: ~30 days, 16% degradation

- **Acremonium sclerotigenum**:
  - PET: ~30 days, 6% degradation
  - PS: ~30 days, 10% degradation

### Correction Factors

- **Temperature**: Optimal ~30°C, Arrhenius factor
- **Humidity**: Optimal 60-80%, fungal growth
- **pH**: Optimal 4-6 for most fungi
- **Form**: Microplastics degrade faster

## 🎯 Results Interpretation

### Confidence Levels
- **High (>0.7)**: Robust literature data
- **Medium (0.4-0.7)**: Limited or extrapolated data
- **Low (<0.4)**: Estimates based on similarity

### Explanatory Notes
The system provides automatic notes about:
- Favorable/unfavorable conditions
- Temperature/humidity/pH limitations
- Plastic form effects

## 🔧 Customization

### Adding New Data

To add new scientific data, edit the `prediction_model.py` file:

```python
self.literature_data = {
    'New_Fungus': {
        'NEW_PLASTIC': {
            'microplastics': {'time': X, 'degradation': Y, 'confidence': Z}
        }
    }
}
```

### Customizing Visualizations

Edit `visualization_utils.py` to:
- Add new chart types
- Modify color palettes
- Create specific analyses

## 📚 Scientific References

The model is based on scientific studies including:

1. **Aspergillus niger, Candida albicans, and Acremonium sclerotigenum** - Biodegradation of PE, PET, and PS microplastics (PubMed: 39502512)

2. **Degrader database** - File `degraders_list_with_images.json` with hundreds of cataloged microorganisms

## 🤝 Contributions

To contribute to the project:
1. Add new scientific data
2. Improve prediction algorithms
3. Create new visualizations
4. Optimize performance

## 📞 Support

For questions or issues:
- Check that all dependencies are installed
- Confirm that the `degraders_list_with_images.json` file is present
- Run `python run_app.py` for automatic diagnosis

---

**Developed for scientific analysis of plastic biodegradation** 🌱