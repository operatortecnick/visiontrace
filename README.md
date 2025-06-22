# VisionTrace — Painel de Rastreamento Total

🔍 Um painel completo desenvolvido com Streamlit para rastreamento de links, coleta de fingerprint, consultas em dumps e geração de relatórios.

---

## 🚀 Funcionalidades
- 🔗 Gerador de links rastreáveis.
- 🧠 Coletor de fingerprint.
- 🔍 Busca em dumps de dados (CSV, JSON e SQL).
- 📜 Logs e geração de relatórios em TXT e PDF.
- 🚀 Envio dos logs diretamente para Telegram.
- 🔐 Sistema de autenticação seguro via arquivo `.env`.
- 🗃️ Logs persistentes utilizando banco SQLite.
- 🎨 Interface customizada com CSS.

---

## 🏗️ Estrutura do Projeto
```
VisionTrace/
├── .env                  # Dados de autenticação (NÃO subir para Git)
├── .gitignore            # Arquivos e pastas ignoradas no Git
├── app.py                # Aplicação principal
├── database/
│   └── db_manager.py     # Gerenciamento do banco SQLite
```
---

## 🔧 Instalação

### 1️⃣ Clone o projeto
```bash
git clone https://seu-repositorio.git
cd VisionTrace
```

### 2️⃣ Crie um ambiente virtual (opcional, recomendado)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 3️⃣ Instale as dependências
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure suas credenciais
Edite o arquivo `.env`:
```
USER=seuusuario
PASSWORD=suaSenhaForte
```

### 5️⃣ Execute o aplicativo
```bash
streamlit run app.py
```

Acesse no navegador:
```
http://localhost:8501
```

### 6️⃣ Refatore seus scripts facilmente

Você pode utilizar a ferramenta `refactor_gui.py` para converter arquivos `*.py`
em versões assíncronas (`*.task.py`). Basta executá-la e escolher a pasta
desejada para a refatoração.

```bash
python refactor_gui.py
```

Uma janela será exibida permitindo selecionar o diretório de trabalho.

---

## 📜 Logs
Os logs são armazenados no banco SQLite `logs.db`.

## 🔐 Segurança
- As credenciais estão armazenadas no arquivo `.env` (não suba isso para o Git).
- O arquivo `.gitignore` já está configurado para proteger arquivos sensíveis.

## 📄 Relatórios
- Pode gerar relatórios TXT e PDF diretamente da interface.
- Envio opcional para Telegram.

---

## 🛠️ Tecnologias utilizadas
- Python
- Streamlit
- SQLite
- Pandas
- ReportLab
- python-telegram-bot

---

## 🧠 Autor
Desenvolvido com ❤️ por [Seu Nome].
