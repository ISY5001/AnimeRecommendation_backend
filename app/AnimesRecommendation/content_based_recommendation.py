ontetnimport pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_recommendations(idx, cosine_sim, num_recommend=10):
    sim_scores = list(enumerate(cosine_sim[idx]))c
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # Get the scores of the 15 most similar movies
    sim_scores = sim_scores[1:num_recommend]
    movie_indices = [i[0] for i in sim_scores]
    return anime['Title'].iloc[movie_indices]

if __name__ == "__main__":
    anime = pd.read_csv("data/cleaned_anime_data.csv", index_col=0)
    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(anime['soup'])
    cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
    print(get_recommendations(15, cosine_sim2))