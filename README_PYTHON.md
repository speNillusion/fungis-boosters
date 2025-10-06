# 🧪 Interface Python para Predição de Degradação de Plásticos por Fungos

Esta aplicação fornece uma interface completa para predição e análise da degradação de plásticos por microrganismos fúngicos, baseada em literatura científica e modelos preditivos avançados.

## 📋 Características Principais

### 🔮 Modelo de Predição
- **Predição baseada em literatura científica**: Utiliza dados de estudos como o de Aspergillus niger, Candida albicans e Acremonium sclerotigenum
- **Fatores ambientais**: Considera temperatura, umidade relativa e pH
- **Tipos de plástico**: Suporte para PVC, PE, PET, PS, PP, PLA, PHB
- **Formas de plástico**: Peças, microplásticos, filmes e pó
- **Confiança estatística**: Cada predição inclui nível de confiança

### 📊 Dashboard Interativo
- **Interface web moderna**: Desenvolvida com Streamlit
- **Visualizações avançadas**: Gráficos 3D, mapas de calor, análise de sensibilidade
- **Análise comparativa**: Compare diferentes cenários simultaneamente
- **Dados históricos**: Acesso à base de dados da literatura científica

### 📈 Visualizações Disponíveis
- Timeline de degradação
- Gráficos radar de condições ambientais
- Mapas de calor de eficiência
- Superfícies 3D de resposta
- Análise de sensibilidade
- Bandas de incerteza
- Distribuições estatísticas

## 🚀 Como Usar

### Instalação Rápida

1. **Execute o script principal**:
   ```bash
   python run_app.py
   ```
   
   O script automaticamente:
   - Verifica dependências
   - Instala pacotes necessários
   - Inicia a aplicação web

2. **Acesse a aplicação**:
   - Abra seu navegador em: `http://localhost:8501`

### Instalação Manual

1. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Execute a aplicação**:
   ```bash
   streamlit run dashboard_app.py
   ```

## 📁 Estrutura dos Arquivos

```
📦 Interface Python
├── 🔮 prediction_model.py      # Modelo de predição principal
├── 📊 dashboard_app.py         # Interface web Streamlit
├── 📈 visualization_utils.py   # Utilitários de visualização
├── 🚀 run_app.py              # Script de execução
├── 📋 requirements.txt        # Dependências Python
└── 📖 README_PYTHON.md        # Esta documentação
```

## 🔬 Exemplo de Uso do Modelo

### Predição Básica

```python
from prediction_model import PlasticDegradationPredictor

# Inicializar o modelo
predictor = PlasticDegradationPredictor()

# Fazer predição (baseada no exemplo fornecido)
prediction = predictor.predict_degradation(
    plastic_type="PVC",
    microorganism="Aspergillus niger",
    temperature=27.0,
    humidity=14.0,
    ph=4.0,
    plastic_form="pieces"
)

print(f"Tempo para degradação: {prediction.time_to_observable_degradation} dias")
print(f"Perda de peso esperada: {prediction.expected_weight_loss}%")
print(f"Confiança: {prediction.confidence}")
```

### Análise em Lote

```python
# Definir múltiplos cenários
scenarios = [
    {'plastic_type': 'PVC', 'microorganism': 'Aspergillus niger', 
     'temperature': 25, 'humidity': 60, 'ph': 5},
    {'plastic_type': 'PE', 'microorganism': 'Aspergillus niger', 
     'temperature': 30, 'humidity': 70, 'ph': 4},
    # ... mais cenários
]

# Executar predições em lote
predictions = predictor.batch_predict(scenarios)
```

## 📊 Funcionalidades do Dashboard

### 1. **Painel de Predição**
- Seleção de parâmetros via interface intuitiva
- Sliders para condições ambientais
- Resultados em tempo real

### 2. **Visualizações Interativas**
- **Timeline de Degradação**: Mostra evolução temporal
- **Radar de Condições**: Compara condições atuais vs ótimas
- **Análise Comparativa**: Múltiplos cenários simultaneamente

### 3. **Análise Avançada**
- **Mapas de Calor**: Eficiência por combinação de parâmetros
- **Superfícies 3D**: Efeito de temperatura e umidade
- **Análise de Sensibilidade**: Impacto de cada parâmetro

### 4. **Dados Históricos**
- Acesso à base de dados científica
- Filtros por plástico e microrganismo
- Informações de enzimas e genes

## 🧬 Base Científica

### Dados da Literatura Integrados

O modelo incorpora dados específicos de estudos científicos:

- **Aspergillus niger + PVC**: 
  - Peças: ~60 dias, 25% degradação
  - Microplásticos: ~30 dias, 16% degradação

- **Acremonium sclerotigenum**:
  - PET: ~30 dias, 6% degradação
  - PS: ~30 dias, 10% degradação

### Fatores de Correção

- **Temperatura**: Ótima ~30°C, fator de Arrhenius
- **Umidade**: Ótima 60-80%, crescimento fúngico
- **pH**: Ótimo 4-6 para maioria dos fungos
- **Forma**: Microplásticos degradam mais rápido

## 🎯 Interpretação dos Resultados

### Níveis de Confiança
- **Alta (>0.7)**: Dados robustos da literatura
- **Média (0.4-0.7)**: Dados limitados ou extrapolados
- **Baixa (<0.4)**: Estimativas baseadas em similaridade

### Notas Explicativas
O sistema fornece notas automáticas sobre:
- Condições favoráveis/desfavoráveis
- Limitações de temperatura/umidade/pH
- Efeitos da forma do plástico

## 🔧 Personalização

### Adicionando Novos Dados

Para adicionar novos dados científicos, edite o arquivo `prediction_model.py`:

```python
self.literature_data = {
    'Novo_Fungo': {
        'NOVO_PLASTICO': {
            'microplastics': {'time': X, 'degradation': Y, 'confidence': Z}
        }
    }
}
```

### Customizando Visualizações

Edite `visualization_utils.py` para:
- Adicionar novos tipos de gráficos
- Modificar paletas de cores
- Criar análises específicas

## 📚 Referências Científicas

O modelo é baseado em estudos científicos incluindo:

1. **Aspergillus niger, Candida albicans, and Acremonium sclerotigenum** - Biodegradation of PE, PET, and PS microplastics (PubMed: 39502512)

2. **Base de dados de degradadores** - Arquivo `degraders_list_with_images.json` com centenas de microrganismos catalogados

## 🤝 Contribuições

Para contribuir com o projeto:
1. Adicione novos dados científicos
2. Melhore algoritmos de predição
3. Crie novas visualizações
4. Otimize performance

## 📞 Suporte

Para dúvidas ou problemas:
- Verifique se todas as dependências estão instaladas
- Confirme que o arquivo `degraders_list_with_images.json` está presente
- Execute `python run_app.py` para diagnóstico automático

---

**Desenvolvido para análise científica de biodegradação de plásticos** 🌱