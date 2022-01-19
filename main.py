import imp
from flask import Flask,jsonify,request
from storage import liked_articles,not_liked_articles
from demographic_filtering import output
from content_based import get_recommendations

app=Flask(__name__)
@app.route('/get-article')
def get_article():
    return jsonify({
        "data":all_articles[0],
        "status":"success"
    })

@app.route('/liked-article',methods=['POST'])
def liked_article():
    global all_articles
    article=all_articles[0]
    all_articles=all_articles[1:]
    liked_articles.append(article)
    return jsonify({
        "status":"success"
    }),201

@app.route('/not-liked-article',methods=['POST'])
def not_liked_article():
    global all_articles
    article=all_articles[0]
    all_articles=all_articles[1:]
    not_liked_articles.append(article)
    return jsonify({
        "status":"success"
    }),201

@app.route('/popular-articles')
def popular_articles():
    articles_data=[]
    for article in output:
        _d={
            'url':article[0],
            'title':article[1],
            'text':article[2],
            'lang':article[3],
            'total_events':article[4]
        }
        articles_data.append(_d)

    return jsonify({
        "data":articles_data,
        "status":"success"
    }),200

@app.route('/recommended-articles')
def recommended_articles():
    all_recommended=[]
    for liked_article in liked_articles:
        output=get_recommendations(liked_article[4])
        for data in output:
            all_recommended.append(data)
    
    import itertools
    all_recommended.sort()
    all_recommended=list(all_recommended for  all_recommended,_ in itertools.groupby(all_recommended))
    articles_data=[]
    for recommended in all_recommended:
        _d={
            'url':recommended[0],
            'title':recommended[1],
            'text':recommended[2],
            'lang':recommended[3],
            'total_events':recommended[4]
        }
        articles_data.append(_d)

    return jsonify({
        "data":articles_data,
        "status":"success"
    }),200

if __name__=="__main__":
    app.run()


