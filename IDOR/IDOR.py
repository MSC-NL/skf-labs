#!/usr/bin/env python3

from flask import Flask, request, url_for, render_template, send_from_directory
import random
from fpdf import FPDF

app = Flask(__name__, static_url_path = '/static', static_folder = 'static')
app.config['DEBUG'] = True

pdf_ids= random.sample(range(0, 100), 60)

def generate_pdf(id, message):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, message)
    pdf.output(str(id) + '.pdf', 'F')

def create_pdf_pool():
    # generate a bunch of dummy pdf files
    for id in pdf_ids[:]:
        generate_pdf(id, 'Try again!')

    # generate the secret pdf
    generate_pdf(pdf_ids[random.randint(0, 60)], 'You have found the secret pdf, congratulations!')

@app.route("/")
def start():
    create_pdf_pool()
    return render_template("index.html")

@app.route("/download", methods = ['POST'])
def download():
    pdf_id = request.form['pdf_id']
    if int(pdf_id) in pdf_ids:
        pdfname = str(pdf_id) + ".pdf"
        return send_from_directory(directory=".", filename= pdfname, mimetype='application/pdf')
    else:
        return render_template("index.html", result = "Pdf not found. Try with another id between 1 and 500.")

@app.route("/create", methods = ['POST'])
def create():
    message = request.form['message']

    if len(pdf_ids) < 500:
        new_id = random.randint(0, 500)
        while new_id in pdf_ids:
            new_id = random.randint(0, 500)

        pdf_ids.append(new_id)
        generate_pdf(new_id, message)
        return render_template("index.html", result = "Pdf created successfully! ID:" + str(new_id))

    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
  app.run(host = '0.0.0.0')

