import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Analizador de ATH", layout="wide")
st.title("📊 Análisis de Distancia al Máximo (200 Ruedas)")

def color_distancia(val):
    abs_val = abs(val)
    if abs_val <= 10: color = '#FFD580'
    elif abs_val <= 20: color = '#FFB7B2'
    else: color = '#D1A7A7'
    return f'background-color: {color}; color: black'

st.sidebar.header("Configuración")
tickers_default = "SPY, KSA, INDY, VEA, EWZ, GLD"
tickers_input = st.sidebar.text_area("Introduce los tickers:", tickers_default)

if st.sidebar.button("Ejecutar Análisis"):
    tickers = [t.strip().upper() for t in tickers_input.split(',') if t.strip()]
    resultados = []

    with st.spinner('Consultando Yahoo Finance...'):
        for ticker in tickers:
            try:
                data = yf.download(ticker, period="1y", progress=False, auto_adjust=True)
                if not data.empty:
                    if isinstance(data.columns, pd.MultiIndex):
                        data.columns = data.columns.get_level_values(0)

                    df_200 = data.iloc[-200:]
                    precio_actual = float(df_200['Close'].iloc[-1])
                    ath_200 = float(df_200['High'].max())
                    distancia_pct = ((precio_actual - ath_200) / ath_200) * 100

                    resultados.append({
                        "Ticker": ticker,
                        "Precio Actual": precio_actual,
                        "Precio ATH": ath_200,
                        "Distancia %": distancia_pct,
                        "Data": df_200
                    })
            except Exception as e:
                st.error(f"Error en {ticker}: {e}")

    if resultados:
        df_resultado = pd.DataFrame([{k: v for k, v in r.items() if k != 'Data'} for r in resultados])
        styled_df = df_resultado.style.map(color_distancia, subset=['Distancia %'])\
            .format({"Precio Actual": "{:.2f}", "Precio ATH": "{:.2f}", "Distancia %": "{:.2f}%"})

        st.subheader("Resumen de Activos")
        st.dataframe(styled_df, use_container_width=True)

        st.subheader("Gráficos Interactivos")
        for res in resultados:
            with st.expander(f"Gráfico de {res['Ticker']}"):
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=res['Data'].index, y=res['Data']['Close'], name='Precio'))
                fig.add_hline(y=res['Precio ATH'], line_dash="dash", line_color="red", annotation_text="ATH 200")
                fig.update_layout(title=f"Evolución {res['Ticker']}", xaxis_title="Fecha", yaxis_title="Precio")
                st.plotly_chart(fig, use_container_width=True)
