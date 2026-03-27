import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Analizador de ATH", layout="wide")
st.title("📊 Análisis de Distancia al Máximo (200 Ruedas)")

def color_distancia(val):
    # Aplicamos tonos pastel según los rangos solicitados
    abs_val = abs(val)
    if abs_val <= 10:
        color = '#FFD580'  # Naranja pastel
    elif abs_val <= 20:
        color = '#FFB7B2'  # Rojo pastel
    else:
        color = '#D1A7A7'  # Bordo pastel
    return f'background-color: {color}; color: black'

# Sidebar para entrada de usuario
st.sidebar.header("Configuración")
tickers_default = "SPY, KSA, INDY, VEA, EWZ, GLD"
tickers_input = st.sidebar.text_area("Introduce los tickers (separados por coma):", tickers_default)

if st.sidebar.button("Ejecutar Análisis"):
    tickers = [t.strip().upper() for t in tickers_input.split(',') if t.strip()]
    resultados = []
    
    with st.spinner('Consultando datos de Yahoo Finance...'):
        for ticker in tickers:
            try:
                # Descargamos 1 año para tener margen de 200 ruedas
                data = yf.download(ticker, period="1y", progress=False)
                if not data.empty:
                    df_200 = data.iloc[-200:]
                    # Extraemos valores escalares
                    precio_actual = float(df_200['Close'].iloc[-1])
                    ath_200 = float(df_200['High'].max())
                    distancia_pct = ((precio_actual - ath_200) / ath_200) * 100
                    
                    resultados.append({
                        "Ticker": ticker,
                        "Precio Actual": round(precio_actual, 2),
                        "Precio ATH": round(ath_200, 2),
                        "Distancia %": round(distancia_pct, 2)
                    })
            except Exception as e:
                st.error(f"Error procesando {ticker}: {e}")

    if resultados:
        df_resultado = pd.DataFrame(resultados)
        
        # Aplicar estilos y formato
        styled_df = df_resultado.style.map(color_distancia, subset=['Distancia %'])\
            .format({"Precio Actual": "{:.2f}", "Precio ATH": "{:.2f}", "Distancia %": "{:.2f}%"})
        
        st.subheader(f"Resultados al {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        st.dataframe(styled_df, use_container_width=True)
    else:
        st.warning("No se encontraron datos para los tickers ingresados.")
else:
    st.info("Configura los tickers en el panel lateral y haz clic en 'Ejecutar Análisis'.")
