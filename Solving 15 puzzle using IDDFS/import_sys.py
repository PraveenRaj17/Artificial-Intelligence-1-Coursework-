import sys

arr = sys.argv[1]
b = sys.argv[2]
c  = sys.argv[3]
array = []

for i in range(1, 4):
    array.append(sys.argv[i])

print("array", array)
print(array[2])