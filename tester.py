


def testA():
    for i in range(1, 10):
        for j in range(1, 5):
            yield "outer "+str(i)+" inner "+str(j)+")"


for res in testA():
    print(res)