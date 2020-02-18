#! /usr/bin/env python3

import sys
import argparse
import requests
from collections import Counter


def fetch_data(server, ext):
    """
        This function is used to fetch data from the server and raises an exception when the request fails (http /
        connection / time out error).
        server: url root
        ext:    url extension
        return: JSON file with fetched data
    """
    try:
        r = requests.get(server + ext, headers={"Content-Type": "application/json"})
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        sys.exit(e)
    return r.json()


def get_count_data(args):
    """
        This function is used to process the requested data and output a table with either:
            1) amino acid count across transcripts on a specific position
            2) mean count of amino acids averaged across a sequence position range
        args:
            args.gene_symbol:       gene symbol
            args.start_position:    used to specify the single position (1) or start position of a range (2)
            args.end_position:      used to specify the end position of the range (2)
    """
    # Initializing start and end indices
    start_index = args.start_position - 1
    # if args.end_position is not None:
    #     end_index = args.end_position - 1

    # Fetch lookup symbol endpoint API
    server = "http://rest.ensembl.org"
    ext_lookup_symbol = "/lookup/symbol/homo_sapiens/" + args.gene_symbol + "?expand=1"
    get_lookup_symbol = fetch_data(server, ext_lookup_symbol)

    # Get stable id and fetch sequence id endpoint API to get amino acid sequence of all protein coding transcripts
    stable_id = get_lookup_symbol['id']
    ext_sequence_id = "/sequence/id/" + stable_id + "?multiple_sequences=1;type=protein"
    get_sequence_id = fetch_data(server, ext_sequence_id)

    # If there is no range [-e] supplied, get count table for a single position
    if args.end_position is None:
        aa_list = []
        try:
            for transcripts in range(len(get_sequence_id)):
                if len(get_sequence_id[transcripts]['seq']) > start_index:
                    aa_list.append(get_sequence_id[transcripts]['seq'][start_index])

            # Count amino acids
            aa_count = Counter(aa_list).most_common()

            # Print output
            if len(aa_count) is not 0:
                print("Fetching results for: " + args.gene_symbol, stable_id, "\nAt position: " + str(args.start_position) +
                      "\nAA \tCount \n-- \t-----")
                for aa, count in aa_count:
                    print(aa + "\t" + str(count))
                print("The amino acid with the highest count is " + str(aa_count[0][0]) + ", with a frequency of " +
                      str(aa_count[0][1]) + ".")
                if len(get_sequence_id) is not len(aa_list):
                    print("Some of the transcripts are out of range at this position, only " + str(len(aa_list)) + "/" +
                          str(len(get_sequence_id)) + " transcripts are shown.")
            else:
                print("Are you sure that " + args.gene_symbol + " has position " + str(args.start_position) + "?")

        except Exception as e:
            print(e)

    # If an end position [-e] is given, get mean count for each amino acid averaged across positions
    else:
        aa_range_list = []
        aa_range = range(start_index, args.end_position)  # -p -e

        try:
            for transcripts in range(len(get_sequence_id)):
                for position in aa_range:  # range(start_index, args.end_position)):
                    if len(get_sequence_id[transcripts]['seq']) > args.end_position:
                        aa_range_list.append(get_sequence_id[transcripts]['seq'][position])

            # Count amino acids
            aa_count = Counter(aa_range_list).most_common()

            # Print output
            if len(aa_count) is not 0:
                print("Fetching results for: " + args.gene_symbol, stable_id + "\nSelected range: " +
                      str(args.start_position) + " - " + str(args.end_position) + "\nAA \tMean count \n-- \t--------")
                sum_mean_count = 0
                for aa, count in aa_count:
                    mean_count = count / len(aa_range)
                    print(aa + "\t" + str(mean_count))
                    sum_mean_count = sum_mean_count + mean_count
                print("\nThe amino acid with highest mean count is " + str(aa_count[0][0]) + ", with a mean count value of "
                      + str(aa_count[0][1]) + ". \nThe sum of mean counts is " + str(sum_mean_count) + ".")

                n_transcripts_in_range = int(len(aa_range_list)/len(aa_range))
                if len(get_sequence_id) is not n_transcripts_in_range:
                    print("Some of the transcripts are out of range at this position, only " +
                          str(n_transcripts_in_range) + "/" + str(len(get_sequence_id)) + " transcripts are shown.")
            else:
                print("Are you sure that " + args.gene_symbol + " covers the range " + str(args.start_position) + "-" +
                      str(args.end_position) + "?")

        except BaseException as e:
            print(e)

    sys.exit("Terminating script ...")


def parse_arguments():
    """
        This function parses the input flags that were given in the command line. The input flags consist of the gene
        symbol, start position of the desired protein sequence, and optionally the end position of this sequence.

    """
    parser = argparse.ArgumentParser(description='Bekir Faydaci - Programming Assignment EMBL-EBI Ensembl: '
                                                 'A tool to query the amino acid count on a specific sequence position '
                                                 'across all protein coding transcripts or the mean count of each '
                                                 'amino acid averaged across a sequence range.')
    parser.add_argument('-n', dest='gene_symbol', type=str, help='Gene symbol', required=True)
    parser.add_argument('-p', dest="start_position", type=int, help='(Start) position of the protein sequence',
                        required=True)
    parser.add_argument('-e', dest='end_position', type=int, help='End position of the protein sequence', required=False)
    parser.set_defaults(func=get_count_data)
    args = parser.parse_args()
    args.func(args)


# Start script
parse_arguments()
