def get_abs_errors(x, y):
    n = len(x)
    return [x[i] - y[i] for i in range(0, n)]
