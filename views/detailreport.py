import plotly.graph_objects as go
import streamlit as st
import pandas as pd
from datetime import datetime
import datetime 


#------------------------------------------------------------------------------------------------------------------

# Excel dosyasını yükleme (örnek bir dosya yolu)
excel_file = "imalat.xlsx"
sheet_name = "summary"

# Excel'den veriyi okuma
df_excel = pd.read_excel(excel_file, sheet_name=sheet_name)

# Tarih kolonunu Excel'den çekelim (örneğin ilk kolon 'DATE' olsun)
dates = df_excel['DATE'].dt.strftime('%Y-%m-%d').tolist()  # Tarih kolonunu listeye çeviriyoruz


# Sidebar: Excel'den alınan kolon isimlerini checkbox olarak göster
st.sidebar.markdown("### Production")
# Tarih ve DATE kolonunu hariç tutarak sadece imalat kolonlarını seçelim
available_columns = df_excel.columns.difference(['DATE'])
selected_columns = st.sidebar.multiselect("Choose Your Productions", available_columns)

# Eğer kullanıcı herhangi bir kolon seçtiyse işlemleri yapalım
if selected_columns:
    # Seçilen imalatlara ait verileri alalım
    selected_values = {col: df_excel[col].tolist() for col in selected_columns}
    
    # DataFrame oluşturma
    df_selected = pd.DataFrame(selected_values, index=dates).T  # Transpoz alıyoruz, böylece malzemeler satır başlıkları, tarihler kolonlar olacak

    # Her imalat için birikimli (cumulative) toplam hesaplama ve yeni satır ekleme
    df_selected.loc['Cumulative Total'] = df_selected.cumsum(axis=1).iloc[0]  # İlk satırın birikimli toplamını al

    # Genel toplamı (tüm imalatların toplamını) alalım
    total_sum = df_selected.loc['Cumulative Total'].max()  # Son kolon genel toplamı verecek

    # Birikimli yüzdeleri hesaplayalım
    cumulative_percentage = (df_selected.loc['Cumulative Total'] / total_sum) * 100

    # Yüzdeleri iki ondalık olacak şekilde yuvarlayıp yüzde işareti ekleyelim
    df_selected.loc['Cumulative Percentage'] = cumulative_percentage.apply(lambda x: f"{round(x, 2)}%")

    # DataFrame'i Streamlit'te gösterme
    st.write("Detailed Data of Selected Productions:")
    #st.dataframe(df_selected, use_container_width=True)

    # Plotly combo chart (bar + scatter)
    fig = go.Figure()

    # Bar chart (seçilen kolonlar için)
    for col in selected_columns:
        fig.add_trace(go.Bar(
            x=dates,
            y=df_selected.loc[col],
            name=col,
            text=df_selected.loc[col],
            textposition='auto'
        ))


    # Layout ayarları (aylar arasında ayırıcılar ve özel tarih formatı)
    fig.update_layout(
        title='Production/s ve Cumulative Percentage',
        xaxis_title='Date',
        yaxis_title='Production',
        xaxis=dict(
            tickmode='array',
            tickvals=dates,
            tickformat='%b %Y',  # Ay ve yıl formatı (örneğin: Jan 2024)
            tickangle=45  # X eksenindeki tarihleri açılı gösterme
        ),
        yaxis2=dict(
            title='Data',
            overlaying='y',
            side='right'
        ),
        legend=dict(x=0.01, y=0.99),
        height=600,
        barmode='group'
    )

    # Grafiği Streamlit'te göster
    st.plotly_chart(fig, use_container_width=True)

else:
    st.write("Please select one or more productions from the sidebar.")

#--------------------------------------------------------------------------------------------------------


# Excel dosyasını yükleme (örnek bir dosya yolu)
excel_file = "imalat.xlsx"
sheet_name = "summary"

# Excel'den veriyi okuma
df_excel = pd.read_excel(excel_file, sheet_name=sheet_name)

# Tarih kolonunu datetime formatına çeviriyoruz
df_excel['DATE'] = pd.to_datetime(df_excel['DATE'])

# Sidebar: Başlangıç ve Bitiş tarihi seçimleri
st.sidebar.markdown("### Select Data Range")
min_date = df_excel['DATE'].min()
max_date = df_excel['DATE'].max()

# Başlangıç tarihi seçimi
start_date = st.sidebar.date_input(
    "Start Date",
    min_value=min_date,
    max_value=max_date,
    value=min_date
)

# Bitiş tarihi seçimi
end_date = st.sidebar.date_input(
    "Finish Date",
    min_value=min_date,
    max_value=max_date,
    value=max_date
)

# Sidebar: Excel'den alınan kolon isimlerini selectbox olarak göster
st.sidebar.markdown("### Production")
# Tarih ve DATE kolonunu hariç tutarak sadece imalat kolonlarını seçelim
available_columns = df_excel.columns.difference(['DATE'])
selected_column = st.sidebar.selectbox("Choose Your Production", available_columns)

# Eğer kullanıcı herhangi bir kolon seçtiyse işlemleri yapalım
if selected_column:
    # Tüm veri üzerinden toplam hesapla (tüm tarihlerin toplamını alacağız)
    total_sum_all_time = df_excel[selected_column].sum()

    # Seçilen tarih aralığına göre veriyi filtreleyelim
    df_filtered = df_excel[(df_excel['DATE'] >= pd.to_datetime(start_date)) & (df_excel['DATE'] <= pd.to_datetime(end_date))]
    
    # Seçilen imalatın değerlerini alalım (seçilen tarihler aralığında)
    selected_values = df_filtered[selected_column].tolist()
    dates = df_filtered['DATE'].dt.strftime('%Y-%m-%d').tolist()  # Filtrelenmiş tarihleri listeye çeviriyoruz
    
    # DataFrame oluşturma
    df_selected = pd.DataFrame({selected_column: selected_values}, index=dates).T  # Transpoz alıyoruz, böylece malzeme satır başlıkları, tarihler kolonlar olacak

    # Seçilen imalat için birikimli (cumulative) toplam hesaplama ve yeni satır ekleme
    df_selected.loc['Cumulative Total'] = df_selected.cumsum(axis=1).iloc[0]  # İlk satırın birikimli toplamını al

    # Cumulative Percentage, tüm veri setine göre hesaplanıyor
    cumulative_percentage = (df_selected.loc['Cumulative Total'] / total_sum_all_time) * 100

    # Yüzdeleri iki ondalık olacak şekilde yuvarlayıp yüzde işareti ekleyelim
    df_selected.loc['Cumulative Percentage'] = cumulative_percentage.apply(lambda x: f"{round(x, 2)}%")

    # DataFrame'i Streamlit'te gösterme
    st.write(f"Detailed Data of the Selected Production Between ({start_date} & {end_date}):")
    st.dataframe(df_selected, use_container_width=True)

    # Plotly combo chart (bar + scatter)
    fig = go.Figure()

    # Bar chart (seçilen kolon için)
    fig.add_trace(go.Bar(
        x=dates,
        y=df_selected.loc[selected_column],
        name=selected_column,
        text=df_selected.loc[selected_column],
        textposition='auto'
    ))

    # Scatter chart (Cumulative Percentage)
    fig.add_trace(go.Scatter(
        x=dates,
        y=cumulative_percentage,
        name='Cumulative Percentage',
        mode='lines+markers+text',
        line=dict(color='rgb(255,99,71)', width=2),
        text=[f"{round(val, 2)}%" for val in cumulative_percentage],
        textposition='top center'
    ))

    # Layout ayarları (aylar arasında ayırıcılar ve özel tarih formatı)
    fig.update_layout(
        title=f'{selected_column} ve Cumulative Percentage ({start_date} - {end_date})',
        xaxis_title='Date',
        yaxis_title=selected_column,
        xaxis=dict(
            tickmode='array',
            tickvals=dates,
            tickformat='%b %Y',  # Ay ve yıl formatı (örneğin: Jan 2024)
            tickangle=45  # X eksenindeki tarihleri açılı gösterme
        ),
        yaxis2=dict(
            title='Cumulative Percentage (%)',
            overlaying='y',
            side='right'
        ),
        legend=dict(x=0.01, y=0.99),
        height=600,
        barmode='group'
    )

    # Grafiği Streamlit'te göster
    st.plotly_chart(fig, use_container_width=True)

else:
    st.write("Please select one or more productions from the sidebar.")
#---------------------------------------------------------------------------------------------
