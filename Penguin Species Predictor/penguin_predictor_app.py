import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsOneClassifier
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
import base64


st.image('penguins.png')

st.write("""
# Penguin Species Predictor

This app uses the One vs One classification approach to predict the species of Penguin:
- Gentoo
- Chinstrap
- Adelie

**Made by Ifeanyi Nneji**


The notebook, dataset and python file are available on my [GitHub](https://github.com/Nneji123/Streamlit-Web-App-Projects)        

Data obtained from the [palmerpenguins library](https://github.com/allisonhorst/palmerpenguins) in R by Allison Horst.

Also thanks to the [Data Professor](https://github.com/dataprofessor)
""")

st.sidebar.header('User Input Features')

st.sidebar.markdown("""
[Example CSV input file]()                    
                    """)

uploaded_file = st.sidebar.file_uploader('Upload your CSV file')
if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file)
else:
    def user_input_features():
        sex = st.sidebar.selectbox('Sex, 1:Male, 0:Female',(0,1))
        culmen_length_mm = st.sidebar.slider('Culmen length (mm)', 32.1,59.6,43.9)
        culmen_depth_mm = st.sidebar.slider('Culmen depth (mm)', 13.1,21.5,17.2)
        flipper_length_mm = st.sidebar.slider('Flipper length (mm)', 172.0,231.0,201.0)
        body_mass_g = st.sidebar.slider('Body mass (g)', 2700.0,6300.0,4207.0)
        data = {
                'culmen_length_mm': culmen_length_mm,
                'culmen_depth_mm': culmen_depth_mm,
                'flipper_length_mm': flipper_length_mm,
                'body_mass_g': body_mass_g,
                'sex': sex}
        features = pd.DataFrame(data, index=[0])
        return features
    input_df = user_input_features() 
    
penguins_raw = pd.read_csv('penguine_cleaned.csv')
penguins = penguins_raw.drop(columns=['species'])
df = pd.concat([input_df,penguins],axis=0)


st.subheader('User Input features')

if uploaded_file is not None:
    st.write(df)
else:
    st.write('Awaiting CSV file to be uploaded. Currently using example input parameters (shown below).')
    st.write(df)

# Reads in saved classification model
load_clf = joblib.load('penguin_classifier.pkl')

# Apply Model to make predictions
prediction = load_clf.predict(df.astype(int))
lsn = pd.DataFrame(prediction)

st.subheader('Prediction')
st.write('The Prediction is: ', lsn.sample(5))


def download_file(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="prediction.csv">Download CSV File</a>'
    return href


st.markdown(download_file(lsn), unsafe_allow_html=True)


if st.button('Confusion Matrix'):
    st.markdown("""
A confusion matrix is a table that is used to define the performance of a classification algorithm. A confusion matrix visualizes and summarizes the performance of a classification algorithm.                
                
                """)
    dt = pd.read_csv('Predicted Species Using OVR and OVO Approach.csv', index_col=0)
    x = dt.One_Vs_One_Prediction
    y = dt['species']
    with sns.axes_style("white"):
        clf_confusion_matrix = pd.crosstab(x, y, rownames = ['Predicted'], colnames=['Actual'])
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(clf_confusion_matrix, annot=True)
    st.pyplot(f)

    st.write("Accuracy= ",accuracy_score(x,y)*100,"%")





