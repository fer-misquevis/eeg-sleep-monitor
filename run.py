#!/usr/bin/env python
"""
Script de inicialização rápida do EEG Sleep Monitor

Uso:
    python run.py              # Inicia servidor padrão
    python run.py --port 5000  # Inicia em porta customizada
    python run.py --debug      # Modo debug com reload
"""

import sys
import argparse
from pathlib import Path

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))


def main():
    parser = argparse.ArgumentParser(description="EEG Sleep Monitor")
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host para bind (padrão: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Porta para servidor (padrão: 8000)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Ativa modo debug com reload automático"
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Não abre navegador automaticamente"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🧠 EEG Sleep Monitor v1.0.0")
    print("=" * 60)
    print(f"\n📡 Servidor iniciando em: http://{args.host}:{args.port}")
    print(f"🌐 Dashboard: http://localhost:{args.port}/static/index.html")
    print(f"📚 API Docs: http://localhost:{args.port}/docs")
    print("\n⚠️  Certifique-se de que 'muselsl stream' está rodando!")
    print("=" * 60)
    print()
    
    # Abre navegador se não desabilitado
    if not args.no_browser:
        import webbrowser
        import time
        import threading
        
        def open_browser():
            time.sleep(2)  # Aguarda servidor iniciar
            url = f"http://localhost:{args.port}/static/index.html"
            print(f"🌐 Abrindo navegador: {url}")
            webbrowser.open(url)
        
        threading.Thread(target=open_browser, daemon=True).start()
    
    # Inicia servidor
    import uvicorn
    from main import app
    
    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        reload=args.debug,
        log_level="info"
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Encerrando servidor...")
        sys.exit(0)
