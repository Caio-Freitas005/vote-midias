# VoteMídias - Sistema de Votação de Filmes e Séries 🎬

Este é um sistema simples desenvolvido como parte de um teste prático de estágio. Ele permite que usuários votem positivamente ou negativamente em filmes e séries, além de cadastrar novas obras e visualizar o total de votos.

## 🧩 Funcionalidades

- ✅ Votar positivamente ou negativamente em filmes/séries
- ✅ Cadastrar novas obras com título, gênero, descrição e imagem
- ✅ Listar todas as obras com total de votos (likes e dislikes)
- ✅ Persistência de dados com SQLite

---

## 💻 Tecnologias Utilizadas

- **Python 3.12**
- **FastAPI**
- **Uvicorn**
- **SQLite3**
- **HTML / CSS / JavaScript (vanilla)**

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
python database.py
```
> Isso criará o banco SQLite e irá populá-lo com 5 filmes/séries iniciais.

### 5. Rode o servidor
```bash
uvicorn main:app --reload
```

### 6. Acesse no navegador
Abra http://localhost:8000

---

# 📁 Estrutura do projeto
```py
projeto/
├── static/                 # Arquivos estáticos (HTML, CSS, JS, imagens)
│   ├── uploads/            # Upload de imagens
│   │   ├── images/
│   ├── index.html
│   ├── style.css 
├── .venv/                  # Ambiente virtual (não versionado)
├── main.py                 # Arquivo principal da API
├── database.py             # Lógica de criação e conexão com o banco
├── requirements.txt        # Dependências do projeto
├── .gitignore
└── README.md
```

---

# ⚠️ Observações
- O projeto utiliza SQLite para facilitar a execução local sem necessidade de instalação extra de banco de dados.

- Para efeitos de teste, cinco obras são automaticamente inseridas na primeira execução.

---
# 📫 Contato
📧 Feito por [Caio da Silva Freitas](mailto:caiodasilvafreitas005@gmail.com)