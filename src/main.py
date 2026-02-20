"""
EEG Sleep Monitor - API FastAPI

API para monitoramento em tempo real de sinais EEG e classificação de
estágios de sono usando Muse headband e LSL (Lab Streaming Layer).
"""

import asyncio
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from pylsl import StreamInlet, resolve_byprop
import numpy as np

from analysis import bandpower, detect_spindles, estimate_sleep_stage


# Configuração da aplicação
app = FastAPI(
    title="EEG Sleep Monitor",
    description="Sistema de monitoramento em tempo real de sinais EEG para análise de sono",
    version="1.0.0"
)

# Serve arquivos estáticos (HTML, CSS, JS)
static_path = Path(__file__).parent.parent / "static"
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# Variável global para o stream EEG
inlet = None


@app.get("/")
def home():
    """Endpoint raiz - Status da API"""
    return {
        "status": "API rodando",
        "version": "1.0.0",
        "endpoints": {
            "info": "/eeg",
            "websocket": "/ws/eeg",
            "dashboard": "/static/index.html"
        }
    }


@app.get("/eeg")
def eeg_info():
    """Retorna informações sobre o stream EEG"""
    return {
        "message": "Use WebSocket para conectar ao stream EEG",
        "endpoint": "ws://localhost:8000/ws/eeg",
        "status": "conectado" if inlet else "desconectado",
        "sample_rate": 256,
        "channels": ["AF7", "AF8", "TP9", "TP10"],
        "bands": {
            "delta": "0.5-4 Hz (sono profundo)",
            "theta": "4-8 Hz (sono REM, meditação)",
            "alpha": "8-12 Hz (relaxamento)",
            "beta": "13-30 Hz (atividade mental)",
            "sigma": "11-16 Hz (spindles N2)"
        }
    }


@app.on_event("startup")
async def startup():
    """Inicializa a conexão com o stream EEG na inicialização"""
    global inlet
    print("🔍 Procurando stream EEG...")
    streams = resolve_byprop('type', 'EEG', timeout=5)
    
    if not streams:
        print("⚠️  Nenhum stream EEG encontrado.")
        print("💡 Certifique-se de que 'muselsl stream' está rodando.")
        return
    
    inlet = StreamInlet(streams[0])
    print("✅ EEG conectado com sucesso!")


@app.websocket("/ws/eeg")
async def eeg_stream(websocket: WebSocket):
    """
    WebSocket para streaming de dados EEG em tempo real.
    
    Envia dados processados a cada 3 segundos:
    - Bandas de frequência (Delta, Theta, Alpha, Beta)
    - Estágio de sono estimado
    - Detecção de spindles
    """
    await websocket.accept()

    # Buffers e configurações
    buffer = []
    sigma_history = []  # Histórico para detecção de spindles
    sf = 256  # Frequência de amostragem (Hz)
    window_size = sf * 3  # Janela de 3 segundos
    
    print("🟢 Cliente WebSocket conectado")

    try:
        while True:
            if inlet is None:
                await websocket.send_json({
                    "error": "Stream EEG não disponível",
                    "message": "Execute 'muselsl stream' primeiro"
                })
                await asyncio.sleep(1)
                continue

            # Coleta uma amostra do stream
            sample, timestamp = inlet.pull_sample()
            buffer.append(sample[1])  # Canal AF7 (frontal esquerdo)

            # Processa quando temos uma janela completa
            if len(buffer) >= window_size:
                signal = np.array(buffer)

                # Calcula potências das bandas de frequência
                features = {
                    "delta": bandpower(signal, sf, (0.5, 4)),
                    "theta": bandpower(signal, sf, (4, 8)),
                    "alpha": bandpower(signal, sf, (8, 12)),
                    "beta": bandpower(signal, sf, (13, 30)),
                }

                # Detecta spindles (característicos do N2)
                spindle_detected, sigma_power, spindle_index = detect_spindles(
                    signal, sf, sigma_history
                )

                # Classifica estágio de sono
                sleep_stage = estimate_sleep_stage(
                    features["delta"],
                    features["theta"],
                    features["alpha"],
                    features["beta"]
                )

                # Envia resultados via WebSocket
                await websocket.send_json({
                    "timestamp": timestamp,
                    "bands": features,
                    "sleep_stage": sleep_stage,
                    "spindle_detected": bool(spindle_detected),
                    "sigma_power": float(sigma_power),
                    "spindle_index": float(round(spindle_index, 2))
                })

                buffer = []  # Limpa o buffer

            await asyncio.sleep(0.001)  # Pequeno delay para não sobrecarregar

    except WebSocketDisconnect:
        print("🔴 Cliente WebSocket desconectado (normal)")
    except Exception as e:
        print(f"🔥 ERRO: {repr(e)}")
        raise


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
