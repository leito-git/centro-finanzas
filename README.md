# Analizador de Distancia al ATH (200 Ruedas)

Esta aplicación de Streamlit calcula la distancia porcentual de una lista de activos financieros respecto a su máximo histórico (ATH) de las últimas 200 ruedas bursátiles.

### Características:
- Descarga de datos en tiempo real mediante Yahoo Finance.
- Cálculo automático de ATH de 200 ruedas.
- Tabla interactiva con formato de colores pastel:
    - **Naranja:** Caída 0% - 10%
    - **Rojo:** Caída 10% - 20%
    - **Bordo:** Caída > 20%

### Instalación Local:
1. Clonar el repositorio.
2. Instalar dependencias: `pip install -r requirements.txt`.
3. Ejecutar: `streamlit run app.py`.
