# app.py
import streamlit as st
import requests
import sqlite3
import pandas as pd
import plotly.express as px

# ================== CARÁTULA ==================
st.set_page_config(page_title="Inteligencia Artificial", layout="wide")

st.markdown("""
# 🤖 Inteligencia Artificial
Alumno : **Anthony Fajardo**  
Carrera : **Desarrollo de software**

## 📓 Guía paso a paso: Consumir API → SQLite → Pandas → Gráficas con Plotly

En esta guía replicamos tu flujo con `sqlite3` y reemplazamos las gráficas de `matplotlib/seaborn` 
por **Plotly** para obtener visualizaciones **interactivas**.

**Fuente de datos:** [https://jsonplaceholder.typicode.com/users](https://jsonplaceholder.typicode.com/users)
---
""")

# ================== CONSUMIR API ==================
DB_NAME = 'usuarios3.db'
API_URL = 'https://jsonplaceholder.typicode.com/users'

st.info("📡 Conectando con la API...")
try:
    response = requests.get(API_URL, timeout=20)
    response.raise_for_status()
    users = response.json()
    st.success(f"✅ Datos obtenidos correctamente ({len(users)} filas)")
except Exception as e:
    st.error(f"❌ Error al obtener datos: {e}")
    st.stop()

# ================== GUARDAR EN SQLITE ==================
conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS users;")
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    username TEXT,
    email TEXT,
    phone TEXT,
    website TEXT
)
""")
for u in users:
    cur.execute("""
    INSERT OR REPLACE INTO users (id, name, username, email, phone, website)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (u.get('id'), u.get('name'), u.get('username'), u.get('email'), u.get('phone'), u.get('website')))
conn.commit()
conn.close()

# ================== LEER CON PANDAS ==================
conn = sqlite3.connect(DB_NAME)
df = pd.read_sql_query("SELECT * FROM users", conn)
conn.close()

st.subheader("📋 Datos de usuarios")
st.dataframe(df, use_container_width=True)

# ================== PROCESAMIENTO ==================
df['domain'] = df['email'].str.split('@').str[1]
domain_count = df['domain'].value_counts().reset_index()
domain_count.columns = ['domain', 'count']

# ================== GRÁFICOS ==================
st.markdown("### 1️⃣ Cantidad de usuarios por dominio de correo")
fig1 = px.bar(domain_count, x='domain', y='count', color='count',
              labels={'domain':'Dominio', 'count':'Cantidad de usuarios'},
              title="Usuarios por dominio de correo")
st.plotly_chart(fig1, use_container_width=True)

st.markdown("### 2️⃣ Visualización de nombre vs username")
fig2 = px.scatter(df, x='username', y='name', color='domain',
                  hover_data=['email','phone','website'],
                  title="Nombre vs Username (color por dominio)")
st.plotly_chart(fig2, use_container_width=True)

st.markdown("### 3️⃣ Gráfico circular de usuarios por dominio")
fig3 = px.pie(domain_count, names='domain', values='count', title='Distribución de usuarios por dominio')
st.plotly_chart(fig3, use_container_width=True)

# ================== NUEVOS GRÁFICOS ==================
# 4️⃣ Longitud de los nombres
df['name_length'] = df['name'].apply(len)
fig4 = px.histogram(df, x='name_length', nbins=10, color_discrete_sequence=['#00CC96'],
                    title='Distribución de la longitud de los nombres')
st.plotly_chart(fig4, use_container_width=True)

st.markdown("""
**Interpretación:**  
Este histograma muestra cómo se distribuye la longitud de los nombres de los usuarios.  
Podemos observar si predominan nombres cortos o largos, lo cual puede ser útil para validar formatos de nombres o analizar patrones de registro.
""")

# 5️⃣ Comparativa de longitud del nombre vs longitud del username
df['username_length'] = df['username'].apply(len)
fig5 = px.scatter(df, x='name_length', y='username_length', text='username', color='domain',
                  title='Relación entre longitud del nombre y del username',
                  labels={'name_length':'Longitud del nombre', 'username_length':'Longitud del username'})
st.plotly_chart(fig5, use_container_width=True)

st.markdown("""
**Interpretación:**  
Esta gráfica compara la longitud de los nombres con la de los usernames.  
Permite detectar si existe una relación entre ambos — por ejemplo, si los usuarios con nombres más largos tienden a tener usernames más cortos o similares.
""")

# ================== CONCLUSIÓN ==================
st.success("""
✅ **Conclusión general:**  
Hemos logrado consumir una API pública, almacenar los datos localmente en SQLite, procesarlos con Pandas y 
visualizarlos mediante **cinco gráficas interactivas** que exploran diferentes aspectos de los usuarios.
""")
