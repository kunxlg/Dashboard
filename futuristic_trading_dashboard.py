import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt

st.set_page_config(layout="wide")
st.markdown("""
    <style>
    .main {background-color: #0f0f0f; color: #00ffe1;}
    h1, h2, h3, h4 {color: #00ffe1;}
    .st-df th {background-color: #111; color: #00ffe1;}
    .st-df td {background-color: #0f0f0f; color: #00ffe1;}
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Futuristic Trading Dashboard")

# --- Sidebar Input ---
st.sidebar.header("Enter Trade Details")
date = st.sidebar.date_input("Trade Date", value=dt.date.today())
stock = st.sidebar.text_input("Stock Symbol")
entry = st.sidebar.number_input("Entry Price", min_value=0.0)
exit = st.sidebar.number_input("Exit Price", min_value=0.0)
qty = st.sidebar.number_input("Quantity", min_value=1, value=1)
note = st.sidebar.text_input("Notes")

if 'trades' not in st.session_state:
    st.session_state.trades = []

if st.sidebar.button("Add Trade"):
    pnl = (exit - entry) * qty
    leverage = 5
    exposure = entry * qty * leverage
    st.session_state.trades.append({
        'Date': date,
        'Stock': stock,
        'Entry': entry,
        'Exit': exit,
        'Quantity': qty,
        'P&L': pnl,
        'Exposure': exposure,
        'Note': note
    })

# --- Convert to DataFrame ---
df = pd.DataFrame(st.session_state.trades)

if not df.empty:
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M')
    total_pnl = df['P&L'].sum()
    win_rate = (df['P&L'] > 0).mean() * 100
    avg_daily_return = df.groupby('Date')['P&L'].sum().mean()
    best_trade = df['P&L'].max()
    worst_trade = df['P&L'].min()
    peak = df['P&L'].cumsum().cummax()
    drawdown = ((df['P&L'].cumsum() - peak).min())

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Total P&L", f"₹{total_pnl:,.2f}")
        st.metric("🔥 Win Rate", f"{win_rate:.2f}%")
    with col2:
        st.metric("📈 Avg Daily Return", f"₹{avg_daily_return:.2f}")
        st.metric("💥 Best Trade", f"₹{best_trade:.2f}")
    with col3:
        st.metric("😞 Worst Trade", f"₹{worst_trade:.2f}")
        st.metric("📉 Max Drawdown", f"₹{drawdown:.2f}")

    # --- Charts ---
    st.subheader("📅 Monthly P&L")
    monthly = df.groupby('Month')['P&L'].sum()
    st.bar_chart(monthly)

    st.subheader("📈 Cumulative Capital Growth")
    cumulative = df['P&L'].cumsum() + 40000
    st.line_chart(cumulative)

    st.subheader("📋 Trade Log")
    st.dataframe(df.style.format({"P&L": "₹{:.2f}", "Exposure": "₹{:.2f}"}))

    # --- Alerts ---
    if drawdown < -5000:
        st.error("⚠️ Alert: Major Drawdown Detected!")
    if win_rate < 50:
        st.warning("⚠️ Warning: Win Rate Below 50%")
else:
    st.info("No trades added yet. Use the sidebar to input trades.")
