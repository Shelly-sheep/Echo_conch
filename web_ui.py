import uuid
import gradio as gr
from webui.chat_with_agent_api import chat_with_agent
from webui.knowledgebase_api import create_kb, delete_kb, upload_docs, list_kbs, update


# 定义一个生成唯一会话 ID 的函数
def generate_session_id():
    return str(uuid.uuid4())


# 在 Gradio 应用加载时生成新的会话ID
def on_app_load():
    session_id = generate_session_id()
    return session_id


with gr.Blocks(fill_width=True, fill_height=True) as demo:
    # 使用 on_load 事件来生成会话ID
    session_state = gr.State(value=on_app_load)

    with gr.Tab("🐚 回音海螺"):
        gr.Markdown("## 🐚 回音海螺")

        with gr.Row():
            with gr.Column(scale=1, variant="panel") as sidebar_left:
                sys_prompt = gr.Textbox(label="系统提示语", value="You are a helpful assistant. Answer questions in chinese !")
                history_len = gr.Slider(minimum=-1, maximum=10, value=-1, label="保留历史消息的数量")
                temperature = gr.Slider(minimum=0.01, maximum=2.0, value=0.5, step=0.01, label="temperature")
                max_tokens = gr.Slider(minimum=64, maximum=1024, value=512, step=8, label="max_length")
                stream = gr.Checkbox(label="stream", value=True)

            # 取消绑定方式，改为动态输入
            with gr.Column(scale=10) as main:
                chatbot = gr.Chatbot(height=600, type="messages")

                msg_input = gr.MultimodalTextbox(
                    label="输入消息",
                    placeholder="输入问题或上传文件...",
                    file_types=["image", "file"],
                    show_label=False
                )

                # 手动绑定提交事件
                msg_input.submit(
                    fn=chat_with_agent,
                    inputs=[msg_input, chatbot, sys_prompt, history_len, temperature, max_tokens, stream, session_state],
                    outputs=chatbot
                ).then(lambda: gr.MultimodalTextbox(value=None), None, msg_input)


    # 知识库操作页
    with gr.Tab("知识库管理"):
        gr.Markdown("## 📚 知识库管理")

        with gr.Row():
            kb_name = gr.Textbox(label="知识库名称", placeholder="请输入知识库名称")
        with gr.Row():
            kb_info = gr.Textbox(label="知识库描述", placeholder="请输入知识库描述")
        with gr.Row():
            # 隐藏的消息框，用于显示操作结果
            message_box = gr.Markdown(visible=False)
        with gr.Row():
            create_button = gr.Button("创建知识库")
            delete_button = gr.Button("删除知识库")

        kbs = list_kbs()['choices']
        with gr.Row():
            kb_name_upload = gr.Dropdown(label="选择知识库", choices=kbs)
        with gr.Row():
            file_uploaded = gr.Files(label="已选择的文件", visible=False)
        with gr.Row():
            file_upload = gr.Files(label="选择文件")
        with gr.Row():
            chunk_size = gr.Number(label="知识库中单段文本最大长度(chunk_size)", value=128, minimum=1, maximum=800)
            chunk_overlap = gr.Number(label="知识库中相邻文本重合长度(chunk_overlap)", value=20, minimum=0, maximum=400)
        with gr.Row():
            upload_button = gr.Button("上传并向量化")
        with gr.Row():
            # 隐藏的消息框，用于显示操作结果
            upload_message_box = gr.Markdown(visible=False)

        create_button.click(create_kb, [kb_name, kb_info], [message_box, kb_name, kb_info]).then(fn=list_kbs,
                                                                                                 outputs=kb_name_upload)

        delete_button.click(delete_kb, [kb_name_upload], [message_box, kb_name]).then(fn=list_kbs, outputs=kb_name_upload)

        file_upload.upload(fn=update, inputs=[file_upload], outputs=[file_uploaded, file_upload])

        upload_button.click(upload_docs, [kb_name_upload, file_uploaded, chunk_size, chunk_overlap],
                            [upload_message_box, file_uploaded])

# 启动应用
demo.launch()
