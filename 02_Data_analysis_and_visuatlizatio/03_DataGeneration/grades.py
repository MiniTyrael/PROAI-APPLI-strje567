# importing libraries
import pandas as pd
import random as rd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import random

# reading the csv files
df_lastNames = pd.read_csv('last_names.csv')
df_firstNames = pd.read_csv('first_names.csv')
df_subjects = pd.read_csv('subjects.csv')

# title of the app
st.title('Grade Analyser')

# sidebar 
studentNr_input = st.sidebar.number_input('Number of students', min_value=1, max_value=100, value=10, step=1)

subjectNr_input = st.sidebar.number_input('Number of subjects', min_value=1, max_value=100, value=10, step=1)

gradesPerSubject_input = st.sidebar.number_input('Grades per subject', min_value=1, max_value=10, value=3, step=1)

minGrade_input = st.sidebar.number_input('Minimum grade', min_value=0, max_value=95, value=1, step=1)

maxGrade_input = st.sidebar.number_input('Maximum grade', min_value=minGrade_input+5, max_value=100, value=10, step=1)

studentList = st.sidebar.selectbox('Student list', ['Random', 'Custom'])


# creates a new dataframe with the number of students and subjects selected and grades per subject, respecting the minimum and maximum grade and 

lastNames = random.choices(df_lastNames['Last name'], k=studentNr_input)

firstNames = random.choices(df_firstNames['First name'], k=studentNr_input)


st.write(firstNames)
st.write(lastNames)