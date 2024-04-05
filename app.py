import streamlit as st
import pandas as pd
import plotly.express as px
import psycopg2

# Configurações do Banco de Dados
db_config = {
    "host": "dpg-cm8onvmn7f5s73dd65c0-a.oregon-postgres.render.com",
    "dbname": "datastore_gnmj",
    "user": "volksdata",
    "password": "ygU5FRgFEZlNyO8oMUwCHI1FiE60aikO"
}

# Conectar ao Banco de Dados
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, ttl=600)
def get_connection():
    return psycopg2.connect(**db_config)

conn = get_connection()

# Consulta SQL
query = "SELECT * FROM record;"

# Executar Consulta e Carregar em DataFrame
df = pd.read_sql_query(query, conn)

# Fechar Conexão
conn.close()

# Streamlit App
st.title('Análise de Dados dos Estudantes')

# Verifica se o DataFrame não está vazio
if not df.empty:
    # Gráfico de Barras - Duração por Aluno
    st.subheader('Duração dos Estudos por Aluno')
    bar_chart = px.bar(df, x='student_name', y='duration', color='student_name', title='Duração dos Estudos por Aluno')
    st.plotly_chart(bar_chart)

    # Gráfico de Linhas - Evolução da Duração
    st.subheader('Evolução da Duração dos Estudos')
    line_chart = px.line(df, x='timestamp', y='duration', color='student_name', title='Evolução da Duração dos Estudos')
    st.plotly_chart(line_chart)

    # Histograma - Distribuição das Durações
    st.subheader('Distribuição das Durações dos Estudos')
    hist_chart = px.histogram(df, x='duration', nbins=20, title='Distribuição das Durações')
    st.plotly_chart(hist_chart)

    # Gráfico de Pizza - Proporção dos Formatos
    st.subheader('Proporção dos Formatos de Estudo')
    pie_chart = px.pie(df, names='format', title='Proporção dos Formatos de Estudo')
    st.plotly_chart(pie_chart)

    # Tabela de Dados Completa
    st.subheader('Tabela de Dados Completa')
    st.dataframe(df)
else:
    st.write("Nenhum dado disponível.")
