import random
from flask import Flask, request, redirect, render_template, session, flash
from decimal import Decimal

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'yrtsimehc'

@app.route('/')
def index():
    return render_template('index.html',title="Measurement Practice")

if __name__ == '__main__':
    app.run()