import black
import isort


def encrypt_caesar(plaintext: str, shift: int) -> str:
    upEng = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowEng = "abcdefghijklmnopqrstuvwxyz"
    upRus = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    lowRus = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    ciphertext = ""
    for i in range(0, len(plaintext)):
        if plaintext[i] in lowEng:
            ciphertext += lowEng[(lowEng.find(plaintext[i]) + shift) % 26]
        else:
            if plaintext[i] in upEng:
                ciphertext += upEng[(upEng.find(plaintext[i]) + shift) % 26]
            else:
                if plaintext[i] in lowRus:
                    ciphertext += lowRus[(lowRus.find(plaintext[i]) + shift) % 33]
                else:
                    if plaintext[i] in upRus:
                        ciphertext += upRus[(upRus.find(plaintext[i]) + shift) % 33]
                    else:
                        ciphertext += plaintext[i]
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int) -> str:
    plaintext = encrypt_caesar(ciphertext, -shift)
    return plaintext
