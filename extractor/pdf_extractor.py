# import libraries
from glob import glob
import pandas as pd
import PyPDF2
import re
import datetime
from dateutil.parser import parse
import requests
import io

urls = ['https://www.inherentresolve.mil/Portals/14/Documents/Strike%20Releases/2015/04April/1%20Apr%20Strike%20Release.pdf?ver=2017-01-13-131120-810',
       'https://www.inherentresolve.mil/Portals/14/Documents/Strike%20Releases/2015/07July/20150707%20Strike%20Release%20final.pdf?ver=2017-01-13-131141-437',
       'https://www.inherentresolve.mil/Portals/14/Documents/Strike%20Releases/2017/01January/20170125%20Strike%20Release%20Final.pdf?ver=2017-01-25-093917-853',
       'https://www.inherentresolve.mil/Portals/14/Documents/Strike%20Releases/2017/02February/20170203%20Strike%20Release%20Final.pdf?ver=2017-02-03-074516-280',
       'https://www.inherentresolve.mil/Portals/14/Documents/Strike%20Releases/2017/02February/20170217%20Strike%20Release%20Final.pdf?ver=2017-02-17-093725-800',
       'https://www.inherentresolve.mil/Portals/14/Documents/Strike%20Releases/2017/10October/20171023%20Strike%20Release.pdf?ver=2017-10-23-033103-287',
       'https://www.inherentresolve.mil/Portals/14/Documents/Strike%20Releases/2017/11November/20171103%20CJTF-OIR%20Strike%20Release.pdf?ver=2017-11-03-065958-837']


def text_from_file(file):
    with open(file, 'rb') as raw_file:
        pdf_reader = PyPDF2.PdfFileReader(raw_file)
        num_pages = pdf_reader.getNumPages()
        full_text = ''
        for x in range(num_pages):  # concatenates all pages
            full_text += pdf_reader.getPage(x).extractText()

    full_text = full_text.replace('\n', '')  # removes newlines(there are a lot for some reason)
    return full_text


def text_from_url(url):
    response = requests.get(url)
    with io.BytesIO(response.content) as raw_file:
        pdf_reader = PyPDF2.PdfFileReader(raw_file)
        num_pages = pdf_reader.getNumPages()
        full_text = ''
        for x in range(num_pages):
            full_text += pdf_reader.getPage(x).extractText()

    full_text = full_text.replace('\n', '')
    return full_text


def date_from(text):
    date = re.search("\w+\.* \d+, \d{4}", text)
    dt_object = parse(date.group())  # parses found date into datetime object for consistent format

    return dt_object


def release_number_from(text):
    release_number = re.search("\d{8}-?\d*", text)
    release_number = release_number.group()

    return release_number


# takes in a dictionary and fills unused keys-values with enough Nones for consistent length
def fill_empty_values(dict):
    number = len(dict[list(dict.keys())[0]])
    for key in dict.keys():
        if len(dict[key]) == 0:
            dict[key] = [None] * number

    return dict


# creates a dataframe from a dictionary, saves the dataframe in the specified file path, and returns the dataframe
def create_and_save_dataframe(dict, dest_file):
    df = pd.DataFrame.from_dict(dict)
    df.to_csv(dest_file, index=None, header=True)

    return df


# given a list of files and a destination path, returns a populated dataframe and writes it to a csv file
# useful for experimentation on a small number of local files
def data_from_files(files, path):
    data = {'Release Number': [],
            'URL': [],
            'Report Date': [],
            'Strike Date': [],
            'Number of Strikes': [],
            'Country': [],
            'Location': [],
            'Targeted': [],
            'Unit': [],
            'Number of Units': [],
            'Detroyed': [],
            'Flagged': [],
            'Initials': []}

    for file in files:
        text = text_from_file(file)
        date = date_from(text)
        release_number = release_number_from(text)
        data['Release Number'].append(release_number)
        data['URL'].append(file)
        data['Report Date'].append(date)

    data = fill_empty_values(data)
    data = create_and_save_dataframe(data, path)
    return data


# given a list of urls and a destination path, returns a populated dataframe and writes it to a csv file
def data_from_urls(urls, path):
    data = {'Release Number': [],
            'URL': [],
            'Report Date': [],
            'Strike Date': [],
            'Number of Strikes': [],
            'Country': [],
            'Location': [],
            'Targeted': [],
            'Unit': [],
            'Number of Units': [],
            'Detroyed': [],
            'Flagged': [],
            'Initials': []}

    for url in urls:
        print(url)
        try:
            text = text_from_url(url)
        except PyPDF2.utils.PdfReadError:
            continue
        date = date_from(text)
        release_number = release_number_from(text)
        data['Release Number'].append(release_number)
        data['URL'].append(url)
        data['Report Date'].append(date)

    data = fill_empty_values(data)
    data = create_and_save_dataframe(data, path)
    return data
