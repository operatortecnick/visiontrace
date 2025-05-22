# Usar imagem oficial do Python
FROM python:3.10-slim

# Diretório de trabalho no container
WORKDIR /app

# Copiar arquivos
COPY . /app

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta do Streamlit
EXPOSE 8501

# Comando para rodar o Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
