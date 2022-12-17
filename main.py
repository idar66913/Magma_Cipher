import functions

key = 'lol'
text = input('Введите строку для шифрования:\n')
print('Строка в формате HEX: ', functions.utf8ToHex(text).upper())

textEncrypt = functions.encode(text, key)
print('Зашифрованный текст:  ', textEncrypt)

textDecrypt = functions.decode(textEncrypt, key)
print('Расшифрованный текст: ', textDecrypt)
print('Расшифрованный текст в формате UTF-8: ', functions.hexToUtf8(textDecrypt))
