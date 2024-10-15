# importing libraries
import pandas as pd # data manipulation
import random as rd # random number generation
import matplotlib.pyplot as plt # plotting
import seaborn as sns # plotting
import streamlit as st # web app
import numpy as np # numerical operations
import plotly.express as px # plotting

# page layout
st.set_page_config(layout="wide")

# caching the data loading functions
@st.cache_data
def load_last_names():
    return pd.read_csv('last_names.csv')

@st.cache_data
def load_first_names():
    return pd.read_csv('first_names.csv')

@st.cache_data
def load_subjects():
    return pd.read_csv('subjects.csv')

# reading the csv files
df_lastNames = load_last_names()
df_firstNames = load_first_names()
df_subjects = load_subjects()


# title of the app
st.title('Grade Analyser')
# 2 columns wide layout
col1, col2 = st.columns(2, vertical_alignment='top',)

# sidebar 
studentNr_input = st.sidebar.number_input('Number of students', min_value=1, max_value=100, value=10, step=1)
subjectNr_input = st.sidebar.number_input('Number of subjects', min_value=1, max_value=100, value=10, step=1)
gradesPerSubject_input = st.sidebar.number_input('Grades per subject', min_value=1, max_value=10, value=3, step=1)
minGrade_input = st.sidebar.number_input('Minimum grade', min_value=0, max_value=95, value=0, step=5)
maxGrade_input = st.sidebar.number_input('Maximum grade', min_value=10, max_value=100, value=10, step=5)

# creates a new dataframe with the number of students and subjects selected and grades per subject, respecting the minimum and maximum grade and 

# creates a list of last names
lastNames = rd.choices(df_lastNames['Last name'], k=studentNr_input)
lastNames = [lastName for lastName in lastNames for _ in range(gradesPerSubject_input * subjectNr_input)]
lastNames.sort()

# creates a list of first names
firstNames = rd.choices(df_firstNames['First name'], k=studentNr_input)
firstNames = [firstName for firstName in firstNames for _ in range(gradesPerSubject_input * subjectNr_input)]

# creates a list of subjects
subjects = rd.choices(df_subjects['Subject'], k=subjectNr_input)
subjects = [subject for subject in subjects for _ in range(gradesPerSubject_input * studentNr_input)]

# creates a list of grades
grades = rd.choices(range(minGrade_input, maxGrade_input + 1, 5), k=studentNr_input * subjectNr_input * gradesPerSubject_input)

# creates a dataframe with the lists created
# Combine first and last names
fullNames = [f"{first} {last}" for first, last in zip(firstNames, lastNames)]

# Create the dataframe with an index as student ID
df = pd.DataFrame({
    'Student ID': range(1, len(fullNames) + 1),
    'Name': fullNames,
    'Subject': subjects,
    'Grade': grades
})

# saves the dataframe in the session state if it does not exist yet in order to keep the data after the app is reloaded
if "dataframe" not in st.session_state:
    st.session_state['dataframe'] = df
    
# creates a list of students after the dataframe is created 
studentList = st.sidebar.selectbox('Select student', df['Name'].unique())
    
# download button  for the dataframe
download = st.sidebar.download_button('Download data as CSV', df.to_csv(), 'grades.csv', 'text/csv')
    
if download:
    df = st.session_state['dataframe']
      
if studentNr_input or subjectNr_input or gradesPerSubject_input or minGrade_input or maxGrade_input:
    st.session_state['dataframe'] = df
    
with col1:
    st.write(df)
    
    fig, ax = plt.subplots()
    sns.kdeplot(data=df, x='Grade', ax=ax, fill=True, hue='Name', legend=False)
    ax.set_xlim(int(minGrade_input), int(maxGrade_input))
    ax.set_title('Grade distribution')
    ax.set_xlabel('Grade')
    ax.set_ylabel('Density')
    st.pyplot(fig)   


with col2:
    st.write(df.describe())
    
    # creates a plotly histogram with the count of grades grouped by subject with overlapping colors
    fig = px.histogram(df, x='Grade', color='Subject', opacity=0.7, barmode='overlay')
    st.plotly_chart(fig)
    
    
    # creates a bar chart with the counted grades for the selected student
    fig, ax = plt.subplots()
    sns.histplot(data=df[df['Name'] == studentList], x='Grade', ax=ax, color='red')
    ax.legend([studentList])
    ax.set_xlabel('Grade')
    ax.set_ylabel('Count')
    st.pyplot(fig)