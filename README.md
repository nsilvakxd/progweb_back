# progweb

Sistema de gerenciamento de vakinhas com autenticação JWT.

## 🗄️ Configuração do Banco de Dados

O sistema suporta dois ambientes diferentes:

### Desenvolvimento (Local)
Para usar o banco de dados local:
1. Configure o arquivo `.env` com `ENVIRONMENT="development"`
2. Configure a `DATABASE_URL` com sua conexão PostgreSQL local
```env
ENVIRONMENT="development"
DATABASE_URL="postgresql://postgres:password@localhost/progwebIII"
```

### Produção (Render)
Para usar o banco de dados de produção:
1. Configure o arquivo `.env` com `ENVIRONMENT="production"`
2. O sistema usará automaticamente a URL do banco no Render
```env
ENVIRONMENT="production"
```

## 🚀 Como executar

1. Copie o arquivo `.env.example` para `.env`
```bash
cp .env.example .env
```

2. Configure as variáveis de ambiente no arquivo `.env`

3. Instale as dependências (se usar Poetry)
```bash
poetry install
```

4. Execute o servidor
```bash
uvicorn main:app --reload
```