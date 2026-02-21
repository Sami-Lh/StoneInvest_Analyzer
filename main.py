# main.py - StoneInvest_Analyzer
import numpy as np
import pandas as pd
import yfinance as yf
from modules.risk_analysis import RiskAnalyzer
from modules.portfolio_optimizer import PortfolioOptimizer
from modules.reporting import ReportGenerator
from config import ASSET_CLASSES

print("StoneInvest_Analyzer - Quant Analysis")
print("=" * 60)

# 1. Données de marché (corrigées)
print("Génération données de test")  #Problème d'accès aux données Yfinance
np.random.seed(42)
dates = pd.date_range("2022-01-01", "2026-02-21", freq="D")
n = len(dates)

returns = pd.DataFrame({
    "ETF_SP500": np.random.normal(0.0008, 0.012, n),      # ~20% annualisé
    "ETF_EuroStoxx": np.random.normal(0.0006, 0.014, n),  # ~15% annualisé  
    "ETF_Oblig_IG": np.random.normal(0.0002, 0.006, n),   # ~5% annualisé
    "SCPI_Corum": np.random.normal(0.0045, 0.008, n),     # ~5.4% stable
    "CapitalProtect": np.random.normal(0.002, 0.003, n),  # ~2.4% garanti
}, index=dates).dropna()

print(f"{len(returns.columns)} actifs — {len(returns)} observations")

# 2. Paramètres portefeuille
portfolio_value = 2_500_000
weights = np.array([0.25, 0.20, 0.15, 0.30, 0.10])
asset_class_map = {
    "ETF_SP500": "equity",
    "ETF_EuroStoxx": "equity", 
    "ETF_Oblig_IG": "bonds",
    "SCPI_Corum": "real_estate",
    "CapitalProtect": "structured",
}

# 3. Analyse des risques
print("\n Analyse des risques...")
analyzer = RiskAnalyzer(returns, weights, portfolio_value)
risk_report = analyzer.full_risk_report(asset_class_map)

print("\n RÉSULTATS RISQUE")
print("-" * 30)
print(f"Volatilité : {risk_report['Volatilité (%)']:.2f}%")
print(f"Sharpe Ratio : {risk_report['Sharpe Ratio']:.4f}")
print(f"Max Drawdown : {risk_report['Max Drawdown (%)']:.2f}%")
print("\n STRESS TESTS")
print(risk_report["Stress Tests"].round(2))

# 4. Optimisation
print("\n Optimisation...")
optimizer = PortfolioOptimizer(returns)
max_sharpe = optimizer.maximize_sharpe()
print(f"\n{max_sharpe['Stratégie']}: Sharpe {max_sharpe['Sharpe Ratio']:.4f}")
for asset, pct in max_sharpe['Allocations'].items():
    print(f"  {asset}: {pct:.1f}%")

# 5. Rapport automatisé
print("\n Génération rapport...")
report = ReportGenerator("Client StoneInvest", portfolio_value)
report.add_summary_sheet(risk_report, max_sharpe)
report.export_excel("outputs/reports/StoneInvest_Rapport_202602.xlsx")

print("\n StoneInvest_Analyzer terminé !")
print(" Rapport : outputs/reports/StoneInvest_Rapport_202602.xlsx")
