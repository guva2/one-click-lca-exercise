from .http_service import GBLHttpService
from .html_parser import CompanySearchHtmlParser

class Scraper():
    def __init__(self):
        self.gbl_http_service = GBLHttpService()

    def scrape_page_pdf_files(self):
        html = self.gbl_http_service.company_search()
        parser = CompanySearchHtmlParser(html)
        company_pdf_links = parser.get_company_pdf_links()

        for company in company_pdf_links:
            for pdf_link in company_pdf_links[company]:
                pdf_file = self.gbl_http_service.get_file(pdf_link)
                pdf_file.dir_path = company
                yield pdf_file

