from flask import Flask, render_template, request,Response
from openai import OpenAI
import datetime
import os
app = Flask(__name__)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.deepseek.com"
)

def generate_article(topic, style, length):
    prompt = f"""
请写一篇关于【{topic}】的文章，
风格：{style}，
长度：{length}，
要求结构清晰，有小标题
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


@app.route("/", methods=["GET", "POST"])
def index():
    article = ""

    if request.method == "POST":
        topic = request.form["topic"]
        style = request.form["style"]
        length = request.form["length"]

        article = generate_article(topic, style, length)

    return render_template("index.html", article=article)

@app.route("/download", methods=["POST"])
def download():
    content = request.form["article"]

    filename = datetime.datetime.now().strftime("article_%Y%m%d_%H%M%S.txt")

    return Response(
        content,
        mimetype="text/plain",
        headers={
            "Content-Disposition": f"attachment;filename={filename}"
        }
    )

if __name__ == "__main__":
    app.run(debug=True)