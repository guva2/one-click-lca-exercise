import camelot
import os

EXCEL_SUFFIX = '.xlsx'


class PdfConverter():
    """
    A class that converts pdf files to excel sheets

    Note that the output excel sheets are not formatted. This would
    probably be worth prettifying if we expected these spreadsheets
    to be used by humans.

    Attributes
    ----------
    output_directory : str
        the directory to which all files are to be written
    min_accuracy : int
        the lower bound for exported table accuracy
    page_range : str
        the range of pages to extract tables from
    line_scale : int
        the camelot line scaling factor
    table_regions : list
        the list of regions where tables may reside on the input pdfs


    Methods
    -------
    convert_pdf(pdf_path, sub_path)
        reads a pdf and exports all its tables to excel sheets
    """

    def __init__(self, output_directory, min_accuracy, page_range,
                 line_scale, table_regions):
        """
        Parameters
        ----------
        output_directory : str
            the directory to which all files are to be written
        min_accuracy : int
            the lower bound for exported table accuracy
        page_range : str
            the range of pages to extract tables from
        line_scale : int
            the camelot line scaling factor
        table_regions : list
            the list of regions where tables may reside on the input pdfs
        """

        self.output_directory = output_directory
        self.min_accuracy = min_accuracy
        self.page_range = page_range
        self.line_scale = line_scale
        self.table_regions = table_regions

    def convert_pdf(self, pdf_path, target_sub_path):
        """
        Parameters
        ----------
        pdf_path : str
            the path to the pdf file to be converted
        target_sub_path : str
            the sub path to which the excel sheets will be written
        """

        print('Extracting tables from {}...'.format(pdf_path))
        tables = camelot.read_pdf(pdf_path, pages=self.page_range,
                                  line_scale=self.line_scale,
                                  table_regions=self.table_regions)

        useful_tables = filter(self.__is_table_useful, tables)
        for i, table in enumerate(useful_tables):
            table_name = '{:03d}'.format(i)
            self.__export_table(table, target_sub_path, table_name)

    def __is_table_useful(self, table):
        is_table_accurate = table.accuracy > self.min_accuracy
        first_row_not_empty = table.df.iloc[0].any()
        return is_table_accurate and first_row_not_empty

    def __export_table(self, table, sub_path, table_name):
        file_path = '/'.join([self.output_directory, sub_path, table_name])
        file_path += EXCEL_SUFFIX
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        table.to_excel(file_path)
