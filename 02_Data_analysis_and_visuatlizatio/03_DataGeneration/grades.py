# importing libraries
import pandas as pd # data manipulation
import random as rd # random number generation
import matplotlib.pyplot as plt # plotting
import seaborn as sns # plotting
import streamlit as st # web app
import numpy as np # numerical operations
import plotly.express as px # plotting


# reading files functions
def read_files(lastnames, firstnames, subjects):
    # caching the data loading functions
    @st.cache_data
    def load_last_names():
        return pd.read_csv(lastnames)

    @st.cache_data
    def load_first_names():
        return pd.read_csv(firstnames)

    @st.cache_data
    def load_subjects():
        return pd.read_csv(subjects)

    # reading the csv files
    df_lastNames = load_last_names()
    df_firstNames = load_first_names()
    df_subjects = load_subjects()

    return df_lastNames, df_firstNames, df_subjects

# sidebar function
def sidebar_creation():
    # sidebar 
    num_students  = st.sidebar.number_input('Number of students', min_value=1, max_value=100, value=10, step=1)
    num_subjects  = st.sidebar.number_input('Number of subjects', min_value=1, max_value=100, value=10, step=1)
    num_grades_per_subject  = st.sidebar.number_input('Grades per subject', min_value=1, max_value=10, value=3, step=1)
    def_max_Grade = 60
    min_grade  = st.sidebar.number_input('Minimum grade', min_value=0, max_value=def_max_Grade-5, value=0, step=5)
    max_grade  = st.sidebar.number_input('Maximum grade', min_value=min_grade+5, max_value=100, value=60, step=5)
    
    return num_students, num_subjects, num_grades_per_subject, min_grade, max_grade

def regenerate_data(lastname, firstname, subjects, num_students, num_subjects, num_grades_per_subject, min_grade, max_grade):
        
    # creates a new dataframe with the number of students and subjects selected and grades per subject, respecting the minimum and maximum grade and the number of students
    # creates a list of last names
    lastNames = rd.choices(lastname['Last name'], k=num_students)
    lastNames = [lastName for lastName in lastNames for _ in range(num_grades_per_subject * num_subjects)]
    lastNames.sort()

    # creates a list of first names
    firstNames = rd.choices(firstname['First name'], k=num_students)
    firstNames = [firstName for firstName in firstNames for _ in range(num_grades_per_subject * num_subjects)]

    # creates a list of subjects
    subjects = rd.choices(subjects['Subject'], k=num_subjects * num_students)
    subjects = [subject for subject in subjects for _ in range(num_grades_per_subject)]

    # creates a list of grades
    grades = rd.choices(range(min_grade, max_grade + 1, 5), k=num_students * num_subjects * num_grades_per_subject)

    # creates a dataframe with the lists created
    # Combine first and last names
    fullNames = [f"{first} {last}" for first, last in zip(firstNames, lastNames)]

    # Create the dataframe with an index as student ID
    # Create a dictionary to store student IDs
    student_id_dict = {}
    current_id = 1

    # Assign student IDs based on names
    student_ids = []
    for name in fullNames:
        if name not in student_id_dict:
            student_id_dict[name] = current_id
            current_id += 1
        student_ids.append(student_id_dict[name])

    df = pd.DataFrame({
        'Student ID': student_ids,
        'Name': fullNames,
        'Subject': subjects,
        'Grade': grades
    })
           
    return df
    
def create_plots(df, minGrade_input, maxGrade_input, selectedStudent, col1, col2):
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
    
        # Filter for student data
        student_data = df[df['Name'] == selectedStudent]
        
        # creates a bar chart with the counted grades for the selected student
        fig, ax = plt.subplots()
        sns.histplot(data=student_data, x='Grade', ax=ax, color='red')
        ax.legend([selectedStudent])
        ax.set_xlabel('Grade')
        ax.set_ylabel('Count')
        st.pyplot(fig)
        
# main function 
def main():
    # page layout
    st.set_page_config(layout="wide")

    # title of the app
    st.title('Grade Analyser')
    # 2 columns wide layout
    col1, col2 = st.columns(2, vertical_alignment='top',)
    
    # read the csv files
    df_lastNames, df_firstNames, df_subjects = read_files('last_names.csv', 'first_names.csv', 'subjects.csv')
    
    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame()
    if 'params' not in st.session_state:
        st.session_state.params = {}
    
    num_students, num_subjects, num_grades_per_subject, min_grade, max_grade = sidebar_creation()

    current_params = {
        'num_students': num_students,
        'num_subjects': num_subjects,
        'num_grades_per_subject': num_grades_per_subject,
        'min_grade': min_grade,
        'max_grade': max_grade
    }
    
    if st.session_state.df.empty or st.session_state.params != current_params:
        st.session_state.df = regenerate_data(df_lastNames, df_firstNames, df_subjects, num_students, num_subjects, num_grades_per_subject, min_grade, max_grade)
        st.session_state.params = current_params
            
    # creates a list of students after the dataframe is created 
    selectedStudent = st.sidebar.selectbox('Select student', st.session_state.df['Name'].unique())
    
    # create the plots
    create_plots(st.session_state.df, min_grade, max_grade, selectedStudent, col1, col2)
    
    # download button  for the dataframe
    st.sidebar.download_button('Download data as CSV', st.session_state.df.to_csv().encode('utf-8'), 'grades.csv', 'text/csv')
    
    
# run the main function if the script is run directly
if __name__ == '__main__':
    main()