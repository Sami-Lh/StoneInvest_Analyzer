import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import streamlit as st
import numpy as np
import pandas as pd

from modules.risk_analysis import RiskAnalyzer
from modules.portfolio_optimizer import PortfolioOptimizer
from modules.var_monte_carlo import MonteCarloVaR
from modules.visualizer import Visualizer
from config import ASSET_CLASSES

# CONFIG PAGE
st.set_page_config(
    page_title="StoneInvest Analyzer",
    page_icon="📊",
    layout="wide"
)

st.title("📊 StoneInvest Analyzer")
st.caption("SCPI · ETF · Produits Structurés | Analyse Risques | Optimisation Markowitz")
st.divider()


# PARAMÈTRES SIDEBAR
with st.sidebar:
    st.header("⚙️ Paramètres")

    portfolio_value = st.number_input(
        "Valeur du portefeuille (€)",
        min_value=500_000,
        max_value=10_000_000,
        value=2_500_000,
        step=100_000,
        format="%d"
    )

    st.subheader("Allocation initiale (%)")
    w1 = st.slider("ETF_SP500",      2, 40, 25)
    w2 = st.slider("ETF_EuroStoxx",  2, 40, 20)
    w3 = st.slider("ETF_Oblig_IG",   2, 40, 15)
    w4 = st.slider("SCPI_Corum",     2, 40, 30)
    w5 = st.slider("CapitalProtect", 2, 40, 10)

    total_w = w1 + w2 + w3 + w4 + w5
    if total_w != 100:
        st.warning(f"⚠️ Total des poids : {total_w}% (doit être 100%)")
    else:
        st.success(f"✅ Total : {total_w}%")

    n_simulations = st.select_slider(
        "Simulations Monte Carlo",
        options=[1_000, 5_000, 10_000, 50_000],
        value=10_000
    )

    run = st.button("🚀 Lancer l'analyse", use_container_width=True)


# DATA
@st.cache_data
def load_data():
    if os.path.exists("data/sample_returns.csv"):
        returns = pd.read_csv("data/sample_returns.csv", index_col=0)
    else:
        np.random.seed(42)
        n = 1080
        returns = pd.DataFrame({
            "ETF_SP500":     np.random.normal(0.0008, 0.012, n),
            "ETF_EuroStoxx": np.random.normal(0.0006, 0.014, n),
            "ETF_Oblig_IG":  np.random.normal(0.0002, 0.006, n),
            "SCPI_Corum":    np.random.normal(0.0045, 0.008, n),
            "CapitalProtect":np.random.normal(0.002,  0.003, n),
        })
    return returns

returns = load_data()

asset_class_map = {
    "ETF_SP500":     "equity",
    "ETF_EuroStoxx": "equity",
    "ETF_Oblig_IG":  "bonds",
    "SCPI_Corum":    "real_estate",
    "CapitalProtect":"structured",
}


# ANALYSE
if True:  
    weights = np.array([w1, w2, w3, w4, w5]) / 100

    analyzer  = RiskAnalyzer(returns, weights, portfolio_value)
    optimizer = PortfolioOptimizer(returns)
    mc        = MonteCarloVaR(analyzer.portfolio_returns, portfolio_value, n_simulations)

    risk_report = analyzer.full_risk_report(asset_class_map)
    stress_df   = risk_report.pop("Stress Tests")
    mc_report   = mc.full_mc_report()
    max_sharpe  = optimizer.maximize_sharpe()
    min_var     = optimizer.minimize_variance()

    # ROW 1 — KPI MÉTRIQUES
    st.subheader("📐 Métriques de Risque")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Volatilité",    f"{risk_report['Volatilité (%)']:.2f}%")
    c2.metric("Sharpe Ratio",  f"{risk_report['Sharpe Ratio']:.2f}")
    c3.metric("Max Drawdown",  f"{risk_report['Max Drawdown (%)']:.2f}%")
    c4.metric("VaR 95% (€)",   f"{risk_report['VaR_param_eur']:,.0f} €")
    c5.metric("CVaR 95% (€)",  f"{risk_report['CVaR_eur']:,.0f} €")

    st.divider()

    # ROW 2 — VAR COMPARAISON + STRESS TESTS
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🎲 Comparaison VaR (95%)")
        var_data = pd.DataFrame({
            "Méthode": ["Paramétrique", "Historique", "Monte Carlo"],
            "VaR (%)": [
                risk_report["VaR_param_pct"],
                risk_report["VaR_hist_pct"],
                mc_report["VaR_mc_pct"],
            ],
            "VaR (€)": [
                risk_report["VaR_param_eur"],
                risk_report["VaR_hist_eur"],
                mc_report["VaR_mc_eur"],
            ],
        })
        st.dataframe(var_data, hide_index=True, use_container_width=True)

    with col2:
        st.subheader("🔥 Stress Tests")
        st.dataframe(stress_df.round(2), use_container_width=True)

    st.divider()

    # ROW 3 — OPTIMISATION
    st.subheader("⚙️ Optimisation Markowitz")
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("**🥇 Max Sharpe Ratio**")
        alloc_ms = pd.DataFrame(
            max_sharpe["Allocations"].items(),
            columns=["Actif", "Poids (%)"]
        )
        st.dataframe(alloc_ms, hide_index=True, use_container_width=True)
        st.caption(f"Sharpe : {max_sharpe['Sharpe Ratio']} | "
                   f"Rdt : {max_sharpe['Rendement (%)']:.2f}% | "
                   f"Vol : {max_sharpe['Volatilité (%)']:.2f}%")

    with col4:
        st.markdown("**🛡️ Min Variance**")
        alloc_mv = pd.DataFrame(
            min_var["Allocations"].items(),
            columns=["Actif", "Poids (%)"]
        )
        st.dataframe(alloc_mv, hide_index=True, use_container_width=True)
        st.caption(f"Sharpe : {min_var['Sharpe Ratio']} | "
                   f"Rdt : {min_var['Rendement (%)']:.2f}% | "
                   f"Vol : {min_var['Volatilité (%)']:.2f}%")

    st.divider()

    # ROW 4 — GRAPHIQUES
    st.subheader("📈 Visualisations")
    col5, col6 = st.columns(2)

    with col5:
        if os.path.exists("outputs/charts/efficient_frontier.png"):
            st.image("outputs/charts/efficient_frontier.png",
                     caption="Frontière Efficiente", use_container_width=True)
        else:
            st.info("Lance main.py pour générer les graphiques")

    with col6:
        if os.path.exists("outputs/charts/correlation_heatmap.png"):
            st.image("outputs/charts/correlation_heatmap.png",
                     caption="Heatmap Corrélation", use_container_width=True)

    if os.path.exists("outputs/charts/stress_tests.png"):
        st.image("outputs/charts/stress_tests.png",
                 caption="Stress Tests — Pertes par Scénario",
                 use_container_width=True)

    st.divider()

    # ROW 5 — EXPORT EXCEL
    report_path = "outputs/reports/StoneInvest_Rapport_202602.xlsx"
    if os.path.exists(report_path):
        with open(report_path, "rb") as f:
            st.download_button(
                label="📥 Télécharger le rapport Excel",
                data=f,
                file_name="StoneInvest_Rapport_202602.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )