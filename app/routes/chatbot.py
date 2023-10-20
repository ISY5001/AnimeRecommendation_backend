
from flask import Flask, request, jsonify
from pprint import pprint
from paddlenlp import Taskflow
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from AnimesRecommendation import collaborative_filtering_recommendation
from AnimesRecommendation import content_based_recommendation
#from ..AnimesRecommendation import content_based_recommendation
#from ..AnimesRecommendation import collaborative_filtering_recommendation
app = Flask(__name__)


def ner(sentence):
    schema = ['Movie']
    sentence = sentence+'.'
    ie_en = Taskflow('information_extraction', schema=schema, model='uie-base-en')
    results = ie_en(sentence)
    print(results)
    texts = []
    # 遍历列表中的每个字典项
    for item in results:
        # 遍历字典的键值对
        for key, values in item.items():
            # 遍历与键关联的列表中的每个字典项
            for value in values:
                # 提取 'text' 键的值并添加到 texts 列表中
                texts.append(value['text'])
                      
    return texts

def lookforanime(animeName):

    #list转化为string
    animeName = ' '.join(animeName)
    recommendations = collaborative_filtering_recommendation.get_recommendation(animeName)
    recommendationList = recommendations['Title'].tolist();
    #recommendationAnimes = []
    #for recommendation in recommendations:
        #recommendationAnimes.append(recommendation[1])

    return recommendationList[0:5]

def reply():
    print(request.data)
    # 获取 JSON 数据
    if request.method == 'POST':
        data = request.get_json()

        # 提取用户消息
        user_message = data.get('userMessage')
        #print(user_message)
        # 调用 ner 函数获取命名实体识别结果
        return_message = ner(user_message)
        recommended_animes = lookforanime(return_message)
        # 在这里处理用户消息，例如调用聊天机器人 API 获取回复
        bot_reply = f"Based on the anime you mentioned: {return_message}, I recommend you to watch: {recommended_animes}"
        
        # bot_reply += ', '.join(recommended_animes)
        # 返回机器人的回复
        return jsonify({'botReply': bot_reply})
    elif request.method == 'OPTIONS':
        # Handle CORS preflight request
        response = jsonify({"msg": "CORS preflight successful"})
        response.status_code = 200
        response.headers["Access-Control-Allow-Methods"] = "POST"  # Allow POST requests
        return response
    else:
        return jsonify({"msg": "Invalid request method!"}), 400
    

if __name__ == '__main__':
    app.run(debug=True)
