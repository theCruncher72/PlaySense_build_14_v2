import streamlit as st

st.set_page_config(
    page_title="About",
    page_icon="📄",
)

st.write("# PlaySense 👋")

st.sidebar.success("Select a Home to find some games...")

st.markdown(
    """
    PlaySense is a web app that aims to provide content-based recommendations of video games based on user input from different game distribution platforms such as Steam, Epic Games, etc.
    The website also gives price analytics of each game that is recommended, such as the current price, the lowest price, the highest price, the price history and redirects the user to a page where they can buy the recommended games from the respective platforms while giving an overview of the games recommended, such as the genre, the rating, the description, and the screenshots.
    **👈 Select Home to try it out** 
    ### Home
    - Search for a game
    - Get pricing and other information of the game and other similar games
    
    ### Analytics
    - Visualization of all the data obtained from your search
"""
)
