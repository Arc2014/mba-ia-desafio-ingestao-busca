#!/bin/bash

# Script para executar a ingestão com ambiente virtual ativado
# Sistema de Ingestão e Busca Semântica com RAG

set -e

# Verificar se está no diretório correto
if [ ! -f "src/ingest.py" ]; then
    echo "❌ Erro: Execute este script da raiz do projeto"
    exit 1
fi

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "❌ Erro: Ambiente virtual não encontrado"
    echo "Execute primeiro: ./install.sh"
    exit 1
fi

# Ativar ambiente virtual e executar ingestão
source venv/bin/activate
python src/ingest.py

