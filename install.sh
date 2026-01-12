#!/bin/bash

# Script de instalação automática
# Sistema de Ingestão e Busca Semântica com RAG

set -e  # Exit on error

echo "=========================================="
echo "Instalação do Sistema RAG"
echo "=========================================="
echo ""

# 1. Verificar se está no diretório correto
if [ ! -f "requirements.txt" ]; then
    echo "❌ Erro: requirements.txt não encontrado"
    echo "Execute este script da raiz do projeto"
    exit 1
fi

# 2. Criar virtual environment
echo "1. Criando ambiente virtual..."
python3 -m venv venv
echo "✅ Ambiente virtual criado"
echo ""

# 3. Ativar ambiente virtual
echo "2. Ativando ambiente virtual..."
source venv/bin/activate
echo "✅ Ambiente virtual ativado"
echo ""

# 4. Atualizar pip
echo "3. Atualizando pip..."
pip install --upgrade pip --quiet
echo "✅ Pip atualizado"
echo ""

# 5. Instalar dependências
echo "4. Instalando dependências (isso pode levar alguns minutos)..."
pip install -r requirements.txt
echo "✅ Dependências instaladas"
echo ""

# 6. Verificar instalação
echo "5. Verificando instalação..."
pip check
echo "✅ Instalação verificada"
echo ""

# 7. Verificar .env
if [ ! -f ".env" ]; then
    if [ -f "src/.env" ]; then
        echo "6. Movendo .env para a raiz do projeto..."
        cp src/.env .env
        echo "✅ Arquivo .env copiado"
    elif [ -f ".env.example" ]; then
        echo "6. Criando .env a partir do .env.example..."
        cp .env.example .env
        echo "⚠️  IMPORTANTE: Edite o arquivo .env e adicione suas API keys!"
    else
        echo "⚠️  Arquivo .env não encontrado"
        echo "   Copie .env.example para .env e configure suas API keys"
    fi
else
    echo "6. Arquivo .env já existe"
    echo "✅ Configuração encontrada"
fi
echo ""

echo "=========================================="
echo "✅ Instalação Concluída!"
echo "=========================================="
echo ""
echo "Próximos passos:"
echo ""
echo "1. Edite o arquivo .env e adicione suas API keys:"
echo "   - OPENAI_API_KEY (se usar OpenAI)"
echo "   - GOOGLE_API_KEY (se usar Google Gemini)"
echo ""
echo "2. Inicie o banco de dados:"
echo "   docker-compose up -d"
echo ""
echo "3. Execute a ingestão do PDF:"
echo "   source venv/bin/activate"
echo "   python src/ingest.py"
echo ""
echo "4. Inicie o chat:"
echo "   python src/chat.py"
echo ""
echo "Para ativar o ambiente virtual no futuro:"
echo "   source venv/bin/activate"
echo ""

