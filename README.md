# VoteMídias - Sistema de Votação de Filmes e Séries 🎬

Este é um sistema simples desenvolvido como parte de um teste prático de estágio. Ele permite que usuários votem positivamente ou negativamente em filmes e séries, além de cadastrar novas obras e visualizar o total de votos.

## 🧩 Funcionalidades

- ✅ Votar positivamente ou negativamente em filmes/séries
- ✅ Cadastrar novas obras com título, gênero, descrição e imagem
- ✅ Listar todas as obras com total de votos (likes e dislikes)
- ✅ Persistência de dados com SQLite

---

## 💻 Tecnologias Utilizadas
### Backend
- **Python 3.12**
- **FastAPI**
- **Uvicorn**
- **SQLite3**

### Frontend
- **HTML**
- **CSS**
- **JavaScript**
- **Bootstrap 5 (CDN)**
- **Bootstrap Icons (CDN)**

---

## ⚙️ Requisitos

- **Python 3.12+ instalado**
- **SQLite 3.XX instalado (caso deseje usar a CLI)**
- **Git (opcional, para clonar o projeto)**

> Obs.: O SQLite pode ser usado via Python puro (`sqlite3`), mas a CLI é útil para inspeção manual.

---

## 🚀 Como rodar o projeto localmente

### 1. Clone o repositório
```bash
git clone https://github.com//Caio-Freitas005/vote-midias.git
cd vote-midias
```

### 2. Crie e ative um ambiente virtual
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# ou
.venv\Scripts\activate      # Windows
```

### 3. Instale as dependências 
```bash
pip install -r requirements.txt
```

### 4. Inicialize o banco de dados
```bash
python setup_database.py
```
> Isso criará o banco SQLite e irá populá-lo com 5 filmes/séries iniciais.

### 5. Rode o servidor
```bash
uvicorn app.main:app --reload
```

### 6. Acesse no navegador

Após iniciar o servidor, você pode acessar a duas URLs principais:

- **Para ver a aplicação (Front-end):**
  Abra o seu navegador em [http://localhost:8000/](http://localhost:8000/)

- **Para ver a documentação da API (Back-end):**
  Abra [http://localhost:8000/docs](http://localhost:8000/docs) para interagir diretamente com a API.

---

## 📁 Estrutura do projeto
```py
vote-midias/
├── app/                      # Pacote principal da aplicação API
│   ├── __init__.py           # Inicializador do pacote Python
│   ├── database.py           # Módulo de conexão com o banco (dependência)
│   ├── main.py               # Camada de API (endpoints e configuração)
│   ├── repositories.py       # Camada de acesso aos dados (queries SQL)
│   ├── schemas.py            # Camada de validação de dados (Pydantic)
│   └── services.py           # Camada de lógica de negócio
├── static/                   # Pacote de front-end (ficheiros estáticos)
│   ├── index.html
│   ├── script.js
│   └── style.css
├── .gitignore
├── requirements.txt          # Dependências do projeto Python
├── setup_database.py         # Script para criar e popular o banco de dados
└── README.md                 # Documentação do projeto
```

---

## ⚠️ Observações
- O projeto utiliza SQLite para facilitar a execução local sem necessidade de instalação extra de banco de dados.

- Para efeitos de teste, cinco obras são automaticamente inseridas na primeira execução.

---

## 📫 Contato
📧 Feito por [Caio da Silva Freitas](mailto:caiodasilvafreitas005@gmail.com)
