from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
from flask import Blueprint, request, jsonify
import base64
import requests
import dashscope

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
        return make_err_response('缺少action参数')

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



bp = Blueprint('index', __name__)
dashscope.api_key = "sk-28e1ec1fb4d74e69a573e9f6dd8cd2f8"

@bp.route('/api/generate', methods=['POST'])
def generate_avatar():
    try:
        # 接收Base64头像
        data = request.get_json()
        img_base64 = data.get("imageBase64")

        if not img_base64:
            return jsonify({"error": "no image provided"}), 400

        # 调用阿里云图片编辑接口
        from dashscope import MultiModalConversation

        messages = [
            {
                "role": "user",
                "content": [
                    {"image": img_base64},
                    {"text": "请保留头像主体，并生成一顶红色圣诞帽戴在头上"}
                ]
            }
        ]

        response = MultiModalConversation.call(
            model="qwen-image-edit-plus",
            messages=messages,
            stream=False,
            n=1,
            prompt_extend=True
        )

        if response.status_code != 200:
            return jsonify({
                "error": "AI error",
                "detail": response.message
            }), 500

        image_url = response.output.choices[0].message.content[0]['image']

        return jsonify({
            "code": 0,
            "imageUrl": image_url
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
