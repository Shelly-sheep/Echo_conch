import json

import requests
import gradio as gr
import pandas as pd

base_url = "http://127.0.0.1:6605"


def create_kb(kb_name, kb_info):
    # 定义API的URL
    url = base_url + "/knowledgebase/create_kb"

    # 定义请求数据
    data = {
        "kb_name": kb_name,
        "kb_info": kb_info
    }

    # 发送POST请求
    try:
        response = requests.post(url, json=data)
        # 检查响应状态码
        if response.status_code == 200:
            return gr.update(value="知识库创建成功！", visible=True), gr.update(value=""), gr.update(value="")
        else:
            return gr.update(value=f"知识库创建失败：{response.json().get('detail', '')}", visible=True), gr.update(value=""), gr.update(
                value="")
    except Exception as e:
        return gr.update(value=f"请求失败：{e}", visible=True), gr.update(value=""), gr.update(value="")


def delete_kb(kb_name):
    # 定义API的URL
    url = base_url + "/knowledgebase/delete_kb"

    # 发送POST请求
    try:
        response = requests.delete(url, params={"kb_name": kb_name})
        # 检查响应状态码
        if response.status_code == 200:
            return gr.update(value="知识库删除成功！", visible=True), gr.update(value="")
        else:
            return gr.update(value=f"删除失败：{response.json().get('detail', '')}", visible=True), gr.update(value="")
    except Exception as e:
        return gr.update(value=f"请求失败：{e}", visible=True), gr.update(value="")


def upload_docs(kb_name_upload, file_upload, chunk_size, chunk_overlap):
    # 定义 API 的 URL
    upload_docs_url = base_url + "/knowledgebase/upload_docs"  # 请确保端口和路径正确
    # 构建文件和表单数据
    files = [('files', (open(file_path, 'rb'))) for file_path in file_upload]
    data = {
        'kb_name': kb_name_upload,
        'chunk_size': chunk_size,
        'chunk_overlap': chunk_overlap
    }
    # 发送POST请求
    try:
        # 发送 POST 请求
        response = requests.post(upload_docs_url, files=files, data=data)

        # 检查响应状态码并输出结果
        if response.status_code == 200:
            return gr.update(value="文件上传成功", visible=True), gr.update(value=[], visible=False)
        else:
            return gr.update(value=f"文件上传失败，状态码: {response.status_code}, 错误信息: {response.json().get('detail', '')}",
                             visible=True), gr.update(value=[], visible=False)
    except Exception as e:
        return gr.update(value=f"请求失败：{e}", visible=True), gr.update(value=[], visible=False)


def list_kbs():
    # 定义API的URL
    list_kbs_url = base_url + "/knowledgebase/list_kbs"  # 请确保端口和路径正确

    # 发送GET请求
    response = requests.get(list_kbs_url)

    # 检查响应状态码并打印结果
    if response.status_code == 200:
        kb_list = response.json()  # 解析JSON格式的知识库列表
        return gr.update(choices=[kb.split(".")[0] for kb in kb_list["knowledgebases"]])
    else:
        return gr.update(choices=[])


# 全局文件列表
selected_files = []


def update(file):
    if file:
        # 将新选中的文件添加到列表中
        for f in file:
            if f not in selected_files:
                selected_files.append(f)
    return gr.update(value=selected_files, visible=True), gr.update(value=[])

