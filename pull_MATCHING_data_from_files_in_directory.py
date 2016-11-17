#! /usr/bin/env python

# pull_matching_data_from_files_in_directory by Wayne Decatur
# ver 0.1
#
#
#
#*************************************************************************
# USES Python 2.7
#
# DEPENDENCIES:
# typical modules like argparse, os
#
# Purpose: extracts lines with matching text in them from files in a folder.
# It outputs the matching lines to a single file.
# In regards to the text to match on each line, it is oblivious to case.
'''
Info on original impetus and use from `All NME1-involved results culled from all plus ligase results.md`:
Did this by making a script that went through every file in the `GSE69472_RAW` folder and checked if name of file ended with `.txt` and contained `_ligase` and then if so, it collected every line that had `NME1` on it. Checking if `.txt` at the end will eliminate those that I had not uncompressed yet because those will have `txt.gz` at end. Checking if `_ligase_` there in name will eliminate any data from the `-noligase_` sets, even if I had happened to unpack them.
Ran the script in the directory above the  `GSE69472_RAW` folder and pointed it at that folder with an argument when called the script.
REFASHIONED CODE FROM `merge_multi_PDBs_into_single_file.py` to make.
Then I decided to try and generalize it to allow setting the text in file names
and text to search in lines of text as user specified fields in the code.
'''
#
#
# v.0.1. - basics done
#
# To do:
# Make so that is general. (nearly done)
# Make so you can provide at least the text in the line to look for as an
# argument when you call the program?
# Other ideas to possibly do:
# Make so you can specify regular expression in name_pattern_for_files_to_mine.
# Make so you can use regular expression to specify text_of_interest.
# May be easier to initially accomplish those last two by making a new version
# where hardcoded in the comparison code first.
#
#
# TO RUN:
# For example, when in the directory containing the directory with the data files
# , the `GSE69472_RAW` folder, enter on the command line, the line
#-----------------------------------
# python pull_matching_data_from_files_in_directory.py GSE69472_RAW
#-----------------------------------
# to generate the file named 'NME1_extracted_data_from_GSE69472_RAW.txt' in your
# working directory.
#
# Meaning that you can point it at a directory and then it will process
# all the files in that folder.
#
#*************************************************************************


##################################
#  USER ADJUSTABLE VALUES        #

##################################
#
name_pattern_for_files_to_mine = ".TXT" #CAPITALIZE HERE. Gets compared to a version where
# made uppercase in order to avoid case causing issues.
second_name_pattern_for_files_to_mine = "_ligase"
text_of_interest = "NME1"

#
#*******************************************************************************
#*******************************************************************************










#*************************************************************************
#*************************************************************************
###DO NOT EDIT BELOW HERE - ENTER VALUES ABOVE###
import os
import sys
from stat import *
#from urllib import urlopen
import logging
import argparse
from argparse import RawTextHelpFormatter
from Bio.PDB import *

#DEBUG CONTROL
#comment line below to turn off debug print statements
#logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)





#argparser from http://docs.python.org/2/library/argparse.html#module-argparse and http://docs.python.org/2/howto/argparse.html#id1
parser = argparse.ArgumentParser(prog='python pull_matching_data_from_files_in_directory.py',description="python pull_matching_data_from_files_in_directory.py extracts lines containg '"+ text_of_interest + "' in them from data in a directory.\nSee code for more information.\n \nWritten by Wayne Decatur --> Fomightez @ Github or Twitter. \n\n\nActual example what to enter on command line to run program:\npython pull_matching_data_from_files_in_directory.py GSE69472_RAW", formatter_class=RawTextHelpFormatter)
#learned how to control line breaks in description above from http://stackoverflow.com/questions/3853722/python-argparse-how-to-insert-newline-the-help-text
#DANG THOUGH THE 'RawTextHelpFormatter' setting seems to apply to all the text then. Not really what I wanted.
parser.add_argument("Directory", help=
    "directory containing data files to extract data from. REQUIRED.")
#I would also like trigger help to display if no arguments provided because need at least a directory
if len(sys.argv)==1:    #from http://stackoverflow.com/questions/4042452/display-help-message-with-python-argparse-when-script-is-called-without-any-argu
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()



###---------------------------HELPER FUNCTIONS---------------------------------###



def extract_pertinent_lines(data_file):
    '''
    Takes a file and finds every line with text on it and adds it to a list.

    Returns the list of the lines.
    '''
    pertinent_lines = []
    inFile = open(data_file)
    for line in inFile:
        text_of_line = line.strip() # don't want line endings so I can easily
        # manipulate later
        if text_of_interest in text_of_line:
            pertinent_lines.append(text_of_line)
    inFile.close()
    return pertinent_lines

def send_list_as_lines_to_a_file(a_list, file_name):
    '''
    The functions takes a list and prints the strings in that list as lines
    in a file with file_name
    '''
    fileoutput = open(file_name, "w")
    output_text = "\n".join(a_list)
    fileoutput.write(output_text)
    fileoutput.close()

def extract_data(list_of_filepaths,name_for_output):
    '''
    The function takes as input a list of filepaths for several individual data
    files and extracts data sought. Saving it in a file.
    '''
    list_of_data_strings=[]
    for data_file in list_of_filepaths:
        list_of_data_strings.extend(extract_pertinent_lines(data_file)) #need extend, not append
    #write the data to a file
    send_list_as_lines_to_a_file(list_of_data_strings, name_for_output)
    sys.stderr.write("The file "+name_for_output+" has been created with just the specified data.\n")

###--------------------------END OF HELPER FUNCTIONS---------------------------###






###----------------------MAIN PART OF SCRIPT--------------------------------###
name_of_file_to_generate = text_of_interest +"_extracted_data_from_" + str(args.Directory) + ".txt"
list_of_filepaths_for_data_files = []


# If provided argument is a DIRECTORY loop through collecting information on
# each file matching the name pattern.
#from http://stackoverflow.com/questions/3204782/how-to-check-if-a-file-is-a-directory-or-regular-file-in-python
if os.path.isfile(args.Directory):
    sys.stderr.write("\n***ERROR ********************ERROR ***************** \n")
    sys.stderr.write("Oops! You only provided a single file.\n This program is for mining data from files in a directory.")
    sys.stderr.write("***ERROR ********************ERROR ***************** \n \n")
elif os.path.isdir(args.Directory):
    for f in os.listdir(args.Directory):
        pathname = os.path.join(args.Directory, f)
        #FOR DEBUGGING
        logging.debug(pathname)
        mode = os.stat(pathname).st_mode
        if S_ISREG(mode) and pathname[-4:].upper() == name_pattern_for_files_to_mine:
            # It's a text data file, collect the path and file name info if
            # also contains `_ligase_`
            if second_name_pattern_for_files_to_mine in pathname:
                list_of_filepaths_for_data_files.append(pathname)



# Now that the name and path info on each pertient data file has been collected,
# extract the data from each and make a file
extract_data(list_of_filepaths_for_data_files, name_of_file_to_generate)
