import os, sys
import nlp_preprocess
import math

def create_corpus():

    data_files = collect_files('data')
    # Collect data of each file
    doc_info = []
    i = 0
    for file in data_files:
        words, stems, lemmas, word_count = nlp_preprocess.preprocess_text(file)

        i += 1
        count = word_count
        temp = {'doc_id': i, 'doc_length': word_count}
        doc_info.append(temp)

    i = 0
    freqDict_list = []
    for file in data_files:
        i += 1
        freq_dict = {}
        words = words
        for word in words:
            if word in freq_dict:
                freq_dict[word] += 1
            else:
                freq_dict[word] = 1
            temp = {'doc_id': i, 'freq_dict': freq_dict}

        freqDict_list.append(temp)

    #computeTF(doc_info, freqDict_list)
    computeIDF(doc_info, freqDict_list)


    #with open('doc_info.txt', 'w') as file:
    #    file.write(doc_info)

    #with open('freqDict_list.txt', 'w') as file:
    #    file.write(freqDict_list)



def computeTF(doc_info, freqDict_list):
    # TF = frequency of a term in the doc / total number of terms in the doc


    TF_scores = []
    for tempDict in freqDict_list:
        id = tempDict['doc_id']
        for k in tempDict['freq_dict']:
            temp = {'doc_id': id,
                    'TF_score': tempDict['freq_dict'][k]/doc_info[id-1]['doc_length'],
                    'key': k}
            TF_scores.append(temp)

    print(TF_scores)
    return TF_scores

def computeIDF(doc_info, freqDict_list):
    # IDF = total number of docs / number of docs with term in it
    IDF_scores = []
    counter = 0
    for dict in freqDict_list:
        counter += 1
        for k in dict['freq_dict'].keys():
            count = sum([k in tempDict['freq_dict'] for tempDict in freqDict_list])
            temp = {'doc_id': counter, 'IDF_score': math.log(len(doc_info)/count), 'key': k}

            IDF_scores.append(temp)

    print(IDF_scores)
    return IDF_scores







def collect_files(directory):
    # Collect all the filenames and paths to use in corpus
    data_files = []

    for dirpath, _, files in os.walk(directory):
        for filename in files:
            if filename == 'body.txt':
                data_files.append(os.path.join(dirpath, filename))

    return data_files





if __name__ == '__main__':
    create_corpus()