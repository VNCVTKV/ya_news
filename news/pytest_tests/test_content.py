from django.urls import reverse
from django.conf import settings

from django.test.client import Client
import pytest
from news.forms import CommentForm

@pytest.mark.django_db
def test_news_count(create_news):
    # Загружаем главную страницу.
    client = Client()
    create_news(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    response = client.get(reverse('news:home'))
    # Код ответа не проверяем, его уже проверили в тестах маршрутов.
    # Получаем список объектов из словаря контекста.
    object_list = response.context['object_list']
    # Определяем количество записей в списке.
    news_count = object_list.count()
    # Проверяем, что на странице именно 10 новостей.
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(create_news):
        
        client = Client()
        create_news(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
        response = client.get(reverse('news:home'))
        object_list = response.context['object_list']
        # Получаем даты новостей в том порядке, как они выведены на странице.
        all_dates = [news.date for news in object_list]
        # Сортируем полученный список по убыванию.
        sorted_dates = sorted(all_dates, reverse=True)
        # Проверяем, что исходный список был отсортирован правильно.
        assert all_dates == sorted_dates
 
@pytest.mark.django_db
def test_comments_order(create_comments, news):
        
        client = Client()
        create_comments(10)
        detail_url = reverse('news:detail', args=(news.id,))
        response = client.get(detail_url)
        # Проверяем, что объект новости находится в словаре контекста
        # под ожидаемым именем - названием модели.
        assert 'news' in response.context
        # Получаем объект новости.
        news = response.context['news']
        # Получаем все комментарии к новости.
        all_comments = news.comment_set.all()
        # Собираем временные метки всех новостей.
        all_timestamps = [comment.created for comment in all_comments]
        # Сортируем временные метки, менять порядок сортировки не надо.
        sorted_timestamps = sorted(all_timestamps)
        # Проверяем, что id первого комментария меньше id второго.
        assert all_timestamps == sorted_timestamps 

@pytest.mark.django_db
def test_anonymous_client_has_no_form(news):
        client = Client()
        detail_url = reverse('news:detail', args=(news.id,))
        response = client.get(detail_url)
        assert 'form' not in response.context

@pytest.mark.django_db
def test_authorized_client_has_form(news, author_client):
        # Авторизуем клиент при помощи ранее созданного пользователя.
        detail_url = reverse('news:detail', args=(news.id,))
        response = author_client.get(detail_url)
        assert 'form' in response.context
        # Проверим, что объект формы соответствует нужному классу формы.
        assert isinstance(response.context['form'], CommentForm) 


 