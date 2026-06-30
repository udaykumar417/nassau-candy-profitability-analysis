# 🍬 Nassau Candy Distributor — Product Line Profitability & Margin Performance Analysis

A data analytics project examining product- and division-level profitability for Nassau Candy Distributor, including a research paper, executive summary, and a live interactive Streamlit dashboard.

---

## 📁 Project Files

| File | Description |
|---|---|
| `Nassau_Candy_Distributor.csv` | Raw dataset (10,194 orders, 18 fields) |
| `nassau_candy_dashboard.py` | Streamlit dashboard application |
| `nassau_candy_research_paper.md` | Full research paper (EDA, methodology, findings, recommendations) |
| `nassau_candy_executive_summary.md` | One-page summary for stakeholders |
| `README.md` | This file |

---

## 📊 Project Overview

Nassau Candy needed visibility into **which products and divisions actually drive profit** — not just sales volume. This project analyzes order-level data across 3 divisions (Chocolate, Sugar, Other) and 15 products to surface:

- Gross margin performance by product and division
- High-sales but low-margin "problem" products
- Profit concentration (Pareto / 80-20) risk
- Cost structure inefficiencies and margin risk flags

**Key result:** Overall gross margin is **65.91%**, but just **5 of 15 products generate 95% of total profit** — revealing a heavily concentrated, Chocolate-driven business.

---

## 🗂️ Dataset

**Source:** `Nassau_Candy_Distributor.csv`
**Size:** 10,194 rows × 18 columns
**Period:** January 2024 – December 2025

| Field | Description |
|---|---|
| Row ID / Order ID | Unique identifiers |
| Order Date / Ship Date | Transaction dates |
| Ship Mode | Shipping method |
| Customer ID, City, State/Province, Postal Code | Customer geography |
| Division, Region | Product division & customer region |
| Product ID, Product Name | Product identifiers |
| Sales, Units, Cost, Gross Profit | Financial metrics |

No missing values, zero-sales records, or negative profits were found — the dataset required no cleaning beyond date parsing.

---

## 🧮 Methodology

1. **Data Cleaning & Validation** — verified sales/cost integrity, parsed dates, standardized labels
2. **KPI Calculation** — Gross Margin %, Profit per Unit, Revenue/Profit Contribution %
3. **Product-Level Analysis** — ranked all 15 products by profit and margin
4. **Division-Level Analysis** — compared Chocolate, Sugar, and Other divisions
5. **Pareto (80/20) Analysis** — identified profit/revenue concentration
6. **Cost Diagnostics** — flagged margin-risk products via cost-vs-sales scatter analysis

---

## 🔑 Key Findings

| Finding | Detail |
|---|---|
| 🍫 Chocolate dominance | 5 Wonka Bar SKUs = 95% of total gross profit |
| ⚠️ Other Division underperforms | 44.8% margin vs. 65.9% company average |
| 💎 Hidden gem | Everlasting Gobstopper: 80% margin, but only $130 revenue (under-distributed) |
| 🚨 Margin risk | Kazookles: 7.7% margin — lowest in portfolio, discontinuation candidate |
| 📈 Concentration risk | Just 5 of 15 products drive 80%+ of profit |

Full details, charts, and recommendations are in `nassau_candy_research_paper.md`.

---

## 🖥️ Running the Dashboard

### Requirements
```bash
pip install streamlit pandas numpy plotly
```

### Setup
1. Place `Nassau_Candy_Distributor.csv` in the same folder as `nassau_candy_dashboard.py`
2. Run:
```bash
streamlit run nassau_candy_dashboard.py
```
3. Open the local URL shown in your terminal (typically `http://localhost:8501`)

### Dashboard Modules
- **📊 Overview & KPIs** — top-line metrics, monthly trends, division comparison
- **🏆 Product Profitability** — margin leaderboard, treemap, revenue/profit bubble chart
- **🏭 Division Performance** — revenue/profit/cost breakdown, regional & factory analysis
- **📈 Pareto Analysis** — profit/revenue concentration curves, state-level dependency
- **🔬 Cost Diagnostics** — risk-flagged scatter plots, recommended actions per product
- **📅 Trend Analysis** — monthly/yearly trends, ship mode profitability

### Interactive Filters (Sidebar)
- Date range selector
- Division filter (multi-select)
- Region filter (multi-select)
- Gross margin threshold slider
- Product name search

---

## 📦 Deliverables Checklist

- [x] Data cleaning & validation
- [x] Profitability metric calculation (Gross Margin %, Profit/Unit, Contribution %)
- [x] Product-level profitability ranking
- [x] Division-level performance comparison
- [x] Pareto (80/20) concentration analysis
- [x] Cost structure diagnostics & risk flagging
- [x] Streamlit interactive dashboard
- [x] Research paper (EDA, insights, recommendations)
- [x] Executive summary for stakeholders

---

## 🏭 Factory Reference

| Factory | State | Supplies |
|---|---|---|
| Lot's O' Nuts | Arizona | Nutty Crunch Surprise, Fudge Mallows, Scrumdiddlyumptious |
| Wicked Choccy's | Georgia | Milk Chocolate, Triple Dazzle Caramel |
| Sugar Shack | Minnesota | Laffy Taffy, SweeTARTS, Nerds, Fun Dip, Fizzy Lifting Drinks |
| Secret Factory | Illinois | Everlasting Gobstopper, Lickable Wallpaper, Wonka Gum |
| The Other Factory | Tennessee | Hair Toffee, Kazookles |

---

## 🛠️ Tech Stack

- **Python** — pandas, numpy for data processing
- **Streamlit** — dashboard framework
- **Plotly** — interactive visualizations (bar, scatter, treemap, Pareto, box plots)

---

*Nassau Candy Distributor · Product Line Profitability & Margin Performance Analysis*
