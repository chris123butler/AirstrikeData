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

# nltk.download('wordnet') # lemmatization
nltk.download('punkt') # sentence tokenization
nltk.download('averaged_perceptron_tagger') # pos tagging
# from nltk.corpus import wordnet as wn
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
    # removes newlines(there are a lot for some reason)
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
    release_number = re.search(r'\d{7,8}-?\d*', text)

    try:
        release_number = release_number.group()
    except AttributeError:
        return None

    return release_number


# creates a list of lists(matrix) based on interesting data items
def strike_results_from(text):
    sentences = sent_tokenize(text)
    relevant = find_relevant(sentences)
    country = None
    l = []

    for sentence in sentences:
        if 'syria' in sentence:
            country = 'syria'
        if 'iraq' in sentence:
            country = 'iraq'
        if sentence in relevant:
            location = None
            num_strikes = None
            subtrees = [x for x in chunk(sentence) if type(x).__name__ == 'Tree']
            results_not_found = True
            for tree in subtrees:
                if tree.label() == 'location':
                    location  = ' '.join([x[0] for x in tree[1:]]).strip()
                if tree.label() == 'numbered_item' and (tree[1][0] in ['strike', 'strikes', 'airstrikes']):
                    try:
                        num_strikes = w2n.word_to_num(tree[0][0])
                    except ValueError:
                        continue
                if tree.label() == 'result_list':
                    action = None
                    action = tree[0][0] # take the leading verb
                    targets = tree[1:] # take the list of targets
                    for target in targets: # for each target
                        try:
                            count = w2n.word_to_num(target[0][0]) #take the leading number
                        except ValueError:
                            continue
                        holding_list = [x[0] for x in target[1:]]
                        holding_list.reverse()
                        for word in holding_list:
                            if word in [',', 'and']:
                                holding_list.remove(word)
                            else:
                                break
                        holding_list.reverse()
                        holding_list = [x for x in holding_list if x not in ['isis', 'isil']]
                        target_string = ' '.join(holding_list)
                        if target_string in ['strikes', 'strike', 'airstrikes']:
                            try:
                                num_strikes = w2n.word_to_num(target[0][0])
                                continue
                            except ValueError:
                                continue
                        results_not_found = False
                        data_tuple = [None, None, None, None, None, None]
                        data_tuple[0] = country
                        data_tuple[1] = location
                        data_tuple[2] = num_strikes
                        data_tuple[3] = action
                        data_tuple[4] = count
                        data_tuple[5] = target_string
                        l.append(data_tuple)
            if results_not_found:
                data_tuple = [country, location, num_strikes, None, None, None]
                l.append(data_tuple)

    return(l)


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
        location: {<IN><JJ>*<NN|VBN>+}
    """

    cp = nltk.RegexpParser(patterns)
    result = cp.parse(tagged)
    return result


# selects only sentences that contain words relevant to out search
def find_relevant(sentences):
    relevant = [sentence for sentence in sentences if ('destroyed' in sentence
                                                    or 'damaged' in sentence
                                                    or 'targeted' in sentence
                                                    or 'engaged' in sentence
                                                    or 'struck' in sentence)]

    return relevant


# strips html tags from a list of strings
def strip_tags(strings):
    stripped = [re.sub('<[^<]+?>', ' ', x) for x in strings]

    return stripped

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
        # d['Flagged'].append(fails_sanity_checks(rel, url, date, result[0], result[1],
        #                                         result[2], result[3], result[4], result[5]))
        d['Flagged'].append(None)
        d['Initials'].append(None)

    return


# gets data from a string, assuming the string represents text of a strike report
def data_from_text(s, d):
    url = 'https://dod.defense.gov/oir/airstrikes/'
    date = date_from(s)
    rel = None
    results = strike_results_from(s)

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
        # d['Flagged'].append(fails_sanity_checks(rel, url, date, result[0], result[1],
        #                                         result[2], result[3], result[4], result[5]))
        d['Flagged'].append(None)
        d['Initials'].append(None)

    return


# this method has access to the data for each row. Returns a flagged message if the data fail sanity checks,
# returns None if the data pass all sanity checks
def fails_sanity_checks(release, url, date, country, location, strikes, action, number, unit):
    flagged_message = 'FLAGGED'
    if (release.equals(None) and not(date.year.equals(2014)) or
            url.equals(None) or
            date.equals(None) or
            country.equals(None) or
            location.equals(None) or
            strikes.equals(None) or
            action.equals(None) or
            number.equals(None) or
            unit.equals(None)):
        return flagged_message

    return None
