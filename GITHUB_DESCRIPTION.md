# 🧪 Dashboard de Degradação de Plásticos por Fungos

> **Sistema inteligente de predição e análise da biodegradação de plásticos por microrganismos fúngicos**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-5.0+-green.svg)](https://plotly.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 Visão Geral

Este projeto oferece uma **plataforma completa** para análise e predição da degradação de plásticos por fungos, combinando dados científicos reais com modelos preditivos avançados. Ideal para pesquisadores, estudantes e profissionais interessados em **biotecnologia ambiental** e **sustentabilidade**.

### ✨ Principais Características

- 🔮 **Modelo Preditivo Inteligente**: Baseado em literatura científica peer-reviewed
- 📊 **Dashboard Interativo**: Interface web moderna e intuitiva
- 📈 **Visualizações Avançadas**: Gráficos 3D, mapas de calor, análise temporal
- 🗄️ **Base de Dados Científica**: 2.432 registros de estudos de biodegradação
- 🧬 **Múltiplos Microrganismos**: 857 fungos e bactérias catalogados
- 🔬 **Diversos Plásticos**: 71 tipos diferentes (PVC, PE, PET, PS, PP, PLA, PHB, etc.)

## 🚀 Demo Rápido

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/plastic-degradation-dashboard.git
cd plastic-degradation-dashboard

# Execute a aplicação (instala dependências automaticamente)
python run_app.py
```

**🌐 Acesse:** `http://localhost:8501`

## 📸 Screenshots

### Dashboard Principal
![Dashboard](https://via.placeholder.com/800x400/1f77b4/ffffff?text=Dashboard+Principal)

### Análise 3D
![Análise 3D](https://via.placeholder.com/800x400/2ca02c/ffffff?text=Visualização+3D)

### Predições em Tempo Real
![Predições](https://via.placeholder.com/800x400/ff7f0e/ffffff?text=Predições+Interativas)

## 🔬 Funcionalidades Científicas

### 🎯 Modelo de Predição
- **Fatores Ambientais**: Temperatura (10-45°C), Umidade (10-95%), pH (2-12)
- **Formas de Plástico**: Peças, microplásticos, filmes, pó
- **Confiança Estatística**: Cada predição inclui nível de confiança
- **Validação Científica**: Baseado em estudos como Aspergillus niger, Candida albicans

### 📊 Análises Disponíveis
- **Timeline de Degradação**: Evolução temporal da biodegradação
- **Mapas de Calor**: Eficiência por combinação de parâmetros
- **Análise de Sensibilidade**: Impacto de cada variável
- **Comparação de Cenários**: Múltiplas condições simultaneamente
- **Distribuições Estatísticas**: Intervalos de confiança

### 🗃️ Base de Dados
- **2.432 registros** de estudos científicos
- **857 microrganismos** únicos catalogados
- **71 tipos de plásticos** diferentes
- **80 enzimas** identificadas
- **Período**: Estudos de 1974-2023

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.8+
- **Interface**: Streamlit
- **Visualizações**: Plotly, Matplotlib
- **Dados**: SQLite, Pandas, NumPy
- **Análise**: SciPy, Scikit-learn

## 📁 Estrutura do Projeto

```
📦 plastic-degradation-dashboard/
├── 🔮 prediction_model.py      # Modelo de predição principal
├── 📊 dashboard_app.py         # Interface web Streamlit
├── 📈 visualization_utils.py   # Utilitários de visualização
├── 🚀 run_app.py              # Script de execução automática
├── 🗄️ degradation_data.db     # Base de dados SQLite
├── 📋 requirements.txt        # Dependências Python
├── 🔧 setup_db.py             # Configuração da base de dados
└── 📖 README.md               # Documentação completa
```

## 🧬 Exemplo de Uso

```python
from prediction_model import PlasticDegradationPredictor

# Inicializar o modelo
predictor = PlasticDegradationPredictor()

# Fazer predição
prediction = predictor.predict_degradation(
    plastic_type="PVC",
    microorganism="Aspergillus niger",
    temperature=27.0,
    humidity=14.0,
    ph=4.0,
    plastic_form="pieces"
)

print(f"Tempo para degradação: {prediction.degradation_time_days} dias")
print(f"Perda de peso: {prediction.weight_loss_percentage}%")
print(f"Confiança: {prediction.confidence:.2f}")
```

## 📈 Casos de Uso

### 🎓 **Pesquisa Acadêmica**
- Planejamento de experimentos de biodegradação
- Análise comparativa de microrganismos
- Otimização de condições experimentais

### 🏭 **Indústria**
- Avaliação de biodegradabilidade de produtos
- Desenvolvimento de plásticos biodegradáveis
- Análise de impacto ambiental

### 🌱 **Sustentabilidade**
- Estudos de decomposição de resíduos plásticos
- Avaliação de tecnologias de biorremediação
- Educação ambiental

## 🤝 Contribuindo

Contribuições são bem-vindas! Veja como ajudar:

1. **Fork** o projeto
2. **Crie** uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)
5. **Abra** um Pull Request

### 🎯 Áreas para Contribuição
- 📊 Novas visualizações e análises
- 🔬 Integração de novos dados científicos
- 🚀 Otimização de performance
- 🌐 Internacionalização
- 📱 Interface mobile

## 📚 Referências Científicas

O projeto é baseado em estudos científicos peer-reviewed, incluindo:

- **Biodegradation studies** - PubMed: 39502512
- **Fungal degradation mechanisms** - Diversos estudos catalogados
- **Environmental factors** - Literatura especializada em biotecnologia

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- Comunidade científica pela disponibilização de dados
- Desenvolvedores do Streamlit e Plotly
- Pesquisadores em biotecnologia ambiental

---

<div align="center">

**🌍 Contribuindo para um futuro mais sustentável através da ciência** 

[⭐ Star](../../stargazers) • [🐛 Report Bug](../../issues) • [💡 Request Feature](../../issues)

</div>