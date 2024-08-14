import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=75d69d667bf2006d5bde7269cb75b3e7&append_to_response=videos"
    response = requests.get(url)

    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data["poster_path"]


def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies, recommended_movies_posters

st.title("Movies Recommender System")
selected_movie_name = st.selectbox("ENTER MOVIE NAME", movies["title"].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        col.markdown(f"<h5 style='text-align: center;'>{names[idx]}</h5>", unsafe_allow_html=True)
        col.image(posters[idx])