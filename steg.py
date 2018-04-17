#!/usr/bin/env python3

# Image Steganography

import numpy as np
from PIL import Image
from os import path
import time

def encode(password, text, image_path):
    image = Image.open(image_path)
    img = np.array(image)
    code_text = (chr(1114111)) + password + text + (chr(1114111))
    code_text_hex = ''
    for character in code_text:
        asc = ord(character)
        if asc < 16:
            code_text_hex += ('0' + hex(asc)[2:])
        else:
            code_text_hex += (hex(asc))[2:]
    len_hex = len(code_text_hex)
    i = 0
    for pix_i in range(len(img)):
        for pix_j in range(len(img[pix_i])):
            r, g, b = img[pix_i][pix_j][0], img[pix_i][pix_j][1], img[pix_i][pix_j][2]
            if i < len_hex:
                r = int(hex(r)[:-1] + code_text_hex[i], 16)
                img[pix_i][pix_j][0] = r
                i += 1
            else:
                break
            if i < len_hex:
                g = int(hex(g)[:-1] + code_text_hex[i], 16)
                img[pix_i][pix_j][1] = g
                i += 1
            else:
                break
            if i < len_hex:
                b = int(hex(b)[:-1] + code_text_hex[i], 16)
                img[pix_i][pix_j][2] = b
                i += 1
            else:
                break
    if i == len_hex:
        img = Image.fromarray(img)
        img.save(image_path)
        return (True,)
    else:
        error_msg = 'Text too large for the given image.'
        return (False, error_msg)

def decode(password, image_path):
    image = Image.open(image_path)
    img = np.array(image)
    code_text_hex = ''
    flag_pass = True
    eof, flag_eof = '', False
    sof, flag_sof = '', False
    for r, g, b in img[0][:2]:
        sof += (hex(r)[-1] + hex(g)[-1] + hex(b)[-1])
    if int(sof, 16) == 1114111:
        flag_sof = True
    if flag_sof == True:
        i = 0
        pass_hex = ''
        for character in password:
            pass_hex += (hex(ord(character)))[2:]
        len_pass = len(pass_hex)
        for pix_row in img:
            for r, g, b in pix_row:
                code_text_hex += (hex(r)[-1] + hex(g)[-1] + hex(b)[-1])
                if i == 0 and len(code_text_hex) >= (6 + len_pass):
                    if code_text_hex[6:6+len_pass] != pass_hex:
                        flag_pass = False
                    i += 1
                if code_text_hex.count(hex(1114111)[2:]) == 2:
                    flag_eof = True
                    break
            if flag_eof == True:
                break
        if flag_eof == True and flag_pass == True:
            text = ''
            text_hex = code_text_hex[6+len_pass:-6]
            len_text_hex = len(text_hex)
            i = 0
            while i+1 < len_text_hex:
                text += chr(int(text_hex[i:i+2], 16))
                i += 2
            return (True, text)
        elif flag_eof == False and flag_pass == True:
            error_msg = 'Cannot extract text. End not reached.'
            return (False, error_msg)
        else:
            error_msg = 'Wrong Password.'
            return (False, error_msg)
    else:
        error_msg = 'Image contains no hidden data.'
        return (False, error_msg)


if __name__ == '__main__':
    print('Enter 1 to hide text into an image.')
    print('Enter 2 to extract text from an image.')
    n = int(input())

    if n == 1:
        print('Enter the text to be hidden:')
        s = input()
        p = input('Enter password: ')
        img = input('Enter the full path of the image file: ')
        if not path.exists(img):
            print('Invalid path.')
            exit()
        else:
            t1 = time.time()
            check = encode(p, s, img)
            t2 = time.time()
            if check[0] == True:
                print('Text successfully hidden in '+str(t2-t1)+' seconds.')
                print('Use same password to extract the text.')
            else:
                print('ERROR: ' + check[1])
    elif n == 2:
        img = input('Enter the full path of the image file: ')
        if not path.exists(img):
            print('Invalid path.')
            exit()
        else:
            p = input('Enter password: ')
            t1 = time.time()
            check = decode(p, img)
            t2 = time.time()
            if check[0] == True:
                print('Text successfully extracted in '+str(t2-t1)+' seconds.')
                print('Extracted text:')
                print(check[1])
            else:
                print('ERROR: ' + check[1])
    else:
        print('Wrong Choice.')
