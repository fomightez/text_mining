#!/usr/bin/env python
# find_overlap_in_lists.py by Wayne Decatur
# ver 0.2
#
#*******************************************************************************
# USES Python 2.7 but should be convertable via 2to3, see https://docs.python.org/3.0/library/2to3.html
#
# PURPOSE: Takes files with items listed one item to a line and determines items
# that occur in all the lists. Thus, it identifies only those items shared by
# all the lists of items. It was intended to be used for lists of genes but can
# work for any type of list. The default settings cause the comparisons to be
# case-insensitive with the caveat that the case of the shared items will be
# set by whatever list is provided in the first position when calling the script.
# Matching is by default independent of case to make the comparisons more robust.
# The optional flag `--sensitive` can be used to override that behavior and make
# the comparisons case-sensitive.
#
# A file listing the shared items (genes) will be saved in the same directory
# in which the script finds the first file.
#
# Note, if using with yeast genes, probably best to use my script
# `geneID_list_to_systematic_names.py` to convert all to yeast systematic
# names so that the lists are standardized before running
# `find_overlap_in_lists.py`.
#
#
#
#
#
#
# Dependencies beyond the mostly standard libraries/modules:
# None
#
#
#
# VERSION HISTORY:
# v.0.1. basic working version
# v.0.2. basic working version with the list files supplied via command line
#
#
#
#
# TO RUN:
# Example,
# Enter on the command line of your terminal, the line
#-----------------------------------
# find_overlap_in_lists.py list1.txt list2.txt
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


###---------------------------HELPER FUNCTIONS---------------------------------###


def generate_output_file_name(file_name):
    '''
    Takes a file name as an argument and returns string for the name of the
    output file. The generated name is based on the original file
    name.

    Specific example
    ================
    Calling function with
        ("file1.txt")
    when `list_files_to_analyze_list` contains 3 file names
    returns
        "file1_and_3others_shared_items.txt"
    '''
    main_part_of_name, file_extension = os.path.splitext(
        file_name) #from http://stackoverflow.com/questions/541390/extracting-extension-from-filename-in-python
    if len(list_files_to_analyze_list) == 2:
        base_name_without_extension_for_second_file = os.path.splitext(
            os.path.basename(list_files_to_analyze_list[1]))[0]
        if '.' in file_name:  #I don't know if this is needed with the os.path.splitext method but I had it before so left it
            return main_part_of_name + "_and_"+ base_name_without_extension_for_second_file +"_shared_items" + file_extension
        else:
            return file_name + "_and_"+ base_name_without_extension_for_second_file +"_shared_items"
    else:
        if '.' in file_name:  #I don't know if this is needed with the os.path.splitext method but I had it before so left it
            return main_part_of_name + "_and_"+ str(len(
                list_files_to_analyze_list) - 1) +"others_shared_items" + file_extension
        else:
            return file_name + "_and_"+ str(len(
                list_files_to_analyze_list) - 1) +"others_shared_items"

def generate_output_file(provided_text):
    '''
    function takes text and saves it as a text file
    '''
    name_of_file_to_save = generate_output_file_name(list_files_to_analyze_list[0])
    data_file_stream = open(name_of_file_to_save , "w")
    data_file_stream.write(provided_text.rstrip('\r\n')) #rstrip to remove trailing newline
    # from http://stackoverflow.com/questions/275018/how-can-i-remove-chomp-a-newline-in-python
    data_file_stream.close()
    sys.stderr.write( "\nOverlap identified! Shared items list saved as '{0}'.\n".format(name_of_file_to_save))

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
parser = argparse.ArgumentParser(prog='find_overlap_in_lists.py',description="find_overlap_in_lists.py \
    takes any number of files of lists with items on separate lines and reports \
    those items shared by all. It was originally intended to be used for lists \
    of genes, but works on any lists. **** Script by Wayne Decatur   \
    (fomightez @ github) ***")
parser.add_argument("Files", help="Names of files containing lists to compare. AT LEAST ONE REQUIRED.", nargs="+")
# see http://stackoverflow.com/questions/13219910/argparse-get-undefined-number-of-arguments
# for how last line allows any number of files to be used.
parser.add_argument("-s", "--sensitive",help=
    "add this flag to force comparison of items to be case-sensitive (NOT \
    recommended). Default (recommended) is to make the comparisons independent \
    of character case in order make matching more robust, and not miss matches \
    when case use is inconsistent among the lists.",
    action="store_true")
#I would also like trigger help to display if no arguments provided because need at least one input file
if len(sys.argv)==1:    #from http://stackoverflow.com/questions/4042452/display-help-message-with-python-argparse-when-script-is-called-without-any-argu
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()
list_files_to_analyze_list = args.Files
case_sensitive = args.sensitive



###-----------------Actual Main portion of script---------------------------###

# warn if only one file provided
if len(list_files_to_analyze_list) == 1:
    sys.stderr.write( "\n***WARNING***. Hard to check for overlap between lists, when given only one list.\nForget to add others? By default overlap equals provided list...\n")


# Go through each file making a list of the items
list_of_items_in_each_item_list=[]
case_resolving_dictionary = {} # to be used unless `case_sensitive` flag set
for each_item_list_file in list_files_to_analyze_list:
    input_file_stream = open(each_item_list_file , "r")
    file_items_list= []
    for line in input_file_stream:
        line = line.strip() #  # don't want line endings so I can easily
        # manipulate later, hence the use of `.strip()`
        file_items_list.append(line)
        # For first file, collect the lines for the conversion dictionary to
        # restore the case later.
        if each_item_list_file == list_files_to_analyze_list[0]:
            case_resolving_dictionary[line.upper()] = line
    #Completed scan of input file and therefore close file and add item list to list of item lists
    input_file_stream.close()

    # Changing case of all items in the list will make comparisons more robust,
    # but this may not be desired in all cases. Because of the simple
    # implementation being used, the process will result in output where
    # case used in first provided file us used. This behavior also may not be
    # desired and so there is way to override the case independence of the
    # comparisons. Note though that making the comparisons sensitive to case may
    # result in missing some matches if case use inconsistent in the lists.
    #
    if not case_sensitive:
        file_items_list = [x.upper() for x in file_items_list]


    list_of_items_in_each_item_list.append(set(file_items_list)) # The typecast
    # to `set` insures the list only includes unique items and set is that gets
    # used in the main function.

    #print len(file_items_list) # for verifying works/debugging
    #print len(set(file_items_list)) # for verifying works/debugging

    # Monitor state of redundancy in lists to allow later use in formatting
    # feedback about percent overlap represents for each list.
    redundancy_noted = True if len(set(
        file_items_list)) < len(file_items_list) else False
    #print redundancy_noted # for verifying works/debugging






# Warn about case issue. (But not in a loop.)
if case_sensitive:
    sys.stderr.write( "\n***NOTICE***. Be aware using `--senstive` option may result in missing matches if case use inconsistent in lists. ***NOTICE***\n")

# Now determine items that occur in ALL the item lists, i.e., the overlap
shared_items = set.intersection(*list_of_items_in_each_item_list) # see http://stackoverflow.com/questions/2541752/how-best-do-i-find-the-intersection-of-multiple-sets-in-python

# if there was overlap identified handle generating the output
if len(shared_items) > 0:
    # Before making output, if comparisons were case-insensitive (the default),
    # convert items all changed to uppercase for robustness of comparison back
    # to the case found in the first file provided when calling the script.
    if not case_sensitive:
        shared_items_case_restored = [] # List to store case restored list to not
        # change list while iterating.
        for each_item in shared_items:
            shared_items_case_restored.append(case_resolving_dictionary[each_item])
        # with list of items restored to match case of original input in hand,
        # now set the shared_items set to this.
        shared_items = set(shared_items_case_restored)



    # Make the list into text that can be easily made into an output file by
    # separating each item with a new line
    text_to_save = list2text(shared_items)




    # Save results
    generate_output_file(text_to_save)

    # give user feedback on percentage of each list the overlap represents
    for index, item_list in enumerate(list_of_items_in_each_item_list):
        info_on_percent_overlap = (
            "The overlap represents {0:.2%} of the list '{1}'".format(
                len(shared_items)/float(len(item_list)),
                list_files_to_analyze_list[index]))
        if redundancy_noted:
            sys.stderr.write(
                info_on_percent_overlap + ", disregarding redundancy in the list.\n")
        else:
            sys.stderr.write(info_on_percent_overlap + ".\n")

else:
    sys.stderr.write( "\nNo overlap identified. Check your lists.\n")




#*******************************************************************************
###-***********************END MAIN PORTION OF SCRIPT***********************-###
#*******************************************************************************
