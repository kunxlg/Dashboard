import streamlit as st
import pandas as pd
from datetime import datetime
import calendar

# Constants
CAPITAL = 20000
LEVERAGE = 5
EXPOSURE = CAPITAL * LEVERAGE
TARGET_PERCENT = 5
MONTHLY_TARGET = EXPOSURE * TARGET_PERCENT / 100

# Initialize session state
if 'daily_data' not in st.session_state:
    st.session_state.daily_data = []

# UI Style
st.set_page_config(layout="wide", page_title="Performance Tracker", page_icon="📊")
st.markdown(
    """
    <style>
        body {
            background-color: #0f1117;
            color: #f0f0f0;
        }
        .stProgress > div > div > div > div {
            background-image: linear-gradient(to right, #00f260 , #0575e6);
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🚀 Trading Performance Tracker")

# Input Section
with st.sidebar:
    st.subheader("📆 Enter Daily P&L")
    date_input = st.date_input("Date", value=datetime.today())
    pl_input = st.number_input("Profit/Loss (₹)", step=100, format="%.2f")
    if st.button("Add Entry"):
        st.session_state.daily_data.append({"date": date_input.strftime("%Y-%m-%d"), "pnl": pl_input})

# Prepare Data
df = pd.DataFrame(st.session_state.daily_data)

if not df.empty:
    # Safely convert to datetime, drop invalid rows
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])
    df = df.sort_values(by='date')
    df['month'] = df['date'].dt.to_period("M")
else:
    df = pd.DataFrame(columns=['date', 'pnl', 'month'])

current_month = datetime.today().strftime("%Y-%m")
month_df = df[df['date'].dt.strftime("%Y-%m") == current_month]

total_pnl = month_df['pnl'].sum() if not month_df.empty else 0
progress_percent = min(100, (total_pnl / MONTHLY_TARGET) * 100)

# Days left this month
today = datetime.today()
_, last_day = calendar.monthrange(today.year, today.month)
days_left = last_day - today.day + 1

# Metrics Row
col1, col2, col3, col4 = st.columns(4)
col1.metric("🎯 Monthly Target", f"₹{MONTHLY_TARGET:,.0f}")
col2.metric("📊 Current P&L", f"₹{total_pnl:,.0f}")
col3.metric("📅 Days Left", f"{days_left} days")
remaining = MONTHLY_TARGET - total_pnl
daily_needed = remaining / days_left if days_left > 0 else 0
col4.metric("🔥 Needed / Day", f"₹{daily_needed:,.0f}" if remaining > 0 else "🎉 Target Hit")

# Progress Bar
st.markdown("### 🚦 Progress Toward Target")
st.progress(progress_percent / 100)

# Daily Table
st.markdown("### 📋 Daily Performance")
st.dataframe(month_df[['date', 'pnl']].rename(columns={'date': 'Date', 'pnl': 'Profit/Loss (₹)'}), use_container_width=True)

# Monthly Summary
monthly_summary = df.groupby('month')['pnl'].sum().reset_index()
monthly_summary.columns = ['Month', 'Total P&L']
monthly_summary['Month'] = monthly_summary['Month'].astype(str)

st.markdown("### 📆 Monthly Summary")
st.table(monthly_summary)
import streamlit as st
import pandas as pd
from datetime import datetime
import calendar

# Constants
CAPITAL = 20000
LEVERAGE = 5
EXPOSURE = CAPITAL * LEVERAGE
TARGET_PERCENT = 5
MONTHLY_TARGET = EXPOSURE * TARGET_PERCENT / 100

# Initialize session state
if 'daily_data' not in st.session_state:
    st.session_state.daily_data = []

# UI Style
st.set_page_config(layout="wide", page_title="Performance Tracker", page_icon="📊")
st.markdown(
    """
    <style>
        body {
            background-color: #0f1117;
            color: #f0f0f0;
        }
        .stProgress > div > div > div > div {
            background-image: linear-gradient(to right, #00f260 , #0575e6);
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🚀 Trading Performance Tracker")

# Input Section
with st.sidebar:
    st.subheader("📆 Enter Daily P&L")
    date_input = st.date_input("Date", value=datetime.today())
    pl_input = st.number_input("Profit/Loss (₹)", step=100, format="%.2f")
    if st.button("Add Entry"):
        st.session_state.daily_data.append({"date": date_input.strftime("%Y-%m-%d"), "pnl": pl_input})

# Prepare Data
df = pd.DataFrame(st.session_state.daily_data)

if not df.empty:
    # Safely convert to datetime, drop invalid rows
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])
    df = df.sort_values(by='date')
    df['month'] = df['date'].dt.to_period("M")
else:
    df = pd.DataFrame(columns=['date', 'pnl', 'month'])

current_month = datetime.today().strftime("%Y-%m")
month_df = df[df['date'].dt.strftime("%Y-%m") == current_month]

total_pnl = month_df['pnl'].sum() if not month_df.empty else 0
progress_percent = min(100, (total_pnl / MONTHLY_TARGET) * 100)

# Days left this month
today = datetime.today()
_, last_day = calendar.monthrange(today.year, today.month)
days_left = last_day - today.day + 1

# Metrics Row
col1, col2, col3, col4 = st.columns(4)
col1.metric("🎯 Monthly Target", f"₹{MONTHLY_TARGET:,.0f}")
col2.metric("📊 Current P&L", f"₹{total_pnl:,.0f}")
col3.metric("📅 Days Left", f"{days_left} days")
remaining = MONTHLY_TARGET - total_pnl
daily_needed = remaining / days_left if days_left > 0 else 0
col4.metric("🔥 Needed / Day", f"₹{daily_needed:,.0f}" if remaining > 0 else "🎉 Target Hit")

# Progress Bar
st.markdown("### 🚦 Progress Toward Target")
st.progress(progress_percent / 100)

# Daily Table
st.markdown("### 📋 Daily Performance")
st.dataframe(month_df[['date', 'pnl']].rename(columns={'date': 'Date', 'pnl': 'Profit/Loss (₹)'}), use_container_width=True)

# Monthly Summary
monthly_summary = df.groupby('month')['pnl'].sum().reset_index()
monthly_summary.columns = ['Month', 'Total P&L']
monthly_summary['Month'] = monthly_summary['Month'].astype(str)

st.markdown("### 📆 Monthly Summary")
st.table(monthly_summary)
