from flask import Flask, render_template, request, url_for, redirect
from wtforms import Form, TextAreaField, validators
import pickle
import sqlite3
import os
import numpy as np
import re
from nltk.stem.porter import PorterStemmer

cur_dir = os.path.dirname(__file__)
stemmer = PorterStemmer()
stop_words = pickle.load(open(os.path.join(cur_dir, 'pkl_objects', 'stopwords.pkl'), 'rb'))

def preprocessor(text):
    text = re.sub(r'<[^>]*>', '', text)
    text = re.sub(r'[\W]+', ' ', text.lower())
    return text

def tokenizer(text):
    return [stemmer.stem(word) for word in text.split() if word not in stop_words]

vect = pickle.load(open(os.path.join('pkl_objects', 'tfidfvectorizer.pkl'),'rb')) # ベクトル変換器の読み込み
clf = pickle.load(open(os.path.join('pkl_objects', 'classifier.pkl'),'rb'))  # 分類器の読み込み

app = Flask(__name__)
db = os.path.join(cur_dir, 'movie.sqlite')

def classify(document):
    # documnetの内容がnegativeかpositiveかを判別
    label = {0: 'negative', 1: 'positive'}
    X = vect.transform([preprocessor(document)])
    y = clf.predict(X)[0]
    proba = np.max(clf.predict_proba(X))
    return label[y], proba

def sqlite_entry(path, document, y):
    # pathのデータベースを開き、レビュー文とpositive or negativeと日付を登録
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("INSERT INTO movie_db (review, sentiment, date)"\
    " VALUES (?, ?, DATETIME('now'))", (document, y))
    conn.commit()
    conn.close()

#### Flask ####
class ReviewForm(Form):
    moviereview = TextAreaField('', [validators.DataRequired(),
                                     validators.length(min=15)])

@app.route('/')
def index():
    form = ReviewForm(request.form)
    return render_template('reviewform.html', form=form)

@app.route('/results', methods=['POST'])
def results():
    form = ReviewForm(request.form)
    if request.method == 'POST' and form.validate():
        review = request.form['moviereview']
        y, proba = classify(review)
        return render_template('results.html',
                                content=review,
                                prediction=y,
                                probability=round(proba*100, 2))
    return render_template('reviewform.html', form=form)

@app.route('/feedback', methods=['POST'])
def feedback():
    ### 課題 ###
    # 現在はフォームから送られたreview情報を0(negative)としてデータベースに登録している。
    # ユーザの押したボタン(正しい or 間違い)の情報から正しいpositive or negativeの
    # 情報をデータベースに登録出来るように修正せよ。
    ############
    review = request.form['review']
    feedback = request.form['feedback']
    sentiment = 0
    if feedback == "正しい":
        sentiment = 1
    sqlite_entry(db, review, sentiment)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
