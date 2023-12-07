#!/usr/bin/env python
# coding: utf-8

# # 画像を読み込み、RGBの値を10進数で出力
# 
# ### 画像はpng形式のみ
# ### jpeg等の非可逆圧縮の場合、LSBが保持されることは可能性として限りなく少ないため。

import matplotlib.pyplot as plt #画像を表示するためのモジュール
import cv2  #OpenCVをインポート
import numpy as np #numpyをインポート
from PIL import Image, ImageFilter
 
img_ = Image.open("bridge.png")
img_ = img_.convert('RGB')
img_array = np.asarray(img_) #numpyで扱える配列をつくる

print(img_array.shape)

plt.imshow(img_array)
plt.show()


# # 入力したいパスワードを2進数に変換

pass_string = input("パスワードを入力してください  >>  ")
#ordで文字のunicodeを返す。　そのunicodeを8bitの2進数に戻す。

binary_representation = ''.join(format(ord(char), '08b') for char in pass_string)
#0000000000000000は終了コード
binary_representation = binary_representation+"0000000000000000"
print(binary_representation)


# # パスワードを画像の中に入れる関数を書く。
# ## 見た目の劣化を防ぐため、RGBすべての値を書き換える。

#pic_RGB_numはRGBの値
#pass_numはパスワードを2進数にした1つの値
def password_in_picture(pic_RGB_num , pass_num):
    binary_pic_RGB_num = format(pic_RGB_num , '08b')
    # LSBが1で、pass_numが0の場合、LSBを0に変更
    if(int(binary_pic_RGB_num[7]) == 1 and int(pass_num) == 0):
        return pic_RGB_num -1
    # LSBが0で、pass_numが1の場合、LSBを1に変更
    elif(int(binary_pic_RGB_num[7]) == 0 and int(pass_num) == 1):
        return pic_RGB_num +1
    # LSBとpass_numが同じの場合、変更せずreturn
    return pic_RGB_num

pass_idx = 0
# 画像の中のRGBすべてをなめる
for row_ in range(img_array.shape[0]):
    for col_ in range(img_array.shape[1]):
        for color_idx in range(3):
            if(pass_idx < len(binary_representation)):
                img_array[row_,col_ ,color_idx]=password_in_picture(img_array[row_ , col_ , color_idx] , binary_representation[pass_idx])
                pass_idx+=1


# # 実際にパスワードを注入した画像が以下


plt.imshow(img_array)
plt.show()
# numpyからPIL.Image.Imageに変更
img_ = Image.fromarray(img_array)
img_.save("bridge_result.png")


# # 画像から文字列を取得する
#画像から、文字列を取得する。

img_ = Image.open("bridge_result.png")

pass_img = np.asarray(img_)

print(pass_img.shape)

plt.imshow(pass_img)
plt.show()


# # 各ピクセルのRGBデータのLSBだけを取り出す。

def get_password_from_picture(num_in_pic):
    binary_in_pass = format(num_in_pic , '08b')
    return binary_in_pass[7]


# # 0が16回来ると、終了コードなので、ifで判断する。


pass_str = [] # 画像内に入っている2進数を入れるリスト
null_flag = 0# 0の個数を数えるための変数
num =0  # 何週回ったのか、カウントのための変数

for row_ in range(pass_img.shape[0]):
    if null_flag == 16:
        break
    for col_ in range(pass_img.shape[1]):
        if null_flag == 16:
            break
        for color_idx in range(3):
            lsb_ = get_password_from_picture(pass_img[row_, col_, color_idx])
            pass_str.append(lsb_)
            num+=1
            if int(lsb_) == 0:
                null_flag += 1
            else:
                null_flag = 0
            
            if null_flag == 16:
                break


# # 取り出したバイナリデータを、8個ずつに分けて文字にする。
unicode_string = ''.join(chr(int(password_idx, 2)) for password_idx in [''.join(pass_str[i:i+8]) for i in range(0, len(pass_str), 8)])


# # 入力したパスワードを整形して、出力する
print(unicode_string)

