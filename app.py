from flask import Flask, render_template, request


app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
def home():

    article = request.form.get('article')

    return render_template("index.html", article=article)


if __name__ == "__main__":
    app.run(debug=True)
