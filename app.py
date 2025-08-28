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
    # Usar st.rerun() com time.sleep para simular atualização periódica
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

        # Ler todas as abas do Excel e retornar como dicionário
        todas_abas = pd.read_excel(excel_file, sheet_name=None)
        abas_disponiveis = list(todas_abas.keys())

        st.success(
            f"✅ Arquivo carregado com sucesso! {len(abas_disponiveis)} ligas encontradas - {datetime.now().strftime('%H:%M:%S')}")
        return todas_abas, abas_disponiveis

    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {e}")
        return None, None


def carregar_proximos_jogos(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        excel_file = BytesIO(response.content)

        # Ler os próximos jogos
        df_jogos = pd.read_excel(excel_file)

        # Manter todas as colunas do arquivo original
        st.success(f"✅ Dados do simulador carregados com sucesso! - {datetime.now().strftime('%H:%M:%S')}")
        return df_jogos

    except Exception as e:
        st.error(f"❌ Erro ao carregar dados do simulador: {e}")
        return None


# Carregar dados SEM cache para sempre obter versões atualizadas
todas_abas, abas_disponiveis = carregar_dados_excel(url_excel)
df_proximos_jogos = carregar_proximos_jogos(url_proximos_jogos)

# Exibir hora da última atualização
st.sidebar.markdown(f"**Última atualização:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

# Mapeamento completo com as 18 ligas principais
mapeamento_ligas = {
    # INGLATERRA (4)
    'E0': 'Premier League (Inglaterra)',
    'E1': 'Championship (Inglaterra)',
    'E2': 'League One (Inglaterra)',
    'E3': 'League Two (Inglaterra)',

    # ESCÓCIA (4)
    'SC0': 'Premiership (Escócia)',
    'SC1': 'Championship (Escócia)',
    'SC2': 'League One (Escócia)',
    'SC3': 'League Two (Escócia)',

    # ALEMANHA (2)
    'D1': 'Bundesliga (Alemanha)',
    'D2': '2. Bundesliga (Alemanha)',

    # ITÁLIA (2)
    'I1': 'Serie A (Itália)',
    'I2': 'Serie B (Itália)',

    # ESPANHA (2)
    'SP1': 'La Liga (Espanha)',
    'SP2': 'La Liga 2 (Espanha)',

    # FRANÇA (2)
    'F1': 'Ligue 1 (França)',
    'F2': 'Ligue 2 (França)',

    # HOLANDA (1)
    'N1': 'Eredivisie (Holanda)',

    # BÉLGICA (1)
    'B1': 'Jupiler Pro League (Bélgica)',

    # PORTUGAL (1)
    'P1': 'Primeira Liga (Portugal)',

    # TURQUIA (1)
    'T1': 'Super Lig (Turquia)',

    # GRÉCIA (1)
    'G1': 'Super League (Grécia)'
}

# ⭐⭐ VERIFICAÇÃO DAS LIGAS CARREGADAS ⭐⭐
st.sidebar.markdown("### 🔍 VERIFICAÇÃO DE LIGAS")
if abas_disponiveis:
    st.sidebar.write(f"**Total de ligas carregadas:** {len(abas_disponiveis)}")
    st.sidebar.write("**Ligas encontradas:**")
    for i, aba in enumerate(abas_disponiveis, 1):
        nome = mapeamento_ligas.get(aba, f"{aba} (não mapeada)")
        st.sidebar.write(f"{i}. {aba} - {nome}")
else:
    st.sidebar.write("❌ Nenhuma liga foi carregada")

# Dicionário de tradução das colunas para todas as abas
traducao_colunas = {
    'Div': 'Liga',
    'Date': 'Data',
    'Time': 'Hora',
    'HomeTeam': 'Mandante',
    'AwayTeam': 'Visitante',
    'FTHG': 'Gols Casa',
    'FTAG': 'Gols Fora',
    'FTR': 'Resultado Final',
    'HTHG': 'Gols Casa 1T',
    'HTAG': 'Gols Fora 1T',
    'HTR': 'Resultado 1T',
    'HS': 'Chutes Mandante',
    'AS': 'Chutes Visitante',
    'HST': 'Chutes no Gol Mandante',
    'AST': 'Chutes no Gol Visitante',
    'HF': 'Faltas Mandante',
    'AF': 'Faltas Visitante',
    'HC': 'Escanteios Mandante',
    'AC': 'Escanteios Visitante',
    'HY': 'Cartões Amarelos Mandante',
    'AY': 'Cartões Amarelos Visitante',
    'HR': 'Cartões Vermelhos Mandante',
    'AR': 'Cartões Vermelhos Visitante',
    'B365H': 'B365 Casa',
    'B365D': 'B365 Empate',
    'B365A': 'B365 Fora',
    'B365>2.5': 'B365 Over 2.5',
    'B365<2.5': 'B365 Under 2.5',
    'AvgH': 'Avg Casa',
    'AvgD': 'Avg Empate',
    'AvgA': 'Avg Fora',
    'Avg>2.5': 'Avg Over 2.5',
    'Avg<2.5': 'Avg Under 2.5'
}


# Função para traduzir colunas de um dataframe
def traduzir_colunas_df(df):
    # Criar cópia do dataframe
    df_traduzido = df.copy()

    # Renomear colunas existentes
    colunas_renomear = {}
    for coluna in df_traduzido.columns:
        if coluna in traducao_colunas:
            colunas_renomear[coluna] = traducao_colunas[coluna]

    df_traduzido = df_traduzido.rename(columns=colunas_renomear)

    return df_traduzido


# Função para calcular probabilidades a partir das odds
def calcular_probabilidades(odd):
    if pd.isna(odd) or odd <= 0:
        return 0
    return round((1 / odd) * 100, 1)


# Função para formatar probabilidades com %
def formatar_probabilidade(valor):
    return f"{valor}%"


# Função para calcular relatório detalhado da liga
def calcular_relatorio_liga(df_liga, nome_liga):
    """Calcula estatísticas detalhadas para uma liga específica"""

    if df_liga.empty:
        return None

    # Dicionário para armazenar os resultados
    relatorio = {
        'Liga': nome_liga,
        'Total de Jogos': len(df_liga),
        'Estatísticas': {}
    }

    # Cálculos básicos de resultados
    if 'FTR' in df_liga.columns:
        total_jogos = len(df_liga)
        vitorias_casa = len(df_liga[df_liga['FTR'] == 'H'])
        empates = len(df_liga[df_liga['FTR'] == 'D'])
        vitorias_fora = len(df_liga[df_liga['FTR'] == 'A'])

        relatorio['Estatísticas']['Vitória do Mandante'] = f"{(vitorias_casa / total_jogos) * 100:.1f}%"
        relatorio['Estatísticas']['Empate'] = f"{(empates / total_jogos) * 100:.1f}%"
        relatorio['Estatísticas']['Vitória do Visitante'] = f"{(vitorias_fora / total_jogos) * 100:.1f}%"

    # ⭐⭐ NOVAS ESTATÍSTICAS DE GOLS ⭐⭐
    if 'HTHG' in df_liga.columns and 'HTAG' in df_liga.columns and 'FTHG' in df_liga.columns and 'FTAG' in df_liga.columns:
        total_jogos = len(df_liga)

        # Gols no primeiro tempo (HT)
        total_gols_ht = df_liga['HTHG'].sum() + df_liga['HTAG'].sum()
        media_gols_ht = total_gols_ht / total_jogos
        relatorio['Estatísticas']['Gols HT por Jogo'] = f"{media_gols_ht:.2f}"

        # Gols no tempo total (FT)
        total_gols_ft = df_liga['FTHG'].sum() + df_liga['FTAG'].sum()
        media_gols_ft = total_gols_ft / total_jogos
        relatorio['Estatísticas']['Gols FT por Jogo'] = f"{media_gols_ft:.2f}"

        # Porcentagem de gols no 1º tempo
        if total_gols_ft > 0:
            porcentagem_gols_1t = (total_gols_ht / total_gols_ft) * 100
            relatorio['Estatísticas']['Porcentagem de Gols no 1T'] = f"{porcentagem_gols_1t:.1f}%"

        # Porcentagem de gols no 2º tempo
        if total_gols_ft > 0:
            total_gols_2t = total_gols_ft - total_gols_ht
            porcentagem_gols_2t = (total_gols_2t / total_gols_ft) * 100
            relatorio['Estatísticas']['Porcentagem de Gols no 2T'] = f"{porcentagem_gols_2t:.1f}%"

    # Cálculos de gols - Primeiro Tempo (HT)
    if 'HTHG' in df_liga.columns and 'HTAG' in df_liga.columns:
        total_jogos = len(df_liga)

        # 0.5 HT - Jogos com pelo menos 1 gol no primeiro tempo
        jogos_over_05_ht = len(df_liga[(df_liga['HTHG'] + df_liga['HTAG']) > 0.5])
        relatorio['Estatísticas']['Over 0.5 HT'] = f"{(jogos_over_05_ht / total_jogos) * 100:.1f}%"

        # 1.5 HT - Jogos com pelo menos 2 gols no primeiro tempo
        jogos_over_15_ht = len(df_liga[(df_liga['HTHG'] + df_liga['HTAG']) > 1.5])
        relatorio['Estatísticas']['Over 1.5 HT'] = f"{(jogos_over_15_ht / total_jogos) * 100:.1f}%"

    # Cálculos de gols - Tempo Total (FT)
    if 'FTHG' in df_liga.columns and 'FTAG' in df_liga.columns:
        total_jogos = len(df_liga)

        # 0.5 FT
        jogos_over_05_ft = len(df_liga[(df_liga['FTHG'] + df_liga['FTAG']) > 0.5])
        relatorio['Estatísticas']['Over 0.5 FT'] = f"{(jogos_over_05_ft / total_jogos) * 100:.1f}%"

        # 1.5 FT
        jogos_over_15_ft = len(df_liga[(df_liga['FTHG'] + df_liga['FTAG']) > 1.5])
        relatorio['Estatísticas']['Over 1.5 FT'] = f"{(jogos_over_15_ft / total_jogos) * 100:.1f}%"

        # 2.5 FT
        jogos_over_25_ft = len(df_liga[(df_liga['FTHG'] + df_liga['FTAG']) > 2.5])
        relatorio['Estatísticas']['Over 2.5 FT'] = f"{(jogos_over_25_ft / total_jogos) * 100:.1f}%"

        # 3.5 FT
        jogos_over_35_ft = len(df_liga[(df_liga['FTHG'] + df_liga['FTAG']) > 3.5])
        relatorio['Estatísticas']['Over 3.5 FT'] = f"{(jogos_over_35_ft / total_jogos) * 100:.1f}%"

        # 4.5 FT
        jogos_over_45_ft = len(df_liga[(df_liga['FTHG'] + df_liga['FTAG']) > 4.5])
        relatorio['Estatísticas']['Over 4.5 FT'] = f"{(jogos_over_45_ft / total_jogos) * 100:.1f}%"

        # BTTS FT - Both Teams To Score
        btts_ft = len(df_liga[(df_liga['FTHG'] > 0) & (df_liga['FTAG'] > 0)])
        relatorio['Estatísticas']['BTTS FT'] = f"{(btts_ft / total_jogos) * 100:.1f}%"

    # Cálculos de estatísticas de jogo
    if 'HC' in df_liga.columns and 'AC' in df_liga.columns:
        total_jogos = len(df_liga)
        media_escanteios = (df_liga['HC'].sum() + df_liga['AC'].sum()) / total_jogos
        relatorio['Estatísticas']['Média de Escanteios por Jogo'] = f"{media_escanteios:.1f}"

    if 'HY' in df_liga.columns and 'AY' in df_liga.columns:
        total_jogos = len(df_liga)
        media_amarelos = (df_liga['HY'].sum() + df_liga['AY'].sum()) / total_jogos
        relatorio['Estatísticas']['Média de Cartões Amarelos por Jogo'] = f"{media_amarelos:.1f}"

    if 'HS' in df_liga.columns and 'AS' in df_liga.columns:
        total_jogos = len(df_liga)
        media_chutes = (df_liga['HS'].sum() + df_liga['AS'].sum()) / total_jogos
        relatorio['Estatísticas']['Média de Chutes por Jogo'] = f"{media_chutes:.1f}"

    if 'HST' in df_liga.columns and 'AST' in df_liga.columns:
        total_jogos = len(df_liga)
        media_chutes_gol = (df_liga['HST'].sum() + df_liga['AST'].sum()) / total_jogos
        relatorio['Estatísticas']['Média de Chutes no Gol por Jogo'] = f"{media_chutes_gol:.1f}"

    if 'HF' in df_liga.columns and 'AF' in df_liga.columns:
        total_jogos = len(df_liga)
        media_faltas = (df_liga['HF'].sum() + df_liga['AF'].sum()) / total_jogos
        relatorio['Estatísticas']['Média de Faltas por Jogo'] = f"{media_faltas:.1f}"

    return relatorio


# Função para calcular estatísticas detalhadas por time
def calcular_estatisticas_time(df_liga, nome_time):
    """Calcula estatísticas detalhadas para um time específico em uma liga"""

    # Filtrar jogos onde o time é mandante ou visitante
    jogos_mandante = df_liga[df_liga['HomeTeam'] == nome_time]
    jogos_visitante = df_liga[df_liga['AwayTeam'] == nome_time]

    # Combinar todos os jogos do time
    todos_jogos = pd.concat([jogos_mandante, jogos_visitante])

    if todos_jogos.empty:
        return None, None

    # Ordenar por data (se disponível)
    if 'Date' in todos_jogos.columns:
        todos_jogos = todos_jogos.sort_values('Date')

    # Pegar os últimos 5 jogos
    ultimos_5_jogos = todos_jogos.tail(5)

    # Calcular estatísticas básicas
    total_jogos = len(todos_jogos)

    # Calcular vitórias, empates e derrotas
    vitorias = 0
    empates = 0
    derrotas = 0

    gols_marcados = 0
    gols_sofridos = 0

    gols_marcados_ht = 0
    gols_sofridos_ht = 0

    # Estatísticas de jogo
    escanteios = 0
    cartoes_amarelos = 0
    cartoes_vermelhos = 0
    chutes = 0
    chutes_gol = 0
    faltas = 0

    # Contadores para estatísticas de mercado
    over_05_ht = 0
    over_05_ft = 0
    over_15_ft = 0
    over_25_ft = 0
    btts = 0

    # Listas para estatísticas dos últimos 5 jogos
    chutes_gol_lista = []
    chutes_lista = []
    escanteios_favor_lista = []
    escanteios_contra_lista = []
    escanteios_total_lista = []
    cartoes_amarelos_lista = []
    faltas_total_lista = []

    # Criar lista de índices dos últimos 5 jogos para comparação
    ultimos_5_indices = ultimos_5_jogos.index.tolist()

    for idx, jogo in todos_jogos.iterrows():
        # Determinar se o time é mandante ou visitante
        if jogo['HomeTeam'] == nome_time:
            # Time é mandante
            gols_feitos = jogo['FTHG'] if 'FTHG' in jogo else 0
            gols_sof = jogo['FTAG'] if 'FTAG' in jogo else 0
            gols_feitos_ht = jogo['HTHG'] if 'HTHG' in jogo else 0
            gols_sof_ht = jogo['HTAG'] if 'HTAG' in jogo else 0

            # Resultado
            if jogo['FTR'] == 'H':
                vitorias += 1
            elif jogo['FTR'] == 'D':
                empates += 1
            else:
                derrotas += 1

            # Estatísticas de jogo (mandante)
            escanteios_jogo = jogo['HC'] if 'HC' in jogo and not pd.isna(jogo['HC']) else 0
            cartoes_amarelos_jogo = jogo['HY'] if 'HY' in jogo and not pd.isna(jogo['HY']) else 0
            cartoes_vermelhos_jogo = jogo['HR'] if 'HR' in jogo and not pd.isna(jogo['HR']) else 0
            chutes_jogo = jogo['HS'] if 'HS' in jogo and not pd.isna(jogo['HS']) else 0
            chutes_gol_jogo = jogo['HST'] if 'HST' in jogo and not pd.isna(jogo['HST']) else 0
            faltas_jogo = jogo['HF'] if 'HF' in jogo and not pd.isna(jogo['HF']) else 0

            # Adicionar às listas se for um dos últimos 5 jogos
            if idx in ultimos_5_indices:
                chutes_gol_lista.append(chutes_gol_jogo)
                chutes_lista.append(chutes_jogo)
                escanteios_favor_lista.append(escanteios_jogo)
                escanteios_contra_lista.append(jogo['AC'] if 'AC' in jogo and not pd.isna(jogo['AC']) else 0)
                escanteios_total_lista.append(
                    escanteios_jogo + (jogo['AC'] if 'AC' in jogo and not pd.isna(jogo['AC']) else 0))
                cartoes_amarelos_lista.append(cartoes_amarelos_jogo)
                faltas_total_lista.append(faltas_jogo + (jogo['AF'] if 'AF' in jogo and not pd.isna(jogo['AF']) else 0))

        else:
            # Time é visitante
            gols_feitos = jogo['FTAG'] if 'FTAG' in jogo else 0
            gols_sof = jogo['FTHG'] if 'FTHG' in jogo else 0
            gols_feitos_ht = jogo['HTAG'] if 'HTAG' in jogo else 0
            gols_sof_ht = jogo['HTHG'] if 'HTHG' in jogo else 0

            # Resultado
            if jogo['FTR'] == 'A':
                vitorias += 1
            elif jogo['FTR'] == 'D':
                empates += 1
            else:
                derrotas += 1

            # Estatísticas de jogo (visitante)
            escanteios_jogo = jogo['AC'] if 'AC' in jogo and not pd.isna(jogo['AC']) else 0
            cartoes_amarelos_jogo = jogo['AY'] if 'AY' in jogo and not pd.isna(jogo['AY']) else 0
            cartoes_vermelhos_jogo = jogo['AR'] if 'AR' in jogo and not pd.isna(jogo['AR']) else 0
            chutes_jogo = jogo['AS'] if 'AS' in jogo and not pd.isna(jogo['AS']) else 0
            chutes_gol_jogo = jogo['AST'] if 'AST' in jogo and not pd.isna(jogo['AST']) else 0
            faltas_jogo = jogo['AF'] if 'AF' in jogo and not pd.isna(jogo['AF']) else 0

            # Adicionar às listas se for um dos últimos 5 jogos
            if idx in ultimos_5_indices:
                chutes_gol_lista.append(chutes_gol_jogo)
                chutes_lista.append(chutes_jogo)
                escanteios_favor_lista.append(escanteios_jogo)
                escanteios_contra_lista.append(jogo['HC'] if 'HC' in jogo and not pd.isna(jogo['HC']) else 0)
                escanteios_total_lista.append(
                    escanteios_jogo + (jogo['HC'] if 'HC' in jogo and not pd.isna(jogo['HC']) else 0))
                cartoes_amarelos_lista.append(cartoes_amarelos_jogo)
                faltas_total_lista.append(faltas_jogo + (jogo['HF'] if 'HF' in jogo and not pd.isna(jogo['HF']) else 0))

        # Acumular gols
        gols_marcados += gols_feitos
        gols_sofridos += gols_sof
        gols_marcados_ht += gols_feitos_ht
        gols_sofridos_ht += gols_sof_ht

        # Acumular estatísticas de jogo
        escanteios += escanteios_jogo
        cartoes_amarelos += cartoes_amarelos_jogo
        cartoes_vermelhos += cartoes_vermelhos_jogo
        chutes += chutes_jogo
        chutes_gol += chutes_gol_jogo
        faltas += faltas_jogo

        # Verificar mercados
        total_gols_ht = gols_feitos_ht + gols_sof_ht
        total_gols_ft = gols_feitos + gols_sof

        if total_gols_ht > 0.5:
            over_05_ht += 1

        if total_gols_ft > 0.5:
            over_05_ft += 1

        if total_gols_ft > 1.5:
            over_15_ft += 1

        if total_gols_ft > 2.5:
            over_25_ft += 1

        if gols_feitos > 0 and gols_sof > 0:
            btts += 1

    # Calcular médias
    aproveitamento = (vitorias * 3 + empates) / (total_jogos * 3) * 100 if total_jogos > 0 else 0

    # Calcular médias de gols
    media_gols_marcados_ht = gols_marcados_ht / total_jogos if total_jogos > 0 else 0
    media_gols_sofridos_ht = gols_sofridos_ht / total_jogos if total_jogos > 0 else 0
    media_ht = media_gols_marcados_ht + media_gols_sofridos_ht

    media_gols_marcados_ft = gols_marcados / total_jogos if total_jogos > 0 else 0
    media_gols_sofridos_ft = gols_sofridos / total_jogos if total_jogos > 0 else 0
    media_ft = media_gols_marcados_ft + media_gols_sofridos_ft

    # Preparar dicionário de resultados
    estatisticas = {
        'Time': nome_time,
        'Total Jogos': total_jogos,
        'Vitórias': vitorias,
        'Empates': empates,
        'Derrotas': derrotas,
        'Aproveitamento': f"{aproveitamento:.1f}%",
        'Gols Marcados': gols_marcados,
        'Gols Sofridos': gols_sofridos,
        'Saldo de Gols': gols_marcados - gols_sofridos,
        'Gols Marcados HT': gols_marcados_ht,
        'Gols Sofridos HT': gols_sofridos_ht,
        'Soma HT': gols_marcados_ht + gols_sofridos_ht,
        'Soma FT': gols_marcados + gols_sofridos,
        # Adicionando as médias que estavam faltando
        'Média Gols Marcados HT': f"{media_gols_marcados_ht:.2f}",
        'Média Gols Sofridos HT': f"{media_gols_sofridos_ht:.2f}",
        'Média HT': f"{media_ht:.2f}",
        'Média Gols Marcados FT': f"{media_gols_marcados_ft:.2f}",
        'Média Gols Sofridos FT': f"{media_gols_sofridos_ft:.2f}",
        'Média FT': f"{media_ft:.2f}",
        'Over 0.5 HT': f"{over_05_ht}/{total_jogos} ({over_05_ht / total_jogos * 100:.1f}%)" if total_jogos > 0 else "0/0 (0%)",
        'Over 0.5 FT': f"{over_05_ft}/{total_jogos} ({over_05_ft / total_jogos * 100:.1f}%)" if total_jogos > 0 else "0/0 (0%)",
        'Over 1.5 FT': f"{over_15_ft}/{total_jogos} ({over_15_ft / total_jogos * 100:.1f}%)" if total_jogos > 0 else "0/0 (0%)",
        'Over 2.5 FT': f"{over_25_ft}/{total_jogos} ({over_25_ft / total_jogos * 100:.1f}%)" if total_jogos > 0 else "0/0 (0%)",
        'BTTS': f"{btts}/{total_jogos} ({btts / total_jogos * 100:.1f}%)" if total_jogos > 0 else "0/0 (0%)",
        'Média Escanteios': f"{(escanteios / total_jogos):.1f}" if total_jogos > 0 else "0",
        'Média Cartões Amarelos': f"{(cartoes_amarelos / total_jogos):.1f}" if total_jogos > 0 else "0",
        'Média Cartões Vermelhos': f"{(cartoes_vermelhos / total_jogos):.1f}" if total_jogos > 0 else "0",
        'Média Chutes': f"{(chutes / total_jogos):.1f}" if total_jogos > 0 else "0",
        'Média Chutes no Gol': f"{(chutes_gol / total_jogos):.1f}" if total_jogos > 0 else "0",
        'Média Faltas': f"{(faltas / total_jogos):.1f}" if total_jogos > 0 else "0",
        # Estatísticas dos últimos 5 jogos
        'Chutes no Gol (Últimos 5)': '-'.join(map(str, chutes_gol_lista)) if chutes_gol_lista else 'N/A',
        'Chutes (Últimos 5)': '-'.join(map(str, chutes_lista)) if chutes_lista else 'N/A',
        'Escanteios a Favor (Últimos 5)': '-'.join(
            map(str, escanteios_favor_lista)) if escanteios_favor_lista else 'N/A',
        'Escanteios Contra (Últimos 5)': '-'.join(
            map(str, escanteios_contra_lista)) if escanteios_contra_lista else 'N/A',
        'Escanteios Total (Últimos 5)': '-'.join(map(str, escanteios_total_lista)) if escanteios_total_lista else 'N/A',
        'Cartões Amarelos (Últimos 5)': '-'.join(map(str, cartoes_amarelos_lista)) if cartoes_amarelos_lista else 'N/A',
        'Faltas Total (Últimos 5)': '-'.join(map(str, faltas_total_lista)) if faltas_total_lista else 'N/A',
        # Sequências para alertas
        'Sequencia Chutes Gol': '-'.join(map(str, chutes_gol_lista)) if chutes_gol_lista else 'N/A',
        'Sequencia Chutes': '-'.join(map(str, chutes_lista)) if chutes_lista else 'N/A',
        'Sequencia Escanteios Favor': '-'.join(map(str, escanteios_favor_lista)) if escanteios_favor_lista else 'N/A',
        'Sequencia Escanteios Contra': '-'.join(
            map(str, escanteios_contra_lista)) if escanteios_contra_lista else 'N/A',
        'Sequencia Escanteios Total': '-'.join(map(str, escanteios_total_lista)) if escanteios_total_lista else 'N/A',
        'Sequencia Amarelos': '-'.join(map(str, cartoes_amarelos_lista)) if cartoes_amarelos_lista else 'N/A',
        'Sequencia Faltas': '-'.join(map(str, faltas_total_lista)) if faltas_total_lista else 'N/A'
    }

    return estatisticas, todos_jogos


# Função para analisar sequências e dar dicas
def analisar_sequencias(todos_jogos, nome_time):
    """Analisa as sequências dos últimos 5 jogos e fornece dicas"""

    if len(todos_jogos) < 5:
        return ["⚠️ Time precisa de pelo menos 5 jogos para análise de sequência"]

    # Pegar os últimos 5 jogos
    ultimos_5 = todos_jogos.tail(5)

    dicas = []

    # Verificar sequências de resultados
    resultados = []
    over_05_ht_seq = []
    over_25_ft_seq = []
    btts_seq = []

    for _, jogo in ultimos_5.iterrows():
        # Determinar resultado do time
        if jogo['HomeTeam'] == nome_time:
            resultados.append(jogo['FTR'])
            gols_ht = jogo['HTHG'] + jogo['HTAG'] if 'HTHG' in jogo and 'HTAG' in jogo else 0
            gols_ft = jogo['FTHG'] + jogo['FTAG'] if 'FTHG' in jogo and 'FTAG' in jogo else 0
            btts_jogo = 1 if (jogo['FTHG'] > 0 and jogo['FTAG'] > 0) else 0
        else:
            resultados.append('A' if jogo['FTR'] == 'H' else 'H' if jogo['FTR'] == 'A' else 'D')
            gols_ht = jogo['HTHG'] + jogo['HTAG'] if 'HTHG' in jogo and 'HTAG' in jogo else 0
            gols_ft = jogo['FTHG'] + jogo['FTAG'] if 'FTHG' in jogo and 'FTAG' in jogo else 0
            btts_jogo = 1 if (jogo['FTHG'] > 0 and jogo['FTAG'] > 0) else 0

        over_05_ht_seq.append(1 if gols_ht > 0.5 else 0)
        over_25_ft_seq.append(1 if gols_ft > 2.5 else 0)
        btts_seq.append(btts_jogo)

    # Verificar sequência de vitórias
    if all(r == 'H' or r == 'A' for r in resultados if r != 'D'):
        vitorias_seguidas = sum(1 for r in resultados if r == 'H' or r == 'A')
        dicas.append(f"✅ {vitorias_seguidas} vitórias consecutivas")

    # Verificar sequência de derrotas
    if all(r == 'A' or r == 'H' for r in resultados if r != 'D'):
        derrotas_seguidas = sum(1 for r in resultados if r == 'A' or r == 'H')
        dicas.append(f"❌ {derrotas_seguidas} derrotas consecutivas")

    # Verificar sequência de Over 0.5 HT
    if sum(over_05_ht_seq) >= 4:
        dicas.append(f"⚽ Over 0.5 HT em {sum(over_05_ht_seq)} dos últimos 5 jogos")

    # Verificar sequência de Over 2.5 FT
    if sum(over_25_ft_seq) >= 4:
        dicas.append(f"🥅 Over 2.5 FT em {sum(over_25_ft_seq)} dos últimos 5 jogos")

    # Verificar sequência de BTTS
    if sum(btts_seq) >= 4:
        dicas.append(f"🔁 BTTS em {sum(btts_seq)} dos últimos 5 jogos")

    # Verificar sequência sem vitórias
    if not any(r == 'H' or r == 'A' for r in resultados):
        dicas.append("😞 Sem vitórias nos últimos 5 jogos")

    # Verificar sequência sem derrotas
    if not any(r == 'A' or r == 'H' for r in resultados):
        dicas.append("🛡️ Sem derrotas nos últimos 5 jogos")

    if not dicas:
        dicas.append("📊 Sem sequências significativas nos últimos 5 jogos")

    return dicas


# Função para analisar sequências estatísticas relevantes
def analisar_sequencias_estatisticas(todos_jogos, nome_time, estatisticas):
    """Analisa sequências estatísticas relevantes nos últimos 5 jogos"""

    if len(todos_jogos) < 5:
        return ["⚠️ Time precisa de pelo menos 5 jogos para análise de sequência"]

    # Pegar os últimos 5 jogos
    ultimos_5 = todos_jogos.tail(5)

    alertas = []

    # Listas para armazenar estatísticas dos últimos 5 jogos
    over_05_ht_seq = []
    over_05_ft_seq = []
    over_15_ft_seq = []
    over_25_ft_seq = []
    btts_seq = []
    chutes_favor_seq = []
    chutes_total_seq = []
    escanteios_favor_seq = []
    escanteios_total_seq = []
    amarelos_favor_seq = []

    for _, jogo in ultimos_5.iterrows():
        # Determinar se o time é mandante ou visitante
        if jogo['HomeTeam'] == nome_time:
            # Time é mandante
            gols_ht = jogo['HTHG'] + jogo['HTAG'] if 'HTHG' in jogo and 'HTAG' in jogo else 0
            gols_ft = jogo['FTHG'] + jogo['FTAG'] if 'FTHG' in jogo and 'FTAG' in jogo else 0
            btts_jogo = 1 if (jogo['FTHG'] > 0 and jogo['FTAG'] > 0) else 0

            # Estatísticas de jogo
            chutes_favor = jogo['HS'] if 'HS' in jogo and not pd.isna(jogo['HS']) else 0
            chutes_total = chutes_favor + (jogo['AS'] if 'AS' in jogo and not pd.isna(jogo['AS']) else 0)
            escanteios_favor = jogo['HC'] if 'HC' in jogo and not pd.isna(jogo['HC']) else 0
            escanteios_total = escanteios_favor + (jogo['AC'] if 'AC' in jogo and not pd.isna(jogo['AC']) else 0)
            amarelos_favor = jogo['HY'] if 'HY' in jogo and not pd.isna(jogo['HY']) else 0

        else:
            # Time é visitante
            gols_ht = jogo['HTHG'] + jogo['HTAG'] if 'HTHG' in jogo and 'HTAG' in jogo else 0
            gols_ft = jogo['FTHG'] + jogo['FTAG'] if 'FTHG' in jogo and 'FTAG' in jogo else 0
            btts_jogo = 1 if (jogo['FTHG'] > 0 and jogo['FTAG'] > 0) else 0

            # Estatísticas de jogo
            chutes_favor = jogo['AS'] if 'AS' in jogo and not pd.isna(jogo['AS']) else 0
            chutes_total = chutes_favor + (jogo['HS'] if 'HS' in jogo and not pd.isna(jogo['HS']) else 0)
            escanteios_favor = jogo['AC'] if 'AC' in jogo and not pd.isna(jogo['AC']) else 0
            escanteios_total = escanteios_favor + (jogo['HC'] if 'HC' in jogo and not pd.isna(jogo['HC']) else 0)
            amarelos_favor = jogo['AY'] if 'AY' in jogo and not pd.isna(jogo['AY']) else 0

        # Acumular estatísticas
        over_05_ht_seq.append(1 if gols_ht > 0.5 else 0)
        over_05_ft_seq.append(1 if gols_ft > 0.5 else 0)
        over_15_ft_seq.append(1 if gols_ft > 1.5 else 0)
        over_25_ft_seq.append(1 if gols_ft > 2.5 else 0)
        btts_seq.append(btts_jogo)
        chutes_favor_seq.append(chutes_favor)
        chutes_total_seq.append(chutes_total)
        escanteios_favor_seq.append(escanteios_favor)
        escanteios_total_seq.append(escanteios_total)
        amarelos_favor_seq.append(amarelos_favor)

    # Verificar sequências de Over 0.5 HT
    if sum(over_05_ht_seq) == 5:
        alertas.append(f"✅ {nome_time} tem 5 jogos seguidos com Over 0.5 Gols HT")

    # Verificar sequências de Over 0.5 FT
    if sum(over_05_ft_seq) == 5:
        alertas.append(f"✅ {nome_time} tem 5 jogos seguidos com Over 0.5 Gols FT")

    # Verificar sequências de Over 1.5 FT
    if sum(over_15_ft_seq) == 5:
        alertas.append(f"✅ {nome_time} tem 5 jogos seguidos com Over 1.5 Gols FT")

    # Verificar sequências de Over 2.5 FT
    if sum(over_25_ft_seq) == 5:
        alertas.append(f"✅ {nome_time} tem 5 jogos seguidos com Over 2.5 Gols FT")

    # Verificar sequências de BTTS
    if sum(btts_seq) == 5:
        alertas.append(f"✅ {nome_time} tem 5 jogos seguidos com BTTS")

    # Verificar sequências de Chutes a Favor >= 11
    if all(chutes >= 11 for chutes in chutes_favor_seq):
        alertas.append(
            f"✅ {nome_time} tem 5 jogos seguidos com Total de Chutes a Favor >=11 | Últimos 5 Jogos = {'-'.join(map(str, chutes_favor_seq))}")

    # Verificar sequências de Chutes Totais >= 17
    if all(chutes >= 17 for chutes in chutes_total_seq):
        alertas.append(
            f"✅ {nome_time} tem 5 jogos seguidos com Total de Chutes >=17 | Últimos 5 Jogos = {'-'.join(map(str, chutes_total_seq))}")

    # Verificar sequências de Escanteios a Favor >= 7
    if all(escanteios >= 7 for escanteios in escanteios_favor_seq):
        alertas.append(
            f"✅ {nome_time} tem 5 jogos seguidos com Total Escanteios a Favor >=7 | Últimos 5 Jogos = {'-'.join(map(str, escanteios_favor_seq))}")

    # Verificar sequências de Escanteios Totais >= 7
    if all(escanteios >= 7 for escanteios in escanteios_total_seq):
        alertas.append(
            f"✅ {nome_time} tem 5 jogos seguidos com Total Escanteios >=7 | Últimos 5 Jogos = {'-'.join(map(str, escanteios_total_seq))}")

    # Verificar sequências de Cartões Amarelos a Favor >= 2
    if all(amarelos >= 2 for amarelos in amarelos_favor_seq):
        alertas.append(
            f"✅ {nome_time} tem 5 jogos seguidos com Total Cartão Amarelo a Favor >=2 | Últimos 5 Jogos = {'-'.join(map(str, amarelos_favor_seq))}")

    if not alertas:
        alertas.append("📊 Sem sequências estatísticas relevantes nos últimos 5 jogos")

    return alertas


# Criar abas principais
if todas_abas is not None and abas_disponiveis:
    # Criar abas: Simulador primeiro, depois Relatórios, depois Times, depois Buscar Equipe, depois cada liga
    nomes_abas = ["🎯 Simulador", "📊 Relatórios Liga", "👥 Análise por Time", "🔍 Buscar Equipe"]
    nomes_abas.extend([mapeamento_ligas.get(aba, f"{aba} (Liga)") for aba in abas_disponiveis])

    tabs = st.tabs(nomes_abas)

    # ABA 1: SIMULADOR (Todos os Próximos Jogos)
    with tabs[0]:
        st.header("🏆 Atualização dos jogos até 24h antes de cada rodada.")

        if df_proximos_jogos is not None and not df_proximos_jogos.empty:
            # Selecionar apenas las colunas desejadas
            colunas_desejadas = ['Div', 'Date', 'HomeTeam', 'AwayTeam', 'B365H', 'B365D', 'B365A', 'B365>2.5',
                                 'B365<2.5']

            # Verificar quais colunas existen no dataframe
            colunas_existentes = [col for col in colunas_desejadas if col in df_proximos_jogos.columns]

            # Criar novo dataframe apenas com as colunas desejadas
            df_simulador = df_proximos_jogos[colunas_existentes].copy()

            # Converter a coluna Date para datetime e formatar para DD/MM
            if 'Date' in df_simulador.columns:
                df_simulador['Date'] = pd.to_datetime(df_simulador['Date'], errors='coerce')
                # Formatar data para DD/MM/YYYY
                df_simulador['Date'] = df_simulador['Date'].dt.strftime('%d/%m/%Y')

            # Renomear colunas para português E substituir abreviações por nomes complete
            df_simulador = df_simulador.rename(columns={
                'Div': 'Liga',
                'Date': 'Data',
                'HomeTeam': 'Mandante',
                'AwayTeam': 'Visitante'
            })

            # SUBSTITUIR ABREVIAÇÕES POR NOMES COMPLETOS NA COLUNA LIGA
            df_simulador['Liga'] = df_simulador['Liga'].map(mapeamento_ligas).fillna(df_simulador['Liga'])

            # CALCULAR PROBABILIDADES DAS ODDS
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

            # FORMATAR PROBABILIDADES COM % E UMA CASA DECIMAL
            colunas_probabilidades = ['Vitória', 'Empate', 'Derrota', 'Over 2.5 FT', 'Under 2.5 FT']
            for coluna in colunas_probabilidades:
                if coluna in df_simulador.columns:
                    df_simulador[coluna] = df_simulador[coluna].apply(formatar_probabilidade)

            # REORDENAR COLUNAS NA ORDEN SOLICITADA
            colunas_ordenadas = ['Data', 'Liga', 'Mandante', 'Visitante']
            colunas_probabilidades = ['Vitória', 'Empate', 'Derrota', 'Over 2.5 FT', 'Under 2.5 FT']

            # Adicionar colunas de probabilidades se existirem
            for coluna in colunas_probabilidades:
                if coluna in df_simulador.columns:
                    colunas_ordenadas.append(coluna)

            # Manter as colunas de odds originais também
            colunas_odds_originais = ['B365H', 'B365D', 'B365A', 'B365>2.5', 'B365<2.5']
            for coluna in colunas_odds_originais:
                if coluna in df_simulador.columns:
                    colunas_ordenadas.append(coluna)

            df_simulador = df_simulador[colunas_ordenadas]

            # Ordenar por data (convertendo para datetime para ordenação correta)
            if 'Data' in df_simulador.columns:
                df_simulador['Data_Ordenacao'] = pd.to_datetime(df_simulador['Data'], format='%d/%m/%Y',
                                                                errors='coerce')
                df_simulador = df_simulador.sort_values('Data_Ordenacao')
                df_simulador = df_simulador.drop('Data_Ordenacao', axis=1)

            # Filtros para o simulador
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

            # Aplicar filtros
            df_filtrado = df_simulador.copy()

            if liga_filtro != "Todas as Ligas":
                df_filtrado = df_filtrado[df_filtrado['Liga'] == liga_filtro]

            if 'Data' in df_filtrado.columns and 'data_filtro' in locals() and data_filtro != "Todas as Datas":
                df_filtrado = df_filtrado[df_filtrado['Data'] == data_filtro]

            # Exibir dados filtrados
            st.subheader("⚡️ Jogos da Rodada ⚡️ ")

            # Mostrar contador de resultados
            st.info(f"📊 **{len(df_filtrado)} jogos encontrados**")

            # Exibir tabela com filtros nos cabeçalhos
            st.dataframe(df_filtrado, use_container_width=True, height=500)

            # Estatísticas do simulador (usando valores numéricos para cálculos)
            st.subheader("📊 Estatísticas")

            # Criar cópia para cálculos (sem o %)
            df_calculos = df_simulador.copy()
            for coluna in colunas_probabilidades:
                if coluna in df_calculos.columns:
                    df_calculos[coluna] = df_calculos[coluna].str.replace('%', '').astype(float)

            # Aplicar mesmos filtros ao dataframe de cálculos
            df_calculos_filtrado = df_calculos.copy()
            if liga_filtro != "Todas as Ligas":
                df_calculos_filtrado = df_calculos_filtrado[df_calculos_filtrado['Liga'] == liga_filtro]
            if 'Data' in df_calculos_filtrado.columns and 'data_filtro' in locals() and data_filtro != "Todas as Datas":
                df_calculos_filtrado = df_calculos_filtrado[df_calculos_filtrado['Data'] == data_filtro]

            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.metric("Total de Jogos", len(df_filtrado))

            with col2:
                st.metric("Ligas Diferentes", df_filtrado['Liga'].nunique())

            with col3:
                if 'Data' in df_filtrado.columns:
                    dias = df_filtrado['Data'].nunique()
                    st.metric("Dias com Jogos", dias)

            with col4:
                if 'Vitória' in df_calculos_filtrado.columns:
                    media_vitoria = df_calculos_filtrado['Vitória'].mean()
                    st.metric("Média Vitória", f"{media_vitoria:.1f}%")

            with col5:
                if 'Over 2.5 FT' in df_calculos_filtrado.columns:
                    media_over = df_calculos_filtrado['Over 2.5 FT'].mean()
                    st.metric("Média Over 2.5", f"{media_over:.1f}%")

            # Download dos dados
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

    # ABA 2: RELATÓRIOS LIGA
    with tabs[1]:
        st.header("📊 Relatórios Detalhados por Liga")

        # ⭐⭐ CORREÇÃO: Verificar se há abas disponíveis ⭐⭐
        if not abas_disponiveis:
            st.warning("⚠️ Nenhuma liga disponível para análise")
        else:
            # Selecionar liga para análise
            ligas_disponiveis_relatorios = []
            for aba in abas_disponiveis:
                nome_completo = mapeamento_ligas.get(aba, f"{aba} (Liga)")
                ligas_disponiveis_relatorios.append((aba, nome_completo))

            # Ordenar por nome completo
            ligas_disponiveis_relatorios.sort(key=lambda x: x[1])

            opcoes_ligas = [f"{nome} ({codigo})" for codigo, nome in ligas_disponiveis_relatorios]

            liga_selecionada = st.selectbox(
                "Selecione a liga para análise:",
                options=opcoes_ligas,
                index=0
            )

            # Extrair código da liga selecionada
            codigo_liga_selecionada = liga_selecionada.split('(')[-1].replace(')', '').strip()
            nome_liga_selecionada = liga_selecionada.split('(')[0].strip()

            # Gerar relatório
            if st.button("Gerar Relatório", type="primary"):
                if codigo_liga_selecionada in todas_abas:
                    df_liga = todas_abas[codigo_liga_selecionada]
                    relatorio = calcular_relatorio_liga(df_liga, nome_liga_selecionada)

                    if relatorio:
                        st.success(f"Relatório gerado para {nome_liga_selecionada}")

                        # Exibir estatísticas em cards
                        st.subheader(f"📈 Estatísticas Gerais - {nome_liga_selecionada}")

                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.metric("Total de Jogos", relatorio['Total de Jogos'])

                        # Calcular média de gols
                        if 'FTHG' in df_liga.columns and 'FTAG' in df_liga.columns:
                            total_gols = df_liga['FTHG'].sum() + df_liga['FTAG'].sum()
                            media_gols = total_gols / relatorio['Total de Jogos']
                            with col2:
                                st.metric("Média de Gols", f"{media_gols:.2f}")

                        # Calcular porcentagem de jogos com gols
                        if 'FTHG' in df_liga.columns and 'FTAG' in df_liga.columns:
                            jogos_sem_gols = len(df_liga[(df_liga['FTHG'] == 0) & (df_liga['FTAG'] == 0)])
                            porcentagem_sem_gols = (jogos_sem_gols / relatorio['Total de Jogos']) * 100
                            with col3:
                                st.metric("Jogos sem Gols", f"{porcentagem_sem_gols:.1f}%")

                        # Exibir estatísticas em tabela organizada
                        st.subheader("📋 Estatísticas Detalhadas")

                        # Organizar estatísticas in categorias
                        categorias = {
                            'Resultados': ['Vitória do Mandante', 'Empate', 'Vitória do Visitante'],
                            'Estatísticas de Gols': ['Gols HT por Jogo', 'Gols FT por Jogo',
                                                     'Porcentagem de Gols no 1T', 'Porcentagem de Gols no 2T'],
                            'Primeiro Tempo': ['Over 0.5 HT', 'Over 1.5 HT'],
                            'Tempo Total': ['Over 0.5 FT', 'Over 1.5 FT', 'Over 2.5 FT',
                                            'Over 3.5 FT', 'Over 4.5 FT', 'BTTS FT'],
                            'Estatísticas de Jogo': ['Média de Escanteios por Jogo',
                                                     'Média de Cartões Amarelos por Jogo',
                                                     'Média de Chutes por Jogo', 'Média de Chutes no Gol por Jogo',
                                                     'Média de Faltas por Jogo']
                        }

                        for categoria, estatisticas in categorias.items():
                            st.markdown(f"**{categoria}**")

                            dados_categoria = []
                            for estatistica in estatisticas:
                                if estatistica in relatorio['Estatísticas']:
                                    dados_categoria.append({
                                        'Estatística': estatistica,
                                        'Valor': relatorio['Estatísticas'][estatistica]
                                    })

                            if dados_categoria:
                                df_categoria = pd.DataFrame(dados_categoria)
                                st.dataframe(df_categoria, use_container_width=True, hide_index=True)

                        # Download do relatório
                        st.subheader("💾 Exportar Relatório")

                        # Converter relatório para DataFrame
                        dados_relatorio = []
                        for estatistica, valor in relatorio['Estatísticas'].items():
                            dados_relatorio.append({'Estatística': estatistica, 'Valor': valor})

                        df_relatorio = pd.DataFrame(dados_relatorio)
                        csv = df_relatorio.to_csv(index=False, sep=';')

                        st.download_button(
                            label="📥 Download Relatório CSV",
                            data=csv,
                            file_name=f"relatorio_{codigo_liga_selecionada}.csv",
                            mime="text/csv",
                            key=f"download_relatorio_{codigo_liga_selecionada}"
                        )

                    else:
                        st.error("Não foi possível gerar o relatório para esta liga.")
                else:
                    st.error("Liga selecionada não encontrada nos dados.")

            # Informações adicionais
            st.markdown("---")
            st.info("""
            **📝 Notas sobre as estatísticas:**
            - Todas as porcentagens são calculadas com base no total de jogos da temporada
            - **Gols HT**: Gols no primeiro tempo (primeiros 45 minutos)
            - **Gols FT**: Gols no tempo total (jogo completo)
            - **Over X.5**: Porcentagem de jogos com mais de X gols no tempo especificado
            - **BTTS**: Both Teams To Score - Ambos os times marcaram gols
            - As médias são calculadas por jogo
            """)

    # ABA 3: ANÁLISE POR TIME
    with tabs[2]:
        st.header("👥 Análise Detalhada por Time")

        if not abas_disponiveis:
            st.warning("⚠️ Nenhuma liga disponível para análise")
        else:
            # Selecionar liga primeiro
            ligas_disponiveis_times = []
            for aba in abas_disponiveis:
                nome_completo = mapeamento_ligas.get(aba, f"{aba} (Liga)")
                ligas_disponiveis_times.append((aba, nome_completo))

            # Ordenar por nome completo
            ligas_disponiveis_times.sort(key=lambda x: x[1])

            opcoes_ligas_times = [f"{nome} ({codigo})" for codigo, nome in ligas_disponiveis_times]

            liga_selecionada_time = st.selectbox(
                "Selecione a liga:",
                options=opcoes_ligas_times,
                index=0,
                key="liga_times"
            )

            # Extrair código da liga selecionada
            codigo_liga_selecionada_time = liga_selecionada_time.split('(')[-1].replace(')', '').strip()

            if codigo_liga_selecionada_time in todas_abas:
                df_liga_time = todas_abas[codigo_liga_selecionada_time]

                # Obter lista de times únicos
                times_mandantes = df_liga_time['HomeTeam'].unique() if 'HomeTeam' in df_liga_time.columns else []
                times_visitantes = df_liga_time['AwayTeam'].unique() if 'AwayTeam' in df_liga_time.columns else []
                todos_times = sorted(list(set(list(times_mandantes) + list(times_visitantes))))

                if todos_times:
                    # Criar expanders para cada time
                    for time in todos_times:
                        with st.expander(f"🔍 {time}"):
                            estatisticas, todos_jogos = calcular_estatisticas_time(df_liga_time, time)

                            if estatisticas:
                                # ⭐⭐ MODIFICAÇÃO: Aumentar o tamanho da fonte ⭐⭐
                                st.markdown("""
                                    <style>
                                    .medium-text {
                                        font-size: 16px;
                                        margin-bottom: 8px;
                                        line-height: 1.4;
                                    }
                                    .section-divider {
                                        border-top: 2px solid #ddd;
                                        margin: 15px 0;
                                        padding-top: 15px;
                                    }
                                    .highlight {
                                        font-weight: bold;
                                        color: #1f77b4;
                                    }
                                    .alert-text {
                                        font-size: 16px;
                                        margin-bottom: 8px;
                                        line-height: 1.4;
                                        color: #ff4b4b;
                                        font-weight: bold;
                                    }
                                    </style>
                                """, unsafe_allow_html=True)

                                # Estatísticas Básicas
                                st.markdown(
                                    f'<div class="medium-text"><span class="highlight">Jogos</span> = {estatisticas["Total Jogos"]}</div>',
                                    unsafe_allow_html=True)
                                st.markdown(
                                    f'<div class="medium-text"><span class="highlight">Jogos 0.5 HT</span> = {estatisticas["Over 0.5 HT"]}</div>',
                                    unsafe_allow_html=True)
                                st.markdown(
                                    f'<div class="medium-text"><span class="highlight">Jogos 0.5 FT</span> = {estatisticas["Over 0.5 FT"]}</div>',
                                    unsafe_allow_html=True)
                                st.markdown(
                                    f'<div class="medium-text"><span class="highlight">Jogos 1.5 FT</span> = {estatisticas["Over 1.5 FT"]}</div>',
                                    unsafe_allow_html=True)
                                st.markdown(
                                    f'<div class="medium-text"><span class="highlight">Jogos 2.5 FT</span> = {estatisticas["Over 2.5 FT"]}</div>',
                                    unsafe_allow_html=True)
                                st.markdown(
                                    f'<div class="medium-text"><span class="highlight">Jogos BTTS</span> = {estatisticas["BTTS"]}</div>',
                                    unsafe_allow_html=True)

                                vit_percent = (estatisticas["Vitórias"] / estatisticas["Total Jogos"] * 100) if \
                                estatisticas["Total Jogos"] > 0 else 0
                                emp_percent = (estatisticas["Empates"] / estatisticas["Total Jogos"] * 100) if \
                                estatisticas["Total Jogos"] > 0 else 0
                                der_percent = (estatisticas["Derrotas"] / estatisticas["Total Jogos"] * 100) if \
                                estatisticas["Total Jogos"] > 0 else 0

                                st.markdown(
                                    f'<div class="medium-text"><span class="highlight">Vitórias %</span> = {estatisticas["Vitórias"]}/{estatisticas["Total Jogos"]} {vit_percent:.1f}%</div>',
                                    unsafe_allow_html=True)
                                st.markdown(
                                    f'<div class="medium-text"><span class="highlight">Empates %</span> = {estatisticas["Empates"]}/{estatisticas["Total Jogos"]} {emp_percent:.1f}%</div>',
                                    unsafe_allow_html=True)
                                st.markdown(
                                    f'<div class="medium-text"><span class="highlight">Derrotas %</span> = {estatisticas["Derrotas"]}/{estatisticas["Total Jogos"]} {der_percent:.1f}%</div>',
                                    unsafe_allow_html=True)

                                st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

                                # Estatísticas de Gols
                                st.markdown(
                                    f'<div class="medium-text"><span class="highlight">Média de Gols Marcados HT</span> = {estatisticas["Média Gols Marcados HT"]}</div>',
                                    unsafe_allow_html=True)
                                st.markdown(
                                    f'<div class="medium-text"><span class="highlight">Média de Gols Sofridos HT</span> = {estatisticas["Média Gols Sofridos HT"]}</div>',
                                    unsafe_allow_html=True)
                                st.markdown(
                                    f'<div class="medium-text"><span class="highlight">Média HT</span> = {estatisticas["Média HT"]}</div>',
                                    unsafe_allow_html=True)
                                st.markdown(
                                    f'<div class="medium-text"><span class="highlight">Média de Gols Marcados FT</span> = {estatisticas["Média Gols Marcados FT"]}</div>',
                                    unsafe_allow_html=True)
                                st.markdown(
                                    f'<div class="medium-text"><span class="highlight">Média de Gols Sofridos FT</span> = {estatisticas["Média Gols Sofridos FT"]}</div>',
                                    unsafe_allow_html=True)
                                st.markdown(
                                    f'<div class="medium-text"><span class="highlight">Média FT</span> = {estatisticas["Média FT"]}</div>',
                                    unsafe_allow_html=True)

                                st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

                                # Estatísticas dos Últimos 5 Jogos
                                st.markdown(
                                    f'<div class="medium-text"><span class="highlight">Total de Chutes no Gol a favor | Últimos 5 Jogos</span> = {estatisticas["Chutes no Gol (Últimos 5)"]}</div>',
                                    unsafe_allow_html=True)
                                st.markdown(
                                    f'<div class="medium-text"><span class="highlight">Total de Chutes a favor | Últimos 5 Jogos</span> = {estatisticas["Chutes (Últimos 5)"]}</div>',
                                    unsafe_allow_html=True)
                                st.markdown(
                                    f'<div class="medium-text"><span class="highlight">Total Escanteios a Favor | Últimos 5 Jogos</span> = {estatisticas["Escanteios a Favor (Últimos 5)"]}</div>',
                                    unsafe_allow_html=True)
                                st.markdown(
                                    f'<div class="medium-text"><span class="highlight">Total de Escanteios por jogo | Últimos 5 Jogos</span> = {estatisticas["Escanteios Total (Últimos 5)"]}</div>',
                                    unsafe_allow_html=True)
                                st.markdown(
                                    f'<div class="medium-text"><span class="highlight">Total Cartão Amarelo a Favor | Últimos 5 Jogos</span> = {estatisticas["Cartões Amarelos (Últimos 5)"]}</div>',
                                    unsafe_allow_html=True)
                                st.markdown(
                                    f'<div class="medium-text"><span class="highlight">Total de Cartão Amarelo por jogo | Últimos 5 Jogos</span> = {estatisticas["Cartões Amarelos (Últimos 5)"]}</div>',
                                    unsafe_allow_html=True)
                                st.markdown(
                                    f'<div class="medium-text"><span class="highlight">Total de faltas a favor | Últimos 5 Jogos</span> = {estatisticas["Faltas Total (Últimos 5)"]}</div>',
                                    unsafe_allow_html=True)
                                st.markdown(
                                    f'<div class="medium-text"><span class="highlight">Total de faltas por jogo | Últimos 5 Jogos</span> = {estatisticas["Faltas Total (Últimos 5)"]}</div>',
                                    unsafe_allow_html=True)

                                # Análise de sequências e dicas
                                st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
                                st.markdown(
                                    '<div class="medium-text"><span class="highlight">💡 Análise de Sequências (Últimos 5 Jogos):</span></div>',
                                    unsafe_allow_html=True)

                                dicas = analisar_sequencias(todos_jogos, time)
                                for dica in dicas:
                                    st.markdown(f'<div class="medium-text">{dica}</div>', unsafe_allow_html=True)

                                # Alertas estatísticos
                                st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
                                st.markdown(
                                    '<div class="medium-text"><span class="highlight" style="color: #ff4b4b;">🚨 ALERTAS ESTATÍSTICOS (Últimos 5 Jogos):</span></div>',
                                    unsafe_allow_html=True)

                                alertas = analisar_sequencias_estatisticas(todos_jogos, time, estatisticas)
                                for alerta in alertas:
                                    st.markdown(f'<div class="alert-text">{alerta}</div>', unsafe_allow_html=True)

                                # Download das estatísticas
                                st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
                                df_estatisticas = pd.DataFrame([estatisticas])
                                csv = df_estatisticas.to_csv(index=False, sep=';')

                                st.download_button(
                                    label=f"📥 Download Estatísticas {time}",
                                    data=csv,
                                    file_name=f"estatisticas_{time}.csv",
                                    mime="text/csv",
                                    key=f"download_time_{time}_{codigo_liga_selecionada_time}"
                                )
                else:
                    st.warning("Nenhum time encontrado nesta liga.")
            else:
                st.error("Liga selecionada não encontrada nos dados.")

    # ABA 4: BUSCAR EQUIPE (nova aba)
    with tabs[3]:
        st.header("🔍 Buscar Equipe - Todas as Ligas")

        if todas_abas is not None and abas_disponiveis:
            # Coletar todos os times de todas as ligas
            todos_times_todas_ligas = []
            times_por_liga = {}

            for codigo_liga in abas_disponiveis:
                df_liga = todas_abas[codigo_liga]
                nome_liga = mapeamento_ligas.get(codigo_liga, f"{codigo_liga} (Liga)")

                # Obter times da liga
                times_mandantes = df_liga['HomeTeam'].unique() if 'HomeTeam' in df_liga.columns else []
                times_visitantes = df_liga['AwayTeam'].unique() if 'AwayTeam' in df_liga.columns else []
                times_liga = sorted(list(set(list(times_mandantes) + list(times_visitantes))))

                # Armazenar informações
                for time in times_liga:
                    todos_times_todas_ligas.append((time, nome_liga, codigo_liga))
                    if time not in times_por_liga:
                        times_por_liga[time] = []
                    times_por_liga[time].append(nome_liga)

            # Ordenar times alfabeticamente
            todos_times_todas_ligas.sort(key=lambda x: x[0])

            # Busca rápida por nome do time
            st.subheader("🔎 Busca Rápida")
            termo_busca = st.text_input("Digite o nome do time:", "")

            # Filtrar times com base na busca
            times_filtrados = todos_times_todas_ligas
            if termo_busca:
                times_filtrados = [t for t in todos_times_todas_ligas if termo_busca.lower() in t[0].lower()]

            st.info(f"📋 Encontrados {len(times_filtrados)} times")

            # Exibir todos os times em expanders
            st.subheader("📋 Lista de Times (Ordenados Alfabeticamente)")

            for time_info in times_filtrados:
                time_nome, liga_nome, codigo_liga = time_info

                with st.expander(f"⚽ {time_nome} - {liga_nome}"):
                    # Carregar dados da liga específica
                    df_liga_especifica = todas_abas[codigo_liga]

                    # Calcular estatísticas do time
                    estatisticas, todos_jogos = calcular_estatisticas_time(df_liga_especifica, time_nome)

                    if estatisticas:
                        # Aplicar o mesmo estilo da aba "Análise por Time"
                        st.markdown("""
                            <style>
                            .medium-text {
                                font-size: 16px;
                                margin-bottom: 8px;
                                line-height: 1.4;
                            }
                            .section-divider {
                                border-top: 2px solid #ddd;
                                margin: 15px 0;
                                padding-top: 15px;
                            }
                            .highlight {
                                font-weight: bold;
                                color: #1f77b4;
                            }
                            .alert-text {
                                font-size: 16px;
                                margin-bottom: 8px;
                                line-height: 1.4;
                                color: #ff4b4b;
                                font-weight: bold;
                            }
                            </style>
                        """, unsafe_allow_html=True)

                        # Estatísticas Básicas
                        st.markdown(f'<div class="medium-text"><span class="highlight">Liga</span> = {liga_nome}</div>',
                                    unsafe_allow_html=True)
                        st.markdown(
                            f'<div class="medium-text"><span class="highlight">Jogos</span> = {estatisticas["Total Jogos"]}</div>',
                            unsafe_allow_html=True)
                        st.markdown(
                            f'<div class="medium-text"><span class="highlight">Jogos 0.5 HT</span> = {estatisticas["Over 0.5 HT"]}</div>',
                            unsafe_allow_html=True)
                        st.markdown(
                            f'<div class="medium-text"><span class="highlight">Jogos 0.5 FT</span> = {estatisticas["Over 0.5 FT"]}</div>',
                            unsafe_allow_html=True)
                        st.markdown(
                            f'<div class="medium-text"><span class="highlight">Jogos 1.5 FT</span> = {estatisticas["Over 1.5 FT"]}</div>',
                            unsafe_allow_html=True)
                        st.markdown(
                            f'<div class="medium-text"><span class="highlight">Jogos 2.5 FT</span> = {estatisticas["Over 2.5 FT"]}</div>',
                            unsafe_allow_html=True)
                        st.markdown(
                            f'<div class="medium-text"><span class="highlight">Jogos BTTS</span> = {estatisticas["BTTS"]}</div>',
                            unsafe_allow_html=True)

                        vit_percent = (estatisticas["Vitórias"] / estatisticas["Total Jogos"] * 100) if estatisticas[
                                                                                                            "Total Jogos"] > 0 else 0
                        emp_percent = (estatisticas["Empates"] / estatisticas["Total Jogos"] * 100) if estatisticas[
                                                                                                           "Total Jogos"] > 0 else 0
                        der_percent = (estatisticas["Derrotas"] / estatisticas["Total Jogos"] * 100) if estatisticas[
                                                                                                            "Total Jogos"] > 0 else 0

                        st.markdown(
                            f'<div class="medium-text"><span class="highlight">Vitórias %</span> = {estatisticas["Vitórias"]}/{estatisticas["Total Jogos"]} {vit_percent:.1f}%</div>',
                            unsafe_allow_html=True)
                        st.markdown(
                            f'<div class="medium-text"><span class="highlight">Empates %</span> = {estatisticas["Empates"]}/{estatisticas["Total Jogos"]} {emp_percent:.1f}%</div>',
                            unsafe_allow_html=True)
                        st.markdown(
                            f'<div class="medium-text"><span class="highlight">Derrotas %</span> = {estatisticas["Derrotas"]}/{estatisticas["Total Jogos"]} {der_percent:.1f}%</div>',
                            unsafe_allow_html=True)

                        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

                        # Estatísticas de Gols
                        st.markdown(
                            f'<div class="medium-text"><span class="highlight">Média de Gols Marcados HT</span> = {estatisticas["Média Gols Marcados HT"]}</div>',
                            unsafe_allow_html=True)
                        st.markdown(
                            f'<div class="medium-text"><span class="highlight">Média de Gols Sofridos HT</span> = {estatisticas["Média Gols Sofridos HT"]}</div>',
                            unsafe_allow_html=True)
                        st.markdown(
                            f'<div class="medium-text"><span class="highlight">Média HT</span> = {estatisticas["Média HT"]}</div>',
                            unsafe_allow_html=True)
                        st.markdown(
                            f'<div class="medium-text"><span class="highlight">Média de Gols Marcados FT</span> = {estatisticas["Média Gols Marcados FT"]}</div>',
                            unsafe_allow_html=True)
                        st.markdown(
                            f'<div class="medium-text"><span class="highlight">Média de Gols Sofridos FT</span> = {estatisticas["Média Gols Sofridos FT"]}</div>',
                            unsafe_allow_html=True)
                        st.markdown(
                            f'<div class="medium-text"><span class="highlight">Média FT</span> = {estatisticas["Média FT"]}</div>',
                            unsafe_allow_html=True)

                        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

                        # Estatísticas dos Últimos 5 Jogos
                        st.markdown(
                            f'<div class="medium-text"><span class="highlight">Total de Chutes no Gol a favor | Últimos 5 Jogos</span> = {estatisticas["Chutes no Gol (Últimos 5)"]}</div>',
                            unsafe_allow_html=True)
                        st.markdown(
                            f'<div class="medium-text"><span class="highlight">Total de Chutes a favor | Últimos 5 Jogos</span> = {estatisticas["Chutes (Últimos 5)"]}</div>',
                            unsafe_allow_html=True)
                        st.markdown(
                            f'<div class="medium-text"><span class="highlight">Total Escanteios a Favor | Últimos 5 Jogos</span> = {estatisticas["Escanteios a Favor (Últimos 5)"]}</div>',
                            unsafe_allow_html=True)
                        st.markdown(
                            f'<div class="medium-text"><span class="highlight">Total de Escanteios por jogo | Últimos 5 Jogos</span> = {estatisticas["Escanteios Total (Últimos 5)"]}</div>',
                            unsafe_allow_html=True)
                        st.markdown(
                            f'<div class="medium-text"><span class="highlight">Total Cartão Amarelo a Favor | Últimos 5 Jogos</span> = {estatisticas["Cartões Amarelos (Últimos 5)"]}</div>',
                            unsafe_allow_html=True)
                        st.markdown(
                            f'<div class="medium-text"><span class="highlight">Total de Cartão Amarelo por jogo | Últimos 5 Jogos</span> = {estatisticas["Cartões Amarelos (Últimos 5)"]}</div>',
                            unsafe_allow_html=True)
                        st.markdown(
                            f'<div class="medium-text"><span class="highlight">Total de faltas a favor | Últimos 5 Jogos</span> = {estatisticas["Faltas Total (Últimos 5)"]}</div>',
                            unsafe_allow_html=True)
                        st.markdown(
                            f'<div class="medium-text"><span class="highlight">Total de faltas por jogo | Últimos 5 Jogos</span> = {estatisticas["Faltas Total (Últimos 5)"]}</div>',
                            unsafe_allow_html=True)

                        # Análise de sequências e dicas
                        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
                        st.markdown(
                            '<div class="medium-text"><span class="highlight">💡 Análise de Sequências (Últimos 5 Jogos):</span></div>',
                            unsafe_allow_html=True)

                        dicas = analisar_sequencias(todos_jogos, time_nome)
                        for dica in dicas:
                            st.markdown(f'<div class="medium-text">{dica}</div>', unsafe_allow_html=True)

                        # Alertas estatísticos
                        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
                        st.markdown(
                            '<div class="medium-text"><span class="highlight" style="color: #ff4b4b;">🚨 ALERTAS ESTATÍSTICOS (Últimos 5 Jogos):</span></div>',
                            unsafe_allow_html=True)

                        alertas = analisar_sequencias_estatisticas(todos_jogos, time_nome, estatisticas)
                        for alerta in alertas:
                            st.markdown(f'<div class="alert-text">{alerta}</div>', unsafe_allow_html=True)

                        # Download das estatísticas
                        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
                        df_estatisticas = pd.DataFrame([estatisticas])
                        csv = df_estatisticas.to_csv(index=False, sep=';')

                        st.download_button(
                            label=f"📥 Download Estatísticas {time_nome}",
                            data=csv,
                            file_name=f"estatisticas_{time_nome}.csv",
                            mime="text/csv",
                            key=f"download_all_{time_nome}_{codigo_liga}"
                        )
                    else:
                        st.warning(f"Não foi possível carregar estatísticas para {time_nome}")
        else:
            st.warning("⚠️ Nenhum dado disponível para busca de equipes")

    # Abas para cada liga histórica (restantes abas)
    for i, aba in enumerate(abas_disponiveis):
        # Ajuste o índice para começar após as 4 abas principais
        with tabs[i + 4]:  # +4 porque as primeiras 4 abas são Simulador, Relatórios, Times e Buscar Equipe
            df_liga = todas_abas[aba]
            nome_liga = mapeamento_ligas.get(aba, f"{aba} (Liga)")

            st.header(f"📊 {nome_liga} - Dados Históricos")

            # TRADUZIR COLUNAS PARA PORTUGUÊS
            df_liga_traduzido = traduzir_colunas_df(df_liga)

            # Formatar datas para DD/MM/YYYY
            if 'Data' in df_liga_traduzido.columns:
                df_liga_traduzido['Data'] = pd.to_datetime(df_liga_traduzido['Data'], errors='coerce')
                df_liga_traduzido['Data'] = df_liga_traduzido['Data'].dt.strftime('%d/%m/%Y')

            # Exibir dados da liga traduzidos
            st.dataframe(df_liga_traduzido, use_container_width=True, height=400)

            # Estatísticas básicas
            st.subheader("📈 Estatísticas da Liga")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total de Jogos", len(df_liga))

            with col2:
                if 'FTHG' in df_liga.columns and 'FTAG' in df_liga.columns:
                    total_gols = df_liga['FTHG'].sum() + df_liga['FTAG'].sum()
                    st.metric("Total de Gols", total_gols)
                else:
                    st.metric("Total de Gols", "N/D")

            with col3:
                if 'FTHG' in df_liga.columns and 'FTAG' in df_liga.columns and len(df_liga) > 0:
                    media_gols = round(total_gols / len(df_liga), 2)
                    st.metric("Média de Gols", media_gols)
                else:
                    st.metric("Média de Gols", "N/D")

            with col4:
                if 'FTR' in df_liga.columns and len(df_liga) > 0:
                    vitorias_casa = len(df_liga[df_liga['FTR'] == 'H'])
                    percent_casa = round((vitorias_casa / len(df_liga)) * 100, 1)
                    st.metric("Vitórias em Casa", f"{percent_casa}%")
                else:
                    st.metric("Vitórias em Casa", "N/D")

            # Download dos dados traduzidos
            st.subheader("💾 Exportar Dados")
            csv = df_liga_traduzido.to_csv(index=False, sep=';')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"dados_{aba}_traduzidos.csv",
                mime="text/csv",
                key=f"download_{aba}"  # Chave única para cada botão
            )

else:
    st.error("❌ Não foi possível carregar os dados")

# Rodapé
st.markdown("---")
st.caption("Dados obtidos de football-data.co.uk | Simulador desenvolvido com Streamlit")