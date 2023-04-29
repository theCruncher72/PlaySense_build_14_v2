import streamlit as st
import pandas as pd
import numpy as np
import re
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import altair as alt

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
)




def get_st_button_a_tag(url_link, button_name):
    """
    generate html a tag
    :param url_link:
    :param button_name:
    :return:
    """
    return f'''
    <a href={url_link}><button style="
    fontWeight: 400;
    padding: 0.25rem 0.75rem;
    borderRadius: 0.25rem;
    lineHeight: 1.6;
    width: auto;
    text-align: center; 
    margin: auto;
    userSelect: none;
    backgroundColor: #FFFFFF;
    border: 1px solid rgba(49, 51, 63, 0.2);">{button_name}</button></a>
    '''


def extract_app_id(url):
    pattern = r"\/app\/(\d+)\/"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None


@st.cache_data
def load_data():
    games_dict = pickle.load(open('test_pkl.pkl', 'rb'))
    df = pd.DataFrame(games_dict)
    return df

df = load_data()


tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(df["tags"])


cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)


def get_recommendations(title, cosine_sim=cosine_sim):

    idx = df[df["title"] == title].index[0]


    sim_scores = list(enumerate(cosine_sim[idx]))


    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)


    sim_scores = sim_scores[1:11]


    game_indices = [i[0] for i in sim_scores]


    return df["title"].iloc[game_indices]


st.sidebar.header("PlaySense")
user_input = st.sidebar.selectbox(
    'Enter the name of the game:',
    df['title'].values)
button = st.sidebar.button("Submit")
st.session_state["uinput"] = user_input

st.session_state['steam_prices'] = []
Dump1 = df[df['title'] == user_input]['steam_price'].iloc[0]
st.session_state['steam_prices'].append(Dump1)
st.session_state['epic_prices'] = []
Dump2 = df[df['title'] == user_input]['epic_price'].iloc[0]
st.session_state['epic_prices'].append(Dump2)
st.session_state['ps_prices'] = []
Dump3 = df[df['title'] == user_input]['ps_price'].iloc[0]
st.session_state['ps_prices'].append(Dump3)
st.session_state['titles'] = []
st.session_state['titles'].append(user_input)




if button:
    st.title(f"You entered: {user_input}")

    left_co, right_co = st.columns(2)
    with left_co:
        game_id = extract_app_id(df[df['title'] == user_input]['steam_url'].iloc[0])
        url = "https://cdn.cloudflare.steamstatic.com/steam/apps/TEST/header.jpg"
        new_url = url.replace("TEST", game_id)
        st.image(new_url)
        # st.image("https://cdn.akamai.steamstatic.com/steam/apps/2620/header.jpg?t=1646762112")
    with right_co:
        tab1, tab2, tab3, tab4 = st.tabs(["Description", "Publisher", "Genre","Release"])
        with tab1:

            st.write(f"Description: {df[df['title'] == user_input]['descrip'].iloc[0]}")
        with tab2:
            st.write(f"Publisher: {df[df['title'] == user_input]['publisher'].iloc[0]}")
        with tab3:
            st.write(f"Genre: {df[df['title'] == user_input]['categories'].iloc[0]}")
        with tab4:
            st.write(f"Date Released : {df[df['title'] == user_input]['release'].iloc[0]}")


    sub_left, sub_right = st.columns(2)
    with sub_left:
        st.image("https://support.steampowered.com/images/faq/steam_universe/Hardware_SteamLogo_Banner.png")
    with sub_right:
        st.markdown(get_st_button_a_tag(df[df['title'] == user_input]['steam_url'].iloc[0], 'Click here🔗'),
                    unsafe_allow_html=True)
        st.write(f"Price: ₹{df[df['title'] == user_input]['steam_price'].iloc[0]}")
    sub_left, sub_right = st.columns(2)
    with sub_left:
        st.image("https://media.sidefx.com/uploads/article/epic-games-invests-in-sidefx/epic_logo_black_banner3.jpg")
    with sub_right:
        st.markdown(get_st_button_a_tag(df[df['title'] == user_input]['epic_url'].iloc[0], 'Click here🔗'),
                    unsafe_allow_html=True)
        st.write(f"Price: ₹{df[df['title'] == user_input]['epic_price'].iloc[0]}")
    sub_left, sub_right = st.columns(2)
    with sub_left:
        st.image("https://mmos.com/wp-content/uploads/2021/03/playstation-store-logo-banner.jpg")
    with sub_right:
        st.markdown(get_st_button_a_tag(df[df['title'] == user_input]['ps_url'].iloc[0], 'Click here🔗'),
                    unsafe_allow_html=True)
        st.write(f"Price: ₹{df[df['title'] == user_input]['ps_price'].iloc[0]}")



    game_stores = ["Steam", "Epic Games", "PlayStation Store"]
    counts = [int(df[df['title'] == user_input]['steam_price'].iloc[0]), int(df[df['title'] == user_input]['epic_price'].iloc[0]), int(df[df['title'] == user_input]['ps_price'].iloc[0])]

    #altair-bar-chart
    games_df = pd.DataFrame({
        "Store": game_stores,
        "Prices": counts,
    })

    chart = alt.Chart(games_df).mark_bar().encode(
        y='Store',
        x='Prices'
    ).properties(
        width=550,
        height=200,
    )

    st.altair_chart(chart)




    st.write("---")
    st.subheader("Here are some games you might like:")
    recommendations = get_recommendations(user_input)
    for i, game in enumerate(recommendations):
        st.write(f"{i + 1}. {game}")
        st.session_state['titles'].append(game)
        left_co, right_co = st.columns(2)
        with left_co:
            game_id = extract_app_id(df[df['title'] == game]['steam_url'].iloc[0])
            url = "https://cdn.cloudflare.steamstatic.com/steam/apps/TEST/header.jpg"
            new_url = url.replace("TEST", game_id)
            st.image(new_url)
            # st.image("https://cdn.akamai.steamstatic.com/steam/apps/2620/header.jpg?t=1646762112")
        with right_co:
            tab1, tab2, tab3, tab4 = st.tabs(["Description", "Publisher", "Genre", "Release"])
            with tab1:

                st.write(f"Description: {df[df['title'] == game]['descrip'].iloc[0]}")
            with tab2:
                st.write(f"Publisher: {df[df['title'] == game]['publisher'].iloc[0]}")
            with tab3:
                st.write(f"Genre: {df[df['title'] == game]['categories'].iloc[0]}")
            with tab4:
                st.write(f"Date Released : {df[df['title'] == game]['release'].iloc[0]}")
        # st.write("---")
        sub_left, sub_right = st.columns(2)
        with sub_left:
            st.image("https://support.steampowered.com/images/faq/steam_universe/Hardware_SteamLogo_Banner.png")
        with sub_right:
            st.markdown(get_st_button_a_tag(df[df['title'] == game]['steam_url'].iloc[0], 'Click here🔗'),
                        unsafe_allow_html=True)
            st.write(f"Price: ₹{df[df['title'] == game]['steam_price'].iloc[0]}")
            Bump1 = df[df['title'] == game]['steam_price'].iloc[0]
            st.session_state['steam_prices'].append(Bump1)
        sub_left, sub_right = st.columns(2)
        with sub_left:
            st.image(
                "https://media.sidefx.com/uploads/article/epic-games-invests-in-sidefx/epic_logo_black_banner3.jpg")
        with sub_right:
            st.markdown(get_st_button_a_tag(df[df['title'] == game]['epic_url'].iloc[0], 'Click here🔗'),
                        unsafe_allow_html=True)
            st.write(f"Price: ₹{df[df['title'] == game]['epic_price'].iloc[0]}")
            Bump2 = df[df['title'] == game]['epic_price'].iloc[0]
            st.session_state['epic_prices'].append(Bump2)
        sub_left, sub_right = st.columns(2)
        with sub_left:
            st.image("https://mmos.com/wp-content/uploads/2021/03/playstation-store-logo-banner.jpg")
        with sub_right:
            st.markdown(get_st_button_a_tag(df[df['title'] == game]['ps_url'].iloc[0], 'Click here🔗'),
                        unsafe_allow_html=True)
            st.write(f"Price: ₹{df[df['title'] == game]['ps_price'].iloc[0]}")
            Bump3 = df[df['title'] == game]['ps_price'].iloc[0]
            st.session_state['ps_prices'].append(Bump3)

        game_stores = ["Steam", "Epic Games", "PlayStation Store"]
        counts = [int(df[df['title'] == game]['steam_price'].iloc[0]),
                  int(df[df['title'] == game]['epic_price'].iloc[0]),
                  int(df[df['title'] == game]['ps_price'].iloc[0])]

        games_df_2 = pd.DataFrame({
            "Store": game_stores,
            "Prices": counts,
        })

        chart = alt.Chart(games_df_2).mark_bar().encode(
            y='Store',
            x='Prices'
        ).properties(
            width=550,
            height=200,
        )

        st.altair_chart(chart)



        st.write("---")
else:
    st.title("Welcome to PlaySense")
    st.write("Please enter a game title in the sidebar and click on Submit.")