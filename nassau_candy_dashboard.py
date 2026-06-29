import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nassau Candy – Profitability Dashboard",
    page_icon="🍬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    .main { background: #0f0f1a; }
    
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid #2a2a4a;
        border-radius: 16px;
        padding: 20px 24px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        transition: transform 0.2s;
    }
    .metric-card:hover { transform: translateY(-2px); }
    .metric-label { color: #8888aa; font-size: 12px; font-weight: 500; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
    .metric-value { color: #e0e0ff; font-size: 28px; font-weight: 700; }
    .metric-sub { color: #6677ff; font-size: 13px; margin-top: 4px; }
    
    .section-header {
        color: #c0c0ff;
        font-size: 18px;
        font-weight: 600;
        padding: 12px 0 8px 0;
        border-bottom: 2px solid #2a2a5a;
        margin-bottom: 16px;
    }
    
    .risk-badge-high { background: #ff4444; color: white; border-radius: 8px; padding: 2px 10px; font-size: 12px; font-weight: 600; }
    .risk-badge-med  { background: #ffaa00; color: black; border-radius: 8px; padding: 2px 10px; font-size: 12px; font-weight: 600; }
    .risk-badge-low  { background: #00cc88; color: black; border-radius: 8px; padding: 2px 10px; font-size: 12px; font-weight: 600; }
    
    .stSelectbox label, .stMultiSelect label, .stSlider label, .stDateInput label { color: #aaaacc !important; }
    
    [data-testid="stSidebar"] { background: #0d0d1f; border-right: 1px solid #2a2a4a; }
    [data-testid="stSidebar"] .stMarkdown { color: #ccccee; }
    
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #2a2a4a;
        border-radius: 12px;
        padding: 16px;
    }
</style>
""", unsafe_allow_html=True)

# ─── LOAD DATA ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("Nassau_Candy_Distributor.csv")
    df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
    df['Ship Date']  = pd.to_datetime(df['Ship Date'],  dayfirst=True)
    df['Gross Margin (%)'] = (df['Gross Profit'] / df['Sales']) * 100
    df['Profit per Unit']  = df['Gross Profit'] / df['Units']
    df['Month']            = df['Order Date'].dt.to_period('M').astype(str)
    df['Year']             = df['Order Date'].dt.year

    # Factory mapping
    factory_map = {
        'Wonka Bar - Nutty Crunch Surprise'   : "Lot's O' Nuts",
        'Wonka Bar - Fudge Mallows'           : "Lot's O' Nuts",
        'Wonka Bar -Scrumdiddlyumptious'      : "Lot's O' Nuts",
        'Wonka Bar - Milk Chocolate'          : "Wicked Choccy's",
        'Wonka Bar - Triple Dazzle Caramel'   : "Wicked Choccy's",
        'Laffy Taffy'                         : "Sugar Shack",
        'SweeTARTS'                           : "Sugar Shack",
        'Nerds'                               : "Sugar Shack",
        'Fun Dip'                             : "Sugar Shack",
        'Fizzy Lifting Drinks'                : "Sugar Shack",
        'Everlasting Gobstopper'              : "Secret Factory",
        'Lickable Wallpaper'                  : "Secret Factory",
        'Wonka Gum'                           : "Secret Factory",
        'Hair Toffee'                         : "The Other Factory",
        'Kazookles'                           : "The Other Factory",
    }
    df['Factory'] = df['Product Name'].map(factory_map)
    return df

df_raw = load_data()

# ─── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🍬 Nassau Candy")
    st.markdown("### Profitability Analytics")
    st.divider()

    min_date = df_raw['Order Date'].min().date()
    max_date = df_raw['Order Date'].max().date()
    date_range = st.date_input("📅 Order Date Range", value=(min_date, max_date),
                               min_value=min_date, max_value=max_date)

    divisions = st.multiselect("🏭 Division", options=sorted(df_raw['Division'].unique()),
                               default=sorted(df_raw['Division'].unique()))

    regions = st.multiselect("🌎 Region", options=sorted(df_raw['Region'].unique()),
                             default=sorted(df_raw['Region'].unique()))

    margin_threshold = st.slider("📊 Min Gross Margin (%)", 0, 100, 0, step=5)

    product_search = st.text_input("🔍 Search Product", placeholder="e.g. Wonka")

    st.divider()
    st.markdown("**Dashboard Modules**")
    module = st.radio("", [
        "📊 Overview & KPIs",
        "🏆 Product Profitability",
        "🏭 Division Performance",
        "📈 Pareto Analysis",
        "🔬 Cost Diagnostics",
        "📅 Trend Analysis"
    ], label_visibility="collapsed")

# ─── FILTER DATA ───────────────────────────────────────────────────────────────
df = df_raw.copy()
if len(date_range) == 2:
    df = df[(df['Order Date'].dt.date >= date_range[0]) & (df['Order Date'].dt.date <= date_range[1])]
if divisions:
    df = df[df['Division'].isin(divisions)]
if regions:
    df = df[df['Region'].isin(regions)]
df = df[df['Gross Margin (%)'] >= margin_threshold]
if product_search:
    df = df[df['Product Name'].str.contains(product_search, case=False, na=False)]

# ─── AGGREGATIONS ──────────────────────────────────────────────────────────────
def get_product_agg(data):
    prod = data.groupby(['Product Name','Division','Factory']).agg(
        Total_Sales   = ('Sales','sum'),
        Total_Profit  = ('Gross Profit','sum'),
        Total_Units   = ('Units','sum'),
        Total_Cost    = ('Cost','sum'),
        Orders        = ('Row ID','count')
    ).reset_index()
    prod['Gross Margin (%)']        = (prod['Total_Profit'] / prod['Total_Sales']) * 100
    prod['Profit per Unit']         = prod['Total_Profit'] / prod['Total_Units']
    prod['Revenue Contribution (%)']= (prod['Total_Sales'] / prod['Total_Sales'].sum()) * 100
    prod['Profit Contribution (%)'] = (prod['Total_Profit'] / prod['Total_Profit'].sum()) * 100
    return prod

def get_division_agg(data):
    div = data.groupby('Division').agg(
        Total_Sales  = ('Sales','sum'),
        Total_Profit = ('Gross Profit','sum'),
        Total_Cost   = ('Cost','sum'),
        Total_Units  = ('Units','sum'),
        Orders       = ('Row ID','count')
    ).reset_index()
    div['Gross Margin (%)']         = (div['Total_Profit'] / div['Total_Sales']) * 100
    div['Revenue Contribution (%)'] = (div['Total_Sales'] / div['Total_Sales'].sum()) * 100
    return div

prod_df = get_product_agg(df)
div_df  = get_division_agg(df)

COLORS = {
    'Chocolate': '#8B4513',
    'Sugar'    : '#FF69B4',
    'Other'    : '#6A5ACD',
}
PALETTE = ['#6677ff','#ff6b9d','#00cc88','#ffaa44','#ff4466','#44ccff','#cc88ff']

# ─── PLOTLY THEME ──────────────────────────────────────────────────────────────
CHART_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(26,26,46,0.6)',
    font=dict(color='#ccccee', family='Inter'),
    margin=dict(l=10, r=10, t=40, b=10),
    legend=dict(bgcolor='rgba(0,0,0,0)', bordercolor='#2a2a4a'),
    xaxis=dict(gridcolor='#2a2a3a', zerolinecolor='#2a2a3a'),
    yaxis=dict(gridcolor='#2a2a3a', zerolinecolor='#2a2a3a'),
)

# ══════════════════════════════════════════════════════════════════════════════
#  MODULE 1 – OVERVIEW & KPIs
# ══════════════════════════════════════════════════════════════════════════════
if module == "📊 Overview & KPIs":
    st.markdown("## 🍬 Nassau Candy Distributor — Profitability Dashboard")
    st.caption(f"Showing **{len(df):,}** orders | Date range: {date_range[0]} → {date_range[1]}")
    st.divider()

    total_rev    = df['Sales'].sum()
    total_profit = df['Gross Profit'].sum()
    total_cost   = df['Cost'].sum()
    overall_margin = total_profit / total_rev * 100 if total_rev else 0
    total_units  = df['Units'].sum()
    avg_ppu      = df['Gross Profit'].sum() / df['Units'].sum() if total_units else 0
    num_products = df['Product Name'].nunique()

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    cards = [
        (c1,"💰 Total Revenue",   f"${total_rev:,.0f}",   "Gross Sales"),
        (c2,"📈 Total Profit",    f"${total_profit:,.0f}","After COGS"),
        (c3,"🏭 Total Cost",      f"${total_cost:,.0f}",  "COGS"),
        (c4,"📊 Gross Margin",    f"{overall_margin:.1f}%","Overall"),
        (c5,"📦 Units Sold",      f"{total_units:,}",     "All products"),
        (c6,"🎯 Profit / Unit",   f"${avg_ppu:.2f}",      f"{num_products} products"),
    ]
    for col, label, val, sub in cards:
        col.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{val}</div>
            <div class="metric-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Revenue & Profit by Division  +  Monthly trend
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="section-header">Revenue vs Profit by Division</div>', unsafe_allow_html=True)
        fig = go.Figure()
        for i, row in div_df.iterrows():
            clr = COLORS.get(row['Division'], '#6677ff')
            fig.add_trace(go.Bar(name=f"{row['Division']} – Revenue",
                                 x=[row['Division']], y=[row['Total_Sales']],
                                 marker_color=clr, opacity=0.7,
                                 legendgroup=row['Division']))
            fig.add_trace(go.Bar(name=f"{row['Division']} – Profit",
                                 x=[row['Division']], y=[row['Total_Profit']],
                                 marker_color=clr, opacity=1.0,
                                 legendgroup=row['Division'], showlegend=False))
        fig.update_layout(**CHART_LAYOUT, barmode='group', height=320,
                          title="Division: Revenue vs Gross Profit")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown('<div class="section-header">Monthly Revenue & Profit Trend</div>', unsafe_allow_html=True)
        monthly = df.groupby('Month').agg(Revenue=('Sales','sum'), Profit=('Gross Profit','sum')).reset_index()
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=monthly['Month'], y=monthly['Revenue'],
                                  name='Revenue', line=dict(color='#6677ff', width=2.5), fill='tozeroy',
                                  fillcolor='rgba(102,119,255,0.15)'))
        fig2.add_trace(go.Scatter(x=monthly['Month'], y=monthly['Profit'],
                                  name='Profit', line=dict(color='#00cc88', width=2.5), fill='tozeroy',
                                  fillcolor='rgba(0,204,136,0.15)'))
        fig2.update_layout(**CHART_LAYOUT, height=320, title="Monthly Revenue & Profit")
        fig2.update_xaxes(tickangle=45, nticks=12)
        st.plotly_chart(fig2, use_container_width=True)

    # Division margin donut  +  Top 5 products
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-header">Profit Share by Division</div>', unsafe_allow_html=True)
        fig3 = px.pie(div_df, names='Division', values='Total_Profit',
                      color='Division', color_discrete_map=COLORS,
                      hole=0.55)
        fig3.update_traces(textposition='outside', textinfo='label+percent',
                           marker=dict(line=dict(color='#0f0f1a', width=2)))
        fig3.update_layout(**CHART_LAYOUT, height=320,
                           annotations=[dict(text=f"${total_profit:,.0f}", x=0.5, y=0.5,
                                             font_size=14, showarrow=False, font_color='#e0e0ff')])
        st.plotly_chart(fig3, use_container_width=True)

    with c2:
        st.markdown('<div class="section-header">Top 5 Products by Gross Profit</div>', unsafe_allow_html=True)
        top5 = prod_df.nlargest(5,'Total_Profit')[['Product Name','Total_Profit','Gross Margin (%)']].copy()
        top5['Short Name'] = top5['Product Name'].str.replace('Wonka Bar - ','',regex=False).str.replace('Wonka Bar -','',regex=False)
        fig4 = px.bar(top5, x='Total_Profit', y='Short Name', orientation='h',
                      color='Gross Margin (%)', color_continuous_scale='Viridis',
                      text='Total_Profit')
        fig4.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
        fig4.update_layout(**CHART_LAYOUT, height=320, coloraxis_showscale=False,
                           yaxis=dict(autorange='reversed'))
        st.plotly_chart(fig4, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  MODULE 2 – PRODUCT PROFITABILITY
# ══════════════════════════════════════════════════════════════════════════════
elif module == "🏆 Product Profitability":
    st.markdown("## 🏆 Product Profitability Analysis")
    st.divider()

    prod_sorted = prod_df.sort_values('Total_Profit', ascending=False).reset_index(drop=True)
    prod_sorted['Rank'] = prod_sorted.index + 1

    # Margin leaderboard bar chart
    st.markdown('<div class="section-header">Gross Margin Leaderboard</div>', unsafe_allow_html=True)
    prod_m = prod_df.sort_values('Gross Margin (%)', ascending=True)
    prod_m['Short'] = prod_m['Product Name'].str.replace('Wonka Bar - ','',regex=False).str.replace('Wonka Bar -','',regex=False)
    colors_bar = ['#ff4444' if m < 50 else '#ffaa00' if m < 65 else '#00cc88' for m in prod_m['Gross Margin (%)']]
    fig = go.Figure(go.Bar(
        x=prod_m['Gross Margin (%)'], y=prod_m['Short'], orientation='h',
        marker_color=colors_bar, text=prod_m['Gross Margin (%)'].round(1),
        texttemplate='%{text}%', textposition='outside'
    ))
    fig.add_vline(x=65, line_dash='dash', line_color='#6677ff', annotation_text='Avg 65%')
    fig.update_layout(**CHART_LAYOUT, height=420, title='Gross Margin % by Product',
                      xaxis_title='Gross Margin (%)', yaxis_title='')
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-header">Profit Contribution (%)</div>', unsafe_allow_html=True)
        fig2 = px.treemap(prod_df, path=['Division','Product Name'],
                          values='Total_Profit', color='Gross Margin (%)',
                          color_continuous_scale='RdYlGn',
                          color_continuous_midpoint=65)
        fig2.update_layout(**CHART_LAYOUT, height=380)
        st.plotly_chart(fig2, use_container_width=True)

    with c2:
        st.markdown('<div class="section-header">Revenue vs Profit Bubble</div>', unsafe_allow_html=True)
        prod_df['Short'] = prod_df['Product Name'].str.replace('Wonka Bar - ','',regex=False).str.replace('Wonka Bar -','',regex=False)
        fig3 = px.scatter(prod_df, x='Total_Sales', y='Total_Profit',
                          size='Total_Units', color='Division',
                          hover_name='Product Name', text='Short',
                          color_discrete_map=COLORS,
                          size_max=50)
        fig3.update_traces(textposition='top center', textfont_size=9)
        fig3.update_layout(**CHART_LAYOUT, height=380, title='Revenue vs Profit (bubble=units)')
        st.plotly_chart(fig3, use_container_width=True)

    # Product table
    st.markdown('<div class="section-header">📋 Full Product Leaderboard</div>', unsafe_allow_html=True)
    tbl = prod_sorted[['Rank','Product Name','Division','Factory',
                        'Total_Sales','Total_Profit','Gross Margin (%)','Profit per Unit',
                        'Revenue Contribution (%)','Profit Contribution (%)','Orders']].copy()
    tbl.columns = ['#','Product','Division','Factory','Revenue','Profit','Margin %','$/Unit','Rev %','Profit %','Orders']
    for col in ['Revenue','Profit']:
        tbl[col] = tbl[col].map('${:,.2f}'.format)
    for col in ['Margin %','Rev %','Profit %']:
        tbl[col] = tbl[col].map('{:.1f}%'.format)
    tbl['$/Unit'] = tbl['$/Unit'].map('${:.2f}'.format)
    st.dataframe(tbl, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
#  MODULE 3 – DIVISION PERFORMANCE
# ══════════════════════════════════════════════════════════════════════════════
elif module == "🏭 Division Performance":
    st.markdown("## 🏭 Division Performance Dashboard")
    st.divider()

    c1, c2, c3 = st.columns(3)
    for col, (_, row) in zip([c1,c2,c3], div_df.iterrows()):
        col.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{'🍫' if row['Division']=='Chocolate' else '🍭' if row['Division']=='Sugar' else '🎪'} {row['Division']}</div>
            <div class="metric-value">{row['Gross Margin (%)']:.1f}%</div>
            <div class="metric-sub">Revenue: ${row['Total_Sales']:,.0f} | Profit: ${row['Total_Profit']:,.0f}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="section-header">Revenue vs Profit vs Cost</div>', unsafe_allow_html=True)
        fig = go.Figure()
        metrics = ['Total_Sales','Total_Profit','Total_Cost']
        names   = ['Revenue','Profit','Cost']
        colors  = ['#6677ff','#00cc88','#ff4466']
        for m, n, c in zip(metrics, names, colors):
            fig.add_trace(go.Bar(name=n, x=div_df['Division'], y=div_df[m], marker_color=c))
        fig.update_layout(**CHART_LAYOUT, barmode='group', height=360,
                          title='Division Financial Breakdown')
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown('<div class="section-header">Margin Distribution by Division</div>', unsafe_allow_html=True)
        fig2 = px.box(df, x='Division', y='Gross Margin (%)',
                      color='Division', color_discrete_map=COLORS,
                      points='outliers')
        fig2.update_layout(**CHART_LAYOUT, height=360, title='Margin Spread per Division',
                           showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    # Region breakdown
    st.markdown('<div class="section-header">Regional Performance by Division</div>', unsafe_allow_html=True)
    reg_div = df.groupby(['Region','Division']).agg(
        Revenue=('Sales','sum'), Profit=('Gross Profit','sum')
    ).reset_index()
    reg_div['Margin'] = reg_div['Profit'] / reg_div['Revenue'] * 100
    c1, c2 = st.columns(2)
    with c1:
        fig3 = px.bar(reg_div, x='Region', y='Revenue', color='Division',
                      color_discrete_map=COLORS, barmode='group',
                      title='Revenue by Region & Division')
        fig3.update_layout(**CHART_LAYOUT, height=340)
        st.plotly_chart(fig3, use_container_width=True)
    with c2:
        fig4 = px.bar(reg_div, x='Region', y='Margin', color='Division',
                      color_discrete_map=COLORS, barmode='group',
                      title='Gross Margin % by Region & Division')
        fig4.update_layout(**CHART_LAYOUT, height=340)
        st.plotly_chart(fig4, use_container_width=True)

    # Factory performance
    st.markdown('<div class="section-header">Factory-Level Profitability</div>', unsafe_allow_html=True)
    fac = df.groupby('Factory').agg(
        Revenue=('Sales','sum'), Profit=('Gross Profit','sum'),
        Units=('Units','sum'), Orders=('Row ID','count')
    ).reset_index()
    fac['Margin'] = fac['Profit'] / fac['Revenue'] * 100
    fig5 = px.bar(fac, x='Factory', y=['Revenue','Profit'],
                  barmode='group', color_discrete_sequence=['#6677ff','#00cc88'],
                  title='Revenue vs Profit by Factory')
    fig5.update_layout(**CHART_LAYOUT, height=340)
    st.plotly_chart(fig5, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  MODULE 4 – PARETO ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif module == "📈 Pareto Analysis":
    st.markdown("## 📈 Profit Concentration (Pareto) Analysis")
    st.divider()

    prod_p = prod_df.sort_values('Total_Profit', ascending=False).reset_index(drop=True)
    prod_p['Cum_Profit']  = prod_p['Total_Profit'].cumsum()
    prod_p['Cum_Revenue'] = prod_p['Total_Sales'].cumsum()
    total_p = prod_p['Total_Profit'].sum()
    total_r = prod_p['Total_Sales'].sum()
    prod_p['Cum_Profit_Pct']  = prod_p['Cum_Profit']  / total_p * 100
    prod_p['Cum_Revenue_Pct'] = prod_p['Cum_Revenue'] / total_r * 100
    prod_p['Product_Pct']     = (prod_p.index + 1) / len(prod_p) * 100

    # Find 80% lines
    p80_products = prod_p[prod_p['Cum_Profit_Pct'] >= 80].iloc[0]['Product_Pct']
    r80_products = prod_p[prod_p['Cum_Revenue_Pct'] >= 80].iloc[0]['Product_Pct']

    c1, c2, c3 = st.columns(3)
    c1.markdown(f"""<div class="metric-card">
        <div class="metric-label">Products → 80% Profit</div>
        <div class="metric-value">{prod_p[prod_p['Cum_Profit_Pct']<=80].shape[0]+1} of {len(prod_p)}</div>
        <div class="metric-sub">{p80_products:.0f}% of portfolio</div>
    </div>""", unsafe_allow_html=True)
    c2.markdown(f"""<div class="metric-card">
        <div class="metric-label">Products → 80% Revenue</div>
        <div class="metric-value">{prod_p[prod_p['Cum_Revenue_Pct']<=80].shape[0]+1} of {len(prod_p)}</div>
        <div class="metric-sub">{r80_products:.0f}% of portfolio</div>
    </div>""", unsafe_allow_html=True)
    top_div = div_df.nlargest(1,'Total_Profit').iloc[0]
    c3.markdown(f"""<div class="metric-card">
        <div class="metric-label">Top Division Profit Share</div>
        <div class="metric-value">{top_div['Total_Profit']/total_p*100:.1f}%</div>
        <div class="metric-sub">{top_div['Division']}</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="section-header">Profit Pareto Curve</div>', unsafe_allow_html=True)
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=prod_p['Product Name'].str[:20], y=prod_p['Total_Profit'],
                             name='Profit', marker_color='#6677ff'), secondary_y=False)
        fig.add_trace(go.Scatter(x=prod_p['Product Name'].str[:20], y=prod_p['Cum_Profit_Pct'],
                                 name='Cumulative %', line=dict(color='#ff6b9d', width=2.5),
                                 mode='lines+markers'), secondary_y=True)
        fig.add_hline(y=80, line_dash='dash', line_color='#ffaa00',
                      annotation_text='80%', secondary_y=True)
        fig.update_layout(**CHART_LAYOUT, height=400, title='Profit Pareto Analysis')
        fig.update_xaxes(tickangle=45)
        fig.update_yaxes(title_text='Gross Profit ($)', secondary_y=False)
        fig.update_yaxes(title_text='Cumulative Profit (%)', secondary_y=True)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown('<div class="section-header">Revenue Pareto Curve</div>', unsafe_allow_html=True)
        fig2 = make_subplots(specs=[[{"secondary_y": True}]])
        fig2.add_trace(go.Bar(x=prod_p['Product Name'].str[:20], y=prod_p['Total_Sales'],
                              name='Revenue', marker_color='#00cc88'), secondary_y=False)
        fig2.add_trace(go.Scatter(x=prod_p['Product Name'].str[:20], y=prod_p['Cum_Revenue_Pct'],
                                  name='Cumulative %', line=dict(color='#ff6b9d', width=2.5),
                                  mode='lines+markers'), secondary_y=True)
        fig2.add_hline(y=80, line_dash='dash', line_color='#ffaa00', annotation_text='80%', secondary_y=True)
        fig2.update_layout(**CHART_LAYOUT, height=400, title='Revenue Pareto Analysis')
        fig2.update_xaxes(tickangle=45)
        st.plotly_chart(fig2, use_container_width=True)

    # State concentration
    st.markdown('<div class="section-header">Profit Concentration by State (Top 20)</div>', unsafe_allow_html=True)
    state_p = df.groupby('State/Province').agg(Profit=('Gross Profit','sum'), Revenue=('Sales','sum')).reset_index()
    state_p = state_p.sort_values('Profit', ascending=False).head(20)
    state_p['Margin'] = state_p['Profit'] / state_p['Revenue'] * 100
    fig3 = px.bar(state_p, x='State/Province', y='Profit', color='Margin',
                  color_continuous_scale='RdYlGn', color_continuous_midpoint=65,
                  title='Top 20 States by Gross Profit')
    fig3.update_layout(**CHART_LAYOUT, height=360)
    fig3.update_xaxes(tickangle=45)
    st.plotly_chart(fig3, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  MODULE 5 – COST DIAGNOSTICS
# ══════════════════════════════════════════════════════════════════════════════
elif module == "🔬 Cost Diagnostics":
    st.markdown("## 🔬 Cost vs Margin Diagnostics")
    st.divider()

    # Risk flags
    prod_df['Risk'] = 'Low Risk'
    prod_df.loc[prod_df['Gross Margin (%)'] < 50, 'Risk'] = 'High Risk'
    prod_df.loc[(prod_df['Gross Margin (%)'] >= 50) & (prod_df['Gross Margin (%)'] < 60), 'Risk'] = 'Medium Risk'

    risk_counts = prod_df['Risk'].value_counts()
    c1,c2,c3 = st.columns(3)
    for col, (risk, clr, icon) in zip([c1,c2,c3],[
        ('High Risk','#ff4444','⚠️'),
        ('Medium Risk','#ffaa00','🟡'),
        ('Low Risk','#00cc88','✅')
    ]):
        cnt = risk_counts.get(risk, 0)
        col.markdown(f"""<div class="metric-card">
            <div class="metric-label">{icon} {risk}</div>
            <div class="metric-value" style="color:{clr}">{cnt}</div>
            <div class="metric-sub">products</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="section-header">Cost vs Sales Scatter</div>', unsafe_allow_html=True)
        color_map = {'High Risk':'#ff4444','Medium Risk':'#ffaa00','Low Risk':'#00cc88'}
        prod_df['Short'] = prod_df['Product Name'].str.replace('Wonka Bar - ','',regex=False).str.replace('Wonka Bar -','',regex=False)
        fig = px.scatter(prod_df, x='Total_Cost', y='Total_Sales',
                         color='Risk', color_discrete_map=color_map,
                         size='Total_Units', hover_name='Product Name',
                         text='Short', size_max=50,
                         title='Cost vs Revenue (color = margin risk)')
        # Perfect margin line
        mx = prod_df['Total_Cost'].max()
        fig.add_trace(go.Scatter(x=[0, mx], y=[0, mx], mode='lines',
                                 line=dict(dash='dash', color='#888888', width=1),
                                 name='Break-even', showlegend=True))
        fig.update_traces(textposition='top center', textfont_size=8, selector=dict(mode='markers+text'))
        fig.update_layout(**CHART_LAYOUT, height=400)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown('<div class="section-header">Margin Risk by Product</div>', unsafe_allow_html=True)
        prod_risk = prod_df.sort_values('Gross Margin (%)')
        fig2 = px.bar(prod_risk, x='Gross Margin (%)', y='Short', orientation='h',
                      color='Risk', color_discrete_map=color_map,
                      title='Products Ranked by Margin Risk')
        fig2.add_vline(x=50, line_dash='dot', line_color='#ff4444', annotation_text='50% threshold')
        fig2.add_vline(x=60, line_dash='dot', line_color='#ffaa00', annotation_text='60% threshold')
        fig2.update_layout(**CHART_LAYOUT, height=400)
        st.plotly_chart(fig2, use_container_width=True)

    # Cost efficiency table
    st.markdown('<div class="section-header">🚨 Margin Risk Flags & Recommendations</div>', unsafe_allow_html=True)
    risk_tbl = prod_df[['Product Name','Division','Factory','Total_Sales','Total_Cost',
                         'Total_Profit','Gross Margin (%)','Profit per Unit','Risk']].copy()
    risk_tbl = risk_tbl.sort_values('Gross Margin (%)')
    risk_tbl['Action'] = risk_tbl.apply(lambda r:
        '❌ Discontinue / Reprice' if r['Risk'] == 'High Risk' else
        '⚠️ Cost Renegotiation' if r['Risk'] == 'Medium Risk' else
        '✅ Maintain', axis=1)
    for col in ['Total_Sales','Total_Cost','Total_Profit']:
        risk_tbl[col] = risk_tbl[col].map('${:,.2f}'.format)
    risk_tbl['Gross Margin (%)'] = risk_tbl['Gross Margin (%)'].map('{:.1f}%'.format)
    risk_tbl['Profit per Unit']  = risk_tbl['Profit per Unit'].map('${:.2f}'.format)
    risk_tbl.columns = ['Product','Division','Factory','Revenue','Cost','Profit','Margin %','$/Unit','Risk','Action']
    st.dataframe(risk_tbl, use_container_width=True, hide_index=True)

    # Cost structure by division
    st.markdown('<div class="section-header">Cost Structure by Division</div>', unsafe_allow_html=True)
    div_cost = df.groupby('Division').agg(
        Revenue=('Sales','sum'), Cost=('Cost','sum'), Profit=('Gross Profit','sum')
    ).reset_index()
    div_cost_melted = div_cost.melt(id_vars='Division', value_vars=['Cost','Profit'],
                                     var_name='Component', value_name='Amount')
    fig3 = px.bar(div_cost_melted, x='Division', y='Amount', color='Component',
                  barmode='stack', color_discrete_map={'Cost':'#ff4466','Profit':'#00cc88'},
                  title='Cost vs Profit Composition by Division')
    fig3.update_layout(**CHART_LAYOUT, height=340)
    st.plotly_chart(fig3, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  MODULE 6 – TREND ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif module == "📅 Trend Analysis":
    st.markdown("## 📅 Trend & Time Analysis")
    st.divider()

    # Monthly margin trend
    monthly = df.groupby(['Month','Division']).agg(
        Revenue=('Sales','sum'), Profit=('Gross Profit','sum')
    ).reset_index()
    monthly['Margin'] = monthly['Profit'] / monthly['Revenue'] * 100

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-header">Monthly Margin Trend by Division</div>', unsafe_allow_html=True)
        fig = px.line(monthly, x='Month', y='Margin', color='Division',
                      color_discrete_map=COLORS, markers=True,
                      title='Monthly Gross Margin % by Division')
        fig.update_layout(**CHART_LAYOUT, height=360)
        fig.update_xaxes(tickangle=45, nticks=12)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown('<div class="section-header">Monthly Revenue by Division</div>', unsafe_allow_html=True)
        fig2 = px.area(monthly, x='Month', y='Revenue', color='Division',
                       color_discrete_map=COLORS, title='Monthly Revenue by Division')
        fig2.update_layout(**CHART_LAYOUT, height=360)
        fig2.update_xaxes(tickangle=45, nticks=12)
        st.plotly_chart(fig2, use_container_width=True)

    # Ship mode analysis
    st.markdown('<div class="section-header">Profitability by Ship Mode</div>', unsafe_allow_html=True)
    ship = df.groupby('Ship Mode').agg(
        Revenue=('Sales','sum'), Profit=('Gross Profit','sum'),
        Orders=('Row ID','count'), Units=('Units','sum')
    ).reset_index()
    ship['Margin'] = ship['Profit'] / ship['Revenue'] * 100
    c1, c2 = st.columns(2)
    with c1:
        fig3 = px.bar(ship, x='Ship Mode', y=['Revenue','Profit'],
                      barmode='group', color_discrete_sequence=['#6677ff','#00cc88'],
                      title='Revenue vs Profit by Ship Mode')
        fig3.update_layout(**CHART_LAYOUT, height=320)
        st.plotly_chart(fig3, use_container_width=True)
    with c2:
        fig4 = px.bar(ship, x='Ship Mode', y='Margin',
                      color='Margin', color_continuous_scale='RdYlGn',
                      color_continuous_midpoint=65,
                      title='Gross Margin % by Ship Mode')
        fig4.update_layout(**CHART_LAYOUT, height=320, coloraxis_showscale=False)
        st.plotly_chart(fig4, use_container_width=True)

    # Yearly comparison
    if df['Year'].nunique() > 1:
        st.markdown('<div class="section-header">Year-over-Year Comparison</div>', unsafe_allow_html=True)
        yearly = df.groupby(['Year','Division']).agg(
            Revenue=('Sales','sum'), Profit=('Gross Profit','sum')
        ).reset_index()
        yearly['Margin'] = yearly['Profit'] / yearly['Revenue'] * 100
        c1, c2 = st.columns(2)
        with c1:
            fig5 = px.bar(yearly, x='Year', y='Profit', color='Division',
                          color_discrete_map=COLORS, barmode='group',
                          title='YoY Gross Profit by Division')
            fig5.update_layout(**CHART_LAYOUT, height=320)
            st.plotly_chart(fig5, use_container_width=True)
        with c2:
            fig6 = px.bar(yearly, x='Year', y='Margin', color='Division',
                          color_discrete_map=COLORS, barmode='group',
                          title='YoY Gross Margin % by Division')
            fig6.update_layout(**CHART_LAYOUT, height=320)
            st.plotly_chart(fig6, use_container_width=True)

# ─── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#555577;font-size:12px;'>"
    "Nassau Candy Distributor · Product Line Profitability & Margin Performance Analysis · "
    "Built with Streamlit & Plotly"
    "</div>",
    unsafe_allow_html=True
)
