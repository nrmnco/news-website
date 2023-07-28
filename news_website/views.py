import schedule
import time
from threading import Thread

from django.shortcuts import redirect, render
from django.contrib import messages

from .database.user import UserCollection
from .database.articles import ArticleCollection, Article
from .adapters import ai, bbc_parser
from .decorators import custom_login_required


# Create your views here.
def home(request):
    return render(request, 'index.html')


@custom_login_required
def breaking_news(request):
    # Get all today's articles from the database
    today_articles = ArticleCollection.get_all_todays_articles()

    # Render the breaking_news.html template with the article data
    return render(request, 'breaking_news.html', {'articles': today_articles})


@custom_login_required
def verify_news_view(request):
    if request.method == 'POST':
        news = request.POST.get('news_text', '')
        result = ai.fakenews(news)
        return render(request, 'verify.html', {'result': result})
    else:
        return render(request, 'verify.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = UserCollection.get_user_by_credentials(username, password)
        if user:
            print(123)
            # Save the user's ID in the session to indicate successful login
            request.session['logged_in'] = True
            request.session['user_id'] = str(user.name)
            return redirect('/')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')

    return render(request, 'login.html')


def logout(request):
    # Clear the session data to log the user out
    request.session.clear()
    return redirect('home')


def sign_in(request):
    if request.method == 'POST':
        name = request.POST['name']
        password = request.POST['password']
        topics = request.POST.getlist('topics')[0].split(',')

        # Create the user with the provided data
        created_user_id = UserCollection.create_user_with_topics(
            name,
            password,
            topics)

        if created_user_id:
            # Save the new user's ID in the session to indicate successful
            print(str(created_user_id))
            request.session['user_id'] = str(created_user_id)
            return redirect('/')
        else:
            messages.error(request, 'Failed to create user. Please try again.')

    return render(request, 'sign_in.html')


def parse_articles(request):
    parse_and_store_articles()
    return redirect('/')


def parse_and_store_articles():
    print(123)
    url = "https://www.bbc.com/news/world"

    links = bbc_parser.get_all_todays_urls(url)
    print(links)
    links = set(links)
    for link in links:
        if ArticleCollection.get_article_by_url(link) is None:

            print(link)

            try:
                title = bbc_parser.get_title(link)
                content = bbc_parser.get_article_text(link)
                url = link
                if content == '':
                    print('video')
                    continue

            except Exception as e:
                print(e)
                print('error')
                continue

            ai.new_article()
            brief_content = ai.paraphrase(content)
            topics = ai.get_themes(content)

            article = {
                'title': title,
                'content': brief_content,
                'url': url,
                'topics': topics
            }
            print(article)

        # Store the article in MongoDB using the ArticleCollection
            ArticleCollection.create_article(Article(**article))
            time.sleep(40)


# Schedule the parsing and storing of articles to run every hour
schedule.every().hour.do(parse_and_store_articles)


# Function to run the scheduled tasks
def run_scheduled_tasks():
    while True:
        schedule.run_pending()
        time.sleep(1)


Thread(target=run_scheduled_tasks).start()
