import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# Função para carregar e exibir os dados
@st.cache
def carregar_dados():
    try:
        # Carregar os dados do arquivo Excel
        ipeadata = pd.read_excel('ipeadata.xlsx', engine='openpyxl')
        ipeadata['Data'] = pd.to_datetime(ipeadata['Data'], errors='coerce')
        ipeadata.set_index('Data', inplace=True)
        ipeadata = ipeadata[ipeadata.index >= pd.Timestamp.today() - pd.Timedelta(days=365)]  # Dados recentes
        ipeadata['Preço'] = pd.to_numeric(ipeadata['Preço'], errors='coerce')
        ipeadata = ipeadata.dropna()  # Remover valores nulos
        return ipeadata
    except FileNotFoundError:
        st.error("Arquivo `ipeadata.xlsx` não encontrado. Verifique se ele está no diretório correto.")
        return None

# Função para calcular a previsão
def forecast_model(data, steps=1):
    modelo = ARIMA(data['Preço'], order=(2, 1, 2))
    modelo_fit = modelo.fit()
    forecast = modelo_fit.forecast(steps=steps)
    forecast_index = pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=steps, freq='D')
    forecast_series = pd.Series(forecast, index=forecast_index)
    return forecast_series

# Carregar os dados
dados = carregar_dados()
if dados is not None:
    st.title("Dashboard de Previsão do Preço do Petróleo")

    # Exibir os últimos 30 dias de dados
    st.markdown("### Últimos 30 Dias de Dados Históricos")
    ultimos_30_dias = dados.tail(30)
    st.dataframe(ultimos_30_dias)

    # Gráfico dos últimos 30 dias
    st.markdown("### Gráfico dos Últimos 30 Dias")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(ultimos_30_dias.index, ultimos_30_dias['Preço'], color='blue', label='Preço Histórico')
    ax.set_title("Preço do Petróleo - Últimos 30 Dias")
    ax.set_xlabel("Data")
    ax.set_ylabel("Preço (USD)")
    ax.legend()
    st.pyplot(fig)

    # Previsão para amanhã
    previsao_hoje = forecast_model(dados, steps=1)
    previsao_amanha = previsao_hoje.iloc[0]
    st.markdown("### Previsão para Amanhã")
    st.write(f"A previsão para amanhã é: ${previsao_amanha:.2f}")

    # Simulação de previsão de preço
    st.markdown("### Simulação de Previsão de Preço do Petróleo")
    dias_previsao = st.slider("Quantos dias você quer prever?", min_value=1, max_value=365, value=30)
    previsao = forecast_model(dados, steps=dias_previsao)

    # Exibir a tabela de previsões
    previsao_df = pd.DataFrame({
        "Data de Previsão": previsao.index,
        "Previsão de Preço (USD)": previsao.values
    })
    st.dataframe(previsao_df)

    # Gráfico da previsão
    st.markdown("### Gráfico da Previsão")
    fig2, ax2 = plt.subplots(figsize=(14, 6))
    ax2.plot(dados.index, dados['Preço'], label='Preço Histórico', color='blue', alpha=0.5)
    ax2.plot(previsao.index, previsao, label=f'Previsão para {dias_previsao} dias', color='green', linewidth=2)
    ax2.set_title(f"Previsão do Preço do Petróleo para {dias_previsao} Dias")
    ax2.set_xlabel("Data")
    ax2.set_ylabel("Preço (USD)")
    ax2.legend()
    st.pyplot(fig2)
