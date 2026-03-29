import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import pandas as pd
import pytest
from modules.risk_analysis import RiskAnalyzer

#Set up des données
@pytest.fixture
def sample_data():
    np.random.seed(42)
    n = 500
    returns = pd.DataFrame({
        "ETF_SP500":     np.random.normal(0.0008, 0.012, n),
        "ETF_EuroStoxx": np.random.normal(0.0006, 0.014, n),
        "ETF_Oblig_IG":  np.random.normal(0.0002, 0.006, n),
        "SCPI_Corum":    np.random.normal(0.0045, 0.008, n),
        "CapitalProtect":np.random.normal(0.002,  0.003, n),
    })
    weights = np.array([0.25, 0.20, 0.15, 0.30, 0.10])
    portfolio_value = 2_500_000
    return RiskAnalyzer(returns, weights, portfolio_value)

@pytest.fixture
def asset_class_map():
    return {
        "ETF_SP500":     "equity",
        "ETF_EuroStoxx": "equity",
        "ETF_Oblig_IG":  "bonds",
        "SCPI_Corum":    "real_estate",
        "CapitalProtect":"structured",
    }

# Tests de vol
def test_volatility_positive(sample_data):
    assert sample_data.volatility() > 0

def test_volatility_annualized(sample_data):
    assert sample_data.volatility(annualized=True) > sample_data.volatility(annualized=False)

# Tests VaR
def test_var_negative(sample_data):
    var = sample_data.value_at_risk()
    assert var["VaR_param_pct"] < 0
    assert var["VaR_hist_pct"] < 0

def test_var_eur_coherent(sample_data): #VaR en € = VaR % × portfolio_value.
    var = sample_data.value_at_risk()
    expected = round(var["VaR_param_pct"] / 100 * 2_500_000, 2)
    assert abs(var["VaR_param_eur"] - expected) < 50

def test_var_keys_present(sample_data):
    var = sample_data.value_at_risk()
    for key in ["VaR_param_pct", "VaR_hist_pct", "VaR_param_eur", "VaR_hist_eur"]:
        assert key in var

# Tests CVaR
def test_cvar_worse_than_var(sample_data): #CVaR pire que VaR historique.
    var = sample_data.value_at_risk()
    cvar = sample_data.conditional_var()
    assert cvar["CVaR_pct"] < var["VaR_hist_pct"]

def test_cvar_negative(sample_data):
    """CVaR représente une perte — doit être négative."""
    cvar = sample_data.conditional_var()
    assert cvar["CVaR_pct"] < 0

# Tests Sharpe
def test_sharpe_is_float(sample_data): #Sharpe Ratio doit être un float
    assert isinstance(sample_data.sharpe_ratio(), float)

def test_sharpe_positive(sample_data): #rend simulés positifs donc Sharpe > 0.
    assert sample_data.sharpe_ratio() > 0

# Tests Max DD
def test_drawdown_negative(sample_data):
    assert sample_data.max_drawdown() <= 0

def test_drawdown_max_minus_100(sample_data):
    assert sample_data.max_drawdown() >= -100

# Tests Stress Tests
def test_stress_returns_dataframe(sample_data, asset_class_map):
    result = sample_data.run_stress_tests(asset_class_map)
    assert isinstance(result, pd.DataFrame)

def test_stress_4_scenarios(sample_data, asset_class_map):
    result = sample_data.run_stress_tests(asset_class_map)
    assert len(result) == 4

def test_stress_losses_negative(sample_data, asset_class_map):
    result = sample_data.run_stress_tests(asset_class_map)
    assert (result["Perte (%)"] < 0).all()

# RAPPORT TEST COMPLET
def test_full_risk_report_keys(sample_data, asset_class_map):
    """full_risk_report() doit contenir toutes les clés attendues."""
    report = sample_data.full_risk_report(asset_class_map)
    expected_keys = [
        "Volatilité (%)", "Sharpe Ratio", "Max Drawdown (%)",
        "VaR_param_pct", "VaR_hist_pct", "CVaR_pct", "Stress Tests"
    ]
    for key in expected_keys:
        assert key in report, f"Clé manquante : {key}"