from time import sleep
from telebot.types import ReplyKeyboardMarkup
from telebot import TeleBot

from core.config import TOKEN
from database.db import DataBase


class Bot():
    def __init__(self):
        self.bot = TeleBot(TOKEN)
        self.db = DataBase()
        self.conn = self.db.conn

        @self.bot.message_handler(commands=['start'])
        def start_message(message):
            self.bot.reply_to(
                message, "Привет, я бот для поиска работы в Москве")
            registration_type(message)

        def registration_type(message):
            button = ReplyKeyboardMarkup(True, True)
            button.row("1.Работодатель", "2.Работник")
            self.bot.send_message(
                message.chat.id, "Давайте определимся кто вы?")
            self.bot.send_message(
                message.chat.id, "1.Работодатель\n2.Работник", reply_markup=button)
            self.bot.register_next_step_handler(message, registration)

        def registration(message):
            
            if message.text == "1.Работодатель":
                register_company(message)
            if message.text == "2.Работник":
                register_worker(message)

        def register_company(message):
            company_profile = []

            def get_company_name(message):
                company_profile.append(message.from_user.id)
                self.bot.send_message(
                    message.chat.id, "Введите название компании")
                self.bot.register_next_step_handler(
                    message, get_company_description)

            def get_company_description(message):
                company_profile.append(message.text)
                self.bot.send_message(
                    message.chat.id, "Введите описание компании")
                self.bot.register_next_step_handler(
                    message, get_company_url)

            def get_company_url(message):
                company_profile.append(message.text)
                self.bot.send_message(
                    message.chat.id, "Введите ссылку на сайт компании")
                self.bot.register_next_step_handler(
                    message, get_company_email)

            def get_company_email(message):
                company_profile.append(message.text)
                self.bot.send_message(
                    message.chat.id, "Введите email компании")
                self.bot.register_next_step_handler(
                    message, set_company_email)

            def set_company_email(message):
                company_profile.append(message.text)
                register_company_in_database(message, company_profile)
            get_company_name(message)

        def register_worker(message):
            user_profile = []

            def get_user_name(message):
                user_profile.append(message.from_user.id)
                self.bot.send_message(
                    message.chat.id, "Как вас зовут?")
                self.bot.register_next_step_handler(
                    message, get_user_lastname)

            def get_user_lastname(message):
                user_profile.append(message.text)
                self.bot.send_message(
                    message.chat.id, "Какая у вас фамилия?")
                self.bot.register_next_step_handler(
                    message, get_user_age)

            def get_user_age(message):
                user_profile.append(message.text)
                self.bot.send_message(
                    message.chat.id, "Сколько вам лет?")
                self.bot.register_next_step_handler(
                    message, get_user_position)

            def get_user_position(message):
                user_profile.append(message.text)
                self.bot.send_message(
                    message.chat.id, "Накакой должности вы хотите работать")
                self.bot.register_next_step_handler(
                    message, get_user_email)

            def get_user_email(message):
                user_profile.append(message.text)
                self.bot.send_message(
                    message.chat.id, "Ваш email?")
                self.bot.register_next_step_handler(
                    message, get_user_tg_url)

            def get_user_tg_url(message):
                user_profile.append(message.text)
                user_profile.append(
                    f"https://t.me/{message.from_user.username}")
                register_user_in_database(message, user_profile)
            get_user_name(message)

        def register_company_in_database(message, company_profile):
            company_profile = tuple(company_profile)
            print(company_profile)
            self.db.create_company_profile(self.conn, company_profile)
            self.bot.send_message(
                message.chat.id, "Зарегистрировал вашу компанию")

        def register_user_in_database(message, user_profile):
            user_profile = tuple(user_profile)
            print(user_profile)
            self.db.create_worker_profile(self.conn, user_profile)
            self.bot.send_message(
                message.chat.id, "Зарегистрировал ваш")

    def start(self):
        self.bot.infinity_polling()
