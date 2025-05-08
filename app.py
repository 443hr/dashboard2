from flask import Flask, render_template, request, redirect, url_for, Response, flash
import pandas as pd
from data_read.chart_utils import generate_pie_chart, generate_spider_chart

import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend for web apps
import matplotlib.pyplot as plt


app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB limit


# Store file names and row counts
file_counts = {}

@app.route('/', methods=['GET', 'POST'])
def upload_files():
    global file_counts
    file_counts = {}
    if request.method == 'POST':
        uploaded_files = request.files.getlist('files')
        for file in uploaded_files:
            if file.filename.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file)
                file_counts[file.filename] = len(df)
            else:
                flash(f"{file.filename} is not a valid Excel file.", 'error')
        if file_counts:
            return redirect(url_for('dashboard'))
        else:
            flash("No valid files uploaded.", 'error')
    return render_template('upload.html')

@app.route('/dashboard2')
def dashboard2():
    if not file_counts:
        return redirect(url_for('upload_files'))
    return render_template('dashboard2.html')


@app.route('/dashboard')
def dashboard():
    if not file_counts:
        return redirect(url_for('upload_files'))
    return render_template('dashboard.html')

@app.route('/plot.png')
def plot_png():
    if not file_counts:
        return "No data uploaded", 400
    buf = generate_pie_chart(file_counts)
    return Response(buf.getvalue(), mimetype='image/png')


@app.route('/spider.png')
def spider_png():
    if not file_counts:
        return "No data uploaded", 400
    buf = generate_spider_chart(file_counts)
    return Response(buf.getvalue(), mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
