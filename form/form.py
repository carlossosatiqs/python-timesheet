import streamlit as st
import duckdb

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
    st.success('Sugestão cadastrada com sucesso!')
