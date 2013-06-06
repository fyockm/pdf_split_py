PDF Splitter

Scenario:
We have just received a massive document from a vendor. Parts of the document are applicible to different people. Each part of the document can be a different number of pages. Parts are consecutive. There could be more than one recipent per part.  The name of the primary recipient is shown on the first page of their part of the document; auxiliary recipients are 'known" from other sources. They can receive their part via email.
 
Given:
- a PDF document (approx 500+ pages) (generate a random multipage PDF as a DEMO source document)
- approximately 100 parts to the document
- this will need to be done every few weeks
 
Problem:
Design and explain an efficient solution to distribute specific parts of a 500+ page PDF document to specified people. Describe interfaces, tools, datasets, and workflow to achieve the distribution. Include any assumptions you make about the problem.

Assumptions:
- PDF file from vendor is put in a specific directory
- Email of primary recipient and list of auxiliary recipients (and their email addresses) is available in a csv file in a specified directory
- Splitter program kicked off manually (only needed every few weeks) - waste of processing power to poll the directory, and no specific schedule given
- SMTP server available to send email
- Only one primary recipient per part - only first name on page processed
- Using Python 2.7 and pyPdf utility

Algorithm:
- Read file and loop through pages
- Read names file and set up key/value pairs where key is name and value is list of email addresses
- Loop through names, searching pdf page text for match
- If name found, create new pdf by copying page
- Add pages to new pdf until next page is found on big pdf with matching name
- Write new pdf and attach to email
- Recipients read from matching name in CSV
