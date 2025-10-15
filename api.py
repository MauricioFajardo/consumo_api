import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# ================== CONFIGURACIÓN DE LA PÁGINA ==================
st.set_page_config(page_title="Inteligencia Artificial", layout="wide")

st.markdown("""
# 🤖 Inteligencia Artificial
Alumno : *Anthony Fajardo*  
Carrera : *Desarrollo de software*

## 📓 Guía: Consumo de API → Análisis con Pandas → Visualización Interactiva con Plotly
*Fuente de datos:* [https://jsonplaceholder.typicode.com/users](https://jsonplaceholder.typicode.com/users)
---
""")

# ================== CARGAR DATOS DESDE API ==================
API_URL = 'https://jsonplaceholder.typicode.com/users'

with st.spinner('Cargando datos desde la API...'):
    try:
        response = requests.get(API_URL, timeout=20)
        response.raise_for_status()
        users = response.json()
        st.success(f"✅ Datos cargados correctamente ({len(users)} usuarios)")

        # Convertir a DataFrame
        df = pd.DataFrame(users)

        # Extraer datos anidados
        df['city'] = df['address'].apply(lambda x: x.get('city', '') if isinstance(x, dict) else '')
        df['street'] = df['address'].apply(lambda x: x.get('street', '') if isinstance(x, dict) else '')
        df['company_name'] = df['company'].apply(lambda x: x.get('name', '') if isinstance(x, dict) else '')

    except Exception as e:
        st.error(f"❌ Error al cargar datos: {str(e)}")
        st.stop()

# ================== VISTA PREVIA DE DATOS ==================
st.header("📋 Vista Previa de Datos")
df_simple = df[['id', 'name', 'username', 'email', 'phone', 'website', 'city', 'company_name']]
st.dataframe(df_simple, use_container_width=True)

st.markdown("""
📄 **Interpretación:**  
La tabla anterior muestra los datos obtenidos directamente desde la API pública.  
Cada fila representa un usuario con información básica como su nombre, correo, ciudad y compañía.
""")

st.divider()

# ================== TRANSFORMACIONES ==================
df['name_length'] = df['name'].astype(str).apply(len)
df['username_length'] = df['username'].astype(str).apply(len)
df['email_domain'] = df['email'].astype(str).apply(lambda x: x.split('@')[-1].lower() if '@' in str(x) else None)

# ================== MÉTRICAS ==================
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total de Usuarios", len(df))
with col2:
    st.metric("Promedio Longitud Nombre", f"{df['name_length'].mean():.1f}")
with col3:
    st.metric("Dominios Únicos", df['email_domain'].nunique())
with col4:
    st.metric("Compañías Únicas", df['company_name'].nunique())

st.divider()

# ================== VISUALIZACIONES ==================
st.header("📈 Visualizaciones Interactivas")

# ---------------------- 1️⃣ HISTOGRAMA ----------------------
st.subheader("Distribución de caracteres en nombres")
fig1 = px.histogram(df, x='name_length', nbins=10,
                    title='Distribución de caracteres en los nombres',
                    color_discrete_sequence=['#636EFA'])
fig1.update_layout(xaxis_title='Cantidad de caracteres', yaxis_title='Frecuencia')
st.plotly_chart(fig1, use_container_width=True)

st.markdown("📊 **Interpretación:** La mayoría de los usuarios tienen nombres con entre **10 y 20 caracteres**, lo que refleja una longitud media en los nombres registrados.")

html_fig1 = fig1.to_html(include_plotlyjs='cdn')
st.download_button("💾 Descargar Histograma (HTML)", html_fig1, "histograma_nombres.html", "text/html")

st.divider()

# ---------------------- 2️⃣ BARRAS ----------------------
st.subheader("Usuarios por dominio de correo")
dom_counts = df['email_domain'].value_counts().reset_index()
dom_counts.columns = ['email_domain', 'count']

fig2 = px.bar(dom_counts, x='count', y='email_domain', orientation='h',
              title='Usuarios por dominio de correo electrónico',
              color='count', color_continuous_scale='Blues')
fig2.update_layout(xaxis_title='Cantidad de usuarios', yaxis_title='Dominio')
st.plotly_chart(fig2, use_container_width=True)

st.markdown("📊 **Interpretación:** Se observa que la mayoría de los usuarios utilizan **dominios de correo comunes**, lo que sugiere homogeneidad en los proveedores de email entre los registros.")

html_fig2 = fig2.to_html(include_plotlyjs='cdn')
st.download_button("💾 Descargar Barras Dominios (HTML)", html_fig2, "barras_dominios.html", "text/html")

st.divider()

# ---------------------- 3️⃣ DONUT ----------------------
st.subheader("Distribución de dominios de email (Donut)")
fig3 = px.pie(dom_counts, names='email_domain', values='count', hole=0.4,
              title='Distribución de dominios de email (Donut)')
st.plotly_chart(fig3, use_container_width=True)

st.markdown("📊 **Interpretación:** Este gráfico muestra visualmente el porcentaje de usuarios por dominio de correo. La distribución es **equilibrada**, sin un dominio que predomine excesivamente.")

html_fig3 = fig3.to_html(include_plotlyjs='cdn')
st.download_button("💾 Descargar Gráfico Donut (HTML)", html_fig3, "grafico_donut_dominios.html", "text/html")

st.divider()

# ---------------------- 4️⃣ DISPERSIÓN ----------------------
st.subheader("Relación entre longitud del nombre y del username")
fig4 = px.scatter(df, x='name_length', y='username_length',
                  color='city', size='id',
                  hover_data=['name', 'username', 'email_domain'],
                  title='Relación entre longitud del nombre y del username')
fig4.update_layout(xaxis_title='Longitud del Nombre', yaxis_title='Longitud del Username')
st.plotly_chart(fig4, use_container_width=True)

st.markdown("📊 **Interpretación:** La gráfica de dispersión revela que no existe una relación directa entre la longitud del nombre y la del username. Sin embargo, ciertos grupos de usuarios comparten patrones similares según su ciudad de origen.")

html_fig4 = fig4.to_html(include_plotlyjs='cdn')
st.download_button("💾 Descargar Gráfico de Dispersión (HTML)", html_fig4, "grafico_dispersion.html", "text/html")

st.divider()

# ---------------------- 5️⃣ PASTEL ----------------------
st.subheader("Distribución de usuarios por compañía")
company_counts = df['company_name'].value_counts().reset_index()
company_counts.columns = ['company_name', 'count']

fig5 = px.pie(company_counts, names='company_name', values='count',
              title='Distribución de Usuarios por Compañía',
              color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(fig5, use_container_width=True)

st.markdown("📊 **Interpretación:** Cada compañía tiene una cantidad similar de usuarios registrados, lo que indica que los datos están **balanceados** entre distintas empresas ficticias del dataset.")

html_fig5 = fig5.to_html(include_plotlyjs='cdn')
st.download_button("💾 Descargar Gráfico de Pastel (HTML)", html_fig5, "grafico_pastel_companias.html", "text/html")

st.divider()

# ================== CONCLUSIÓN ==================
st.success("""
✅ **Conclusión General:**  
Este dashboard analiza los usuarios obtenidos desde la API pública, mostrando su distribución por nombres, dominios de correo, compañías y relación entre campos.  
Incluye una **vista previa de datos** y **5 visualizaciones interactivas** (histograma, barras, donut, dispersión y pastel) con interpretaciones y opción de descarga en HTML.
""")
