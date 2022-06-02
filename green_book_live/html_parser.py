from bs4 import BeautifulSoup

#TODO: move these to config
COMPANY_HEADER = 'Company'
CERT_NO_HEADER = 'Cert. No.'

class CompanySearchHtmlParser:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')
        self.company_pdf_links = {}

    def get_company_pdf_links(self):
        if not self.company_pdf_links:
            table = self.soup.find(id='search-results')
            company_index, cert_no_index = self.__extract_column_indices(table)
            for row in table.find_all('tr'):
                self.__parse_row(row, company_index, cert_no_index)

        return self.company_pdf_links

    def __extract_column_indices(self, table):
        headers = [h.get_text().strip() for h in table.find_all('th')]
        return (headers.index(COMPANY_HEADER), headers.index(CERT_NO_HEADER))

    def __parse_row(self, row, company_index, cert_no_index):
        cells = row.find_all('td')
        if cells and len(cells) > max(company_index, cert_no_index):
            company = cells[company_index].get_text().strip()
            pdf_link_cell = cells[cert_no_index]
            pdf_links= self.__parse_pdf_links(pdf_link_cell)
            self.company_pdf_links[company] = pdf_links

    def __parse_pdf_links(self, pdf_link_cell):
        pdf_links= []
        raw_pdf_links = pdf_link_cell.find_all('a', href=True)
        return [self.__format_pdf_link(link) for link in raw_pdf_links]

    def __format_pdf_link(self, raw_pdf_link):
        relative_pdf_link = raw_pdf_link.get('href').strip()
        return relative_pdf_link.replace('../', '')
