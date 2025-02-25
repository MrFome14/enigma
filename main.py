import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from cryptography.fernet import Fernet
from yadisk import YaDisk

OAuthCode = "y0__xDkjoCcAxifqDUg67vKphI1gJqnCmtW8nWqVfu1qVRkDkhqdw" # Вставьте сюда ключ


# Шаг 1: Генерация ключа для шифрования
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)


# Шаг 2: Загрузка ключа
def load_key():
    return open("secret.key", "rb").read()


# Шаг 3: Шифрование файла
def encrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, "rb") as file:
        original_data = file.read()

    # Добавляем оригинальное имя файла в начало данных
    original_name = os.path.basename(file_path).encode()  # Преобразуем имя в байты
    encrypted_data = fernet.encrypt(original_name + b"|||" + original_data)  # Разделитель "|||"

    encrypted_file_path = file_path + ".encrypted"
    with open(encrypted_file_path, "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)
    return encrypted_file_path


# Шаг 4: Дешифрование файла
def decrypt_file(encrypted_file_path, key):
    fernet = Fernet(key)
    with open(encrypted_file_path, "rb") as encrypted_file:
        encrypted_data = encrypted_file.read()

    # Дешифруем данные
    decrypted_data = fernet.decrypt(encrypted_data)

    # Извлекаем оригинальное имя файла
    original_name, _, file_data = decrypted_data.partition(b"|||")
    original_name = original_name.decode()  # Преобразуем байты обратно в строку

    # Создаем папку decrypted_files, если её нет
    decrypted_folder = "decrypted_files"
    if not os.path.exists(decrypted_folder):
        os.makedirs(decrypted_folder)

    # Сохраняем файл с оригинальным именем в папке decrypted_files
    decrypted_file_path = os.path.join(decrypted_folder, original_name)
    with open(decrypted_file_path, "wb") as decrypted_file:
        decrypted_file.write(file_data)

    # Удаляем зашифрованный файл
    os.remove(encrypted_file_path)

    return decrypted_file_path


# Шаг 5: Авторизация на Яндекс.Диске
def authorize_yadisk(token):
    ydisk = YaDisk(token=token)
    if not ydisk.check_token():
        raise Exception("Неверный токен Яндекс.Диска")
    return ydisk


# Шаг 6: Загрузка файла на Яндекс.Диск
def upload_to_yadisk(ydisk, file_path, remote_path):
    if not ydisk.exists(remote_path):
        ydisk.mkdir(remote_path)  # Создаем папку, если её нет
    remote_file_path = f"{remote_path}/{os.path.basename(file_path)}"
    ydisk.upload(file_path, remote_file_path)
    messagebox.showinfo("Успех!", f"Файл {file_path} успешно загружен на Яндекс.Диск в папку {remote_path}.")


# Шаг 7: Скачивание файла с Яндекс.Диска
def download_from_yadisk(ydisk, remote_file_path, local_file_path):
    ydisk.download(remote_file_path, local_file_path)
    messagebox.showinfo("Успех!", f"Файл {remote_file_path} успешно скачан на локальный компьютер как {local_file_path}.")


class EnigmaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Enigma")
        self.geometry("1920x1040")
        self.create_widgets()

    def create_widgets(self):
        # Настройка внешнего вида окна
        self.configure(bg = "#333333")  # Серый фон окна

        # Метка заголовка
        title_label = tk.Label(self, text = "Добро пожаловать в Enigma!", font = ("Arial", 36, "bold"), fg = "white",
                               bg = "#333333")
        title_label.pack(pady = (40, 50))  # Увеличенное расстояние сверху и снизу

        # Рамка для выравнивания кнопок по центру
        button_frame = tk.Frame(self, bg = "#333333")
        button_frame.pack(pady = 30)

        # Кнопка выбора файла для шифрования
        encrypt_button = tk.Button(button_frame, text = "Зашифровать",
                                   command = self.encrypt_and_upload,
                                   font = ("Arial", 16, "bold"),
                                   fg = "white",  # Белый текст
                                   bg = "#FF9F1C",  # Приятный оранжевый цвет
                                   activebackground = "#E87200",  # Темнее при нажатии
                                   bd = 5,  # Толстая черная окантовка
                                   relief = tk.SOLID,  # Четкие края
                                   width = 25, height = 2)
        encrypt_button.pack(pady = 20)

        # Кнопка скачивания и дешифрования файла
        decrypt_button = tk.Button(button_frame, text = "Расшифровать",
                                   command = self.download_and_decrypt,
                                   font = ("Arial", 16, "bold"),
                                   fg = "white",  # Белый текст
                                   bg = "#FF9F1C",  # Приятный оранжевый цвет
                                   activebackground = "#E87200",  # Темнее при нажатии
                                   bd = 5,  # Толстая черная окантовка
                                   relief = tk.SOLID,  # Четкие края
                                   width = 25, height = 2)
        decrypt_button.pack(pady = 20)

    def encrypt_and_upload(self):
        # Генерация ключа (если его нет)
        if not os.path.exists("secret.key"):
            generate_key()
        key = load_key()

        # Выбор файла для шифрования
        file_path = filedialog.askopenfilename(title="Выберите файл для шифрования")
        if not file_path:
            return

        # Шифрование файла
        encrypted_file_path = encrypt_file(file_path, key)
        messagebox.showinfo("Успешное шифрование", f"Файл зашифрован и сохранен как {encrypted_file_path}")

        # Авторизация на Яндекс.Диске
        if OAuthCode == "":
            token = simpledialog.askstring("Авторизация", "Введите OAuth-токен Яндекс.Диска:", show = "*")
        else:
            token = OAuthCode
        try:
            ydisk = authorize_yadisk(token)
        except Exception as e:
            messagebox.showerror("Ошибка авторизации", str(e))
            return

        # Загрузка файла на Яндекс.Диск
        type_folder = ""
        for i in range(len(file_path) - 1, 0, -1):
            if file_path[i] != '.':
                type_folder = file_path[i] + type_folder
            else:
                break
        remote_path = f"/encrypted_files/{type_folder}"  # Папка на Яндекс.Диске
        upload_to_yadisk(ydisk, encrypted_file_path, remote_path)

    def download_and_decrypt(self):
        # Авторизация на Яндекс.Диске
        if OAuthCode == "":
            token = simpledialog.askstring("Авторизация", "Введите OAuth-токен Яндекс.Диска:", show="*")
        else:
            token = OAuthCode
        try:
            ydisk = authorize_yadisk(token)
        except Exception as e:
            messagebox.showerror("Ошибка авторизации", str(e))
            return

        # Выбор файла для скачивания
        remote_file_path = simpledialog.askstring("Выбор файла", "Введите путь к файлу на Яндекс.Диске (например, /encrypted_files/test.txt.encrypted): ")
        if not remote_file_path:
            return

        # Скачивание файла
        local_file_path = os.path.basename(remote_file_path)  # Сохраняем файл в текущую директорию
        download_from_yadisk(ydisk, remote_file_path, local_file_path)

        # Дешифрование файла
        key = load_key()  # Загружаем ключ
        decrypted_file_path = decrypt_file(local_file_path, key)
        messagebox.showinfo("Успешное дешифрование", f"Файл расшифрован и сохранен как {decrypted_file_path}")


if __name__ == "__main__":
    app = EnigmaApp()
    app.mainloop()
