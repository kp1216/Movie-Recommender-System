import streamlit as st
import pickle
import pandas as pd
import requests

st.image("https://user-images.githubusercontent.com/33485020/108069438-5ee79d80-7089-11eb-8264-08fdda7e0d11.jpg")

# Load data
movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=75d69d667bf2006d5bde7269cb75b3e7&append_to_response=videos"
    response = requests.get(url)
    data = response.json()
    if data.get("poster_path"):
        return "https://image.tmdb.org/t/p/w500" + data["poster_path"]
    else:
        return "https://via.placeholder.com/500x750?text=No+Image+Available"

def fetch_movie_url(movie_id):
    return f"https://www.themoviedb.org/movie/{movie_id}"  # URL to the movie details page

def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    recommended_movies_urls = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_urls.append(fetch_movie_url(movie_id))  # Get the URL for each movie

    return recommended_movies, recommended_movies_posters, recommended_movies_urls

# Streamlit app
st.title("Movies Recommender System")

selected_movie_name = st.selectbox("ENTER MOVIE NAME", movies["title"].values)

if st.button("Recommend"):
    names, posters, urls = recommend(selected_movie_name)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            # Make each poster image clickable and link to the movie's details page
            col.markdown(
                f'<a href="{urls[idx]}" target="_blank">'
                f'<img src="{posters[idx]}" style="width:100%;">'
                f'</a>',
                unsafe_allow_html=True
            )
            col.markdown(f"<h4 style='text-align: center;'>{names[idx]}</h4>", unsafe_allow_html=True)
