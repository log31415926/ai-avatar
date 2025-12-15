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
    "在图片主体上添加毛线圣诞帽，带可爱的迷你鹿角，色彩柔和温暖，装饰细节丰富，毛绒质感明显，自然贴合头部，节日氛围浓厚",
    "为图片主体添加传统红色圣诞帽，顶端有白色毛球，边缘白色毛绒装饰，光影真实自然，高质量，温馨节日风格",
    "图片主体戴小矮人风格圣诞帽，尖尖帽顶，色彩鲜艳活泼，带趣味装饰如铃铛或彩带，卡通可爱，欢乐节日气氛",
    "在图片主体上添加红色与绿色拼块圣诞帽，设计创意独特，色彩鲜明，装饰丰富，光影逼真，高质量节日风",
    "为图片主体添加卡通动物风格圣诞帽，如兔耳或猫耳帽，色彩柔和可爱，带小饰品装饰，欢乐俏皮，节日氛围浓厚",
    "在图片主体上添加创意圣诞帽，带节日图案花纹，如雪花、圣诞树或星星，色彩协调明亮，装饰丰富，精致节日风",
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