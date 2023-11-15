from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import json
import os
from django.conf import settings
import joblib
import random


# Create your views here.
def get_home_page(request):
    response = render(request, "predict/champions.html")
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    response['Cache-Control'] = f'no-cache, no-store, must-revalidate, max-age={random.randint(1, 3600)}'
    return response

def predict_view(request):
    if request.method == "POST":
        # 获取前端发送的JSON数据
        data = json.loads(request.body)["imput"]
        print(data)
        # 从 static/json 文件夹中加载 JSON 数据
        json_file_path = os.path.join(settings.STATICFILES_DIRS[0], 'json', 'champion_index_2023.json')

        # 然后使用json库或其他适当的工具加载JSON文件
        with open(json_file_path, 'r') as json_file:
            cham_index = json.load(json_file)
        
        data_input = [cham_index["top"][data[0]],cham_index["jug"][data[1]],cham_index["mid"][data[2]],cham_index["ad"][data[3]],cham_index["sup"][data[4]],
                        cham_index["top"][data[5]],cham_index["jug"][data[6]],cham_index["mid"][data[7]],cham_index["ad"][data[8]],cham_index["sup"][data[9]]]
        
        print(data_input)
        
        # load RF model
        model_path = os.path.join(settings.STATICFILES_DIRS[0], 'model', 'RF_cham_1102.pkl')
        RF_model = joblib.load(model_path)
        y_pred = RF_model.predict([data_input])[0]
        y_prob = RF_model.predict_proba([data_input])[:, 1][0]
        if y_pred == 1:
            win = "蓝色方 胜利！ 胜率："
            p = str(round(y_prob*100,1))+"%"
        else:
            win = "红色方 胜利！ 胜率："
            p = str(round((1-y_prob)*100,1))+"%"
        result = win+p

        return JsonResponse({"result":result})
    # else:
    #     # 如果不是POST请求，返回一个渲染的模板
    #     return render(request, "predict/champions.html")
