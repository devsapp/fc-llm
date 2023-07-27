# coding=utf-8
import os


def handler(event, context):
    model_path = os.getenv("LLM_MODEL", "chatglm2-6b")
    app_path = os.getenv("APP_NAME", "chatglm2-6b")
    if not os.path.exists("/mnt/auto/llm/models" + model_path):
        os.makedirs("/mnt/auto/llm" + model_path)
    if not os.path.exists("/mnt/auto/llm" + app_path):
        os.makedirs("/mnt/auto/llm" + app_path)
    if not os.path.exists("/mnt/auto/.kodbox-1.35.031"):
        os.system(
            "wget http://images.devsapp.cn/application/kodbox/kodbox-1.35.031.zip -O /mnt/auto/kodbox-1.35.031.zip")
        os.system(
            "cd /mnt/auto && unzip kodbox-1.35.031.zip && mv kodbox-1.35.031 .kodbox-1.35.031 && rm kodbox-1.35.031.zip && cd -")
    return "nas init"
