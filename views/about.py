import streamlit as st 


# Config the page width



#---------------------- HERO SECTION -------------------#
col1, col2 = st.columns(2, gap= "small", vertical_alignment="center")
with col1:
    st.image('./assets/1.png', width=100,use_column_width="always" )
with col2:
    st.title('Tutku OZKAL', anchor= False)
    st.write(
        'Data Scientist, Planning and Reporting Expert'
    )
   

#---------------------- EXPERIENCE & QUALIFICATIONS -------------------#
st.write("")
st.subheader("Experience & Qualifications", anchor=False)
st.write(
    """
    - 24 Years of experience in Construction works (Planning and Reporting)
    """
)

#---------------------- SKILLS ----------------------------------------#
st.write("")
st.subheader("Hard Skills", anchor=False)
st.write(
    """
    - **Technical Programs**: Primavera, Autocad, Twinmotion, Lumion
    - **Programming**: Python, Excel VBA
    - **Data Visualization**: PowerBI, MS Excel, Plotly
    - **Databases**: MongoDB, MySQL
    """
)