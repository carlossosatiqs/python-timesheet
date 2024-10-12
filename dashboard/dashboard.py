import streamlit as st
import duckdb
import pandas as pd
import matplotlib.pyplot as plt

# Conexão com o banco de dados DuckDB
con = duckdb.connect('sugestoes.db')

st.title('Dashboard de Sugestões')

# Carregar dados da tabela
df = con.execute('SELECT * FROM sugestoes').fetchdf()

# Filtros
tipo_sugestao_filter = st.selectbox('Filtrar por Tipo de Sugestão', ['Todos'] + df['tipo_sugestao'].unique().tolist())
perfil_filter = st.selectbox('Filtrar por Perfil', ['Todos'] + df['perfil'].unique().tolist())

# Aplicar filtros
if tipo_sugestao_filter != 'Todos':
    df = df[df['tipo_sugestao'] == tipo_sugestao_filter]
if perfil_filter != 'Todos':
    df = df[df['perfil'] == perfil_filter]

# Gráfico de Pizza
fig, ax = plt.subplots()
df['tipo_sugestao'].value_counts().plot.pie(ax=ax, autopct='%1.1f%%', startangle=90)
ax.set_ylabel('')
ax.set_title('Distribuição das Sugestões por Tipo')

st.pyplot(fig)

# Tabela de Resultados
st.write('### Resultados Filtrados')
st.dataframe(df)

# Exibir contagem de sugestões
st.write(f"Total de Sugestões: {len(df)}")
