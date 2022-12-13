from urllib.parse import parse_qs

from bottle import redirect, request, route, run, template
from bayes import NaiveBayesClassifier

from db import News, Session
from scraputils import get_news


@route("/")
def root():
    redirect("/news")


@route("/news")
def news_list():
    session = Session()
    rows = session.query(News).filter(News.label == None).all()
    return template("news_template", rows=rows)


@route("/add_label/")
def add_label():
    args = parse_qs(request.query_string)
    news_id = int(args["id"][0])
    news_type = args["label"][0]
    s = Session()
    s.query(News).filter(News.id == news_id).update({"label": news_type})
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    news = get_news("https://news.ycombinator.com/newest")
    session = Session()
    for new in news:
        if (
            not len(
                session.query(News)
                .filter(News.author == new["author"], News.title == new["title"])
                .all()
            )
            and len(new.keys()) == 5
        ):
            session.add(
                News(
                    author=new["author"],
                    title=new["title"],
                    points=new["points"],
                    comments=new["comments"],
                    url=new["url"],
                )
            )
    session.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    redirect("/recommendations")


@route("/recommendations")
def recommendations():
    session = Session()
    classified = session.query(News).filter(News.label != None).all()
    classified_titles = []
    classified_types = []
    for row in classified:
        classified_titles.append(row.title)
        classified_types.append(row.label)
    class_bot = NaiveBayesClassifier(1)
    guess_rows = session.query(News).filter(News.label == None).all()
    guess_titles = []
    class_bot.fit(classified_titles, classified_types)
    for row in guess_rows:
        guess_titles.append(row.title)
    guess_types = class_bot.predict(guess_titles)
    rows = []
    for type in ("good", "maybe", "never"):
        ind = 0
        for guess_type in guess_types:
            if guess_type == type:
                rows.append(guess_rows[ind])
            ind += 1
    return template("news_template", rows=rows)


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)
