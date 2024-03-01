# import library
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import plotly.express as px


st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    initial_sidebar_state="expanded",
    layout="centered"
    )
    

alt.themes.enable("dark")

# Load data
day_df = pd.read_csv("day.csv")

# sidebar
with st.sidebar:
    st.title('🚲 Bike Sharing Dashboard')
    st.text('by Abror Muhammad Hazim')
    
    # Ubah nilai 0 menjadi 2011 dan 1 menjadi 2012
    year_mapping = {0: 2011, 1: 2012}
    year_list = list(day_df.yr.map(year_mapping).unique())[::-1]
    
    selected_year = st.selectbox('Select a year', year_list, index=len(year_list)-1)
    
    # Kembali ubah nilai 2011 menjadi 0 dan 2012 menjadi 1
    selected_year_mapped = [key for key, value in year_mapping.items() if value == selected_year][0]
    
    df_selected_year = day_df[day_df.yr == selected_year_mapped]

# main page
st.title(f'Analisis Bike Sharing Tahun {selected_year}')

filtered_data_selected_year = day_df[(day_df["yr"] == selected_year_mapped)]

fig = px.line(filtered_data_selected_year, x="dteday", y=["registered", "casual"], 
            title=f"Timeline Registered dan Casual User selama Tahun {selected_year}")
fig.update_xaxes(title="Bulan")
fig.update_yaxes(title="Jumlah User")
st.plotly_chart(fig)

# columns

col1, col2, col3 = st.columns(3)
 
with col1:
    st.header("Registered User")
    df_selected_year['total_registered'] = df_selected_year['registered'].cumsum()
    total_registered_user = df_selected_year['registered'].sum()
    st.write(f'{total_registered_user}')

 
with col2:
    st.header("Casual User")
    df_selected_year['total_casual'] = df_selected_year['casual'].cumsum()
    total_casual_user = df_selected_year['casual'].sum()
    st.write(f'{total_casual_user}')


with col3:
    st.header("Total Semua User")
    df_selected_year['total_all'] = df_selected_year['cnt'].cumsum()
    total_all_user = df_selected_year['cnt'].sum()
    st.write(f'{total_all_user}')


tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])
 
with tab1:
    st.header("Hubungan Musim dengan Jumlah Sewa berdasarkan Hari Kerja")
   
    plt.figure(figsize=(8, 6))
    sns.barplot(x='season', y='cnt', hue='workingday', data=df_selected_year)
    plt.title('Hubungan Musim dengan Jumlah Sewa berdasarkan Working Day')
    plt.xlabel('Musim')
    plt.ylabel('Jumlah Sewa')
    plt.legend(title='Hari Kerja', loc='upper right')
    st.pyplot(plt.gcf())

 
with tab2:
    st.header(f'Hubungan Hari Libur dengan Jumlah Sewa - Tahun {selected_year}')

    plt.figure(figsize=(8, 6))
    sns.barplot(x='holiday', y='cnt', data=df_selected_year, hue="holiday")
    plt.title(f'Hubungan Hari Libur dengan Jumlah Sewa - Tahun {selected_year}')
    plt.xlabel('Hari Libur')
    plt.ylabel('Jumlah Sewa')
    plt.legend(title='Hari Libur', loc='upper right')
    st.pyplot(plt.gcf())
 
with tab3:
    st.header(f'Hubungan Cuaca dengan Jumlah Sewa - Tahun {selected_year}')
    fig = px.box(df_selected_year, x='weathersit', y='cnt', color='weathersit',
                title=f'Hubungan Cuaca dengan Jumlah Sewa - Tahun {selected_year}',
                labels={'cnt': 'Jumlah Sewa', 'weathersit': 'Cuaca'})
    fig.update_xaxes(type='category', title='Cuaca', tickvals=[1, 2, 3], ticktext=['Clear', 'Mist', 'Rain/Snow'])
    fig.update_yaxes(title='Jumlah Sewa')

    # Tampilkan plotly chart ke Streamlit
    st.plotly_chart(fig)
 
