def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    upEng = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowEng="abcdefghijklmnopqrstuvwxyz"
    upRus="АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    lowRus = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    ciphertext = ""
    for i in range (0, len(plaintext)):
        if plaintext[i] in lowEng:
            ciphertext+=lowEng[(lowEng.find(plaintext[i])+shift)%26]
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

def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    upEng = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowEng = "abcdefghijklmnopqrstuvwxyz"
    upRus = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    lowRus = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    plaintext = ""
    for i in range (0, len(ciphertext)):
        if ciphertext[i] in lowEng:
            if lowEng.find(ciphertext[i])-shift<0:
                ind=26+lowEng.find(ciphertext[i])-shift
            else:
                ind=lowEng.find(ciphertext[i])-shift
            plaintext+=lowEng[ind]
        else:
            if ciphertext[i] in upEng:
                if upEng.find(ciphertext[i]) - shift < 0:
                    ind = 26 + upEng.find(ciphertext[i]) - shift
                else:
                    ind = upEng.find(ciphertext[i]) - shift
                plaintext += upEng[ind]
            else:
                if ciphertext[i] in lowRus:
                    if lowRus.find(ciphertext[i]) - shift < 0:
                        ind = 33 + lowRus.find(ciphertext[i]) - shift
                    else:
                        ind = lowRus.find(ciphertext[i]) - shift
                    plaintext += lowRus[ind]
                else:
                    if ciphertext[i] in upRus:
                        if upRus.find(ciphertext[i]) - shift < 0:
                            ind = 33 + upRus.find(ciphertext[i]) - shift
                        else:
                            ind = upRus.find(ciphertext[i]) - shift
                        plaintext += upRus[ind]
                    else:
                        plaintext += ciphertext[i]
    return plaintext