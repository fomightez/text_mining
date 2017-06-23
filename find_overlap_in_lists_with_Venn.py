#!/usr/bin/env python
# find_overlap_in_lists_with_Venn.py by Wayne Decatur
# ver 0.1
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
# Matching  independent of case is done to make the comparisons more robust.
# The optional flag `--sensitive` can be used to override that behavior and make
# the comparisons case-sensitive.
#
# When comparing 2, 3, or four lists to  each other, a Venn diagram depicting
# the relationship of the lists will be made by default. Only the output for two
#  or three lists will be an area-weighted diagram. See my script
# `find_overlap_in_lists_with_Venn.py` if you are not interested in generating
# diagrams or use the optional flag to override making the diagram.
#
# A file listing the shared items (genes) will be saved in the same directory
# in which the script finds the first file. If a diagram image is produced, it
# will also be located there.
#
# Note, if using with yeast genes, probably best to use my script
# `geneID_list_to_systematic_names.py` to convert all to yeast systematic
# names so that the lists are standardized before running
# `find_overlap_in_lists_with_Venn.py`.
#
#
#
#
#
#
#
# Dependencies beyond the mostly standard libraries/modules:
# matplotlib_venn
# If comparing four lists it will need the additional script `venn4_from_github.py`
# and pylab
#
#
#
#
# VERSION HISTORY:
# v.0.1. basic working version of `find_overlap_in_lists.py`(v.0.2.) with Venn
# diagram representation added.
#
# Possible 'to do':
# Add a way to use arguments to add names to the labels for the Venn diagrams,
# such as after the file lists. But easy enough for now to edit in image
# processor.
#
#
#
#
# TO RUN:
# Example,
# Enter on the command line of your terminal, the line
#-----------------------------------
# find_overlap_in_lists_with_Venn.py list1.txt list2.txt
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


def generate_image_file_name(file_name):
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
        "file1_and_3others_overlap_representation.png"
    '''
    data_file_name_generator_result = generate_output_file_name(file_name)
    # return data_file_name_generator_result where `_shared_items` and anything after it replaced with `_overlap_representation.png`
    return data_file_name_generator_result.rsplit("_shared_items", 1)[0] + '_overlap_representation.png'

def knights_of_Venn_it(list_of_items_in_each_item_list, shared_items):
    '''
    Using matplotlib_venn for cases where there are two or three lists, it
    represents the overlap between them. It will also make a basic,
    non-weighted output for four lists now.

    Function needs the list of items made from each list and a list of the
    overlapping items shared by all lists.

    Note that as discussed at https://github.com/konstantint/matplotlib-venn/issues/15
    there is a venn4 Kristoffer Sahlin implemented at https://github.com/ksahlin/pyinfor/blob/master/venn.py
    that makes non-area-weighted 4-set diagram, but I have only implemented
    it here as experimental.
    '''
    name_of_image_file_to_save = generate_image_file_name(list_files_to_analyze_list[0])

    from matplotlib import pyplot as plt # by placing here it doesn't get
    # imported if not going to be used

    if len(list_of_items_in_each_item_list) == 2:
        # For case where two lists
        # see http://matthiaseisen.com/pp/patterns/p0144/
        from matplotlib_venn import venn2, venn2_circles
        # Subset sizes
        s = (
            len(list_of_items_in_each_item_list[0]) - len(shared_items),  # Ab (diagram at http://matthiaseisen.com/pp/patterns/p0144/ shows this as "A but not B" which equates to total in A with overlap with B substracted)
            len(list_of_items_in_each_item_list[1]) - len(shared_items),  # aB (diagram at http://matthiaseisen.com/pp/patterns/p0144/ shows this as "B but not A" which equates to total in B with overlap with A substracted)
            len(shared_items),  # AB (intersection, a.k.a. overlap shared between the two sets)
        )

        v = venn2(subsets=s, set_labels=(
            list_files_to_analyze_list[0] + " (" +str(len(list_of_items_in_each_item_list[0])) + " items)", list_files_to_analyze_list[1]  + " (" +str(len(list_of_items_in_each_item_list[1])) + " items)"))

        # Subset alphas and colors
        # Adding try..except combos for these because it turns out if group all a subset of sets some of the subsets won't exist and reference them like `01` and trying to do something throws an errr `AttributeError: 'NoneType'`
        # but if don't exist no harm not changing the properties.
        try:
            v.get_patch_by_id('10').set_color('c')
        except AttributeError:
            pass
        try:
            v.get_patch_by_id('01').set_color('#993333')
        except AttributeError:
            pass
        try:
            v.get_patch_by_id('11').set_color('blue')
        except AttributeError:
            pass

        try:
            v.get_patch_by_id('10').set_alpha(0.5)
        except AttributeError:
            pass
        try:
            v.get_patch_by_id('01').set_alpha(0.5)
        except AttributeError:
            pass
        try:
            v.get_patch_by_id('11').set_alpha(0.5)
        except AttributeError:
            pass

        #plt.show()
        plt.savefig(name_of_image_file_to_save)


    elif len(list_of_items_in_each_item_list) == 3:
        # For case where three lists
        # see http://matthiaseisen.com/pp/patterns/p0145/

        #breaking down subsets in easier way to represent and track
        A_total = len(list_of_items_in_each_item_list[0])
        A_overlap_with_B = len(set.intersection(
            list_of_items_in_each_item_list[0],list_of_items_in_each_item_list[1]))
        A_overlap_with_C = len(set.intersection(
            list_of_items_in_each_item_list[0],list_of_items_in_each_item_list[2]))
        B_total = len(list_of_items_in_each_item_list[1])
        B_overlap_with_C = len(set.intersection(
            list_of_items_in_each_item_list[1],list_of_items_in_each_item_list[2]))
        C_total = len(list_of_items_in_each_item_list[2])
        shared_by_all = len(shared_items)

        A_but_not_B_or_C = (A_total - (
            A_overlap_with_B + A_overlap_with_C) + shared_by_all)

        B_but_not_A_or_C = (B_total - (
            A_overlap_with_B + B_overlap_with_C) + shared_by_all)

        A_n_B_but_not_C = (
            A_overlap_with_B - shared_by_all)

        C_but_not_A_or_B = (C_total - (
            A_overlap_with_C + B_overlap_with_C) + shared_by_all)

        A_n_C_but_not_B = (
            A_overlap_with_C - shared_by_all)

        B_n_C_but_not_A = (
            B_overlap_with_C - shared_by_all)



        from matplotlib_venn import venn3, venn3_circles
        # Subset sizes
        s = (
            A_but_not_B_or_C,    # Abc (diagram at http://matthiaseisen.com/pp/patterns/p0145/ looks to show this as "A but not B or C" which equates to total in A with overlap with both B & C subtracted & with overlap shared by all added back [since already subtracted once])
            B_but_not_A_or_C ,    # aBc (diagram at http://matthiaseisen.com/pp/patterns/p0145/ looks to show this as "B but not A or C" which equates to total in B with overlap with both A & C subtracted & with overlap shared by all added back [since already subtracted once])
            A_n_B_but_not_C,    # ABc
            C_but_not_A_or_B,    # abC (label in diagram at http://matthiaseisen.com/pp/patterns/p0145/ wrong for this one; looks to show this as "C but not A or B"  which equates to total in C with overlap with both A & B subtracted & with overlap shared by all added back [since already subtracted once])
            A_n_C_but_not_B ,    # AbC (label in diagram at http://matthiaseisen.com/pp/patterns/p0145/ wrong for this one; equates to everything shared by A and C that is not in B so it is overlap between A and C with number shared by all substracted)
            B_n_C_but_not_A,  # aBC (label in diagram at http://matthiaseisen.com/pp/patterns/p0145/ wrong for this one;  equates to everything shared by B and C that is not in A so it is overlap between B and C with number shared by all substracted)
            shared_by_all ,    # ABC (intersection, a.k.a. overlap shared between the three sets)
        )

        v = venn3(subsets=s, set_labels=(
            list_files_to_analyze_list[0] + " (" +str(len(list_of_items_in_each_item_list[0])) + " items)", list_files_to_analyze_list[1] + " (" +str(len(list_of_items_in_each_item_list[1])) + " items)", list_files_to_analyze_list[2] + " (" +str(len(list_of_items_in_each_item_list[2])) + " items)"))

        # Subset alphas and colors
        # Adding try..except combos for these because it turns out if group all a subset of sets some of the subsets won't exist and reference them like `010` and trying to do something throws an errr `AttributeError: 'NoneType'`
        # but if don't exist no harm not changing the properties.
        try:
            v.get_patch_by_id('100').set_color('c')
        except AttributeError:
            pass
        try:
            v.get_patch_by_id('010').set_color('#993333')
        except AttributeError:
            pass
        try:
            v.get_patch_by_id('110').set_color('blue')
        except AttributeError:
            pass


        try:
            v.get_patch_by_id('101').set_alpha(0.5)
        except AttributeError:
            pass
        try:
            v.get_patch_by_id('011').set_alpha(0.5)
        except AttributeError:
            pass
        try:
            v.get_patch_by_id('111').set_alpha(0.5)
        except AttributeError:
            pass

        #plt.show()
        plt.savefig(name_of_image_file_to_save)

    else:
        # For case where four lists
        import venn4_from_github

        v = venn4_from_github.venn4_w_fileNameSave(list_of_items_in_each_item_list,
            list_files_to_analyze_list, filename=name_of_image_file_to_save, figsize=(12,12))

    sys.stderr.write( "\nImage of overlap of the lists saved as '{0}'.\n".format(name_of_image_file_to_save))





###--------------------------END OF HELPER FUNCTIONS---------------------------###
###--------------------------END OF HELPER FUNCTIONS---------------------------###














#*******************************************************************************
###-----------------for parsing command line arguments-----------------------###
parser = argparse.ArgumentParser(prog=' find_overlap_in_lists.py',description=" find_overlap_in_lists.py \
    takes any number of files of lists with items on separate lines and reports \
    those items shared by all. It was originally intended to be used for lists \
    of genes, but works on any lists. When comparing 2, 3, or four lists to \
    each other, a Venn diagram depicting the relationship of the lists will be \
    made. Only the output for two or three lists will be an area-weighted \
    diagram.**** Script by Wayne Decatur (fomightez @ github) ***")
parser.add_argument("Files", help="List the names of FILES containing the lists \
    to compare. AT LEAST ONE IS REQUIRED. Of course, it makes more sense with \
    two or more.", nargs="+")
# see http://stackoverflow.com/questions/13219910/argparse-get-undefined-number-of-arguments
# for how last line allows any number of files to be used.
parser.add_argument("-s", "--sensitive",help=
    "add this flag to force comparison of items to be case-sensitive (NOT \
    recommended). Default (recommended) is to make the comparisons independent \
    of character case in order make matching more robust, and not miss matches \
    when case use is inconsistent among the lists.",
    action="store_true")
parser.add_argument("-n", "--nodiagram",help=
    "add this flag to force not making any Venn diagram. (Or you could just \
    use my script 'find_overlap_in_lists.py' that does the same without \
    producing a diagram.)",
    action="store_true")
#I would also like trigger help to display if no arguments provided because need at least one input file
if len(sys.argv)==1:    #from http://stackoverflow.com/questions/4042452/display-help-message-with-python-argparse-when-script-is-called-without-any-argu
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()
list_files_to_analyze_list = args.Files
case_sensitive = args.sensitive
no_diagram = args.nodiagram



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
    # but this may not be desired in all cases. Plus because of the simple
    # implementation being used will the process will result in output where
    # all capitalized and this also may not be desired and so there is way to
    # override the case change. Note though that not changing the case may result
    # in missing some matches if case use inconsistent in the lists.
    #
    if not case_sensitive:
        file_items_list = [x.upper() for x in file_items_list]


    list_of_items_in_each_item_list.append(set(file_items_list)) # The typecast
    # to `set` insures the list only includes unique items and set is that gets
    # used in the main function.

    # Monitor state of redundancy in lists to allow later use in formatting
    # feedback about percent overlap represents for each list.
    redundancy_noted = True if len(set(
        file_items_list)) < len(file_items_list) else False

# Warn about case issue. (But not in a loop.)
if case_sensitive:
    sys.stderr.write( "\n***NOTICE***. Be aware using `--sensitive` option may result in missing matches if case use inconsistent in lists. ***NOTICE**\n")

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

    # Make an accompanying diagram depicting the relationships between the lists,
    # if 2, 3, or 4 lists.
    # Originally could only handle where 2 or 3 lists for making representation due
    # to limit in standard Venn code. I have now tried adding a basic,
    # non-area-weighted output for 4 too. See the function for more info.
    if (len(list_of_items_in_each_item_list) >  1) and (
        len(list_of_items_in_each_item_list) < 5) and not no_diagram:
        knights_of_Venn_it(list_of_items_in_each_item_list, shared_items)

else:
    sys.stderr.write( "\nNo overlap identified. Check your lists.\n")





#*******************************************************************************
###-***********************END MAIN PORTION OF SCRIPT***********************-###
#*******************************************************************************
