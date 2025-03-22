import streamlit as st
import pickle
import pandas as pd
import requests
import os

# Function to download the similarity matrix
@st.cache_resource
def download_similarity_matrix():
    if not os.path.exists('similarity.pkl'):
        with st.spinner('Downloading similarity matrix... This might take a moment.'):
            url = "https://cdaegpf5rescy0ss.public.blob.vercel-storage.com/similarity-CfXh0OhRRlBOgCTxQ7gKmjPdwWtvyn.pkl"
            r = requests.get(url, allow_redirects=True)
            with open('similarity.pkl', 'wb') as f:
                f.write(r.content)
        st.success('Download complete!')
    
    # Load the similarity matrix using your existing code
    import pickle
    with open('similarity.pkl', 'rb') as f:
        return pickle.load(f)


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=4395fff7ad332072b98941c4ef249f15&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/"+poster_path
    return full_path


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = download_similarity_matrix()

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True, key = lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Please Select the Movie for which you want the recommendation for : ',
    movies['title'].values)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])