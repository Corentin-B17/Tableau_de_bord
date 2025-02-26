import pydot
import pandas as pd
import streamlit as st # Import streamlit
import matplotlib.pyplot as plt # Import matplotlib
import seaborn as sns # Import seaborn

# Charger les données
df = pd.read_excel("C:\\Users\\barbu\\Downloads\\salaries_data.xlsx", sheet_name="Sheet1")

# Configuration de la page
st.set_page_config(layout="wide")
st.title("Tableau de Bord des Salaires")

# Barre latérale avec filtres
st.sidebar.header("Filtres")

job_titles = st.sidebar.multiselect("Filtrer par titre de poste", df['job_title'].unique())
experience = st.sidebar.selectbox("Filtrer par niveau d'expérience", ["Tous"] + list(df['experience_level'].unique()))
locations = st.sidebar.multiselect("Filtrer par localisation d'entreprise", df['company_location'].unique())
remote_ratio = st.sidebar.slider("Filtrer par ratio de travail à distance", 0, 100, 0, step=50)

# Filtrer les données
filtered_df = df.copy()
if job_titles:
    filtered_df = filtered_df[filtered_df['job_title'].isin(job_titles)]
if experience != "Tous":
    filtered_df = filtered_df[filtered_df['experience_level'] == experience]
if locations:
    filtered_df = filtered_df[filtered_df['company_location'].isin(locations)]
filtered_df = filtered_df[filtered_df['remote_ratio'] == remote_ratio]

# Calcul des métriques
avg_salary = filtered_df['salary_in_usd'].mean() if not filtered_df.empty else 0
median_salary = filtered_df['salary_in_usd'].median() if not filtered_df.empty else 0
job_count = filtered_df['job_title'].nunique() if not filtered_df.empty else 0
company_count = filtered_df['company_location'].nunique() if not filtered_df.empty else 0

# Disposition des visualisations et métriques
st.subheader("Métriques Clés")
col1, col2, col3, col4 = st.columns(4)

col1.metric(label="Salaire moyen (USD)", value=f"{avg_salary:.2f}")
col2.metric(label="Salaire médian (USD)", value=f"{median_salary:.2f}")
col3.metric(label="Titres de poste uniques", value=job_count)
col4.metric(label="Nombre d'entreprises par localisation", value=company_count)

st.subheader("Distribution des Salaires")
fig_salary = px.histogram(filtered_df, x='salary_in_usd', title='Distribution des Salaires')
st.plotly_chart(fig_salary, use_container_width=True)

st.subheader("Nombre d'entreprises par localisation")
company_counts = filtered_df['company_location'].value_counts().reset_index()
company_counts.columns = ['company_location', 'count']
fig_company = px.bar(company_counts, x='company_location', y='count', 
                      title="Nombre d'entreprises par localisation")
st.plotly_chart(fig_company, use_container_width=True)
