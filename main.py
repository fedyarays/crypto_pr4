from PIL import Image
import numpy as np
import math
import warnings
warnings.filterwarnings('ignore')

vibor = int(input('1 -- Встраивание, 2 -- Извлечение. Ваш выбор: '))


def check_size(img):
    if img.width % 2 != 0:
        print('yu')
        img = img.crop((0, 0, img.width - 1, img.height))
        img = img.convert("L")
        return img
    else:
        img = img.convert("L")
        return img


def l_u(d):
    if 0 <= abs(d) <= 7:
        l, u = 0, 7
    elif 8 <= abs(d) <= 15:
        l, u = 8, 15
    elif 16 <= abs(d) <= 31:
        l, u = 16, 31
    elif 32 <= abs(d) <= 63:
        l, u = 32, 63
    elif 64 <= abs(d) <= 127:
        l, u = 64, 127
    else:
        l, u = 128, 255
    return l, u


def string_to_bits(str_to_conv):
    bin_result = ''.join(format(x, '08b') for x in bytearray(str_to_conv, 'utf-8'))
    return bin_result


if vibor == 1:  # встраивание
    try:
        imag = input('Напишите название контейнера(например: image.png): ')
        original = Image.open(imag)
        opentxt = input('Введите сообщение: ')

        width, height = original.width, original.height
        original = check_size(original)

        pix = np.asarray(original)
        pixels = np.copy(pix)

        bits = string_to_bits(opentxt)
        q = 0

        for i in range(height):  # подсчитываем сколько битов может встроить в себя изображение
            for j in range(0, width, 2):
                d = pixels[i][j] - pixels[i][j + 1]
                l, u = l_u(d)
                n = int(math.log(u - l + 1, 2))
                q += n

        bits = bits.zfill(q)

        for i in range(height):  # начинаем встраивать проходя по парам битов изображения
            for j in range(0, width, 2):
                d = pixels[i][j] - pixels[i][j + 1]
                l, u = l_u(d)
                n = int(math.log(u - l + 1, 2))
                try:
                    m = int(bits[:n], 2)
                    if d >= 0:
                        d_z = l + m
                    else:
                        d_z = -(l + m)

                    if d % 2 != 0:
                        pixels[i][j] += math.ceil((d_z - d) / 2)
                        pixels[i][j + 1] -= math.floor((d_z - d) / 2)
                    else:
                        pixels[i][j] += math.floor((d_z - d) / 2)
                        pixels[i][j + 1] -= math.ceil((d_z - d) / 2)
                    bits = bits[n:]
                except:
                    print('что-то пошло не так...')
                    break

        original_vstroeno = Image.fromarray(pixels)
        original_vstroeno.save('stego.png')
        print("Встраивание прошло успешно, ваше стегоизображение -- stego.png")
        print("Вы встроили сообщение: ", opentxt)
    except FileNotFoundError:
        print('Изображение не найдено!')

elif vibor == 2:
    imag = 'stego.png'  # input('Напишите название контейнера(например: image.png): ')
    original = Image.open(imag)

    width, height = original.width, original.height
    original = check_size(original)

    pix = np.asarray(original)
    pixels = np.copy(pix)

    nums, ns = [], []

    for x in range(height):
        for y in range(0, width, 2):
            d = pixels[x][y] - pixels[x][y + 1]
            l, u = l_u(d)
            n = int(math.log(u - l + 1, 2))
            ns.append(n)
            m = abs(d) - l
            nums.append(m)
    #print(nums, ns)
    txt_bin = ''
    for i in range(len(nums)):
        res = bin(nums[i])[2:].zfill(ns[i])
        txt_bin += str(res)

    while len(txt_bin) % 8 != 0:
        txt_bin = txt_bin[1:]

    txt = ''
    for i in range(0, len(txt_bin), 8):
        txt += chr(int(txt_bin[i: i + 8], 2))

    print(txt)

else:
    print('Введен недопустимый символ, запустите программу еще раз!')
