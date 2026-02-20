# 🧠 EEG Sleep Monitor

Sistema de monitoramento em tempo real de sinais EEG para análise e classificação automática de estágios de sono usando Muse headband.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Índice

- [Sobre](#sobre)
- [Funcionalidades](#funcionalidades)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Uso](#uso)
- [Arquitetura](#arquitetura)
- [API Endpoints](#api-endpoints)
- [Ciência por Trás](#ciência-por-trás)
- [Desenvolvimento](#desenvolvimento)

## 🎯 Sobre

O **EEG Sleep Monitor** é uma aplicação Python que captura sinais EEG em tempo real de um Muse headband via Lab Streaming Layer (LSL), processa esses sinais para extrair características relevantes, e classifica automaticamente os estágios de sono.

### O que faz:

- **Captura** sinais EEG em tempo real (256 Hz)
- **Analisa** bandas de frequência (Delta, Theta, Alpha, Beta)
- **Detecta** spindles do sono (característicos do estágio N2)
- **Classifica** estágios de sono (Acordado, N1, N2, N3, REM)
- **Visualiza** dados em dashboard web interativo

## ✨ Funcionalidades

### Análise de Sinais

- 📊 **Análise espectral**: Calcula potência em bandas de frequência via Welch PSD
- 🌀 **Detecção de spindles**: Identifica oscilações sigma (11-16 Hz) do estágio N2
- 😴 **Classificação de sono**: Estima estágios baseado em proporções de bandas

### Interface Web

- 🎨 **Dashboard em tempo real**: Visualização moderna com Chart.js
- 📈 **Gráficos interativos**: Plotagem contínua das 4 bandas principais
- 🔔 **Alertas visuais**: Indicador animado para detecção de spindles
- 📱 **Design responsivo**: Interface adaptável para diferentes telas

### API

- ⚡ **WebSocket**: Stream de dados em tempo real (atualização a cada 3s)
- 🔌 **REST endpoints**: Informações sobre status e configuração
- 📡 **FastAPI**: Framework moderno com documentação automática

## 🔧 Requisitos

### Hardware

- **Muse Headband** (Muse 2, Muse S, ou similar)
- Computador com Bluetooth

### Software

- Python 3.8 ou superior
- Sistema operacional: Windows, macOS ou Linux

### Dependências Python

```
fastapi==0.109.0
uvicorn[standard]==0.27.0
numpy==1.26.3
scipy==1.12.0
pylsl==1.16.2
```

## 📦 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/eeg-sleep-monitor.git
cd eeg-sleep-monitor
```

### 2. Crie um ambiente virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Instale o muselsl (para Muse headband)

```bash
pip install muselsl
```

## 🚀 Uso

### Passo 1: Inicie o stream do Muse

Conecte o headband e inicie o streaming LSL:

```bash
muselsl stream
```

Você deve ver:
```
Looking for Muse devices...
Found Muse: XX:XX:XX:XX:XX:XX
Streaming started
```

### Passo 2: Inicie o servidor

Em outro terminal, na pasta do projeto:

```bash
cd src
python main.py
```

Ou usando uvicorn diretamente:

```bash
uvicorn src.main:app --reload
```

Você verá:
```
🔍 Procurando stream EEG...
✅ EEG conectado com sucesso!
INFO: Uvicorn running on http://0.0.0.0:8000
```

### Passo 3: Abra o dashboard

Acesse no navegador:
```
http://localhost:8000/static/index.html
```

## 🏗️ Arquitetura

```
eeg-sleep-monitor/
├── src/
│   ├── main.py                 # API FastAPI
│   ├── __init__.py
│   └── analysis/               # Módulos de análise
│       ├── __init__.py
│       ├── bandpower.py        # Cálculo de potência
│       ├── spindles.py         # Detecção de spindles
│       └── sleep_stages.py     # Classificação de estágios
├── static/
│   └── index.html              # Dashboard web
├── docs/
│   └── setup.md
├── requirements.txt
├── .gitignore
└── README.md
```

### Fluxo de Dados

```
Muse Headband
    ↓ Bluetooth
muselsl stream (LSL)
    ↓ Lab Streaming Layer
FastAPI WebSocket
    ↓ Processamento
├─→ Análise de bandas (Welch PSD)
├─→ Detecção de spindles
└─→ Classificação de estágio
    ↓ JSON via WebSocket
Dashboard Web (Chart.js)
```

## 🌐 API Endpoints

### REST

#### `GET /`
Status da API e endpoints disponíveis

#### `GET /eeg`
Informações sobre o stream EEG
- Status de conexão
- Taxa de amostragem
- Canais disponíveis
- Bandas de frequência

### WebSocket

#### `WS /ws/eeg`
Stream de dados em tempo real

**Resposta (a cada 3 segundos):**
```json
{
  "timestamp": 1234567890.123,
  "bands": {
    "delta": 0.45,
    "theta": 0.32,
    "alpha": 0.18,
    "beta": 0.25
  },
  "sleep_stage": "N2 (Moderado)",
  "spindle_detected": true,
  "sigma_power": 0.42,
  "spindle_index": 2.8
}
```

### Documentação Interativa

FastAPI gera documentação automática:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Ciência por Trás

### Bandas de Frequência EEG

| Banda | Frequência | Associação |
|-------|------------|------------|
| **Delta (δ)** | 0.5-4 Hz | Sono profundo (N3), ondas lentas |
| **Theta (θ)** | 4-8 Hz | Sono REM, meditação profunda, N1 |
| **Alpha (α)** | 8-12 Hz | Relaxamento, olhos fechados acordado |
| **Beta (β)** | 13-30 Hz | Atividade mental, concentração |
| **Sigma (σ)** | 11-16 Hz | Spindles do sono (N2) |

### Estágios de Sono

#### Acordado
- Alta atividade Beta (13-30 Hz)
- Presença de Alpha posterior (8-12 Hz)

#### N1 (Sono Leve)
- Transição: Alpha diminui
- Theta (4-8 Hz) começa a aumentar
- Duração: 5-10 minutos

#### N2 (Sono Moderado)
- **Spindles**: Oscilações sigma (11-16 Hz), 0.5-2s
- K-complexes (não detectados nesta versão)
- ~50% do sono total

#### N3 (Sono Profundo / SWS)
- Delta (0.5-4 Hz) domina (>50%)
- Ondas lentas de alta amplitude
- Restauração física

#### REM
- Theta elevado (similar à vigília)
- Beta moderado
- Delta baixo
- Movimentos oculares rápidos
- Sonhos vívidos

### Detecção de Spindles

Algoritmo implementado:

1. Extrai potência na banda sigma (11-16 Hz) via Welch PSD
2. Mantém histórico das últimas 10 janelas
3. Calcula baseline (média das últimas medições)
4. Spindle detectado quando:
   - `sigma_power > 2.5 × baseline`
   - `sigma_power > 0.1` (limiar absoluto)

**Índice de Spindle**: Razão entre potência atual e baseline
- Valores > 2.5 indicam presença de spindle
- Quanto maior, mais confiante a detecção

## 🛠️ Desenvolvimento

### Executar em modo desenvolvimento

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Estrutura dos Módulos

#### `analysis/bandpower.py`
```python
def bandpower(data, sf, band) -> float
```
Calcula potência média usando Welch PSD

#### `analysis/spindles.py`
```python
def detect_spindles(signal, sf, history) -> (bool, float, float)
```
Retorna: (detectado, potência_sigma, índice)

#### `analysis/sleep_stages.py`
```python
def estimate_sleep_stage(delta, theta, alpha, beta) -> str
```
Retorna: "Acordado" | "N1" | "N2" | "N3" | "REM"

### Adicionar Novos Recursos

**Exemplo: Adicionar detecção de K-complexes**

1. Criar `src/analysis/k_complexes.py`
2. Implementar função de detecção
3. Importar em `src/main.py`
4. Adicionar ao WebSocket output
5. Atualizar dashboard em `static/index.html`

## 📊 Parâmetros Ajustáveis

### `src/main.py`

```python
sf = 256              # Taxa de amostragem (Hz)
window_size = sf * 3  # Janela de análise (3 segundos)
channel = sample[1]   # Canal EEG (0=AF7, 1=AF8, 2=TP9, 3=TP10)
```

### `analysis/spindles.py`

```python
SPINDLE_BAND = (11, 16)  # Banda sigma
HISTORY_SIZE = 10         # Tamanho do histórico
THRESHOLD_MULT = 2.5      # Multiplicador do baseline
MIN_POWER = 0.1           # Potência mínima
```

## 🐛 Troubleshooting

### "Nenhum stream EEG encontrado"

✅ Verifique se o Muse está conectado:
```bash
muselsl list
```

✅ Inicie o streaming:
```bash
muselsl stream
```

### "WebSocket não conecta"

✅ Verifique se o servidor está rodando em http://localhost:8000

✅ Verifique firewall/antivírus

### "Dados não aparecem no dashboard"

✅ Abra o console do navegador (F12) para ver erros

✅ Verifique se o WebSocket está conectado (status verde)

## 📝 Limitações

- **Canal único**: Usa apenas AF7 (frontal esquerdo)
- **Classificação simplificada**: Baseada apenas em proporções de bandas
- **Sem K-complexes**: N2 detecta apenas spindles
- **Tempo real limitado**: Janela de 3 segundos
- **Movimento artifacts**: Não há remoção de artefatos

## 🔮 Roadmap

- [ ] Detecção de K-complexes
- [ ] Multi-canal (usar todos os 4 canais)
- [ ] Remoção de artefatos (movimento, piscar)
- [ ] Machine Learning para classificação
- [ ] Gravação e replay de sessões
- [ ] Relatórios de sono (hipnograma)
- [ ] Modo offline (analisar arquivos)

## 📄 Licença

MIT License - veja LICENSE para detalhes

## 👥 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📚 Referências

- [Rechtschaffen & Kales (1968)](https://en.wikipedia.org/wiki/Rechtschaffen_and_Kales) - Critérios clássicos de staging
- [AASM Manual](https://aasm.org/) - Critérios modernos de sono
- [Welch PSD](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html) - Método de análise espectral
- [Lab Streaming Layer](https://labstreaminglayer.org/) - Protocolo LSL
- [Muse Headband](https://choosemuse.com/) - Hardware EEG

## 🙏 Agradecimentos

- **Interaxon** pelo Muse headband
- **Alexandre Barachant** pelo muselsl
- **FastAPI** pela excelente framework
- Comunidade open-source de neurociência

---

Desenvolvido com ❤️ e ☕ para pesquisa em neurociência do sono

**Aviso**: Este software é para fins educacionais e de pesquisa. Não deve ser usado para diagnóstico médico.
