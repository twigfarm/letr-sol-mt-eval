class A:
    def __init__(self, a):
        self.a = a

    def __len__(self):
        return len(self.a)

    def __str__(self):
        # print(self.a)
        return self.a

c = A([1,2,3])
print(len(c))