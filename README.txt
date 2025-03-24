Для начала работы с Enigma необходимо сделать несколько простых шагов:

1. Перейти по ссылке: https://oauth.yandex.ru/client/new/
2. Создать приложение:
    2.1. Название сервиса (произвольное)
    2.2. Веб-сервисы (redirect url: 'https://localhost')
    2.3. Доступ к данным:
        * Запись в любом месте на диске
    2.4 Запомнить Client_ID и Secret_Id
3. Перейти по ссылке: https://oauth.yandex.ru/authorize?response_type=code&client_id=<Client_ID> -- вставить Client_ID
4. В url появится 'code={CODE}&...', необходимо скопировать CODE и вставить в программу get_token.py
5. Полученный OAuth вставить в переменную OAuthCode в main.py

Всё готово!
