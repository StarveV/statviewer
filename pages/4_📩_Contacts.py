import streamlit as st
from pathlib import Path

#  ---- settings ----
page_title = "Contacts"
page_icon = ":incoming_envelope:"   #emoji from https://www.webfx.com/tools/emoji-cheat-sheet/ 
layout = "wide"
#  ----          ----

st.set_page_config(page_title = page_title, page_icon = page_icon, layout = layout)
st.title(page_icon + " " + page_title)


# load the style data from css file
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir/"page_style.css"

with open(css_file) as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

st.caption('---')
st.markdown('##### For any enquires or bug reporting, please contact with the following email:')
st.markdown('##### wchwongg@gmail.com')

st.caption('### Updates to this page will be available soon.')