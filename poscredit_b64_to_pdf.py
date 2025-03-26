# Повзаимствовано у https://github.com/wofiku / ТГ: @cavemeat
# Спешл фор Поскредит. И ТЕБЕ ХЭППИ НЬЮ Э!
# b1.0

# ИМПОРТЫ
from glob import glob  # Поиск файлов в директории в случае массовой выгрузки
from bs4 import BeautifulSoup as Soup  # Парсер; будет вынимать инфу из xml'ки
from base64 import b64decode  # base64 байтовый декодер
from os import mkdir  # Создание директорий; будет создавать папки под доки по номеру заявки
from sys import exit  # Принудительный выход из кода. НЕ ТОТ РЫЧАГ, КРОНК!


# ПЕРЕМЕННЫЕ
all_txt_files: list = glob('*.txt')  # Получаем лист из .txt файлов в текущей директории


# ФУНКЦИИ
def xml_form_to_dict(print_form: list) -> dict:  # Ищем в xml принтформы и делаем из них словарь
    form_name_base64: dict = {}
    for form in print_form:  # Перебираем форму и достаём из неё:
        form_name: str = form.find('printFormName').text  # Имя файла принтформы
        doc_binary: bytes = form.find('binaryData').text  # base64 документ
        form_name_base64[form_name] = doc_binary  # Записываем в словарь: ключ имя файла, значение - base64 документ
    return form_name_base64


def preset_generator(in_file_name: str) -> str:  # Добавляет приставку, берёт её из имени файла
    req_number = in_file_name.split('_')[0]  # Номер запроса
    req_date = in_file_name.rsplit('_')[-3]  # Дата запроса
    req_time = in_file_name.rsplit('_')[-2]  # Время запроса
    preset_to_filename = f'{req_number} {req_date} {req_time}'  # "Номер заявки + дата + время"
    return preset_to_filename


def create_dir(path: str):  # Создание директории
    try:  # Пытаемся создать директорию. Успех - новая директория, провал - ошибка
        mkdir(path)
    except FileExistsError:
        pass  # Если директория существует - пускай; делаем ничего
    except Exception as _e:  # Плюёмся ошибками
        print(f"Ошибка при создании директории {path}:\n{_e}")  # Молодец. Сломал. Чини...
        exit(1)  # Стопорим код по ошибке


def write_file(path: str, file: any):  # Запись файла
    create_dir(path_of_docs)  # Создаём директорию под записываемый файл
    with open(path, 'wb') as pdf_file:
        pdf_file.write(file)


if __name__ == '__main__':  # TODO: разбить этот монолит на модули, НЕ ЗАБУДЬ БАЛИН
    for txt_file in all_txt_files:  # Перебираем все файлы из all_txt_files
        print(f"[PREVIEW] Reading {txt_file}")
        path_of_docs = preset_generator(txt_file)  # Директория где будут храниться файлы

        with open(txt_file, encoding='utf-8', mode='r') as _file:  # Открываем xml файл и достаём из него принтформы
            soup = Soup(_file.read(), 'xml')  # Считываем весь xml файл
            all_print_forms = soup.find_all('printForm')  # Находим все принтформы

            for doc_name, encoded_doc in xml_form_to_dict(all_print_forms).items():  # Перебираем принтформы
                file_name_with_preset = doc_name + '.pdf'  # Имя конечного файла.pdf
                path_to_write_file_to = f'.\\{path_of_docs}\\{file_name_with_preset}'  # Куда записываем PDF файл
                decoded_doc = b64decode(encoded_doc)  # Дешифруем сам документ
                write_file(path=path_to_write_file_to, file=decoded_doc)  # Записываем PDF'ку в текущую директорию
                print(f"[PREVIEW] Successfully wrote \"{path_to_write_file_to}\"")
