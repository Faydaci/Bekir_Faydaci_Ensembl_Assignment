# Bekir Faydaci Ensembl Assignment

## Introduction:
This tool allows you to: <br>
    1) Query the amino acid count at a specific protein sequence position, across transcripts in a given gene. <br>
    2) Query the mean count for each amino acid averaged across a protein sequence range, in a given gene.

## How to use this tool:
To run the tool from the command line, enter: <br>
$ python bekir_faydaci_ensembl_assignment.py -s &lt;gene_symbol&gt; -p &lt;start_position&gt; [-e &lt;end_position&gt;]

## Options:
|Flags |Description|
|:----------|:--------------------------------------------------------------|
| -s | Gene symbol |
| -p | (Start) position of the protein sequence |
| -e | End position of the protein sequence (this position included) |
| -h/--help | Prints help message |

## Example runs:
$ python bekir_faydaci_ensembl_assignment.py -s BRCA2 -p 1

	Fetching data for: BRCA2
    At position: 1
    AA 	Count
    -- 	-----
    M	5.0
    X	2.0
    S	1.0
    V	1.0

    The amino acid with the highest count is M, with a count of 5.

$ python bekir_faydaci_ensembl_assignment.py -s BRCA2 -p 1 -e 100

    Fetching data for: BRCA2
    At range: 1 - 100
    AA 	Mean count
    -- 	----------
    S	0.52
    L	0.46
    P	0.43
    K	0.41
    E	0.39
    T	0.27
    Q	0.27
    I	0.26
    F	0.26
    N	0.24
    V	0.24
    A	0.23
    D	0.2
    G	0.18
    R	0.16
    Y	0.16
    C	0.1
    H	0.1
    M	0.05
    W	0.05
    X	0.02

    The amino acid with highest mean count is S, with a mean count of 0.52.
    Some of the transcripts are out of range at the specified position,
	only the data for 5/9 transcripts are shown.


## Dependencies:
The tool depends on the python module requests, to install this module enter the following line into the terminal: <br>
$ python pip install requests <br><hr> Bekir Faydaci 20/02/2020
