import numpy as np
import pandas as pd
from scipy import stats
from config import CONFIDENCE_LEVEL, STRESS_SCENARIOS

class RiskAnalyzer:
    """
    Calcule les métriques de risque pour les portefeuilles clients :
    VaR, CVaR, volatilité, beta, drawdown maximum, et stress tests.
    """

    def __init__(self, returns: pd.DataFrame, weights: np.ndarray, portfolio_value: float):
        self.returns = returns
        self.weights = weights
        self.portfolio_value = portfolio_value
        self.portfolio_returns = returns.dot(weights)

    def volatility(self, annualized=True) -> float:
        vol = self.portfolio_returns.std()
        return vol * np.sqrt(252) if annualized else vol

    def value_at_risk(self) -> dict:
        """VaR paramétrique et historique."""
        mu = self.portfolio_returns.mean()
        sigma = self.portfolio_returns.std()

        var_param = stats.norm.ppf(1 - CONFIDENCE_LEVEL, mu, sigma)
        var_hist = np.percentile(self.portfolio_returns, (1 - CONFIDENCE_LEVEL) * 100)

        return {
            "VaR_param_pct":  round(var_param * 100, 3),
            "VaR_hist_pct":   round(var_hist * 100, 3),
            "VaR_param_eur":  round(var_param * self.portfolio_value, 2),
            "VaR_hist_eur":   round(var_hist * self.portfolio_value, 2),
        }

    def conditional_var(self) -> dict:
        """CVaR (Expected Shortfall)."""
        threshold = np.percentile(self.portfolio_returns, (1 - CONFIDENCE_LEVEL) * 100)
        cvar = self.portfolio_returns[self.portfolio_returns <= threshold].mean()
        return {
            "CVaR_pct": round(cvar * 100, 3),
            "CVaR_eur": round(cvar * self.portfolio_value, 2),
        }

    def max_drawdown(self) -> float:
        cumulative = (1 + self.portfolio_returns).cumprod()
        rolling_max = cumulative.cummax()
        drawdown = (cumulative - rolling_max) / rolling_max
        return round(drawdown.min() * 100, 3)

    def sharpe_ratio(self, risk_free_rate=0.035) -> float:
        excess_return = self.portfolio_returns.mean() * 252 - risk_free_rate
        return round(excess_return / self.volatility(), 4)

    def run_stress_tests(self, asset_class_map: dict) -> pd.DataFrame:
        results = {}
        for scenario_name, shocks in STRESS_SCENARIOS.items():
            stressed_value = 0
            for asset, weight in zip(self.returns.columns, self.weights):
                asset_class = asset_class_map.get(asset, "equity")
                shock = shocks.get(asset_class, 0)
                stressed_value += weight * self.portfolio_value * (1 + shock)
            loss = stressed_value - self.portfolio_value
            results[scenario_name] = {
                "Valeur stressée (€)": round(stressed_value, 2),
                "Perte (€)":           round(loss, 2),
                "Perte (%)":           round((loss / self.portfolio_value) * 100, 2),
            }
        return pd.DataFrame(results).T

    def full_risk_report(self, asset_class_map: dict) -> dict:
        return {
            "Volatilité (%)": self.volatility() * 100,
            "Sharpe Ratio":    self.sharpe_ratio(),
            "Max Drawdown (%)": self.max_drawdown(),
            **self.value_at_risk(),
            **self.conditional_var(),
            "Stress Tests":    self.run_stress_tests(asset_class_map),
        }
