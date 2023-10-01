import pandas as pd
import numpy as np
import re
import string
from ast import literal_eval
from scipy.sparse import csr_matrix

import logging

# Constants
MIN_VOTES_THRESHOLD = 0.85
MEAN_RATING = 0  # Initialize with a default value

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def text_cleaning(text):
    text = re.sub(r'&quot;', '', text)
    text  = "".join([char for char in text if char not in string.punctuation])
    text = re.sub(r'.hack//', '', text)
    text = re.sub(r'&#039;', '', text)
    text = re.sub(r'A&#039;s', '', text)
    text = re.sub(r'I&#039;', 'I\'', text)
    text = re.sub(r'&amp;', 'and', text)
    text = re.sub(r'Â°', '',text)
    return text

def weighted_rating(x, m, C):
    v = x['ScoredBy']
    R = x['Rating']
    return (v/(v+m)*R)+(m/(m+v)*C)

def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ","")) for i in x]
    else:
        if isinstance(x, str):
            return str.lower(x.replace(" ",""))
        else:
            return ""

def create_soup(data):
    genre = " ".join(data['Genre'])
    media_type = data['Type']
    producers = " ".join(data['Producer'])
    studios = " ".join(data['Studio'])
    synopsis = data['Synopsis']
    result = f"{genre} {media_type} {producers} {studios} {synopsis} {studios}"
    return result

def main():
    # Parameterize file paths
    input_csv = "data/Anime_data.csv"
    output_csv = "data/cleaned_anime_data.csv"

    # Read data from CSV
    try:
        anime = pd.read_csv(input_csv, encoding='latin')
    except FileNotFoundError:
        logger.error(f"File not found: {input_csv}")
        return
    
    logger.info("Cleaning anime data...")
    anime['Title'] = anime['Title'].apply(text_cleaning)
    
    # Compute m and C for weighted rating
    C = anime['Rating'].mean()
    m = anime['ScoredBy'].quantile(MIN_VOTES_THRESHOLD)
    
    # Filter and compute weighted scores
    q_animes = anime.copy().loc[anime['ScoredBy'] >= m]
    q_animes['Score'] = q_animes.apply(lambda x: weighted_rating(x, m, C), axis=1)
    q_animes = q_animes.sort_values('Score', ascending=False)
    best_score = q_animes.sort_values(by=['Score'], ascending=False)[:10]
    best_scores = best_score[['Score','Title','Genre', 'Studio', 'Type']].set_index('Title')

    # Data preprocessing for content-based filtering
    logger.info("Preprocessing data for content-based filtering...")
    anime['Synopsis'] = anime['Synopsis'].fillna('')
    features = ['Genre','Producer', 'Studio']
    anime[features] = anime[features].fillna('[' ']')
    for feature in features:
        anime[feature] = anime[feature].apply(literal_eval)
    features = ['Genre','Producer', 'Studio', 'Type']
    for feature in features:
        anime[feature] = anime[feature].apply(clean_data)
    anime['soup'] = anime.apply(create_soup, axis=1)
    anime = anime.reset_index()
    anime.fillna({'Rating':0}, inplace=True)

    # Export cleaned data
    anime.to_csv(output_csv, index=False, encoding='utf-8')
    logger.info(f"Cleaned data saved to {output_csv}")

if __name__ == "__main__":
    main()
