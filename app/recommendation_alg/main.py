import os
import numpy as np
import pandas as pd
import pymysql
import json

from flask_ngrok import run_with_ngrok
from flask import Flask, make_response, request, jsonify

from data_preprocessing import ML_data_preprocessing
from CB_recommendation import Content_based_recommendation
from CF_recommendation import Collaborative_Filtering_recommendation
# from MF_recommendation import Matrix_Factorization
from measure import measure_method

# 
app = Flask(__name__)
run_with_ngrok(app)
path = "/home/hewen/ISS-workshop/MVP/AnimeRecommendation/python_backend"

# 预处理用户数据与电影数据
def update_preproccessed_data():
  db_conn = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='12345678',
    database='movie_recommend',
    charset='utf8'
  )

  ratings_sql = "select user_id userId, movie_id movieId, rating, timestamp from ratings"
  movies_sql = "select id movieId, name title, genre genres from movies"

  movies_df = pd.read_sql(movies_sql,con=db_conn)
  ratings_df = pd.read_sql(ratings_sql,con=db_conn)

  # data preprocessing: 
  ML_data_preprocessing.data_preprocess(path, movies_df, ratings_df)

  # renew current data
  pred_CB = pd.read_csv(path + '/data/output/pred_ratings_CB.csv', index_col=0)
  pred_CF = pd.read_csv(path + '/data/output/pred_ratings_CF.csv', index_col=0)

  # predict top_K 
def predict_top_K(model_type, user_id, K=10):
  '''
  pred_rating_csv：预测算法的预测打分表
  '''
  # read predicted data:
  # pred = pd.read_csv(pred_rating_csv, index_col=0)
  pred = None
  if model_type == "CB":
    pred = pred_CB
  else:
    pred = pred_CF


  user_feature = user_rating.loc[user_id, :]
  user_unrated_vector = user_feature.loc[user_feature == 0]
  unrated_index = user_unrated_vector.index

  # 对未评分电影的预测评分进行排序
  user_unrated_pred_sorted = pred.loc[user_id, unrated_index].sort_values(ascending=False)

  # topk list
  top_K_list = user_unrated_pred_sorted[:K].index.tolist()
  return top_K_list

# 集成CB与CF的混合算法进行topK预测
def predict_ER_top_K(user_id, K=10):

  user_feature = user_rating.loc[user_id, :]
  user_unrated_vector = user_feature.loc[user_feature == 0]
  unrated_index = user_unrated_vector.index
  
  user_unrated_pred_CB = pred_CB.loc[user_id, unrated_index]
  user_unrated_pred_CF = pred_CF.loc[user_id, unrated_index]

  print(user_unrated_pred_CB)
  print(user_unrated_pred_CF)

# predict_ER_top_K(10)

def get_recommend_performance_dict():
  nonzero_index = user_rating.values.nonzero()

  actual = user_rating.values[nonzero_index[0], nonzero_index[1]]
  pred_CB_perf = pred_CB.values[nonzero_index[0], nonzero_index[1]]
  pred_CF_perf = pred_CF.values[nonzero_index[0], nonzero_index[1]]

  res = []

  cb_dict = {}
  cb_dict['Name'] = 'CB'
  cb_dict['MSE'] = measure_method.comp_mse(pred_CB_perf, actual)[0]
  cb_dict['RMSE'] = measure_method.comp_rmse(pred_CB_perf, actual)[0]
  res.append(cb_dict)

  cf_dict = {}
  cf_dict['Name'] = 'CF'
  cf_dict['MSE'] = measure_method.comp_mse(pred_CF_perf, actual)[0]
  cf_dict['RMSE'] = measure_method.comp_rmse(pred_CF_perf, actual)[0]
  res.append(cf_dict)
  return res

# flask
@app.route("/preprocessing",methods=["GET"])
def preprocessing():
  response = make_response("success", 200)
  return response

@app.route("/cb-recommend",methods=["POST"])
def cb_recommend():
  # Content-based recommendation
  user_id = int(request.json.get("userId"))
  K = int(request.json.get("k"))
  # user's movie rating sheet
  user_feature = user_rating.loc[user_id, :]
  recommend_list = Content_based_recommendation.CB_recommend_top_K(user_feature, movies_feature, K).tolist()
  return jsonify(recommend_list)

@app.route("/cf-recommend",methods=["POST"])
def cf_recommend():
  # Content-based recommendation
  user_id = int(request.json.get("userId"))
  K = int(request.json.get("k"))
  # user's movie rating sheet
  recommend_list = predict_top_K("CF", user_id, K)
  return jsonify(recommend_list)

@app.route("/get-recommend-performance",methods=["GET"])
def get_recommend_performance():
  p_dict = get_recommend_performance_dict()
  return jsonify(p_dict)


if __name__ == '__main__':
    # load preprocessed data
    movies_feature = pd.read_csv(
        path + '/data/movies_feature.csv',
        index_col=0
    )
    user_rating = pd.read_csv(
        path + '/data/user-rating.csv',
        index_col=0
    )
    train, test = ML_data_preprocessing.train_test_split(user_rating)
    train = user_rating

    # content-based
    count = 0
    total = float(train.shape[0])
    print("start to work...")
    for idx, user in train.iterrows():
        unrated_index = user[user == 0].index.values
        rates_lst = []

        for item in unrated_index:
            rate_h = Content_based_recommendation.CB_recommend_estimate(user, movies_feature, int(item))
            rates_lst.append(rate_h)

        train.loc[idx, unrated_index] = rates_lst

        count += 1
        if count % 100 == 0:
            presentage = round((count / total) * 100)
            print('Completed %d' % presentage + '%')
    print("finished")
    train.to_csv(path + '/data/output/pred_ratings_CB.csv')

    # user-user
    count = 0
    total = float(train.shape[0])
    for idx, user in train.iterrows():
        unrated_index = user[user == 0].index.values
        unrated_index_ = map(int, unrated_index)
        rates_lst = Collaborative_Filtering_recommendation.CF_recommend_estimate(train, idx, unrated_index_, 50)

        train.loc[idx, unrated_index] = rates_lst

        count += 1
        print("Round " + str(count) + "/" + str(total) + " completed")
        if count % 100 == 0:
            presentage = round((count / total) * 100)
            print('Completed %d' % presentage + '%')
    train.to_csv(path + '/data/output/pred_ratings_CF.csv')

    # mse and rmse
    pred_CB = pd.read_csv(path + '/data/output/pred_ratings_CB.csv', index_col=0)
    pred_CF = pd.read_csv(path + '/data/output/pred_ratings_CF.csv', index_col=0)

    nonzero_index = user_rating.values.nonzero()

    actual = user_rating.values[nonzero_index[0], nonzero_index[1]]
    pred_CB_perf = pred_CB.values[nonzero_index[0], nonzero_index[1]]
    pred_CF_perf = pred_CF.values[nonzero_index[0], nonzero_index[1]]

    res = []

    cb_dict = {}
    cb_dict['Name'] = 'CB'
    cb_dict['MSE'] = measure_method.comp_mse(pred_CB_perf, actual)[0]
    cb_dict['RMSE'] = measure_method.comp_rmse(pred_CB_perf, actual)[0]
    res.append(cb_dict)

    cf_dict = {}
    cf_dict['Name'] = 'CF'
    cf_dict['MSE'] = measure_method.comp_mse(pred_CF_perf, actual)[0]
    cf_dict['RMSE'] = measure_method.comp_rmse(pred_CF_perf, actual)[0]
    res.append(cf_dict)
    print(res)


    print ('MSE of CB is %s' % measure_method.comp_mse(pred_CB, actual))
    print ('RMSE of CB is %s' % measure_method.comp_rmse(pred_CB, actual))
    print ('MSE of CF is %s' % measure_method.comp_mse(pred_CF, actual))
    print ('RMSE of CF is %s' % measure_method.comp_rmse(pred_CF, actual))

    app.run()