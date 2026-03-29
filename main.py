import os
import numpy as np
import pandas as pd

# Création  des dossiers
os.makedirs("outputs/reports", exist_ok=True)
os.makedirs("outputs/charts", exist_ok=True)
os.makedirs("data", exist_ok=True)

try:
    import yfinance as yf
    USE_YFINANCE = True
except ImportError:
    USE_YFINANCE = False

from modules.risk_analysis import RiskAnalyzer
from modules.portfolio_optimizer import PortfolioOptimizer
from modules.reporting import ReportGenerator
from modules.var_monte_carlo import MonteCarloVaR
from modules.visualizer import Visualizer
from config import ASSET_CLASSES

print("StoneInvest_Analyzer - Quant Analysis")
print("=" * 60)


# 1. Data du marché
print("Génération données de test")

np.random.seed(42)
dates = pd.date_range("2022-01-01", "2026-02-21", freq="B")
n = len(dates)

returns = pd.DataFrame({
    "ETF_SP500":     np.random.normal(0.0008, 0.012, n),
    "ETF_EuroStoxx": np.random.normal(0.0006, 0.014, n),
    "ETF_Oblig_IG":  np.random.normal(0.0002, 0.006, n),
    "SCPI_Corum":    np.random.normal(0.0045, 0.008, n),
    "CapitalProtect":np.random.normal(0.002,  0.003, n),
}, index=dates).dropna()

returns.to_csv("data/sample_returns.csv")
print(f"{len(returns.columns)} actifs — {len(returns)} observations")


# 2. Paramètres du portefeuille
portfolio_value = 2_500_000
weights = np.array([0.25, 0.20, 0.15, 0.30, 0.10])

asset_class_map = {
    "ETF_SP500":     "equity",
    "ETF_EuroStoxx": "equity",
    "ETF_Oblig_IG":  "bonds",
    "SCPI_Corum":    "real_estate",
    "CapitalProtect":"structured",
}


# 3. ANALYSE DES RISQUES
print("\n Analyse des risques")
analyzer = RiskAnalyzer(returns, weights, portfolio_value)
risk_report = analyzer.full_risk_report(asset_class_map)
stress_df = risk_report.pop("Stress Tests")

print("\n RÉSULTATS RISQUE")
print("-" * 40)
print(f"  Volatilité      : {risk_report['Volatilité (%)']:.2f}%")
print(f"  Sharpe Ratio    : {risk_report['Sharpe Ratio']:.4f}")
print(f"  Max Drawdown    : {risk_report['Max Drawdown (%)']:.2f}%")
print(f"  VaR Param (95%) : {risk_report['VaR_param_pct']:.3f}%  |  {risk_report['VaR_param_eur']:,.0f} €")
print(f"  VaR Hist  (95%) : {risk_report['VaR_hist_pct']:.3f}%  |  {risk_report['VaR_hist_eur']:,.0f} €")
print(f"  CVaR      (95%) : {risk_report['CVaR_pct']:.3f}%  |  {risk_report['CVaR_eur']:,.0f} €")


# 4. VAR MONTE CARLO
print("\n VaR Monte Carlo (10 000 simulations)")
mc = MonteCarloVaR(analyzer.portfolio_returns, portfolio_value)
mc_report = mc.full_mc_report()
risk_report.update(mc_report)  

print(f"  VaR MC    (95%) : {mc_report['VaR_mc_pct']:.3f}%  |  {mc_report['VaR_mc_eur']:,.0f} €")
print(f"  CVaR MC   (95%) : {mc_report['CVaR_mc_pct']:.3f}%  |  {mc_report['CVaR_mc_eur']:,.0f} €")

print("\n🔥 STRESS TESTS")
print(stress_df.round(2).to_string())


# 5. OPTIMISATION
print("\n  Optimisation...")
optimizer = PortfolioOptimizer(returns)
max_sharpe = optimizer.maximize_sharpe()
min_var    = optimizer.minimize_variance()

print(f"\n  {max_sharpe['Stratégie']}: Sharpe {max_sharpe['Sharpe Ratio']:.4f} "
      f"| Rdt {max_sharpe['Rendement (%)']:.2f}% | Vol {max_sharpe['Volatilité (%)']:.2f}%")
for asset, pct in max_sharpe['Allocations'].items():
    print(f"    {asset}: {pct:.1f}%")

print(f"\n  {min_var['Stratégie']}: Sharpe {min_var['Sharpe Ratio']:.4f} "
      f"| Rdt {min_var['Rendement (%)']:.2f}% | Vol {min_var['Volatilité (%)']:.2f}%")


# 6. VISUALISATIONS
print("\n Génération des graphiques...")
viz = Visualizer(optimizer, output_dir="outputs/charts")
viz.plot_efficient_frontier()
viz.plot_correlation_heatmap()
viz.plot_stress_tests(stress_df)


# 7. RAPPORT EXCEL
print("\n Génération rapport Excel...")
report = ReportGenerator("Client StoneInvest", portfolio_value)
report.add_summary_sheet(risk_report, max_sharpe)
report.add_stress_test_sheet(stress_df)
report.export_excel("outputs/reports/StoneInvest_Rapport_202602.xlsx")

print("\n StoneInvest_Analyzer terminé !")
print("📁 Rapport    : outputs/reports/StoneInvest_Rapport_202602.xlsx")
print("📁 Graphiques : outputs/charts/")