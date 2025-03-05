import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title= "Data sweeper",layout='wide' )

#custom css
st.markdown(
    """
    <style>
    .stApp{
        background-color: black;
        color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
)


#title and description
st.title("Datasweeper Sterling Integrator")
st.write("transform your files between CVS and Excel formats with built-in data cleaning and visualization Creating the project for quarter 3!")

#file uploader
uploaded_files = st.file_uploader("upload your files(accepts CVS or Excel):", type=["cvs","xlsx"], accept_multiple_files=(True))


if uploaded_files:
        for file in uploaded_files:
            file_ext = os.path.splitext(file.name)[-1]. lower ()
            if file_ext == ".csv":
                df =pd.read_csv(file)
            elif file_ext == "xlx":
                df = pd.read_excel(file)
            else:
                st.error(f"unsupported file type: {file_ext}")
                continue
              
            #file details
            st.write("Preview the head of the Dataeframe")
            st.dataframe(df.head())
              
              
              
            #Data cleaning options
            st.subheader("Data cleaning options")
            if st.checkbox(f"clean data for {file.name}"):
                  col1, col2 =st.columns(2)
                  
                  with col1:
                    if st.button(f"Remove duplicates from the file :{file.name}"):
                        df.drop_duplicates(inplace=True)
                        st.write("duplicates removed!")
                          
                  with col2:
                    if st.button(f"Fill missing value for {file.name}"):
                        numric_cols =df.select_dtypes(include=['number']).colums
                        df[numric_cols] =df[numric_cols].fillna(df[numric_cols].mean())
                        st.write("Missing value have been filled!")
                          
            st.subheader("select colums to keep")
            colums = st.multiselect(f"choose colums for {file.name}",df.columns,default=df.columns)
            df=df[colums]
            
            
            
            
            #Data visualization
            st.subheader("Data visulization")
            if st.checkbox(f"show visulization for {file.name}"):
                st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])
            
            #conversion options

            st.subheader("conversion option")
            conversion_type = st.radio(f"convert {file.name} to:", ["CSV" ,"Excle"], key=file.name)
            if st.button(f"convert {file.name}"):
                buffer=BytesIO()
                if conversion_type == "CSV":
                    df.to.CSV(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"

                elif conversion_type == "Excel":
                    df.to_excel(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                buffer.seek(0)

                st.download_button(
                    label=f"Download {file.name} as {conversion_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )
st.success("All files processed successfully!")