��� ������ ������ � Enigma ���������� ������� ��������� ������� �����:

1. ������� �� ������: https://oauth.yandex.ru/client/new/
2. ������� ����������:
    2.1. �������� ������� (������������)
    2.2. ���-������� (redirect url: 'https://localhost'
    2.3. ������ � ������:
        * ������ � ����� ����� �� �����
    2.4 ��������� Client_ID � Secret_Id
3. ������� �� ������: https://oauth.yandex.ru/authorize?response_type=code&client_id=<Client_ID> -- �������� Client_ID
4. � url �������� 'code=CODE&...', ���������� ����������� CODE � �������� � ��������� get_token.py
5. ���������� OAuth �������� � ���������� OAuthCode � main.py

�� ������!