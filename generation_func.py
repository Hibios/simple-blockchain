import random
random.seed(0)


def make_transaction(max_value=3):
    #  Функция создаёт валидные транзакции в диапозоне от 1 до maxValue
    sign = int(random.getrandbits(1))*2 - 1   # Случайный выбор 1 или -1
    amount = random.randint(1, max_value)  # Сумма перевода
    alicePays = sign * amount  # Снятие или депозит Алисы
    bobPays = -1 * alicePays  # Снятие или депозит Боба
    return {'Alice': alicePays, 'Bob': bobPays}


def update_state(txn, state):
    # Входные данные:
    # txn, state: словари с именами учетных записей,
    # содержащие числовые значения для суммы перевода (txn) или баланса счета (state).
    # Возвращаемое значение: Обновленное состояние с добавлением дополнительных пользователей

    # Если транзакция действительна, обновляем состояние
    state = state.copy()  # Поскольку словари изменчивы, создаём рабочую копию данных.
    for key in txn:
        if key in state.keys():
            state[key] += txn[key]
        else:
            state[key] = txn[key]
    return state


def is_valid_txn(txn, state):
    # Предположим, что транзакция представляет собой словарь с именами учетных записей

    # Убедимся, что сумма пополнений и снятий равна 0
    if sum(txn.values()) is not 0:
        return False

    # Убедимся, что транзакция не вызывает овердрафта
    for key in txn.keys():
        if key in state.keys():
            acctBalance = state[key]
        else:
            acctBalance = 0
        if (acctBalance + txn[key]) < 0:
            return False

    return True


# Набор случайных транзакций
txnBuffer = [make_transaction(5) for i in range(30)]
for txn in txnBuffer:
    print(txn)

state = {'Alice': 5, 'Bob': 5}
print(is_valid_txn({'Alice': -3, 'Bob': 3}, state))  # Базовая транзакция - это прекрасно работает!
print(is_valid_txn({'Alice': -4, 'Bob': 3}, state))  # Но мы не можем создавать или уничтожать токены!
print(is_valid_txn({'Alice': -6, 'Bob': 6}, state))  # Мы также не можем перерасходовать наш счет.
print(is_valid_txn({'Alice': -4, 'Bob': 2, 'Lisa': 2}, state))  # Создание новых пользователей действительно
print(is_valid_txn({'Alice': -4, 'Bob': 3, 'Lisa': 2}, state))  # Но те же правила все еще применяются!
