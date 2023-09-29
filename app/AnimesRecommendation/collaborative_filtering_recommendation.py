import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import pickle

def get_recommendation(anime_title):
    # doing recommendation
    # user_anime = anime[anime['Title']=='Sen to Chihiro no Kamikakushi']
    anime = pd.read_csv('data/cleaned_anime_data.csv', encoding='latin')
    # read rating_matrix
    with open('data/rating_matrix.pkl', 'rb') as rating_matrix_file:
        rating_matrix = pickle.load(rating_matrix_file)
    # read recommender
    with open('data/recommender.pkl', 'rb') as recommender_file:
        recommender = pickle.load(recommender_file)

    user_anime = anime[anime['Title']==anime_title]
    user_anime_index = np.where(rating_matrix.index==int(user_anime['Anime_id']))[0][0]
    user_anime_ratings = rating_matrix.iloc[user_anime_index]
    user_anime_ratings_reshaped = user_anime_ratings.values.reshape(1,-1)
    # the ratings will be plotted and will return 11 indices and distances of nearest neighbors
    # distances, indices = recommender.kneighbors(user_anime_ratings_reshaped,n_neighbors=16)
    _, indices = recommender.kneighbors(user_anime_ratings_reshaped,n_neighbors=16)
    nearest_neighbors_indices = rating_matrix.iloc[indices[0]].index[1:]
    nearest_neighbors = pd.DataFrame({'Anime_id': nearest_neighbors_indices})
    result = pd.merge(nearest_neighbors,anime,on='Anime_id',how='left')
    return result


if __name__ == "__main__":
    # train once and use forever until new data come
    rating = pd.read_csv('data/rating.csv', encoding='latin')
    anime = pd.read_csv('data/cleaned_anime_data.csv', encoding='latin')

    anime_rating = rating.groupby(by = 'anime_id').count()
    anime_rating = anime_rating['rating'].reset_index().rename(columns={'rating':'rating_count'})
    final_anime = anime_rating[anime_rating['rating_count']>50]
    user_rating = rating.groupby(by='user_id').count()
    user_rating = user_rating['rating'].reset_index().rename(columns={'rating':'rating_count'})
    final_user = user_rating[user_rating['rating_count']>80]
    final_anime_dt = rating[rating['anime_id'].isin(final_anime['anime_id'])]
    final_dt = final_anime_dt[final_anime_dt['user_id'].isin(final_user['user_id'])]
    rating_matrix = final_dt.pivot_table(index='anime_id',columns='user_id',values='rating').fillna(0)
    csr_rating_matrix =  csr_matrix(rating_matrix.values)
    # collaborative filltering
    recommender = NearestNeighbors(metric='cosine') 
    recommender.fit(csr_rating_matrix)

    # saved rating_matrix and recommender
    with open('data/rating_matrix.pkl', 'wb') as rating_matrix_file:
        pickle.dump(rating_matrix, rating_matrix_file)
    with open('data/recommender.pkl', 'wb') as recommender_file:
        pickle.dump(recommender, recommender_file)