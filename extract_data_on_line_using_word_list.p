#!/usr/bin/env python
# extract_data_on_line_using_word_list.py by Wayne Decatur
# ver 0.1
#
#*******************************************************************************
# USES Python 2.7 but should be convertable via 2to3, see https://docs.python.org/3.0/library/2to3.html
#
# PURPOSE: Takes a file of words or names (could be gene identifiers, etc.) and
# then examines another file line by line and only keeps the lines in that file
# that contain the words or names the user provided.
# The impetus for this to take a list of genes made using YeastMine and then
# extract lines from data on genes for just the provided list of genes.
# However, it is written more general than that to handle any sort of words and
# then to keep lines in the "data file" that contain those words.
# 
# In the file that provides the word/name list, the list can be in almost any
# form, for example each word or name on a separate line or simplu seperated by 
# a comma or orther punctuation or a mixture. By default spaces will be taken 
# as the separation of words/names. If you'd like to specify that individual
# lines are the basic unit so that you can use more complex names or identifiers 
# like "Mr. Smith", simply add the command line option `--lines`.
# Some attempt is made to even allow words like "don't" but it might not work
# for all cases such as the possesive forms of words ending in 's', 
# like "Wiggins'". Punctuation here refers to any instances of any of next line:
# !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
# Matching is by default independent of case to make the comparisons more robust.
# The optional flag `--sensitive` can be used to override that behavior and make
# the comparisons case-sensitive.
#
# The easiest way to run the script is to provide both the list of words or 
# names file and the "data file" in the same directory with the script. However,
# if you are familiar with designating paths on the command line, thay can be 
# used when invoking the script and pointing it at the files. The script will 
# save the file in the same directory as the provided data file.
#
# The easiest way to create a list_file using a YeastMine multi-column list is
# to paste it in a spreadsheet and extract the gene names column to a new file 
# that you save as text. You'll want to use the `--lines` flag if working with
# tRNA genes like `tP(UGG)A` or any other identifier with punctuation.
#
#
#
#
#
# Dependencies beyond the mostly standard/built-in libraries/modules:
# None
#
#
#
# VERSION HISTORY:
# v.0.1. basic working version
#
#
#
#
#
# TO RUN:
# Example,
# Enter on the command line of your terminal, the line
#-----------------------------------
# python extract_data_on_line_using_word_list.py word_list.txt data_file.txt
#-----------------------------------
#
#
#*******************************************************************************
#


#*******************************************************************************
##################################
#  USER ADJUSTABLE VALUES        #

##################################
#
# ?
#
#*******************************************************************************
#**********************END USER ADJUSTABLE VARIABLES****************************





















#*******************************************************************************
#*******************************************************************************
###DO NOT EDIT BELOW HERE - ENTER VALUES ABOVE###

import sys
import os
import argparse
import string


###---------------------------HELPER FUNCTIONS---------------------------------###


def generate_output_file_name(file_name):
    '''
    Takes a file name as an argument and returns string for the name of the
    output file. The generated name is based on the original file name.

    Specific example
    ================
    Calling function with
        ("data_file.txt")
    returns
        "data_file_extracted.txt"
    '''
    main_part_of_name, file_extension = os.path.splitext(
        file_name) #from http://stackoverflow.com/questions/541390/extracting-extension-from-filename-in-python
    if '.' in file_name:  #I don't know if this is needed with the os.path.splitext method but I had it before so left it
        return main_part_of_name + "_extracted" + file_extension
    else:
        return file_name + "_extracted"


def generate_output_file(provided_text):
    '''
    function takes text and saves it as a text file
    '''
    name_of_file_to_save = generate_output_file_name(data_file.name)
    data_file_stream = open(name_of_file_to_save , "w")
    data_file_stream.write(provided_text.rstrip('\r\n')) #rstrip to remove trailing newline
    # from http://stackoverflow.com/questions/275018/how-can-i-remove-chomp-a-newline-in-python
    data_file_stream.close()
    sys.stderr.write( "\nExtracted lines saved as '{0}'.\n".format(name_of_file_to_save))

def list2text(a_list):
    '''
    a function that takes a lists and makes a string where each item in list
    is on a new line
    '''
    return "\n".join(a_list)

###--------------------------END OF HELPER FUNCTIONS---------------------------###
###--------------------------END OF HELPER FUNCTIONS---------------------------###














#*******************************************************************************
###-----------------for parsing command line arguments-----------------------###
parser = argparse.ArgumentParser(prog='extract_data_on_line_using_word_list.py',description="extract_data_on_line_using_word_list.py \
    takes two files. One file will be used as a list of words or names. That \
    list will be used to examine line by line the `data file` and lines \
    containing words/names from the list will be kept and placed in a resulting \
    file. It was originally intended to be used for lists of gene identifiers, \
    but works with any words or names, etc. **** Script by Wayne Decatur   \
    (fomightez @ github) ***")
parser.add_argument("list_file", help="Name of file containing list or words \
    or names to look for in lines of data file. REQUIRED.", type=argparse.FileType('r'), metavar="ListFile")
parser.add_argument("data_file", help="Name of file containing lines to scan \
    for the presence of the provided list of words or names. Only those lines \
    with those words or names will be kept for the outout file. REQUIRED.", type=argparse.FileType('r'), metavar="DataFile")
parser.add_argument("-l", "--lines",help=
    "add this flag to force individual lines to be used to read the words_list \
    and make the list to be compared to lines in the data file. This enables \
    the use of two-word names with punctutation, like `Mr. Smith`, or even phrases.",
    action="store_true")
parser.add_argument("-s", "--sensitive",help=
    "add this flag to force comparison of items to be case-sensitive (NOT \
    recommended). Default (recommended) is to make the comparisons independent \
    of character case in order make matching more robust, and not miss matches \
    when case use is inconsistent among the sources.",
    action="store_true")
#I would also like trigger help to display if no arguments provided because need at least one input file
if len(sys.argv)==1:    #from http://stackoverflow.com/questions/4042452/display-help-message-with-python-argparse-when-script-is-called-without-any-argu
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()
list_file = args.list_file
data_file = args.data_file
use_lines = args.lines
case_sensitive = args.sensitive




###-----------------Actual Main portion of script---------------------------###


# Go through list_file making a list of the words
list_of_words=[]
#input_file_stream = open(each_item_list_file , "r") # Don't need separate open when use `type=argparse.FileType`. It sets everything up automatically and you will actually cause errors if try to open when already open.
for line in list_file:
    line = line.strip() # don't want line endings so I can easily
    # work with later, hence the use of `.strip()`
    if use_lines:
        line_words = [line]
    else:
        line_words = [word.strip(string.punctuation) for word in line.split()] #tries
        # to address removing punctuation at end but not contractions in middle, 
        # based on Colonel Panic's answer at http://stackoverflow.com/questions/18135967/creating-a-list-of-every-word-from-a-text-file-without-spaces-punctuation
        # print(string.punctuation) yields `!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~`
    list_of_words.extend(line_words)

# Warn about case issue.  
if case_sensitive:
    sys.stderr.write( "\n***NOTICE***. Be aware using `--sensitive` option may result in missing matches if case use inconsistent in lists. ***NOTICE***\n")

# Now go through the data_file keeping lines that contain members of list_of_words
lines_kept_list = []
for line in data_file:
    line = line.strip() # don't want line endings so I can easily
    # work with later, hence the use of `.strip()`
    # Handle differently if `case_sensitive` option activated
    if case_sensitive:
        if any(word in line for word in list_of_words):
            lines_kept_list.append(line)
        # based on Lauritz V. Thaulow's answer at http://stackoverflow.com/questions/6531482/how-to-check-if-a-string-contains-an-element-from-a-list-in-python
    else:
        if any(word.lower() in line.lower() for word in list_of_words):
            lines_kept_list.append(line)
        # expanded from Lauritz V. Thaulow's answer at http://stackoverflow.com/questions/6531482/how-to-check-if-a-string-contains-an-element-from-a-list-in-python

 
# Save results and give feedback
text_to_save = list2text(lines_kept_list)
generate_output_file(text_to_save)


 

#*******************************************************************************
###-***********************END MAIN PORTION OF SCRIPT***********************-###
#*******************************************************************************
