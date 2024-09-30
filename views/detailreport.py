import plotly.graph_objects as go
import streamlit as st

# Örnek veri
dates = ['2024-01-01', '2024-02-01', '2024-03-01', '2024-04-01']
actual_values = [60, 80, 95, 100]  # Bar için
planned_values = [50, 70, 90, 100]  # Bar için
variance_values = [10, 15, 20, 25]  # Line için

# Plotly figürü oluşturma
fig = go.Figure()

# Bar Chart for ACTUAL % with black outline (kontur)
fig.add_trace(go.Bar(
    x=dates, 
    y=actual_values, 
    name='ACTUAL %', 
    marker_color='#04E879', 
    marker_line_color='black',  # Kontur rengi
    marker_line_width=2,        # Kontur genişliği
    opacity=0.6                 # Şeffaflık
))

# Bar Chart for PLANNING % with black outline (kontur)
fig.add_trace(go.Bar(
    x=dates, 
    y=planned_values, 
    name='PLANNING %', 
    marker_color='#0168C9', 
    marker_line_color='black',  # Kontur rengi
    marker_line_width=2,        # Kontur genişliği
    opacity=0.6                 # Şeffaflık
))

# Line Chart for VARIANCE % (Barların üzerinden geçen çizgi)
fig.add_trace(go.Scatter(
    x=dates, 
    y=variance_values, 
    name='VARIANCE %', 
    mode='lines+markers', 
    line=dict(color='red', width=4), 
    marker=dict(size=10)
))

# Layout ayarları
fig.update_layout(
    title='Bar and Line Chart with Bar Contours',
    xaxis_title='Date',
    yaxis_title='Percentage (%)',
    barmode='overlay',  # Barların üzerine çizgi yerleştirmek için overlay modunu kullanıyoruz
    bargap=0.2,         # Barlar arasındaki boşluğu ayarlama
    bargroupgap=0.1,    # Gruplanmış barlar arasındaki boşluğu ayarlama
)

# Streamlit'te figürü gösterme
st.plotly_chart(fig)
