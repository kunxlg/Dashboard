
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import calendar

# ----------------------------
# CONSTANTS
# ----------------------------
CAPITAL = 20000
LEVERAGE = 5
EXPOSURE = CAPITAL * LEVERAGE
TARGET_PERCENT = 5
MONTHLY_TARGET = EXPOSURE * TARGET_PERCENT / 100
today = datetime.today()
current_month = today.strftime("%Y-%m")

# ----------------------------
# SESSION STATE INIT
# ----------------------------
if 'daily_data' not in st.session_state:
    st.session_state.daily_data = []

# ----------------------------
# CUSTOM CSS (Sci-Fi Look)
# ----------------------------
st.set_page_config(layout="wide", page_title="Sci-Fi Trading Dashboard")

st.markdown(
    """
    <style>
    html, body, [class*="css"]  {
        background-color: #0d1117;
        color: #39ff14;
        font-family: 'Courier New', monospace;
    }
    .block-container {
        padding-top: 2rem;
    }
    .metric-box {
        background: rgba(0, 255, 170, 0.07);
        border: 1px solid #00ffe1;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 0 10px #00ffe1;
        text-align: center;
    }
    .metric-box h1 {
        font-size: 2rem;
        color: #00ffe1;
    }
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #00f260 , #0575e6);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# HEADER
# ----------------------------
st.markdown("<h1 style='text-align:center; color:#00ffe1;'>🧠 Sci-Fi Trading Performance HUD</h1>", unsafe_allow_html=True)

# ----------------------------
# INPUT PANEL
# ----------------------------
with st.sidebar:
    st.markdown("## 📆 Enter Daily P&L")
    date_input = st.date_input("Date", value=today)
    pl_input = st.number_input("Profit/Loss (₹)", step=100.0, format="%.2f", value=0.0)
    if st.button("Add Entry"):
        st.session_state.daily_data.append({"date": date_input.strftime("%Y-%m-%d"), "pnl": pl_input})

# ----------------------------
# DATA PROCESSING
# ----------------------------
df = pd.DataFrame(st.session_state.daily_data)
if not df.empty:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])
    df['month'] = df['date'].dt.to_period("M")
    df = df.sort_values(by='date')
    month_df = df[df['date'].dt.strftime("%Y-%m") == current_month]
else:
    df = pd.DataFrame(columns=['date', 'pnl', 'month'])
    month_df = df

# ----------------------------
# CALCULATIONS
# ----------------------------
total_pnl = month_df['pnl'].sum() if not month_df.empty else 0
progress_percent = min(100, (total_pnl / MONTHLY_TARGET) * 100)
_, last_day = calendar.monthrange(today.year, today.month)
days_left = last_day - today.day + 1
remaining = MONTHLY_TARGET - total_pnl
daily_needed = remaining / days_left if days_left > 0 else 0

# ----------------------------
# METRIC PANELS
# ----------------------------
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="metric-box"><h1>💼 Capital</h1><h1>₹{:,}</h1></div>'.format(CAPITAL), unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-box"><h1>⚡ Leverage</h1><h1>{}x</h1></div>'.format(LEVERAGE), unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-box"><h1>📊 Exposure</h1><h1>₹{:,}</h1></div>'.format(EXPOSURE), unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)
with col4:
    st.markdown('<div class="metric-box"><h1>🎯 Monthly Target</h1><h1>₹{:,}</h1></div>'.format(int(MONTHLY_TARGET)), unsafe_allow_html=True)
with col5:
    st.markdown('<div class="metric-box"><h1>💹 Current P&L</h1><h1>₹{:,}</h1></div>'.format(int(total_pnl)), unsafe_allow_html=True)
with col6:
    status = "🎉 Target Hit" if remaining <= 0 else f"₹{daily_needed:,.0f}/day"
    st.markdown('<div class="metric-box"><h1>⏳ Days Left</h1><h1>{} | {}</h1></div>'.format(days_left, status), unsafe_allow_html=True)

# ----------------------------
# PROGRESS BAR
# ----------------------------
st.markdown("### 🔋 Target Completion")
st.progress(progress_percent / 100)

# ----------------------------
# VISUALIZATIONS
# ----------------------------
if not month_df.empty:
    st.markdown("### 📊 Daily P&L Chart")
    bar_chart = px.bar(month_df, x='date', y='pnl', labels={'pnl': 'Profit/Loss'}, title='Daily P&L')
    st.plotly_chart(bar_chart, use_container_width=True)

    st.markdown("### 📈 Cumulative P&L Over Time")
    month_df['cumulative'] = month_df['pnl'].cumsum()
    line_chart = px.line(month_df, x='date', y='cumulative', title='Cumulative P&L')
    st.plotly_chart(line_chart, use_container_width=True)

    win_count = (month_df['pnl'] > 0).sum()
    loss_count = (month_df['pnl'] <= 0).sum()
    st.markdown("### 🧩 Win vs Loss Days")
    pie_chart = px.pie(values=[win_count, loss_count], names=['Win', 'Loss'], title='Win/Loss Distribution')
    st.plotly_chart(pie_chart, use_container_width=True)

# ----------------------------
# DATA TABLES
# ----------------------------
st.markdown("### 📋 Daily P&L Entries")
if not month_df.empty:
    st.dataframe(month_df[['date', 'pnl']].rename(columns={'date': 'Date', 'pnl': 'Profit/Loss (₹)'}), use_container_width=True)
else:
    st.write("No entries this month.")

st.markdown("### 🧾 Monthly Summary")
if not df.empty:
    monthly_summary = df.groupby('month')['pnl'].sum().reset_index()
    monthly_summary.columns = ['Month', 'Total P&L']
    monthly_summary['Month'] = monthly_summary['Month'].astype(str)
    summary_chart = px.bar(monthly_summary, x='Month', y='Total P&L', title='Monthly Total P&L')
    st.plotly_chart(summary_chart, use_container_width=True)
else:
    st.write("No data yet.")
