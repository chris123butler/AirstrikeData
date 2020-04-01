# import libraries
from glob import glob
import pandas as pd
import PyPDF2
import re
import datetime
from dateutil.parser import parse
import requests
import io
import nltk

nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import wordnet as wn
from nltk import word_tokenize
from nltk.tokenize import sent_tokenize
from word2number import w2n


# given the file path, opens a file from local machine and returns a string
def text_from_file(file):
    with open(file, 'rb') as raw_file:
        pdf_reader = PyPDF2.PdfFileReader(raw_file)
        num_pages = pdf_reader.getNumPages()
        full_text = ''
        for x in range(num_pages):  # concatenates all pages
            full_text += pdf_reader.getPage(x).extractText()

    full_text = full_text.replace('\n', '').replace(' a ', ' 1 ').replace(' an ', ' 1 ').replace(' the ', ' 1 ').lower()
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

    full_text = full_text.replace('\n', '').replace(' a ', ' 1 ').replace(' an ', ' 1 ').replace(' the ', ' 1 ').lower()
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


# creates a list of tuples based on interesting data items
def strike_results_from(text):
    sentences = sent_tokenize(text)
    relevant = find_relevant(sentences)
    country = None
    results = []

    for sentence in sentences:
        if 'syria' in sentence:
            country = 'syria'
        if 'iraq' in sentence:
            country = 'iraq'
        if sentence in relevant:
            location = None
            num_strikes = None
            subtrees = [x for x in chunk(sentence) if type(x).__name__ == 'Tree']
            for tree in subtrees:
                if tree.label() == 'location':
                    location = ''
                    for x in list(tree)[1:]:
                        location += x[0] + ' '
                    location = location.strip()
                if tree.label() == 'numbered_item':
                    try:
                        num_strikes = w2n.word_to_num(tree[0][0])
                    except ValueError:
                        continue
                if tree.label() == 'result_list':
                    action = tree[0][0]  # take the leading verb
                    targets = tree[1:]  # take the list of targets
                    for target in targets:  # for each target
                        try:
                            count = w2n.word_to_num(target[0][0])  # take the leading number
                        except ValueError:
                            continue
                        target_string = ''
                        for x in target[1:]:
                            target_string += x[0] + ' '
                        target_string = target_string.replace('and', '').replace(',', '').strip()
                        data_tuple = [None, None, None, None, None, None]
                        data_tuple[0] = country
                        data_tuple[1] = location
                        data_tuple[2] = num_strikes
                        data_tuple[3] = action
                        data_tuple[4] = count
                        data_tuple[5] = target_string
                        results.append(data_tuple)

    return results


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


# breaks down a sentence into chunks corresponding to our data columns
def chunk(sentence):
    tagged = nltk.pos_tag(word_tokenize(sentence))

    patterns = r"""
        numbered_item: {<CD|DT><NN|NNS>?<IN>?<NN|NNS|RB|JJ|VBG|CC>*<VBD|VBN>*<NN|NNS|RB|JJ|VBG|CC>+<,|CC>*}
        result_list: {<VBD|VBN><numbered_item>+}
        location: {<IN><JJ>*<NN>+}
    """

    cp = nltk.RegexpParser(patterns)
    result = cp.parse(tagged)
    # result.draw()
    # print(result)
    return result


# selects only sentences that contain words relevant to out search
def find_relevant(sentences):
    relevant = [sentence for sentence in sentences if ('destroyed' in sentence
                                                       or 'damaged' in sentence
                                                       or 'targeted' in sentence
                                                       or 'engaged' in sentence)]

    return relevant


# given a list of files and a destination path, returns a populated dataframe and writes it to a csv file
# useful for experimentation on a small number of local files
def data_from_files(files, path):
    data = {'Release Number': [],
            'URL': [],
            'Report Date': [],
            'Country': [],
            'Location': [],
            'Number of Strikes': [],
            'Action': [],
            'Number of Units': [],
            'Unit': [],
            'Flagged': [],
            'Initials': []}

    for file in files:
        text = text_from_file(file)
        date = date_from(text)
        release_number = release_number_from(text)
        results = strike_results_from(text)
        for result in results:
            data['Release Number'].append(release_number)
            data['URL'].append(file)
            data['Report Date'].append(date)
            data['Country'].append(result[0])
            data['Location'].append(result[1])
            data['Number of Strikes'].append(result[2])
            data['Action'].append(result[3])
            data['Number of Units'].append(result[4])
            data['Unit'].append(result[5])
            data['Flagged'].append(None)
            data['Initials'].append(None)

    data = create_and_save_dataframe(data, path)
    return data


# given a single url and a dictionary, appends the data extracted to the passed dictionary
def data_from_url(url, d):
    print(url)
    try:
        text = text_from_url(url)
    except PyPDF2.utils.PdfReadError:
        print("****[ERROR WITH URL] " + url)
        return

    date = date_from(text)
    rel = release_number_from(text)
    results = strike_results_from(text)

    for result in results:
        d['Release Number'].append(rel)
        d['URL'].append(url)
        d['Report Date'].append(date)
        d['Country'].append(result[0])
        d['Location'].append(result[1])
        d['Number of Strikes'].append(result[2])
        d['Action'].append(result[3])
        d['Number of Units'].append(result[4])
        d['Unit'].append(result[5])
        d['Flagged'].append(None)
        d['Initials'].append(None)

    return
