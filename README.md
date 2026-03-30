StoneInvest_Analyzer

SCPI · ETF · Produits Structurés | Analyse Risques | Optimisation Markowitz | Reporting Automatisé

Outil d'analyse quantitative développé dans le cadre d'un stage en gestion de patrimoine.
Automatise l'analyse des risques, l'optimisation d'allocation et le reporting mensuel
pour des portefeuilles >2M€ composés de SCPI, ETF et produits structurés.


##  Contexte Professionnel

Stage Analyste Quantitatif — Gestion de Patrimoine @ Stone Invest

| Réalisation | Impact |
| Analyse risques + stress tests | 15+ portefeuilles >2M€ |
| Optimisation allocation d'actifs | +12% rendement ajusté au risque |
| Automatisation reporting mensuel | -35% temps traitement (8h → 5h) |
| Univers d'investissement | SCPI, ETF, Produits Structurés |



##  Fonctionnalités

### 1.  Analyse des Risques — `RiskAnalyzer`
- **VaR 95%** : méthode paramétrique, historique et Monte Carlo (10 000 simulations)
- **CVaR / Expected Shortfall** : perte moyenne au-delà de la VaR
- **Sharpe Ratio** — rendement ajusté au risque
- **Maximum Drawdown** — pire perte depuis un pic
- **Stress Tests** sur 4 scénarios historiques :

| Scénario | Actions | Obligations | Immobilier | Structurés |

| Crise 2008 | -45% | -8% | -20% | -30% |
| COVID Mars 2020 | -35% | +5% | -10% | -20% |
| Hausse taux 2022 | -20% | -15% | -12% | -8% |
| Choc inflation | -15% | -20% | +5% | -10% |

### 2.  Optimisation de Portefeuille — `PortfolioOptimizer`
- **Maximum Sharpe Ratio** (portefeuille tangent)
- **Minimum Variance Portfolio**
- **Frontière Efficiente** (100 points)
- Contraintes réalistes : 2% ≤ poids ≤ 40% par actif
- Algorithme : SLSQP (`scipy.optimize`)

### 3. 🎲 VaR Monte Carlo — `MonteCarloVaR`
- 10 000 simulations de rendements journaliers
- VaR et CVaR Monte Carlo au seuil de 95%
- Comparaison avec méthodes paramétrique et historique

### 4. 📄 Reporting Automatisé — `ReportGenerator`
- Export Excel professionnel (`openpyxl`)
- Onglet **Synthèse** : métriques risque + allocation optimisée
- Onglet **Stress Tests** : résultats détaillés par scénario

### 5. 📈 Visualisations & Dashboard — `Visualizer` & `Streamlit`
- Frontière efficiente (Max Sharpe + Min Variance)
- Heatmap de corrélation des actifs
- Graphique des pertes par scénario de stress
- **Dashboard interactif** pour simuler les allocations en temps réel

---

## 🗂️ Architecture

```text
StoneInvest_Analyzer/
├── modules/
│   ├── __init__.py
│   ├── risk_analysis.py       # VaR, CVaR, Sharpe, Drawdown, Stress Tests
│   ├── portfolio_optimizer.py # Markowitz, Max Sharpe, Min Variance, Frontier
│   ├── reporting.py           # Export Excel automatisé
│   ├── var_monte_carlo.py     # VaR Monte Carlo 10 000 simulations
│   └── visualizer.py          # Frontière efficiente, heatmap, stress tests
├── outputs/
│   ├── charts/                # Graphiques PNG générés
│   └── reports/               # Rapports Excel mensuels
├── data/
│   └── sample_returns.csv     # Données de rendements (reproductibilité)
├── tests/
│   ├── test_risk.py           # Tests unitaires RiskAnalyzer
│   └── test_optimizer.py      # Tests unitaires PortfolioOptimizer
├── config.py                  # Paramètres globaux
├── main.py                    # Pipeline principal
├── dashboard.py               # Dashboard Streamlit interactif
└── requirements.txt           # Dépendances du projet
```

---

## 🚀 Installation & Lancement

```bash
# 1. Cloner le repo
git clone https://github.com/[ton-username]/StoneInvest_Analyzer.git
cd StoneInvest_Analyzer

# 2. Créer l'environnement virtuel
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer l'analyse en ligne de commande
python main.py

# 5. Lancer le dashboard interactif (optionnel)
streamlit run dashboard.py
```

---

## 📦 Output attendu (CLI)

```text
✅ 5 actifs — 1080 observations
  Volatilité      : 7.78%
  Sharpe Ratio    : 6.1081
  Max Drawdown    : -2.49%
  VaR Param (95%) : -0.604%  |  -15,092 €
  VaR MC    (95%) : -0.618%  |  -15,450 €
  CVaR MC   (95%) : -0.823%  |  -20,574 €

  Max Sharpe: Sharpe 10.81 | Rdt 63.77% | Vol 5.58%

✅ Rapport exporté : outputs/reports/StoneInvest_Rapport_202602.xlsx
✅ Sauvegardé : outputs/charts/efficient_frontier.png
```

---

## 🛠️ Stack Technique

| Librairie | Usage |
|---|---|
| `numpy` / `pandas` | Calculs matriciels, manipulation données |
| `scipy.optimize` | Optimisation SLSQP (Markowitz) |
| `scipy.stats` | VaR paramétrique (loi normale) |
| `matplotlib` / `seaborn` | Visualisations |
| `openpyxl` | Export Excel |
| `streamlit` | Dashboard interactif web |

---

## 👤 Auteur

**[Ton Prénom Nom]** — Étudiant en Finance Quantitative  
🔗 [LinkedIn](https://linkedin.com/in/ton-profil) · 📧 ton@email.com
