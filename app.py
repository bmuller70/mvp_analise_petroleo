import streamlit as st
import pandas as pd
import pickle
from prophet import Prophet
import matplotlib.pyplot as plt

# Configuração inicial do Streamlit
st.set_page_config(page_title='Dashboard de Previsão do Petróleo', layout='wide')

# Funções auxiliares
@st.cache_resource
def carregar_dados():
    """Carregar os dados de petróleo do arquivo ipeadata.xlsx."""
    try:
        dados = pd.read_excel('ipeadata.xlsx', engine='openpyxl')  # Ajuste o caminho se necessário
        dados['data'] = pd.to_datetime(dados['data'])
        dados = dados.rename(columns={"data": "ds", "preco": "y"})  # Adequação para Prophet
        return dados
    except FileNotFoundError:
        st.error("Arquivo `ipeadata.xlsx` não encontrado. Certifique-se de que o arquivo está no diretório correto.")
        return None

@st.cache_resource
def carregar_modelo():
    """Carregar o modelo Prophet treinado."""
    try:
        arquivo_modelo = "modelo_prophet.pkl"
        with open(arquivo_modelo, "rb") as f:
            modelo = pickle.load(f)
        return modelo
    except FileNotFoundError:
        st.error("Arquivo `modelo_prophet.pkl` não encontrado. Certifique-se de que o modelo está no diretório correto.")
        return None

# Carregando dados e modelo
dados = carregar_dados()
modelo = carregar_modelo()

if dados is not None and modelo is not None:
    # Visualização dos dados
    st.title("Dashboard de Previsão do Preço do Petróleo")
    st.write("### Dados históricos do preço do petróleo")
    st.dataframe(dados.tail(30))  # Mostrar os últimos 30 dias

    # Gráfico dos dados históricos
    st.write("### Gráfico de Preços Históricos")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(dados['ds'], dados['y'], label="Preço Histórico", color='blue')
    ax.set_title("Histórico de Preços do Petróleo")
    ax.set_xlabel("Data")
    ax.set_ylabel("Preço (USD)")
    ax.legend()
    st.pyplot(fig)

    # Previsão com Prophet
    st.write("### Previsão com Modelo Prophet")
    periodos = st.slider("Escolha o número de dias para previsão:", min_value=1, max_value=60, value=30)
    if st.button("Gerar Previsão"):
        futuro = modelo.make_future_dataframe(periods=periodos)
        previsao = modelo.predict(futuro)

        # Exibir a previsão
        st.write("#### Resultados da Previsão")
        st.dataframe(previsao[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periodos))

        # Gráfico da previsão
        st.write("### Gráfico da Previsão")
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        ax2.plot(previsao['ds'], previsao['yhat'], label="Previsão", color='green')
        ax2.fill_between(previsao['ds'], previsao['yhat_lower'], previsao['yhat_upper'], color='gray', alpha=0.3, label="Intervalo de Confiança")
        ax2.set_title("Previsão do Preço do Petróleo")
        ax2.set_xlabel("Data")
        ax2.set_ylabel("Preço (USD)")
        ax2.legend()
        st.pyplot(fig2)

    # Orientações para Deploy
    st.write("### Orientações para Deploy")
    st.markdown("""
    - Utilize plataformas como Streamlit Cloud, AWS ou Google Cloud para hospedar o aplicativo.
    - Certifique-se de carregar os arquivos necessários (dados e modelo) no ambiente de produção.
    """)
else:
    st.error("Não foi possível carregar os dados ou o modelo. Verifique os arquivos e tente novamente.")
