import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import pymysql
import seaborn as sns

# 从 MySQL 获取 DataFrame
def get_df_from_sql():
    # 请根据实际情况修改下面的连接参数
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='085258',
                                 database='user_data')
    
    sql_query = "SELECT * FROM cleaned_anime_data"
    df = pd.read_sql(sql_query, connection)
    connection.close()
    return df

# 找到给定电影的相似电影
def find_similar_movies(movie_title, df):
    movie_cluster = df.loc[df['Title'] == movie_title, 'cluster'].iloc[0]  # 获取给定电影的聚类
    similar_movies = df[(df['cluster'] == movie_cluster) & (df['Title'] != movie_title)]  # 获取属于同一聚类的所有电影，排除给定电影
    top_5_movies = similar_movies.head(5)  # 获取前五个相似的电影
    return top_5_movies['Title'].tolist()  

# 找出包含指定关键词的所有电影
def find_movies_by_keyword(keyword, df):

    movies_with_keyword = df[df['soup'].str.contains(keyword, case=False, na=False)]
    if not movies_with_keyword.empty:
        movie_cluster = movies_with_keyword.iloc[0]['cluster']
        # 获取同一聚类中的所有电影
        similar_movies = df[df['cluster'] == movie_cluster]
        # 获取前五部相似电影的标题（确保它们包含指定的关键词）
        top_5_movies = similar_movies[similar_movies['soup'].str.contains(keyword, case=False, na=False)].head(5)
        return top_5_movies['Title'].tolist() 

    return []  


# 提取 "soup" 列，并使用 KMeans 聚类
def kmeans_clustering(df):
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(df['soup'].values.astype('U'))
    # 随便搞了个5类
    kmeans = KMeans(n_clusters=5, random_state=0).fit(X)
    df['cluster'] = kmeans.labels_

     # 打印每个聚类的顶部关键词
    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()
    for i in range(5):  
        print(f"Cluster {i}:")
        for ind in order_centroids[i, :5]:  
            print(f" {terms[ind]}", end='')
        print()

    # 使用 PCA 降维以便可视化
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(X.toarray())
    principal_df = pd.DataFrame(data=principal_components, columns=['pc1', 'pc2'])
    final_df = pd.concat([principal_df, df[['cluster']]], axis=1)

    # # 绘制散点图
    # plt.figure(figsize=(10, 7))
    # sns.scatterplot(x='pc1', y='pc2', hue='cluster', data=final_df, palette='viridis')
    # plt.title('KMeans Clustering with 2D PCA')
    # plt.show()


if __name__ == "__main__":
    df = get_df_from_sql()
    kmeans_clustering(df)

    # # 举个栗子, 用电影名称查找相似电影
    # movie_title = 'Mezzo DSA'  
    # similar_movies = find_similar_movies(movie_title, df)
    # print(similar_movies)  

    # 举个栗子，使用关键词查找相似电影
    keyword = 'comedy'
    similar_movies = find_movies_by_keyword(keyword, df)
    print(similar_movies)       