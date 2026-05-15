import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Page Config: Wide Layout ---
st.set_page_config(layout="wide")

# --- Custom CSS to expand tabs evenly ---
st.markdown("""
    <style>
    /* Make tab labels fit across the page */
    .stTabs [role="tablist"] {
        display: flex;
        justify-content: space-between;
    }
    .stTabs [role="tab"] {
        flex: 1;  /* each tab takes equal space */
        text-align: center;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# Load your data
df = pd.read_excel("master_table.csv.xlsx")
summary_df = pd.read_csv("executive_summary.csv")

# --- Clean percentage columns ---
df["LoanGrowth_pct"] = (
    df["LoanGrowth_pct"].astype(str)
    .str.replace("%", "")
    .str.replace("—", "0")
)
df["LoanGrowth_pct"] = pd.to_numeric(df["LoanGrowth_pct"], errors="coerce")

df["NetNPA_pct"] = (
    df["NetNPA_pct"].astype(str)
    .str.replace("%", "")
    .str.replace("—", "0")
)
df["NetNPA_pct"] = pd.to_numeric(df["NetNPA_pct"], errors="coerce")

# --- Add ICICI Bank Logo ---
st.image("icici_logo.png", width=120)  # logo at the top
st.title("ICICI Financial Analysis Dashboard")

# --- KPI Banner with Colors (medium tones) ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        "<div style='background-color:#FF9933;padding:15px;border-radius:8px;text-align:center'>"
        "<h4 style='color:white'>Net Profit (₹ Cr)</h4>"
        "<h2 style='color:white'>51.03</h2>"
        "<p style='color:lightgreen'>+15.3% YoY</p>"
        "</div>", unsafe_allow_html=True
    )

with col2:
    st.markdown(
        "<div style='background-color:#336699;padding:15px;border-radius:8px;text-align:center'>"
        "<h4 style='color:white'>ROA (%)</h4>"
        "<h2 style='color:white'>1.93%</h2>"
        "<p style='color:lightgreen'>+0.06% YoY</p>"
        "</div>", unsafe_allow_html=True
    )

with col3:
    st.markdown(
        "<div style='background-color:#339966;padding:15px;border-radius:8px;text-align:center'>"
        "<h4 style='color:white'>CAR (%)</h4>"
        "<h2 style='color:white'>16.55%</h2>"
        "<p style='color:lightgreen'>+0.22% YoY</p>"
        "</div>", unsafe_allow_html=True
    )

# --- Overview ---
st.markdown("""
### 📊 Overview
This dashboard presents ICICI's financial performance across profitability, lending, risk, capital efficiency, and forecasting.
Use the tabs to explore interactive charts, scenario analysis, and executive summary metrics.
""")

# Tabs (Key Insights removed)
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Profitability", 
    "Digital Lending", 
    "Risk Management", 
    "Capital Efficiency", 
    "Forecasts & Scenarios", 
    "Risk Heatmap", 
    "Executive Summary"
])

# --- Profitability ---
with tab1:
    st.header("Profitability Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("ROA vs ROE Trend")

        # Year filter slider
        year_filter = st.slider(
            "Select Year Range",
            int(df["Year"].min()),
            int(df["Year"].max()),
            (2015, 2025),
            key="year_range_slider"
        )
        filtered = df[(df["Year"] >= year_filter[0]) & (df["Year"] <= year_filter[1])]

        # ✅ Checkbox to toggle labels
        show_labels = st.checkbox("Show Data Labels", value=False, key="labels_toggle")

        fig, ax1 = plt.subplots(figsize=(10,6))

        # ROA line
        ax1.plot(filtered["Year"], filtered["ROA_pct"], color="#1f77b4", marker="o", linewidth=2.5, label="ROA (Return on Assets)")
        ax1.set_xlabel("Year")
        ax1.set_ylabel("ROA (%)", color="#1f77b4")
        ax1.tick_params(axis="y", labelcolor="#1f77b4")

        # ROE line on secondary axis
        ax2 = ax1.twinx()
        ax2.plot(filtered["Year"], filtered["ROE_pct"], color="#ff7f0e", marker="s", linewidth=2.5, label="ROE (Return on Equity)")
        ax2.set_ylabel("ROE (%)", color="#ff7f0e")
        ax2.tick_params(axis="y", labelcolor="#ff7f0e")

        # ✅ Add labels only if checkbox is ticked
        if show_labels:
            for year, roa_val, roe_val in zip(filtered["Year"], filtered["ROA_pct"], filtered["ROE_pct"]):
                ax1.text(year, roa_val + 0.05, f"{roa_val:.2f}%", color="#1f77b4", fontsize=8, ha="center")
                ax2.text(year, roe_val + 0.2, f"{roe_val:.2f}%", color="#ff7f0e", fontsize=8, ha="center")

        # Title, grid, legend
        plt.title("ROA vs ROE Trend", fontsize=14, weight="bold")
        plt.grid(alpha=0.3)
        fig.tight_layout()

        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines + lines2, labels + labels2, loc="upper left")

        st.pyplot(fig, use_container_width=True)

        # ✅ Insights directly below chart
        st.caption("""
        📈 ROA shows steady recovery post‑2020 dip, indicating improved asset efficiency.  
        📊 ROE consistently outpaces ROA, reflecting stronger shareholder returns.  
        ⚠️ The 2020 decline highlights vulnerability during stress periods.  
        ✅ Overall upward trend signals resilience and profitability growth.  
        """)

    with col2:
        st.subheader("Supporting Charts")
        st.image("roa_vs_roe_corrected.png", use_container_width=True)
        st.image("NetProfitEvents.png", use_container_width=True)



# --- Digital Lending ---
with tab2:
    st.header("Digital Lending")
    fig, ax = plt.subplots()
    ax.scatter(df["LoanGrowth_pct"], df["NetNPA_pct"], color="orange")
    ax.set_xlabel("Loan Growth %")
    ax.set_ylabel("Net NPA %")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Loan Growth vs Net NPA")
        st.pyplot(fig, use_container_width=True)
    with col2:
        st.subheader("Supporting Charts")
        st.image("LoanGrowth.png", use_container_width=True)
        st.image("NetNPA.png", use_container_width=True)

    st.markdown("""
    **Insights:**
    - 📊 Higher loan growth years correlate with elevated Net NPA risk.  
    - ⚠️ Aggressive lending strategies can compromise asset quality.  
    - ✅ Recent moderation in loan growth has stabilized NPAs.  
    """)

# --- Risk Management ---
with tab3:
    st.header("Risk Management")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Stress Test")
        st.image("StressTest.png", use_container_width=True)

        # ✅ Insights with tight spacing
        st.caption("""
        ⚠️ Stress tests reveal vulnerability in extreme downturn scenarios.  
        📉 Monte Carlo simulations show CAR dipping below thresholds under high‑risk conditions.  
        ✅ Current capital buffers provide resilience in base case.  
        """)

    with col2:
        st.subheader("Monte Carlo & Capital Adequacy")
        st.image("MonteCarlo.png", use_container_width=True)
        st.image("capital_adequacy_chart.png", use_container_width=True)




# --- Capital Efficiency ---
with tab4:
    st.header("Capital Efficiency")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("ROA Recovery")
        st.image("roa_recovery_chart.png", use_container_width=True)
    with col2:
        st.subheader("CAR% Trend")
        st.image("capital_adequacy_chart.png", use_container_width=True)

    st.markdown("""
    **Insights:**
    - 📊 CAR% remains above regulatory minimum, ensuring compliance.  
    - ✅ ROA recovery indicates improved efficiency in asset deployment.  
    - ⚠️ Stress conditions highlight potential capital strain if NPAs rise sharply.  
    """)

# --- Forecasts & Scenarios ---
with tab5:
    st.header("Forecasts & Scenarios")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Confidence Level Forecast")
        st.image("forecast_net_profit_arima.png", use_container_width=True)

        # ✅ Insights with tight spacing
        st.caption("""
        📈 Net Profit forecast shows steady growth across scenarios.  
        ⚠️ Pessimistic scenario highlights profitability erosion under rising NPAs.  
        ✅ Optimistic lending growth with controlled NPAs sustains stable CAR levels.  
        """)

    with col2:
        st.subheader("Scenario Selector")
        scenario = st.selectbox("Choose Scenario", ["Base", "Optimistic", "Pessimistic"], key="scenario_forecast")
        if scenario == "Base":
            st.image("forecast_net_profit_scenario.png", use_container_width=True)
            st.image("forecast_car_scenario.png", use_container_width=True)
        elif scenario == "Optimistic":
            st.image("forecast_net_profit_scenario.png", use_container_width=True)
        else:
            st.image("forecast_net_profit_scenario.png", use_container_width=True)


# --- Risk Heatmap ---
with tab6:
    st.header("Risk Heatmap")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Heatmap")
        st.image("risk_heatmap.png", use_container_width=True)

    with col2:
        st.subheader("Insights")
        st.markdown("""
        ⚠️ Net Profit is sensitive to NPA increases; heatmap highlights risk zones.  
        📊 Higher loan growth correlates with elevated risk exposure.  
        🔍 Stress scenarios show CAR dipping below regulatory thresholds in extreme cases.  
        🛡️ Diversification across lending segments reduces concentration risk.  
        📉 Pessimistic scenarios reveal profitability erosion when NPAs rise sharply.  
        ✅ Optimistic lending growth with controlled NPAs sustains stable CAR levels.  
        🔔 Monitoring early warning signals (like rising NPAs) can help mitigate risks.  
        """)

# --- Executive Summary ---
with tab7:
    st.header("Executive Summary Metrics")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Avg ROA", f"{summary_df.loc[0,'Value']}")
    col2.metric("Avg ROE", f"{summary_df.loc[1,'Value']}")
    col3.metric("Worst-case Profit", f"{summary_df.loc[2,'Value']}")
    col4.metric("Forecasted CAR% 2030", f"{summary_df.loc[3,'Value']}")

    st.table(summary_df)

    # Add download button
    csv_data = summary_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Executive Summary (CSV)",
        data=csv_data,
        file_name="executive_summary.csv",
        mime="text/csv"
    )
