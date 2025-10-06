#!/usr/bin/env python3
"""
Script principal para executar a aplicação de predição de degradação de plásticos
"""

import subprocess
import sys
import os
from pathlib import Path

def check_requirements():
    """Verifica se as dependências estão instaladas"""
    try:
        import streamlit
        import plotly
        import pandas
        import numpy
        print("✅ Todas as dependências estão instaladas")
        return True
    except ImportError as e:
        print(f"❌ Dependência faltando: {e}")
        return False

def install_requirements():
    """Instala as dependências necessárias"""
    print("📦 Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências")
        return False

def run_streamlit_app():
    """Executa a aplicação Streamlit"""
    print("🚀 Iniciando aplicação...")
    
    # Configurações do Streamlit
    config_args = [
        "--server.port=8501",
        "--server.address=localhost",
        "--server.headless=false",
        "--browser.gatherUsageStats=false",
        "--theme.primaryColor=#1f77b4",
        "--theme.backgroundColor=#ffffff",
        "--theme.secondaryBackgroundColor=#f0f2f6"
    ]
    
    cmd = [sys.executable, "-m", "streamlit", "run", "dashboard_app.py"] + config_args
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n👋 Aplicação encerrada pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao executar aplicação: {e}")

def main():
    """Função principal"""
    print("🧪 Dashboard de Degradação de Plásticos por Fungos")
    print("=" * 50)
    
    # Verificar se estamos no diretório correto
    if not Path("dashboard_app.py").exists():
        print("❌ Arquivo dashboard_app.py não encontrado no diretório atual")
        print("Certifique-se de estar no diretório correto")
        return
    
    # Verificar dependências
    if not check_requirements():
        print("\n📦 Instalando dependências necessárias...")
        if not install_requirements():
            print("❌ Falha na instalação das dependências")
            return
    
    print("\n🌐 A aplicação será aberta em: http://localhost:8501")
    print("💡 Para parar a aplicação, pressione Ctrl+C")
    print("-" * 50)
    
    # Executar aplicação
    run_streamlit_app()

if __name__ == "__main__":
    main()