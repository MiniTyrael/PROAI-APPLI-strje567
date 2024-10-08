import streamlit as st
import pandas as pd

# title of the app
st.title('Global Earthquake Data')

# description of the dataset
st.write('''Comprehensive dataset of global earthquakes with key attributes for analysis by https://www.kaggle.com/datasets/shreyasur965/recent-earthquakes?resource=download''')

# loads the dataset
earthquake_df = pd.read_csv('https://raw.githubusercontent.com/MiniTyrael/PROAI-APPLI-strje567/refs/heads/main/02_Data_analysis_and_visuatlizatio/01_GlobalEarthquakeData/earthquakes.csv')

# displays the first few rows of the dataset
st.write(earthquake_df.head())

# line break
st.write('---')

# new header
st.header('Magnitude')
st.write("Minimum :", earthquake_df['magnitude'].min())
st.write("Mean :", earthquake_df['magnitude'].mean())
st.write("Maximum :", earthquake_df['magnitude'].max())

# line break
st.write('---')

# new network header
st.header('Network')

# searchbar
net_list = earthquake_df['net'].unique()
selected_net = st.selectbox('Network', net_list)

# creates new dataframe only with the selected data net data from the selectbox
df_net = earthquake_df[earthquake_df['net'] == selected_net]

# Counts the number of earthquakes
st.write(f'The number of earthquakes for {selected_net}: {df_net['id'].count()}')

# number of earthquakes by network
st.write('Number of earthquakes by network')

# counts the number of earthquakes by network
earthquake_counts = earthquake_df['net'].value_counts().reset_index()

# renames the columns
earthquake_counts.columns = ['Network', 'Number of Earthquakes']

# creates a bar chart
st.bar_chart(earthquake_counts.set_index('Network'))

# line break
st.write('---')
