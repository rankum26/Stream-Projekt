import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load Pokémon dataset
@st.cache_data
def load_data():
    url = "https://gist.githubusercontent.com/armgilles/194bcff35001e7eb53a2a8b441e8b2c6/raw/92200bc0a673d5ce2110aaad4544ed6c4010f687/pokemon.csv"
    data = pd.read_csv(url)
    return data

# Title of the app
st.title('Ranujans Pokémon App')

# Load data
data = load_data()

# Display first few rows of the dataset
st.write("Verfügbare Spalten im Dataset:", data.columns.tolist())

# Sidebar for filters
st.sidebar.header('Filter Options')

# Filter by Pokémon Type 1
type1 = st.sidebar.selectbox('Wähle den Pokémon-Typ (Type 1):', ['All'] + sorted(data['Type 1'].dropna().unique()))

# Filter by Generation
generation = st.sidebar.selectbox('Wähle die Generation:', ['All'] + sorted(data['Generation'].dropna().unique()))

# Filter by HP
min_hp, max_hp = st.sidebar.slider('Wähle die HP Range:', int(data['HP'].min()), int(data['HP'].max()), (int(data['HP'].min()), int(data['HP'].max())))

# Apply filters
if type1 != 'All':
    data = data[data['Type 1'] == type1]

if generation != 'All':
    data = data[data['Generation'] == int(generation)]

data = data[(data['HP'] >= min_hp) & (data['HP'] <= max_hp)]

# Display filtered data
st.write(f"Gefilterte Datenübersicht ({data.shape[0]} Einträge):", data)

# Plotting
st.header('Visualisierungen')

# Number of Pokémon by Type
st.subheader('Anzahl der Pokémon pro Typ')
fig, ax = plt.subplots()
sns.countplot(data=data, x='Type 1', order=data['Type 1'].value_counts().index, ax=ax)
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
st.pyplot(fig)

# Distribution of HP
st.subheader('Verteilung der HP')
fig, ax = plt.subplots()
sns.histplot(data['HP'], bins=30, kde=True, ax=ax)
ax.set_title('Verteilung der HP')
st.pyplot(fig)

# Boxplot of HP by Type
st.subheader('HP nach Typ')
fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(data=data, x='Type 1', y='HP', ax=ax)
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
st.pyplot(fig)

# Scatterplot of Attack vs Defense
st.subheader('Attack vs. Defense')
fig, ax = plt.subplots()
sns.scatterplot(data=data, x='Attack', y='Defense', hue='Type 1', ax=ax)
ax.set_title('Attack vs. Defense')
st.pyplot(fig)


