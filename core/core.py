from time import sleep
from telebot.types import ReplyKeyboardMarkup
from telebot import TeleBot

from core.config import TOKEN
from database.db import DataBase


class Bot():
    def __init__(self):
        self.__bot = TeleBot(TOKEN)
        self.__db = DataBase()

        @self.__bot.message_handler(commands=["start"])
        def send_welcome(message):
            self.__bot.reply_to(
                message, "Привет, я бот для поиска работы молодым специалистам.")
            sleep(2)
            self.__bot.send_message(
                message.chat.id, "Давайте определимся кто вы?", reply_markup=None)
            buttons = ReplyKeyboardMarkup(True, True)
            buttons.row("1. Работодатель", "2. Работник")
            sleep(2)
            message = self.__bot.send_message(
                message.chat.id, "1. Я работодатель\n2. Я работник", reply_markup=buttons)

            self.__bot.register_next_step_handler(message, account_type)

        def account_type(message):
            if message.text == "1. Работодатель":
                message = self.__bot.register_next_step_handler(
                    message, register_company)
            elif message.text == "2. Работник":
                self.__bot.send_message(
                    message.chat.id, "круто не иди нахуй")

        def register_company(message):
            company_profile = []
            self.__bot.send_message(
                message.chat.id, "Давайте зарегистрируемся?")

            def get_company_name(message):
                self.__db.get_last_id()
                company_name = self.__bot.send_message(
                    message.chat.id, "Введите название своей компании")
                company_profile.append(company_name)
                self.__bot.register_next_step_handler(
                    message, get_company_description)

            def get_company_description(message):
                company_description = self.__bot.send_message(
                    message.chat.id, "Введите краткое описание своей компании")
                company_profile.append(company_description)
                self.__bot.register_next_step_handler(
                    message, get_company_site_url)

            def get_company_site_url(message):
                company_site = self.__bot.send_message(
                    message.chat.id, "Введите ссылку на сайт своей компании")
                company_profile.append(company_site)
                self.__bot.register_next_step_handler(
                    message, get_company_email)

            def get_company_email(message):
                company_email = self.__bot.send_message(
                    message.chat.id, "Введите корпаративную почту")
                message = company_email
                company_profile.append(company_email)
                self.__bot.register_next_step_handler(
                    message, register_company_in_database, company_profile)

            self.__bot.register_next_step_handler(
                message, get_company_name)

        def register_company_in_database(message, company_profile):
            company_profile = tuple(company_profile)
            self.__db.create_company_profile(self.__db.conn, company_profile)
            self.__bot.send_message(
                message.chat.id, "Зарегистрировал вашу компанию")

    def start(self):
        self.__bot.infinity_polling()
