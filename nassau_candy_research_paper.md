# Product Line Profitability & Margin Performance Analysis
## Nassau Candy Distributor — Research Paper

**Prepared by:** Machine Learning & Analytics Team  
**Date:** May 2026  
**Dataset Period:** January 2, 2024 – December 31, 2025  
**Total Records Analyzed:** 10,194 orders

---

## Abstract

This research paper presents a comprehensive profitability and margin performance analysis for Nassau Candy Distributor. Using transactional order data spanning two fiscal years, this study evaluates gross margin performance, profit contribution by product and division, cost structure efficiency, and concentration risks. Key findings reveal that the Chocolate Division dominates financial performance with 95.0% of total revenue, while the Other Division operates at a structurally deficient margin of 44.8%. A Pareto analysis confirms that just 5 of 15 products (33%) account for over 80% of total gross profit. Actionable recommendations are provided for pricing strategy, product rationalization, and margin improvement.

---

## 1. Introduction

### 1.1 Background

Nassau Candy Distributor operates across multiple product lines including Chocolate, Sugar, and Other specialty confections. The organization distributes products manufactured at five geographically distributed facilities: Lot's O' Nuts (Arizona), Wicked Choccy's (Georgia), Sugar Shack (Minnesota), Secret Factory (Illinois), and The Other Factory (Tennessee).

Despite consistent sales volume, the absence of structured profitability visibility has limited the organization's ability to make informed decisions regarding pricing, product portfolio management, and operational investment. This analysis addresses that gap.

### 1.2 Problem Statement

The organization currently lacks:
- Visibility into which product lines deliver the highest gross margin
- Understanding of whether high-sales products are truly profitable
- Comparative profitability analysis across divisions and regions
- Identification of products representing margin risk or requiring strategic intervention

### 1.3 Objectives

1. Calculate and benchmark gross margin KPIs across all products and divisions
2. Identify high-margin vs. margin-risk products
3. Conduct a Pareto (80/20) analysis on profit and revenue concentration
4. Diagnose cost structure inefficiencies
5. Deliver data-driven recommendations for portfolio optimization

---

## 2. Data Overview & Cleaning

### 2.1 Dataset Description

| Field | Type | Description |
|---|---|---|
| Order ID | String | Unique order identifier |
| Order/Ship Date | Date | Order and fulfillment dates |
| Division | Categorical | Chocolate, Sugar, Other |
| Region | Categorical | Interior, Atlantic, Gulf, Pacific |
| Product Name | String | 15 unique products |
| Sales | Float | Order revenue |
| Units | Integer | Units sold |
| Gross Profit | Float | Sales minus Cost |
| Cost | Float | Cost of goods sold |

### 2.2 Data Quality Assessment

| Check | Result |
|---|---|
| Missing values | 0 across all 18 fields |
| Zero-sales records | 0 |
| Negative profit records | 0 |
| Zero-unit records | 0 |
| Duplicate Order IDs | None detected |

The dataset is clean and requires no imputation or removal of records. Date fields were parsed to datetime format (DD-MM-YYYY). Derived KPI columns were computed for all analyses.

---

## 3. Profitability Metric Calculation

The following KPIs were computed for each product and division:

| KPI | Formula | Purpose |
|---|---|---|
| Gross Margin (%) | Gross Profit ÷ Sales × 100 | Core profitability measure |
| Profit per Unit | Gross Profit ÷ Units | Unit-level efficiency |
| Revenue Contribution (%) | Product Sales ÷ Total Sales | Portfolio weight by revenue |
| Profit Contribution (%) | Product Profit ÷ Total Profit | Portfolio weight by profit |

### 3.1 Portfolio-Level KPIs

| KPI | Value |
|---|---|
| **Total Revenue** | $141,783.63 |
| **Total Gross Profit** | $93,442.80 |
| **Total COGS** | $48,340.83 |
| **Overall Gross Margin** | **65.91%** |
| **Total Units Sold** | ~38,654 |
| **Average Profit per Unit** | $2.42 |
| **Products in Portfolio** | 15 |
| **Analysis Period** | Jan 2024 – Dec 2025 |

---

## 4. Product-Level Profitability Analysis

### 4.1 Product Profitability Rankings

| Rank | Product | Revenue | Gross Profit | Margin % | Profit/Unit |
|---|---|---|---|---|---|
| 1 | Wonka Bar – Scrumdiddlyumptious | $27,874.80 | $19,357.50 | 69.4% | $2.50 |
| 2 | Wonka Bar – Triple Dazzle Caramel | $28,485.00 | $18,610.20 | 65.3% | $2.45 |
| 3 | Wonka Bar – Milk Chocolate | $26,867.75 | $17,443.37 | 64.9% | $2.11 |
| 4 | Wonka Bar – Nutty Crunch Surprise | $23,574.95 | $16,819.95 | 71.3% | $2.49 |
| 5 | Wonka Bar – Fudge Mallows | $24,890.40 | $16,593.60 | 66.7% | $2.40 |
| 6 | Lickable Wallpaper | $7,860.00 | $3,930.00 | 50.0% | $10.00 |
| 7 | Wonka Gum | $597.50 | $310.70 | 52.0% | $0.65 |
| 8 | Everlasting Gobstopper | $130.00 | $104.00 | **80.0%** | $8.00 |
| 9 | Kazookles | $1,205.75 | $92.75 | **7.7%** | $0.25 |
| 10 | Hair Toffee | $76.50 | $59.50 | 77.8% | $3.50 |
| 11 | Fizzy Lifting Drinks | $78.75 | $47.25 | 60.0% | $2.25 |
| 12 | Laffy Taffy | $53.73 | $33.48 | 62.3% | $1.24 |
| 13 | SweeTARTS | $61.50 | $28.70 | 46.7% | $0.70 |
| 14 | Nerds | $15.00 | $7.00 | 46.7% | $0.70 |
| 15 | Fun Dip | $12.00 | $4.80 | **40.0%** | $0.60 |

### 4.2 Product Segmentation

**Segment 1 – High Profit / High Margin (Stars):**  
The five Wonka Bar variants (Scrumdiddlyumptious, Triple Dazzle Caramel, Milk Chocolate, Nutty Crunch Surprise, Fudge Mallows) collectively generate $88,824.62 in gross profit at margins ranging from 64.9% to 71.3%. These are the financial backbone of the business.

**Segment 2 – High Margin / Low Volume (Hidden Gems):**  
Everlasting Gobstopper has the highest gross margin in the portfolio at 80.0% and a strong profit-per-unit of $8.00, but with only $130 in total revenue it is severely under-distributed. Hair Toffee similarly shows 77.8% margin. Both represent significant growth opportunities if volumes can be scaled.

**Segment 3 – Low Margin / Margin Risk (Problem Products):**  
Kazookles exhibits a critically low margin of 7.7% — the lowest in the portfolio by a wide margin. Fun Dip (40.0%), SweeTARTS (46.7%), and Nerds (46.7%) all fall below the 50% margin threshold and require pricing review or cost renegotiation.

---

## 5. Division-Level Performance Analysis

### 5.1 Division Financial Summary

| Division | Revenue | Gross Profit | COGS | Gross Margin | Orders |
|---|---|---|---|---|---|
| **Chocolate** | $131,692.90 | $88,824.62 | $42,868.28 | **67.4%** | 9,844 |
| **Other** | $9,663.25 | $4,333.45 | $5,329.80 | **44.8%** | 310 |
| **Sugar** | $427.48 | $284.73 | $142.75 | **66.6%** | 40 |

### 5.2 Key Division Insights

**Chocolate Division:**  
Overwhelmingly dominant, representing 92.9% of total revenue and 95.0% of total gross profit. All five Wonka Bar SKUs perform above 64% margin. The division benefits from high unit volumes, consistent pricing, and strong market demand. Operational priority should be volume expansion and geographic market penetration.

**Other Division:**  
Structurally underperforming at 44.8% gross margin — more than 20 percentage points below the portfolio average. COGS ($5,329.80) nearly equals profit ($4,333.45), indicating that cost is consuming margin. Products like Kazookles (7.7% margin) are anchor weights on divisional performance. This division requires urgent product rationalization and cost renegotiation.

**Sugar Division:**  
Marginal revenue contribution (0.3% of total) but relatively healthy margin at 66.6%. Volume uplift for Sugar products, particularly Laffy Taffy and Everlasting Gobstopper, could provide meaningful profit contribution without significant investment.

---

## 6. Pareto (Profit Concentration) Analysis

### 6.1 Product Concentration

The 80/20 rule analysis confirms a highly concentrated profit profile:

| Metric | Concentration |
|---|---|
| Products generating 80% of gross profit | **5 of 15 (33%)** |
| Products generating 80% of revenue | **5 of 15 (33%)** |
| Top division profit share (Chocolate) | **95.0%** |

The top 5 products — all Chocolate Wonka Bar variants — are responsible for $88,824.62 or **95.0%** of total gross profit. This extreme concentration presents both opportunity and risk:

- **Opportunity:** Optimizing these 5 products (pricing, volume, channel mix) has disproportionate impact on total profitability.
- **Risk:** Over-dependency on a single division and product family creates significant vulnerability to supply disruptions, cost increases, or market demand shifts.

### 6.2 Dependency Risk Assessment

| Risk Factor | Assessment |
|---|---|
| Product concentration | **HIGH** — 5 products = 95% profit |
| Division concentration | **HIGH** — Chocolate = 95% profit |
| Factory concentration | **MEDIUM** — Lot's O' Nuts + Wicked Choccy's supply all Chocolate SKUs |
| Geographic spread | **MEDIUM** — 4 regions covered |

---

## 7. Cost Structure Diagnostics

### 7.1 Cost-to-Revenue Ratio by Division

| Division | COGS | Revenue | Cost Ratio |
|---|---|---|---|
| Chocolate | $42,868.28 | $131,692.90 | 32.6% |
| Other | $5,329.80 | $9,663.25 | 55.2% |
| Sugar | $142.75 | $427.48 | 33.4% |

The Other Division's 55.2% cost-to-revenue ratio is a structural red flag. For every dollar of Other Division revenue, 55 cents goes to COGS, leaving only 45 cents as gross profit.

### 7.2 Margin Risk Flag Summary

| Risk Level | Products | Recommended Action |
|---|---|---|
| 🔴 High Risk (< 50% margin) | Kazookles, Fun Dip, SweeTARTS, Nerds | Reprice or discontinue |
| 🟡 Medium Risk (50–60%) | Lickable Wallpaper, Wonka Gum, Fizzy Lifting Drinks | Cost renegotiation |
| ✅ Low Risk (> 60%) | All 5 Wonka Bars, Hair Toffee, Everlasting Gobstopper, Laffy Taffy | Maintain & scale |

### 7.3 Kazookles Deep Dive

Kazookles is the most problematic product in the portfolio with a gross margin of only 7.7% — compared to the portfolio average of 65.9%. At $1,205.75 in revenue with only $92.75 in gross profit, Kazookles contributes less than 0.1% of total profit while consuming operational resources, sales bandwidth, and supply chain attention. Immediate action is warranted.

---

## 8. Key Findings Summary

1. **Strong overall financial performance:** Nassau Candy's 65.91% blended gross margin is high for a distributor, driven primarily by Chocolate Division efficiency.

2. **Chocolate Division is the profit engine:** 5 Wonka Bar SKUs from 2 factories generate 95% of all gross profit. The Nutty Crunch Surprise leads on margin (71.3%) while Triple Dazzle Caramel leads on absolute profit ($18,610).

3. **Other Division is a margin liability:** Operating at 44.8% margin with COGS nearly equaling profit, this division requires structural intervention.

4. **Hidden value in low-volume high-margin products:** Everlasting Gobstopper (80% margin, $8.00/unit) and Hair Toffee (77.8% margin, $3.50/unit) are dramatically underdistributed.

5. **Kazookles represents a discontinuation candidate:** With 7.7% margin and <0.1% profit contribution, it delivers no meaningful financial value and should be reviewed for removal.

6. **Extreme profit concentration creates risk:** 33% of products generate 95%+ of profit — portfolio diversification or volume building in secondary products is strategically advisable.

---

## 9. Recommendations

### 9.1 Immediate Actions (0–3 months)

| Action | Product/Division | Expected Impact |
|---|---|---|
| Reprice or discontinue Kazookles | Kazookles | Eliminate 7.7% margin drag |
| Reprice Fun Dip, SweeTARTS, Nerds | Sugar Division | Bring margin above 50% threshold |
| Audit Other Division cost structure | Other Division | Identify cost reduction opportunities |

### 9.2 Short-Term Strategy (3–6 months)

| Action | Rationale |
|---|---|
| Scale Everlasting Gobstopper distribution | 80% margin, $8/unit — highest margin in portfolio |
| Increase Hair Toffee market reach | 77.8% margin with no volume — underexploited |
| Negotiate COGS for Lickable Wallpaper | 50% margin is recoverable with 5–8% cost reduction |
| Expand Wonka Bar volume in Pacific and Gulf regions | Highest-profit products in under-penetrated regions |

### 9.3 Long-Term Portfolio Strategy (6–18 months)

| Strategy | Description |
|---|---|
| **Portfolio Rebalancing** | Reduce dependence on Chocolate Division from 95% → target 80% of profit |
| **Sugar Division Revival** | Sugar Shack factory has capacity; invest in SweeTARTS and Laffy Taffy volume |
| **Product Rationalization** | Limit SKU count in Other Division to products exceeding 55% margin |
| **Factory Risk Hedging** | Dual-source Chocolate SKUs across Lot's O' Nuts and Wicked Choccy's to mitigate supply risk |

---

## 10. Conclusion

This analysis reveals that Nassau Candy Distributor is financially strong in its core Chocolate Division but faces significant structural vulnerabilities in its Other Division and long-tail product portfolio. The 65.91% overall gross margin is healthy; however, it masks a highly uneven profit landscape where 5 products carry 95% of the profit burden.

By acting on the recommendations outlined — particularly addressing Kazookles, scaling hidden gems like Everlasting Gobstopper, and restructuring the Other Division — Nassau Candy can improve margin resilience, reduce concentration risk, and strengthen its competitive position across all four U.S. regions.

---

## Appendix

### A. Factory Coordinates

| Factory | Location | Latitude | Longitude |
|---|---|---|---|
| Lot's O' Nuts | Arizona | 32.88°N | 111.77°W |
| Wicked Choccy's | Georgia | 32.08°N | 81.09°W |
| Sugar Shack | Minnesota | 48.12°N | 96.18°W |
| Secret Factory | Illinois | 41.45°N | 90.57°W |
| The Other Factory | Tennessee | 35.12°N | 89.97°W |

### B. Product-Factory Mapping

| Division | Product | Factory |
|---|---|---|
| Chocolate | Nutty Crunch Surprise, Fudge Mallows, Scrumdiddlyumptious | Lot's O' Nuts |
| Chocolate | Milk Chocolate, Triple Dazzle Caramel | Wicked Choccy's |
| Sugar | Laffy Taffy, SweeTARTS, Nerds, Fun Dip, Fizzy Lifting Drinks | Sugar Shack |
| Sugar/Other | Everlasting Gobstopper, Lickable Wallpaper, Wonka Gum | Secret Factory |
| Other | Hair Toffee, Kazookles | The Other Factory |

---

*End of Research Paper — Nassau Candy Distributor Profitability Analysis*
