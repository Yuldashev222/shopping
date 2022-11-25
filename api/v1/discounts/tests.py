# # n = 5
# # i = 1
# # # for i in range(1, n ** 2 + 1):
# # print(i, i + 2, i + 2 + 3, i + 2 + 3 + 4, i + 2 + 3 + 4 + 5)
# # print(i + 1, 0, 0, 0, i + 2 + 3 + 4 + 5 + n - 1)
# # print(i + 1 + 2, 0, 0, 0, i + 2 + 3 + 4 + 5 + n - 1 + n - 2)
# # print(i + 1 + 2 + 3, 0, 0, 0, i + 2 + 3 + 4 + 5 + n - 1 + n - 2 + n - 3)
# # print(i + 1 + 2 + 3 + 4, 0, 0, 0, i + 2 + 3 + 4 + 5 + n - 1 + n - 2 + n - 3 + n - 4)
# #
# # k = 1
# # print()
# # i = 0
# # j = 1
# # while j < 12:
# #     a = j
# #     for z in range(2, n + 2):
# #         print(f'{i + j:2}', end=' ')
# #         j += z
# #     print()
# #     j = a + k
# #     k += 1
#
#
# n = 11
# i = 1
# q = 1
# while i < n + 1:
#     j = 1
#     g = q
#     while j + i < n + 1:
#         if j == 1:
#             print(f'{q:3}', end=' ')
#         q += i + j
#         print(f'{q:3}', end=' ')
#         j += 1
#     else:
#         if i == n:
#             print(f'{q:3}', end=' ')
#         s = n
#         for k in range(i - 1):
#             q += s
#             print(f'{q:3}', end=' ')
#             s -= 1
#     print()
#     q = g + i
#     i += 1
