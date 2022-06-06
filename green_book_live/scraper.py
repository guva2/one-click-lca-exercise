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

    def scrape_all_pdf_files(self, partid, results_pp=50):
        """
        Retrieves and returns all pdfs across all pages from a Green
        Book Live company search via generator. Note that we use a
        generator so that we only have to keep a single file in memory
        at a time. Pagination is handled by incrementing from_ and
        iterating until Green Book Live responds with an empty search
        results page.

        Note that the green book live site caps the number of returned
        companies to 50, so this is our upper bound.

        Parameters
        ----------
        part_id : int
            Some sort of search index for company search
        results_pp : int
            The number of search results returned on each page

        Returns
        -------
        generator
            A sequence of all downloaded pdfs represented as MemoryFiles
        """

        company_pdf_links = {}
        from_ = 0

        new_company_pdf_links = self.__get_pdf_links(partid, from_, results_pp)
        while new_company_pdf_links:
            company_pdf_links.update(new_company_pdf_links)
            from_ += results_pp
            new_company_pdf_links = self.__get_pdf_links(partid, from_,
                                                         results_pp)
        return self.__generate_pdf_files(company_pdf_links)


    def scrape_page_pdf_files(self, partid, from_=0, results_pp=None):
        """
        Retrieves and returns the pdfs from a Green Book Live company
        search paeg via generator. Note that we use a generator so that
        we only have to keep a single file in memory at a time.

        Parameters
        ----------
        part_id : int
            Some sort of search index for company search
        from_: int
            The company index from which to start the search
        results_pp : int
            The number of search results returned in the response

        Returns
        -------
        generator
            A sequence of all downloaded pdfs represented as MemoryFiles
        """

        company_pdf_links = self.__get_pdf_links(partid, from_, results_pp)
        return self.__generate_pdf_files(company_pdf_links)


    def __get_pdf_links(self, partid, from_, results_pp):
        html = self.gbl_http_service.company_search(partid,
                                                    from_=from_,
                                                    results_pp=results_pp)
        return self.parser.extract_company_pdf_links(html)

    def __generate_pdf_files(self, company_pdf_links):
        for company in company_pdf_links:
            for pdf_link in company_pdf_links[company]:
                pdf_file = self.gbl_http_service.get_file(pdf_link)
                if pdf_file:
                    pdf_file.dir_path = company
                    yield pdf_file
