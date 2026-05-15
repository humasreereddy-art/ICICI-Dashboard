import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Load dataset
df = pd.read_excel("master_table.csv.xlsx")   # or pd.read_csv("master_table.csv")

# 1. Net Profit Trend
fig_profit = px.line(df, x='Year', y='NetProfit_Cr',
                     markers=True, template='plotly_white',
                     title="Net Profit (₹ Cr) Over Time")
fig_profit.update_traces(line=dict(color='green', width=4))
fig_profit.show()

# 2. Loan Growth vs Profit Growth
fig_growth = px.bar(df, x='Year', y='LoanGrowth_pct',
                    template='plotly_white', title="Loan Growth % vs Net Profit Growth %",
                    color_discrete_sequence=['#1f77b4'])
fig_growth.add_scatter(x=df['Year'], y=df['NetProfitGrowth_pct'],
                       mode='lines+markers', name='Net Profit Growth %',
                       line=dict(color='orange', width=3))
fig_growth.show()

# 3. Net NPA % Trend
fig_npa = px.line(df, x='Year', y='NetNPA_pct',
                  markers=True, template='plotly_white',
                  title="Net NPA % Trend")
fig_npa.update_traces(line=dict(color='red', width=4))
fig_npa.show()

# 4. CAR % Gauge
latest_car = df.iloc[-1]['CAR_pct']
fig_car = go.Figure(go.Indicator(
    mode="gauge+number",
    value=latest_car,
    title={'text': "Capital Adequacy Ratio (CAR %)"},
    gauge={'axis': {'range': [0, 25]},
           'bar': {'color': "darkgreen"},
           'steps': [{'range':[0,10],'color':'#ffcccc'},
                     {'range':[10,20],'color':'#ffffcc'},
                     {'range':[20,25],'color':'#ccffcc'}]}
))
fig_car.show()

# 5. Monte Carlo Simulation
simulated = np.random.normal(loc=df['NetProfit_Cr'].mean(),
                             scale=df['NetProfit_Cr'].std(), size=1000)
fig_mc = px.histogram(simulated, nbins=30, template='plotly_white',
                      title="Monte Carlo Simulation: Profit Distribution",
                      color_discrete_sequence=['#17becf'])
fig_mc.add_vline(x=np.percentile(simulated, 5), line_dash="dash", line_color="red", annotation_text="5th %")
fig_mc.add_vline(x=np.median(simulated), line_dash="solid", line_color="black", annotation_text="Median")
fig_mc.add_vline(x=np.percentile(simulated, 95), line_dash="dash", line_color="green", annotation_text="95th %")
fig_mc.show()

# 6. Forecasting (dummy ARIMA data)
fcast_df = pd.DataFrame({
    "Year": [2026, 2027, 2028, 2029, 2030],
    "mean": [55, 63, 72, 82, 93],
    "mean_ci_lower": [50, 58, 67, 77, 88],
    "mean_ci_upper": [60, 68, 77, 87, 98]
})
fig_forecast = px.line(fcast_df, x="Year", y="mean", template='plotly_white',
                       title="Net Profit Forecast (ARIMA)",
                       markers=True, color_discrete_sequence=['purple'])
fig_forecast.add_scatter(x=fcast_df["Year"], y=fcast_df["mean_ci_lower"], mode='lines',
                         line=dict(dash='dot', color='gray'), name='Lower CI')
fig_forecast.add_scatter(x=fcast_df["Year"], y=fcast_df["mean_ci_upper"], mode='lines',
                         line=dict(dash='dot', color='gray'), name='Upper CI')
fig_forecast.show()

# 7. Liquidity Ratios
fig_liq = px.line(df, x='Year', y=['CurrentRatio','QuickRatio'],
                  markers=True, template='plotly_white',
                  title="Liquidity Ratios",
                  color_discrete_sequence=['navy','gold'])
fig_liq.show()

# 8. Efficiency Ratios
fig_eff = px.line(df, x='Year', y=['ROA_pct','ROE_pct'],
                  markers=True, template='plotly_white',
                  title="Efficiency Ratios (ROA vs ROE)",
                  color_discrete_sequence=['#9467bd','#ff7f0e'])
fig_eff.show()

# 9. Net Profit with Key Events
fig_events = px.line(df, x='Year', y='NetProfit_Cr',
                     markers=True, template='plotly_white',
                     title="Net Profit with Key Events",
                     color_discrete_sequence=['#2ca02c'])
if 'KeyEvent' in df.columns:
    for i, row in df.iterrows():
        if pd.notna(row['KeyEvent']) and row['KeyEvent'] != '—':
            fig_events.add_annotation(x=row['Year'], y=row['NetProfit_Cr'],
                                      text=row['KeyEvent'], showarrow=True,
                                      arrowhead=2, bgcolor="yellow")
fig_events.show()
