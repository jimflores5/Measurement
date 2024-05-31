import random
from flask import Flask, request, redirect, render_template, session, flash
from decimal import Decimal

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'yrtsimehc'

@app.route('/')
def index():
    return render_template('index.html',title='Measurement Practice')

@app.route('/measurement_practice')
def measurement():
    num_divisions = random.choice([1, 10, 100])
    if num_divisions == 100:
        num_decimals = 2
    elif num_divisions == 10:
        num_decimals = 1
    else:
        num_decimals = 0
    # starting_value = random.randint(0,101)
    starting_value = 0
    # end_value = starting_value + num_divisions
    end_value = 10
    # wide = round(random.uniform(starting_value, end_value-1)/end_value*100,2)
    # object_length = round(starting_value + wide/100*num_divisions,2)
    object_length = round(random.uniform(starting_value+0.3, end_value),num_decimals)
    wide = round(9.96*object_length+0.261, 1)
    return render_template('measurement_practice.html',title='Measurement Practice', 
        wide = wide, start_value = starting_value, end_value = end_value, 
        object_length = object_length, num_divisions = num_divisions)

if __name__ == '__main__':
    app.run()