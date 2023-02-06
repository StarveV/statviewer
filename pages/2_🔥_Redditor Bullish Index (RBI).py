import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from streamlit_option_menu import option_menu
from pymongo import MongoClient
from dotenv import load_dotenv

# Load the environment
load_dotenv()
# Connect to MongoDB
mongo_key=os.getenv('mongo_key')
client = MongoClient(mongo_key)

db = client['heatmap']
collection_post = db['wsb_heatmap']
collection_post2 = db['investing_heatmap']
collection_post3 = db['options_heatmap']

#  ---- settings ----
page_title = "Redditor Bullish Index (RBI)"
page_icon = ":fire:"   #emoji from https://www.webfx.com/tools/emoji-cheat-sheet/ 
layout = "wide"
#  ----          ----

st.set_page_config(page_title = page_title, page_icon = page_icon, layout = layout)
st.title(page_icon + " " + page_title)

st.markdown("""
<style>
.big-font {
    font-size:20px !important;
}
</style>
""", unsafe_allow_html=True)

# Heading
st.markdown("#### The Redditor Bullish Index (RBI) measures retail investors' bullish or bearish outlook based on sentiment analysis of relevant subreddit posts over the past seven days.")
with st.expander("What is RBI?"):
    st.markdown(" The RBI draws on the concepts of the Relative Strength Index (RSI) and the Volatility Index (VIX) and seeks to quantify retail investors' emotional state. The sentiment score is calculated by utilizing two distinct deep learning models, which analyze all entities identified in the posts of the designated subreddit during the past seven days. The database is updated on a daily basis to ensure the most accurate representation of retail investor sentiment. For more detailed information regarding the calculation of the RBI, please visit the 'About' page.")
#---------
# Read in the data from MongoDB
original_cursor = collection_post.find({})
wsb_df = pd.DataFrame(list(original_cursor))

original_cursor2 = collection_post2.find({})
investing_df = pd.DataFrame(list(original_cursor2))

original_cursor3 = collection_post3.find({})
options_df = pd.DataFrame(list(original_cursor3))


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

if selected=="r/Wallstreetbet":
    df= wsb_df

if selected=="r/Investing":
    df= investing_df

if selected=="r/Options":
    df= options_df

# Calculate the sum of weighted occurrence
sum_weighted_occurrence = df['total_occurrence'].sum()

# Calculate the weighted average score
df['weighted_average_score'] = df['RBI'] * (df['total_occurrence'] / sum_weighted_occurrence)

RBI = df['weighted_average_score'].sum()

# Gauge chart--------------
# Define the data to be plotted and the parameters for the chart:
def plot_gauge(value, selected, max_value):
    fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = value,
    title = {"text": 'RBI'},
    domain = {'x': [0, 1], 'y': [0, 1]},
    gauge = {
        'axis': {'range': [-100, 100]},
        'bar': {'color': "#ACACAC", 'thickness': 0},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [-100, -75], 'color': '#E97777'},
            {'range': [-75, -50], 'color': '#FF9F9F'},
            {'range': [-50, -25], 'color': '#FCDDB0'},
            {'range': [-25, 0], 'color': '#FFFAD7'},
            {'range': [0, 25], 'color': '#DBE8CC'},
            {'range': [25, 50], 'color': '#A4BE7B'},
            {'range': [50, 75], 'color': '#5F8D4E'},
            {'range': [75, 100], 'color': '#285430'},],
        'threshold': {
            'line': {'color': "#50577A", 'width': 8},
            'thickness': 0.8,
            'value': value
        }
    }))
    return fig


value = RBI
title = ("")
st.plotly_chart(plot_gauge(value, title, 100))
