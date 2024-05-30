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
    starting_value = random.randint(0,101)
    end_value = starting_value + num_divisions
    wide = round(random.uniform(starting_value, end_value-1)/end_value*100,1)
    object_length = round(starting_value + wide/100*num_divisions,1)
    return render_template('measurement_practice.html',title='Measurement Practice', wide = wide, start_value = starting_value, end_value = end_value, object_length = object_length)

if __name__ == '__main__':
    app.run()