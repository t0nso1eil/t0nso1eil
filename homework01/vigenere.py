def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    upEng = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowEng = "abcdefghijklmnopqrstuvwxyz"
    upRus = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    lowRus = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    ciphertext = ""
    shift=[0]*len(plaintext)
    for i in range(0, len(plaintext)):
        if keyword[i%len(keyword)] in upEng:
            shift[i]=upEng.find(keyword[i%len(keyword)])
        else:
            if keyword[i%len(keyword)] in lowEng:
                shift[i] = lowEng.find(keyword[i%len(keyword)])
            else:
                if keyword[i%len(keyword)] in upRus:
                    shift[i] = upRus.find(keyword[i%len(keyword)])
                else:
                    if keyword[i%len(keyword)] in lowRus:
                        shift[i] = lowRus.find(keyword[i%len(keyword)])
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
    upEng = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowEng = "abcdefghijklmnopqrstuvwxyz"
    upRus = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    lowRus = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    plaintext = ""
    shift = [0] * len(ciphertext)
    for i in range(0, len(ciphertext)):
        if keyword[i%len(keyword)] in upEng:
            shift[i] = upEng.find(keyword[i%len(keyword)])
        else:
            if keyword[i%len(keyword)] in lowEng:
                shift[i] = lowEng.find(keyword[i%len(keyword)])
            else:
                if keyword[i%len(keyword)] in upRus:
                    shift[i] = upRus.find(keyword[i%len(keyword)])
                else:
                    if keyword[i%len(keyword)] in lowRus:
                        shift[i] = lowRus.find(keyword[i%len(keyword)])
    for i in range(0, len(ciphertext)):
        if ciphertext[i] in lowEng:
            if lowEng.find(ciphertext[i])-shift[i]<0:
                ind=26+lowEng.find(ciphertext[i])-shift[i]
            else:
                ind=lowEng.find(ciphertext[i])-shift[i]
            plaintext += lowEng[ind]
        else:
            if ciphertext[i] in upEng:
                if upEng.find(ciphertext[i]) - shift[i] < 0:
                    ind = 26 + upEng.find(ciphertext[i]) - shift[i]
                else:
                    ind = upEng.find(ciphertext[i]) - shift[i]
                plaintext += upEng[ind]
            else:
                if ciphertext[i] in lowRus:
                    if lowRus.find(ciphertext[i]) - shift[i] < 0:
                        ind = 33 + lowRus.find(ciphertext[i]) - shift[i]
                    else:
                        ind = lowRus.find(ciphertext[i]) - shift[i]
                    plaintext += lowRus[ind]
                else:
                    if ciphertext[i] in upRus:
                        if upRus.find(ciphertext[i]) - shift[i] < 0:
                            ind = 33 + upRus.find(ciphertext[i]) - shift[i]
                        else:
                            ind = upRus.find(ciphertext[i]) - shift[i]
                        plaintext += upRus[ind]
                    else:
                        plaintext += ciphertext[i]
    return plaintext
