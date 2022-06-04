from bs4 import BeautifulSoup

COMPANY_HEADER = 'Company'
CERT_NO_HEADER = 'Cert. No.'


class CompanySearchHtmlParser:
    """
    A parser that extracts pdf links from a company search results page.

    Note that the link extraction could be made more robust with a web
    driver. The linked pdfs use relative paths, and this implementation
    simply ignores some details. If this site were to undergo changes
    to routing, this parser would break.

    Methods
    -------
    extract_company_pdf_links(html)
        Extracts all pdf links from a given company search HTML page
    """

    def __init__(self):
        self._processed_pdf_links = {}

    def extract_company_pdf_links(self, html):
        """
        Extracts all pdf links from a company search results page.

        Parameters
        ----------
        html : str
            A string representation of the html to be parsed

        Returns
        -------
        dict
            A dictionary mapping company names to their pdf links

        """

        company_pdf_links = {}
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find(id='search-results')
        company_index, cert_no_index = self.__extract_column_indices(table)
        for row in table.find_all('tr'):
            company, links = self.__parse_row(row,
                                              company_index,
                                              cert_no_index)
            if company and links:
                new_links = links - self._processed_pdf_links.get(company,
                                                                  set())
                company_pdf_links[company] = new_links
                self.__add_processed_pdf_links(company, new_links)
        return company_pdf_links

    def __extract_column_indices(self, table):
        headers = [h.get_text().strip() for h in table.find_all('th')]
        return (headers.index(COMPANY_HEADER), headers.index(CERT_NO_HEADER))

    def __parse_row(self, row, company_index, cert_no_index):
        cells = row.find_all('td')
        if cells and len(cells) > max(company_index, cert_no_index):
            company = cells[company_index].get_text().strip()
            pdf_link_cell = cells[cert_no_index]
            return (company, self.__parse_pdf_links(pdf_link_cell))
        return (None, None)

    def __parse_pdf_links(self, pdf_link_cell):
        pdf_links = []
        raw_pdf_links = pdf_link_cell.find_all('a', href=True)
        return {self.__format_pdf_link(link) for link in raw_pdf_links}

    def __format_pdf_link(self, raw_pdf_link):
        relative_pdf_link = raw_pdf_link.get('href').strip()
        return relative_pdf_link.replace('../', '')

    def __add_processed_pdf_links(self, company, pdf_links):
        if self._processed_pdf_links.get(company):
            self._processed_pdf_links[company].update(pdf_links)
        else:
            self._processed_pdf_links[company] = pdf_links
