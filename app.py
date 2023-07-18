from logging import debug
from flask import Flask, render_template, redirect, request, url_for
import os

app = Flask(__name__)
# app.config['SECRET_KEY'] =  os.environ.get('SECRET_KEY')
app.config['SECRET_KEY'] = "changeme"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/conversion_temperature", methods=['GET', 'POST'])
def conversion_Temperature():
    if request.method == 'POST':
        input_val = float(request.form['inputval'])
        choice = request.form['selected_temp']
        if choice == '1':
            # Convert F to C
            result = format((input_val * 9/5 + 32), '.2f')
        elif choice == '2':
            # Convert C to F
            result = format(((input_val - 32) * 5/9), '.2f')
        else:
            result = 0

        return render_template("conversion_temperature.html", result=result, input_val=input_val, choice=choice)
    return render_template("conversion_temperature.html")


@app.route("/simulation", methods=['GET', 'POST'])
def simulation():
    return render_template("simulation.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
