import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
import streamlit as st
from streamlit_option_menu import option_menu
import time
import locale

# Set locale to FR to display month names in French
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

# Set app settings
st.set_page_config(
    page_title="Eden Palace Cinema - Recommandation de films",
    layout="centered")

# Apply settings from CSS style file
with open("static/style.css") as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

with st.sidebar:
    st.image("client_logo.png")

    selected = option_menu(menu_title=None,
                       menu_icon="list",
                       options=["Accueil", 'Découvrir de nouveaux films'],
                       icons=['house', 'film'],
                       default_index=0,
                       styles={
                           "container": {"background-color": "transparent!important"},
                           "nav_link": {
                               "font-size": "25px"
                           }
                       }
                       )

if selected == "Accueil":
    st.image(
        "client_logo_white.png",
        width=300)
    # st.title("EDEN PALACE")
    st.divider()

    welcome_text = """
            Bonjour et bienvenue à tous les cinéphiles !
            Nous sommes ravis de vous présenter notre tout nouveau service de recommandation de films !<br><br>
            Vous êtes à la recherche de la prochaine pépite à ajouter à votre liste de films préférés ? 
            Ne cherchez plus ! Notre système de recommandation de pointe est là pour vous aider à trouver 
            votre prochain coup de cœur. Il vous suffit de saisir le nom de votre film préféré dans notre 
            onglet « Trouver des films » et laissez notre algorithme magique faire le reste. Nous sommes 
            certains que nos suggestions sauront combler vos envies et vos attentes les plus folles !<br><br>
            Que vous soyez fan de blockbusters, de films d’auteur ou de comédies romantiques, notre système 
            de recommandation vous permettra de trouver votre prochain film préféré en un rien de temps.<br><br>
            Alors, pourquoi attendre ? Rejoignez notre communauté de cinéphiles dès maintenant. 
            Nous sommes impatients de vous voir découvrir le meilleur du cinéma avec nous !
             """
    st.markdown(welcome_text, unsafe_allow_html=True)
    st.divider()

if selected == "Découvrir de nouveaux films":
    st.title("RECOMMANDATION DE FILMS")
    st.divider()

    text = """
    Plus besoin de passer des heures à chercher le film parfait pour une soirée cinéma ! 
    Notre système de recommandation de film est là pour vous aider. C’est simple, rapide et efficace !
    """
    st.write(f"{text}")
    st.divider()

    # Load movies dataset processed for NN model
    df = pd.read_csv(
        "df_movies_model.csv")
    df_actors = pd.read_csv(
        "df_actors_final.csv")

    # User input
    movie_list = df["title_fr"].tolist()
    user_movie = st.selectbox("Entrez un film de votre choix :",
                              options=sorted(movie_list))

    user_number_movies = st.radio(
        "Combien de films voulez-vous que nous vous recommandions ?",
        [3, 5, 10],
        horizontal=True)
    rec_button = st.button("C'est parti !")

    if rec_button:
        # Progress bar
        progress_text = "Nous recherchons vos prochains coups de coeur..."
        progress_bar = st.progress(0, progress_text)
        progress_bar.empty()

        for percent_complete in range(100):
            time.sleep(0.02)
            progress_bar.progress(percent_complete + 1, text=progress_text)

        progress_bar.empty()

        # Create dataframes and X
        df_user = df[df["title_fr"] == user_movie]

        X_user = df_user.select_dtypes(include="number").drop(["runtimeMinutes", "numVotes",
                                                               "budget", "revenue",
                                                               "high votes", "medium votes",
                                                               "low votes"], axis=1)

        df_movies = df[df["title_fr"] != user_movie].reset_index(drop=True)

        X_movies = df_movies.select_dtypes(include="number").drop(["runtimeMinutes", "numVotes",
                                                                   "budget", "revenue",
                                                                   "high votes", "medium votes",
                                                                   "low votes"], axis=1)

        # Normalize data
        scaler = MinMaxScaler()

        X_movies_scaled = pd.DataFrame(
            scaler.fit_transform(X_movies), columns=X_movies.columns)

        X_user_scaled = pd.DataFrame(
            scaler.transform(X_user), columns=X_user.columns)

        # Retrieve user movie genres and apply coefficients to these genres in X_movies and X_user
        df_user = df[df["title_fr"] == user_movie]
        user_movie_genres = df_user["genres"].apply(eval)

        for genre in user_movie_genres:
            X_movies_scaled[genre] = X_movies_scaled[genre] * 10
            X_user_scaled[genre] = X_user_scaled[genre] * 10

        # NearestNeighbors model
        NNmodel = NearestNeighbors(
            n_neighbors=user_number_movies).fit(X_movies_scaled)

        distance, indices = NNmodel.kneighbors(X_user_scaled)

        rec_movies_index = indices[0]

        # Display movie tabs

        # Retrieve recommended movies, order by Popularity and reset index for future use
        df_rec_movies = df_movies.loc[indices[0], :].sort_values(
            by="popularity", ascending=False).reset_index()

        # Reformat release date
        df_rec_movies["release_date"] = pd.to_datetime(
            df_rec_movies["release_date"], format="%d/%m/%Y").dt.strftime(date_format="%d %B %Y")

        # Reformat runtime
        df_rec_movies["runtimeMinutes"] = df_rec_movies["runtimeMinutes"].apply(
            lambda x: "{:d}h {:02d}min".format(*divmod(x, 60)))

        def display_movie_info(index):
            st.subheader(
                df_rec_movies.loc[index, "title_fr"].upper())

            col1, col2, col3, col4 = st.columns([1, 1, 2, 1])
            with col1:
                imdb_rating = df_rec_movies.loc[index, "averageRating"]
                st.metric("Note IMDB", "{}/10".format(imdb_rating))
                # imdb_stars = int(round(imdb_rating)) * "⭐"
                # st.write(f"{imdb_stars}")
            with col2:
                popularity_rating = df_rec_movies.loc[index, "popularity"]
                st.metric("Popularité", round(popularity_rating, 1))

            col5, col6 = st.columns([1, 2])
            with col5:
                try:
                    st.image(
                        df_rec_movies.loc[index, "poster_url"])
                except:
                    st.error("Poster non disponible")

            with col6:
                date_sortie = df_rec_movies.loc[index, "release_date"]
                st.write(f"**Date de sortie** : {date_sortie}")

                genres = df_rec_movies.loc[index, "genres"]
                genres = eval(genres)
                genre_list = ", ".join(genres)
                st.write(f"**Genres** : {genre_list}")

                st.write("**Durée** :",
                         df_rec_movies.loc[index, "runtimeMinutes"])

                tconst = df_rec_movies.loc[index, 'tconst']
                condition = df_actors["tconst_in_db"].str.contains(tconst)
                movie_actors = df_actors[condition]["primaryName"].tolist()
                sorted_actors = sorted(movie_actors)
                actor_list = ", ".join(sorted_actors)
                st.write(f"**Acteurs·trices** : {actor_list}")

                st.write("**SYNOPSIS**")
                synopsis = df_rec_movies.loc[index, "overview"]
                st.markdown(
                    f'<div style="text-align: justify;">{synopsis}</div>', unsafe_allow_html=True)

        rec_movies = []
        for i in range(1, len(rec_movies_index)+1):
            rec_movies.append(f"Film {i}")

        movie_index = 0
        for tab in st.tabs(rec_movies):
            with tab:
                display_movie_info(movie_index)
            movie_index += 1
