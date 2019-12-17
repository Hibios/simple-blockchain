import sys
import json
import random
from hash_function import hash_func
random.seed(0)


def make_transaction(max_value=3):
    """ Функция создаёт валидные транзакции в диапозоне от 1 до maxValue """
    sign = int(random.getrandbits(1))*2 - 1   # Случайный выбор 1 или -1
    amount = random.randint(1, max_value)  # Сумма перевода
    alicePays = sign * amount  # Снятие или депозит Алисы
    bobPays = -1 * alicePays  # Снятие или депозит Боба
    return {'Alice': alicePays, 'Bob': bobPays}


def makeBlock(txns, chain):
    """ Функция создаёт новые блоки """
    parentBlock = chain[-1]  # Определяем родительский блок
    parentHash = parentBlock[u'hash']  # Берём его хеш
    blockNumber = parentBlock[u'contents'][u'blockNumber'] + 1  # Определяем номер нового блока на основе старого
    txnCount = len(txns)  # Считаем количество поданных на вход функции транзакций
    blockContents = {u'blockNumber': blockNumber, u'parentHash': parentHash,
                     u'txnCount': len(txns), 'txns': txns}  # Наполняем макет блока данными
    blockHash = hash_func(blockContents, 'sha256')  # Хешируем макет
    print("Хеш:", blockHash)
    block = {u'hash': blockHash, u'contents': blockContents}  # Создаём новый блок с его хешем и контентом

    return block


def update_state(txn, state):
    """
    # Входные данные:
    # txn, state: словари с именами учетных записей,
    # содержащие числовые значения для суммы перевода (txn) или баланса счета (state).
    # Возвращаемое значение: Обновленное состояние с добавлением дополнительных пользователей
    """

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

state = {'Alice': 5, 'Bob': 5}

# Набор случайных транзакций
txnBuffer = [make_transaction(5) for i in range(30)]
for txn in txnBuffer:
    print(is_valid_txn(txn, state))

print('================TRANSACTIONS TEST=================')
state = {'Alice': 5, 'Bob': 5}
print("State:", state)
print(is_valid_txn({'Alice': -3, 'Bob': 3}, state))  # Базовая транзакция - это прекрасно работает!
print(is_valid_txn({'Alice': -4, 'Bob': 3}, state))  # Но мы не можем создавать или уничтожать токены(Боб должен был получить 4 токена!)!
print(is_valid_txn({'Alice': -6, 'Bob': 6}, state))  # Мы также не можем перерасходовать наш счет.
print(is_valid_txn({'Alice': -4, 'Bob': 2, 'Lisa': 2}, state))  # Создание новых пользователей действительно
print(is_valid_txn({'Alice': -4, 'Bob': 3, 'Lisa': 2}, state))  # Но те же правила все еще применяются!
print('==================================================\n')
print('================CHAIN TEST=================')
"""
Данная часть кода является жизненным циклом блокчейна, она начнётся здесь как жизнь и будет продолжаться до самой остановки платформы
"""
state = {u'Alice': 50, u'Bob': 50}  # Начальное состояние системы, деньги на счету в самом начале
genesisBlockTxns = [state]  # Первый блок представляет собой список, с первым состоянием системы
# Содержание первого блока(наполняем блок):
# -номер
# -хеш родителя
# -число транзакций
# -транзакции
genesisBlockContents = {u'blockNumber': 0, u'parentHash': None, u'txnCount': 1, u'txns': genesisBlockTxns}
# Далее определяем хеш первого блока
genesisHash = hash_func(genesisBlockContents, 'sha256')
# Создаём блок в виде словаря
# Составляющие:
# -хеш содержания первого блока
# -содержание первого блока
genesisBlock = {u'hash': genesisHash, u'contents': genesisBlockContents}

genesisBlockStr = json.dumps(genesisBlock, sort_keys=True)


# Да да, это первая переменная которая и будет позднее весить десятки гигабайтов.
# Здесь будут хранится все блоки начиная с первого(Позднее вынести в бд)
chain = [genesisBlock]


blockSizeLimit = 5  # Произвольное количество транзакций в блоке выбирается майнером блоков и может варьироваться между блоками!

# tnxBuffer - переменная в которой будут накапливаться транзакции

print("TXN_BUFF:", txnBuffer)
print(state)
while len(txnBuffer) > 0:    # Цикл начинается если добавилось достаточно транзакций(В нашем случае больше 0)
    bufferStartSize = len(txnBuffer)

    # Соберите набор допустимых транзакций для включения
    txnList = []
    while (len(txnBuffer) > 0) & (len(txnList) < blockSizeLimit):
        # Наполняем блок до тех пор пока не будет достигнут лимит или транзакции кончаться

        # Следующие строки делают так: первая достаёт по одной транзакции из буфера, а вторая проверяет на правильность
        newTxn = txnBuffer.pop()
        print("Текущая транзакция:", newTxn)
        validTxn = is_valid_txn(newTxn, state)  # Возвращает False если транзакция не верна

        if validTxn:  # Выполняем если транзакция верная
            txnList.append(newTxn)  # Добавляем в список
            state = update_state(newTxn, state)  # Обновляем состояние блокчейна, то есть все кошельки и т.д. после операции
        else:
            # Иначе просто игнорируем транзакцию
            print("Транзакция игнорирована")
            sys.stdout.flush()
            continue  # Переходим к следующей транзакции, так как эта брак

    # Создаём блок и добавляем его в цепь
    myBlock = makeBlock(txnList, chain)
    chain.append(myBlock)

for index, block in enumerate(chain):
    print("\nБлок номер {}".format(index))
    print(block)
