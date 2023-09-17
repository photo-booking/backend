import logging
import requests
from django.conf import settings

from users.models import User
from users.generation_password import generation_password


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def get_data_google(token):
    headers = {'Authorization': 'Bearer ' + token}
    url = 'https://www.googleapis.com/oauth2/v3/userinfo?alt=json'
    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        logging.critical('Error:', exc_info=e)
        return {'error': 'Неверный токен, доступ к аккаунту гугл запрещен'}


def create_google_user(token):
    try:
        data_user = get_data_google(token=token)
        logging.info(f'data user - {data_user}')
        email_user = data_user.get('email')
        first_name = data_user.get('given_name')
        last_name = data_user.get('family_name')
        profile_photo = data_user.get('picture')
    except ValueError:
        return {'error': 'Неверный токен, доступ к аккаунту гугл запрещен'}
    else:
        if User.objects.filter(email=email_user).exists():
            return User.objects.filter(email=email_user)
        else:
            User.objects.create(
                email=email_user,
                first_name=first_name,
                last_name=last_name,
                profile_photo=profile_photo,
                is_client=True,
                password=generation_password())
            return User.objects.filter(email=email_user)


def get_data_vk(code):
    params_dict = {'client_id': {settings.SOCIAL_AUTH_VK_OAUTH2_KEY},
                   'client_secret': {settings.SOCIAL_AUTH_VK_OAUTH2_SECRET},
                   'redirect_uri': 'https://photo-market\
                    .acceleratorpracticum.ru/sign-in',
                   'code': {code}
                   }
    url = 'https://oauth.vk.com/access_token'
    first_response = requests.get(url, params=params_dict)
    token_data = first_response.json()
    logging.info(f'dates from first token {token_data}')
    user_id = token_data.get('user_id')
    access_token = token_data.get('access_token')
    email = token_data.get('email')
    params_dict_vk = {
        'user_ids': {user_id},
        'fields': 'bdate',
        'access_token': {access_token},
        'v': '5.131',
    }

    url_vk = 'https://api.vk.com/method/users.get'
    final_responce = requests.get(url_vk, params=params_dict_vk)
    logging.info(f'dates from last responce {final_responce.json()}')
    return final_responce.json(), email


def create_vk_user(code):
    try:
        user_responce, email = get_data_vk(code)
        logging.info(f'Получили данные из ВК {user_responce}, почта: {email}')
    except ValueError:
        return {'error': 'Неверный токен, доступ к аккаунту гугл запрещен'}
    else:
        if User.objects.filter(email=email).exists():
            return User.objects.filter(email=email)
        else:
            data_user = user_responce.get('response')
            logging.info(f'data user - {data_user}')
            for data in data_user:
                first_name = data.get('first_name')
                last_name = data.get('last_name')
            try:
                User.objects.create(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    is_client=True,
                    password=generation_password())
                return User.objects.filter(email=email)
            except Exception as e:
                logging.critical('Error:', exc_info=e)
                return {'error': 'Пользователь не создан'}
