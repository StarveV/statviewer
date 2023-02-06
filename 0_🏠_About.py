import streamlit as st
import plotly.express as px
import json
import requests
from streamlit_option_menu import option_menu
from pathlib import Path
from streamlit_lottie import st_lottie

#  ---- settings ----
page_title = "About"
page_icon = "🏠"   #emoji from https://www.webfx.com/tools/emoji-cheat-sheet/ 
layout = "wide"


#  ----          ----

st.set_page_config(page_title = page_title, page_icon = page_icon, layout = layout,initial_sidebar_state='expanded')


st.sidebar.success("Select a page")


st.markdown("""
<style>
.big-font {
    font-size:20px !important;
}
</style>
""", unsafe_allow_html=True)

# load the style data from css file
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir/"styles"/"main.css"
with open(css_file) as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
    

# Heading
about1, about2 = st.columns([7,3])
with about1:
    st.markdown(' ')
    st.title('Statviewer.app')
    st.markdown(' ')
    st.markdown('###### StatViewer aims to simplify financial analysis by providing comprehensive, alternative statistics with unique data, accessible through an intuitive user interface, making investment analysis accessible to a wider audience.')

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
lottie_stat = load_lottieurl('https://assets5.lottiefiles.com/packages/lf20_ic37y4kv.json')

with about2:
    # Data animation
    st_lottie(lottie_stat,height=200)

st.caption('---')

# RBI heatmap
st.markdown('### RBI Heatmap/Treemap')
st.write('''
    This website collects data by scraping the designated subreddit, including r/wallstreetbet, to retrieve all 
    posts and threads posted in the past seven days. The data is stored in MongoDB and undergoes entity recognition 
    and sentiment analysis using two distinct deep learning models, SPACY and a BERT-based model. The heat map/tree 
    map displays the most-discussed tickers and companies in the selected subreddit, along with their respective RBI 
    for the past seven days. This provides a clear and intuitive way to identify the most-discussed stocks and understand 
    the bullish or bearish sentiment of redditors towards them.
''')
st.caption('---')

# RBI
st.markdown('### Redditor Bullish Index (RBI).')
st.write('''
    The Redditor Bullish Index (RBI). is inspired by the Relative Strength Index (RSI) 
    and the Volatility Index (VIX) and seeks to measure retail investors' emotions. The sentiment 
    score is determined by analyzing all entities identified in posts within the designated subreddit 
    over the past seven days. Two distinct deep learning models, a SPACY model for entity recognition 
    and a BERT-based model for sentiment analysis, are used to extract the discussed stock or company 
    and perform sentiment analysis, respectively. The weighted score of the stock's occurrence and sentiment 
    score is then calculated to form the RBI.

    Compared to traditional financial indicators, the RBI provides a more accurate reflection of retail investors' 
    emotions and highlights the most-discussed stocks among retail investors. However, it is important to note that 
    the RBI may lag in time and may not accurately reflect investors' emotions at a specific time frame, as it is based 
    on all posts from the past seven days.
''')
st.caption("---")

# Financial Visualiser
st.markdown('### Financial Visualiser')
st.write('''
    The financial visualizer on statViewer.app offers an intuitive interface for investors to visualize the historical 
    performance of any publicly traded company. Rather than relying on traditional, spreadsheet-style data frames, StatViewer.app 
    provides an easy-to-use graphical user interface (GUI) that allows users to easily explore and comprehend past performance with 
    a quick glance. This enhances the ability of investors to understand the financial performance of companies they are interested in.
''')
st.caption("---")