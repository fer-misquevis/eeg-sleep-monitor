# Início Rápido - EEG Sleep Monitor

## 🚀 Start em 3 passos

### 1. Instale dependências
```bash
cd eeg-sleep-monitor
pip install -r requirements.txt
pip install muselsl
```

### 2. Inicie o stream do Muse
```bash
muselsl stream
```

### 3. Execute o sistema
```bash
python run.py
```

O navegador abrirá automaticamente! 🎉

## 📖 Documentação Completa

- **README.md** - Visão geral e documentação completa
- **docs/setup.md** - Guia detalhado de instalação
- **http://localhost:8000/docs** - API interativa (após iniciar)

## 🆘 Problemas?

```bash
# Verificar se Muse está conectado
muselsl list

# Reiniciar stream
muselsl stream

# Testar em porta diferente
python run.py --port 5000

# Modo debug (reload automático)
python run.py --debug
```

## 📁 Estrutura do Projeto

```
eeg-sleep-monitor/
├── src/
│   ├── main.py              # 🚀 Servidor FastAPI
│   └── analysis/            # 🧠 Algoritmos de análise
│       ├── bandpower.py     # Cálculo de potências
│       ├── spindles.py      # Detecção de spindles
│       └── sleep_stages.py  # Classificação de sono
├── static/
│   └── index.html           # 🎨 Dashboard web
├── docs/
│   └── setup.md             # 📖 Guia completo
├── run.py                   # ⚡ Script de inicialização
├── requirements.txt         # 📦 Dependências
└── README.md                # 📚 Documentação
```

## 🎯 O que o sistema faz

✅ Captura sinais EEG em tempo real (256 Hz)  
✅ Analisa 4 bandas de frequência (Delta, Theta, Alpha, Beta)  
✅ Detecta spindles do sono (característica do N2)  
✅ Classifica estágios: Acordado, N1, N2, N3, REM  
✅ Dashboard interativo com gráficos em tempo real  

## 💡 Dicas

- Use o canal AF7 (frontal esquerdo) para melhor detecção de sono
- Janela de 3 segundos = atualização a cada 3s no dashboard
- Spindles são detectados quando sigma > 2.5x baseline
- Mantenha-se parado para melhor qualidade de sinal

---

**Bom monitoramento! 😴📊**
