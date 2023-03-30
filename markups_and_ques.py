from telegram import ReplyKeyboardMarkup
from db_data.work_with_db import get_questions

main_markup = ReplyKeyboardMarkup(
    [["1-4 классы", "5-11 классы"]], one_time_keyboard=False
)

# предлагает выбрать смену
groups = ReplyKeyboardMarkup([['1-я смена (29 мая - 9 июня)'],
                              ['2-я смена (13 июня - 23 июня)']], one_time_keyboard=False)

# меню с выбором действий для 1-4 классов
markup_1 = ReplyKeyboardMarkup(
    [['Летние образовательные смены'],
     ['Летние курсы'],
     ['Назад']], one_time_keyboard=False)

# меню вопросов для летних образовательных программ для 1-4 классов
markup_1_1 = ReplyKeyboardMarkup(
    [['Описание', 'Стоимость', 'Расписание'],
     ['Вопросы', 'Адрес', 'Контакты'],
     ['Назад']], one_time_keyboard=False)

# меню вопросов для летних курсов
markup_1_2 = ReplyKeyboardMarkup(
    [['Каллиграфия', 'Курс1', 'Курс2'],
     ['Назад']], one_time_keyboard=False)

# пока что просто вопросы для 5-11 классов
markup_5 = ReplyKeyboardMarkup(
    [['Летние курсы'],
     ['Назад']], one_time_keyboard=False)

markup_courses = ReplyKeyboardMarkup(
    [['Описание'],
     ['Записаться на курс'],
     ['Назад']], one_time_keyboard=False)

markup_address = ReplyKeyboardMarkup(
    [['Сиреневый бульвар'],
     ['Микрорайон В'],
     ['Назад']], one_time_keyboard=False)

que_dct_1 = que_dct_5 = get_questions()  # получение данных из бд
markup_q_1 = markup_q_5 = ReplyKeyboardMarkup([['Назад']] + list(map(lambda x: [x], que_dct_1)),
                                              one_time_keyboard=False)
