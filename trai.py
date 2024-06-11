# ["FRAME WORK LIBRARIES"]
import streamlit as st 
import matplotlib.pyplot as plt
import seaborn as sns
from plotly import express as px  
from streamlit_option_menu import option_menu

import folium
from streamlit_folium import folium_static
import PIL
from PIL import Image

import streamlit.components.v1 as components

#["PYTHON LIBRARIES FOR TABULAR DATA AND FILE HANDLING"]
import pandas as pd
import numpy as np
import json

from geopy.geocoders import Nominatim
import re
#icon = Image.open("C:/Users/mahes/OneDriveDesktop/trai project/traiicon.jpeg")
# SETTING PAGE CONFIGURATION...........
st.set_page_config(page_title='TRAI',layout="wide")

# OPTION MENU FOR CHOICES OF VIEWS
selected = option_menu(None,
                       options = ["About","Home","Analysis"],
                       icons = ["safe2 fill","house-door-fill","bar-chart-line-fill"],
                       default_index=0,
                       orientation="horizontal",
                       styles={"container": {"width": "100%"},
                               "icon": {"color": "white", "font-size": "24px"},
                               "nav-link": {"font-size": "24px", "text-align": "center", "margin": "-2px"},
                               "nav-link-selected": {"background-color": "#6F36AD"}})

st.set_option('deprecation.showPyplotGlobalUse', False)

df1 = pd.read_csv("C:/Users/mahes/OneDrive/Desktop/trai project/dataset/Mar18-Aug18.csv")
df2 = pd.read_csv("C:/Users/mahes/OneDrive/Desktop/trai project/dataset/Sep18-Feb19.csv")
df3 = pd.read_csv("C:/Users/mahes/OneDrive/Desktop/trai project/dataset/Mar19-Aug19.csv")
df4 = pd.read_csv("C:/Users/mahes/OneDrive/Desktop/trai project/dataset/Sep19-Feb20.csv")
df5 = pd.read_csv("C:/Users/mahes/OneDrive/Desktop/trai project/dataset/Mar20-Aug20.csv")
df6 = pd.read_csv("C:/Users/mahes/OneDrive/Desktop/trai project/dataset/Sep20-Feb21.csv")
df7 = pd.read_csv("C:/Users/mahes/OneDrive/Desktop/trai project/dataset/Mar21-Aug21.csv")
df8 = pd.read_csv("C:/Users/mahes/OneDrive/Desktop/trai project/dataset/Sep21-Feb22.csv")
df9 = pd.read_csv("C:/Users/mahes/OneDrive/Desktop/trai project/dataset/Mar22-Aug22.csv")
df10 = pd.read_csv("C:/Users/mahes/OneDrive/Desktop/trai project/dataset/Sep22-Feb23.csv")
df11 = pd.read_csv("C:/Users/mahes/OneDrive/Desktop/trai project/dataset/Mar23-Aug23.csv")
df12 = pd.read_csv("C:/Users/mahes/OneDrive/Desktop/trai project/dataset/Sep23-Feb24.csv")
df13 = pd.read_csv("C:/Users/mahes/OneDrive/Desktop/trai project/dataset/Mar24-Aug24.csv")

json1 = f'C:/Users/mahes/OneDrive/Desktop/trai project/states_india.geojson'
dataDf = pd.read_csv("C:/Users/mahes/OneDrive/Desktop/trai project/data.csv")
dataDf1 = pd.read_csv("C:/Users/mahes/OneDrive/Desktop/trai project/data1.csv")
dataDf2 = pd.read_csv("C:/Users/mahes/OneDrive/Desktop/trai project/data2.csv")

# Initialize the geolocator
geolocator = Nominatim(user_agent="my_geocoder")


# Define a function to get coordinates
def get_coordinates(state):
    location = geolocator.geocode(state)
    if location:
        return f"{location.latitude}, {location.longitude}"
    else:
        return None
    

def folium_map(data):
    mapObj = folium.Map(location=[22.167057857886153, 82.44140625000001],
                    zoom_start=5)
    borderStyle={
        "color": "green",
        "weight": 2,
        "fill": False  
    }
    folium.GeoJson("states_india.geojson",
                            name='States',
                            style_function=lambda x : borderStyle).add_to(mapObj)
    
    # Apply the function to each row
    data['city_coord'] = data['Circles'].apply(get_coordinates)
    data[['x', 'y']] = data.city_coord.apply(lambda c: pd.Series(dict(zip(['x', 'y'], re.findall('[-]?[0-9]+\.[0-9]+', c.strip())))))

    
    # create a layer for bubble map using FeatureGroup
    #NetworkLayer = folium.FeatureGroup("Service Provider")
    # add the created layer to the map
    #NetworkLayer.add_to(mapObj)

    # iterate through each dataframe row
    for i in range(len(data)):
        state_name = data.iloc[i]['Circles']
        airtel = data.iloc[i]['AIRTEL(Mbps)']
        bsnl = data.iloc[i]['BSNL(Mbps)']
        jio = data.iloc[i]['RJIO(Mbps)']
        vi = data.iloc[i]['Vi India(Mbps)']
        
        # derive the circle pop up html content 
        popUpStr = 'Name - {0}<br>Airtel - {1}<br>BSNL - {2}<br>RJIO - {3}<br>Vi India - {4} Mbps'.format(
            state_name,airtel, bsnl, jio, vi)
        folium.Marker(location=[data['x'][i],data['y'][i]],
              icon=folium.Icon(icon='glyphicon-signal', color='red'),
              popup=folium.Popup(popUpStr,max_width = 500)
              ).add_to(mapObj)

        # add layer control over the map
        #folium.LayerControl().add_to(mapObj)

    folium_static(mapObj, width=1200, height=950)
def line_chart(data):
    plt.plot(data['Circles'], data['AIRTEL(Mbps)'], label='Airtel')  # Plot the first line
    plt.plot(data['Circles'], data['BSNL(Mbps)'], label='BSNL')  # Plot the second line
    plt.plot(data['Circles'], data['RJIO(Mbps)'], label='JIO')  # Plot the third line
    plt.plot(data['Circles'], data['Vi India(Mbps)'], label='VI')  # Plot the fourth line
    plt.title('Multiple Lines Chart')
    plt.xlabel('STATES')
    plt.ylabel('SERVICE PROVIDER')
    plt.legend()  # Show legend based on labels provided above
    st.pyplot()
            
        
def bar_chart(df):
    x=df['Service_Provider']
    y=df['Data_Speed']

    plt.bar(x,y)
    st.pyplot()


def about():
    url1 = 'https://myspeed.trai.gov.in/explore.html'
    video_url = 'https://youtu.be/hgAE2aBjD-8'
    col1, col2, = st.columns(2)
    
    col1.image(Image.open("C:/Users/mahes/OneDrive/Desktop/trai project/Telecom_Regulatory_Authority_of_India_TRAI.png") ,width=600)
    with col1:
        st.subheader("The Telecom Regulatory Authority of In a (TRAI) has undertaken a number of initiatives in this regard. This includes specifying QoS norms for wireless networks and the mechanisms to measure it on a regular basis. TRAI has also taken initiatives to empower customers to measure and report observed quality of wireless data networks.")
        
        st.markdown(f'''<a href={url1}><button style="background-color:#8a2be2;"><border style="display:inline-block;padding:0.5em 1em;border-radius:12px;border-color:none"><text style="color:#f2f3f4;">DOWNLOAD THE APP</button></a>''',unsafe_allow_html=True)

    with col2:
        st.video(video_url)
        st.subheader("SKILLS:")
        st.write("Python Scripting,Data Visualization,Geo visualization,MYSQL")
        st.subheader("DOMAIN")
        st.write("Telecom Industry")
        
def home():
    Image.open("C:/Users/mahes/OneDrive/Desktop/trai project/MySpeed_11012018.jpg")        
    col1,col2 = st.columns(2)
    with col1:
        st.image(Image.open("C:/Users/mahes/OneDrive/Desktop/trai project/download.jpeg"), width=500)
        st.markdown("## :violet[Done by] : UMAMAHESWARI S")
        st.markdown("[Inspired from](https://myspeed.trai.gov.in/index.php)")
        st.markdown("[Githublink](https://github.com/mahes101)")
        
    with col2:
        st.title("Wireless Data Speed")
        st.write('Speed of Internet connection is considered to be the most important and fundamental metric to measure broadband experience. '
                'Broadband experience across geographic locations and different networks also provides insights into the extent and level of achievement of the goals setby the Government.')
        st.subheader('Measurement of Wireless Data')
        
        url3 = "https://trai.gov.in/release-publication/reports/wireless-data-reports"
        text = "DOWNLOAD MEASUREMENT OF WIRELESS DATA REPORT"
        st.markdown(f'''<a href={url3}><button style="background-color:#8a2be2;"><border style="display:inline-block;padding:0.5em 1em;border-radius:12px;"><text style="color:#f2f3f4;">{text}</button></a>''',unsafe_allow_html=True)
        
def analysis():
    html_temp = """
        <div style="background-color:#fb607f;padding:10px;border-radius:10px">
        <h1 style="color:white;text-align:center;">WIRELESS DATA SPEED</h1>
        </div>"""

        # components.html("<p style='color:red;'> Streamlit Components is Awesome</p>")
    components.html(html_temp)
    list_operator = df1['Service_Provider'].unique()
    list_month = ["Mar18-Aug18","Sep18-Feb19","Mar19-Aug19","Sep19-Feb20","Mar20-Aug20","Sep20-Feb21","Mar21-Aug21","Sep21-Feb22","Mar22-Aug22","Sep22-Feb23","Mar23-Aug23","Sep23-Feb24","Mar24-Aug24"]
    operator_choice = st.selectbox("OPERATOR",list_operator)
    technology_choice = st.selectbox("TECHNOLOGY",['3G','4G'])
    period_choice = st.selectbox("SELECT PERIODIC MONTH",list_month)
    type_choice = st.radio("SELECT TEST TYPE",['UPLOAD','DOWNLOAD'])
    submit_button = st.button(label="SUBMIT")
    st.markdown("""
                    <style>
                    div.stButton > button:first-child {
                        background-color: #009999;
                        color: white;
                        width: 100%;
                    }
                    </style>
                """, unsafe_allow_html=True)
    if submit_button:
        if period_choice == "Mar18-Aug18":
            if type_choice == "UPLOAD":
                df1_new = df1.loc[(df1['Service_Provider']==operator_choice)&(df1['Technology']==technology_choice) & (df1['Test_Type']=="Upload") |(df1['Test_Type']=="UPLOAD")|(df1['Test_Type']=="upload")]
                df1_new.groupby('Data_Speed')['LSA'].unique().explode().reset_index()
            
                bar_chart(df1_new)
            else:
                df1_new = df1.loc[(df1['Service_Provider']==operator_choice)&(df1['Technology']==technology_choice) & (df1['Test_Type']=="Download") |(df1['Test_Type']=="download")|(df1['Test_Type']=="download")]
                df1_new.groupby('Data_Speed')['LSA'].unique().explode().reset_index()
                
                bar_chart(df1_new)
                    
        elif period_choice == "Sep18-Feb19":
            if type_choice == "UPLOAD":
                df2_new = df2.loc[(df2['Service_Provider']==operator_choice)&(df2['Technology']==technology_choice) & (df2['Test_Type']=="Upload") |(df2['Test_Type']=="UPLOAD")|(df2['Test_Type']=="upload")]
                df2_new.groupby('Data_Speed')['LSA'].unique().explode().reset_index()
                
                bar_chart(df2_new)
            else:
                df2_new = df2.loc[(df2['Service_Provider']==operator_choice)&(df2['Technology']==technology_choice) & (df2['Test_Type']=="Download") |(df2['Test_Type']=="download")|(df2['Test_Type']=="download")]
                df2_new.groupby('Data_Speed')['LSA'].unique().explode().reset_index()
                
                bar_chart(df2_new)
            
        elif period_choice == "Mar19-Aug19":
            if type_choice == "UPLOAD":
                df3_new = df3.loc[(df3['Service_Provider']==operator_choice)&(df3['Technology']==technology_choice) & (df3['Test_Type']=="Upload") |(df3['Test_Type']=="UPLOAD")|(df3['Test_Type']=="upload")]
                df3_new.groupby('Data_Speed')['LSA'].unique().explode().reset_index()
                
                bar_chart(df3_new)
            else:
                df3_new = df3.loc[(df3['Service_Provider']==operator_choice)&(df3['Technology']==technology_choice) & (df3['Test_Type']=="Download") |(df3['Test_Type']=="download")|(df3['Test_Type']=="download")]
                df3_new.groupby('Data_Speed')['LSA'].unique().explode().reset_index()
                
                bar_chart(df3_new)
            
        elif period_choice == "Sep19-Feb20":
            if type_choice == "UPLOAD":
                df4_new = df4.loc[(df4['Service_Provider']==operator_choice)&(df4['Technology']==technology_choice) & (df4['Test_Type']=="Upload") |(df4['Test_Type']=="UPLOAD")|(df4['Test_Type']=="upload")]
                df4_new.groupby('Data_Speed')['LSA'].unique().explode().reset_index()
                
                bar_chart(df4_new)
            else:
                df4_new = df4.loc[(df4['Service_Provider']==operator_choice)&(df4['Technology']==technology_choice) & (df4['Test_Type']=="Download") |(df4['Test_Type']=="download")|(df4['Test_Type']=="download")]
                df4_new.groupby('Data_Speed')['LSA'].unique().explode().reset_index()
                
                bar_chart(df4_new)
            
        elif period_choice == "Mar20-Aug20":
            if type_choice == "UPLOAD":
                df5_new = df5.loc[(df5['Service_Provider']==operator_choice)&(df5['Technology']==technology_choice) & (df5['Test_Type']=="Upload") |(df5['Test_Type']=="UPLOAD")|(df5['Test_Type']=="upload")]
                df5_new.groupby('Data_Speed')['LSA'].unique().explode().reset_index()
                
                bar_chart(df5_new)
            else:
                df5_new = df5.loc[(df5['Service_Provider']==operator_choice)&(df5['Technology']==technology_choice) & (df5['Test_Type']=="Download") |(df5['Test_Type']=="download")|(df5['Test_Type']=="download")]
                df5_new.groupby('Data_Speed')['LSA'].unique().explode().reset_index()
                
                bar_chart(df5_new)
            
            
        elif period_choice == "Sep20-Feb21":
            if type_choice == "UPLOAD":
                df6_new = df6.loc[(df6['Service_Provider']==operator_choice)&(df6['Technology']==technology_choice) & (df6['Test_Type']=="Upload") |(df6['Test_Type']=="UPLOAD")|(df6['Test_Type']=="upload")]
                df6_new.groupby('Data_Speed')['LSA'].unique().explode().reset_index()
                
                bar_chart(df6_new)
            else:
                df6_new = df6.loc[(df6['Service_Provider']==operator_choice)&(df6['Technology']==technology_choice) & (df6['Test_Type']=="Download") |(df6['Test_Type']=="download")|(df6['Test_Type']=="download")]
                df6_new.groupby('Data_Speed')['LSA'].unique().explode().reset_index()
                
                bar_chart(df6_new)
        elif period_choice == "Mar21-Aug21":
            if type_choice == "UPLOAD":
                df7_new = df7.loc[(df7['Service_Provider']==operator_choice)&(df7['Technology']==technology_choice) & (df7['Test_Type']=="Upload") |(df7['Test_Type']=="UPLOAD")|(df7['Test_Type']=="upload")]
                df7_new.groupby('Data_Speed')['LSA'].unique().explode().reset_index()
                
                bar_chart(df7_new)
            else:
                df7_new = df7.loc[(df7['Service_Provider']==operator_choice)&(df7['Technology']==technology_choice) & (df7['Test_Type']=="Download") |(df7['Test_Type']=="download")|(df7['Test_Type']=="download")]
                df7_new.groupby('Data_Speed')['LSA'].unique().explode().reset_index()
                
                bar_chart(df7_new)
        elif period_choice == "Sep21-Feb22":
            if type_choice == "UPLOAD":
                df8_new = df8.loc[(df8['Service_Provider']==operator_choice)&(df8['Technology']==technology_choice) & (df8['Test_Type']=="Upload") |(df8['Test_Type']=="UPLOAD")|(df8['Test_Type']=="upload")]
                df8_new.groupby('Data_Speed')['LSA'].unique().explode().reset_index()
                
                bar_chart(df8_new)
            else:
                df8_new = df8.loc[(df8['Service_Provider']==operator_choice)&(df8['Technology']==technology_choice) & (df8['Test_Type']=="Download") |(df8['Test_Type']=="download")|(df8['Test_Type']=="download")]
                df8_new.groupby('Data_Speed')['LSA'].unique().explode().reset_index()
                
                bar_chart(df8_new)
        elif period_choice == "Mar22-Aug22":
            if type_choice == "UPLOAD":
                df9_new = df9.loc[(df9['Service_Provider']==operator_choice)&(df9['Technology']==technology_choice) & (df9['Test_Type']=="Upload") |(df9['Test_Type']=="UPLOAD")|(df9['Test_Type']=="upload")]
                df9_new.groupby('Data_Speed')['LSA'].unique().explode().reset_index()
                
                bar_chart(df9_new)
            else:
                df9_new = df9.loc[(df9['Service_Provider']==operator_choice)&(df9['Technology']==technology_choice) & (df9['Test_Type']=="Download") |(df9['Test_Type']=="download")|(df9['Test_Type']=="download")]
                df9_new.groupby('Data_Speed')['LSA'].unique().explode().reset_index()
                
                bar_chart(df9_new)
        elif period_choice == "Sep22-Feb23":
            if type_choice == "UPLOAD":
                df10_new = df10.loc[(df10['Service_Provider']==operator_choice)&(df10['Technology']==technology_choice) & (df10['Test_Type']=="Upload") |(df10['Test_Type']=="UPLOAD")|(df10['Test_Type']=="upload")]
                df10_new.groupby('Data_Speed')['LSA'].unique().explode().reset_index()
                
                bar_chart(df10_new)
            else:
                df10_new = df10.loc[(df10['Service_Provider']==operator_choice)&(df10['Technology']==technology_choice) & (df10['Test_Type']=="Download") |(df10['Test_Type']=="download")|(df10['Test_Type']=="download")]
                df10_new.groupby('Data_Speed')['LSA'].unique().explode().reset_index()
                
                bar_chart(df10_new)
        elif period_choice == "Mar23-Aug23":
            if type_choice == "UPLOAD":
                df11_new = df11.loc[(df11['Service_Provider']==operator_choice)&(df11['Technology']==technology_choice) & (df11['Test_Type']=="Upload") |(df11['Test_Type']=="UPLOAD")|(df11['Test_Type']=="upload")]
                df11_new.groupby('Data_Speed')['LSA'].unique().explode().reset_index()
                
                bar_chart(df11_new)
            else:
                df11_new = df11.loc[(df11['Service_Provider']==operator_choice)&(df11['Technology']==technology_choice) & (df11['Test_Type']=="Download") |(df11['Test_Type']=="download")|(df11['Test_Type']=="download")]
                df11_new.groupby('Data_Speed')['LSA'].unique().explode().reset_index()
                
                bar_chart(df11_new)
        elif period_choice == "Sep24-Feb24":
            if type_choice == "UPLOAD":
                df12_new = df12.loc[(df12['Service_Provider']==operator_choice)&(df12['Technology']==technology_choice) & (df12['Test_Type']=="Upload") |(df12['Test_Type']=="UPLOAD")|(df12['Test_Type']=="upload")]
                df12_new.groupby('Data_Speed')['LSA'].unique().explode().reset_index()
                
                bar_chart(df12_new)
            else:
                df12_new = df12.loc[(df12['Service_Provider']==operator_choice)&(df12['Technology']==technology_choice) & (df12['Test_Type']=="Download") |(df12['Test_Type']=="download")|(df12['Test_Type']=="download")]
                df12_new.groupby('Data_Speed')['LSA'].unique().explode().reset_index()
                
                bar_chart(df12_new)
        elif period_choice == "Mar24-Aug24":
            if type_choice == "UPLOAD":
                df13_new = df13.loc[(df13['Service_Provider']==operator_choice)&(df13['Technology']==technology_choice) & (df13['Test_Type']=="Upload") |(df13['Test_Type']=="UPLOAD")|(df13['Test_Type']=="upload")]
                df13_new.groupby('Data_Speed')['LSA'].unique().explode().reset_index()
                
                bar_chart(df13_new)
            else:
                df13_new = df13.loc[(df13['Service_Provider']==operator_choice)&(df13['Technology']==technology_choice) & (df13['Test_Type']=="Download") |(df13['Test_Type']=="download")|(df13['Test_Type']=="download")]
                df13_new.groupby('Data_Speed')['LSA'].unique().explode().reset_index()
        else:
            pass
    
       
        
####### ....STREAMLIT MAIN CODING.....######
if selected == "About":
    about()
if selected == "Home":
    home()        
if selected == "Analysis":
    with st.sidebar:
        option = st.selectbox("ANALYSIS TYPE",["Graphical Analysis","Geospacial Analysis"])
        choice = st.radio("Select Option",['Option1','Option2','Option3'])
    if option == "Graphical Analysis": 
        analysis()    
    elif option == "Geospacial Analysis":    
        if choice =="Option1":
            folium_map(dataDf)
            line_chart(dataDf)
        elif choice == "Option2":
            folium_map(dataDf1)   
            line_chart(dataDf1) 
        else:
            folium_map(dataDf2) 
            line_chart(dataDf2)
    else:
        pass           