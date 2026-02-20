# Guia de Setup - EEG Sleep Monitor

Este guia detalha o processo de instalação e configuração do sistema.

## 🔌 Configuração do Muse Headband

### 1. Conectar via Bluetooth

#### Windows
1. Abra **Configurações** → **Dispositivos** → **Bluetooth**
2. Ligue o Muse (LED piscando)
3. Clique em **Adicionar Bluetooth ou outro dispositivo**
4. Selecione seu Muse na lista
5. Aguarde conectar

#### macOS
1. **Preferências do Sistema** → **Bluetooth**
2. Ligue o Muse
3. Clique em **Conectar** ao lado do dispositivo

#### Linux
```bash
bluetoothctl
scan on
# Aguarde aparecer o Muse
pair XX:XX:XX:XX:XX:XX
connect XX:XX:XX:XX:XX:XX
```

### 2. Testar Conexão

```bash
# Instalar muselsl
pip install muselsl

# Listar dispositivos
muselsl list

# Deve aparecer algo como:
# Found Muse: Muse-XXXX (XX:XX:XX:XX:XX:XX)
```

### 3. Iniciar Streaming

```bash
muselsl stream
```

Saída esperada:
```
Looking for Muse devices...
Found device: Muse-XXXX
Streaming started
Receiving data...
```

## 🐍 Instalação Python

### Opção 1: Instalação Manual

```bash
# Clonar repositório
git clone https://github.com/seu-usuario/eeg-sleep-monitor.git
cd eeg-sleep-monitor

# Criar ambiente virtual
python -m venv venv

# Ativar (Windows)
venv\Scripts\activate

# Ativar (Linux/macOS)
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
pip install muselsl
```

### Opção 2: Instalação via setup.py

```bash
pip install -e .
```

## 🚀 Executando o Sistema

### Modo Desenvolvimento

```bash
cd src
python main.py
```

Ou com reload automático:

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Modo Produção

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🌐 Acessando o Dashboard

Após iniciar o servidor:

1. Abra o navegador
2. Acesse: http://localhost:8000/static/index.html
3. Aguarde conexão (status deve ficar verde)

## 🔧 Configurações Avançadas

### Mudar Porta do Servidor

```bash
uvicorn src.main:app --port 5000
```

Ou editando `src/main.py`:
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
```

### Mudar Canal EEG

Edite `src/main.py`, linha ~120:

```python
# Canais disponíveis:
# 0 = AF7 (frontal esquerdo)
# 1 = AF8 (frontal direito)
# 2 = TP9 (temporal esquerdo)
# 3 = TP10 (temporal direito)

buffer.append(sample[0])  # Mude o índice aqui
```

### Ajustar Janela de Análise

```python
window_size = sf * 3  # 3 segundos (padrão)
window_size = sf * 5  # 5 segundos (mais suave)
window_size = sf * 1  # 1 segundo (mais responsivo)
```

## 📊 Verificando Qualidade do Sinal

### Via muselsl-viewer

```bash
pip install muselsl[viewer]
muselsl view
```

Isso abre uma janela com os sinais em tempo real.

### Critérios de Qualidade

✅ **Boa qualidade**:
- Ondas suaves e contínuas
- Sem picos extremos constantes
- Amplitude estável

❌ **Má qualidade**:
- Muitos artefatos (picos)
- Sinal cortando (desconexões)
- Ruído excessivo

### Melhorar Qualidade

1. **Posicionamento**: Ajuste o headband
2. **Contato**: Umedeça ligeiramente sensores
3. **Cabelo**: Afaste cabelos dos sensores
4. **Movimento**: Fique parado durante gravação

## 🐛 Solução de Problemas Comuns

### Erro: "No module named 'fastapi'"

```bash
pip install -r requirements.txt
```

### Erro: "Nenhum stream EEG encontrado"

1. Verifique Bluetooth conectado
2. Inicie `muselsl stream`
3. Aguarde 5-10 segundos antes de iniciar o servidor

### WebSocket desconecta constantemente

- **Causa**: Muse perdendo conexão Bluetooth
- **Solução**: 
  - Aproxime Muse do computador
  - Recarregue bateria
  - Reinicie Bluetooth

### Valores sempre zero

- **Causa**: Canal errado ou sem sinal
- **Verificar**: Use `muselsl view` para confirmar dados
- **Solução**: Ajuste posição do headband

### Erro: "Address already in use"

Porta 8000 já está em uso:

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/macOS
lsof -ti:8000 | xargs kill -9
```

## 📱 Acesso Remoto

Para acessar de outros dispositivos na rede:

1. Encontre seu IP:
```bash
# Windows
ipconfig

# Linux/macOS
ifconfig
```

2. Inicie com host 0.0.0.0:
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

3. Acesse de outro dispositivo:
```
http://<SEU_IP>:8000/static/index.html
```

## 🔒 Segurança

### Para uso em produção

1. **Use HTTPS**:
```bash
uvicorn src.main:app --ssl-keyfile=key.pem --ssl-certfile=cert.pem
```

2. **Adicione autenticação**:
```python
from fastapi.security import HTTPBasic
```

3. **Configure CORS** (se necessário):
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
)
```

## 📦 Criando Executável

### Windows (PyInstaller)

```bash
pip install pyinstaller

pyinstaller --onefile --add-data "static;static" src/main.py
```

### Alternativa: Docker

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0"]
```

Construir e executar:
```bash
docker build -t eeg-monitor .
docker run -p 8000:8000 eeg-monitor
```

## 📝 Testando em Modo Simulação

Se não tem Muse, pode simular dados:

```python
# Adicione em src/main.py
import random

def simulate_sample():
    return [random.random() for _ in range(4)], time.time()

# No websocket, substitua:
# sample, timestamp = inlet.pull_sample()
sample, timestamp = simulate_sample()
```

## ✅ Checklist de Instalação

- [ ] Python 3.8+ instalado
- [ ] Muse conectado via Bluetooth
- [ ] `muselsl stream` rodando
- [ ] Ambiente virtual criado
- [ ] Dependências instaladas
- [ ] Servidor FastAPI iniciado
- [ ] Dashboard acessível no navegador
- [ ] WebSocket conectado (status verde)
- [ ] Dados aparecem no gráfico

## 📞 Suporte

Se encontrar problemas:

1. Verifique as [Issues](https://github.com/seu-usuario/eeg-sleep-monitor/issues)
2. Consulte o [README.md](../README.md)
3. Abra uma nova issue com:
   - Versão do Python
   - Sistema operacional
   - Mensagem de erro completa
   - Passos para reproduzir

---

**Próximos passos**: Leia o [README.md](../README.md) para entender a arquitetura e funcionalidades!
