# def f(numbers):
#
#     # recursiya qachon toxtashini elon qilib qoyayapman
#     if len(numbers) == 1:
#         return [numbers]
#     result = []
#
#     for i in range(len(numbers)):
#         m = numbers[i]
#         new_numbers = numbers[:i] + numbers[i + 1:]
#
#         for j in f(new_numbers):
#             result.append(m + j)
#     return result
#
#
# data = '123'
# print(f(data))


letter = "54".isalpha()
print(letter.real)