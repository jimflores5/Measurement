import random
from flask import Flask, request, redirect, render_template, session, flash
from math import log

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'yrtsimehc'

def pick_numbers(divisions):
    first_num = 0
    # Set the end number on the ruler (1, 10, or 1000 units larger than start)
    last_num = first_num + 10**(random.randint(-2, 3))
    last_sig_fig_position = (last_num-first_num)/(10*divisions)
    if last_sig_fig_position >= 1:
        last_sig_fig_position = int(last_sig_fig_position)
    return [first_num, last_num, last_sig_fig_position]

def add_trailing_zero(length, sig_fig_position):
    if sig_fig_position >= 1:
        return str(length)
    if 'e' not in str(sig_fig_position):
        num_decimals = len(str(sig_fig_position).split('.')[1])
    else:
        num_decimals = int(str(sig_fig_position)[-1])
    if len(str(length).split('.')[1]) < num_decimals:
        length = str(length) + '0'
    return length

def is_valid_measurement(ans):
    if len(ans) > 7 or ans == '':
        # Submitted answer should be 7 characters long or less.
        return False
    for char in ans:
        # Check for negative or non-numerical entries.
        if char not in '0123456789.':
            return False
    return True

def is_correct_precision(ans, corr_ans, precis):
    if precis < 1:
        # If the last sig fig is to the right of the decimal, compare the
        # number of decimal places the answer and the correct answer.
        try:
            ans_decimals = len(ans.split('.')[1])
        except:
            return False
        correct_decimals = len(str(corr_ans).split('.')[1])
        return ans_decimals == correct_decimals
    elif precis == 1:
        # If the last sig fig is in the 1's place, the submitted answer must
        # be an integer.
        return '.' not in ans
    elif precis == 10:
        # If the last sig fig is in the 10's place, the answer must be an
        # integer, and the digit in the 1's place MUST be 0.
        return '.' not in ans and ans[-1] == '0'
    else:
        # If the last sig fig is in the 100's place, the answer must be an
        # integer, and the digits in the 10's and 1's places MUST be 0.
        return '.' not in ans and ans[-2:] == '00'

def is_correct_answer(ans, corr_ans, precis, divisions):
    if precis >= 1:
        # Length values are whole numbers. Convert string values to int.
        ans = int(ans)
        decimal_places = 0
    else:
        # Length values are decimal results.
        decimal_places = len(str(corr_ans).split('.')[1])
        ans = round(float(ans), decimal_places)
    valid_range = find_range(corr_ans, precis, divisions)
    return valid_range[0] <= ans <= valid_range[1]

def find_range(corr_ans, precis, divisions):
    if precis >= 1:
        decimal_places = 0
        corr_ans = int(corr_ans)
    else:
        decimal_places = len(str(corr_ans).split('.')[1])
        corr_ans = round(float(corr_ans), decimal_places)
    if divisions == 100:
        # For 100 divisions on the ruler, accept +/- 2 of the last sig fig.
        error = round(2*precis, decimal_places)
    else:
        # For 10 or fewer divisions on the ruler, accept +/- 1 of the last sig fig.
        error = precis
    start = round(corr_ans - error, decimal_places)
    end = round(corr_ans + error, decimal_places)
    return (start, end)

@app.route('/')
def index():
    session.clear()
    session['num_attempted'] = 0
    session['num_correct'] = 0
    return render_template('index.html',title='Measurement Practice')

@app.route('/accuracy_vs_precision/<page>', methods=['POST', 'GET'])
def accuracy(page):
    page_title = 'Accuracy vs. Precision'
    num_pages = 3
    template_name = 'accuracy_vs_precision'
    page = int(page)
    if request.method == 'POST':
        pass
    else:
        if page == 1:
            subheading = 'Accuracy & precision definitions & examples...'
        elif page == 2:
            subheading = 'Precision vs. # of decimal places...'
        elif page == 3:
            subheading = 'Concept questions...'
        else:
            subheading = 'Content for this page TBD...'
    return render_template('accuracy_vs_precision.html',title='Accuracy vs. Precision', page = page, page_title = page_title, 
            num_pages = num_pages, template = template_name, subheading = subheading)

@app.route('/measuring/<page>', methods=['POST', 'GET'])
def measuring(page):
    page_title = 'Taking Measurements'
    num_pages = 5
    template_name = 'measuring'
    page = int(page)
    if request.method == 'POST':
        pass
    else:
        subheading = 'Content coming soon...'
    return render_template('measuring.html',title='Taking Measurements', page = page, page_title = page_title, 
            num_pages = num_pages, template = template_name, subheading = subheading)

@app.route('/common_mistakes/<page>', methods=['POST', 'GET'])
def common_mistakes(page):
    page_title = 'Common Measurement Mistakes'
    num_pages = 2
    template_name = 'common_mistakes'
    page = int(page)
    if request.method == 'POST':
        pass
    else:
        subheading = 'Content coming soon...'
    return render_template('common_mistakes.html',title='Common Measurement Mistakes', page = page, page_title = page_title, 
            num_pages = num_pages, template = template_name, subheading = subheading)

@app.route('/measurement_practice', methods=['POST', 'GET'])
def measurement():
    if request.method == 'POST':
        answer = request.form['answer']
        if answer[0] == '.':
            answer = '0' + answer
        if not is_valid_measurement(answer):
            # Check if answer is a valid, positive number.
            # If not, display error message.
            flash('Please enter a positive, numerical value with the correct precision.', 'error')
        elif not is_correct_precision(answer, session['length'], session['precision']):
            # Check if answer has the corret precision.
            # If not, display error message.
            flash(f"Incorrect precision. Round to the nearest {session['precision']} {session['unit']} (e.g. {session['length']} {session['unit']}).", 'error')
        elif not is_correct_answer(answer, session['length'], session['precision'], session['divisions']):
            # Check if submitted answer falls within accepted range compared
            # to the actual length. If not, display error message.
            flash(f"Correct precision but incorrect measurement. Actual length ≈ {session['length']} {session['unit']}", 'error')
        else:
            # Submitted answer has correct value and precision.
            # Display favorable message.
            flash('Correct!  :-)', 'correct')
            if session['first_try']:
                session['num_correct'] += 1
        session['first_try'] = False
        display_value = answer
    else:
        num_divisions = random.choice([1, 10, 100])
        unit = random.choice(['µm', 'mm', 'cm', 'm'])
        numbers = pick_numbers(num_divisions)
        session['precision'] = numbers[2]
        if num_divisions != 1:
            object_length = random.uniform(numbers[1]*0.03, numbers[1])
        else:
            object_length = random.uniform(numbers[1]*0.1, numbers[1])
        if numbers[2] < 1:
            round_to = -1*int(round(log(numbers[2],10),1))
            object_length = round(object_length, round_to)
        elif numbers[2] > 1:
            round_to = len(str(numbers[2]))-1
            object_length = int(object_length/10**round_to)*10**round_to
        else:
            object_length = int(object_length)
        wide = round(9.965*object_length*10/numbers[1]+0.2614, 3)
        # Add trailing significant zero, if needed.
        object_length = add_trailing_zero(object_length, numbers[2])
        session['length'] = object_length
        session['wide'] = wide
        session['numbers'] = numbers
        session['divisions'] = num_divisions
        session['unit'] = unit
        session['num_attempted'] += 1
        session['first_try'] = True
        display_value = ''
    percent_correct = round(session['num_correct']/session['num_attempted']*100,1)
    return render_template('measurement_practice.html',title='Measurement Practice', 
        wide = session['wide'], start_value = session['numbers'][0], end_value = session['numbers'][1], 
        object_length = session['length'], num_divisions = session['divisions'], nums = session['numbers'],
        unit = session['unit'], display_value = display_value, correct = percent_correct)

if __name__ == '__main__':
    app.run()