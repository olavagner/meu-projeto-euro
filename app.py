# URLs dos arquivos
url_excel = "https://www.football-data.co.uk/mmz4281/2526/all-euro-data-2025-2026.xlsx"
url_proximos_jogos = "https://www.football-data.co.uk/fixtures.xlsx"

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import requests
from datetime import datetime, timedelta
import time

# Configuração da página
st.set_page_config(page_title="FutAlgorithm", page_icon="⚽", layout="wide")

# Configurações de estilo - TEMA ESCURO
st.markdown("""
    <style>
    /* TEMA ESCURO COMPLETO */
    .main {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    .stApp {
        background-color: #0E1117;
    }
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #64B5F6;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .positive-value { color: #4CAF50; font-weight: bold; }
    .negative-value { color: #F44336; font-weight: bold; }
    .neutral-value { color: #FF9800; font-weight: bold; }
    .stDataFrame { 
        font-size: 0.9rem;
        background-color: #1E1E1E;
        color: #FFFFFF;
    }

    /* CARDS DAS DICAS - TEMA ESCURO */
    .dica-item {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #1E88E5;
        color: #FFFFFF;
        font-family: 'Arial', sans-serif;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease;
    }
    .dica-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.4);
    }
    .dica-header {
        font-weight: bold;
        color: #64B5F6;
        margin-bottom: 8px;
        font-size: 1.1rem;
        border-bottom: 1px solid #333;
        padding-bottom: 5px;
    }
    .dica-content {
        color: #E0E0E0;
        font-size: 1rem;
        line-height: 1.4;
    }

    /* BOTÕES E FILTROS - TEMA ESCURO */
    .stSelectbox > div > div {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    .stSelectbox label {
        color: #64B5F6 !important;
        font-weight: bold;
    }

    /* METRIC CARDS - TEMA ESCURO */
    .stMetric {
        background-color: #1E1E1E;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 10px;
    }
    .css-1r6slb0 {
        color: #64B5F6 !important;
    }
    .css-1fv8s86 {
        color: #FFFFFF !important;
    }

    /* TABELA - TEMA ESCURO */
    .dataframe {
        background-color: #1E1E1E !important;
        color: #FFFFFF !important;
    }
    .dataframe th {
        background-color: #2D2D2D !important;
        color: #64B5F6 !important;
    }
    .dataframe td {
        background-color: #1E1E1E !important;
        color: #FFFFFF !important;
        border: 1px solid #333 !important;
    }

    /* ABAS - TEMA ESCURO */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1E1E1E;
        color: #FFFFFF;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        border: 1px solid #333;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E88E5 !important;
        color: #FFFFFF !important;
        font-weight: bold;
    }

    /* SCROLLBAR PERSONALIZADA */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #1E1E1E;
    }
    ::-webkit-scrollbar-thumb {
        background: #1E88E5;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #1565C0;
    }

    /* ESTILO PARA CITAÇÃO */
    .citacao {
        font-size: 0.9rem;
        font-style: italic;
        color: #888;
        text-align: center;
        margin-top: -10px;
        margin-bottom: 20px;
    }

    /* ESTILO PARA FILTROS */
    .filtro-section {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 1px solid #333;
    }
    .filtro-header {
        color: #64B5F6;
        font-weight: bold;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)


# Remover cache para garantir dados sempre atualizados
@st.cache_data(ttl=3600)
def carregar_dados_excel(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        excel_file = BytesIO(response.content)
        todas_abas = pd.read_excel(excel_file, sheet_name=None)
        abas_disponiveis = list(todas_abas.keys())
        return todas_abas, abas_disponiveis
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {e}")
        return None, None


@st.cache_data(ttl=1800)
def carregar_proximos_jogos(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        excel_file = BytesIO(response.content)
        df_jogos = pd.read_excel(excel_file)
        return df_jogos
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados do simulador: {e}")
        return None


# Carregar dados
todas_abas, abas_disponiveis = carregar_dados_excel(url_excel)
df_proximos_jogos = carregar_proximos_jogos(url_proximos_jogos)

# Mapeamento de ligas
mapeamento_ligas = {
    'E0': 'Premier League', 'E1': 'Championship', 'E2': 'League One', 'E3': 'League Two',
    'SC0': 'Premiership', 'SC1': 'Championship', 'SC2': 'League One', 'SC3': 'League Two',
    'D1': 'Bundesliga', 'D2': '2. Bundesliga', 'I1': 'Serie A', 'I2': 'Serie B',
    'SP1': 'La Liga', 'SP2': 'La Liga 2', 'F1': 'Ligue 1', 'F2': 'Ligue 2',
    'N1': 'Eredivisie', 'B1': 'Jupiler Pro League', 'P1': 'Primeira Liga',
    'T1': 'Super Lig', 'G1': 'Super League'
}


# FUNÇÕES DO ALGORITMO
def obter_ultimos_jogos_por_cenario(df_liga, time, cenario, num_jogos=10):
    """Obtém os últimos N jogos de um time em um cenário específico"""
    if cenario == 'mandante':
        jogos = df_liga[df_liga['HomeTeam'] == time].tail(num_jogos)
    elif cenario == 'visitante':
        jogos = df_liga[df_liga['AwayTeam'] == time].tail(num_jogos)
    else:  # geral
        jogos_casa = df_liga[df_liga['HomeTeam'] == time].tail(num_jogos)
        jogos_fora = df_liga[df_liga['AwayTeam'] == time].tail(num_jogos)
        jogos = pd.concat([jogos_casa, jogos_fora]).tail(num_jogos)
    return jogos


def calcular_estatisticas_completas(jogos, time, cenario):
    """Calcula estatísticas COMPLETAS para um cenário específico"""
    if jogos.empty:
        return None

    stats = {
        'jogos_analisados': len(jogos),
        'vitorias': 0, 'empates': 0, 'derrotas': 0,
        'gols_marcados_ft': 0, 'gols_sofridos_ft': 0,
        'gols_marcados_ht': 0, 'gols_sofridos_ht': 0,
        'over_05_ht': 0, 'over_05_ft': 0, 'over_15_ft': 0, 'over_25_ft': 0, 'over_35_ft': 0, 'btts': 0,
        'chutes_total': 0, 'chutes_gol': 0,
        'escanteios': 0, 'cartoes_amarelos': 0, 'faltas': 0, 'impedimentos': 0
    }

    for _, jogo in jogos.iterrows():
        is_mandante = jogo['HomeTeam'] == time

        if is_mandante:
            gols_feitos_ft = jogo.get('FTHG', 0)
            gols_sofridos_ft = jogo.get('FTAG', 0)
            gols_feitos_ht = jogo.get('HTHG', 0)
            gols_sofridos_ht = jogo.get('HTAG', 0)
            resultado = jogo.get('FTR', '')

            stats['chutes_total'] += jogo.get('HS', 0)
            stats['chutes_gol'] += jogo.get('HST', 0)
            stats['escanteios'] += jogo.get('HC', 0)
            stats['cartoes_amarelos'] += jogo.get('HY', 0)
            stats['faltas'] += jogo.get('HF', 0)
            stats['impedimentos'] += jogo.get('HI', 0) if 'HI' in jogo else 0
        else:
            gols_feitos_ft = jogo.get('FTAG', 0)
            gols_sofridos_ft = jogo.get('FTHG', 0)
            gols_feitos_ht = jogo.get('HTAG', 0)
            gols_sofridos_ht = jogo.get('HTHG', 0)
            resultado = 'A' if jogo.get('FTR', '') == 'H' else ('H' if jogo.get('FTR', '') == 'A' else 'D')

            stats['chutes_total'] += jogo.get('AS', 0)
            stats['chutes_gol'] += jogo.get('AST', 0)
            stats['escanteios'] += jogo.get('AC', 0)
            stats['cartoes_amarelos'] += jogo.get('AY', 0)
            stats['faltas'] += jogo.get('AF', 0)
            stats['impedimentos'] += jogo.get('AI', 0) if 'AI' in jogo else 0

        # Estatísticas básicas
        stats['gols_marcados_ft'] += gols_feitos_ft
        stats['gols_sofridos_ft'] += gols_sofridos_ft
        stats['gols_marcados_ht'] += gols_feitos_ht
        stats['gols_sofridos_ht'] += gols_sofridos_ht

        if resultado == 'H' and is_mandante:
            stats['vitorias'] += 1
        elif resultado == 'A' and not is_mandante:
            stats['vitorias'] += 1
        elif resultado == 'D':
            stats['empates'] += 1
        else:
            stats['derrotas'] += 1

        # Estatísticas de mercado
        gols_ht = gols_feitos_ht + gols_sofridos_ht
        gols_ft = gols_feitos_ft + gols_sofridos_ft

        if gols_ht > 0.5: stats['over_05_ht'] += 1
        if gols_ft > 0.5: stats['over_05_ft'] += 1
        if gols_ft > 1.5: stats['over_15_ft'] += 1
        if gols_ft > 2.5: stats['over_25_ft'] += 1
        if gols_ft > 3.5: stats['over_35_ft'] += 1
        if gols_feitos_ft > 0 and gols_sofridos_ft > 0: stats['btts'] += 1

    # Calcular médias
    if stats['jogos_analisados'] > 0:
        stats['media_gols_marcados_ft'] = stats['gols_marcados_ft'] / stats['jogos_analisados']
        stats['media_gols_sofridos_ft'] = stats['gols_sofridos_ft'] / stats['jogos_analisados']
        stats['media_gols_marcados_ht'] = stats['gols_marcados_ht'] / stats['jogos_analisados']
        stats['media_gols_sofridos_ht'] = stats['gols_sofridos_ht'] / stats['jogos_analisados']
        stats['media_gols_total_ft'] = stats['media_gols_marcados_ft'] + stats['media_gols_sofridos_ft']
        stats['media_gols_total_ht'] = stats['media_gols_marcados_ht'] + stats['media_gols_sofridos_ht']

        stats['media_chutes_total'] = stats['chutes_total'] / stats['jogos_analisados']
        stats['media_chutes_gol'] = stats['chutes_gol'] / stats['jogos_analisados']
        stats['media_escanteios'] = stats['escanteios'] / stats['jogos_analisados']
        stats['media_cartoes_amarelos'] = stats['cartoes_amarelos'] / stats['jogos_analisados']
        stats['media_faltas'] = stats['faltas'] / stats['jogos_analisados']
        stats['media_impedimentos'] = stats['impedimentos'] / stats['jogos_analisados'] if stats[
                                                                                               'impedimentos'] > 0 else 0

        for key in ['over_05_ht', 'over_05_ft', 'over_15_ft', 'over_25_ft', 'over_35_ft', 'btts']:
            stats[key] = (stats[key] / stats['jogos_analisados']) * 100

    return stats


def calcular_probabilidades_avancadas(df_liga, mandante, visitante):
    """Calcula probabilidades AVANÇADAS para o confronto"""
    cenarios = ['mandante', 'visitante', 'geral']
    pesos = {'mandante': 0.4, 'visitante': 0.4, 'geral': 0.2}

    resultados = {}

    for cenario in cenarios:
        # Estatísticas do mandante
        jogos_mandante = obter_ultimos_jogos_por_cenario(df_liga, mandante, cenario)
        stats_mandante = calcular_estatisticas_completas(jogos_mandante, mandante, cenario)

        # Estatísticas do visitante
        jogos_visitante = obter_ultimos_jogos_por_cenario(df_liga, visitante, cenario)
        stats_visitante = calcular_estatisticas_completas(jogos_visitante, visitante, cenario)

        if stats_mandante and stats_visitante:
            # Calcular probabilidades para este cenário
            prob_cenario = {
                # Resultados
                'casa_vence': (stats_mandante.get('vitorias', 0) / stats_mandante['jogos_analisados'] * 100 * 0.6 +
                               stats_visitante.get('derrotas', 0) / stats_visitante['jogos_analisados'] * 100 * 0.4),
                'empate': ((stats_mandante.get('empates', 0) / stats_mandante['jogos_analisados'] * 100 +
                            stats_visitante.get('empates', 0) / stats_visitante['jogos_analisados'] * 100) / 2),

                # Gols
                'gols_ht_total': (stats_mandante.get('media_gols_total_ht', 0) + stats_visitante.get(
                    'media_gols_total_ht', 0)) / 2,
                'gols_ft_total': (stats_mandante.get('media_gols_total_ft', 0) + stats_visitante.get(
                    'media_gols_total_ft', 0)) / 2,
                'gols_casa_esperados': stats_mandante.get('media_gols_marcados_ft', 0) * 0.7 + stats_visitante.get(
                    'media_gols_sofridos_ft', 0) * 0.3,
                'gols_fora_esperados': stats_visitante.get('media_gols_marcados_ft', 0) * 0.7 + stats_mandante.get(
                    'media_gols_sofridos_ft', 0) * 0.3,

                # Mercados
                'over_05_ht': (stats_mandante.get('over_05_ht', 0) + stats_visitante.get('over_05_ht', 0)) / 2,
                'over_05_ft': (stats_mandante.get('over_05_ft', 0) + stats_visitante.get('over_05_ft', 0)) / 2,
                'over_15_ft': (stats_mandante.get('over_15_ft', 0) + stats_visitante.get('over_15_ft', 0)) / 2,
                'over_25_ft': (stats_mandante.get('over_25_ft', 0) + stats_visitante.get('over_25_ft', 0)) / 2,
                'over_35_ft': (stats_mandante.get('over_35_ft', 0) + stats_visitante.get('over_35_ft', 0)) / 2,
                'btts': (stats_mandante.get('btts', 0) + stats_visitante.get('btts', 0)) / 2,

                # Estatísticas avançadas - Por equipe
                'escanteios_casa_esperados': stats_mandante.get('media_escanteios', 0),
                'escanteios_fora_esperados': stats_visitante.get('media_escanteios', 0),
                'escanteios_total_ft': (
                        stats_mandante.get('media_escanteios', 0) + stats_visitante.get('media_escanteios', 0)),

                'finalizacoes_casa_esperadas': stats_mandante.get('media_chutes_total', 0),
                'finalizacoes_fora_esperadas': stats_visitante.get('media_chutes_total', 0),
                'finalizacoes_total_ft': (
                        stats_mandante.get('media_chutes_total', 0) + stats_visitante.get('media_chutes_total', 0)),

                'chutes_gol_casa_esperados': stats_mandante.get('media_chutes_gol', 0),
                'chutes_gol_fora_esperados': stats_visitante.get('media_chutes_gol', 0),
                'chutes_gol_total_ft': (
                        stats_mandante.get('media_chutes_gol', 0) + stats_visitante.get('media_chutes_gol', 0)),

                'cartoes_casa_esperados': stats_mandante.get('media_cartoes_amarelos', 0),
                'cartoes_fora_esperados': stats_visitante.get('media_cartoes_amarelos', 0),
                'cartoes_total_ft': (stats_mandante.get('media_cartoes_amarelos', 0) + stats_visitante.get(
                    'media_cartoes_amarelos', 0)),

                'impedimentos_total_ft': (
                        stats_mandante.get('media_impedimentos', 0) + stats_visitante.get('media_impedimentos', 0))
            }

            resultados[cenario] = prob_cenario

    # Combinar resultados com pesos
    probabilidades_finais = {}
    for metric in resultados['mandante'].keys():
        total = 0
        for cenario in cenarios:
            total += resultados[cenario][metric] * pesos[cenario]
        probabilidades_finais[metric] = min(max(total, 0), 100) if '%' in metric or metric in ['over_05_ht',
                                                                                               'over_05_ft',
                                                                                               'over_15_ft',
                                                                                               'over_25_ft',
                                                                                               'over_35_ft',
                                                                                               'btts'] else round(total,
                                                                                                                  2)

    # Ajustar probabilidades de resultado
    total_resultados = probabilidades_finais['casa_vence'] + probabilidades_finais['empate'] + (
            100 - probabilidades_finais['casa_vence'] - probabilidades_finais['empate'])
    probabilidades_finais['casa_vence'] = (probabilidades_finais['casa_vence'] / total_resultados) * 100
    probabilidades_finais['empate'] = (probabilidades_finais['empate'] / total_resultados) * 100
    probabilidades_finais['fora_vence'] = 100 - probabilidades_finais['casa_vence'] - probabilidades_finais['empate']

    return probabilidades_finais


def processar_todos_jogos_completos(todas_abas, df_proximos_jogos):
    """Processa todos os jogos com estatísticas COMPLETAS"""
    resultados = []

    if df_proximos_jogos is not None and not df_proximos_jogos.empty:
        for _, jogo in df_proximos_jogos.iterrows():
            try:
                liga = jogo.get('Div', '')
                mandante = jogo.get('HomeTeam', '')
                visitante = jogo.get('AwayTeam', '')
                data = jogo.get('Date', '')

                if liga in todas_abas and mandante and visitante:
                    df_liga = todas_abas[liga]
                    prob = calcular_probabilidades_avancadas(df_liga, mandante, visitante)

                    resultados.append({
                        # Informações básicas
                        'Data': data.strftime('%d/%m/%Y') if hasattr(data, 'strftime') else str(data),
                        'Liga': mapeamento_ligas.get(liga, liga),
                        'Casa': mandante,
                        'Fora': visitante,

                        # Resultados
                        'Casa Vence': f"{prob['casa_vence']:.1f}%",
                        'Empate': f"{prob['empate']:.1f}%",
                        'Fora Vence': f"{prob['fora_vence']:.1f}%",

                        # Gols
                        'Gols HT': f"{prob['gols_ht_total']:.2f}",
                        'Gols FT': f"{prob['gols_ft_total']:.2f}",

                        # Mercados
                        'Over 0.5 HT': f"{prob['over_05_ht']:.1f}%",
                        'Over 0.5 FT': f"{prob['over_05_ft']:.1f}%",
                        'Over 1.5 FT': f"{prob['over_15_ft']:.1f}%",
                        'Over 2.5 FT': f"{prob['over_25_ft']:.1f}%",
                        'Over 3.5 FT': f"{prob['over_35_ft']:.1f}%",
                        'BTTS FT': f"{prob['btts']:.1f}%",

                        # Média de gols esperada - Por equipe
                        'Gols Casa Esp': f"{prob['gols_casa_esperados']:.2f}",
                        'Gols Fora Esp': f"{prob['gols_fora_esperados']:.2f}",

                        # Escanteios
                        'Escanteios Casa Esp': f"{prob['escanteios_casa_esperados']:.1f}",
                        'Escanteios Fora Esp': f"{prob['escanteios_fora_esperados']:.1f}",
                        'Escanteios FT': f"{prob['escanteios_total_ft']:.1f}",

                        # Finalizações
                        'Finalizações Casa Esp': f"{prob['finalizacoes_casa_esperadas']:.1f}",
                        'Finalizações Fora Esp': f"{prob['finalizacoes_fora_esperadas']:.1f}",
                        'Finalizações FT': f"{prob['finalizacoes_total_ft']:.1f}",

                        # Chutes ao gol
                        'Chutes Gol Casa Esp': f"{prob['chutes_gol_casa_esperados']:.1f}",
                        'Chutes Gol Fora Esp': f"{prob['chutes_gol_fora_esperados']:.1f}",
                        'Chutes Gol FT': f"{prob['chutes_gol_total_ft']:.1f}",

                        # Cartões amarelos
                        'Cartões Casa Esp': f"{prob['cartoes_casa_esperados']:.1f}",
                        'Cartões Fora Esp': f"{prob['cartoes_fora_esperados']:.1f}",
                        'Cartões FT': f"{prob['cartoes_total_ft']:.1f}",

                        # Impedimentos
                        'Impedimentos FT': f"{prob['impedimentos_total_ft']:.1f}" if prob[
                                                                                         'impedimentos_total_ft'] > 0 else "N/D"
                    })
            except Exception as e:
                continue

    return pd.DataFrame(resultados)


# FUNÇÕES PARA DICAS INTELIGENTES MELHORADAS
def gerar_dicas_inteligentes(df_proximos_jogos, todas_abas):
    """Gera dicas inteligentes baseadas nos últimos 5 jogos"""

    dicas_todas = []

    if df_proximos_jogos is None or todas_abas is None:
        return []

    for _, jogo in df_proximos_jogos.iterrows():
        try:
            liga = jogo.get('Div', '')
            mandante = jogo.get('HomeTeam', '')
            visitante = jogo.get('AwayTeam', '')

            if liga in todas_abas and mandante and visitante:
                df_liga = todas_abas[liga]

                # Analisar mandante
                dicas_mandante = analisar_equipe_dicas(df_liga, mandante)
                # Analisar visitante
                dicas_visitante = analisar_equipe_dicas(df_liga, visitante)

                # Combinar dicas
                dicas_jogo = dicas_mandante + dicas_visitante

                for dica in dicas_jogo:
                    dicas_todas.append({
                        'Jogo': f"{mandante} x {visitante}",
                        'Liga': mapeamento_ligas.get(liga, liga),
                        'Dica': dica
                    })

        except Exception as e:
            continue

    return dicas_todas


def analisar_equipe_dicas(df_liga, time):
    """Analisa uma equipe específica e retorna dicas inteligentes"""

    dicas = []

    # Obter últimos 5 jogos
    ultimos_5 = obter_ultimos_jogos_por_cenario(df_liga, time, 'geral', 5)

    if ultimos_5.empty or len(ultimos_5) < 5:
        return dicas

    # Dicas de Gols HT
    dicas.extend(analisar_gols_ht_melhorado(ultimos_5, time))

    # Dicas de Gols FT
    dicas.extend(analisar_gols_ft_melhorado(ultimos_5, time))

    # Dicas de BTTS
    dicas.extend(analisar_btts_melhorado(ultimos_5, time))

    # Dicas de Escanteios
    dicas.extend(analisar_escanteios_melhorado(ultimos_5, time))

    # Dicas de Cartões
    dicas.extend(analisar_cartoes_melhorado(ultimos_5, time))

    # Dicas de Finalizações
    dicas.extend(analisar_finalizacoes_melhorado(ultimos_5, time))

    # Dicas de Chutes ao Gol
    dicas.extend(analisar_chutes_gol_melhorado(ultimos_5, time))

    # Dicas de Impedimentos
    dicas.extend(analisar_impedimentos_melhorado(ultimos_5, time))

    return dicas


def analisar_gols_ht_melhorado(jogos, time):
    """Analisa estatísticas de gols no primeiro tempo - formato melhorado"""
    dicas = []

    jogos_com_gol_ht = 0
    valores_gols_ht = []

    for _, jogo in jogos.iterrows():
        if jogo['HomeTeam'] == time:
            gols_time_ht = jogo.get('HTHG', 0)
            gols_adversario_ht = jogo.get('HTAG', 0)
        else:
            gols_time_ht = jogo.get('HTAG', 0)
            gols_adversario_ht = jogo.get('HTHG', 0)

        total_gols_ht = gols_time_ht + gols_adversario_ht
        valores_gols_ht.append(total_gols_ht)

        if total_gols_ht > 0.5:
            jogos_com_gol_ht += 1

    # Dica: Sequência de gols HT
    if jogos_com_gol_ht >= 4:
        dicas.append(f"O {time} teve {jogos_com_gol_ht} dos seus últimos 5 jogos com 0.5 Gols HT.")

    return dicas


def analisar_gols_ft_melhorado(jogos, time):
    """Analisa estatísticas de gols no tempo completo - formato melhorado"""
    dicas = []

    jogos_over_15 = 0
    jogos_over_25 = 0
    jogos_over_35 = 0

    for _, jogo in jogos.iterrows():
        if jogo['HomeTeam'] == time:
            gols_time_ft = jogo.get('FTHG', 0)
            gols_adversario_ft = jogo.get('FTAG', 0)
        else:
            gols_time_ft = jogo.get('FTAG', 0)
            gols_adversario_ft = jogo.get('FTHG', 0)

        total_gols_ft = gols_time_ft + gols_adversario_ft

        if total_gols_ft > 1.5:
            jogos_over_15 += 1
        if total_gols_ft > 2.5:
            jogos_over_25 += 1
        if total_gols_ft > 3.5:
            jogos_over_35 += 1

    # Dicas Over
    if jogos_over_15 >= 4:
        dicas.append(f"O {time} teve {jogos_over_15} dos seus últimos 5 jogos com 1.5 Gols FT.")
    if jogos_over_25 >= 3:
        dicas.append(f"O {time} teve {jogos_over_25} dos seus últimos 5 jogos com 2.5 Gols FT.")
    if jogos_over_35 >= 2:
        dicas.append(f"O {time} teve {jogos_over_35} dos seus últimos 5 jogos com 3.5 Gols FT.")

    return dicas


def analisar_btts_melhorado(jogos, time):
    """Analisa estatísticas de BTTS - formato melhorado"""
    dicas = []

    jogos_btts = 0

    for _, jogo in jogos.iterrows():
        if jogo['HomeTeam'] == time:
            gols_time = jogo.get('FTHG', 0)
            gols_adversario = jogo.get('FTAG', 0)
        else:
            gols_time = jogo.get('FTAG', 0)
            gols_adversario = jogo.get('FTHG', 0)

        if gols_time > 0 and gols_adversario > 0:
            jogos_btts += 1

    # Dica BTTS
    if jogos_btts >= 3:
        dicas.append(f"O {time} teve {jogos_btts} dos seus últimos 5 jogos com BTTS FT.")

    return dicas


def analisar_escanteios_melhorado(jogos, time):
    """Analisa estatísticas de escanteios - formato melhorado"""
    dicas = []

    escanteios_jogos = []
    jogos_10_escanteios = 0

    for _, jogo in jogos.iterrows():
        if jogo['HomeTeam'] == time:
            escanteios_time = jogo.get('HC', 0)
            escanteios_adversario = jogo.get('AC', 0)
        else:
            escanteios_time = jogo.get('AC', 0)
            escanteios_adversario = jogo.get('HC', 0)

        total_escanteios = escanteios_time + escanteios_adversario
        escanteios_jogos.append(total_escanteios)

        if total_escanteios >= 10:
            jogos_10_escanteios += 1

    # Dica escanteios
    if jogos_10_escanteios >= 3:
        dicas.append(f"O {time} teve {jogos_10_escanteios} dos seus últimos 5 jogos com >= 10 Escanteios FT.")

    # Dica média alta
    if sum(escanteios_jogos) / 5 >= 11:
        valores_str = "-".join(map(str, escanteios_jogos))
        dicas.append(
            f"O {time} teve {sum(escanteios_jogos) / 5:.1f}+ Escanteios FT em média nos últimos 5 jogos. ({valores_str})")

    return dicas


def analisar_cartoes_melhorado(jogos, time):
    """Analisa estatísticas de cartões - formato melhorado"""
    dicas = []

    cartoes_jogos = []
    jogos_25_cartoes = 0

    for _, jogo in jogos.iterrows():
        if jogo['HomeTeam'] == time:
            cartoes_time = jogo.get('HY', 0)
            cartoes_adversario = jogo.get('AY', 0)
        else:
            cartoes_time = jogo.get('AY', 0)
            cartoes_adversario = jogo.get('HY', 0)

        total_cartoes = cartoes_time + cartoes_adversario
        cartoes_jogos.append(total_cartoes)

        if total_cartoes >= 2.5:
            jogos_25_cartoes += 1

    # Dica cartões
    if jogos_25_cartoes >= 3:
        dicas.append(f"O {time} teve {jogos_25_cartoes} dos seus últimos 5 jogos com >= 2.5 Cartões Amarelos FT.")

    return dicas


def analisar_finalizacoes_melhorado(jogos, time):
    """Analisa estatísticas de finalizações - formato melhorado"""
    dicas = []

    finalizacoes_jogos = []

    for _, jogo in jogos.iterrows():
        if jogo['HomeTeam'] == time:
            finalizacoes = jogo.get('HS', 0)
        else:
            finalizacoes = jogo.get('AS', 0)

        finalizacoes_jogos.append(finalizacoes)

    # Dica finalizações altas
    if sum(finalizacoes_jogos) / 5 >= 12:
        valores_str = "-".join(map(str, finalizacoes_jogos))
        dicas.append(f"O {time} teve 12+ Finalizações na partida nos seus últimos 5 jogos. ({valores_str})")

    return dicas


def analisar_chutes_gol_melhorado(jogos, time):
    """Analisa estatísticas de chutes ao gol - formato melhorado"""
    dicas = []

    chutes_gol_jogos = []

    for _, jogo in jogos.iterrows():
        if jogo['HomeTeam'] == time:
            chutes_gol = jogo.get('HST', 0)
        else:
            chutes_gol = jogo.get('AST', 0)

        chutes_gol_jogos.append(chutes_gol)

    # Dica chutes ao gol altos
    if sum(chutes_gol_jogos) / 5 >= 5:
        valores_str = "-".join(map(str, chutes_gol_jogos))
        dicas.append(f"O {time} teve 5+ Chutes ao Gol na partida nos seus últimos 5 jogos. ({valores_str})")

    return dicas


def analisar_impedimentos_melhorado(jogos, time):
    """Analisa estatísticas de impedimentos - formato melhorado"""
    dicas = []

    impedimentos_jogos = []

    for _, jogo in jogos.iterrows():
        if jogo['HomeTeam'] == time:
            if 'HI' in jogo:
                impedimentos = jogo.get('HI', 0)
                impedimentos_jogos.append(impedimentos)
        else:
            if 'AI' in jogo:
                impedimentos = jogo.get('AI', 0)
                impedimentos_jogos.append(impedimentos)

    # Só gerar dica if tiver dados de impedimentos
    if len(impedimentos_jogos) >= 3:
        if sum(impedimentos_jogos) / len(impedimentos_jogos) >= 3:
            valores_str = "-".join(map(str, impedimentos_jogos))
            dicas.append(f"O {time} teve 3+ Impedimentos FT em média nos últimos jogos. ({valores_str})")

    return dicas


# Interface principal
st.markdown('<h1 class="main-header">💀 FutAlgorithm - Software Esportivo</h1>', unsafe_allow_html=True)
st.markdown('<p class="citacao">⚰️ In Memoriam – Denise Bet365..</p>', unsafe_allow_html=True)
st.markdown("---")

# Criar abas
tab_titles = ["⚽️ Simulador", "⚡️ Dicas Inteligentes"]
tabs = st.tabs(tab_titles)

# Aba 1: Simulador
with tabs[0]:
    st.header("⚡️ Programador | FutAlgorithm ®️")

    if todas_abas and df_proximos_jogos is not None:
        with st.spinner('🔍 Calculando probabilidades COMPLETAS...'):
            df_resultados = processar_todos_jogos_completos(todas_abas, df_proximos_jogos)

        if not df_resultados.empty:
            st.success(f"⭐️ Busca Concluída! {len(df_resultados)} Jogos Encontrados")

            # REMOVIDOS TODOS OS FILTROS - AGORA MOSTRA TODOS OS JOGOS SEM FILTRAGEM
            df_filtrado = df_resultados.copy()

            # Exibir estatísticas
            st.info(f"🔷 Exibindo todos os {len(df_filtrado)} Jogos Disponíveis")

            # Exibir tabela completa com TODAS as colunas
            st.dataframe(df_filtrado, use_container_width=True, height=600)

            # Botão de download
            csv = df_filtrado.to_csv(index=False, sep=';')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="futalgorithm_previsoes.csv",
                mime="text/csv"
            )

        else:
            st.warning("⚠️ Nenhum jogo pôde ser processado. Verifique os dados.")
    else:
        st.error("❌ Dados não disponíveis para análise")

# Aba 2: Dicas Inteligentes
with tabs[1]:
    st.header("💡 Dicas Inteligentes - Análise por Partida")

    if todas_abas and df_proximos_jogos is not None:
        with st.spinner('🔍 Analisando estatísticas dos últimos 5 jogos...'):
            dicas = gerar_dicas_inteligentes(df_proximos_jogos, todas_abas)

        if dicas:
            st.success(f"✅ {len(dicas)} dicas inteligentes encontradas!")

            # Converter dicas para DataFrame para facilitar filtros
            df_dicas = pd.DataFrame(dicas)

            # 🔥 CORREÇÃO: PEGAR DATAS REAIS DOS JOGOS
            # Criar mapeamento de jogos para datas
            mapa_datas = {}
            for _, jogo in df_proximos_jogos.iterrows():
                mandante = jogo.get('HomeTeam', '')
                visitante = jogo.get('AwayTeam', '')
                data = jogo.get('Date', '')

                if mandante and visitante and not pd.isna(data):
                    chave_jogo = f"{mandante} x {visitante}"
                    # Formatando a data corretamente
                    if hasattr(data, 'strftime'):
                        data_formatada = data.strftime('%d/%m/%Y')
                    else:
                        try:
                            data_formatada = pd.to_datetime(data).strftime('%d/%m/%Y')
                        except:
                            data_formatada = str(data)
                    mapa_datas[chave_jogo] = data_formatada

            # Adicionar coluna de data REAL aos dados
            df_dicas['Data'] = df_dicas['Jogo'].map(mapa_datas)

            # Preencher datas faltantes com "Data não disponível"
            df_dicas['Data'].fillna('Data não disponível', inplace=True)

            # Extrair times do jogo
            df_dicas['Time_Casa'] = df_dicas['Jogo'].apply(lambda x: x.split(' x ')[0] if ' x ' in x else '')
            df_dicas['Time_Fora'] = df_dicas['Jogo'].apply(lambda x: x.split(' x ')[1] if ' x ' in x else '')

            # 🔍 CAIXAS DE PESQUISA NA PARTE SUPERIOR
            st.subheader("🔍 Filtros de Pesquisa")

            col1, col2, col3 = st.columns([2, 2, 1])

            with col1:
                # Filtro por data - TODAS AS DATAS DISPONÍVEIS
                datas_unicas = sorted([d for d in df_dicas['Data'].unique() if d != 'Data não disponível'])
                if datas_unicas:
                    data_filtro = st.selectbox(
                        "📅 Filtrar por Data:",
                        options=["Todas as datas"] + datas_unicas,
                        help="Selecione uma data específica"
                    )
                else:
                    data_filtro = "Todas as datas"
                    st.selectbox("📅 Filtrar por Data:", ["Todas as datas"], disabled=True)

            with col2:
                # Filtro por equipe - TODAS AS EQUIPES DISPONÍVEIS
                todas_equipes = sorted(list(set(df_dicas['Time_Casa'].unique()) | set(df_dicas['Time_Fora'].unique())))
                todas_equipes = [e for e in todas_equipes if e and e != '']  # Remover valores vazios

                if todas_equipes:
                    equipe_filtro = st.selectbox(
                        "⚽ Filtrar por Equipe:",
                        options=["Todas as equipes"] + todas_equipes,
                        help="Selecione uma equipe específica"
                    )
                else:
                    equipe_filtro = "Todas as equipes"
                    st.selectbox("⚽ Filtrar por Equipe:", ["Todas as equipes"], disabled=True)

            with col3:
                # Filtro por liga - TODAS AS LIGAS DISPONÍVEIS
                ligas_unicas = sorted([l for l in df_dicas['Liga'].unique() if l and l != ''])  # Remover valores vazios

                if ligas_unicas:
                    liga_filtro = st.selectbox(
                        "🏆 Filtrar por Liga:",
                        options=["Todas as ligas"] + ligas_unicas,
                        help="Selecione uma liga específica"
                    )
                else:
                    liga_filtro = "Todas as ligas"
                    st.selectbox("🏆 Filtrar por Liga:", ["Todas as ligas"], disabled=True)

            # Aplicar filtros
            dicas_filtradas = df_dicas.copy()

            if data_filtro != "Todas as datas":
                dicas_filtradas = dicas_filtradas[dicas_filtradas['Data'] == data_filtro]

            if equipe_filtro != "Todas as equipes":
                dicas_filtradas = dicas_filtradas[
                    (dicas_filtradas['Time_Casa'] == equipe_filtro) |
                    (dicas_filtradas['Time_Fora'] == equipe_filtro)
                    ]

            if liga_filtro != "Todas as ligas":
                dicas_filtradas = dicas_filtradas[dicas_filtradas['Liga'] == liga_filtro]

            # Converter de volta para lista de dicionários
            dicas_filtradas_list = dicas_filtradas.to_dict('records')

            # Exibir estatísticas dos filtros
            st.info(f"🔷 Mostrando {len(dicas_filtradas_list)} de {len(dicas)} dicas após filtros")

            # 📊 Mostrar contagem de opções disponíveis
            col_info1, col_info2, col_info3 = st.columns(3)
            with col_info1:
                st.caption(f"📅 {len(datas_unicas)} datas disponíveis")
            with col_info2:
                st.caption(f"⚽ {len(todas_equipes)} equipes disponíveis")
            with col_info3:
                st.caption(f"🏆 {len(ligas_unicas)} ligas disponíveis")

            # Exibir dicas filtradas
            st.subheader(f"🎯 Dicas Filtradas")

            if dicas_filtradas_list:
                for dica in dicas_filtradas_list:
                    st.markdown(f"""
                    <div class="dica-item">
                        <div class="dica-header">{dica['Jogo']} - {dica['Liga']} - {dica['Data']}</div>
                        <div class="dica-content">{dica['Dica']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ Nenhuma dica encontrada com os filtros aplicados.")
                st.info("💡 Tente relaxar os filtros para ver mais dicas.")

            # Estatísticas das dicas
            st.subheader("📈 Estatísticas das Dicas")
            col1, col2, col3 = st.columns(3)

            total_dicas_filtradas = len(dicas_filtradas_list)
            total_dicas_geral = len(dicas)

            col1.metric("Dicas Filtradas", total_dicas_filtradas)
            col2.metric("Total de Dicas", total_dicas_geral)

            if total_dicas_filtradas > 0:
                dicas_por_liga = pd.DataFrame(dicas_filtradas_list)['Liga'].value_counts()
                if not dicas_por_liga.empty:
                    col3.metric("Liga Principal", dicas_por_liga.index[0])

            # Botão para limpar filtros
            if st.button("🧹 Limpar Filtros", help="Voltar a mostrar todas as dicas"):
                st.rerun()

        else:
            st.warning("⚠️ Nenhuma dica inteligente encontrada. Verifique os dados.")
    else:
        st.error("❌ Dados não disponíveis para análise")