# # +, *
# # str()
# # len()
# # in
# # > <
# # ord()
# # chr()
# # input()
# # 0 1 2 3 4 5 6
# # -1 -2 -3 -4 -5
# #
# # [::]
# # []
# # s[1] = '111'
# #
# # s[1:] + 'a' + s[2:]
# #
# # upper()
# # lower()
# # count()
# # find()
# # rfind()
# # index()
# # replace()
# # isalpha()
# # isdigit()
# # int()
# # rjust()
# # ljust()
# # split()
# # join()
# # strip()
# # rstrip()
# # f''
# # format()
# # callable()
# # capitalize()
# # casefold()
# # center()
# # encode()
# # endswith()
# # expantabs()
# # isascii()
# # print('1')
#
# # my_str = '\t1'
# # print(my_str.expandtabs(100), my_str)
#
#
# # satr = 'Hello world! asd'.replace(' ', 'hello')
# #
# # print(satr)
#
#
# a = 'heLlO'
#
# # print(a.center(11, '*'))
# # print(a.swapcase())
# # print(text.find('name', 8, 13))
# # slovar = str.maketrans({'H': 'key', 'i': 'k'})
#
# # print(text.maketrans({'H': 'key', 'i': 'k'}))
# # print(chr(105))
# # print(text.encode('ascii', errors='ignore'))
# # soz = input('>>> ')
# # text = f'Hi my name is John! {soz} салом'
# # print(text)
# # print(text[:text.index('!') + 1] + ' ' + soz + text[text.index('!') + 1:])
# # print(text.strip())
#
# # print(text.ljust(100, 'q'))
# # lst = text.split()
# # print(lst)
# # text = 'salom'.join(lst)
# # print(text)
# # print('123'.join(text))
#
#
# # print('hello world!!!')
# # print(f'hello world!!!')
#
# # lotin = 'abcde'
# # kiril = 'абсдею'
# #
# # text = 'абдулла кодирий'
# #
# # yangi_lotin = ''
# # for harf in text:
# #     if harf in kiril:
# #         yangi_lotin += lotin[kiril.index(harf)]
# #     else:
# #         yangi_lotin += harf
# # print(yangi_lotin)
#
# text = 'adsjd asdkasdkjhdhksad kajsdhas asdkasdkjhdhksad sss asdkasdkjhdhksad sss'
#
# # print(len(max(text.split(), key=len)))
# # print(text.split())
#
# max_count = text.split()[0]
# for i in text.split():
#     if text.count(i) > text.count(max_count):
#         max_count = i
#
# print(max_count)


# n = 20
# for i in range(n):
#     for j in range(65, i + 65):
#         print(chr(j), end=' ')
#     print()

# n = 20
# tub_sonlar = ''
# for i in range(1, n + 1):
#     bol = True
#     for j in range(2, i):
#         if i % j != 0:
#             bol = False
#             continue
#     if bol:
#         tub_sonlar += f'{i}, '
# print(tub_sonlar)
