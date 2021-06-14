#!/venv/bin/python3

from configuration import vk_token, ya_token, version
from vk import VkPhotos
from yauploader import YaUploader
import time
from tqdm import tqdm


HELP = '''
тут будет перечень доступных команд
vk - копирование из Vkontakte
ok - Одноклассники
in - Instagram
help - справка
exit - выход
'''


class BackupPhotoVk:

    def __init__(self, ya_token, vk_token, version):

        self.ya_agent = YaUploader(token=ya_token)
        self.vk_agent = VkPhotos(token=vk_token, version=version)
        self.photos_info = self.vk_agent.photos_info()

    def backup(self):

        c = 0
        for photo in tqdm(self.photos_info):
            self.ya_agent.upload_vk_photo(file_name=photo['file_name'], link=photo['link'])
            time.sleep(1)
            c += 1

        print(f'Резервное копирование завершено. Сохранено {c} фотографий.')


class UserAgent:

    def __init__(self):

        self.commands = {
            'vk_ak': 1,
            'vk': self.user_vk_agent
        }

    def user_input(self):

        print(HELP)
        run = True
        while run:
            command = input('Введите комманду: ').lower()

            if command in self.commands:
                self.commands[command]()

            elif command == 'exit':
                print('До новых встреч!')
                run = False

            elif command == 'help':
                print(HELP)

            else:
                print(f'Данная команда {command} не обнаружена. Для справки введите help')

    def user_vk_agent(self):

        vk_default = BackupPhotoVk(ya_token=ya_token, vk_token=vk_token, version=version)
        




if __name__ == '__main__':
    vk_agent = UserAgent()
    vk_agent.user_input()
