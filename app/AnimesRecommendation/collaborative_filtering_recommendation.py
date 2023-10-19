import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import pickle
import os
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

current_directory = os.getcwd()

def train_recommendation_system():
    # Load anime and rating data
    rating = pd.read_csv(os.path.join(current_directory, 'data/rating.csv'), encoding='latin')
    anime = pd.read_csv(os.path.join(current_directory, 'data/cleaned_anime_data.csv'), encoding='latin')

    # Filter anime and users based on rating counts
    anime_rating = rating.groupby(by='anime_id').count()
    anime_rating = anime_rating['rating'].reset_index().rename(columns={'rating': 'rating_count'})
    final_anime = anime_rating[anime_rating['rating_count'] > 50]
    user_rating = rating.groupby(by='user_id').count()
    user_rating = user_rating['rating'].reset_index().rename(columns={'rating': 'rating_count'})
    final_user = user_rating[user_rating['rating_count'] > 80]
    print(rating.columns)
    print(final_anime.columns)
    final_anime_dt = rating[rating['anime_id'].isin(final_anime['anime_id'])]
    final_dt = final_anime_dt[final_anime_dt['user_id'].isin(final_user['user_id'])]

    # Create a rating matrix
    rating_matrix = final_dt.pivot_table(index='anime_id', columns='user_id', values='rating').fillna(0)
    csr_rating_matrix = csr_matrix(rating_matrix.values)

    # Train collaborative filtering recommender
    recommender = NearestNeighbors(metric='cosine')
    recommender.fit(csr_rating_matrix)

    # Save rating matrix and recommender to files
    with open(os.path.join(current_directory, 'data/rating_matrix.pkl'), 'wb') as rating_matrix_file:
        pickle.dump(rating_matrix, rating_matrix_file)
    with open(os.path.join(current_directory, 'data/recommender.pkl'), 'wb') as recommender_file:
        pickle.dump(recommender, recommender_file)

def get_recommendation(anime_title):
    print(">>>>>>>>>>>>>>Calling get_recommendation")
    try:
        # Load anime data
        anime = pd.read_csv(os.path.join(current_directory, 'data/cleaned_anime_data.csv'), encoding='latin')
        # Load rating matrix and recommender
        with open(os.path.join(current_directory, 'data/rating_matrix.pkl'), 'rb') as rating_matrix_file:
            rating_matrix = pickle.load(rating_matrix_file)
        with open(os.path.join(current_directory, 'data/recommender.pkl'), 'rb') as recommender_file:
            recommender = pickle.load(recommender_file)
        print(">>>>>>>>>>recommend loaded success!")
        # Find the index of the user's chosen anime
        user_anime = anime[anime['Title'] == anime_title]
        user_anime_index = np.where(rating_matrix.index == int(user_anime['Anime_id']))[0][0]

        # Get recommendations based on the chosen anime
        user_anime_ratings = rating_matrix.iloc[user_anime_index]
        user_anime_ratings_reshaped = user_anime_ratings.values.reshape(1, -1)
        _, indices = recommender.kneighbors(user_anime_ratings_reshaped, n_neighbors=16)
        nearest_neighbors_indices = rating_matrix.iloc[indices[0]].index[1:]
        nearest_neighbors = pd.DataFrame({'Anime_id': nearest_neighbors_indices})
        result = pd.merge(nearest_neighbors, anime, on='Anime_id', how='left')

        return result
    except Exception as e:
        print(str(e))
        return str(e)

if __name__ == "__main__":
    print("Training the recommendation system...")
    # Train the recommendation system (call this only once or when data changes)
    train_recommendation_system()
    print("Done training the recommendation system.")

    # Get recommendations for a specific anime
    # anime_title = 'Sen to Chihiro no Kamikakushi'  # Replace with the anime title you want to use
    anime_title = 'Cowboy Bebop Tengoku no Tobira'
    recommendations = get_recommendation(anime_title)
    print(recommendations)
    # Print the recommendations
    '''
    if not recommendations.empty:
        print("Recommended Anime:")
        print(recommendations[['Title', 'Genre', 'Type']])
    else:
        print("Anime not found or an error occurred.")
    '''
