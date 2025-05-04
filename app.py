from flask import Flask, render_template, request
from sympy import symbols, sympify, lambdify
import numpy as np

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result_table = []
    if request.method == "POST":
        expr_str = request.form.get("expression")  # e.g. "x + y"
        x0 = float(request.form.get("x0"))
        y0 = float(request.form.get("y0"))
        h = float(request.form.get("h"))
        steps = int(request.form.get("steps"))
        method = request.form.get("method")  # AB2, AB3, AB4, AM2

        x, y = symbols("x y")
        expr = sympify(expr_str)
        f = lambdify((x, y), expr, modules=["numpy"])

        xs = [x0]
        ys = [y0]

        # Start with RK2 for bootstrapping
        for _ in range(min(3, steps)):
            k1 = f(xs[-1], ys[-1])
            k2 = f(xs[-1] + h, ys[-1] + h * k1)
            y_next = ys[-1] + (h / 2) * (k1 + k2)
            x_next = xs[-1] + h
            xs.append(x_next)
            ys.append(y_next)

        for i in range(3, steps):
            xi, yi = xs[i], ys[i]
            xi_1, yi_1 = xs[i - 1], ys[i - 1]
            xi_2, yi_2 = xs[i - 2], ys[i - 2]

            if method == "AB2":
                y_next = yi + h * (3 * f(xi, yi) - f(xi_1, yi_1)) / 2
            elif method == "AB3":
                y_next = yi + h * (23 * f(xi, yi) - 16 * f(xi_1, yi_1) + 5 * f(xi_2, yi_2)) / 12
            elif method == "AB4":
                xi_3, yi_3 = xs[i - 3], ys[i - 3]
                y_next = yi + h * (55 * f(xi, yi) - 59 * f(xi_1, yi_1) + 37 * f(xi_2, yi_2) - 9 * f(xi_3, yi_3)) / 24
            elif method == "AM2":
                f_pred = f(xi, yi)
                x_next = xi + h
                y_predictor = yi + h * f_pred
                y_next = yi + h * (f_pred + f(x_next, y_predictor)) / 2
            else:
                y_next = yi  # fallback

            x_next = xi + h
            xs.append(x_next)
            ys.append(y_next)

        result_table = list(zip(xs, ys))

    return render_template("index.html", result_table=result_table)

if __name__ == "__main__":
    app.run(debug=True)








# /////////////////////////////////////////////////////////


# from flask import Flask, render_template, request, flash, redirect
# import numpy as np
# import matplotlib.pyplot as plt
# from sympy import symbols, lambdify
# import io
# import base64

# app = Flask(__name__)
# app.secret_key = 'secret_key_here'  # Required for flash messages

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     result = None
#     table = []
#     img = None

#     if request.method == 'POST':
#         try:
#             expr = request.form['equation'].replace('^', '**')  # Fix here
#             x0 = float(request.form['x0'])
#             y0 = float(request.form['y0'])
#             h = float(request.form['h'])
#             xn = float(request.form['xn'])
#             method = request.form['method']
#             bootstrap_method = request.form['bootstrap']

#             x, y = symbols('x y')
#             f = lambdify((x, y), expr)

#             xs = [x0]
#             ys = [y0]
#             steps = int((xn - x0) / h)

#             # Bootstrap requirement map
#             required_bootstrap_steps = {
#                 'AB2': 2,
#                 'AB3': 3,
#                 'AB4': 4,
#                 'AM2': 1
#             }
#             bootstrap_needed = required_bootstrap_steps.get(method, 1)

#             if steps < bootstrap_needed:
#                 flash(f"Step count too low for {method}. At least {bootstrap_needed} steps are required.")
#                 return redirect('/')

#             # Bootstrap phase
#             for _ in range(bootstrap_needed):
#                 xi, yi = xs[-1], ys[-1]
#                 if bootstrap_method == "Euler":
#                     y_next = yi + h * f(xi, yi)
#                 elif bootstrap_method == "Heun":
#                     k1 = f(xi, yi)
#                     k2 = f(xi + h, yi + h * k1)
#                     y_next = yi + (h / 2) * (k1 + k2)
#                 elif bootstrap_method == "RK2":
#                     k1 = f(xi, yi)
#                     k2 = f(xi + h/2, yi + h/2 * k1)
#                     y_next = yi + h * k2
#                 elif bootstrap_method == "RK4":
#                     k1 = f(xi, yi)
#                     k2 = f(xi + h/2, yi + h/2 * k1)
#                     k3 = f(xi + h/2, yi + h/2 * k2)
#                     k4 = f(xi + h, yi + h * k3)
#                     y_next = yi + (h / 6) * (k1 + 2*k2 + 2*k3 + k4)
#                 else:
#                     flash("Invalid bootstrap method selected.")
#                     return redirect('/')
#                 x_next = xi + h
#                 xs.append(x_next)
#                 ys.append(y_next)

#             # Adams phase
#             for i in range(len(xs), steps + 1):
#                 xi = xs[-1]
#                 if method == "AB2":
#                     fi_1 = f(xs[-2], ys[-2])
#                     fi = f(xs[-1], ys[-1])
#                     y_next = ys[-1] + h * ((3/2)*fi - (1/2)*fi_1)
#                 elif method == "AB3":
#                     fi_2 = f(xs[-3], ys[-3])
#                     fi_1 = f(xs[-2], ys[-2])
#                     fi = f(xs[-1], ys[-1])
#                     y_next = ys[-1] + h * ((23*fi - 16*fi_1 + 5*fi_2)/12)
#                 elif method == "AB4":
#                     fi_3 = f(xs[-4], ys[-4])
#                     fi_2 = f(xs[-3], ys[-3])
#                     fi_1 = f(xs[-2], ys[-2])
#                     fi = f(xs[-1], ys[-1])
#                     y_next = ys[-1] + h * ((55*fi - 59*fi_1 + 37*fi_2 - 9*fi_3)/24)
#                 elif method == "AM2":
#                     fi_1 = f(xs[-1], ys[-1])
#                     predictor = ys[-1] + h * fi_1
#                     fi = f(xs[-1] + h, predictor)
#                     y_next = ys[-1] + h * (fi + fi_1)/2
#                 else:
#                     flash("Invalid Adams method selected.")
#                     return redirect('/')
#                 x_next = xs[-1] + h
#                 xs.append(x_next)
#                 ys.append(y_next)

#             # Create table
#             for xi, yi in zip(xs, ys):
#                 table.append({'x': round(xi, 4), 'y': round(yi, 4)})

#             # Plotting
#             fig, ax = plt.subplots()
#             ax.plot(xs, ys, marker='o')
#             ax.set_title('Solution Curve')
#             ax.set_xlabel('x')
#             ax.set_ylabel('y')
#             ax.grid(True)

#             buf = io.BytesIO()
#             plt.savefig(buf, format='png')
#             buf.seek(0)
#             img = base64.b64encode(buf.getvalue()).decode('utf-8')
#             buf.close()

#         except Exception as e:
#             flash(f"An error occurred: {str(e)}")
#             return redirect('/')

#     return render_template('index.html', result=result, table=table, img=img)

# if __name__ == '__main__':
#     app.run(debug=True)
