# 🧪 Plastic Degradation by Fungi Dashboard

> Intelligent system for prediction and analysis of plastic biodegradation by fungal microorganisms

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/seu-usuario/plastic-degradation-dashboard.git
cd plastic-degradation-dashboard

# Run the application (automatically installs dependencies)
python run_app.py
```

**🌐 Access:** `http://localhost:8501`

## ✨ Main Features

- 🔮 **Predictive Model**: Based on 2,432 scientific studies
- 📊 **Interactive Dashboard**: Modern web interface with Streamlit
- 📈 **Advanced Visualizations**: 3D charts, heat maps, temporal analysis
- 🧬 **857 Microorganisms**: Cataloged fungi and bacteria
- 🔬 **71 Plastic Types**: PVC, PE, PET, PS, PP, PLA, PHB and more

## 🔬 Functionalities

### Intelligent Prediction
- Environmental factors (temperature, humidity, pH)
- Multiple plastic forms
- Statistical confidence
- Scientific validation

### Available Analyses
- Degradation timeline
- Efficiency heat maps
- Sensitivity analysis
- Scenario comparison
- Statistical distributions

## 📊 Database

- **2,432 records** from scientific studies (1974-2023)
- **857 unique microorganisms**
- **71 plastic types**
- **80 identified enzymes**
- **416 evidence types**

## 🛠️ Technologies

- **Python 3.8+** - Backend and analysis
- **Streamlit** - Web interface
- **Plotly** - Interactive visualizations
- **SQLite** - Database
- **Pandas/NumPy** - Data processing

## 📁 Structure

```
📦 Project/
├── 🔮 prediction_model.py      # Prediction model
├── 📊 dashboard_app.py         # Web interface
├── 📈 visualization_utils.py   # Visualizations
├── 🚀 run_app.py              # Automatic execution
├── 🗄️ degradation_data.db     # Database
└── 📋 requirements.txt        # Dependencies
```

## 🧬 Usage Example

```python
from prediction_model import PlasticDegradationPredictor

predictor = PlasticDegradationPredictor()

prediction = predictor.predict_degradation(
    plastic_type="PVC",
    microorganism="Aspergillus niger",
    temperature=27.0,
    humidity=14.0,
    ph=4.0,
    plastic_form="pieces"
)

print(f"Time: {prediction.degradation_time_days} days")
print(f"Degradation: {prediction.weight_loss_percentage}%")
```

## 🎯 Use Cases

- **🎓 Academic Research**: Experiment planning
- **🏭 Industry**: Biodegradability assessment
- **🌱 Sustainability**: Environmental studies
- **📚 Education**: Biotechnology teaching

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🙏 Acknowledgments

- Scientific community for data availability
- Streamlit and Plotly developers
- Environmental biotechnology researchers

---

<div align="center">

**🌍 Contributing to a more sustainable future through science**

[⭐ Star](../../stargazers) • [🐛 Issues](../../issues) • [💡 Features](../../issues)

</div>