# TalentFlow

TalentFlow é uma aplicação web em Flask para gestão de talentos, análise de habilidades e recomendações de carreira. Ela integra dados de colaboradores e vagas, calcula compatibilidade de skills, importa usuários via Excel e, opcionalmente, gera planos de carreira com a API da OpenAI. Persistência via MongoDB.

## Objetivo
- Centralizar informações de colaboradores e vagas.
- Identificar compatibilidade de habilidades e gaps em projetos.
- Recomendar oportunidades e gerar plano de carreira acionável.

## Funcionalidades
- Dashboard com filtros, top skills e gaps por projeto.
- Detalhe do perfil com recomendações de vagas por compatibilidade.
- Geração de plano de carreira usando OpenAI (opcional).
- Importação de colaboradores via planilha `.xlsx`.
- Cadastro manual de novos colaboradores.
- Páginas de gráficos agregados e styleguide.

## Arquitetura
- `run.py`: ponto de entrada, inicia o servidor Flask.
- `app/__init__.py`: fábrica `create_app()`, carrega `.env` e conecta ao MongoDB.
- `app/routes.py`: rotas principais (`/dashboard`, `/perfil/<id>`, `/upload_usuarios`, `/novo_usuario`, `/graficos`, `/plano_carreira/<id>`, `/styleguide`).
- `app/templates`: páginas Jinja2 (HTML).
- `app/static`: arquivos estáticos (CSS/JS/imagens).
- `app/nlp/extractor.py`: utilitário para extrair skills de textos.
- `app/recommendation/recommender.py`: recomendações offline via JSON (uso auxiliar).

## Requisitos
- Python 3.8+ (recomendado 3.10 ou superior).
- MongoDB (local ou remoto) para persistência.
- Dependências Python (vide `requirements.txt`):
  - `Flask==2.2.2`
  - `Werkzeug<3.0`
  - `openpyxl==3.1.5`
  - `openai>=1.10.0`
  - `python-dotenv>=1.0.1`
  - `pymongo>=4.8.0`
  - (opcional) `certifi` para TLS em conexões MongoDB.

## Como baixar
Você pode clonar o repositório ou baixar o ZIP:
- Clonar com Git: `git clone <URL-do-repositório>`
- Ou baixe e extraia o ZIP em `C:\TalentFlow`

## Instalação (Windows)
1. Abra um terminal PowerShell.
2. Crie e ative um ambiente virtual (opcional, recomendado):
   - `python -m venv .venv`
   - `./.venv/Scripts/Activate.ps1`
3. Instale as dependências:
   - `pip install -r requirements.txt`

## Configuração (.env)
Crie um arquivo `.env` na raiz com as variáveis:
- `MONGODB_URI`: string de conexão (ex.: `mongodb+srv://usuario:senha@cluster/db?retryWrites=true&w=majority`).
- `MONGODB_DB`: nome do banco (padrão: `talentflow`).
- `OPENAI_API_KEY`: chave da API OpenAI para gerar plano de carreira.
- `OPENAI_MODEL`: modelo (padrão: `gpt-5-nano`).

Observações:
- Sem `MONGODB_URI`, a aplicação inicia mas funcionalidades que dependem de banco ficarão limitadas.
- Sem `OPENAI_API_KEY`, a geração de plano de carreira não estará disponível.

## Como usar
1. Inicie o servidor: `python run.py`
2. Acesse `http://localhost:5000/` no navegador.
3. Fluxos principais:
   - `Dashboard` (`/dashboard`): visualizar colaboradores, filtrar por cargo/área, ver top skills e gaps.
   - `Perfil` (`/perfil/<id>`): checar compatibilidade com vagas e acionar plano de carreira.
   - `Novo Usuário` (`/novo_usuario`): cadastrar colaborador manualmente.
   - `Upload de Usuários` (`/upload_usuarios`): importar via `.xlsx`.
   - `Gráficos` (`/graficos`): visualizar distribuição de skills e compatibilidade.
   - `Styleguide` (`/styleguide`): componentes e estilos.

## Importação via Excel
- Utilize os modelos em `app/data/funcionarios_modelo.xlsx` ou `app/data/funcionarios_modelo_novo.xlsx`.
- Aba esperada: `Funcionarios`.
- Cabeçalhos mínimos: `id`, `nome`, `cargo`, `email`, `habilidades_declaradas`.
- Valores em `habilidades_declaradas` podem ser separados por vírgula.

## Geração de Plano de Carreira (OpenAI)
- Endpoint: `POST /plano_carreira/<id>` a partir da página de perfil.
- Requisitos: `OPENAI_API_KEY` válido e opcionalmente `OPENAI_MODEL`.
- Saída: texto com metas mensais, habilidades, cursos (Alura, Data Science Academy, Udemy, Microsoft Learning), tempo estimado e nível.

## Banco de Dados (MongoDB)
Coleções esperadas:
- `funcionarios`: `{ id, nome, cargo, email, habilidades_declaradas[], habilidades_descobertas[] }`
- `vagas`: `{ id, titulo, area, habilidades_requeridas[] }`
- `projetos`: `{ id_projeto, nome_projeto, participantes[], tarefas[] }`

## Estrutura de pastas
```
TalentFlow/
├─ app/
│  ├─ __init__.py
│  ├─ routes.py
│  ├─ templates/
│  ├─ static/
│  │  └─ css/style.css
│  ├─ data/
│  ├─ nlp/
│  │  └─ extractor.py
│  └─ recommendation/
│     └─ recommender.py
├─ run.py
└─ requirements.txt
```

## Boas práticas
- Não versionar o `.env` nem expor chaves.
- Manter dependências atualizadas e compatíveis com `Flask 2.2.x`.
- Validar dados antes de importações em massa.
