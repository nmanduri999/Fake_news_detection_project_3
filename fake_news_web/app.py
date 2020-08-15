from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
# import pickle
import nltk
from nltk.stem import WordNetLemmatizer
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from joblib import dump, load

model = load_model("neural_network.h5")
# model = dump("neural_network.h5")
tfIdfVectorizer=load('tfidfV.joblib')

def findClass(new_data):
    wl = WordNetLemmatizer()
    stopwords= nltk.corpus.stopwords.words('english')
    words = re.split('\W+', new_data)
    text = []
    for word in words:
        if word not in stopwords:
            text.append(wl.lemmatize(word))
    new_text = [" ".join(text)]
    new_tfidf = tfIdfVectorizer.transform(new_text)
    new_tfidf.sort_indices()
    new_pred = model.predict_classes(new_tfidf)
    if new_pred[0] == 0:
        return "True"
    else:
        return "Fake"


app = Flask(__name__)

@app.route("/index.html", methods = ['POST', 'GET'])
def home():

    article = request.form.get('article')
    if article:
        result = findClass(str(article))
    else:
        result = None
    return render_template("index.html", article=article, result=result)

@app.route("/methods.html")
def methods():
    return render_template("methods.html")

@app.route("/summary.html")
def summary():
    return render_template("summary.html")


if __name__ == "__main__":
    app.run(debug=True)
