import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('Forbes Billionaires EDA App')

st.markdown("""

Made by **Ifeanyi Nneji**

This app retrieves the list of the **Forbes Billionaires** (from Wikipedia) and its corresponding **data**!
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn
* **Data source:** [Wikipedia](https://en.wikipedia.org/wiki/The_World%27s_Billionaires).
""")

st.sidebar.header('User select year')

selected_year = st.sidebar.selectbox('Year', list(reversed(range(2010, 2022))))


# Web Scraping of Billionaires stats
@st.cache
def load_data(year):
    url = "https://en.wikipedia.org/wiki/The_World%27s_Billionaires"
    html = pd.read_html(url, header=0)
    # i = {selected_year:}
    i = 0
    x = selected_year
    if x == 2021:
        i = 3
    elif x == 2020:
        i = 4
    elif x == 2019:
        i = 5
    elif x == 2018:
        i = 6
    elif x == 2017:
        i = 7
    elif x == 2016:
        i = 8
    elif x == 2015:
        i = 9
    elif x == 2014:
        i = 10
    elif x == 2013:
        i = 11
    elif x == 2012:
        i = 12
    elif x == 2011:
        i = 13
    elif x == 2010:
        i = 14
    df = html[i]
    df = df.set_index('No.')
    return df


billstats = load_data(selected_year)

# Nationality Selection
sorted_unique_nationality = sorted(billstats['Nationality'].unique())
selected_nationality = st.sidebar.multiselect('Country', sorted_unique_nationality, sorted_unique_nationality)

# Filtering Data

df_selected_nation = (billstats[(billstats.Nationality.isin(selected_nationality))]).astype(str)

st.header('Display Billionaire Stats of Selected Nation(s)')
st.write("Data Dimension: " + str(df_selected_nation.shape[0]) + ' rows and ',
         str(df_selected_nation.shape[1]) + ' columns. ')
st.dataframe(df_selected_nation)


# Download Billionaire Statistical Data

def download_file(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="billionaire_stats.csv">Download CSV File</a>'
    return href


st.markdown(download_file(df_selected_nation), unsafe_allow_html=True)

# Heatmap and Various Plot Diagrams
if st.button('Bar Plot'):
    st.header('Age and Networth BarPlot')
    df_selected_nation.to_csv('output.csv', index=False)
    df = pd.read_csv('output.csv')

    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.barplot(x=df.Age, y=df['Net worth (USD)'])
    st.pyplot(f)

