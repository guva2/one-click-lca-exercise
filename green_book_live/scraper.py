from .http_service import GBLHttpService
from .html_parser import CompanySearchHtmlParser

class Scraper():
    """
    A scraper that extracts pdfs from GreenBookLive.

    Attributes
    ----------
    gbl_http_service : GBLHttpService
        the GreenBookLive http service through which requests are made

    Methods
    -------
    scrape_page_pdf_files()
        retrieves and returns all searched pdfs

    """

    def __init__(self, base_url):
        self.gbl_http_service = GBLHttpService(base_url)
        self.parser = CompanySearchHtmlParser()

    def scrape_page_pdf_files(self, partid, results_pp=None):
        """
        Retrieves and returns all pdfs from a Green Book Live company
        search via generator. Note that we use a generator so that we
        only have to keep a single file in memory at a time.

        Parameters
        ----------
        part_id : int
            Some sort of search index for company search

        results_pp : int
            The number of search results returned in the response

        Returns
        -------
        generator
            A sequence of all downloaded pdfs represented as MemoryFiles
        """

        html = self.gbl_http_service.company_search(partid,
                                                    results_pp=results_pp)
        company_pdf_links = self.parser.extract_company_pdf_links(html)

        for company in company_pdf_links:
            for pdf_link in company_pdf_links[company]:
                pdf_file = self.gbl_http_service.get_file(pdf_link)
                pdf_file.dir_path = company
                yield pdf_file

