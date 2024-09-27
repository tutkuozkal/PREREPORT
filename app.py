
#import module
import pandas as pd
import streamlit as st
import plotly.express as px 
import altair as alt 
from streamlit_extras.dataframe_explorer import dataframe_explorer 
from datetime import datetime
import datetime
import plotly.graph_objects as go
from PIL import Image


# Config the page width
st.set_page_config(page_title="Home", page_icon="", layout="wide")


#------------------------------------ OVERALL PROGRESS -----------------------------------------------------

# Load data set
excel_file = "rapor.xlsx"
sheet_name = "summary"

df = pd.read_excel(excel_file,
                    sheet_name=sheet_name,
                    usecols='A:D',
                    header=0,
                    index_col=0,
                    skiprows=0,
                    nrows=7,
                    dtype={'ACTIVITY': str, 'PLANNED %': int, 'ACTUAL %': int, 'VARIANCE %': int, 'BOQ': int},
                    )

#------------------------------- SOL BAR SIDE BAR ----------------------------------------------
#sidebar date picker
min_date = datetime.date(2024,1,1)
max_date = datetime.date(2024,9,1)
with st.sidebar:
    st.title("Select Date Range")
    start_date = st.date_input(label="Start Date",value=min_date)

with st.sidebar:
    finish_date = st.date_input(label="Finish Date",value=max_date)

#------------------------------- ACTUAL SOL ALAN ----------------------------------------------
excel_file1 = "actual.xlsx"
sheet_name1 = "summary"

df2 = pd.read_excel("actual.xlsx")

#filter data range
df3 = df2[(df2["DATE"]>=str(start_date)) & (df2["DATE"]<=str(finish_date))]
# Örnek veri: 'DATE' sütunu olan bir DataFrame
df3['DATE'] = pd.to_datetime(df2['DATE'], errors='coerce')  # Tarih formatına çevirme
df3['DATE'] = df3['DATE'].dt.strftime('%d-%m-%Y')  # "D MMM YYYY" formatına çevirme
st.write("")

a1,a2 = st.columns(2)
with a1:
     st.expander("Iki Tarih Arasi Veri Tablosu")
     filtered_df = dataframe_explorer(df3,case=False,)
     st.dataframe(filtered_df,use_container_width=True,width=500, height=282)
st.write("")
with a2:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.markdown("""
    <div style="text-align: center;">
    <b>OVERALL PROGRESS</b>
    """, unsafe_allow_html=True)
    st.dataframe(df,use_container_width=True,width=500, height=282)
st.divider()
datas = ["ACTUAL %","PLANNING %"]

area1 = px.bar(df3,
    x = "DATE",
    y = "ACTUAL %",
    text_auto='.2s',
    width=1600, 
    height=400,
    barmode="group"

)

area2 = px.bar(df3,
    x = "DATE",
    y = "PLANNING %",
    text_auto='.2s',
    width=1600, 
    height=400
)

st.plotly_chart(area1)
st.plotly_chart(area2)
st.divider()

# Veriyi uzun formata dönüştürme (melt)
df_melted = df3.melt(id_vars='DATE', value_vars=['ACTUAL %', 'PLANNING %'],
                           var_name='Category', value_name='Percentage')

# Bar grafiği oluşturma (gruplandırılmış)
st.markdown("""
    <br>        
    <div style="text-align: center;">
    <b>Actual vs Planning %</b>
    """,unsafe_allow_html=True)
# Özel renkleri tanımlayın (her kategori için bir renk)
custom_colors = {
    'ACTUAL %': '#04E879',  # Mavi
    'PLANNING %': '#0168C9'  # Kırmızı
}

fig = px.bar(df_melted, x='DATE', y='Percentage', color='Category', barmode='group',
             text_auto='.2s',color_discrete_map=custom_colors)
st.plotly_chart(fig)

# ----------------------------- PLOTLY ----------------------------------------------
st.write("")
st.markdown("""
    <div style="text-align: center;">
    <b>TOTAL PROGRESS S-CURVE</b>
    """, unsafe_allow_html=True)
# Create the Plotly figure
fig = go.Figure()

# Add bar chart for PLANNING % and ACTUAL %t
fig.add_trace(go.Bar(x=df3['DATE'], y=df3['PLANNING %'], name='PLANNING %', marker_color='blue',text=df3['PLANNING %'], textposition='inside'))
fig.add_trace(go.Bar(x=df3['DATE'], y=df3['ACTUAL %'], name='ACTUAL %', marker_color='green',text=df3['ACTUAL %'], textposition='inside'))

# Add line chart for VARIANCE % on secondary y-axis
fig.add_trace(go.Scatter(x=df3['DATE'], y=df3['VARIANCE %'], name='VARIANCE %', 
                         mode='lines+markers+text', line=dict(shape='spline',color='red', width=2), yaxis='y2',text=[f"<b>{val}</b>" for val in df3['VARIANCE %']], textposition='top center'))

# Add another smooth line for TREND % on secondary y-axis
fig.add_trace(go.Scatter(x=df3['DATE'], y=df3['BOQ'], name='BOQ', 
                         mode='lines+markers+text', line=dict(shape='linear', color='black', width=2, dash='dot'), yaxis='y2',text=[f"<b>{val}</b>" for val in df3['BOQ']], textposition='top center'))


# Update layout to include a secondary y-axis
fig.update_layout(
    #title='PLANNING % vs ACTUAL % with VARIANCE % and BOQ',
    xaxis_title='Date',
    yaxis_title='Percentage (%)',
    yaxis2=dict(title='Variance / Trend (%)', overlaying='y', side='right'),  # Secondary y-axis for both lines
    barmode='group',
    #width=800,  # Set figure width to 800 pixels
    #height=400  # Set figure height to 400 pixels
)

# Show the figure in Streamlit
st.plotly_chart(fig)

st.divider()
#------------------------------- IMALAT TABLOSU ----------------------------------------------
# Excel dosyasını yükle
excel_file2 = "imalat.xlsx"
sheet_name2 = "summary"

df4 = pd.read_excel(excel_file2,
                    sheet_name=sheet_name2,
                    usecols='A:D',
                    header=0,
                    #index_col=0,
                    skiprows=0,
                    dtype={'PLASTER': int, 'GYPSUM_PLASTER': int, 'PAINT': int})

# Tarih formatını düzeltelim (Tarih sütununu datetime'a çevir)
df4['DATE'] = pd.to_datetime(df4['DATE'], errors='coerce')

# start_date ve finish_date'in tarih formatına çevrilmesi
start_date = pd.to_datetime(start_date)
finish_date = pd.to_datetime(finish_date)

# Veriyi filtrele (start_date ve finish_date arasında)
df5 = df4[(df4["DATE"] >= start_date) & (df4["DATE"] <= finish_date)]

# Tarih formatını sadece yıl olarak gösterme
df5['DATE'] = df5['DATE'].dt.strftime('%d-%m-%Y')

# Filtrelenmiş tabloyu Streamlit'te göster
st.dataframe(df5, use_container_width=True)

st.divider()

#------------------------------- RESIMLER ----------------------------------------------

# Add to image line
r1,r2 = st.columns(2)
with r1:
    st.image('1.jpg',use_column_width='auto')
with r2:
    st.image('2.jpg',use_column_width='never',)

