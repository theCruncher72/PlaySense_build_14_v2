import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Analytics",
    page_icon="📈",
)


# steam_prices = []
# epic_prices = []
# playstation_prices = []

# recommendations_with_prices = recommendations.join(df["steam_price"].to_list())
# st.bar_chart(recommendations_with_prices["steam_price"])

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


st.dataframe(games_df_1)

st.line_chart(games_df_2)

st.bar_chart(games_df_2)
