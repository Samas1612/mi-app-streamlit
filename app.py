import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# --- Título ---
st.set_page_config(page_title="Analítica de Datos", layout="wide")
st.title("📊 Dashboard de Analítica de Datos")

# --- Subida de archivo ---
st.sidebar.header("📁 Carga tu archivo CSV")
file = st.sidebar.file_uploader("Selecciona un archivo CSV", type=["csv"])

if file is not None:
    # Leer datos
    df = pd.read_csv(file)
    st.subheader("Vista previa de los datos")
    st.dataframe(df.head())

    # --- Información básica ---
    st.subheader("📋 Información general del dataset")
    st.write(f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}")
    st.write("Columnas:", list(df.columns))

    # --- Estadísticas descriptivas ---
    st.subheader("📈 Estadísticas descriptivas")
    st.write(df.describe(include='all'))

    # --- Selección de columnas para análisis ---
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=['number']).columns.tolist()

    # --- Gráfico interactivo ---
    st.subheader("📊 Gráfico interactivo (Plotly)")
    if len(numeric_cols) >= 2:
        x_col = st.selectbox("Eje X:", numeric_cols)
        y_col = st.selectbox("Eje Y:", numeric_cols, index=1)
        fig = px.scatter(df, x=x_col, y=y_col, title=f"Relación entre {x_col} y {y_col}")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Sube un dataset con al menos dos columnas numéricas para ver el gráfico.")

    # --- Mapa de calor de correlación ---
    st.subheader("🔥 Mapa de calor de correlación (solo variables numéricas)")
    numeric_df = df.select_dtypes(include=['number'])

    if not numeric_df.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)
    else:
        st.warning("No hay columnas numéricas para mostrar correlaciones.")
else:
    st.info("👈 Sube un archivo CSV para comenzar el análisis.")
