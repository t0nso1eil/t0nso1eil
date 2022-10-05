import black
import isort


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    upEng = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowEng = "abcdefghijklmnopqrstuvwxyz"
    upRus = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    lowRus = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    ciphertext = ""
    shift = [0] * len(plaintext)
    for i in range(0, len(plaintext)):
        if keyword[i % len(keyword)] in upEng:
            shift[i] = upEng.find(keyword[i % len(keyword)])
        else:
            if keyword[i % len(keyword)] in lowEng:
                shift[i] = lowEng.find(keyword[i % len(keyword)])
            else:
                if keyword[i % len(keyword)] in upRus:
                    shift[i] = upRus.find(keyword[i % len(keyword)])
                else:
                    if keyword[i % len(keyword)] in lowRus:
                        shift[i] = lowRus.find(keyword[i % len(keyword)])
    for i in range(0, len(plaintext)):
        if plaintext[i] in lowEng:
            ciphertext += lowEng[(lowEng.find(plaintext[i]) + shift[i]) % 26]
        else:
            if plaintext[i] in upEng:
                ciphertext += upEng[(upEng.find(plaintext[i]) + shift[i]) % 26]
            else:
                if plaintext[i] in lowRus:
                    ciphertext += lowRus[(lowRus.find(plaintext[i]) + shift[i]) % 33]
                else:
                    if plaintext[i] in upRus:
                        ciphertext += upRus[(upRus.find(plaintext[i]) + shift[i]) % 33]
                    else:
                        ciphertext += plaintext[i]
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    upEng = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowEng = "abcdefghijklmnopqrstuvwxyz"
    upRus = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    lowRus = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    shift = ""
    for i in range(0, len(ciphertext)):
        if keyword[i % len(keyword)] in upEng:
            shift += upEng[26 - upEng.find(keyword[i % len(keyword)])]
        else:
            if keyword[i % len(keyword)] in lowEng:
                shift += lowEng[26 - lowEng.find(keyword[i % len(keyword)])]
            else:
                if keyword[i % len(keyword)] in upRus:
                    shift += upRus[33 - upRus.find(keyword[i % len(keyword)])]
                else:
                    if keyword[i % len(keyword)] in lowRus:
                        shift += lowRus[33 - lowRus.find(keyword[i % len(keyword)])]
    plaintext = encrypt_vigenere(ciphertext, shift)
    return plaintext
