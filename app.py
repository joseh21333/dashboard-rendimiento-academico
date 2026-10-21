import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Rendimiento académico", layout="wide")

df = pd.read_csv("Estudiantes_Limpio.csv")

st.title("Dashboard de rendimiento académico")
st.write("Análisis de las calificaciones de estudiantes")

# Filtros
st.sidebar.header("Filtros")

genero = st.sidebar.multiselect(
    "Selecciona el género",
    df["Genero"].unique(),
    default=list(df["Genero"].unique())
)

preparacion = st.sidebar.multiselect(
    "Preparación para el examen",
    df["Preparacion_examen"].unique(),
    default=list(df["Preparacion_examen"].unique())
)

rango = st.sidebar.slider(
    "Calificación en Matemáticas", 0, 100, (0, 100)
)

datos = df[
    df["Genero"].isin(genero)
    & df["Preparacion_examen"].isin(preparacion)
    & df["Matematicas"].between(rango[0], rango[1])
]

# Indicadores
st.header("Indicadores principales")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Estudiantes", len(datos))
c2.metric("Promedio Matemáticas", f"{datos['Matematicas'].mean():.2f}")
c3.metric("Promedio Lectura", f"{datos['Lectura'].mean():.2f}")
c4.metric("Promedio Escritura", f"{datos['Escritura'].mean():.2f}")

# Gráfica 1
st.header("Promedios por materia")

promedios = datos[["Matematicas", "Lectura", "Escritura"]].mean().reset_index()
promedios.columns = ["Materia", "Promedio"]

fig1 = px.bar(
    promedios,
    x="Materia",
    y="Promedio",
    color="Materia",
    title="Promedio de calificaciones",
    range_y=[0, 100]
)
st.plotly_chart(fig1, use_container_width=True)

# Gráfica 2
st.header("Preparación para el examen")

fig2 = px.box(
    datos,
    x="Preparacion_examen",
    y="Matematicas",
    color="Preparacion_examen",
    title="Calificaciones según preparación"
)
st.plotly_chart(fig2, use_container_width=True)

# Gráfica 3
st.header("Relación entre materias")

fig3 = px.scatter(
    datos,
    x="Matematicas",
    y="Lectura",
    color="Genero",
    title="Matemáticas vs Lectura"
)
st.plotly_chart(fig3, use_container_width=True)

st.header("Tabla de estudiantes")
st.dataframe(datos)
