import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Função para carregar os dados
@st.cache
def carregar_dados():
    # Carregue os dados do arquivo (substitua pelo caminho real)
    dados = pd.read_csv('/mnt/data/seus_dados.csv', parse_dates=['data'])
    return dados

# Função de previsão
def forecast_model(dados):
    # Adicione a lógica para o seu modelo de previsão de acordo com sua implementação
    forecast = dados.copy()
    forecast['previsao'] = forecast['preco'].shift(-1)  # Exemplo simples para demonstração
    return forecast

# Carregar os dados
dados = carregar_dados()

# Filtrar os últimos 30 dias
dados_ultimos_30 = dados[dados['data'] >= (dados['data'].max() - pd.Timedelta(days=30))]

# Exibir os dados no Streamlit
st.title("Dashboard de Análise de Preço do Petróleo")
st.write("Últimos 30 Dias de Dados Históricos")
st.dataframe(dados_ultimos_30)

# Criar o gráfico dos últimos 30 dias
st.subheader("Gráfico dos Últimos 30 Dias")
plt.figure(figsize=(12, 6))
plt.plot(dados_ultimos_30['data'], dados_ultimos_30['preco'], label='Preço Histórico', color='blue')
plt.title('Preço do Petróleo - Últimos 30 Dias')
plt.xlabel('Data')
plt.ylabel('Preço do Petróleo (USD)')
plt.grid(True)
plt.legend()
st.pyplot(plt)

# Executar a previsão e mostrar os resultados
previsao_hoje = forecast_model(dados_ultimos_30)
st.subheader("Previsão para Hoje")
st.write(previsao_hoje.iloc[-1])  # Exibe a última linha da previsão
