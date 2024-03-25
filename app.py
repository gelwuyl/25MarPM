from flask import Flask, request, render_template
import google.generativeai as palm
import replicate
import os

palm.configure(api_key="AIzaSyBgrPrnCD5XvXkFVavjqlVXQU9wnyY1AAA")
model = {
    "model": "models/chat-bison-001",
}

os.environ["REPLICATE_API_TOKEN"] = "r8_GK2JD0n2YkmAffAeWciRy2ZHTh9f8ww1X5bTE"

change_name_flag = 1
name = ""

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    return(render_template("index.html"))

@app.route("/main", methods=["GET","POST"])
def main():
    global name, change_name_flag
    if change_name_flag == 1:
        name = request.form.get("name")
        change_name_flag = 0
    return(render_template("main.html",r=name))

@app.route("/palm", methods=["GET","POST"])
def palm_flask():
    return(render_template("palm.html"))

@app.route("/midjourney", methods=["GET","POST"])
def midjourney():
    return(render_template("midjourney.html"))

@app.route("/palm_query", methods=["GET","POST"])
def palm_query():
    q = request.form.get("q")
    print(q)
    r = palm.chat(
        **model,
        messages=q
    )
    print(r.last)
    return(render_template("palm_reply.html",r=r.last))

@app.route("/midjourney_query", methods=["GET","POST"])
def midjourney_query():
    q = request.form.get("q")
    r = replicate.run(
        "stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf", 
        input={"prompt": q}
    )
    return(render_template("midjourney_reply.html",r=r[0]))

@app.route("/end", methods=["GET","POST"])
def end():
    return(render_template("end.html",r=name))

if __name__ == "__main__":
    app.run()
