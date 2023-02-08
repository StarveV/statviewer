import streamlit as st
import plotly.express as px
import pandas as pd
import datetime
import os
from streamlit_option_menu import option_menu
from pymongo import MongoClient
from pathlib import Path
from dotenv import load_dotenv


# Load the environment
load_dotenv()
# Connect to MongoDB
mongo_key=os.getenv('mongo_key')
client = MongoClient(mongo_key)

db = client['heatmap']
collection = db['wsb_heatmap']
collection2 = db['investing_heatmap']
collection3 = db['options_heatmap']

collection_post = db['wsb_spacy']
collection_post2 = db['investing_spacy']
collection_post3 = db['options_spacy']
#  ---- settings ----
page_title = "RBI Heatmap/Treemap"
page_icon = "📊"   #emoji from https://www.webfx.com/tools/emoji-cheat-sheet/ 
layout = "wide"


#  ----          ----

st.set_page_config(page_title = page_title, page_icon = page_icon, layout = layout,initial_sidebar_state='expanded')
st.title(page_icon + " " + page_title)


st.markdown("""
<style>
.big-font {
    font-size:20px !important;
}
</style>
""", unsafe_allow_html=True)

# load the style data from css file
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir/"page_style.css"

with open(css_file) as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
    

# Heading
st.subheader("The treemap below indicate the most discussed stocks and commodiity acorss different subreddit, and how bullish and bearish redditors are") 

with st.expander("What is RBI?"):
    st.markdown(" The RBI draws on the concepts of the Relative Strength Index (RSI) and the Volatility Index (VIX) and seeks to quantify retail investors' emotional state. The sentiment score is calculated by utilizing two distinct deep learning models, which analyze all entities identified in the posts of the designated subreddit during the past seven days. The database is updated on a daily basis to ensure the most accurate representation of retail investor sentiment. For more detailed information regarding the calculation of the RBI, please visit the 'About' page.")

st.subheader(" ")

# Horizontal navigation bar for choosing different subreddit
selected = option_menu(
    menu_title=None,
    options=["r/Wallstreetbet", "r/Investing", "r/Options"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"2px"},        
    }
)

# Treemap
# Loading screen
with st.spinner('Generating Heatmap...'):
    # -------r/WSB-------
    if selected=="r/Wallstreetbet":
        
        no_post = collection_post.count_documents({})
        no_ent = collection.count_documents({})

        # Find documents in the collection
        heatmap_data = list(collection.find())

        # Convert the data to a Pandas DataFrame
        heatmap_df = pd.DataFrame(heatmap_data)
        heatmap_df = heatmap_df.dropna()

        heatmap_df.sort_values(by=['ticker'],inplace=True)

        # Create a treemap
        fig = px.treemap (heatmap_df, path=['ticker'], values='total_occurrence',
                        color='RBI',
                        color_continuous_scale=['#e30819', "#3c3c3d", '#19e308'],
                        color_continuous_midpoint=0, labels='RBI')

        # Display the RBI of each ticker
        fig.data[0].customdata = heatmap_df[['ticker', 'total_occurrence', 'RBI']].round(2)
        fig.data[0].texttemplate = "%{label}<br>%{customdata[2]}"


        fig.update_traces(textposition="middle center", 
                        selector=dict(type='treemap'))

        #Custom borders
        fig.update_layout(margin=dict(l=0,r=0,t=20,b=5), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        # Show the treemap in the website
        st.plotly_chart(fig, use_container_width=True)


    # -------r/Investing-------
    if selected=="r/Investing":

        no_post = collection_post2.count_documents({})
        no_ent = collection2.count_documents({})

        # Find documents in the collection
        heatmap_data = list(collection2.find())

        # Convert the data to a Pandas DataFrame
        heatmap_df = pd.DataFrame(heatmap_data)
        heatmap_df = heatmap_df.dropna()

        heatmap_df.sort_values(by=['ticker'],inplace=True)

        # Create a treemap
        fig = px.treemap (heatmap_df, path=['ticker'], values='total_occurrence',
                        color='RBI',
                        color_continuous_scale=['#e30819', "#3c3c3d", '#19e308'],
                        color_continuous_midpoint=0, labels='RBI')

        # Display the RBI of each ticker
        fig.data[0].customdata = heatmap_df[['ticker', 'total_occurrence', 'RBI']].round(2)
        fig.data[0].texttemplate = "%{label}<br>%{customdata[2]}"


        fig.update_traces(textposition="middle center", 
                        selector=dict(type='treemap'))

        #Custom borders
        fig.update_layout(margin=dict(l=0,r=0,t=20,b=5), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        # Show the treemap in the website
        st.plotly_chart(fig, use_container_width=True)


    # -------r/Options-------
    if selected=="r/Options":

        no_post = collection_post3.count_documents({})
        no_ent = collection3.count_documents({})

        # Find documents in the collection
        heatmap_data = list(collection3.find())

        # Convert the data to a Pandas DataFrame
        heatmap_df = pd.DataFrame(heatmap_data)
        heatmap_df = heatmap_df.dropna()

        heatmap_df.sort_values(by=['ticker'],inplace=True)

        # Create a treemap
        fig = px.treemap (heatmap_df, path=['ticker'], values='total_occurrence',
                        color='RBI',
                        color_continuous_scale=['#e30819', "#3c3c3d", '#19e308'],
                        color_continuous_midpoint=0, labels='RBI')

        # Display the RBI of each ticker
        fig.data[0].customdata = heatmap_df[['ticker', 'total_occurrence', 'RBI']].round(2)
        fig.data[0].texttemplate = "%{label}<br>%{customdata[2]}"


        fig.update_traces(textposition="middle center", 
                        selector=dict(type='treemap'))

        #Custom borders
        fig.update_layout(margin=dict(l=0,r=0,t=20,b=5), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        # Show the treemap in the website
        st.plotly_chart(fig, use_container_width=True) 


    # 3 Card to display related data
    newest_entry = collection_post.find_one(sort=[("date", -1)])
    update_date = newest_entry["date"]
    update_date = datetime.datetime.strptime(update_date, "%Y-%m-%d %H:%M:%S")
    update_date = update_date.strftime("%d/%m/%Y %H:%M")

    col1, col2, col3 = st.columns(3)
    col1.metric("Number of Post:", no_post)
    col2.metric("Number of Entities Recognised:", no_ent)
    col3.metric("Last Updated (GMT):", update_date)