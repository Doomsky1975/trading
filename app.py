import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# CONFIGURATION DE L'APPLI (Look Mobile)
st.set_page_config(page_title="IA Trading Master", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    div[data-testid="stMetricValue"] { font-size: 1.8rem; color: #00ff00; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 IA TRADING MASTER")
st.caption("Signaux Haute Probabilité & Gestion du Risque")

# --- BARRE LATÉRALE (Paramètres) ---
st.sidebar.header("Configuration")
symbol = st.sidebar.text_input("Actif (ex: BTC-USD, EURUSD=X)", "BTC-USD")
timeframe = st.sidebar.selectbox("Unité de temps", ["1m", "5m", "15m", "1h"], index=1)
risk_per_trade = st.sidebar.slider("Risque par trade (%)", 0.1, 5.0, 1.0)
capital = st.sidebar.number_input("Capital ($)", value=1000)

# --- MOTEUR DE DONNÉES IA ---
df = yf.download(symbol, period="1d", interval=timeframe).tail(100)

if not df.empty:
    # Indicateurs IA
    df['EMA_9'] = ta.ema(df['Close'], length=9)
    df['EMA_21'] = ta.ema(df['Close'], length=21)
    df['RSI'] = ta.rsi(df['Close'], length=14)
    
    last_price = df['Close'].iloc[-1]
    prev_close = df['Close'].iloc[-2]
    rsi_val = df['RSI'].iloc[-1]
    
    # LOGIQUE DE SIGNAL (Filtre IA 85%)
    buy_cond = (df['EMA_9'].iloc[-1] > df['EMA_21'].iloc[-1]) and (rsi_val < 65)
    sell_cond = (df['EMA_9'].iloc[-1] < df['EMA_21'].iloc[-1]) and (rsi_val > 35)
    
    # LOGIQUE "TROP TARD"
    move_pct = abs(last_price - prev_close) / prev_close * 100
    is_too_late = move_pct > 0.15  # Trop tard si le prix a bougé de +0.15% en 1 bougie

    # --- AFFICHAGE DES SIGNAUX ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Prix Actuel", f"${last_price:,.2f}")
        
    with col2:
        if is_too_late:
            st.warning("⚠️ SIGNAL EXPIRÉ (Trop tard pour entrer)")
        elif buy_cond:
            st.success("🚀 SIGNAL : ACHAT FORT")
        elif sell_cond:
            st.error("📉 SIGNAL : VENTE FORTE")
        else:
            st.info("⌛ ANALYSE : Attente de confirmation...")

    # --- GESTION DU RISQUE (Tout-en-un) ---
    st.write("---")
    st.subheader("🛠️ Plan de Trade IA")
    
    if (buy_cond or sell_cond) and not is_too_late:
        # Calcul des paliers
        stop_loss = last_price * 0.995 if buy_cond else last_price * 1.005
        take_profit = last_price * 1.01 if buy_cond else last_price * 0.99
        risk_amount = capital * (risk_per_trade / 100)
        position_size = risk_amount / abs(last_price - stop_loss)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("STOP LOSS", f"{stop_loss:,.2f}")
        c2.metric("TAKE PROFIT", f"{take_profit:,.2f}")
        c3.metric("TAILLE POSITION", f"{position_size:.4f}")
    else:
        st.write("Aucun trade actif. En attente d'une opportunité à haute probabilité.")

    # Graphique Interactif
    fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
    fig.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("Erreur de connexion aux marchés.")
