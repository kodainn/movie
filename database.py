import sqlite3

# データベースに接続
conn = sqlite3.connect('movie.sqlite')
c = conn.cursor()

# テーブルの作成
c.execute('DROP TABLE IF EXISTS movie_db')
c.execute('CREATE TABLE movie_db (review TEXT, sentiment INTEGER, date TEXT)')

# テーブルにデータを登録
review1 = 'I like this movie'
review2 = 'I do not like this movie'
c.execute("INSERT INTO movie_db (review, sentiment, date) VALUES (?, ?, DATETIME('now'))", (review1, 1))
c.execute("INSERT INTO movie_db (review, sentiment, date) VALUES (?, ?, DATETIME('now'))", (review2, 0))
conn.commit()
conn.close()

### 課題 ###
# 以下のSQL文を実行し、結果を表示せよ。
# "SELECT * FROM movie_db WHERE date BETWEEN '2017-01-01 10:10:10' AND DATETIME('now')"
############
conn = sqlite3.connect('movie.sqlite')
c = conn.cursor()
c.execute("SELECT * FROM movie_db WHERE date BETWEEN '2017-01-01 10:10:10' AND DATETIME('now')")
results = c.fetchall()
conn.close()

print(results)