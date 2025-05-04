# def rk2(f, x, y, h):
#     k1 = f(x, y)
#     k2 = f(x + h, y + h * k1)
#     return y + (h / 2) * (k1 + k2)

# def ab2_method(f, x0, y0, h, n):
#     xs = [x0]
#     ys = [y0]
#     xs.append(x0 + h)
#     ys.append(rk2(f, x0, y0, h))

#     for i in range(1, n):
#         x_new = xs[i] + h
#         y_new = ys[i] + (h / 2) * (3 * f(xs[i], ys[i]) - f(xs[i - 1], ys[i - 1]))
#         xs.append(x_new)
#         ys.append(y_new)
#     return list(zip(xs, ys))

# def ab3_method(f, x0, y0, h, n):
#     xs = [x0]
#     ys = [y0]
#     for i in range(2):
#         xs.append(xs[-1] + h)
#         ys.append(rk2(f, xs[-2], ys[-2], h))

#     for i in range(2, n):
#         x_new = xs[i] + h
#         y_new = ys[i] + (h / 12) * (23 * f(xs[i], ys[i]) - 16 * f(xs[i - 1], ys[i - 1]) + 5 * f(xs[i - 2], ys[i - 2]))
#         xs.append(x_new)
#         ys.append(y_new)
#     return list(zip(xs, ys))

# def ab4_method(f, x0, y0, h, n):
#     xs = [x0]
#     ys = [y0]
#     for i in range(3):
#         xs.append(xs[-1] + h)
#         ys.append(rk2(f, xs[-2], ys[-2], h))

#     for i in range(3, n):
#         x_new = xs[i] + h
#         y_new = ys[i] + (h / 24) * (
#             55 * f(xs[i], ys[i]) - 59 * f(xs[i - 1], ys[i - 1]) +
#             37 * f(xs[i - 2], ys[i - 2]) - 9 * f(xs[i - 3], ys[i - 3])
#         )
#         xs.append(x_new)
#         ys.append(y_new)
#     return list(zip(xs, ys))

# def adams_moulton2(f, x0, y0, h, n):
#     xs = [x0]
#     ys = [y0]
#     xs.append(x0 + h)
#     ys.append(rk2(f, x0, y0, h))

#     for i in range(1, n):
#         x_pred = xs[i] + h
#         y_pred = ys[i] + (h / 2) * (3 * f(xs[i], ys[i]) - f(xs[i - 1], ys[i - 1]))
#         y_corr = ys[i] + (h / 12) * (
#             5 * f(x_pred, y_pred) + 8 * f(xs[i], ys[i]) - f(xs[i - 1], ys[i - 1])
#         )
#         xs.append(x_pred)
#         ys.append(y_corr)
#     return list(zip(xs, ys))