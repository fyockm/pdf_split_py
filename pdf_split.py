from pyPdf import PdfFileWriter, PdfFileReader

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import csv
import smtplib
import sys

"""PDF split problem

Expected CSV format:
Drew Fyock,fyockm@gmail.com,amfyock@gmail.com
Kurt Lesker,kurtl@lesker_x.com
Cyndy Lesker,cyndyl@lesker_x.com,kurtl@lesker_x.com
Tad Dockstader,tomd@lesker_x.com
...

sample input for pdfReader:
>python kjlc_pdf_split.py kjlc.pdf email_list.txt

pyPdf info:
http://pybrary.net/pyPdf/

Developer : Drew Fyock (fyockm@gmail.com)
All code (c)2012 - All rights reserved
"""

def get_names(nameCsv):
  names = {}
  file = open(nameCsv,"rb")
  reader = csv.reader(file)    # read a line from the csv
  try:
    for row in reader:         # row is a list of elements
      names[row[0]] = row[1:]  # create key/value pairs (name/emails)
  except csv.Error, e:
    sys.exit('file %s, line %d: %s' % (file,reader.line_num,e))
  file.close()
  return names


def send_email(smtp,pdfWriter,filename,names):
  # write the file
  filename += '.pdf'
  wf = file(filename,"wb")
  pdfWriter.write(wf)
  wf.close()
  
  # send email to recipients
  msg = MIMEMultipart()
  msg['From'] = 'fyockm@gmail.com'
  msg['To'] =  ', '.join(names[prevName])
  msg['Subject'] = 'PDF from Vendor'

  # message text
  msg.attach(MIMEText("See attachment!"))

  # read the recent file and add as email attachment
  fp = open(filename,'rb')
  attach = MIMEApplication(fp.read(),'pdf')
  attach.add_header('Content-Disposition','attachment',filename=filename)
  msg.attach(attach)
  fp.close()

  # Send the email
  smtp.sendmail(msg['From'],msg['To'],msg.as_string())


def parse_file(pdfFile,nameFile):
  pdfReader = PdfFileReader(file(pdfFile,"rb"))
  
  # read the names and emails from csv file
  names = get_names(nameFile)
  
  # create an instance in SMTP server
  smtp = smtplib.SMTP('localhost')
  
  # loop through the pages of the pdf
  # when a name is found, write pages to a new pdf until next name is found
  # then write the file and email as attachment
  i = 0
  prevName = ""
  while i<pdfReader.getNumPages():
    page = pdfReader.getPage(i)
    pageStr = page.extractText()      # extract the pdf text
    for name in names.keys():
      if pageStr.lower().find(name.lower())!=-1:
        if 'pdfWriter' in locals():   # send the current pdf
          send_email(smtp,pdfWriter,prevName,names)

        pdfWriter = PdfFileWriter()   # create new pdfWriter file and add current page
        prevName = name               # save off previous name
        break
    if 'pdfWriter' in locals():
      pdfWriter.addPage(page)
    i+=1

  # send the last file
  if 'pdfWriter' in locals():
    send_email(smtp,pdfWriter,prevName,names)
    
  # quit the smtp server
  smtp.quit()

  
# This basic command line argument parsing code
# 1 pdf file to parse 
# 2 name/email csv
def main():
  if len(sys.argv) != 3:
    print 'usage: ./kjlc_pdf_split.py pdfFile nameCsv'
    sys.exit(1)

  pdfFile = sys.argv[1]
  nameCsv = sys.argv[2]
  
  parse_file(pdfFile,nameCsv)


if __name__ == '__main__':
  main()
