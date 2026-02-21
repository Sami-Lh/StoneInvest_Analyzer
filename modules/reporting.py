import pandas as pd
import numpy as np
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

class ReportGenerator:
    """
    Génère automatiquement les rapports mensuels clients en Excel.
    """

    def __init__(self, client_name: str, portfolio_value: float, report_date: str = None):
        self.client_name = client_name
        self.portfolio_value = portfolio_value
        self.report_date = report_date or datetime.now().strftime("%Y-%m")
        self.wb = Workbook()

    def add_summary_sheet(self, risk_metrics: dict, optimization_result: dict):
        ws = self.wb.active
        ws.title = "Synthèse"

        # Header
        ws["A1"] = f"Rapport Mensuel — {self.client_name}"
        ws["A1"].font = Font(bold=True, size=14)
        ws["A2"] = f"Valeur : {self.portfolio_value:,.0f} € | {self.report_date}"

        # Métriques de risque
        ws["A4"] = "MÉTRIQUES DE RISQUE"
        ws["A4"].font = Font(bold=True)
        metrics_map = {
            "Volatilité (%)": f"{risk_metrics.get('Volatilité (%)', 'N/A'):.2f}",
            "Sharpe Ratio": str(risk_metrics.get("Sharpe Ratio", "N/A")),
            "Max Drawdown (%)": f"{risk_metrics.get('Max Drawdown (%)', 'N/A'):.2f}",
        }
        for i, (label, value) in enumerate(metrics_map.items(), start=5):
            ws[f"A{i}"] = label
            ws[f"B{i}"] = value

        # Allocation optimisée
        ws["D4"] = "ALLOCATION OPTIMISÉE"
        ws["D4"].font = Font(bold=True)
        allocations = optimization_result.get("Allocations", {})
        for i, (asset, weight) in enumerate(allocations.items(), start=5):
            ws[f"D{i}"] = asset
            ws[f"E{i}"] = f"{weight:.2f}%"

    def export_excel(self, filepath: str):
        self.wb.save(filepath)
        print(f"✅ Rapport exporté : {filepath}")
