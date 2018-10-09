import os
from flask import Flask, render_template, request, send_from_directory, jsonify, Response, send_file
import cv2
import numpy as np
import datetime
import processImage
import flask_excel as excel
import pandas as pd
from io import BytesIO
import xlsxwriter
from flask_mail import Mail, Message
import random
#from models import db
#from vincent.colors import brews

app = Flask(__name__)
excel.init_excel(app)

# Mail setup

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'spinachfarmerdemo@gmail.com'
app.config['MAIL_PASSWORD'] = 'eatspinach'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/learningflask'

@app.route("/")
def welcome():
    return render_template("Welcome.html")

@app.route("/prescan")
def prescan():
    return render_template("prescan.html")

@app.route("/home")
def home():
    return render_template("home.html", image_A="/static/spinA.jpg", image_B="/static/spinB.jpg", image_C="/static/spinC.jpg", image_outA="static/spinOutA.jpg", image_outB="static/spinOutB.jpg", image_outC="static/spinOutC.jpg")

@app.route("/download", methods=['GET'])
def download_file():
    return excel.make_response_from_array([[1, 2], [3, 4]], "csv")


@app.route("/getPlotCSV")
def getPlotCSV():
    now = datetime.datetime.now()
    reportname = "Report" + str(now) + ".xlsx"


    CLT = {'Poor': 1200, 'Mid': 5000, 'Good': 19000}
    LA = {'Poor': 200, 'Mid': 3000, 'Good': 12000}
    SD = {'Poor': 1100, 'Mid': 4000, 'Good': 17000}
    PHX = {'Poor': 900, 'Mid': 6000, 'Good': 20000}

    data1 = [CLT, LA, SD, PHX]
    index1 = ['CLT', 'LA', 'SD', 'PHX']


    # headings = ['Month', 'CLT', 'LA', 'SD', 'PHX']
    # data2 = [
    #     [1,2,3,4,5,6,7,8,9,10,11,12],
    #     [-5, 5, 1, 6, -2, 3, 9, 0, 1, -3, 0, 1],
    #     [-5, 5, 1, 6, -2, 3, 9, 0, 1, -3, 0, 1],
    #     [-5, 5, 1, 6, -2, 3, 9, 0, 1, -3, 0, 1],
    #     [-5, 5, 1, 6, -2, 3, 9, 0, 1, -3, 0, 1],
    #  ]

    df = pd.DataFrame(data1, index=index1)
    # df2 = pd.DataFrame(data2, index=headings)

    output = BytesIO()

    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    sheetname = 'Farm_Report'
    # sheetname2 = 'Growth_Report'

    df.to_excel(writer, sheet_name=sheetname)
    # df2.to_excel(writer, sheet_name=sheetname2)

    workbook = writer.book
    worksheet = writer.sheets[sheetname]
    # worksheet2 = writer.sheets[sheetname2]


    barChart = workbook.add_chart({'type': 'column', 'subtype': 'stacked'})
    # lineChart = workbook({'type': 'line'})

    for col_num in range(1, len(CLT) + 1):
        barChart.add_series({
            'name': [sheetname, 0, col_num],
            'categories': [sheetname, 1, 0, 4, 0],
            'values': [sheetname, 1, col_num, 4, col_num],
            'gap': 20,
        })

    # lineChart.add_series({
    #     'name': [sheetname2, 0, 2],
    #     'categories': [sheetname2, 1, 0, 6, 0],
    #     'values': [sheetname2, 1, 2, 6, 2],
    # })

    barChart.set_x_axis({'name': 'Farms'})
    barChart.set_y_axis({'name': 'Output', 'major_gridlines': {'visible': False}})



    worksheet.insert_chart('A1', barChart)
    worksheet.insert_image('G14', '/Users/rafrank/Desktop/CapstoneCV/static/Oracle-Logo.png', {'x_scale': 0.03, 'y_scale': 0.03})
    writer.close()

    output.seek(0)

    return send_file(output, attachment_filename=reportname, as_attachment=True)

@app.route("/send_recall_notification")
def send_recall_notification():
    msg = Message('Recall Event', sender='spinachfarmerdemo@gmail.com', recipients=['frankr333@gmail.com'])
    now = datetime.datetime.now()

    msg.body = str(now) + " --- This is a recall notitication reagrding your spinach order"
    mail.send(msg)
    return "Recall notification successfully sent"


# def qualityCheck(brownAreaSum, fullArea):
#     brownRatio = (brownAreaSum / fullArea) * 100
#     return round(brownRatio, 2)
#
# @app.route("/upload/<filename>")
# def send_image(filename):
#     return send_from_directory("images", filename)

# @app.route("/upload", methods=['POST'])
# def upload():
#     target = os.path.join(APP_ROOT, 'images')
#     #print(target)
#
#     if not os.path.isdir(target):
#         os.mkdir(target)
#     else:
#         print("Couldn't create upload directory: {}".format(target))
#     #print(request.files.getlist("file"))
#
#     for upload in request.files.getlist("file"):
#         # print(upload)
#         filename = upload.filename
#         destination = "/".join([target, filename])
#         # print("Target:", target)
#         # print("Accept incoming file:", filename)
#         # print("Save it to:", destination)
#         upload.save(destination)
#
#     return render_template("complete.html", image_name=filename)


###################################


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)


