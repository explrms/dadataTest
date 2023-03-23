import sqlite3
from dadata import Dadata

cursor = sqlite3.connect('db.sqlite3').cursor()
cursor.execute('SELECT api_key FROM user_settings')
TOKEN = cursor.fetchone()[0]
cursor.close()


def search_address():
    """
    The function searches for the complete address when prompted by the user.
    If more than one address is available, it asks the user for the specific address.
    """
    dadata = Dadata(TOKEN)

    while True:
        # Ask the user for a query string
        user_query = input('Введите адрес для поиска(для выхода напишите /q): ')
        # Exit the program if the exit command "/q" is sent
        if user_query == '/q':
            print('\nРабота программы завершена')
            break

        # Getting data from the API
        results = dadata.suggest(name='address', query=user_query)

        match len(results):
            case 0:
                # Message when there are no prompts on request
                print('По вашему запросу ничего не найдено')
                continue
            case 1:
                # If there is only one prompt, the coordinates are immediately displayed
                current_result = results[0]
            case _:
                # If there are several prompts, specify the serial number of the address from the results of the query
                print('Результаты поиска:\n------------------')
                for i, result in enumerate(results):
                    print(f'{i + 1}: {result["unrestricted_value"]}')
                # Protecting the script from crashing during the user data entry phase
                while True:
                    try:
                        number = int(input('------------------\n'
                                           f'Выберите порядковый номер адреса (1 - {len(results)}): '))
                        current_result = results[number - 1]
                        break
                    except (ValueError, IndexError):
                        print(f'Внимание! Вы должны ввести целое число от 1 до {len(results)}')
        print(f'Координаты: Широта: {current_result["data"]["geo_lat"]}, Долгота: {current_result["data"]["geo_lon"]}')


if __name__ == '__main__':
    try:
        search_address()
    except KeyboardInterrupt:
        print('\nРабота программы завершена')
