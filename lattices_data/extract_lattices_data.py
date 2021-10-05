import requests
import re
import numpy as np
import json


def get_NAME(site_return):
    initial_str = '<a NAME="NAME"><STRONG>NAME</STRONG></a><br>'
    final_str = '<br><p><li>'
    initial_index = site_return.find(initial_str)+len(initial_str)
    final_index = initial_index + site_return[initial_index:].find(final_str)

    return site_return[initial_index:final_index]


def get_DIMENSION(site_return):
    if '<a NAME="DIMENSION"><STRONG>DIMENSION</STRONG></a><br>' in site_return:
        initial_str = '<a NAME="DIMENSION"><STRONG>DIMENSION</STRONG></a><br>'
    elif '<a NAME="DIM"><STRONG>DIM</STRONG></a><br>' in site_return:
        initial_str = '<a NAME="DIM"><STRONG>DIM</STRONG></a><br>'
    else:
        return ''

    final_str = '<br><p><li>'
    initial_index = site_return.find(initial_str)+len(initial_str)
    final_index = initial_index + site_return[initial_index:].find(final_str)

    return int(site_return[initial_index:final_index])


def get_DET(site_return):
    if '<a NAME="DET"><STRONG>DET</STRONG></a><br>' in site_return:
        initial_str = '<a NAME="DET"><STRONG>DET</STRONG></a><br>'
    else:
        return ''
    final_str = '<br><p><li>'
    initial_index = site_return.find(initial_str)+len(initial_str)
    final_index = initial_index + site_return[initial_index:].find(final_str)

    return float(site_return[initial_index:final_index])


def get_MINIMAL_NORM(site_return):
    if '<a NAME="MINIMAL_NORM"><STRONG>MINIMAL_NORM</STRONG></a><br>' in site_return:
        initial_str = '<a NAME="MINIMAL_NORM"><STRONG>MINIMAL_NORM</STRONG></a><br>'
    else:
        return ''
    final_str = '<br><p><li>'
    initial_index = site_return.find(initial_str)+len(initial_str)
    final_index = initial_index + site_return[initial_index:].find(final_str)

    return float(site_return[initial_index:final_index])


def get_KISSING_NUMBER(site_return):
    if '<a NAME="KISSING_NUMBER"><STRONG>KISSING_NUMBER</STRONG></a><br>' in site_return:
        initial_str = '<a NAME="KISSING_NUMBER"><STRONG>KISSING_NUMBER</STRONG></a><br>'
    else:
        return ''
    final_str = '<br><p><li>'
    initial_index = site_return.find(initial_str)+len(initial_str)
    final_index = initial_index + site_return[initial_index:].find(final_str)

    return int(site_return[initial_index:final_index])


def get_BASIS(site_return):
    if '<a NAME="BASIS"><STRONG>BASIS</STRONG></a><br>' in site_return:
        initial_str = '<a NAME="BASIS"><STRONG>BASIS</STRONG></a><br>'
    else:
        return ''
    final_str = '<br><p><li>'
    initial_index = site_return.find(initial_str)+len(initial_str)
    final_index = initial_index + site_return[initial_index:].find(final_str)

    numeric_const_pattern = '[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
    rx = re.compile(numeric_const_pattern, re.VERBOSE)

    numbers = [float(s) for s in rx.findall(
        site_return[initial_index:final_index])]
    num_row = int(numbers[0])
    num_columns = int(numbers[1])

    gen_matrix = np.array(numbers[2:]).reshape(num_row, num_columns)

    return {'num_vectors': num_row, 'len_vectors': num_columns, 'gen_matrix': gen_matrix.tolist()}


def get_GRAM(site_return):
    if get_BASIS(site_return)['gen_matrix']:
        matrix = np.array(get_BASIS(site_return)['gen_matrix']).reshape(
            get_BASIS(site_return)['num_vectors'], get_BASIS(site_return)['len_vectors'])
        gram = matrix.dot(matrix.transpose())
        return gram.tolist()
    else:
        return ''


def requested_lattices():
    print('type the list of lattices you want (to finish type "end"). ')
    lattice = input()
    list_lattices = []
    while lattice != ('end' or 'END'):
        list_lattices.append(lattice)
        lattice = input()

    return list_lattices


def dictionary_import(list_lattices):
    dictionary = {}

    for lattice in list_lattices:
        response = requests.get(
            f'https://www.math.rwth-aachen.de/~Gabriele.Nebe/LATTICES/{lattice}.html'
        )
        site_return = str(response.content).replace('\\n', '')
        dictionary_lattice = {}
        properties_list = ['get_NAME', 'get_DIMENSION', 'get_DET',
                           'get_MINIMAL_NORM', 'get_KISSING_NUMBER', 'get_BASIS', 'get_GRAM']

        for propritie in properties_list:
            dictionary_lattice[propritie[4:]] = globals()[
                propritie](site_return)

        dictionary[lattice] = dictionary_lattice

    return dictionary


def json_export(dictionary):
    json_object = json.dumps(dictionary, indent=4)
    with open("lattices.json", "w") as outfile:
        outfile.write(json_object)


def main():

    #list_lattices = requested_lattices()
    json_export(dictionary_import(requested_lattices()))


if __name__ == "__main__":
    main()