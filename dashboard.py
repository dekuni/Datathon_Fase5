import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Projeto - Passos Mágicos", layout="wide", page_icon="✨")

st.markdown("""
<style>
    /* Cores principais */
    :root {
        --primary: #1E3A8A; /* Azul escuro */
        --secondary: #2563EB; /* Azul médio */
        --light-blue: #93C5FD; /* Azul claro */
        --background: #1E293B; /* Fundo escuro */
        --text: #E5E7EB; /* Texto claro */
    }
    
    /* Estilos gerais */
    .main {background-color: var(--background)}
    .stMetricLabel {font-size: 1.1rem!important; color: var(--text)!important;}
    .st-b7 {color: var(--text)!important;}
    .css-18e3th9 {padding: 2rem 5rem;}
    
    /* Cards */
    .custom-card {
        border-radius: 15px;
        padding: 20px;
        background: var(--background);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        color: var(--text);
    }
    
    /* Títulos */
    .custom-title {
        color: var(--primary);
        border-left: 5px solid var(--secondary);
        padding-left: 1rem;
        margin: 2rem 0 1.5rem 0;
    }
    
    /* Radio buttons */
    .stRadio > div {
        background: var(--background);
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: var(--text);
    }
</style>
""", unsafe_allow_html=True)

# Selector para alternar entre dashboards
dashboard = st.radio(
    "Escolha o Dashboard",
    ("Análise de Alunos", "Análise das Aulas"),
    index=0,
    horizontal=True
)

# Função para criar métricas estilizadas
def styled_metric(label, value, help_text=None):
    return f"""
    <div class="custom-card">
        <div style="font-size: 1.8rem; color: var(--primary); font-weight: 600;">{value}</div>
        <div style="font-size: 1.1rem; color: var(--text); margin-top: 0.5rem;">{label}</div>
        {f'<div style="font-size: 0.9rem; color: #666; margin-top: 0.3rem;">{help_text}</div>' if help_text else ''}
    </div>
    """

if dashboard == "Análise de Alunos":
    # Header
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 3rem;">
        <h1 style="color: var(--primary); font-size: 2.5rem; margin-bottom: 0.5rem;">📊 Projeto Passos Mágicos</h1>
        <h2 style="color: var(--secondary); font-size: 1.8rem;">Análise de Alunos</h2>
    </div>
    """, unsafe_allow_html=True)

    # Linha de métricas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(styled_metric("Total de Alunos", "2.246", "Ativos em 2023"), unsafe_allow_html=True)
    with col2:
        st.markdown(styled_metric("Alunos Homens", "1.039", "46.3% do total"), unsafe_allow_html=True)
    with col3:
        st.markdown(styled_metric("Alunos Mulheres", "1.207", "53.7% do total"), unsafe_allow_html=True)

    # Gráficos principais
    col4, col5 = st.columns([2, 1])
    with col4:
        st.markdown('<div class="custom-title">📈 Resultado Final por Ano de Conclusão</div>', unsafe_allow_html=True)
        
        # Processamento dos dados
        resultado_final = pd.read_csv('alunos.csv').dropna(subset=['AnoConclusao', 'ResultadoFinal'])
        resultado_final['AnoConclusao'] = resultado_final['AnoConclusao'].astype(str)
        
        # Gráfico atualizado
        fig = px.histogram(resultado_final, x="AnoConclusao", color="ResultadoFinal",
                         barmode="group", text_auto=True,
                         color_discrete_sequence=["#6A1B9A", "#9C27B0", "#E1BEE7"])
        fig.update_layout(height=400, showlegend=True, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    with col5:
        st.markdown('<div class="custom-title">📅 Distribuição por Idade</div>', unsafe_allow_html=True)
        
        # Processamento dos dados
        idades = pd.read_csv("alunos.csv").dropna(subset=["Idade"])
        idades = idades["Idade"].value_counts().reset_index().sort_values(by="Idade")
        idades.columns = ["Idade", "Quantidade"]
        
        # Gráfico atualizado
        fig = px.area(idades, x="Idade", y="Quantidade", markers=True,
                     color_discrete_sequence=["#9C27B0"])
        fig.update_layout(height=350, showlegend=False, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    # Gráficos secundários
    col6, col7 = st.columns(2)
    with col6:
        st.markdown('<div class="custom-title">🧑🏽‍🤝‍🧑🏻 Distribuição por Raça e Gênero</div>', unsafe_allow_html=True)
        
        # Processamento dos dados
        dados_raca = pd.read_csv("alunos.csv")
        dados_raca = dados_raca[dados_raca["CorRaca"] != "I"].dropna(subset=["Sexo", "CorRaca"])
        dados_raca = dados_raca.groupby(["Sexo", "CorRaca"]).size().reset_index(name="Quantidade")
        dados_raca["Percentual"] = dados_raca.groupby("Sexo")["Quantidade"].transform(lambda x: (x/x.sum())*100)
        
        # Gráfico atualizado
        fig = px.bar(dados_raca, x="Sexo", y="Percentual", color="CorRaca",
                    text=dados_raca["Percentual"].round(2).astype(str) + "%",
                    color_discrete_sequence=px.colors.sequential.Purples_r)
        fig.update_layout(barmode="stack", height=400, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    with col7:
        st.markdown('<div class="custom-title">📋 Status do Cadastro Responsável</div>', unsafe_allow_html=True)

        # Processamento dos dados
        status = pd.read_csv("alunos.csv").dropna(subset=["StatusResponsavel"])

        # Contar os status e renomear colunas corretamente
        status = status["StatusResponsavel"].value_counts().reset_index()
        status.columns = ["StatusResponsavel", "Quantidade"]  # Renomear para colunas corretas

        # Gráfico corrigido
        fig = px.pie(status, values="Quantidade", names="StatusResponsavel", hole=0.4,
                    color_discrete_sequence=px.colors.sequential.Purples_r)
        fig.update_layout(height=400, showlegend=True)
        fig.update_traces(textposition='inside', textinfo='percent+label')

        st.plotly_chart(fig, use_container_width=True)


elif dashboard == "Análise das Aulas":
    # Header
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 3rem;">
        <h1 style="color: var(--primary); font-size: 2.5rem; margin-bottom: 0.5rem;">📚 Projeto Passos Mágicos</h1>
        <h2 style="color: var(--secondary); font-size: 1.8rem;">Análise das Aulas</h2>
    </div>
    """, unsafe_allow_html=True)

    # Linha de métricas
    cols = st.columns(5)
    metrics = [
        ("Presenças", "246.232", "Total registrado"),
        ("Faltas", "61.603", "13.8% das aulas"),
        ("Faltas Justificadas", "5.136", "8.3% das faltas"),
        ("Presença Masculina", "111.863", "45.4% do total"),
        ("Presença Feminina", "134.266", "54.6% do total")
    ]
    
    for col, (label, value, help_text) in zip(cols, metrics):
        with col:
            st.markdown(styled_metric(label, value, help_text), unsafe_allow_html=True)

    # Gráficos principais
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('<div class="custom-title">📊 Frequência por Disciplina</div>', unsafe_allow_html=True)

        # Carregar os dados do CSV
        try:
            conteudos = pd.read_csv("frequencia_por_disciplina.csv")


            # Pré-processamento
            conteudos = conteudos[conteudos['StPresencaFalta'] == 'P']
            conteudos['NomeDisciplina'] = conteudos['NomeDisciplina'].astype(str).str.strip()
            conteudos['qtd'] = pd.to_numeric(conteudos['qtd'], errors='coerce').fillna(0)

            # Agrupar por conteúdo ministrado e somar as presenças
            freq_agrupada = conteudos.groupby('NomeDisciplina')['qtd'].sum().reset_index()
            freq_agrupada = freq_agrupada.sort_values(by='qtd', ascending=False).head(10)

            # Criar gráfico de barras com layout ajustado
            fig = px.bar(
                freq_agrupada,
                x='qtd',
                y='NomeDisciplina',
                orientation='h',
                color='NomeDisciplina',
                color_discrete_sequence=px.colors.sequential.Blues
            )

            fig.update_layout(
                height=500,
                width=1600,
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title="Frequência",
                yaxis_title="Disciplinas",
                showlegend=False,
                margin=dict(l=200, r=20, t=50, b=50)
            )

            st.plotly_chart(fig, use_container_width=False)

        except Exception as e:
            st.error(f"Erro ao carregar e exibir o gráfico: {str(e)}")

    with col2:
        st.markdown('<div class="custom-title">🏆 Top Conteúdos Mais Acessados</div>', unsafe_allow_html=True)
        
        conteudos = pd.read_csv("frequencia_por_disciplina.csv")
        
        # Pré-processamento
        conteudos = conteudos[conteudos['StPresencaFalta'] == 'P']
        conteudos['ConteudoMinistrado'] = 'Disciplina ' + conteudos['ConteudoMinistrado'].astype(str).str.strip()
        conteudos['qtd'] = pd.to_numeric(conteudos['qtd'], errors='coerce').fillna(0)

        # Agrupar e calcular totais
        turma_totais = conteudos.groupby('ConteudoMinistrado')['qtd'].sum().reset_index()
        turma_totais = turma_totais.sort_values(by='qtd', ascending=False)  # Ordenar turmas pela frequência total
        top_20_turmas = turma_totais.nlargest(10, 'qtd')['ConteudoMinistrado'].tolist()

        # Filtrar e formatar dados
        freq_filtrada = conteudos[conteudos['ConteudoMinistrado'].isin(top_20_turmas)]
        freq_agrupada = freq_filtrada.groupby(['ConteudoMinistrado', 'Sexo'])['qtd'].sum().reset_index()

        # Criar gráfico de pizza
        fig = px.pie(
            freq_agrupada,
            names='ConteudoMinistrado',
            values='qtd',
            color='Sexo',
            color_discrete_sequence=["#1E3A8A", "#2563EB"]
        )
        fig.update_layout(
            height=400,
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            title_text="Top Conteúdos Mais Acessados"
        )
        st.plotly_chart(fig, use_container_width=True)


    st.markdown('<div class="custom-title">👥 Frequência por Turma e Gênero (Top 20)</div>', unsafe_allow_html=True)

    try:
        # Processamento dos dados
        frequencia = pd.read_csv("frequencia_por_disciplina.csv")
        
        # Pré-processamento
        frequencia = frequencia[frequencia['StPresencaFalta'] == 'P']
        frequencia['IdTurma'] = 'Turma ' + frequencia['IdTurma'].astype(str).str.strip()
        frequencia['qtd'] = pd.to_numeric(frequencia['qtd'], errors='coerce').fillna(0)

        # Agrupar e calcular totais
        turma_totais = frequencia.groupby('IdTurma')['qtd'].sum().reset_index()
        turma_totais = turma_totais.sort_values(by='qtd', ascending=False)  # Ordenar turmas pela frequência total
        top_20_turmas = turma_totais.nlargest(20, 'qtd')['IdTurma'].tolist()

        # Filtrar e formatar dados
        freq_filtrada = frequencia[frequencia['IdTurma'].isin(top_20_turmas)]
        freq_agrupada = freq_filtrada.groupby(['IdTurma', 'Sexo'])['qtd'].sum().unstack(fill_value=0)
        
        # Ordenar turmas pelo total
        freq_agrupada['Total'] = freq_agrupada['F'] + freq_agrupada['M']
        freq_agrupada = freq_agrupada.loc[top_20_turmas].drop(columns='Total')
        
        # Converter para formato longo
        freq_agrupada = freq_agrupada.reset_index().melt(
            id_vars='IdTurma', 
            var_name='Gênero', 
            value_name='Frequência'
        )

        # Criar visualização
        fig = px.line(
            freq_agrupada,
            x='IdTurma',
            y='Frequência',
            color='Gênero',
            markers=True,
            color_discrete_map={'M': '#6A1B9A', 'F': '#9C27B0'}
        )

        # Ajustes estéticos
        fig.update_layout(
            height=500,
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title='Turma',
            yaxis_title='Total de Presenças',
            xaxis=dict(
                type='category',
                tickangle=45,
                categoryorder='array',
                categoryarray=top_20_turmas,  # Ordenar corretamente as turmas
                title_font=dict(size=14),
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                title_font=dict(size=14),
                tickfont=dict(size=12),
                gridcolor='lightgrey'
            ),
            legend=dict(
                title='Gênero',
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="Arial"
            )
        )

        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Erro ao processar dados de frequência: {str(e)}")
