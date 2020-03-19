# import libraries
from glob import glob
import pandas as pd
import PyPDF2
import re
import datetime
from dateutil.parser import parse
import requests
import io


# given the file path, opens a file from local machine and returns a string
def text_from_file(file):
    with open(file, 'rb') as raw_file:
        pdf_reader = PyPDF2.PdfFileReader(raw_file)
        num_pages = pdf_reader.getNumPages()
        full_text = ''
        for x in range(num_pages):  # concatenates all pages
            full_text += pdf_reader.getPage(x).extractText()

    full_text = full_text.replace('\n', '')  # removes newlines(there are a lot for some reason)
    return full_text


# given the url, opens a file remotely and returns a string
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


# strips leading digits from dates
def remove_leading_digits(bad_date):
    good_date = ''
    for i in range(len(bad_date)):
        if bad_date[i].isalpha():
            good_date = bad_date[i:]
            break
        else:
            continue

    return good_date


# returns a datetime object from a string using regular expression
def date_from(text):
    date = re.search(r'\w+\.* \d+, \d{4}', text)
    try:
        dt_object = parse(date.group())  # parses found date into datetime object for consistent format
    except AttributeError:
        return None
    except ValueError:
        dt_object = parse(remove_leading_digits(date.group()))

    return dt_object


# returns a release number from a string using regular expression
def release_number_from(text):
    release_number = re.search(r'\d{8}', text)

    try:
        release_number = release_number.group()
    except AttributeError:
        return None

    return release_number


# takes in a dictionary and fills unused keys-values with enough Nones for consistent length
def fill_empty_values(dictionary):
    number = len(dictionary[list(dictionary.keys())[0]])
    for key in dictionary.keys():
        if len(dictionary[key]) == 0:
            dictionary[key] = [None] * number

    return dictionary


# creates a dataframe from a dictionary, saves the dataframe in the specified file path, and returns the dataframe
def create_and_save_dataframe(dictionary, dest_file):
    df = pd.DataFrame.from_dict(dictionary)
    df.to_csv(dest_file, index=None, header=True)

    return df


# given a list of files and a destination path, returns a populated dataframe and writes it to a csv file
# useful for experimentation on a small number of local files
def data_from_files(files, path):
    data = {'Release Number': [],
            'URL': [],
            'Report Date':  [],
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
