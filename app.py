import streamlit as st
from link_tracker import generator
from fingerprint import detector
from database import parser, search, db_manager
from reports import generator as report_gen, telegram_bot
from dotenv import load_dotenv
import os
import json

# Carrega as variáveis do arquivo .env
load_dotenv()

USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

st.set_page_config(page_title="VisionTrace", layout="wide")
st.title("🔍 VisionTrace — Painel de Rastreamento Total")

st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .css-18e3th9 {
        background-color: white;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 20px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
</style>
""", unsafe_allow_html=True)

st.sidebar.subheader("🔐 Login")
username = st.sidebar.text_input("Usuário")
password = st.sidebar.text_input("Senha", type="password")

if username != USER or password != PASSWORD:
    st.warning("Por favor, insira suas credenciais para acessar o painel.")
    st.stop()

conn = db_manager.create_connection()
db_manager.initialize_db(conn)

menu = ["Link Tracker", "Fingerprint", "Consulta Dados", "Logs e Relatórios"]
choice = st.sidebar.selectbox("🗂️ Menu", menu)

if choice == "Link Tracker":
    st.subheader("🔗 Link Tracker")

    server_ip = st.text_input(
        "Informe seu IP (ou domínio público)", value="127.0.0.1"
    )

    if st.button("🚀 Gerar Link Rastreável"):
        with st.spinner("🔄 Gerando link..."):
            try:
                link, uid = generator.generate_tracking_link(server_ip)
                st.success(f"✅ Link Gerado: {link}")
                db_manager.insert_log(conn, f"Link gerado: {link}")
            except Exception as e:
                st.error(f"❌ Erro ao gerar link: {e}")
                db_manager.insert_log(conn, f"Erro ao gerar link: {e}")

elif choice == "Fingerprint":
    st.subheader("🧠 Fingerprint Detector")

    with st.spinner("🔄 Coletando fingerprint..."):
        try:
            detector.fingerprint_collector()
            st.success("✅ Fingerprint coletado com sucesso!")
            db_manager.insert_log(conn, "Fingerprint coletado")
        except Exception as e:
            st.error(f"❌ Erro no coletor de fingerprint: {e}")
            db_manager.insert_log(conn, f"Erro no fingerprint: {e}")

elif choice == "Consulta Dados":
    st.subheader("🔍 Busca em Dumps")

    uploaded_file = st.file_uploader(
        "📂 Faça upload do arquivo de dump (CSV, JSON ou SQL)",
        type=["csv", "json", "sql"]
    )

    if uploaded_file:
        with st.spinner("🔄 Carregando dados..."):
            try:
                df = parser.load_data(uploaded_file)
                st.dataframe(df)

                query = st.text_input("🔎 Buscar por (CPF, Email, Nome, Tel, Senha)")

                if st.button("Buscar"):
                    with st.spinner("🔍 Realizando busca..."):
                        results = search.query_data(df, query)

                        if not results.empty:
                            st.success(f"🔍 {len(results)} resultado(s) encontrado(s):")
                            st.dataframe(results)
                        else:
                            st.warning("⚠️ Nenhum dado encontrado para essa busca.")

            except Exception as e:
                st.error(f"❌ Erro ao processar o arquivo: {e}")

elif choice == "Logs e Relatórios":
    st.subheader("📜 Logs e Relatórios")

    total_logs = db_manager.count_logs(conn)
    page_size = 10
    total_pages = (total_logs // page_size) + 1

    page = st.number_input(
        "Página", min_value=1, max_value=total_pages, value=1, step=1
    )
    offset = (page - 1) * page_size

    logs = db_manager.fetch_logs(conn, limit=page_size, offset=offset)

    if logs:
        for log in logs:
            st.json({"timestamp": log[0], "message": log[1]})
    else:
        st.warning("⚠️ Nenhum log encontrado.")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📄 Gerar TXT"):
            with st.spinner("🔄 Gerando TXT..."):
                report_gen.generate_txt([f"{t} - {m}" for t, m in logs])
                st.success("✅ Relatório TXT Gerado com sucesso!")

    with col2:
        if st.button("📄 Gerar PDF"):
            with st.spinner("🔄 Gerando PDF..."):
                report_gen.generate_pdf([f"{t} - {m}" for t, m in logs])
                st.success("✅ Relatório PDF Gerado com sucesso!")

    with col3:
        if st.button("🚀 Enviar para Telegram"):
            with st.spinner("🔄 Enviando para Telegram..."):
                telegram_bot.send_message(
                    "\n".join(f"{t} - {m}" for t, m in logs)
                )
                st.success("✅ Logs enviados para o Telegram com sucesso!")
