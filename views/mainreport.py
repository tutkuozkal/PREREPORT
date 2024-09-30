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
#st.set_page_config(page_title="Home", page_icon="", layout="wide")


#------------------------------- SOL BAR SIDE BAR ----------------------------------------------------------
#sidebar date picker
min_date = datetime.date(2024,1,1)
max_date = datetime.date(2024,8,15)
with st.sidebar:
    st.title("Select Date Range")
    start_date = st.date_input(label="Start Date",value=min_date)

with st.sidebar:
    finish_date = st.date_input(label="Finish Date",value=max_date)

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
                    dtype={'ACTIVITY': str, 'PLANNED %': int, 'ACTUAL %': int, 'VARIANCE %': int},
                    )

#------------------------------- ACTUAL SOL ALAN (WEEKLY PROGRESS) -----------------------------------------------------------
excel_file1 = "actual.xlsx"
sheet_name1 = "summary"

df2 = pd.read_excel("actual.xlsx", 
                    usecols="A:G",
                    header=0,
                    #index_col=0, 
                    dtype={'DATE': str, 'PLANNED %': int, 'ACTUAL %': int, 'VARIANCE %': int, 'BASE': int,'OVERALL_ACTUAL': int,'OVERALL2': int}
                    )


#filter data range
df3 = df2[(df2["DATE"]>=str(start_date)) & (df2["DATE"]<=str(finish_date))]
# Örnek veri: 'DATE' sütunu olan bir DataFrame
df3['DATE'] = pd.to_datetime(df2['DATE'], errors='coerce')  # Tarih formatına çevirme
df3['DATE'] = df3['DATE'].dt.strftime('%d-%m-%Y')  # "D MMM YYYY" formatına çevirme
st.write("")

a1,a2 = st.columns(2)
with a1:
     #st.expander("Iki Tarih Arasi Veri Tablosu")
     #filtered_df = dataframe_explorer(df3,case=False,)
     st.markdown("""
    <div style="text-align: center;">
    <b>WEEKLY PROGRESS</b>
    """, unsafe_allow_html=True)
     st.write("")
     st.dataframe(df3,use_container_width=True,width=500, height=282)

with a2:
    st.markdown("""
    <div style="text-align: center;">
    <b>OVERALL PROGRESS</b>
    """, unsafe_allow_html=True)
    st.write("")
    st.dataframe(df,use_container_width=True,width=500, height=282)
st.divider()


area1 = px.bar(df3,
    x = "DATE",
    y = "ACTUAL %",
    text_auto='.2s',
    width=1600, 
    height=400,
    barmode="group",
    color='ACTUAL %',
    #color_continuous_scale=px.colors.sequential.Plasma,
    color_continuous_scale=["#0168C9","#04E879"],
    #color_discrete_sequence=['FF1E1E']
    

)
st.markdown("""
    <br>        
    <div style="text-align: center;">
    <b>ACTUAL %</b>
    """,unsafe_allow_html=True)
area2 = px.bar(df3,
    x = "DATE",
    y = "PLANNING %",
    text_auto='.2s',
    width=1600, 
    height=400,
    color='PLANNING %',
    color_continuous_scale=["#357928",'#0168C9'],
    
)

st.plotly_chart(area1)
st.markdown("""
    <br>        
    <div style="text-align: center;">
    <b>PLANNING %</b>
    """,unsafe_allow_html=True)
st.plotly_chart(area2)

st.divider()

# Veriyi uzun formata dönüştürme (melt)
df_melted = df3.melt(id_vars='DATE', value_vars=['ACTUAL %', 'PLANNING %'],
                           var_name='Category', value_name='Percentage')

# Bar grafiği oluşturma (gruplandırılmış)
st.markdown("""
    <br>        
    <div style="text-align: center;">
    <b>ACTUAL & PLANNING %</b>
    """,unsafe_allow_html=True)
# Özel renkleri tanımlayın (her kategori için bir renk)
custom_colors = {
    'ACTUAL %': '#04E879',  # Mavi
    'PLANNING %': '#0168C9'  # Kırmızı
}

fig = px.bar(df_melted, x='DATE', y='Percentage', color='Category', barmode='group',
             text_auto='.2s',color_discrete_map=custom_colors)
st.plotly_chart(fig)

# ----------------------------- PLOTLY S-CURVE -------------------------------------------------------------

# st.write() boş bir satır oluşturur, gerekliyse kullanın
st.write("")

# Başlık için ortalanmış bir markdown yapısı
st.markdown("""
    <div style="text-align: center;">
    <b>TOTAL PROGRESS S-CURVE</b>
    </div>
    """, unsafe_allow_html=True)
df3['OVERALL'] = df3['OVERALL'].astype(str) + '%'
# Plotly figürü oluşturma
fig = go.Figure()

# Add bar chart for PLANNING % and ACTUAL %
fig.add_trace(go.Bar(x=df3['DATE'], y=df3['ACTUAL %'], name='ACTUAL', marker_color='#04E879',marker_line_color='black',marker_line_width=1,opacity=0.8, text=df3['ACTUAL %'], textposition='inside'))
fig.add_trace(go.Bar(x=df3['DATE'], y=df3['PLANNING %'], name='PLANNING', marker_color='#0168C9',marker_line_color='black',marker_line_width=1,opacity=0.8, text=df3['PLANNING %'], textposition='inside'))


# # Add line chart for VARIANCE % on secondary y-axis
fig.add_trace(go.Scatter(x=df3['DATE'], y=df3['VARIANCE %'], name='VARIANCE', 
                         mode='lines+markers+text', line=dict(shape='spline', color='red', width=2), yaxis='y2',
                         text=[f"<b>{val}</b>" for val in df3['VARIANCE %']], textposition='top center'))


# Add another smooth line for TREND % on secondary y-axis
fig.add_trace(go.Scatter(x=df3['DATE'], y=df3['PLANNING %'], name='PLANNING', 
                         mode='lines+markers+text', line=dict(shape='spline', color='#0168C9', width=2), yaxis='y2',
                         text=[f"<b>{val}</b>" for val in df3['PLANNING %']], textposition='top center'))

# Add another smooth line for TREND % on secondary y-axis
fig.add_trace(go.Scatter(x=df3['DATE'], y=df3['OVERALL'], name='OVERALL %', 
                         mode='lines+markers+text', line=dict(shape='spline', color='red', width=2, dash='dot'), yaxis='y2',
                         text=[f"<b>{val}</b>" for val in df3['OVERALL']], textposition='top center'))

# Add another smooth line for TREND % on secondary y-axis
fig.add_trace(go.Scatter(x=df3['DATE'], y=df3['OVERALL2'], name='OVERALL2 %', 
                         mode='lines+markers+text', line=dict(shape='spline', color='blue', width=2, dash='dot'), yaxis='y2',
                         text=[f"<b>{val}</b>" for val in df3['OVERALL2']], textposition='bottom center'))

# Layout'u güncelleme
fig.update_layout(
    xaxis_title='Date',
    yaxis_title='Percentage (%)',
    yaxis2=dict(title='Percentage %', overlaying='y', side='right'),  # Secondary y-axis for both lines
    barmode='group',
    bargap=0.2,         # Barlar arasındaki boşluğu ayarlama
    bargroupgap=0.1,
    
)

# Figürü Streamlit'te gösterme
st.plotly_chart(fig)

st.divider()
#------------------------------- IMALAT TABLOSU -----------------------------------------------------------
# Excel dosyasını yükle
# Veri okuma fonksiyonu - cache ile optimize edildi
@st.cache_data
def load_data(excel_file, sheet_name):
    # Excel dosyasını yükleyelim
    df = pd.read_excel(excel_file,
                       sheet_name=sheet_name,
                       usecols='A:D',
                       header=0,
                       skiprows=0,
                       dtype={'PLASTER': int, 'GYPSUM_PLASTER': int, 'PAINT': int})
    
    # Tarih sütununu datetime formatına çevirelim
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
    return df

# Excel dosyasını yükle ve cache'e al
excel_file2 = "imalat.xlsx"
sheet_name2 = "summary"
df4 = load_data(excel_file2, sheet_name2)

# start_date ve finish_date'in tarih formatına çevrilmesi
start_date = pd.to_datetime(start_date)
finish_date = pd.to_datetime(finish_date)

# Veriyi filtrele (start_date ve finish_date arasında)
df5 = df4[(df4["DATE"] >= start_date) & (df4["DATE"] <= finish_date)]

# Tarih formatını sadece yıl olarak gösterme
df5['DATE'] = df5['DATE'].dt.strftime('%d-%m-%Y')

# Imalat birimlerini ekleyelim
df5['PLASTER'] = df5['PLASTER'].astype(str) + ' m²'
df5['GYPSUM_PLASTER'] = df5['GYPSUM_PLASTER'].astype(str) + ' m²'
df5['PAINT'] = df5['PAINT'].astype(str) + ' m²'

# Yüzde hesaplama fonksiyonu
def calculate_percentage(part, whole):
    return round((part / whole) * 100, 2) if whole != 0 else 0

# Sayısal verilerle toplam hesaplama (orijinal verileri kullanıyoruz)
total_plaster = df4['PLASTER'].sum()
total_gypsum = df4['GYPSUM_PLASTER'].sum()
total_paint = df4['PAINT'].sum()

# Filtrelenmiş veriler için toplamlara göre yüzdeleri hesaplama
plaster_sum = df5['PLASTER'].replace(' m²', '', regex=True).astype(float).sum()
gypsum_sum = df5['GYPSUM_PLASTER'].replace(' m²', '', regex=True).astype(float).sum()
paint_sum = df5['PAINT'].replace(' m²', '', regex=True).astype(float).sum()

# Doğru yüzdeleri hesaplama
plaster_percentage = calculate_percentage(plaster_sum, total_plaster)
gypsum_percentage = calculate_percentage(gypsum_sum, total_gypsum)
paint_percentage = calculate_percentage(paint_sum, total_paint)

# # İki kolon oluştur ve dataframe ve metrik sonuçlarını göster
# s1, s2 = st.columns(2)
# with s1:
#     st.dataframe(df5, use_container_width=True, width=500, height=282)
s1,s2 = st.columns(2)

with s1:
    # Toplam sonuçları ve yüzdeleri gösterelim
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("")
        st.metric(label="Plaster Total", value=f"{plaster_sum} m²", delta=f"{plaster_percentage} %")
    with col2:
        st.write("")
        st.metric(label="Gypsum Plaster Total", value=f"{gypsum_sum} m²", delta=f"{gypsum_percentage} %")
    with col3:
        st.write("")
        st.metric(label="Paint Total", value=f"{paint_sum} m²", delta=f"{paint_percentage} %")
with s2:
    # Sonuçların tablosunu göster
    data = {
        'Material': ['PLASTER', 'GYPSUM_PLASTER', 'PAINT'],
        'Total': [f"{plaster_sum} m²", f"{gypsum_sum} m²", f"{paint_sum} m²"],
        'Percentage': [f"{plaster_percentage} %", f"{gypsum_percentage} %", f"{paint_percentage} %"]
    }
    
    df_totals = pd.DataFrame(data)
    st.dataframe(df_totals, use_container_width=True)

# Alt çizgi ile ayırıcı
st.divider()
#------------------------------- RESIMLER -----------------------------------------------------------------

# Add to image line
r1,r2 = st.columns(2)
with r1:
    st.image('1.jpg',use_column_width='auto')
with r2:
    st.image('2.jpg',use_column_width='never',)



