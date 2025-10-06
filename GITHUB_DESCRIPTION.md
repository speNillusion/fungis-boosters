# 🧪 Plastic Degradation Dashboard by Fungi

> **Intelligent system for prediction and analysis of plastic biodegradation by fungal microorganisms**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-5.0+-green.svg)](https://plotly.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 Overview

This project offers a **complete platform** for analysis and prediction of plastic degradation by fungi, combining real scientific data with advanced predictive models. Ideal for researchers, students and professionals interested in **environmental biotechnology** and **sustainability**.

### ✨ Key Features

- 🔮 **Intelligent Predictive Model**: Based on peer-reviewed scientific literature
- 📊 **Interactive Dashboard**: Modern and intuitive web interface
- 📈 **Advanced Visualizations**: 3D charts, heat maps, temporal analysis
- 🗄️ **Scientific Database**: 2,432 biodegradation study records
- 🧬 **Multiple Microorganisms**: 857 cataloged fungi and bacteria
- 🔬 **Diverse Plastics**: 71 different types (PVC, PE, PET, PS, PP, PLA, PHB, etc.)

## 🚀 Quick Demo

```bash
# Clone the repository
git clone https://github.com/your-username/plastic-degradation-dashboard.git
cd plastic-degradation-dashboard

# Run the application (installs dependencies automatically)
python run_app.py
```

**🌐 Access:** `http://localhost:8501`

## 📸 Screenshots

### Main Dashboard
![Dashboard](https://via.placeholder.com/800x400/1f77b4/ffffff?text=Main+Dashboard)

### 3D Analysis
![3D Analysis](https://via.placeholder.com/800x400/2ca02c/ffffff?text=3D+Visualization)

### Real-time Predictions
![Predictions](https://via.placeholder.com/800x400/ff7f0e/ffffff?text=Interactive+Predictions)

## 🔬 Scientific Features

### 🎯 Prediction Model
- **Environmental Factors**: Temperature (10-45°C), Humidity (10-95%), pH (2-12)
- **Plastic Forms**: Pieces, microplastics, films, powder
- **Statistical Confidence**: Each prediction includes confidence level
- **Scientific Validation**: Based on studies like Aspergillus niger, Candida albicans

### 📊 Available Analyses
- **Degradation Timeline**: Temporal evolution of biodegradation
- **Heat Maps**: Efficiency by parameter combination
- **Sensitivity Analysis**: Impact of each variable
- **Scenario Comparison**: Multiple conditions simultaneously
- **Statistical Distributions**: Confidence intervals

### 🗃️ Database
- **2,432 records** of scientific studies
- **857 unique microorganisms** cataloged
- **71 different plastic types**
- **80 enzymes** identified
- **Period**: Studies from 1974-2023

## 🛠️ Technologies Used

- **Backend**: Python 3.8+
- **Interface**: Streamlit
- **Visualizations**: Plotly, Matplotlib
- **Data**: SQLite, Pandas, NumPy
- **Analysis**: SciPy, Scikit-learn

## 📁 Project Structure

```
📦 plastic-degradation-dashboard/
├── 🔮 prediction_model.py      # Main prediction model
├── 📊 dashboard_app.py         # Streamlit web interface
├── 📈 visualization_utils.py   # Visualization utilities
├── 🚀 run_app.py              # Automatic execution script
├── 🗄️ degradation_data.db     # SQLite database
├── 📋 requirements.txt        # Python dependencies
├── 🔧 setup_db.py             # Database configuration
└── 📖 README.md               # Complete documentation
```

## 🧬 Usage Example

```python
from prediction_model import PlasticDegradationPredictor

# Initialize the model
predictor = PlasticDegradationPredictor()

# Make prediction
prediction = predictor.predict_degradation(
    plastic_type="PVC",
    microorganism="Aspergillus niger",
    temperature=27.0,
    humidity=14.0,
    ph=4.0,
    plastic_form="pieces"
)

print(f"Time to degradation: {prediction.degradation_time_days} days")
print(f"Weight loss: {prediction.weight_loss_percentage}%")
print(f"Confidence: {prediction.confidence:.2f}")
```

## 📈 Use Cases

### 🎓 **Academic Research**
- Planning biodegradation experiments
- Comparative analysis of microorganisms
- Optimization of experimental conditions

### 🏭 **Industry**
- Product biodegradability assessment
- Development of biodegradable plastics
- Environmental impact analysis

### 🌱 **Sustainability**
- Plastic waste decomposition studies
- Bioremediation technology assessment
- Environmental education

## 🤝 Contributing

Contributions are welcome! Here's how to help:

1. **Fork** the project
2. **Create** a branch for your feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### 🎯 Areas for Contribution
- 📊 New visualizations and analyses
- 🔬 Integration of new scientific data
- 🚀 Performance optimization
- 🌐 Internationalization
- 📱 Mobile interface

## 📚 Scientific References

The project is based on peer-reviewed scientific studies, including:

- **Biodegradation studies** - PubMed: 39502512
- **Fungal degradation mechanisms** - Various cataloged studies
- **Environmental factors** - Specialized biotechnology literature

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Scientific community for data availability
- Streamlit and Plotly developers
- Environmental biotechnology researchers

---

<div align="center">

**🌍 Contributing to a more sustainable future through science** 

[⭐ Star](../../stargazers) • [🐛 Report Bug](../../issues) • [💡 Request Feature](../../issues)

</div>