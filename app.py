# URLs dos arquivos
url_excel = "https://www.football-data.co.uk/mmz4281/2526/all-euro-data-2025-2026.xlsx"
url_proximos_jogos = "https://www.football-data.co.uk/fixtures.xlsx"

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import requests
from datetime import datetime, timedelta
import time

# Configuração da página
st.set_page_config(page_title="FutAlgorithm", page_icon="⚽", layout="wide")

st.title("💀 FutAlgorithm - Futebol Europeu 2025-2026 ⚡️ ")
st.markdown("---")

# Adicionar controle de atualização
st.sidebar.markdown("### ⚙️ Controle de Atualização")
atualizar_automatico = st.sidebar.checkbox("Atualização Automática", value=True)
intervalo_atualizacao = st.sidebar.slider("Intervalo (minutos)", 1, 60, 5)

if atualizar_automatico:
    st.sidebar.info(f"📡 Atualizando a cada {intervalo_atualizacao} minutos")
    time.sleep(intervalo_atualizacao * 60)
    st.rerun()

# Botão para atualização manual
if st.sidebar.button("🔄 Atualizar Agora"):
    st.rerun()

# Remover cache para garantir dados sempre atualizados
def carregar_dados_excel(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        excel_file = BytesIO(response.content)
        todas_abas = pd.read_excel(excel_file, sheet_name=None)
        abas_disponiveis = list(todas_abas.keys())
        st.success(f"✅ Arquivo carregado com sucesso! {len(abas_disponiveis)} ligas encontradas - {datetime.now().strftime('%H:%M:%S')}")
        return todas_abas, abas_disponiveis
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {e}")
        return None, None

def carregar_proximos_jogos(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        excel_file = BytesIO(response.content)
        df_jogos = pd.read_excel(excel_file)
        st.success(f"✅ Dados do simulador carregados com sucesso! - {datetime.now().strftime('%H:%M:%S')}")
        return df_jogos
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados do simulador: {e}")
        return None

# Carregar dados
todas_abas, abas_disponiveis = carregar_dados_excel(url_excel)
df_proximos_jogos = carregar_proximos_jogos(url_proximos_jogos)

# Exibir hora da última atualização
st.sidebar.markdown(f"**Última atualização:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

# Mapeamento completo com as 18 ligas principais
mapeamento_ligas = {
    'E0': 'Premier League (Inglaterra)', 'E1': 'Championship (Inglaterra)', 'E2': 'League One (Inglaterra)', 'E3': 'League Two (Inglaterra)',
    'SC0': 'Premiership (Escócia)', 'SC1': 'Championship (Escócia)', 'SC2': 'League One (Escócia)', 'SC3': 'League Two (Escócia)',
    'D1': 'Bundesliga (Alemanha)', 'D2': '2. Bundesliga (Alemanha)', 'I1': 'Serie A (Itália)', 'I2': 'Serie B (Itália)',
    'SP1': 'La Liga (Espanha)', 'SP2': 'La Liga 2 (Espanha)', 'F1': 'Ligue 1 (França)', 'F2': 'Ligue 2 (França)',
    'N1': 'Eredivisie (Holanda)', 'B1': 'Jupiler Pro League (Bélgica)', 'P1': 'Primeira Liga (Portugal)', 'T1': 'Super Lig (Turquia)', 'G1': 'Super League (Grécia)'
}

# Verificação das ligas
st.sidebar.markdown("### 🔍 VERIFICAÇÃO DE LIGAS")
if abas_disponiveis:
    st.sidebar.write(f"**Total de ligas carregadas:** {len(abas_disponiveis)}")
else:
    st.sidebar.write("❌ Nenhuma liga foi carregada")

# Dicionário de tradução das colunas
traducao_colunas = {
    'Div': 'Liga', 'Date': 'Data', 'Time': 'Hora', 'HomeTeam': 'Mandante', 'AwayTeam': 'Visitante',
    'FTHG': 'Gols Casa', 'FTAG': 'Gols Fora', 'FTR': 'Resultado Final', 'HTHG': 'Gols Casa 1T', 'HTAG': 'Gols Fora 1T',
    'HTR': 'Resultado 1T', 'HS': 'Chutes Mandante', 'AS': 'Chutes Visitante', 'HST': 'Chutes no Gol Mandante',
    'AST': 'Chutes no Gol Visitante', 'HF': 'Faltas Mandante', 'AF': 'Faltas Visitante', 'HC': 'Escanteios Mandante',
    'AC': 'Escanteios Visitante', 'HY': 'Cartões Amarelos Mandante', 'AY': 'Cartões Amarelos Visitante',
    'HR': 'Cartões Vermelhos Mandante', 'AR': 'Cartões Vermelhos Visitante', 'B365H': 'B365 Casa',
    'B365D': 'B365 Empate', 'B365A': 'B365 Fora', 'B365>2.5': 'B365 Over 2.5', 'B365<2.5': 'B365 Under 2.5'
}

def traduzir_colunas_df(df):
    df_traduzido = df.copy()
    colunas_renomear = {}
    for coluna in df_traduzido.columns:
        if coluna in traducao_colunas:
            colunas_renomear[coluna] = traducao_colunas[coluna]
    df_traduzido = df_traduzido.rename(columns=colunas_renomear)
    return df_traduzido

def calcular_probabilidades(odd):
    if pd.isna(odd) or odd <= 0:
        return 0
    return round((1 / odd) * 100, 1)

def formatar_probabilidade(valor):
    return f"{valor}%"

def calcular_relatorio_liga(df_liga, nome_liga):
    if df_liga.empty:
        return None

    relatorio = {'Liga': nome_liga, 'Total de Jogos': len(df_liga), 'Estatísticas': {}}

    if 'FTR' in df_liga.columns:
        total_jogos = len(df_liga)
        vitorias_casa = len(df_liga[df_liga['FTR'] == 'H'])
        empates = len(df_liga[df_liga['FTR'] == 'D'])
        vitorias_fora = len(df_liga[df_liga['FTR'] == 'A'])
        relatorio['Estatísticas']['Vitória do Mandante'] = f"{(vitorias_casa / total_jogos) * 100:.1f}%"
        relatorio['Estatísticas']['Empate'] = f"{(empates / total_jogos) * 100:.1f}%"
        relatorio['Estatísticas']['Vitória do Visitante'] = f"{(vitorias_fora / total_jogos) * 100:.1f}%"

    if 'HTHG' in df_liga.columns and 'HTAG' in df_liga.columns and 'FTHG' in df_liga.columns and 'FTAG' in df_liga.columns:
        total_jogos = len(df_liga)
        total_gols_ht = df_liga['HTHG'].sum() + df_liga['HTAG'].sum()
        media_gols_ht = total_gols_ht / total_jogos
        relatorio['Estatísticas']['Gols HT por Jogo'] = f"{media_gols_ht:.2f}"
        total_gols_ft = df_liga['FTHG'].sum() + df_liga['FTAG'].sum()
        media_gols_ft = total_gols_ft / total_jogos
        relatorio['Estatísticas']['Gols FT por Jogo'] = f"{media_gols_ft:.2f}"

    if 'HTHG' in df_liga.columns and 'HTAG' in df_liga.columns:
        total_jogos = len(df_liga)
        jogos_over_05_ht = len(df_liga[(df_liga['HTHG'] + df_liga['HTAG']) > 0.5])
        relatorio['Estatísticas']['Over 0.5 HT'] = f"{(jogos_over_05_ht / total_jogos) * 100:.1f}%"
        jogos_over_15_ht = len(df_liga[(df_liga['HTHG'] + df_liga['HTAG']) > 1.5])
        relatorio['Estatísticas']['Over 1.5 HT'] = f"{(jogos_over_15_ht / total_jogos) * 100:.1f}%"

    if 'FTHG' in df_liga.columns and 'FTAG' in df_liga.columns:
        total_jogos = len(df_liga)
        jogos_over_05_ft = len(df_liga[(df_liga['FTHG'] + df_liga['FTAG']) > 0.5])
        relatorio['Estatísticas']['Over 0.5 FT'] = f"{(jogos_over_05_ft / total_jogos) * 100:.1f}%"
        jogos_over_15_ft = len(df_liga[(df_liga['FTHG'] + df_liga['FTAG']) > 1.5])
        relatorio['Estatísticas']['Over 1.5 FT'] = f"{(jogos_over_15_ft / total_jogos) * 100:.1f}%"
        jogos_over_25_ft = len(df_liga[(df_liga['FTHG'] + df_liga['FTAG']) > 2.5])
        relatorio['Estatísticas']['Over 2.5 FT'] = f"{(jogos_over_25_ft / total_jogos) * 100:.1f}%"
        btts_ft = len(df_liga[(df_liga['FTHG'] > 0) & (df_liga['FTAG'] > 0)])
        relatorio['Estatísticas']['BTTS FT'] = f"{(btts_ft / total_jogos) * 100:.1f}%"

    return relatorio

def calcular_estatisticas_ultimos_5_jogos(df_liga, nome_time):
    jogos_mandante = df_liga[df_liga['HomeTeam'] == nome_time]
    jogos_visitante = df_liga[df_liga['AwayTeam'] == nome_time]
    todos_jogos = pd.concat([jogos_mandante, jogos_visitante])

    if len(todos_jogos) == 0:
        return None

    if 'Date' in todos_jogos.columns:
        todos_jogos = todos_jogos.sort_values('Date', ascending=False)

    ultimos_5 = todos_jogos.head(5)

    if len(ultimos_5) == 0:
        return None

    estatisticas = {
        'jogos_analisados': len(ultimos_5), 'vitorias': 0, 'empates': 0, 'derrotas': 0,
        'over_05_ht': 0, 'over_05_ft': 0, 'over_15_ft': 0, 'over_25_ft': 0, 'btts': 0,
        'gols_marcados_ht': 0, 'gols_sofridos_ht': 0, 'gols_marcados_ft': 0, 'gols_sofridos_ft': 0,
        'chutes_gol': [], 'chutes': [], 'escanteios_favor': [], 'escanteios_contra': [],
        'amarelos_favor': [], 'amarelos_contra': [], 'faltas_favor': [], 'faltas_contra': [],
        'impedimentos_favor': [], 'impedimentos_contra': []
    }

    for _, jogo in ultimos_5.iterrows():
        if jogo['HomeTeam'] == nome_time:
            gols_feitos_ft = jogo['FTHG'] if 'FTHG' in jogo else 0
            gols_sofridos_ft = jogo['FTAG'] if 'FTAG' in jogo else 0
            gols_feitos_ht = jogo['HTHG'] if 'HTHG' in jogo else 0
            gols_sofridos_ht = jogo['HTAG'] if 'HTAG' in jogo else 0

            if jogo['FTR'] == 'H':
                estatisticas['vitorias'] += 1
            elif jogo['FTR'] == 'D':
                estatisticas['empates'] += 1
            else:
                estatisticas['derrotas'] += 1

            estatisticas['chutes_gol'].append(jogo['HST'] if 'HST' in jogo and not pd.isna(jogo['HST']) else 0)
            estatisticas['chutes'].append(jogo['HS'] if 'HS' in jogo and not pd.isna(jogo['HS']) else 0)
            estatisticas['escanteios_favor'].append(jogo['HC'] if 'HC' in jogo and not pd.isna(jogo['HC']) else 0)
            estatisticas['escanteios_contra'].append(jogo['AC'] if 'AC' in jogo and not pd.isna(jogo['AC']) else 0)
            estatisticas['amarelos_favor'].append(jogo['HY'] if 'HY' in jogo and not pd.isna(jogo['HY']) else 0)
            estatisticas['amarelos_contra'].append(jogo['AY'] if 'AY' in jogo and not pd.isna(jogo['AY']) else 0)
            estatisticas['faltas_favor'].append(jogo['HF'] if 'HF' in jogo and not pd.isna(jogo['HF']) else 0)
            estatisticas['faltas_contra'].append(jogo['AF'] if 'AF' in jogo and not pd.isna(jogo['AF']) else 0)

            if 'HI' in jogo and not pd.isna(jogo['HI']):
                estatisticas['impedimentos_favor'].append(jogo['HI'])
            if 'AI' in jogo and not pd.isna(jogo['AI']):
                estatisticas['impedimentos_contra'].append(jogo['AI'])
        else:
            gols_feitos_ft = jogo['FTAG'] if 'FTAG' in jogo else 0
            gols_sofridos_ft = jogo['FTHG'] if 'FTHG' in jogo else 0
            gols_feitos_ht = jogo['HTAG'] if 'HTAG' in jogo else 0
            gols_sofridos_ht = jogo['HTHG'] if 'HTHG' in jogo else 0

            if jogo['FTR'] == 'A':
                estatisticas['vitorias'] += 1
            elif jogo['FTR'] == 'D':
                estatisticas['empates'] += 1
            else:
                estatisticas['derrotas'] += 1

            estatisticas['chutes_gol'].append(jogo['AST'] if 'AST' in jogo and not pd.isna(jogo['AST']) else 0)
            estatisticas['chutes'].append(jogo['AS'] if 'AS' in jogo and not pd.isna(jogo['AS']) else 0)
            estatisticas['escanteios_favor'].append(jogo['AC'] if 'AC' in jogo and not pd.isna(jogo['AC']) else 0)
            estatisticas['escanteios_contra'].append(jogo['HC'] if 'HC' in jogo and not pd.isna(jogo['HC']) else 0)
            estatisticas['amarelos_favor'].append(jogo['AY'] if 'AY' in jogo and not pd.isna(jogo['AY']) else 0)
            estatisticas['amarelos_contra'].append(jogo['HY'] if 'HY' in jogo and not pd.isna(jogo['HY']) else 0)
            estatisticas['faltas_favor'].append(jogo['AF'] if 'AF' in jogo and not pd.isna(jogo['AF']) else 0)
            estatisticas['faltas_contra'].append(jogo['HF'] if 'HF' in jogo and not pd.isna(jogo['HF']) else 0)

            if 'AI' in jogo and not pd.isna(jogo['AI']):
                estatisticas['impedimentos_favor'].append(jogo['AI'])
            if 'HI' in jogo and not pd.isna(jogo['HI']):
                estatisticas['impedimentos_contra'].append(jogo['HI'])

        estatisticas['gols_marcados_ht'] += gols_feitos_ht
        estatisticas['gols_sofridos_ht'] += gols_sofridos_ht
        estatisticas['gols_marcados_ft'] += gols_feitos_ft
        estatisticas['gols_sofridos_ft'] += gols_sofridos_ft

        total_gols_ht = gols_feitos_ht + gols_sofridos_ht
        total_gols_ft = gols_feitos_ft + gols_sofridos_ft

        if total_gols_ht > 0.5:
            estatisticas['over_05_ht'] += 1
        if total_gols_ft > 0.5:
            estatisticas['over_05_ft'] += 1
        if total_gols_ft > 1.5:
            estatisticas['over_15_ft'] += 1
        if total_gols_ft > 2.5:
            estatisticas['over_25_ft'] += 1
        if gols_feitos_ft > 0 and gols_sofridos_ft > 0:
            estatisticas['btts'] += 1

    estatisticas['media_gols_marcados_ht'] = estatisticas['gols_marcados_ht'] / estatisticas['jogos_analisados'] if estatisticas['jogos_analisados'] > 0 else 0
    estatisticas['media_gols_sofridos_ht'] = estatisticas['gols_sofridos_ht'] / estatisticas['jogos_analisados'] if estatisticas['jogos_analisados'] > 0 else 0
    estatisticas['media_ht'] = estatisticas['media_gols_marcados_ht'] + estatisticas['media_gols_sofridos_ht']
    estatisticas['media_gols_marcados_ft'] = estatisticas['gols_marcados_ft'] / estatisticas['jogos_analisados'] if estatisticas['jogos_analisados'] > 0 else 0
    estatisticas['media_gols_sofridos_ft'] = estatisticas['gols_sofridos_ft'] / estatisticas['jogos_analisados'] if estatisticas['jogos_analisados'] > 0 else 0
    estatisticas['media_ft'] = estatisticas['media_gols_marcados_ft'] + estatisticas['media_gols_sofridos_ft']

    return estatisticas

def obter_cor_percentual(percentual):
    if percentual >= 80:
        return "🟢"
    elif percentual >= 60:
        return "🟡"
    else:
        return "🔴"

def obter_probabilidade_historica_liga(codigo_liga, mercado):
    if codigo_liga in todas_abas:
        df_liga = todas_abas[codigo_liga]
        relatorio = calcular_relatorio_liga(df_liga, mapeamento_ligas.get(codigo_liga, codigo_liga))
        if relatorio and mercado in relatorio['Estatísticas']:
            valor_str = relatorio['Estatísticas'][mercado].replace('%', '')
            try:
                return float(valor_str)
            except:
                return None
    return None

# Criar abas principais
if todas_abas is not None and abas_disponiveis:
    nomes_abas = ["🎯 Simulador", "📊 Relatórios Liga", "👥 Análise por Time", "🔍 Buscar Equipe"]
    nomes_abas.extend([mapeamento_ligas.get(aba, f"{aba} (Liga)") for aba in abas_disponiveis])
    tabs = st.tabs(nomes_abas)

    # ABA 1: SIMULADOR
    with tabs[0]:
        st.header("🏆 Atualização dos jogos até 24h antes de cada rodada.")

        if df_proximos_jogos is not None and not df_proximos_jogos.empty:
            colunas_desejadas = ['Div', 'Date', 'HomeTeam', 'AwayTeam', 'B365H', 'B365D', 'B365A', 'B365>2.5', 'B365<2.5']
            colunas_existentes = [col for col in colunas_desejadas if col in df_proximos_jogos.columns]
            df_simulador = df_proximos_jogos[colunas_existentes].copy()

            if 'Date' in df_simulador.columns:
                df_simulador['Date'] = pd.to_datetime(df_simulador['Date'], errors='coerce')
                df_simulador['Date'] = df_simulador['Date'].dt.strftime('%d/%m/%Y')

            df_simulador = df_simulador.rename(columns={'Div': 'Liga', 'Date': 'Data', 'HomeTeam': 'Mandante', 'AwayTeam': 'Visitante'})
            df_simulador['Liga'] = df_simulador['Liga'].map(mapeamento_ligas).fillna(df_simulador['Liga'])

            if 'B365H' in df_simulador.columns:
                df_simulador['Vitória'] = df_simulador['B365H'].apply(calcular_probabilidades)
            if 'B365D' in df_simulador.columns:
                df_simulador['Empate'] = df_simulador['B365D'].apply(calcular_probabilidades)
            if 'B365A' in df_simulador.columns:
                df_simulador['Derrota'] = df_simulador['B365A'].apply(calcular_probabilidades)
            if 'B365>2.5' in df_simulador.columns:
                df_simulador['Over 2.5 FT'] = df_simulador['B365>2.5'].apply(calcular_probabilidades)
            if 'B365<2.5' in df_simulador.columns:
                df_simulador['Under 2.5 FT'] = df_simulador['B365<2.5'].apply(calcular_probabilidades)

            colunas_probabilidades = ['Vitória', 'Empate', 'Derrota', 'Over 2.5 FT', 'Under 2.5 FT']
            for coluna in colunas_probabilidades:
                if coluna in df_simulador.columns:
                    df_simulador[coluna] = df_simulador[coluna].apply(formatar_probabilidade)

            colunas_ordenadas = ['Data', 'Liga', 'Mandante', 'Visitante']
            for coluna in colunas_probabilidades:
                if coluna in df_simulador.columns:
                    colunas_ordenadas.append(coluna)

            colunas_odds_originais = ['B365H', 'B365D', 'B365A', 'B365>2.5', 'B365<2.5']
            for coluna in colunas_odds_originais:
                if coluna in df_simulador.columns:
                    colunas_ordenadas.append(coluna)

            df_simulador = df_simulador[colunas_ordenadas]

            if 'Data' in df_simulador.columns:
                df_simulador['Data_Ordenacao'] = pd.to_datetime(df_simulador['Data'], format='%d/%m/%Y', errors='coerce')
                df_simulador = df_simulador.sort_values('Data_Ordenacao')
                df_simulador = df_simulador.drop('Data_Ordenacao', axis=1)

            # Filtros
            st.subheader("🔍 Filtros")
            col1, col2 = st.columns(2)
            with col1:
                ligas_disponiveis = sorted(df_simulador['Liga'].unique())
                liga_filtro = st.selectbox("Filtrar por liga:", ["Todas as Ligas"] + list(ligas_disponiveis))
            with col2:
                if 'Data' in df_simulador.columns:
                    datas_disponiveis = sorted(df_simulador['Data'].unique())
                    if datas_disponiveis:
                        data_filtro = st.selectbox("Filtrar por data:", ["Todas as Datas"] + list(datas_disponiveis))

            df_filtrado = df_simulador.copy()
            if liga_filtro != "Todas as Ligas":
                df_filtrado = df_filtrado[df_filtrado['Liga'] == liga_filtro]
            if 'Data' in df_filtrado.columns and 'data_filtro' in locals() and data_filtro != "Todas as Datas":
                df_filtrado = df_filtrado[df_filtrado['Data'] == data_filtro]

            # Exibir jogos
            st.subheader("⚡️ Jogos da Rodada ⚡️ ")
            st.info(f"📊 **{len(df_filtrado)} jogos encontrados**")

            for idx, jogo in df_filtrado.iterrows():
                codigo_liga = None
                for codigo, nome in mapeamento_ligas.items():
                    if nome == jogo['Liga']:
                        codigo_liga = codigo
                        break

                with st.expander(f"🏟️ {jogo['Mandante']} vs {jogo['Visitante']} - {jogo['Liga']} - {jogo['Data']}"):
                    col1, col2, col3 = st.columns([1, 1, 1])

                    with col1:
                        st.subheader("📊 Odds e Probabilidades")
                        st.metric("Vitória", jogo.get('Vitória', 'N/D'))
                        st.metric("Empate", jogo.get('Empate', 'N/D'))
                        st.metric("Derrota", jogo.get('Derrota', 'N/D'))
                        st.metric("Over 2.5 FT", jogo.get('Over 2.5 FT', 'N/D'))
                        st.metric("Under 2.5 FT", jogo.get('Under 2.5 FT', 'N/D'))

                    with col2:
                        st.subheader("🎯 Sugestão do Sistema")
                        if codigo_liga:
                            prob_historica_over = obter_probabilidade_historica_liga(codigo_liga, "Over 2.5 FT")
                            if prob_historica_over is not None and 'Over 2.5 FT' in jogo and pd.notna(jogo['Over 2.5 FT']):
                                prob_odd_over = float(jogo['Over 2.5 FT'].replace('%', ''))
                                if prob_odd_over >= prob_historica_over:
                                    st.success(f"✅ OVER 2.5 (Odd: {prob_odd_over}% ≥ Histórico: {prob_historica_over}%)")
                                else:
                                    st.error(f"❌ UNDER 2.5 (Odd: {prob_odd_over}% < Histórico: {prob_historica_over}%)")
                            else:
                                st.info("ℹ️ Dados insuficientes para sugestão")
                        else:
                            st.info("ℹ️ Liga não encontrada para análise")

                    with col3:
                        st.subheader("📈 Estatísticas da Liga")
                        if codigo_liga and codigo_liga in todas_abas:
                            relatorio = calcular_relatorio_liga(todas_abas[codigo_liga], jogo['Liga'])
                            if relatorio:
                                st.write(f"**Over 2.5 FT:** {relatorio['Estatísticas'].get('Over 2.5 FT', 'N/D')}")
                                st.write(f"**BTTS FT:** {relatorio['Estatísticas'].get('BTTS FT', 'N/D')}")
                                st.write(f"**Média de Gols:** {relatorio['Estatísticas'].get('Gols FT por Jogo', 'N/D')}")

                    # Comparação detalhada
                    st.markdown("---")
                    st.subheader("📊 Comparação dos Últimos 5 Jogos")

                    if codigo_liga and codigo_liga in todas_abas:
                        df_liga = todas_abas[codigo_liga]
                        stats_mandante = calcular_estatisticas_ultimos_5_jogos(df_liga, jogo['Mandante'])
                        stats_visitante = calcular_estatisticas_ultimos_5_jogos(df_liga, jogo['Visitante'])

                        if stats_mandante and stats_visitante:
                            # Preparar dados para tabela comparativa
                            dados_mandante = {}
                            dados_visitante = {}

                            # Estatísticas básicas
                            dados_mandante['Jogos'] = f"{stats_mandante['jogos_analisados']}"
                            dados_visitante['Jogos'] = f"{stats_visitante['jogos_analisados']}"

                            percentuais = [
                                ('Jogos 0.5 HT', stats_mandante['over_05_ht'], stats_visitante['over_05_ht']),
                                ('Jogos 0.5 FT', stats_mandante['over_05_ft'], stats_visitante['over_05_ft']),
                                ('Jogos 1.5 FT', stats_mandante['over_15_ft'], stats_visitante['over_15_ft']),
                                ('Jogos 2.5 FT', stats_mandante['over_25_ft'], stats_visitante['over_25_ft']),
                                ('Jogos BTTS', stats_mandante['btts'], stats_visitante['btts']),
                                ('Vitórias', stats_mandante['vitorias'], stats_visitante['vitorias']),
                                ('Empates', stats_mandante['empates'], stats_visitante['empates']),
                                ('Derrotas', stats_mandante['derrotas'], stats_visitante['derrotas'])
                            ]

                            for nome, mandante_val, visitante_val in percentuais:
                                percent_mandante = (mandante_val / stats_mandante['jogos_analisados'] * 100) if stats_mandante['jogos_analisados'] > 0 else 0
                                percent_visitante = (visitante_val / stats_visitante['jogos_analisados'] * 100) if stats_visitante['jogos_analisados'] > 0 else 0

                                dados_mandante[nome] = f"{obter_cor_percentual(percent_mandante)} {mandante_val}/{stats_mandante['jogos_analisados']} ({percent_mandante:.0f}%)"
                                dados_visitante[nome] = f"{obter_cor_percentual(percent_visitante)} {visitante_val}/{stats_visitante['jogos_analisados']} ({percent_visitante:.0f}%)"

                            # Médias de gols
                            medias = [
                                ('Média de Gols Marcados HT', stats_mandante['media_gols_marcados_ht'], stats_visitante['media_gols_marcados_ht']),
                                ('Média de Gols Sofridos HT', stats_mandante['media_gols_sofridos_ht'], stats_visitante['media_gols_sofridos_ht']),
                                ('Média Total HT (Marcados + Sofridos)', stats_mandante['media_ht'], stats_visitante['media_ht']),
                                ('Média de Gols Marcados FT', stats_mandante['media_gols_marcados_ft'], stats_visitante['media_gols_marcados_ft']),
                                ('Média de Gols Sofridos FT', stats_mandante['media_gols_sofridos_ft'], stats_visitante['media_gols_sofridos_ft']),
                                ('Média Total FT (Marcados + Sofridos)', stats_mandante['media_ft'], stats_visitante['media_ft'])
                            ]

                            for nome, mandante_val, visitante_val in medias:
                                dados_mandante[nome] = f"{mandante_val:.2f}"
                                dados_visitante[nome] = f"{visitante_val:.2f}"

                            # Sequências
                            sequencias = [
                                ('Chutes no Gol (últimos 5)', stats_mandante['chutes_gol'], stats_visitante['chutes_gol']),
                                ('Chutes Totais (últimos 5)', stats_mandante['chutes'], stats_visitante['chutes']),
                                ('Escanteios a favor (últimos 5)', stats_mandante['escanteios_favor'], stats_visitante['escanteios_favor']),
                                ('Escanteios por jogo (total)',
                                 [a+b for a, b in zip(stats_mandante['escanteios_favor'], stats_mandante['escanteios_contra'])],
                                 [a+b for a, b in zip(stats_visitante['escanteios_favor'], stats_visitante['escanteios_contra'])]),
                                ('Cartões amarelos a favor (últimos 5)', stats_mandante['amarelos_favor'], stats_visitante['amarelos_favor']),
                                ('Cartões amarelos por jogo (total)',
                                 [a+b for a, b in zip(stats_mandante['amarelos_favor'], stats_mandante['amarelos_contra'])],
                                 [a+b for a, b in zip(stats_visitante['amarelos_favor'], stats_visitante['amarelos_contra'])]),
                                ('Faltas a favor (últimos 5)', stats_mandante['faltas_favor'], stats_visitante['faltas_favor']),
                                ('Faltas por jogo (total)',
                                 [a+b for a, b in zip(stats_mandante['faltas_favor'], stats_mandante['faltas_contra'])],
                                 [a+b for a, b in zip(stats_visitante['faltas_favor'], stats_visitante['faltas_contra'])])
                            ]

                            for nome, mandante_seq, visitante_seq in sequencias:
                                dados_mandante[nome] = ' - '.join(map(str, mandante_seq))
                                dados_visitante[nome] = ' - '.join(map(str, visitante_seq))

                            # Impedimentos (se disponíveis)
                            if stats_mandante['impedimentos_favor'] and stats_visitante['impedimentos_favor']:
                                dados_mandante['Impedimentos a favor (últimos 5)'] = ' - '.join(map(str, stats_mandante['impedimentos_favor']))
                                dados_visitante['Impedimentos a favor (últimos 5)'] = ' - '.join(map(str, stats_visitante['impedimentos_favor']))

                                dados_mandante['Impedimentos por jogo (total)'] = ' - '.join([str(a+b) for a, b in zip(stats_mandante['impedimentos_favor'], stats_mandante['impedimentos_contra'])])
                                dados_visitante['Impedimentos por jogo (total)'] = ' - '.join([str(a+b) for a, b in zip(stats_visitante['impedimentos_favor'], stats_visitante['impedimentos_contra'])])

                            # Criar tabela comparativa
                            categorias = list(dados_mandante.keys())
                            tabela_comparativa = pd.DataFrame({
                                'Categoria': categorias,
                                jogo['Mandante']: [dados_mandante[cat] for cat in categorias],
                                jogo['Visitante']: [dados_visitante[cat] for cat in categorias]
                            })

                            # Exibir tabela
                            st.dataframe(
                                tabela_comparativa,
                                use_container_width=True,
                                hide_index=True,
                                column_config={
                                    "Categoria": st.column_config.Column(width="large"),
                                    jogo['Mandante']: st.column_config.Column(width="medium"),
                                    jogo['Visitante']: st.column_config.Column(width="medium")
                                }
                            )

                            # Legenda
                            st.caption("🎯 **Legenda:** 🟢 ≥80% | 🟡 60-79% | 🔴 <60%")
                        else:
                            st.warning("Dados insuficientes para análise detalhada")
                    else:
                        st.warning("Dados da liga não disponíveis para análise")

            # Estatísticas e download
            st.subheader("📊 Estatísticas")
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Total de Jogos", len(df_filtrado))
            with col2:
                st.metric("Ligas Diferentes", df_filtrado['Liga'].nunique())
            with col3:
                if 'Data' in df_filtrado.columns:
                    dias = df_filtrado['Data'].nunique()
                    st.metric("Dias com Jogos", dias)

            st.subheader("💾 Exportar Dados")
            csv = df_filtrado.to_csv(index=False, sep=';')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="simulador_apostas.csv",
                mime="text/csv",
                key="download_simulador"
            )
        else:
            st.warning("⚠️ Não há dados disponíveis para simulação")

    # [Mantenha as outras abas aqui...]

else:
    st.error("❌ Não foi possível carregar os dados")

# Rodapé
st.markdown("---")
st.caption("Dados obtidos de football-data.co.uk | Simulador desenvolvido com Streamlit")