# Bekir_Faydaci_Ensembl_Assignment

## Introduction:
This tool allows you to:
    1) query the amino acid count at a specific sequence position, across transcripts in a given gene, or
    2) the mean count for each amino acid averaged across positions

## How to use this tool:
To run the tool from the command line:
$ python Bekir_Faydaci_Ensembl_Assignment.py -n <gene symbol> -p <start position> [-e <end position>]

## Options:
-n		    Gene symbol
-p		    (Start) position of the protein sequence
-e		    End position of the protein sequence
-h/--help	prints help message

## Example runs:
Bekir_Faydaci_Ensembl_Assignment.py -n BRCA2 -p 1

Bekir_Faydaci_Ensembl_Assignment.py -n BRCA2 -p 1 -e 100

## Dependencies:
python pip install request