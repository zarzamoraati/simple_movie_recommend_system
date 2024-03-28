import streamlit as st 
import pickle
import requests


# API
API_TMDB_KEY="103866fd8ae0a7f3f6767d60b38857d5"
# Loading movies
list_movies=pickle.load(open("model/movies_list.pkl","rb"))
# print(list_movies.columns)

# Obtaining values for title field
movie_list_title=list_movies.title.values
# print(list_movies) Cheking movies 

# Loading similarity matrix 
similarity_mtx=pickle.load(open("model/similarity_matrix.pkl","rb"))

def fetching_posters(movie_id):
   url_imdb = "https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US".format(movie_id,API_TMDB_KEY)

   data=requests.get(url_imdb)
   data=data.json()
   poster_path=data["poster_path"]
   return  "https://image.tmdb.org/t/p/w500"+poster_path


def recommendation_movies(movie_name:str,n_movies:int):
  
  idx_movie=list_movies[list_movies["title"]==movie_name].index[0]
  
  distance=sorted(list(enumerate(similarity_mtx[idx_movie])),reverse=True,key=lambda x:x[1])
  
  recommend_movies=[]
  poster_movies=[]

  for (idx,_) in distance[1:n_movies+1]:
    movie_id=list_movies.iloc[idx].id
    movie_poster=fetching_posters(movie_id)
    poster_movies.append(movie_poster)
    recommend_movies.append(list_movies.iloc[idx].title)

  return recommend_movies,poster_movies


st.header("Movie Recommender Ssytem")

movie_selected=st.selectbox("Select a movie",movie_list_title)
n_movies=st.slider("Number of recommendations?",min_value=1,max_value=10)

if st.button("Show Recommend"):
    recommend_movies,poster_movies=recommendation_movies(movie_selected,n_movies=n_movies)
    tuple_cols=st.columns(len(recommend_movies))
    
    for idx,col in enumerate(tuple_cols):
      with col:
        st.text(recommend_movies[idx])
        st.image(poster_movies[idx])



