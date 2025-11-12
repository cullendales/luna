import bbc
from text_and_audio.tts import respond


def get_news(category="US & Canada news"):
    news = bbc.news.get_news(bbc.Languages.English)
    categories = news.news_categories()
    print("Available categories:", categories)

    if category not in categories:
        respond(f"Sorry, I couldn't find the category '{category}'. Showing 'Latest' instead.")
        category = "Latest"

    section_news = news.news_category(category)
    for news_dict in section_news[:5]:
        title = news_dict.get("title")
        summary = news_dict.get("summary")

        if title:
            respond(title)
        if summary and isinstance(summary, str):
            respond(summary)
        else:
            respond("No summary available for this story.")
