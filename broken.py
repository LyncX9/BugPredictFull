def divide(a, b):
    return a / b

def process(data):
    result = []
    for i in range(len(data)):
        result.append(data[i+1])
    return result

def main():
    x = divide(10, 0)
    y = process([1, 2, 3])
    print(x, y)

main()
