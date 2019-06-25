a = [1,2,3]

def func():
    global a
    a = []

print(a)
a.append(4)
print(a)
func()
print(a)
print("done")