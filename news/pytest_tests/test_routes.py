from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertRedirects
import pytest


# Указываем в фикстурах встроенный клиент.
@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',  # Имя параметра функции.
    # Значения, которые будут передаваться в name.
    (   
        ('news:detail', pytest.lazy_fixture('news')),
        ('news:home', None),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),
    ),
)
# Указываем имя изменяемого параметра в сигнатуре теста.
def test_pages_availability_for_anonymous_user(client, name, args):
    if args is not None:
        url = reverse(name, args=(args.id,))
    else:    
        url = reverse(name)  # Получаем ссылку на нужный адрес.
    response = client.get(url)  # Выполняем запрос.
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    # Предварительно оборачиваем имена фикстур 
    # в вызов функции pytest.lazy_fixture().
    (
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'name',
    ('news:delete', 'news:edit',),
)
def test_pages_availability_for_author(
        parametrized_client, author_client, name, comment, expected_status
):
    url = reverse(name, args=(comment.id,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    ('news:delete', 'news:edit',),
)
# Передаём в тест анонимный клиент, name проверяемых страниц и args:
def test_redirects(client, name, comment):
    login_url = reverse('users:login')
    # Теперь не надо писать никаких if и можно обойтись одним выражением.
    url = reverse(name, args=(comment.id,))
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)