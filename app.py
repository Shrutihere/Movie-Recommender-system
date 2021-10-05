import streamlit as st
import pickle
import requests

new_df = pickle.load(open("df.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))

def fetch_poster(movie_name):
    response = requests.get(f'https://api.themoviedb.org/3/search/movie?api_key=15fd7b73ee00a6c0edcf28d56b09d802&language=en-US&query={movie_name}')
    data = response.json()
    return data['results'][0]['poster_path']

def recommend(movie, similarity):
    index_pos = new_df[new_df['title'] == movie].index[0]
    movie_list = sorted(list(enumerate(similarity[index_pos])), key=lambda x:x[1], reverse=True)[1:6]
    l = []
    for item in movie_list:
        l.append(new_df.iloc[item[0]]['title'])
    return l

st.title("Movie Recommendor System")
selected_movie = st.selectbox("Select Movie: ", new_df['title'].values)
button = st.button("Go")
if button:
    result = recommend(selected_movie, similarity)

    col1, col2, col3, col4, col5 = st.beta_columns(5)
    cols = [col1, col2, col3, col4, col5]
    for i in range(len(result)):
        with cols[i]:
            title = st.text(result[i])
            poster = st.image('https://image.tmdb.org/t/p/w500'+fetch_poster(result[i]))