import streamlit as st
import pickle
import pandas as pd
import  requests

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=e8286ea906682bbd896ec7e2972d563d&language=en-US'.format(movie_id))

    data=response.json()

    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie_name):
    movie_index = movies[movies['original_title'] == movie_name].index[0]

    L = sorted(list(enumerate(similarity_matrix[movie_index])), reverse=True, key=lambda x: x[1])

    recommended_movies=[]
    recommended_movies_posters=[]


    for i in L[1:6]:
        movie_id=movies.iloc[i[0]]['id']

        recommended_movies.append(movies.iloc[i[0]]['original_title'])
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movies_posters

similarity_matrix=pickle.load(open('similarity_matrix.pkl','rb'))

movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

st.title('Movie Recommender System')

selected_movie_name=st.selectbox('Which movie have you recently watched?',
                    movies['original_title'].values)

if st.button('Recommend'):
    names,posters=recommend(selected_movie_name)
    col1,col2,col3,col4,col5=st.beta_columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])