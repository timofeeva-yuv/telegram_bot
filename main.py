import telebot
import telegram
import time
import requests
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class Bot(telebot.TeleBot):
    def find_info(self, flag, html):
        start = html.find(flag)
        start += len(flag)
        end = start
        if start - len(flag) != -1:
            if html[start - 1] != '>':
                while html[start - 1] != '>':
                    start += 1
            while html[end] != '<':
                end += 1
        return html[start:end]

    def find_town(self, html):
        flag = '<span class="breadcrumbs__title" itemprop="name">'
        start = html.rfind(flag)
        start += len(flag)
        end = start
        if start - len(flag) != -1:
            if html[start - 1] != '>':
                while html[start - 1] != '>':
                    start += 1
            while html[end] != '<':
                end += 1
        return html[start:end]

    def find_url(self, flag, html):
        start = html.find(flag)
        start += len(flag)
        end = start
        if start - len(flag) != -1:
            while html[end] != '"':
                end += 1
        return html[start:end]

    def search(self, message):
        town = message.text
        link = 'https://yandex.ru/pogoda/search?request=' + town
        response = requests.get(link)
        file = response.text
        with open('respond.txt', 'w') as f:
            f.write(file)
        flag_page_title = '<h1 class="title title_level_1">'
        if self.find_info(flag_page_title, file) == 'По вашему запросу ничего не нашлось' or self.find_info(flag_page_title,
                                                                                                  file) == 'Такой страницы не существует':
            bot.send_message(message.from_user.id, 'По вашему запросу ничего не нашлось')
        else:
            answer = []
            flag_first_link = 'class="link link_theme_normal place-list__item-name i-bem" tabindex="0" href="'
            url = self.find_url(flag_first_link, file)
            if url == '':
                url = self.find_url('dataUrl":"', file)
            else:
                url = 'https://yandex.ru' + url
            response = requests.get(url)
            file = response.text
            answer.append(self.find_town(file))
            flags = ['<div class="temp fact__temp fact__temp_size_s"><span class="temp__value">',
                     '<div class="link__condition day-anchor i-bem" data-bem=',
                     '<dl class="term term_orient_h fact__feels-like"><dt class="term__label">',
                     '<dd class="term__value"><div class="temp"><span class="temp__value">',
                     '<p class="maps-widget-fact__title">']
            for flag in flags:
                answer.append(self.find_info(flag, file))
            if 'Погода сейчас и прогноз — на картах' in answer:
                answer[answer.index('Погода сейчас и прогноз — на картах')] = 'Подробности - ' + url
            if answer[0] == '':
                bot.send_message(message.from_user.id, 'По вашему запросу ничего не нашлось. Возможно, в слове ошибка')
            else:
                bot.send_chat_action(message.from_user.id, action=telegram.ChatAction.TYPING)
                time.sleep(1)
                bot.send_message(message.from_user.id, 'По запросу: ' + str(answer.pop(0)))
                bot.send_message(message.from_user.id, str(answer.pop(0)) + " " + str(answer.pop(0)))
                bot.send_message(message.from_user.id, str(answer.pop(0)) + " " + str(answer.pop(0)))
                bot.send_message(message.from_user.id, str(answer.pop(0)))


bot = Bot("your token")


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_chat_action(message.from_user.id, action=telegram.ChatAction.TYPING)
    time.sleep(1)
    bot.send_message(message.from_user.id,
        'Привет! Я бот, показывающий информацию о погоде в разных уголках света.\n'
        'Введи название города или населенного пункта, для которого хочешь узнать ее.\n'
        'Кстати! Я понимаю латиницу! А еще названия, которые были введены неправильно! \n'
        "Но не все... \n"
        "Начнем? Погоду в каком месте хочешь узнать?")


@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.search(message)


def main():
    bot.polling(none_stop=True, interval=0)


if __name__ == "__main__":
    main()
