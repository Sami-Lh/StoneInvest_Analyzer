import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from modules.portfolio_optimizer import PortfolioOptimizer


class Visualizer:
    """
    Génère les 3 visualisations principales du projet StoneInvest.
    """

    def __init__(self, optimizer: PortfolioOptimizer, output_dir: str = "outputs/charts"):
        self.optimizer = optimizer
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)  

    # 1. FRONTIÈRE EFFICIENTE
    def plot_efficient_frontier(self, n_points: int = 100, save: bool = True):
        frontier = self.optimizer.efficient_frontier(n_points=n_points)
        vols = [p["Volatilité (%)"] for p in frontier]
        rets = [p["Rendement (%)"] for p in frontier]

        max_sharpe = self.optimizer.maximize_sharpe()
        min_var    = self.optimizer.minimize_variance()

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(vols, rets, "b-", linewidth=2, label="Frontière efficiente")
        ax.scatter(
            max_sharpe["Volatilité (%)"], max_sharpe["Rendement (%)"],
            color="gold", s=150, zorder=5,
            label=f"Max Sharpe ({max_sharpe['Sharpe Ratio']})"
        )
        ax.scatter(
            min_var["Volatilité (%)"], min_var["Rendement (%)"],
            color="green", s=150, zorder=5,
            label="Min Variance"
        )
        ax.set_xlabel("Volatilité (%)")
        ax.set_ylabel("Rendement (%)")
        ax.set_title("Frontière Efficiente — StoneInvest Analyzer")
        ax.legend()
        ax.grid(True, alpha=0.3)

        if save:
            path = f"{self.output_dir}/efficient_frontier.png"
            fig.savefig(path, dpi=150, bbox_inches="tight")
            print(f"✅ Sauvegardé : {path}")
        plt.close()


    # 2. HEATMAP DE CORRÉLATION
    def plot_correlation_heatmap(self, save: bool = True):
        corr = self.optimizer.returns.corr()

        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(
            corr,
            annot=True, fmt=".2f",
            cmap="RdYlGn", center=0,
            vmin=-1, vmax=1,
            linewidths=0.5,
            ax=ax
        )
        ax.set_title("Corrélation des Actifs — StoneInvest Analyzer")

        if save:
            path = f"{self.output_dir}/correlation_heatmap.png"
            fig.savefig(path, dpi=150, bbox_inches="tight")
            print(f"✅ Sauvegardé : {path}")
        plt.close()


    # 3. STRESS TESTS
    def plot_stress_tests(self, stress_df: pd.DataFrame, save: bool = True):
        scenarios  = stress_df.index.tolist()
        losses_pct = stress_df["Perte (%)"].values
        colors     = ["#d62728" if x < 0 else "#2ca02c" for x in losses_pct]

        fig, ax = plt.subplots(figsize=(9, 5))
        bars = ax.bar(scenarios, losses_pct, color=colors, edgecolor="black", linewidth=0.7)
        ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
        ax.set_ylabel("Perte (%)")
        ax.set_title("Stress Tests — Pertes par Scénario")

        for bar, val in zip(bars, losses_pct):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() - 0.5,
                f"{val:.1f}%",
                ha="center", va="top",
                fontsize=10, color="white", fontweight="bold"
            )

        if save:
            path = f"{self.output_dir}/stress_tests.png"
            fig.savefig(path, dpi=150, bbox_inches="tight")
            print(f"✅ Sauvegardé : {path}")
        plt.close()