#!/usr/bin/python3

import requests
import time
from configuration import vk_token, version
from pprint import pprint


class VkPhotos:
    URL = 'https://api.vk.com/method/'

    def __init__(self, token, version):

        self.token = token
        self.version = version
        self.params = {
            'access_token': self.token,
            'v': self.version
        }
        self.owner_id = requests.get(self.URL + 'users.get', self.params).json()['response'][0]['id']

    def user_info(self):

        user_url = self.URL + 'users.get'
        user_id = input(
           'Введите id пользователя, или его короткое имя (screen_name).\n'
           'Для текущего пользователя оставьте поле пустым нажав Enter: '
            )
        if user_id == '':
            user_id = self.owner_id
        user_params = {
            'user_ids': user_id
        }
        params = {**self.params, **user_params}
        response = requests.get(user_url, params).json()

        self.first_name = response['response'][0]['first_name']
        self.last_name = response['response'][0]['last_name']
        self.user_id = response['response'][0]['id']
        print(f'Найден пользователь {self.first_name} {self.last_name} id: {self.user_id}')

        return self.first_name, self.last_name, self.user_id

    def albums(self):

        self.user_info()

        albums_url = self.URL + 'photos.getAlbums'
        albums_params = {
            'owner_id': self.user_id,
            'need_system': 1,
        }

        params = {**self.params, **albums_params}
        response = requests.get(albums_url, params).json()
        pprint(response)

        return response

    def photos_get(self):

        self.user_info()

        photos_url = self.URL + 'photos.get'
        photos_params = {
            'owner_id': self.user_id,
            'album_id': 'profile',
            'rev': 0,
            'extended': 1,
            'count': 13
        }

        params = {**self.params, **photos_params}
        response = requests.get(photos_url, params).json()

        return response

    def photos_info(self):
        items = self.photos_get()['response']['items']
        photos_info = []
        info = {}
        likes_count = []
        repeat_likes_count = []

        for like in items:
            likes_count.append(like['likes']['count'])

        for like in likes_count:
            if likes_count.count(like) > 1:
                repeat_likes_count.append(like)

        for item in items:
            like = item['likes']['count']
            date_photo = time.strftime('%d%m%y', time.gmtime(item['date']))
            info = {
                'size': item['sizes'][-1]['type'],
                'link': item['sizes'][-1]['url']
            }

            if like in repeat_likes_count:
                info['file_name'] = f'{like}_{date_photo}.jpg'
                photos_info.append(info)

            else:
                info['file_name'] = f'{like}.jpg'
                photos_info.append(info)
                        
        return photos_info


if __name__ == '__main__':
    user = VkPhotos(token=vk_token, version=version)
    # q = user.user_info()
    # print(q)
    # user.photos_get()
    user.albums()
