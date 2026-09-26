# SMS — Plataforma de Mensageria, Guia Local e Carteira Digital

Sistema de mensageria pessoal e comercial com geolocalização e carteira digital segura.

---

## Estrutura do Projeto

```
sms/
├── app/                  # Frontend Mobile Flet (Python / Flutter engine)
│   ├── core/theme.py     # Tokens de design (Esmeralda & Ciano)
│   ├── main.py           # Ponto de entrada do aplicativo
│   └── requirements.txt
├── backend/              # API FastAPI assíncrona
│   ├── app/
│   │   ├── core/config.py
│   │   └── main.py
│   ├── .env.example
│   └── requirements.txt
├── docs/                 # Documentação e Engenharia
│   ├── dia1.md           # Registro completo consolidado do Dia 1
│   ├── schema-sms.sql    # DDL PostgreSQL + PostGIS revisado
│   └── PROMPTS_JULES.md  # Prompts estruturados para Jules & IAs
└── projeto_geral/        # 14 telas de protótipo Stitch (code.html e screen.png)
```

---

## Como Rodar Localmente

### 1. Pré-requisitos
- **Python 3.10+** instalado no sistema.
- **PostgreSQL com PostGIS** (local via Docker/Postgres ou na nuvem via Neon/Supabase gratuito).

### 2. Rodando o Backend (FastAPI)
```bash
cd backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Acesse a documentação interativa Swagger em: `http://localhost:8000/docs`

### 3. Rodando o App Mobile (Flet)
```bash
cd app
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
flet run main.py
```
*Dica para hot-reload e visualização mobile: `flet run main.py -d`*
