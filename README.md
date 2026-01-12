# Desafio MBA Engenharia de Software com IA - Full Cycle

## 🚀 Como Executar

Use os scripts automatizados que cuidam de tudo para você:

```bash
# 1. Clone o repositório
git clone <seu-repositorio>
cd mba-ia-desafio-ingestao-busca

# 2. Configure sua API Key
cp .env.example .env
# Edite .env e adicione OPENAI_API_KEY ou GOOGLE_API_KEY

# 3. Instale tudo automaticamente (cria venv, instala dependências)
./install.sh

# 4. Inicie o banco de dados
docker-compose up -d

# 5. Execute a ingestão do PDF
./ingest.sh

# 6. Inicie o chat
./chat.sh
```

**Pronto! Só isso.** ✅