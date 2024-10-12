import streamlit as st
import duckdb
import pandas as pd
import matplotlib.pyplot as plt

# Conexão com o banco de dados DuckDB
con = duckdb.connect('sugestoes.db')

# Criar a tabela se ela não existir
con.execute('''
    CREATE TABLE IF NOT EXISTS sugestoes (
        tipo_sugestao TEXT,
        perfil TEXT,
        funcionalidade TEXT,
        sugestao TEXT
    )
''')

# Definir as páginas da aplicação
def pagina1():
    st.title('Formulário de Cadastro de Ideias para o Timesheet')
    # Campos do formulário
    tipo_sugestao = st.selectbox('Tipo de Sugestão', ['Melhoria', 'Bug', 'Outra'])
    perfil = st.selectbox('Perfil de uso', ['Administrador', 'Gerente', 'Usuário'])
    funcionalidade = st.text_input('Funcionalidade')

    sugestao = st.text_area('Sugestão')

    if st.button('Enviar'):
        con.execute('''
            INSERT INTO sugestoes (tipo_sugestao, perfil, funcionalidade, sugestao) 
            VALUES (?, ?, ?, ?)
        ''', (tipo_sugestao, perfil, funcionalidade, sugestao))
        # Limpar o formulário
        st.session_state['tipo_sugestao'] = 'Melhoria'
        st.session_state['perfil'] = ''
        st.session_state['funcionalidade'] = ''
        st.session_state['sugestao'] = ''    
        
        st.success('Sugestão cadastrada com sucesso!')

    # Exibir as sugestões cadastradas
    if st.checkbox('Mostrar sugestões cadastradas'):
        data = con.execute('SELECT * FROM sugestoes').fetchall()
        st.write(data)

def pagina2():
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

# Menu de navegação
pagina = st.sidebar.selectbox('Selecionar Página', ['Sugestões', 'Dashboard'])

# Carregar a página selecionada
if pagina == 'Sugestões':
    pagina1()
elif pagina == 'Dashboard':
    pagina2()


