import binascii


def hexToUtf8(text):
    '''
    Преобразовывает текст из формата HEX в UTF-8
    :param text: строка с текстом, который необходимо преобразовать
    :return: преобразованная в UTF-8 строка
    '''
    text = binascii.unhexlify(text).decode('utf8')
    text = text.replace('\x00', '')
    return text


def utf8ToHex(text):
    '''
    Преобразовывает текст из формата UTF-8 в HEX
    :param text: строка с текстом, который необходимо преобразовать
    :return: преобразованная в HEX строка
    '''
    text = binascii.hexlify(text.encode('utf8')).decode('utf8')
    return text


def xor(num1, num2, base=2):
    '''
    Исключающее сложение
    :param num1: число №1
    :param num2: число №2
    :param base: система счисления
    :return: результат сложения
    '''
    len1 = len(str(num1))
    num1 = int(num1, base)
    num2 = int(num2, base)

    num = str(bin(num1 ^ num2)[2:])

    num = fillZerosBeforeNumber(num, len1)

    return num


def fillZerosBeforeNumber(num, length):
    '''
    Заполняет строку нулями (до числа)
    :param num: число
    :param length: длина итоговой строки
    :return: строка с нулями в начале и числом в конце
    '''
    num = str(num)
    if len(str(num)) != length:
        for i in range(length - len(str(num))):
            num = '0' + num
    return num


def fillZerosAfterNumber(num, length):
    """
    Заполняет строку нулями (после числа)
    :param num: число
    :param length: длина итоговой строки
    :return: строка с нулями в конце и числом в начале
    """
    num = str(num)
    if len(str(num)) != length:
        for i in range(length - len(str(num))):
            num = num + '0'
    return num


transformation_table = [
    [1, 7, 14, 13, 0, 5, 8, 3, 4, 15, 10, 6, 9, 12, 11, 2],
    [8, 14, 2, 5, 6, 9, 1, 12, 15, 4, 11, 0, 13, 10, 3, 7],
    [5, 13, 15, 6, 9, 2, 12, 10, 11, 7, 8, 1, 4, 3, 14, 0],
    [7, 15, 5, 10, 8, 1, 6, 13, 0, 9, 3, 14, 11, 4, 2, 12],
    [12, 8, 2, 1, 13, 4, 15, 6, 7, 0, 10, 5, 3, 14, 9, 11],
    [11, 3, 5, 8, 2, 15, 10, 13, 14, 1, 7, 4, 12, 9, 6, 0],
    [6, 8, 2, 3, 9, 10, 5, 12, 1, 14, 4, 7, 11, 13, 0, 15],
    [12, 4, 6, 2, 10, 5, 11, 9, 14, 8, 13, 7, 0, 3, 15, 1]
]


def tableTransformation(numIn):
    '''
    Преобразует 32-битное число путем разбития на 8 4-битных и замены по таблице transformaion_table
    :param numIn: 32-битное число
    :return: Преобразованное число
    '''
    numOut = ''
    for i in range(8):
        num1 = numIn[i * 4: i * 4 + 4]
        num2 = bin(transformation_table[i][int(numIn[i * 4: i * 4 + 4], 2)])[2:]
        num2 = fillZerosBeforeNumber(num2, 4)

        numOut += xor(num1, num2, 2)
    return numOut


def transformation(numLeft, numRight, key):
    '''
    Исполняет одну итерацию шифрования блока
    :param numLeft: левая половина блока
    :param numRight: правая половина блока
    :param key: ключ, соответствующий данной итерации
    :return: кортеж с двумя новыми половинами блока
    '''
    numLeftOut = numRight
    numRightOut = xor(numRight, key, 2)
    numRightOut = tableTransformation(numRightOut)
    numRightOut = xor(numRightOut, numLeft, 2)
    return numLeftOut, numRightOut


def chainOfTransformations(numLeft, numRight, key, move='straight'):
    '''
    Исполняет все итерации шифрования блока
    :param numLeft: левая половина блока
    :param numRight: правая половина блока
    :param key: массив ключей для каждой итерации
    :param move: направление кодирования (straight для кодирования, reverse для декодирования)
    :return: кортеж с двумя новыми половинами блока
    '''
    start = 0
    stop = 31
    step = 1
    last = 31
    if move == 'reverse':
        start = 31
        stop = 0
        step = -1
        last = 0
    for i in range(start, stop, step):
        numLeft, numRight = transformation(numLeft, numRight, key[i])
    numRightLast = numRight
    numLeft, numRight = transformation(numLeft, numRight, key[last])
    return numRight + numRightLast


def convertBase(num, toBase=10, fromBase=10):
    '''
    Преобразует число из одной системы счисления в другую
    :param num: число
    :param toBase: необходимая система счисления
    :param fromBase: изначальная система счисления
    :return: число в необходимой системе счисления
    '''
    if isinstance(num, str):
        n = int(num, fromBase)
    else:
        n = int(num)
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if n < toBase:
        return alphabet[n]
    else:
        return convertBase(n // toBase, toBase) + alphabet[n % toBase]


def transformKey(key):
    '''
    Переводит ключ из UTF-8 в HEX и в случае необходимости увеличивает его длину
    :param key: ключ
    :return: преобразованный ключ
    '''
    key = binascii.hexlify(key.encode('utf8')).decode('utf8')
    while len(key) < 64:
        key += key
    return key[:64]


def keyToKeys(key):
    '''
    Из 256-битного ключа создает массив 8-битных
    :param key: 256-битный ключ
    :return: массив 8-битных ключей
    '''
    key = convertBase(key, 2, 16)
    keys = []
    for i in range(3):
        for j in range(8):
            keys.append(key[j * 32: j * 32 + 32])
    for i in range(7, -1, -1):
        keys.append(key[i * 32: i * 32 + 32])
    return keys


def encode(text, key):
    '''
    Шифрует строку
    :param text: строку
    :param key: ключ
    :return: зашифрованная строка
    '''
    key = transformKey(key)
    key = keyToKeys(key)
    text = convertBase(utf8ToHex(text), toBase=2, fromBase=16)
    if len(text) % 8 != 0:
        text = fillZerosBeforeNumber(text, (len(text) // 8) * 8 + 8)
    textArray = []
    textEncrypt = ''
    if (len(text) // 64 * 64) != len(text):
        count = len(text) // 64 + 1
    else:
        count = len(text) // 64
    for i in range(count):
        textForAppend = text[i * 64: i * 64 + 64]
        textForAppend = fillZerosAfterNumber(textForAppend, 64)
        textArray.append(textForAppend)
    for i in range(len(textArray)):
        textEncrypt += chainOfTransformations(textArray[i][:32], textArray[i][32:], key)
    textEncrypt = convertBase(textEncrypt, toBase=16, fromBase=2)
    return textEncrypt


def decode(text, key):
    '''
    Дешифрует строку
    :param text: строка
    :param key: ключ
    :return: дешифрованная строка
    '''
    key = transformKey(key)
    key = keyToKeys(key)
    text = convertBase(text, toBase=2, fromBase=16)
    if len(text) % 8 != 0:
        text = fillZerosBeforeNumber(text, (len(text) // 8) * 8 + 8)
    textArray = []
    textDecrypt = ''
    if (len(text) // 64 * 64) != len(text):
        count = len(text) // 64 + 1
    else:
        count = len(text) // 64
    for i in range(count):
        textForAppend = text[i * 64: i * 64 + 64]
        textForAppend = fillZerosAfterNumber(textForAppend, 64)
        textArray.append(textForAppend)
    for i in range(len(textArray)):
        textDecrypt += chainOfTransformations(textArray[i][:32], textArray[i][32:], key, move='reverse')
    textDecrypt = convertBase(textDecrypt, toBase=16, fromBase=2)
    return textDecrypt
