import pytest
from django.conf import settings
from django.urls import reverse
from datetime import datetime, timedelta 
from django.utils import timezone

# Импортируем класс клиента.
from django.test.client import Client

# Импортируем модель заметки, чтобы создать экземпляр.
from news.models import News, Comment


@pytest.fixture
# Используем встроенную фикстуру для модели пользователей django_user_model.
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):  # Вызываем фикстуру автора.
    # Создаём новый экземпляр клиента, чтобы не менять глобальный.
    client = Client()
    client.force_login(author)  # Логиним автора в клиенте.
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)  # Логиним обычного пользователя в клиенте.
    return client


@pytest.fixture
def news():
    news = News.objects.create(  # Создаём объект заметки.
        title='Новость',
        text='Текст новости',
    )
    return news


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(  # Создаём объект заметки.
        text='Текст комментария',
        author=author,
        news=news,
    )
    return comment


@pytest.fixture
def create_news(db):
    def _create_news(count: int):
        today = datetime.today()
        news_objects = [
            News(
                title=f'Новость {i}',
                text=f'Текст новости {i}',
                date=today - timedelta(days=i),
            )
            for i in range(count)
        ]
        return News.objects.bulk_create(news_objects)
    return _create_news


@pytest.fixture
def create_comments(db, author, news):
    def _create_comments(count: int):
        now = timezone.now()
        for index in range(count):
            # Создаём объект и записываем его в переменную.
            comment = Comment.objects.create(
                news=news, author=author, text=f'Tекст {index}',
            )
            # Сразу после создания меняем время создания комментария.
            comment.created = now + timedelta(days=index)
            # И сохраняем эти изменения.
            comment.save()     
    return _create_comments