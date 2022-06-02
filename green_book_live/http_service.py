from file_management.memory_file import MemoryFile

import requests

#TODO: store default values in config file and/or accept them as varargs
GREEN_BOOK_LIVE_BASE_URL = 'https://www.greenbooklive.com/'
COMPANY_SEARCH_PATH = 'search/companysearch.jsp'
DEFAULT_PART_ID = 10028
DEFAULT_ID = 260
DEFAULT_RESULTS_PER_PAGE = 50
 
 
class GBLHttpService:
    def __init__(self):
        #TODO: setup base url here probably
        pass

    #TODO: figure out which parameters are required
    def company_search(self, from_=0, partid=DEFAULT_PART_ID, companyName='',
                       productName='', productType='', certNo='', regionId=0,
                       countryId=0, addressPostcode='', certBody='',
                       id_=DEFAULT_ID, results_pp=DEFAULT_RESULTS_PER_PAGE,
                       sortResultsComp=''):
        payload = {
            'from': from_,
            'partid': partid,
            'companyName': companyName,
            'productName': productName,
            'productType': productType,
            'certNo': certNo,
            'regionId': regionId,
            'countryId': countryId,
            'addressPostcode': addressPostcode,
            'certBody': certBody,
            'id': id_,
            'results_pp': results_pp,
            'sortResultsComp': ''
        }

        return self._http_get(COMPANY_SEARCH_PATH, payload)

    def get_file(self, path, payload={}):
        file_name = path.split('/')[-1]
        file_content = self._http_get(path, payload)
        return MemoryFile(file_name, file_content)

    def _http_get(self, path, payload={}):
        url = GREEN_BOOK_LIVE_BASE_URL + path
        response = requests.get(url, payload)
        return response.content
