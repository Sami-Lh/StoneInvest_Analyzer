import pandas as pd

RISK_FREE_RATE = 0.035       # Taux sans risque OAT 10 ans
CONFIDENCE_LEVEL = 0.95      # Niveau de confiance VaR
TRADING_DAYS = 252           # Jours de trading annuels
MIN_PORTFOLIO_VALUE = 2_000_000  # Seuil portefeuille (2M€)

# Classes d'actifs
ASSET_CLASSES = {
    "SCPI": ["SCPI_PierrePlus", "SCPI_Corum", "SCPI_Primopierre"],
    "ETF":  ["ETF_SP500", "ETF_EuroStoxx600", "ETF_Oblig_IG"],
    "Structured": ["CapitalProtect_2026", "AutoCall_Eurostoxx"],
}

# Scénarios de stress test
STRESS_SCENARIOS = {
    "Crise 2008":        {"equity": -0.45, "bonds": -0.08, "real_estate": -0.20, "structured": -0.30},
    "COVID Mars 2020":   {"equity": -0.35, "bonds": +0.05, "real_estate": -0.10, "structured": -0.20},
    "Hausse taux 2022":  {"equity": -0.20, "bonds": -0.15, "real_estate": -0.12, "structured": -0.08},
    "Choc inflation":    {"equity": -0.15, "bonds": -0.20, "real_estate": +0.05, "structured": -0.10},
}
