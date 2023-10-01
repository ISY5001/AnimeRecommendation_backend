import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_recommendations(idx, cosine_sim, num_recommend=10):
    # Create an enumerated list of movie similarity scores
    sim_scores = list(enumerate(cosine_sim[idx]))
    # Sort by similarity scores (in descending order)
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # Get the top N most similar movies (excluding the input movie itself)
    sim_scores = sim_scores[1:num_recommend + 1]
    # Get the indices of the most similar movies
    movie_indices = [i[0] for i in sim_scores]
    # Return the titles of the recommended movies
    return anime['Title'].iloc[movie_indices]

if __name__ == "__main__":
    # Load the cleaned anime data
    anime = pd.read_csv("data/cleaned_anime_data.csv", index_col=0)
    # Initialize the CountVectorizer
    count = CountVectorizer(stop_words='english')
    # Fit and transform the text data
    count_matrix = count.fit_transform(anime['soup'])
    # Compute cosine similarity between anime
    cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
    # Get recommendations for a specific anime (e.g., index 15)
    recommendations = get_recommendations(15, cosine_sim2, num_recommend=10)
    # Print the recommendations
    print("Recommended Anime:")
    for i, title in enumerate(recommendations, start=1):
        print(f"{i}. {title}")
