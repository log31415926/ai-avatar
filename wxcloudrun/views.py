from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
from flask import Blueprint, request, jsonify
import base64
import requests
import random
#import dashscope
from .dashscope_http import generate_image

@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')


@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数111111')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)



#api = Blueprint("api", __name__)

"""
@api.route("/api/generate", methods=["POST"])
def generate():
    data = request.json or {}

    image_url = data.get("image_url")
    prompt = data.get("prompt", "给图片戴上一顶圣诞帽")

    if not image_url:
        return jsonify({"error": "image_url is required"}), 400

    result = generate_image(image_url, prompt)

    images = result["output"]["choices"][0]["message"]["content"]
    image_urls = [i["image"] for i in images]

    return jsonify({
        "images": image_urls
    })
"""

"""
@app.route('/api/generate', methods=['POST'])
def generate_hat():
    data = request.json or {}

    image_url = data.get("image_url")
    prompt = data.get("prompt", "在图片主体上添加一顶圣诞帽，自然贴合主体头部，时尚美观，色彩明亮，充满节日气氛，高质量，光影自然")

    if not image_url:
        return jsonify({"error": "image_url is required"}), 400

    result = generate_image(image_url, prompt)

    images = result["output"]["choices"][0]["message"]["content"]
    image_urls = [i["image"] for i in images]

    return jsonify({
        "images": image_urls
    })
"""

SANTA_HAT_PROMPTS = [
    "在图片主体头部添加一顶毛线圣诞帽。帽子为柔软毛线材质，整体轮廓自然贴合头部。帽顶带一对小巧的迷你鹿角，比例克制，不夸张。颜色柔和，装饰细节集中在帽子本身",
    "在图片主体头部添加一顶传统红色圣诞帽。帽体为自然下垂的锥形，顶端有白色毛球。帽檐为白色毛绒材质，贴合头部轮廓，边缘整齐,整体设计简洁真实。",
    "在图片主体头部添加一顶红色与绿色拼块设计的圣诞帽。帽体由清晰分区的拼色构成，色块边界整齐。造型自然贴合头部，装饰元素集中在帽子表面。不改变人物外观、背景或整体画面风格。",
    "在图片主体头部添加一顶卡通动物造型的圣诞帽。帽子带小型动物耳朵，如兔耳或猫耳，比例小巧柔软。耳朵自然附着在帽体上，不影响头部结构。整体设计可爱但简洁",
    "在图片主体头部添加一顶创意圣诞帽。帽子表面带有细小节日图案花纹，如雪花、圣诞树或星星。图案分布均匀，尺寸克制，不覆盖帽子整体结构。颜色搭配协调。",
    "在图片主体头部添加一顶精致的红色圣诞帽，自然下垂的锥形帽体，白色毛绒帽檐与白色毛球。帽子上面有细腻的小型节日刺绣图案，如麋鹿、圣诞老人和雪花，图案均匀分布，精致但不夸张。白色毛绒帽檐外侧点缀一圈低调的珠宝装饰，造型类似公主王冠，由小宝石和珍珠组成，贴合帽檐轮廓，不突出、不硬质。整体柔软温馨，童话感与高级感并存。"
]
@app.route('/api/generate', methods=['POST'])
def generate_hat():
    data = request.json or {}

    image_url = data.get("image_url")
    user_prompt = data.get("prompt")  # 可选：是否允许前端传

    if not image_url:
        return jsonify({"error": "image_url is required"}), 400

    # 🎲 随机选一条 prompt
    final_prompt = random.choice(SANTA_HAT_PROMPTS)

    result = generate_image(image_url, final_prompt)

    images = result["output"]["choices"][0]["message"]["content"]
    image_urls = [i["image"] for i in images]

    return jsonify({
        "images": image_urls,
        "prompt_used": final_prompt  # 👈 调试用，可后期删
    })

@app.route('/api/generate_all', methods=['POST'])
def generate_all():
    data = request.json or {}

    image_url = data.get("image_url")
    prompt = data.get("prompt", "给图片戴上一顶圣诞帽")

    if not image_url:
        return jsonify({"error": "image_url is required"}), 400

    result = generate_image(image_url, prompt)

    images = result["output"]["choices"][0]["message"]["content"]
    image_urls = [i["image"] for i in images]

    return jsonify({
        "images": image_urls
    })

@app.route("/ping")
def ping():
    return "pong"