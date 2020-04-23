class Items:
    def __init__(self, items):
        self.items = items

    def __getitem__(self, index):
        print('call __getitem__')
        return self.items[index]

    def __iter__(self):
        print('call __iter__')
        return iter(self.items)


def my_for(iterable):
    if getattr(iterable, '__iter__', None):
        print('Есть __iter__')
        iterator = iter(iterable)
        while True:
            try:
                print(next(iterator))
            except StopIteration:
                break
    elif getattr(iterable, '__getitem__', None):
        print('No __ite__ but in use __getitem__')
        index = 0
        while True:
            try:
                print(iterable[index])
                index += 1
            except IndexError:
                break

class Items:
    def __init__(self, items):
        self.items = items

    def __getitem__(self, index):
        print("call __getitem__")
        return self.items[index]

iterable_2 = Items([1, 2, 3, 4, 5, 6])
my_for(iterable_2)


iterable_1 = Items([1, 2, 3, 4, 5])

for i in iterable_1:
    print('>>', i)
print(list(map(str, iterable_1)))

l1 = [1, 2, 3, 4]

my_for(l1)
