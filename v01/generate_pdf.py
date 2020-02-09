#-------------IMPORTS------------#
from PyPDF2 import PdfFileReader, PdfFileWriter
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.ttfonts import pdfmetrics
from datetime import date
import csv
from reportlab.pdfgen import canvas
import os


#--------------------FORMAT TODAYS DATE FOR THE INVOICE----------------------#
def formatInvoiceDate(): # gets todays date and formats date for the header date
    currdate = date.today().strftime("%d%B%Y")

    dateString = ""
    dateString += "{} {} {}".format(currdate[0:2],currdate[2:5],currdate[-4::])

    return dateString

#--------------------FORMATS INVOICE DATES FOR THE INVOICE----------------------#
def stripDate(table): # Formats the date for the invoice dates
    startDate = table[1].split()
    endDate =  table[2].split()
    dateString = ""



    if(startDate[1] == endDate[1]):
        dateString += "{}-{} {} {}".format(startDate[0],endDate[0],startDate[1][0:3],startDate[2])
    else:
        dateString += "{} {}-{} {} {}".format(startDate[0], startDate[1][0:3], endDate[0], endDate[1][0:3], startDate[2])

    return dateString

#--------------------LOADS ADDRESSES FROM THE CSV-----------------#
def loadAddresses(): # Loads addresses from the cvs
    file = open('addresses.csv','r')
    reader = csv.reader(file)
    addresses = {}

    for row in reader:
        addresses[row[0]] = row[1::]

    file.close()
    return addresses
#########################################################################
#                   HERE THE PDF IS GENERATED                           #
#########################################################################

def generate_invoice(invoice_data,PO_number, extra_lines,path):

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    pdfmetrics.registerFont(TTFont('roboto-light', 'Roboto-Light.ttf'))
    pdfmetrics.registerFont(TTFont('roboto', 'Roboto-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('bold', 'Roboto-Bold.ttf'))
    can.setFont('roboto-light', 11)

    leftMargin = 168
    rightMargin = 560
    middleCol = 400
    invoice = invoice_data.copy()

    #-----------------------------------------PRINT ADDRESS----------------------------#
    addresses = loadAddresses()
    if invoice[3] in addresses:
        add = addresses[invoice[3]].copy() # copy the stored address
        add.insert(0, invoice[3]) # insert company name
        lines = len(add) # count number of lines

        baseLine = 700 # height of the first line

        for text in add:
            can.drawString(leftMargin, baseLine + 13 * lines, text)
            lines -= 1


    # ------------------------------DATE AND NUMBER-------------------------------------#
    invDate = formatInvoiceDate()
    number = str(invoice[6])
    can.drawRightString(545, 698, invDate)
    can.drawRightString(545, 686, number)

    # -----------------------------STANDARD ITEMS---------------------------------------#

    dateRange = stripDate(invoice)
    itemsNo = "{} x {}".format(invoice[5], invoice[4])

    can.setFont('roboto', 12)

    firstLine = 580
    can.drawString(leftMargin, firstLine, dateRange)
    can.drawRightString(middleCol, firstLine, itemsNo)
    can.drawRightString(rightMargin, firstLine, "£{:.2f}".format(float(invoice[7])))

    # -----------------------------EXTRA ITEMS-------------------------------------------#
    first_line_extra = 555
    if extra_lines:

        for line in extra_lines:
            can.drawString(leftMargin, first_line_extra, line[0]) # ITEM NAME
            if line[2]<0:
                can.drawRightString(middleCol, first_line_extra, "{} x -£{:.2f}".format(line[1], line[2]*-1))  # UNITS x PRICE
            else:
                can.drawRightString(middleCol, first_line_extra, "{} x £{:.2f}".format(line[1], line[2]))  # UNITS x PRICE
            price = float(line[1]) * float(line[2])
            if price <0:
                can.drawRightString(rightMargin, first_line_extra, '-£{:.2f}'.format(price*-1))  # FINAL PRICE
            else:
                can.drawRightString(rightMargin, first_line_extra, '£{:.2f}'.format(price))  # FINAL PRICE
            first_line_extra -= 20

        add_to_total = sum([float(line[1])*float(line[2]) for line in extra_lines])
        invoice[7] += add_to_total
        invoice[8] = invoice[7] * 0.2
        invoice[9] = invoice[7] + invoice[8]

        first_line_extra -= 20
        can.drawRightString(middleCol, first_line_extra, "SUBTOTAL")
        can.drawRightString(rightMargin, first_line_extra, '£{:.2f}'.format(invoice[7]))
        first_line_extra -=20




    # --------------------------------VAT------------------------------------------------#
    secondLine = 530-(555-first_line_extra)
    can.drawString(leftMargin, secondLine, "VAT")
    can.drawRightString(middleCol, secondLine, "20%")
    can.drawRightString(rightMargin, secondLine, "£{:.2f}".format(float(invoice[8])))

    # SEPARATOR
    sepLine = secondLine-30
    can.line(leftMargin, sepLine, rightMargin, sepLine)

    # TOTAL
    totalLine = secondLine-70
    can.setFont('bold', 30)
    can.drawString(300, totalLine, "TOTAL")
    can.drawRightString(rightMargin, totalLine, "£{:.2f}".format(float(invoice[9])))

    # PO

    if PO_number:

        can.setFont('bold', 24)
        can.drawString(300, 700, PO_number)

    can.save()

    packet.seek(0)
    newPdf = PdfFileReader(packet)

    existingPdf = PdfFileReader(open("invoice_BLANK.pdf", "rb"))
    output = PdfFileWriter()

    page = existingPdf.getPage(0)
    page.mergePage(newPdf.getPage(0))
    output.addPage(page)
    if (PO_number):
        filename = "{}-{}-{}-{}.pdf".format(invoice[6], invoice[7], "YOURNAME", invoice[3])
    else:
        filename = "{}-{}-{}.pdf".format(invoice[6], "YOURNAME", invoice[3])

    filename = path + "/" + filename

    outputStream = open(filename, "wb")
    output.write(outputStream)
    outputStream.close()
    os.startfile(filename)
