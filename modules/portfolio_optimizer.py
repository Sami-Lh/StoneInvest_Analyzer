import numpy as np
import pandas as pd
from scipy.optimize import minimize
from config import RISK_FREE_RATE, TRADING_DAYS

class PortfolioOptimizer:
    """
    Optimisation de portefeuille via frontière efficiente de Markowitz.
    """

    def __init__(self, returns: pd.DataFrame):
        self.returns = returns
        self.n_assets = returns.shape[1]
        self.mean_returns = returns.mean() * TRADING_DAYS
        self.cov_matrix = returns.cov() * TRADING_DAYS
        self.asset_names = returns.columns.tolist()

    def _portfolio_stats(self, weights):
        ret = np.dot(weights, self.mean_returns)
        vol = np.sqrt(weights.T @ self.cov_matrix @ weights)
        sharpe = (ret - RISK_FREE_RATE) / vol
        return ret, vol, sharpe

    def _constraints_and_bounds(self, min_weight=0.02, max_weight=0.40):
        constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1}]
        bounds = tuple((min_weight, max_weight) for _ in range(self.n_assets))
        return constraints, bounds

    def maximize_sharpe(self, min_weight=0.02, max_weight=0.40) -> dict:
        constraints, bounds = self._constraints_and_bounds(min_weight, max_weight)
        init_weights = np.array([1 / self.n_assets] * self.n_assets)

        result = minimize(
            fun=lambda w: -self._portfolio_stats(w)[2],
            x0=init_weights,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
        )

        ret, vol, sharpe = self._portfolio_stats(result.x)
        return {
            "Stratégie": "Max Sharpe",
            "Rendement (%)": round(ret * 100, 3),
            "Volatilité (%)": round(vol * 100, 3),
            "Sharpe Ratio": round(sharpe, 4),
            "Allocations": dict(zip(self.asset_names, np.round(result.x * 100, 2))),
        }

    def minimize_variance(self, min_weight=0.02, max_weight=0.40) -> dict:
        constraints, bounds = self._constraints_and_bounds(min_weight, max_weight)
        init_weights = np.array([1 / self.n_assets] * self.n_assets)

        result = minimize(
            fun=lambda w: self._portfolio_stats(w)[1],
            x0=init_weights,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
        )

        ret, vol, sharpe = self._portfolio_stats(result.x)
        return {
            "Stratégie": "Min Variance",
            "Rendement (%)": round(ret * 100, 3),
            "Volatilité (%)": round(vol * 100, 3),
            "Sharpe Ratio": round(sharpe, 4),
            "Allocations": dict(zip(self.asset_names, np.round(result.x * 100, 2))),
        }
