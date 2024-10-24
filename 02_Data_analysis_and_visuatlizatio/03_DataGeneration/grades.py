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
        
    current_params = {'num_students': num_students, 'num_subjects': num_subjects,
                    'num_grades_per_subject': num_grades_per_subject,
                    'min_grade': min_grade, 'max_grade': max_grade}

    # creates a new dataframe with the number of students and subjects selected and grades per subject, respecting the minimum and maximum grade and the number of students
    # creates a list of last names
    lastNames = rd.choices(lastname['Last name'], k=num_students)
    lastNames = [lastName for lastName in lastNames for _ in range(num_grades_per_subject * num_subjects)]
    lastNames.sort()

    # creates a list of first names
    firstNames = rd.choices(firstname['First name'], k=num_students)
    firstNames = [firstName for firstName in firstNames for _ in range(num_grades_per_subject * num_subjects)]

    # creates a list of subjects
    subjects = rd.choices(subjects['Subject'], k=num_subjects)
    subjects = [subject for subject in subjects for _ in range(num_grades_per_subject * num_students)]

    # creates a list of grades
    grades = rd.choices(range(min_grade, max_grade + 1, 5), k=num_students * num_subjects * num_grades_per_subject)

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
    
    # creates a list of students after the dataframe is created 
    selectedStudent = st.sidebar.selectbox('Select student', df['Name'].unique())
        
    # download button  for the dataframe
    download = st.sidebar.download_button('Download data as CSV', df.to_csv(), 'grades.csv', 'text/csv')
       
    return df, selectedStudent, current_params

    
# if download:
#     df = st.session_state['dataframe']
      
# if studentNr_input or subjectNr_input or gradesPerSubject_input or minGrade_input or maxGrade_input:
#     st.session_state['dataframe'] = df
    
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
    
    
        # creates a bar chart with the counted grades for the selected student
        fig, ax = plt.subplots()
        sns.histplot(data=df[df['Name'] == selectedStudent], x='Grade', ax=ax, color='red')
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
    
    num_students, num_subjects, num_grades_per_subject, min_grade, max_grade = sidebar_creation()
           
    # regenerate the data
    df, selectedStudent, current_params = regenerate_data(df_lastNames, df_firstNames, df_subjects, num_students, num_subjects, num_grades_per_subject, min_grade, max_grade)
    
        # regenerate the data
    # if 'df' not in st.session_state:
    #     st.session_state.df = pd.DataFrame()
    # if 'params' not in st.session_state:
    #     st.session_state.params = {}
    
    
    
    # regenerate the data
    # if st.session_state.df is None or st.session_state.params != current_params:
    #     df, minGrade_input, maxGrade_input, selectedStudent, current_params = regenerate_data(df_lastNames, df_firstNames, df_subjects)
    #     st.session_state.df = df
    #     st.session_state.params = current_params
    
    # create the plots
    create_plots(df, min_grade, max_grade, selectedStudent, col1, col2)
    
    
# run the main function if the script is run directly
if __name__ == '__main__':
    main()