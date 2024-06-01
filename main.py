import random
from flask import Flask, request, redirect, render_template, session, flash
from decimal import Decimal
from math import log

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'yrtsimehc'

def pick_numbers(divisions):
    first_num = 0
    # Set the end number on the ruler (1, 10, 1000, or 10,000 units larger than start)
    last_num = first_num + 10**(random.randint(-2, 3))
    last_sig_fig_position = (last_num-first_num)/(10*divisions)
    return [first_num, last_num, last_sig_fig_position]

@app.route('/')
def index():
    return render_template('index.html',title='Measurement Practice')

@app.route('/measurement_practice')
def measurement():
    num_divisions = random.choice([1, 10, 100])
    numbers = pick_numbers(num_divisions)
    object_length = random.uniform(numbers[1]*0.03, numbers[1])
    if numbers[2] < 1:
        round_to = -1*int(round(log(numbers[2],10),1))
        object_length = round(object_length, round_to)
    elif numbers[2] > 1:
        round_to = len(str(numbers[2]))-3
        object_length = int(object_length/10**round_to)*10**round_to
    else:
        object_length = int(object_length)
    wide = round(9.965*object_length*10/numbers[1]+0.2614, 3)
    return render_template('measurement_practice.html',title='Measurement Practice', 
        wide = wide, start_value = numbers[0], end_value = numbers[1], 
        object_length = object_length, num_divisions = num_divisions, nums = numbers)

if __name__ == '__main__':
    app.run()