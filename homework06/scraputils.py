import requests  # type: ignore
from bs4 import BeautifulSoup


def extract_news(parser: BeautifulSoup) -> list:
    """Extract news from https://news.ycombinator.com/newest site"""
    news = []
    title_lines = list(
        map(
            lambda x: x.find("span", {"class": "titleline"}),
            parser.findAll("tr", {"class": "athing"}),
        )
    )
    sub_lines = parser.findAll("td", {"class": "subtext"})
    for i in range(0, len(title_lines)):
        title_line = title_lines[i]
        sub_line = sub_lines[i]
        title = title_line.find("a").text
        author = sub_line.find("a", {"class": "hnuser"}).text
        url = title_line.find("a")["href"]
        # comments = sub_line.find("comment").text[:sub_line.find("comment").text.find("&")]
        comments = sub_line.find("a")[-1].text
        print(comments)
        points = sub_line.find("span", {"class": "score"}).text
        news.append(
            {
                "title": title,
                "author": author,
                "url": url,
                "comments": comments,
                "points": points,
            }
        )
    return news


def extract_next_page(parser: BeautifulSoup) -> str:
    """Extract next page URL"""
    return parser.table.findAll("table")[1].findAll("tr")[-1].contents[2].find("a").get("href")


def get_news(url, n_pages=1):
    """Collect news from a given web page"""
    news = []
    for i in range(0, n_pages):
        response = requests.get(url)
        parser = BeautifulSoup(response.text, "html.parser")
        news_arr = extract_news(parser)
        next_page = extract_next_page(parser)
        if next_page is None:
            return news
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_arr)
    return news
