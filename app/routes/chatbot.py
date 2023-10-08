from flask import Flask, request, jsonify
from pprint import pprint
from paddlenlp import Taskflow
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ..AnimesRecommendation import content_based_recommendation
from ..AnimesRecommendation import collaborative_filtering_recommendation
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

def lookforanime(num):
    
    anime = pd.read_csv("app/data/cleaned_anime_data.csv", index_col=0)
    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(anime['soup'])
    cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
    recommendations = content_based_recommendation.get_recommendations(num, cosine_sim2, num_recommend=10)
    return recommendations

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
        # 在这里处理用户消息，例如调用聊天机器人 API 获取回复
        bot_reply = f"Based on the anime you mentioned: {return_message}, chatbot recommend you to watch:"

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
