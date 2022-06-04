import configparser
import os

from file_management.pdf_converter import PdfConverter

def get_pdf_name(root_path, file_name):
    return '/'.join([root_path, file_name])

def get_output_sub_path(input_root, input_path, input_file_name):
    input_sub_path = input_path.removeprefix(input_root)
    pdf_name_stem = input_file_name.removesuffix('.pdf')
    return '/'.join([input_sub_path, pdf_name_stem])

def main():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    input_directory = config['pdf.converter']['INPUT_DIRECTORY']
    output_directory = config['pdf.converter']['OUTPUT_DIRECTORY']
    min_accuracy = int(config['pdf.converter']['MIN_ACCURACY'])
    page_range = config['pdf.converter']['PAGE_RANGE']
    line_scale = int(config['pdf.converter']['LINE_SCALE'])
    table_regions = [config['pdf.converter']['TABLE_REGION']]

    pdf_converter = PdfConverter(output_directory, min_accuracy, page_range,
                                 line_scale, table_regions)

    for root_path, dir_names, file_names in os.walk(input_directory):
        for file_name in file_names:
            pdf_name = get_pdf_name(root_path, file_name)
            output_sub_path = get_output_sub_path(input_directory,
                                                  root_path,
                                                  file_name)

            pdf_converter.convert_pdf(pdf_name, output_sub_path)

if __name__ == '__main__':
    main()
