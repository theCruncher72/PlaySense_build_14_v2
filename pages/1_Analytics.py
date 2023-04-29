import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Analytics",
    page_icon="📈",
)





games_df_1 = pd.DataFrame({
        "Titles": st.session_state['titles'],
        "Steam": st.session_state['steam_prices'],
        "Epic": st.session_state['epic_prices'],
        "Playstation": st.session_state['ps_prices']
})



games_df_2 = pd.DataFrame({
        "Steam": st.session_state['steam_prices'],
        "Epic": st.session_state['epic_prices'],
        "Playstation": st.session_state['ps_prices']
        })
st.markdown(""" ### Tabular Comparison of all Recommendations""")
st.dataframe(games_df_1)
st.markdown(""" ### Visualization of store wise pricing""")
st.write("Line Chart")
st.line_chart(games_df_2)
st.write("Bar Chart ")
st.bar_chart(games_df_2)
