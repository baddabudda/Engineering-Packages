import numpy as np
import matplotlib.pyplot as plt

# a = np.arange(10)
# b = np.linspace(0, 10, 9)
# print(b)

# x, y = np.mgrid[0:5, 0:5]
# print(x, y, sep="\n")

# random = np.random.rand(3, 3)
# print(random, '\n')
# d = np.diag(np.diag(random))
# print(d)

# считываение с файла - np.genfromtxt

# маски - ?
# b = np.array([n for n in range(5)])
# print(b)
# row_mask = np.array([True, False, True, False, False])
# print(b[row_mask])

# использование функции для поиска индексов
# indices = np.where(row_mask)
# row_idxs = [1, 4]
# print(b[indices])
# print(b.take(row_idxs))

# из вектора сделать матрицу
# k = np.arange(24)
# l = k.reshape(4, 6)

# booklist = np.genfromtxt("books_for_lib.txt", dtype=str, delimiter=',', encoding="utf-8")
# size = booklist.size
# foreignAuthors = booklist[(size//2):size]
# print(foreignAuthors)
#
# newEnding = size - size // 4 # 15
# print(foreignAuthors[0:newEnding])
# requiredScope = foreignAuthors[0:(size - sectionSize)]
# print(requiredScope)

# print(requiredScope[2:(requiredScope.size):3])
data = np.genfromtxt("stockholm_tmp.dat", dtype=int)
# сохранение  - np.savetxt
# print(data)
mean = np.mean(data[:, 3])
stdev = np.std(data[:, 3])
disp = np.var(data[:, 3])
min = data[:, 3].min()
max = data[:, 3].max()
# y/m/d/mean/min/max/location
uniqueElem = np.unique(data[:, 1])
# сред.температура по месяцам + как менялась температура в апреле с 1800 - н.в.
meanMonths = np.zeros(12)
for i in range(1, 13):
    maskMonth = data[:, 1] == i
    month = data[maskMonth]
    meanMonths[i-1] = np.mean(month[:, 3])

print(meanMonths)

# plt.title("Mean monthy temperatures: 1800-2011")
plt.bar([1,2,3,4,5,6,7,8,9,10,11,12], meanMonths)
plt.show()

