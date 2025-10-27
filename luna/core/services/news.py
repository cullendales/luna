import bbc
from text_and_audio.tts import respond


def bbc_news():
    news = bbc.news.get_news(bbc.Languages.English)
    categories = news.news_categories()
    for category in categories:
        section_news = news.news_category(World)
        for news_dict in section_news[:5]:
            respond(news_dict['title'])
            respond(news_dict['summary'])
            
def get_news():
    respond("Certainly, here is the news trending today")
    bbc_news()