from green_book_live.scraper import Scraper
from file_management.file_writer import FileWriter

import configparser


def main():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    base_url = config['scraper']['GREEN_BOOK_LIVE_BASE_URL']
    search_partid = int(config['scraper']['COMPANY_SEARCH_PARTID'])
    search_results_pp = int(config['scraper']['COMPANY_SEARCH_RESULTS_PP'])
    output_directory = config['scraper']['OUTPUT_DIRECTORY']

    scraper = Scraper(base_url)
    files = scraper.scrape_all_pdf_files(search_partid,
                                         results_pp=search_results_pp)
    file_writer = FileWriter(output_directory)
    file_writer.write_all(files)


if __name__ == '__main__':
    main()
