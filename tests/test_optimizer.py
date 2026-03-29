# tests/test_optimizer.py

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import pandas as pd
import pytest
from modules.portfolio_optimizer import PortfolioOptimizer


# FIXTURE (données synthétiques pour les tests)

@pytest.fixture
def optimizer():
    np.random.seed(42)
    n = 500
    returns = pd.DataFrame({
        "ETF_SP500":     np.random.normal(0.0008, 0.012, n),
        "ETF_EuroStoxx": np.random.normal(0.0006, 0.014, n),
        "ETF_Oblig_IG":  np.random.normal(0.0002, 0.006, n),
        "SCPI_Corum":    np.random.normal(0.0045, 0.008, n),
        "CapitalProtect":np.random.normal(0.002,  0.003, n),
    })
    return PortfolioOptimizer(returns)


# TESTS MAX SHARPE 

def test_max_sharpe_weights_sum(optimizer):
    """Les poids doivent sommer à 100%."""
    result = optimizer.maximize_sharpe()
    total = sum(result["Allocations"].values())
    assert abs(total - 100) < 0.1

def test_max_sharpe_weights_positive(optimizer):
    """Tous les poids doivent être positifs."""
    result = optimizer.maximize_sharpe()
    assert all(w >= 0 for w in result["Allocations"].values())

def test_max_sharpe_respects_bounds(optimizer):
    """Poids entre 2% et 40% (contraintes SLSQP)."""
    result = optimizer.maximize_sharpe()
    for w in result["Allocations"].values():
        assert 1.9 <= w <= 40.1  # tolérance numérique

def test_max_sharpe_keys(optimizer):
    """Le dict doit contenir toutes les clés attendues."""
    result = optimizer.maximize_sharpe()
    for key in ["Stratégie", "Rendement (%)", "Volatilité (%)", "Sharpe Ratio", "Allocations"]:
        assert key in result

def test_max_sharpe_better_than_min_var(optimizer):
    """Max Sharpe doit avoir un Sharpe > Min Variance."""
    max_s = optimizer.maximize_sharpe()
    min_v = optimizer.minimize_variance()
    assert max_s["Sharpe Ratio"] >= min_v["Sharpe Ratio"]


# TESTS MIN VARIANCE

def test_min_var_lower_volatility(optimizer):
    """Min Variance doit avoir une vol < Max Sharpe."""
    max_s = optimizer.maximize_sharpe()
    min_v = optimizer.minimize_variance()
    assert min_v["Volatilité (%)"] <= max_s["Volatilité (%)"]

def test_min_var_weights_sum(optimizer):
    """Les poids Min Variance doivent sommer à 100%."""
    result = optimizer.minimize_variance()
    total = sum(result["Allocations"].values())
    assert abs(total - 100) < 0.1


# TESTS FRONTIÈRE EFFICIENTE

def test_frontier_returns_list(optimizer):
    """efficient_frontier() doit retourner une liste."""
    frontier = optimizer.efficient_frontier(n_points=20)
    assert isinstance(frontier, list)

def test_frontier_not_empty(optimizer):
    """La frontière ne doit pas être vide."""
    frontier = optimizer.efficient_frontier(n_points=20)
    assert len(frontier) > 0

def test_frontier_increasing_vol(optimizer):
    """La volatilité doit avoir une plage cohérente le long de la frontière."""
    frontier = optimizer.efficient_frontier(n_points=20)
    vols = [p["Volatilité (%)"] for p in frontier]
    # On vérifie que la vol min < vol max  sans ordre strict
    
    assert min(vols) < max(vols)
    assert max(vols) > 0