import httpx
import json
from pathlib import Path

OLLAMA_URL = "http://localhost:11434/api/chat"

amount_chat = [
]

PROMPT = {
        "model": "qwen3:4b",
        "messages": [
            {
                "role": "system",
                "content": "Ты QWEN, работающий в интерфейсе терминала. Отвечай кратко, по делу и строго без эмодзи, но всегда учитывай контекст реплик пользователя»."
            }
        ],
        "stream": False
    }

check_memory = Path("./memory")
if check_memory.exists():
    if check_memory.is_dir():
        print("Папка памяти обнаружена.")
    else:
        check_memory.unlink()    
        check_memory.mkdir(exist_ok=True)
else:
    check_memory.mkdir(exist_ok=True)

path_to_memory = Path("./memory")

for i in path_to_memory.iterdir():
    if i.suffix == ".json":
        file = {
            "number": len(amount_chat)+1,
            "file": i.name
        }
        amount_chat.append(file)   


def know_path(pick_user_in_func):
    for i in amount_chat:
        if i.get("number") == pick_user_in_func:
            pre_current_json = i.get("file")
            current_json = "memory/" + pre_current_json
            return current_json, i.get("number")
    return None, 0

while True:
    print("""
     ==========================================
     | Модель - QWEN 3:4B | "Qwenity" VER 1.0 |
     ==========================================

        1. Создать новый чат
        2. Продолжить существующий чат
    """)
    current_json = None
    answer = input()
    if answer == "2":     
        if len(amount_chat) == 0:
            print("Сохранённых чатов пока нет. Создайте новый чат, чтобы начать работу.")
        else:
            for i in amount_chat:
                print("")
                print(f" === Чат №{i.get("number")} ===")
                print(f" Файл: {i.get("file")}")
                print(" ===================")
                print("")
            
            while True:
                while True:
                    try:
                        pick_user = int(input("Напиши номер чата - "))
                        current_json, num = know_path(pick_user)
                        break
                        
                    except ValueError:
                        print("Некорректный ввод. Введите целый номер чата.")
    
                if current_json is None:
                    print("Чат с таким номером не найден. Проверьте номер и попробуйте ещё раз.")
                else:
                    print(f"Чат №{num} успешно выбран.")
                    break
            break
    elif answer == "1":
        while True:
            name_newchat = input("Введи название нового чата - ")
            if len(name_newchat) >= 3:
                break
            else:
                print("Название чата должно содержать не менее 3 символов. Попробуйте ещё раз.")
        check_file = Path(f"./memory/{name_newchat}.json")

        while True:
            if not check_file.is_file():
                file = Path(f"./memory/{name_newchat}.json")
                print(f"Создан новый чат: '{file}'. Чтобы продолжить его позже, выберите второй пункт главного меню.")
                file.touch()
                current_json = f"memory/{name_newchat}.json"
                with open(current_json, "w") as file8:
                    json.dump(PROMPT, file8, indent=2)
                break
            else:
                print("Чат с таким названием уже существует. Выберите другое название.")
                name_newchat = input("Введи название нового чата - ")
                check_file = Path(f"./memory/{name_newchat}.json")
        break
    else:
            print("Неизвестный пункт меню. Введите 1 или 2.")

print()
"""
ФУНКЦИЯ ДОБАВЛЕНИЯ ЗАПРОСА/ОТВЕТА В history.json
"""

def add_prompt(Promptik: dict):
    with open(current_json, "r") as file4:
        json_add = json.load(file4)
    json_add["messages"].append(Promptik)
    with open(current_json, "w") as file5:
        json.dump(json_add, file5, indent=2)



"""
ФУНКЦИЯ ВОСТАНОВЛЕНИЯ СИСТЕМНОГО ПРОМТА
"""

def return_system_promt():
        load_current = PROMPT
        with open(current_json, "w") as file2:
            json.dump(load_current, file2, indent=2)


"""
ПРОВЕРКА НА НАЛИЧИЕ И ЦЕЛОСТНОСТЬ СИСТЕМНОГО ПРОМПТА И ВОСТАНОВЛЕНИЕ ПРИ НЕОБХОДИМОСТИ
"""

history_file = Path(current_json)
if history_file.exists():
    try:
        with open(current_json, "r") as file:
            json_dict = json.load(file)
        if "messages" in json_dict:
            if isinstance(json_dict["messages"], list):
                try:
                    if isinstance(json_dict["messages"][0], dict):
                        if isinstance(json_dict["messages"][0].get("role"), str):
                            if json_dict["messages"][0]["role"] == "system":
                                print("Системный промпт найден. Структура истории выглядит корректной.")
                            else:
                                print("Системный промпт повреждён: роль первого сообщения не равна system. Восстанавливаю исходный промпт.")
                                return_system_promt()
                        else:
                            print("Структура повреждена: значение поля role должно быть строкой. Восстанавливаю исходный промпт.")
                            return_system_promt()
                    else:
                        print("Структура повреждена: первое сообщение должно быть словарём. Восстанавливаю исходный промпт.")
                        return_system_promt()
                except IndexError:
                    print("История повреждена: список messages пуст. Восстанавливаю исходный промпт.")
                    return_system_promt()
                except KeyError:
                    print("История повреждена: не найден обязательный ключ. Восстанавливаю исходный промпт.")
                    return_system_promt()
            else:
                print("История повреждена: поле messages должно содержать список. Восстанавливаю исходный промпт.")
                return_system_promt()
        else:
            print("История повреждена: поле messages отсутствует. Восстанавливаю исходный промпт.")
            return_system_promt()
    except json.decoder.JSONDecodeError:
        with open(current_json, "w") as file3:
            json.dump(PROMPT, file3, indent=2)
else:
    history_file.touch()
    with open(current_json, "w") as file7:
        json.dump(PROMPT, file7, indent=2)
        print("История чата создана и готова к работе.")

"""
ОСНОВНАЯ ЛОГИКА ПРОЕКТА
"""

while True:
    ggg = input("Введите свой промпт для qwen3:4b (Для выхода напиши /bye) - ")
    if ggg != "/bye":
        new_user_prompt = {
            "role": "user",
            "content": ggg
        }

        add_prompt(new_user_prompt)
        try:
            with open(current_json, "r") as file6:
                request_to_ollama = json.load(file6)
            ollama_requrest = httpx.post(OLLAMA_URL, json=request_to_ollama, timeout=300)
            if ollama_requrest.is_success:
                response = ollama_requrest.json()

                new_asistant_prompt = {
                    "role": "assistant",
                    "content": response["message"]["content"]
                }

                add_prompt(new_asistant_prompt)
                print(response["message"]["content"])
            elif ollama_requrest.is_client_error:
                print(f"HTTP {ollama_requrest.status_code}: запрос отклонён. Проверьте параметры запроса и доступность Ollama.")
            elif ollama_requrest.is_server_error:
                print(f"HTTP {ollama_requrest.status_code}: произошла ошибка на стороне сервера Ollama.")
            else:
                print(f"Неожиданный HTTP-статус: {ollama_requrest.status_code}.")
        except httpx.RequestError:
            print("Не удалось связаться с Ollama. Убедитесь, что Ollama запущена и доступна.")
    else:
        break