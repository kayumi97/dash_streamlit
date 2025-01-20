import streamlit as st
import psycopg2
import pandas as pd

# Configuração do título do dashboard
st.title("Relatório Mundial de Felicidade")

# Conexão com o banco
conn = psycopg2.connect(
    host="database-hap.cb6ei4cq2ox1.us-east-2.rds.amazonaws.com",
    database="postgres",
    user="postgres",
    password="batataFRITA",
    port=5432
)

# Consulta os dados do banco
query = "SELECT country, year, happiness_score FROM world_happiness;"
df = pd.read_sql(query, conn)

# Filtro por país
st.sidebar.header("Filtros")
selected_country = st.sidebar.selectbox("Selecione um país", ["Todos"] + list(df['country'].unique()))
if selected_country != "Todos":
    df = df[df['country'] == selected_country]

# Filtro por ano
if df['year'].nunique() > 1:  # Verifica se existem vários anos no DataFrame
    selected_year = st.sidebar.slider("Selecione o ano", int(df['year'].min()), int(df['year'].max()))
else:
    st.sidebar.write("Apenas um ano disponível.")
    selected_year = df['year'].unique()[0]  # Seleciona o único ano disponível


# Exibição dos dados filtrados
st.subheader("Dados Filtrados")
st.write(df)

# Gráfico de barras
st.subheader("Gráfico de Felicidade por País")
chart_data = df.groupby('country')['happiness_score'].mean().reset_index()
st.bar_chart(chart_data.set_index('country'))

# Fechar a conexão
conn.close()
