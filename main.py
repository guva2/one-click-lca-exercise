from green_book_live.scraper import Scraper
from file_management.file_writer import FileWriter

def main():
    scraper = Scraper()
    pdf_files = scraper.scrape_page_pdf_files()
    file_writer = FileWriter()
    file_writer.write_all(pdf_files)

if __name__ == '__main__':
    main()
