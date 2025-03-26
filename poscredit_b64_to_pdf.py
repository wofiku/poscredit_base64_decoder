# Повзаимствовано у https://github.com/wofiku / ТГ: @cavemeat
# Спешл фор Поскредит. И ТЕБЕ ХЭППИ НЬЮ Э!
# v0.3.2b
# Решение по переводу .py в .exe - https://habr.com/ru/sandbox/64702/

# ИМПОРТЫ
from glob import glob  # Поиск файлов в директории в случае массовой выгрузки
from zipfile import ZipFile as zipfile_open
from bs4 import BeautifulSoup as Soup  # Парсер; будет вынимать инфу из xml'ки
from json import loads as json_loads
from base64 import b64decode  # base64 байтовый декодер
from os import mkdir  # Создание директорий; будет создавать папки под доки по номеру заявки


# ПЕРЕМЕННЫЕ
banks_id: dict = {1: "OTP", 2: "RENCREDIT", 3: "RUSFINANCE", 4: "RSB", 5: "VEXPRESS", 6: "ALFABANK", 7: "LETOBANK",
                  8: "TCS", 9: "CEBANK", 10: "CETELEM", 11: "MIGCREDIT", 12: "KVIKU", 13: "MTS", 14: "SOVEST",
                  15: "INSUR_RENLIFE", 16: "INSUR_CAPLIFE", 17: "ALFACARD", 18: "HALVA", 19: "SMSFIN", 20: "CELEADGEN",
                  21: "SOVEST_LEADGEN", 22: "CEBCARD", 23: "INSUR_VSK", 24: "INSUR_D2", 25: "<null>", 26: "HALVACARD",
                  27: "SOVKOMBANK", 28: "ZAPROSTO", 29: "ALFACARDMILE", 30: "EXPO", 31: "HOMECREDIT", 32: "MTSCARD",
                  33: "KUPINEKOPI", 35: "MOKKA", 36: "VDD_HCFB", 37: "VDD_MKK", 39: "VANTA", 40: "ASIACREDIT",
                  43: "OTPCARD", 44: "LOKOBANK", 45: "MKBCARD", 47: "ISLAM", 48: "<null>", 49: "PAYLATE", 51: "DENUM",
                  52: "SOVKOM_HALVA_MKK", 53: "URALSIB", 54: "SBER"}
banks_full_rus: dict = {1: "ОТП Банк", 2: "Ренессанс Кредит Банк", 3: "Русфинанс Банк", 4: "Банк Русский Стандарт",
                        5: "Восточный Банк", 6: "Альфа-Банк", 7: "Почта Банк", 8: "Т-Банк", 9: "Кредит Европа Банк",
                        10: "Сотрудник ТО", 11: "Миг Кредит", 12: "МФО Квику", 13: "МТС-Банк ПАО",
                        14: "Карта \"Совесть\"", 15: "СК \"Ренессанс Жизнь\"",
                        16: "СК «Капитал Лайф Страхование Жизни»", 17: "_Альфа- Карта (неактивно)",
                        18: "Карта «Халва» Лидогенерация", 19: "МФК СМСФинанс", 20: "Кредит Европа Банк Лидогенерация",
                        21: "Карта \"Совесть\" Лидогенерация", 22: "Карта \"Кредит Европа Банк\"",
                        23: "Страховое АО «ВСК»", 24: "АО «Д2 Страхование»", 25: "АО «Группа Ренессанс Страхование»",
                        26: "Карта Рассрочки «Халва»", 27: "Совкомбанк", 28: "Запросто", 29: "Альфа-Карта",
                        30: "Экспобанк", 31: "Хоум Кредит", 32: "МТС Карта", 33: "МКК \"Купи не копи\"", 35: "Мокка",
                        36: "Хоум Кредит ВД", 37: "МКК \"Купи не копи\" ВД", 39: "Ванта Рассрочка", 40: "Азия Кредит",
                        43: "ОТП posline", 44: "ЛОКО", 45: "МКБ Карта", 47: "05RU", 48: "МФК ОТП Финанс", 49: "PayLate",
                        51: "Денум", 52: "Быстрые покупки", 53: "Банк Уралсиб", 54: "Сбербанк"}

soup_docs_logfile_out = {1: 'out_CreateAgreement', 2: 'step4_out', 4: 'out_getPrintFormsRequest',
                         6: 'stepGetPrintForms_out', 8: 'step420_out', 9: 'step5_documents_out',
                         13: 'step2_out_POSITIVE_DECISION_BANK_BRK', 26: 'step3_out', 27: 'step3_out', 29: 'step11_out',
                         44: 'stepapplication_status_out', 52: 'step3_out',
                         53: 'callback_-uralsib-pos-loans-v1-applications-callback-attachments'}
obj_docs_full: dict = {1: 'Document', 2: 'documents', 4: 'printForm', 6: 'printForms', 8: 'return', 9: 'doc',
                       13: 'document', 26: 'documents', 27: 'documents', 29: 'printForms',
                       44: ('contractData', 'contractDocuments'), 52: 'documents',
                       53: ('attachmentsInfo', 'files')}
obj_docs_doc_name: dict = {1: 'Document_Type', 2: None, 4: 'printFormName', 6: 'name', 8: None, 9: 'type',
                           13: 'docTypeName', 26: 'name', 27: 'name', 29: 'name', 44: 'fileName', 52: 'name',
                           53: 'name'}
obj_docs_doc_encoded: dict = {1: 'Document_Buffer', 2: 'oferta', 4: 'binaryData', 6: 'data', 8: 'document',
                              9: 'file_content', 13: 'docData', 26: 'file', 27: 'file', 29: 'data', 44: 'fileData',
                              52: 'file', 53: 'content'}

arch_all: list = glob('*.zip')  # Получаем лист из .zip архивов в текущей директории
txt_all: list = glob('*.txt')  # Получаем лист из .txt файлов в текущей директории
dummy_bytes: bytes = b'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YWRhdGEvU3VidHlwZSAvWE1MPj4Kc3RyZWFtCjw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+DQo8eDp4bXBtZXRhIHhtbG5zOng9ImFkb2JlOm5zOm1ldGEvIj4NCiAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4NCiAgICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczpwZGY9Imh0dHA6Ly9ucy5hZG9iZS5jb20vcGRmLzEuMy8iPg0KICAgICAgPHBkZjpUaXRsZT5tYWdpY2stTDUwTkx4SWFWSE1SWElId2NLUk05bFEwZWVBUzh3ekMmI3gwOzwvcGRmOlRpdGxlPg0KICAgICAgPHBkZjpBdXRob3I+SW1hZ2UmI3gwOzwvcGRmOkF1dGhvcj4NCiAgICAgIDxwZGY6Q3JlYXRvcj5odHRwczovL2ltYWdlbWFnaWNrLm9yZyYjeDA7PC9wZGY6Q3JlYXRvcj4NCiAgICAgIDxwZGY6UHJvZHVjZXI+Q29udmVydEFQSSYjeDA7PC9wZGY6UHJvZHVjZXI+DQogICAgICA8cGRmOkNyZWF0aW9uRGF0ZT4yMDI0LTEyLTExVDEzOjQwOjE3KzAwOjAwPC9wZGY6Q3JlYXRpb25EYXRlPg0KICAgICAgPHBkZjpNb2REYXRlPjIwMjQtMTItMTFUMTM6NDA6MTYrMDA6MDA8L3BkZjpNb2REYXRlPg0KICAgIDwvcmRmOkRlc2NyaXB0aW9uPg0KICAgIDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyI+DQogICAgICA8eG1wOkNyZWF0ZURhdGU+MjAyNC0xMi0xMVQxMzo0MDoxNyswMDowMDwveG1wOkNyZWF0ZURhdGU+DQogICAgICA8eG1wOkNyZWF0b3JUb29sPmh0dHBzOi8vaW1hZ2VtYWdpY2sub3JnJiN4MDs8L3htcDpDcmVhdG9yVG9vbD4NCiAgICAgIDx4bXA6TW9kaWZ5RGF0ZT4yMDI0LTEyLTExVDEzOjQwOjE2KzAwOjAwPC94bXA6TW9kaWZ5RGF0ZT4NCiAgICAgIDx4bXA6TWV0YWRhdGFEYXRlPjIwMjQtMTItMTFUMTM6NDA6MTYrMDA6MDA8L3htcDpNZXRhZGF0YURhdGU+DQogICAgPC9yZGY6RGVzY3JpcHRpb24+DQogICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6ZGM9Imh0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvIj4NCiAgICAgIDxkYzpjcmVhdG9yPg0KICAgICAgICA8cmRmOlNlcT4NCiAgICAgICAgICA8cmRmOmxpPkltYWdlJiN4MDs8L3JkZjpsaT4NCiAgICAgICAgPC9yZGY6U2VxPg0KICAgICAgPC9kYzpjcmVhdG9yPg0KICAgICAgPGRjOnRpdGxlPg0KICAgICAgICA8cmRmOkFsdD4NCiAgICAgICAgICA8cmRmOmxpIHhtbDpsYW5nPSJ4LWRlZmF1bHQiPm1hZ2ljay1MNTBOTHhJYVZITVJYSUh3Y0tSTTlsUTBlZUFTOHd6QyYjeDA7PC9yZGY6bGk+DQogICAgICAgIDwvcmRmOkFsdD4NCiAgICAgIDwvZGM6dGl0bGU+DQogICAgPC9yZGY6RGVzY3JpcHRpb24+DQogIDwvcmRmOlJERj4NCjwveDp4bXBtZXRhPg0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIA0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIA0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIA0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIA0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIA0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIA0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIA0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIA0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIA0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIA0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIA0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIA0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIA0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIA0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIA0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIA0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIA0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIA0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIA0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIA0KPD94cGFja2V0IGVuZD0idyI/PgplbmRzdHJlYW0KZW5kb2JqCjEyIDAgb2JqCjw8L0xlbmd0aCAzNjcvVHlwZSAvT2JqU3RtL04gNy9GaXJzdCAzOS9GaWx0ZXIgL0ZsYXRlRGVjb2RlPj4Kc3RyZWFtCnjabVJha8IwEN1PuW9TxpaktrWKCF2Ls2inqyKC+KG2QbtpU9J0uv36XZvJYAgh5O693HuXCwMKBtgWdIBRCywwbAoOGE4HemA6JmbBosZgQObxnpfIpRCR5VfBgXixio9iT2YFz91EZSKv2TUechWniAJjdTwcAhbQl5oyZJKlJWxQFFHYEk9UuQL2n4eb5Aho0YiXopIJmkDSerZ754mqj8GJgq1lyFyKZMEV9qHjkKdZ/CwuqFU7Y5SCadeCUhS30iJXKFiCqds8VKcddH9b2KApfwRkyS8KUBUNerBtHGfqyKGFmSz5eJxa9HV6CeLVOIzWwficTKKwd3yjnLsL5/zt3bWJW6mDkNBqimDsSR6rOnFQqij7hGQ1oOs9CblHCnaWVglHDpr85FK58+B6E1/ejxU68PsGNUxmMMY6JmXdB0rvcbVJKNKbDPvKaPrT4yCjTK3wtP0bhp4uWQB5EUtBfPwb+k1+ABJin2kKZW5kc3RyZWFtCmVuZG9iagoxMyAwIG9iago8PC9MZW5ndGggNTQvVHlwZSAvWFJlZi9TaXplIDE0L0luZm8gOCAwIFIvUm9vdCAxIDAgUi9JRCBbIDxDRkE2MzAzOTcwRUM0MTQ3NjFDOEFDNzIzNzdFNjVDQzlBMDRDRTI1OTFENEJDMDMzREIyNkFFNTQ1MzkzNkNGPiA8Q0ZBNjMwMzk3MEVDNDE0NzYxQzhBQzcyMzc3RTY1Q0M5QTA0Q0UyNTkxRDRCQzAzM0RCMjZBRTU0NTM5MzZDRj4gXS9XIFsgMSAyIDIgXS9GaWx0ZXIgL0ZsYXRlRGVjb2RlPj4Kc3RyZWFtCnjaY2AAAiYGHgjBCCKYGBn4IVxmRoZiBgZGXn8IlwVEsIIINkbe90AJ6WtAQnYpAwMASZUECwplbmRzdHJlYW0KZW5kb2JqCnN0YXJ0eHJlZgo3NTg5CiUlRU9GCg=='
logger_spl_file_read = "[BETA v0.3] Reading \"{file_reading}\""
logger_spl_file_write: str = "[BETA v0.3] Successfully wrote \"{file_wrote}\""


# ФУНКЦИИ
def check_on_empty(var: any, replace_with: any) -> any:  # Проверка переменной на пустоту
    return replace_with if var in ('', ' ', 'null', None) else var


def check_on_empty_docs(doc_name: str | None, doc_encoded: bytes | str | None) -> tuple:
    # Заменяем пустые поля, чтобы случайно не сломать файлы
    doc_name = check_on_empty(doc_name, "ДОКУМЕНТ")
    doc_encoded = check_on_empty(doc_encoded, dummy_bytes)
    return doc_name, doc_encoded


def create_dir(path: str) -> None:  # Создание директории
    try:  # Пытаемся создать директорию. Успех - новая директория, провал - ошибка
        mkdir(path)
    except FileExistsError:
        pass  # Если директория существует - пускай; делаем ничего
    return None


def write_file(filename: str, path: str, file: any) -> None:  # Запись файла
    create_dir(path)  # Создаём директорию под записываемый файл
    filename_path = f'{path}\\{filename}'  # Полный путь файла
    with open(filename_path, 'wb') as pdf_file:
        pdf_file.write(file)
        print(logger_spl_file_write.format(file_wrote=filename_path))
    return None


def file_decoder(file_name: str = None, file_encoded: bytes = None, path: str = '.',
                 out_extension: str = 'pdf') -> None:  # Декодироваение файлов из base64
    # Имя конечного файла
    file_name_preset = file_name + out_extension if out_extension[0] == '.' else f'{file_name}.{out_extension}'
    decoded_file = b64decode(file_encoded)  # Дешифруем содержимое файла
    write_file(filename=file_name_preset, path=path, file=decoded_file)  # Записываем файл в директорию 'path'
    return None


def preset_generator(in_file_name: str, step_name: str) -> str:  # Добавляет приставку, берёт её из имени файла
    req_number: int = int(in_file_name.split('_')[0])  # Номер запроса
    req_datetime: str = in_file_name.split(step_name)[1][1:-4]  # Дата и время запроса
    preset_to_filename: str = f'{req_number} {req_datetime}'  # "Номер заявки + дата + время"
    return preset_to_filename


def detect_real_file_type(content: str | bytes) -> str:  # Определяет тип файла по его "внутренностям"
    # С помощью первого символа
    first_letter = content[:1].decode('utf-8') if type(content) == bytes else content[:1]
    match first_letter:  # Находим тип файла по первому символу
        case '<':
            file_type: str = 'xml'
        case '{':
            file_type: str = 'json'
        case _:
            file_type: str = "unknown"
    return file_type


def docs_handler_xml(content, bank_id):
    soup = Soup(content, 'xml')  # Считываем весь xml файл
    obj_form_docs = soup.find_all(obj_docs_full[bank_id])  # Находим все тэги с документами
    return obj_form_docs


def docs_handler_json(content, bank_id):
    full_json = json_loads(content)
    obj_docs_full_form = obj_docs_full[bank_id]

    match obj_docs_full_form:
        case tuple() | list() | set():
            obj_form_docs = full_json
            for _obj in obj_docs_full_form:
                obj_form_docs = obj_form_docs[_obj] if obj_form_docs and _obj in obj_form_docs else None
        case str() | _:
            obj_form_docs = full_json[obj_docs_full_form] if obj_docs_full_form in full_json else None
    return obj_form_docs


def find_docs(file: str, bank_id: int, archive: str) -> tuple:
    check_on_empty(var=archive, replace_with=None)
    # Открываем xml файл
    file = zipfile_open(archive, 'r').open(file, 'r') if archive else open(file, encoding='utf-8', mode='r')
    file_content = file.read()  # Содержимое файла
    file_type = detect_real_file_type(content=file_content)  # Определяем тип файла, чтобы узнать, где в нём искать
    # документы

    match file_type:
        case 'xml':
            form_docs = docs_handler_xml(content=file_content, bank_id=bank_id)
        case 'json':
            form_docs = docs_handler_json(content=file_content, bank_id=bank_id)
        case _:
            form_docs = None
    file.close()  # Закрываем файл/архив, чтобы не засорять память
    return form_docs, file_type


def form_to_dict(docs_form: list, bank_id: int, file_type: str) -> dict:  # Ищем в xml принтформы файлов и делаем из них словарь
    # ПЕРЕМЕННЫЕ
    obj_docs_doc_name_current = obj_docs_doc_name[bank_id]
    obj_docs_doc_encoded_current = obj_docs_doc_encoded[bank_id]
    filename_with_base64: dict = {}

    if docs_form:
        for form in docs_form:  # Перебираем форму и достаём из неё:
            match file_type:
                case 'xml':
                    form_name: str = form.find(obj_docs_doc_name_current).text if obj_docs_doc_name_current else None  # Имя будущего файла
                    doc_binary: bytes = form.find(obj_docs_doc_encoded_current).text if obj_docs_doc_encoded_current else None # base64 файл
                case 'json':
                    form_name: str = form[obj_docs_doc_name_current] if obj_docs_doc_name_current else None
                    doc_binary: bytes = form[obj_docs_doc_encoded_current] if obj_docs_doc_encoded_current else None
                case _:
                    form_name, doc_binary = None, None
            form_name, doc_binary = check_on_empty_docs(form_name, doc_binary)
            filename_with_base64[form_name] = doc_binary  # Записываем в словарь: ключ - имя файла, значение - base64 файл
    return filename_with_base64


def encoded_docs_to_pdf(docs_form, path: str, bank_id: int, file_type: str) -> None:  # Перебирает форму, сохраняет найденные документы в PDF
    for doc_name, encoded_doc in form_to_dict(docs_form=docs_form, bank_id=bank_id, file_type=file_type).items():
        file_decoder(file_name=doc_name, file_encoded=encoded_doc, path=str(path), out_extension='pdf')
    return None


def get_bank_id_by_arch(archive: str) -> int:  # Поиск ID банка по имени архива
    bank_id: int = int(archive.split('bank')[1].split('-')[0])  # Ищем ID банка
    return bank_id


def arch_export_out_docs(archive: str) -> None:
    print(logger_spl_file_read.format(file_reading=archive))
    # Распаковка архива и поиск логфайла, который прислал банк
    # ПЕРЕМЕННЫЕ
    bank_id: int = get_bank_id_by_arch(archive=archive)
    step_name = soup_docs_logfile_out[bank_id]
    arch = zipfile_open(archive, 'r')
    arch_files: list = arch.namelist()
    arch_files_docs_out: list = [file_doc for file_doc in arch_files if step_name in file_doc]

    for file_txt in arch_files_docs_out:
        # Директория где будут храниться файлы
        docs_form = find_docs(file=file_txt, bank_id=bank_id, archive=archive)[0]
        docs_file_type = find_docs(file=file_txt, bank_id=bank_id, archive=archive)[1]
        docs_path = f'.\\{preset_generator(in_file_name=file_txt, step_name=step_name)}'
        # Сохраняем документы из файла
        encoded_docs_to_pdf(docs_form=docs_form, path=docs_path, bank_id=bank_id, file_type=docs_file_type)
    return None


# MAIN
if __name__ == '__main__':
    for arch_name in arch_all:
        arch_export_out_docs(archive=arch_name)
