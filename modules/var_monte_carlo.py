import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import numpy as np
from config import CONFIDENCE_LEVEL


class MonteCarloVaR: #VaR Monte Carlo
    
    def __init__(self, portfolio_returns, portfolio_value: float, n_simulations: int = 10_000):
        self.portfolio_returns = portfolio_returns
        self.portfolio_value = portfolio_value
        self.n_simulations = n_simulations
        self.mu = portfolio_returns.mean()
        self.sigma = portfolio_returns.std()

    def simulate(self, seed: int = 42) -> np.ndarray: #Génère n_simulations daily_rend via distrib normale

        rng = np.random.default_rng(seed)
        return rng.normal(self.mu, self.sigma, self.n_simulations)

    def compute_var(self) -> dict: #VaR Monte Carlo au seuil CONFIDENCE_LEVEL
        
        simulated = self.simulate()
        var_mc = np.percentile(simulated, (1 - CONFIDENCE_LEVEL) * 100)
        return {
            "VaR_mc_pct": round(var_mc * 100, 3),
            "VaR_mc_eur": round(var_mc * self.portfolio_value, 2),
            "n_simulations": self.n_simulations,
        }

    def compute_cvar(self) -> dict: #CVaR Monte Carlo
       
        simulated = self.simulate()
        threshold = np.percentile(simulated, (1 - CONFIDENCE_LEVEL) * 100)
        cvar_mc = simulated[simulated <= threshold].mean()
        return {
            "CVaR_mc_pct": round(cvar_mc * 100, 3),
            "CVaR_mc_eur": round(cvar_mc * self.portfolio_value, 2),
        }

    def full_mc_report(self) -> dict:
        return {
            **self.compute_var(),
            **self.compute_cvar(),
        }