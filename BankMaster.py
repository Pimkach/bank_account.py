from datetime import datetime

BALANCE_FILE = 'balance.txt'
HISTORY_FILE = 'history.txt'

balance = 0
history = []
current_time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

try:
    with open(BALANCE_FILE, 'r') as f:
        balance = float(f.read())
except FileNotFoundError:
    print("Файл баланса не найден. Начальный баланс: 0")

try:
    with open(HISTORY_FILE, 'r', encoding="utf-8") as f:
        history = [eval(line.strip()) for line in f]
except FileNotFoundError:
    print("Файл истории не найден. Начинаем с пустой истории.")
except (IOError, SyntaxError) as e:
    print(f"Ошибка при чтении файла истории: {e}")

def check_balance():
    print(f"Текущий баланс: {balance}")

def up_money():
    global balance
    try:
        add_money = float(input('Какую сумму вы хотите внести? '))
        if add_money <= 0:
            raise ValueError("Сумма должна быть положительной")
        balance += add_money
        add_to_history("внесение", add_money)
        print(f"Внесено {add_money}. Новый баланс: {balance}")
    except ValueError as e:
        print(f'Ошибка: {e}')

def down_money():
    global balance
    try:
        down_money = float(input('Какую сумму вы хотите снять? '))
        if down_money <= 0:
            raise ValueError("Сумма должна быть положительной")
        if balance < down_money:
            raise ValueError("Недостаточно средств на счете")
        balance -= down_money
        add_to_history("снятие", down_money)
        print(f"Снято {down_money}. Новый баланс: {balance}")
    except ValueError as e:
        print(f"Ошибка: {e}")

def add_to_history(operation_type, amount):
    history.append({
        "тип": operation_type,
        "сумма": amount,
        "время": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

def save_balance():
    with open(BALANCE_FILE, 'w') as f:
        f.write(str(balance))

def save_history():
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            for h in history:
                print(h, file=file)
    except IOError:
        print("Ошибка при сохранении истории.")
def check_history():
    try:
        count = int(input('Сколько последних операций вы хотите посмотреть? '))
        if count <= 0:
            raise ValueError("Количество операций должно быть положительным")
        for operation in history[-count:]:
            print(f"{operation['время']} - {operation['тип']}: {operation['сумма']}")
    except ValueError as e:
        print(f"Ошибка: {e}")


def main():

    operations = {
        '1': check_balance,
        '2': up_money,
        '3': down_money,
        '4': check_history,
        '5': exit_program
    }

    while True:
        print("\nБанковский счет")
        print("1. Проверить баланс")
        print("2. Внести деньги")
        print("3. Снять деньги")
        print("4. Посмотреть историю")
        print("5. Выйти")

        choice = input("Выберите действие (1-5):\n")
        if choice in operations:
            operations[choice]()
        else:
            print("Неверный выбор. Попробуйте снова.")


def exit_program():
    save_balance()
    save_history()
    print("Спасибо за использование нашего банка. До свидания!")
    exit()


if __name__ == "__main__":
    main()

