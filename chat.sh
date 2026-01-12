#!/bin/bash

# Script para executar o chat com ambiente virtual ativado
# Sistema de Ingestão e Busca Semântica com RAG

set -e

# Verificar se está no diretório correto
if [ ! -f "src/chat.py" ]; then
    echo "❌ Erro: Execute este script da raiz do projeto"
    exit 1
fi

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "❌ Erro: Ambiente virtual não encontrado"
    echo "Execute primeiro: ./install.sh"
    exit 1
fi

# Ativar ambiente virtual e executar chat
source venv/bin/activate
python src/chat.py
# Script para executar o chat com ambiente virtual ativado


