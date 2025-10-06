# 🧪 Dashboard de Degradação de Plásticos por Fungos

> Sistema inteligente de predição e análise da biodegradação de plásticos por microrganismos fúngicos

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚀 Início Rápido

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/plastic-degradation-dashboard.git
cd plastic-degradation-dashboard

# Execute a aplicação (instala dependências automaticamente)
python run_app.py
```

**🌐 Acesse:** `http://localhost:8501`

## ✨ Características Principais

- 🔮 **Modelo Preditivo**: Baseado em 2.432 estudos científicos
- 📊 **Dashboard Interativo**: Interface web moderna com Streamlit
- 📈 **Visualizações Avançadas**: Gráficos 3D, mapas de calor, análise temporal
- 🧬 **857 Microrganismos**: Fungos e bactérias catalogados
- 🔬 **71 Tipos de Plásticos**: PVC, PE, PET, PS, PP, PLA, PHB e mais

## 🔬 Funcionalidades

### Predição Inteligente
- Fatores ambientais (temperatura, umidade, pH)
- Múltiplas formas de plástico
- Confiança estatística
- Validação científica

### Análises Disponíveis
- Timeline de degradação
- Mapas de calor de eficiência
- Análise de sensibilidade
- Comparação de cenários
- Distribuições estatísticas

## 📊 Base de Dados

- **2.432 registros** de estudos científicos (1974-2023)
- **857 microrganismos** únicos
- **71 tipos de plásticos**
- **80 enzimas** identificadas
- **416 tipos de evidência**

## 🛠️ Tecnologias

- **Python 3.8+** - Backend e análise
- **Streamlit** - Interface web
- **Plotly** - Visualizações interativas
- **SQLite** - Base de dados
- **Pandas/NumPy** - Processamento de dados

## 📁 Estrutura

```
📦 Projeto/
├── 🔮 prediction_model.py      # Modelo de predição
├── 📊 dashboard_app.py         # Interface web
├── 📈 visualization_utils.py   # Visualizações
├── 🚀 run_app.py              # Execução automática
├── 🗄️ degradation_data.db     # Base de dados
└── 📋 requirements.txt        # Dependências
```

## 🧬 Exemplo de Uso

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

print(f"Tempo: {prediction.degradation_time_days} dias")
print(f"Degradação: {prediction.weight_loss_percentage}%")
```

## 🎯 Casos de Uso

- **🎓 Pesquisa Acadêmica**: Planejamento de experimentos
- **🏭 Indústria**: Avaliação de biodegradabilidade
- **🌱 Sustentabilidade**: Estudos ambientais
- **📚 Educação**: Ensino de biotecnologia

## 🤝 Contribuindo

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Distribuído sob a Licença MIT. Veja `LICENSE` para mais informações.

## 🙏 Agradecimentos

- Comunidade científica pela disponibilização de dados
- Desenvolvedores do Streamlit e Plotly
- Pesquisadores em biotecnologia ambiental

---

<div align="center">

**🌍 Contribuindo para um futuro mais sustentável através da ciência**

[⭐ Star](../../stargazers) • [🐛 Issues](../../issues) • [💡 Features](../../issues)

</div>