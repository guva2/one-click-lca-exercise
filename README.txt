Technical assignment for One Click LCA.

How To Run:
-----------

Installation:
Install the required libraries listed in requirements.txt

    pip install -r requirements.txt

Running:
Execute 'main.py' with your preferred method.

    python main.py

Configuration:
Various parameters can be modified via configuration. Simply edit values in
the settings.ini file as needed.

Dependencies:
-------------

This implementation uses 2 external libraries and 2 internal python libraries.
The requirements.txt file lists the external libraries and versions used:

    1) Requests for executing http requests
    2) BeautifulSoup for html parsing
    3) Camelot for pdf -> xlsx conversion in the expansion problem

The internal python libraries are:

    1) os for file management and directory creation
    2) configparser to allow for configurable parameters

Design:
-------

This project is a web scraper that downloads all pdf files from an html table
and writes them to disk. Specifically, this scraper is designed for the company
search results table on the www.greenbooklive.com site.

Each table cell can have multiple PDF links, which all appear to be associated
with a single company that is specified in a different table column. For clarity
we will organize the PDFs in directories by company. To illustrate, the PDF files
for the first three companies should be stored in directories as follows:

         2tec2            Addagrip Terraco            Aggregate Industries
           |                      |                            |
    ---------------               |              -----------------------------
    |             |               |              |             |             |
B...167.pdf   B...168.pdf    B...209.pdf    B...199.pdf   B...205.pdf   B...206.pdf

This implementation is split up into a few components for the sake of
readability and readiness for change:

    * A green_book_live package that handles all web interactions with the Green
      Book Live site. All http interactions and html parsing happens here. More
      precisely, this package includes the following:

        * GBLHttpService which handles requests and manages http client
          interactions with Green Book Live

        * CompanySearchHtmlParser which parses company search html pages
          and extracts pdf links

        * A scraper to coordinate the http service and html parser

    * A file_management package that handles file management and disk writing.
      This package includes the following:

        * MemoryFile which is a light wrapper around a file which allows us to
          manage pdfs in memory when writing to disk

        * FileWriter which writes MemoryFiles to disk

    * A main application 'main.py' which loads configuration parameters, and
      manages coordination of the scraping and file management packages.

Note that the web scraping service is deliberately isolated because it seems
likely that a script such as this should eventually be ported to use a proper
Green Book Live API of some sort. If someone ever wanted to accomplish this,
they could simply replace the scraper package with an API service call, and not
have to worry about the other components.

Future Changes:
---------------

This project was left a open ended, and there are features that would be nice
to add that I thought were out of scope for this project. I will list them here
for clarity:

    * Logging. This project was framed as a script that only needs to be run
      once, for a single url. If this were to run as a regular cronjob, one
      would probably want to add proper logging.

    * Error Handling/Healthcheck. Obviously this project won't work when faced
      with server-side HTTP/HTML errors, or I/O file errors. I didn't add robust
      error handling for these cases, but this would be necessary for monitoring
      if this script were to run regularly.

    * Unit Tests. I was hesitant to add unit tests to the scraping components
      because scrapers are not robust and vulnerable to change by nature. If
      the site were to change its http routing or html layouts, the scraping
      component would have to be rewritten altogether. Writing tests for such
      a brittle system seems counterproductive, as they will also have to be
      rewritten with every change. Moreover, robust testing is not as important
      for scripts that will not run regularly.

    * Web Driver. I initially chose not to use a web driver because I thought it
      would be overkill. I didn't expect any significant link crawling would be
      necessary. As it turns out the search results are paginated, and the pdf
      links are relative links as opposed to absolute links. This script could
      benefit from a proper web driver to navigate these specific links. 

    * Company Search parameters. The Green Book Live company search takes many
      parameters. Most of them seemed irrelevant for this assignment. As such
      I didn't make them accessible end-to-end. I did set up the http client to
      handle these arguments, but didn't expose them all the way to the main
      script. If this script was meant to be used regularly, I'd expose all
      of these parameters via config and program arguments.

Expansion:
----------

I've added a pdf converter that extracts pdf tables and exports them to xlsx
files. The PdfConverter class is under the file_management package. The main
code to convert pdfs is 'excel_main.py'. Simply install the requirements and
run:

    python excel_main.py

There are various parameters for this script which can also be configured in
'settings.ini'.

Note that pdf conversion has many edge cases so some tables could be skipped
or misformatted. I checked the files for 2tec2 and they seemed correct, but
obviously couldn't check every single pdf/xlsx file.

Output:
-------

All results are written to the out/ directory for your convenience.
