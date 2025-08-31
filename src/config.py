from configparser import ConfigParser

def config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename, encoding='utf-8')
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            value = str(param[1]).strip()
            try:
                value = value.encode('utf-8').decode('utf-8')
                db[param[0]] = value
                print(f"Parameter {param[0]}: {value} (raw: {repr(value)})")  # Отладка
            except UnicodeDecodeError as e:
                print(f"Ошибка кодировки в параметре {param[0]}: {e}")
                raise
    else:
        raise Exception(f"Секция {section} не найдена в файле {filename}.")
    return db