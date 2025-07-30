def fibonacci(n):
    fibos = []
    for i in range(n + 1):
        if i == 0:
            fibos.append(0)
        elif i == 1:
            fibos.append(1)
        else:
            fibos.append(fibos[i - 1] + fibos[i - 2])
    return fibos[n]

def fibonacci_sum(n1, n2):
    fb_n1 = fibonacci(n1)
    fb_n2 = fibonacci(n2)

    print(f"Fibonacci({n1}) = {fb_n1}, Fibonacci({n2}) = {fb_n2}")  # Debugging line
    result = fb_n1 + fb_n2
    return result