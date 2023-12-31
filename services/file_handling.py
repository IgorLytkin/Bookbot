import os
import sys

BOOK_PATH = 'book/book.txt'
PAGE_SIZE = 1050

book: dict[int, str] = {}

# Реализуйте функцию _get_part_text(), которая принимает три аргумента в следующем порядке:
#   text - строка с полным текстом, из которого нужно получить страницу не больше заданного размера
#   start - номер первого символа в тексте, с которого должна начинаться страница (нумерация идет с нуля)
#   page_size - максимальный размер страницы, которая должна получиться на выходе
# Функция должна вернуть текст страницы (тип str) и ее получившийся размер в символах (тип int).
# Список знаков препинания, которые могут быть окончанием текста страницы, состоит из знаков:
#   , - запятая
#   . - точка
#   ! - восклицательный знак
#   : - двоеточие
#   ; - точка с запятой
#   ? - вопросительный знак
# Примечание 1. Гарантируется, что подаваемый в функцию текст, не пустой, а в тексте страницы обязательно встретятся
# знаки препинания из списка выше
# Примечание 2. Также гарантируется, что стартовый символ будет меньше, чем длина подаваемого в функцию текста.
# Примечание 3. Если в тексте встречается многоточие (а также другие сочетания идущих подряд знаков препинания,
# типа, ?!, ?.., !.. и т.п.) - они либо целиком должны попасть в текущую страницу, либо не попасть в страницу вообще.
# Нельзя разорвать такую последовательность, потому что следующая страница книги тогда начнется с точки, точек или
# других знаков препинания, что для пользователя будет смотреться, как неправильное форматирование текста.
# Примечание 4. Обрезать невидимые символы (перенос строки, пробел и т.п.), получившиеся слева от текста, не надо.


def _get_part_text(p_text: str, start: int, page_size: int) -> tuple[str, int]:
    stop_symbols: str = ',.!:;?'  # знаки препинания
    len_text = len(p_text)
    len_result = page_size  # длина возвращаемой страницы
    # Особый случай 1 - последняя страница текста, возвращаем остаток text от start до конца text
    if start + page_size > len_text:
        len_result = len_text - start  # длина остатка текста от start до конца
    # Проверяем последний символ страницы на принадлежность множеству стоп-символов
    else:
        c_end = p_text[start + page_size - 1: start + page_size]       # последний символ страницы
        c_end_1 = p_text[start + page_size - 2: start + page_size - 1]   # предпоследний символ страницы
        if c_end == '.':  # если последний символ точка - проверяем предпоследний
            if c_end_1 in stop_symbols:   # если предпоследний символ - знак препинания (..)
                len_result = page_size-2  # пропускаем 2 символа
            else:  # предпоследний символ - не знак препинания
                len_result = page_size  # предпоследний символ, последний точка, возвращаем до точки включительно
    # если последний символ страницы это обычный символ, то идём влево до любого из стоп-символов
    while p_text[start + len_result - 1: start + len_result] not in stop_symbols:
        len_result -= 1
    return p_text[start:start + len_result], len_result

# Функция, формирующая словарь книги


# Функция, возвращающая строку с текстом страницы и ее размер (автор: Михаил Крыжановский @kmsint)
# https://github.com/kmsint/aiogram3_stepik_course/blob/master/book_bot/services/file_handling.py
def _get_part_text_kmsint(p_text: str, start: int, size: int) -> tuple[str, int]:
    end_signs = ',.!:;?'
    counter = 0
    if len(p_text) < start + size:
        size = len(p_text) - start
        p_text = p_text[start:start + size]
    else:
        if p_text[start + size] == '.' and p_text[start + size - 1] in end_signs:
            p_text = p_text[start:start + size - 2]
            size -= 2
        else:
            p_text = p_text[start:start + size]
        for i in range(size - 1, 0, -1):
            if p_text[i] in end_signs:
                break
            counter = size - i
    page_text = p_text[:size - counter]
    page_size = size - counter
    return page_text, page_size


# Тесты
# text = '0123456789, 01234567890 123456789'
# print(*_get_part_text(text, 0, 20), sep='\n')
# print(*_get_part_text_kmsint(text, 0, 20), sep='\n')

# text = 'Раз. Два. Три. Четыре. Пять. Прием!'
# print(*_get_part_text(text, 5, 9), sep='\n')
# print(*_get_part_text_kmsint(text, 5, 9), sep='\n')

# text = ('Да? Вы точно уверены? Может быть, вам это показалось?.. Ну, хорошо, приходите завтра, тогда и посмотрим, что '
#         'можно сделать. И никаких возражений! Завтра, значит, завтра!')
# print(*_get_part_text(text, 22, 145), sep='\n')

# text = ('— Я всё очень тщательно проверил, — сказал компьютер, — и со всей определённостью заявляю, что это и есть '
#         'ответ. Мне кажется, если уж быть с вами абсолютно честным, то всё дело в том, что вы сами не знали, '
#         'в чём вопрос.')
# print(*_get_part_text(text, 54, 70), sep='\n')

def prepare_book(path: str) -> None:
    with open(file=path, mode='r', encoding='utf-8') as file:
        p_text: str = file.read()
    start, page_number = 0, 1
    while start < len(p_text):
        page_text, page_size = _get_part_text_kmsint(p_text, start, PAGE_SIZE)
        start += page_size
        book[page_number] = page_text.strip()
        page_number += 1
    print(book)


# Вызов функции prepare_book для подготовки книги из текстового файла
prepare_book(os.path.join(sys.path[0], os.path.normpath(BOOK_PATH)))
# print(book)
