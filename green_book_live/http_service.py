from file_management.memory_file import MemoryFile

import requests

COMPANY_SEARCH_PATH = 'search/companysearch.jsp'
 
class GBLHttpService:
    """
    A service that handles http interactions with GreenBookLive.

    Note that this Service could be improved with better error handling.
    Since we are scraping a site, we don't have any contracts/guarantees
    with regard to error codes, formatting, etc. This implementation
    could benefit from stronger error handling, monitoring, and logging
    before being deployed in practice.

    Attributes
    ----------
    base_url : str
        the root url to which HTTP requests will be made

    Methods
    -------
    company_search(self, partid, from_=0, result_pp='', companyName='',
                   productName='', productType='', certNo='',
                   regionId=0, countryId=0, addressPostcode='',
                   certBody='', id_=0, sortResultsComp='')
        executes a company search and returns the html response content

    get_file(self, path, payload={})
        retrieves a file and returns it wrapped as a MemoryFile
    """

    def __init__(self, base_url):
        """
        Parameters
        ----------
        base_url: str
            the root url to which HTTP request will be made
        """

        self.base_url = base_url

    def company_search(self, partid, from_=0, results_pp='', companyName='',
                       productName='', productType='', certNo='', regionId=0,
                       countryId=0, addressPostcode='', certBody='',
                       id_=0, sortResultsComp=''):
        """
        Executes a company search on Green Book Live and returns the
        html response content.

        Parameters
        ----------
        partid : int
            Some sort of search index
        from_ : int
            The index of the company from which we want to start
            searching, useful for pagination
        results_pp : int
            The number of companies to show per request (this number
            is truncated to 50 on the server side)

        Unclear what the other parameters explicitly do, but presumably
        they offer filtering and sorting functionality for a search

        Returns
        -------
        str
            A string representation of the response HTML page
        """

        payload = {
            'partid': partid,
            'from': from_,
            'results_pp': results_pp,
            'companyName': companyName,
            'productName': productName,
            'productType': productType,
            'certNo': certNo,
            'regionId': regionId,
            'countryId': countryId,
            'addressPostcode': addressPostcode,
            'certBody': certBody,
            'id': id_,
            'sortResultsComp': ''
        }

        return self._http_get(COMPANY_SEARCH_PATH, payload)

    def get_file(self, path, payload={}):
        """
        Retrieves and returns a file from Green Book Live.

        Parameters
        ----------
        path : str
            The url path to the file

        Returns
        -------
        bytes
            A byte represention of the response file.
        """

        file_name = path.split('/')[-1]
        file_content = self._http_get(path, payload)
        return MemoryFile(file_name, file_content)

    def _http_get(self, path, payload={}):
        url = self.base_url + path
        print("Executing GET Request at: %s" % url) 
        response = requests.get(url, payload)
        return response.content
