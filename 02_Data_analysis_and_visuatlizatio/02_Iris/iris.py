import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# title of the app
st.title('Iris Data')

# description of the dataset
st.write('''This is one of the earliest datasets used in the literature on classification methods and widely used in statistics and machine learning. The data set contains 3 classes of 50 instances each, where each class refers to a type of iris plant. One class is linearly separable from the other 2; the latter are not linearly separable from each other: https://archive.ics.uci.edu/dataset/53/iris''')

# loads the dataset
iris_df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data')

# add column names to the dataset
iris_df.columns = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']

st.write('Here are the first 5 data rows:')

# displays the first few rows of the dataset
st.write(iris_df.head())

st.write('And here are some basic statistics:')
st.write(iris_df.describe())

# line break
st.write('---')

# new header
st.header('Data distributions')

# creates a bar chart with the each column with matplotlib and adds it to the streamlit app
for col in iris_df:
    fig, ax = plt.subplots()
    plt.title(iris_df[col].name)
    ax.hist(iris_df[col])
    st.pyplot(fig)