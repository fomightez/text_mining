#!/usr/bin/env python
# df_subgroups_states2summary_df.py
__author__ = "Wayne Decatur" #fomightez on GitHub
__license__ = "MIT"
__version__ = "0.1.0"


# df_subgroups_states2summary_df.py by Wayne Decatur
# ver 0.1
#
#*******************************************************************************
# Verified compatible with both Python 2.7 and Python 3.7; written initially in 
# Python 3. 
#
#
# PURPOSE: Takes a dataframe, and some information about columns in the 
# dataframe and makes a summary data table with the percents for each 
# subgrouping state per total and each group. 
# The dataframe can also be provided as pickled or text form saved as a file.
#
#
#
#
#
#
# Meant to sort of be a text way based to summarize data similar to what
# I ended up making with 
# `donut_plot_with_total_summary_and_subgroups_from_dataframe.py`
# for development, see 
# `developing making dataframe summarizing groups and subgroups with counts and percent.ipynb`
# The initial parts, dataframe or tabular text (text table) handling and initial
# dataframe munging inherit largely from my related donut plot plotting scripts.
# 
#
#
#
#
#
# Dependencies beyond the mostly standard libraries/modules:
# 
#
#
#
# VERSION HISTORY:
# v.0.1. basic working version

#
# To do:
# - test with Python 2 as well
#
#
#
#
# TO RUN:
# Examples,
# Enter on the command line of your terminal, the line
#-----------------------------------
# python df_subgroups_states2summary_df.py data.tsv groups_col subgroups_col
#-----------------------------------
# Issue `df_subgroups_states2summary_df.py -h` for 
# details.
# 
#
#
#
# To use this after importing into a cell in a Jupyter 
# notebook, specify at least XXXXXXXXXXX????????:
# from df_subgroups_states2summary_df import df_subgroups_states2summary_df
# df_subgroups_states2summary_df(df_file="data.tsv",groups_col="status",subgroups_col="subtype");
#
# 
#
'''
CURRENT ACTUAL CODE FOR RUNNING/TESTING IN A NOTEBOOK WHEN IMPORTED/LOADED OR 
PASTED IN ANOTHER CELL:
from df_subgroups_states2summary_df import df_subgroups_states2summary_df
df_subgroups_states2summary_df(df_file="data.tsv",groups_col="Manufacturer",subgroups_col="In_Stock");
'''
#
#
#*******************************************************************************
#





#*******************************************************************************
##################################
#  USER ADJUSTABLE VALUES        #

##################################
#

save_name_prefix = "summary"
simple_summary_additional_tag = "basic"


#
#*******************************************************************************
#**********************END USER ADJUSTABLE VARIABLES****************************






















#*******************************************************************************
#*******************************************************************************
###DO NOT EDIT BELOW HERE - ENTER VALUES ABOVE###

import sys
import os
try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path
import pandas as pd
import numpy as np
import itertools


###---------------------------HELPER FUNCTIONS--------------------------------###

def generate_output_file_name(file_name,save_name_prefix):
    '''
    Takes a file name prefix as an argument and returns string for the name of 
    the output file based on that.  


    Specific example
    =================
    Calling function with
        ("data.tsv","summary")
    returns
        "summary_data"
    '''
    return "{}_{}".format(save_name_prefix, Path(file_name).stem)


def extract_dataframe(file_name):
    '''
    Takes a file name and using the extension determines how to extract the
    dataframe recorded in it. 
    Returns a pandas dataframe object.

    Works with pickled, tab-separated text, and comma-seperated text.
    (haven't added json yet).
    Specify, which with file ending in `.pkl`,`.tsv`, or `.csv`.
    Case doesn't matter for the extension.
    '''
    extension = Path(file_name).suffix
    if extension.lower() == ".pkl":
        return pd.read_pickle(file_name)
    elif extension.lower() == ".tsv":
        return pd.read_csv(file_name, sep='\t')
    elif extension.lower() == ".csv":
        return pd.read_csv(file_name)
    else:
        sys.stderr.write("\n**ERROR** Cannot determine how dataframe is stored "
            "in '{}'.\nChange the file name extension in the input file to be "
            "`.pkl`, `.tsv`, or `.csv` to indicate\nif dataframe stored "
            "pickled, stored as tab-separated text, or stored as\n"
            "comma-separated text."
            ".\n**EXITING !!**.\n".format(file_name))
        sys.exit(1)

    

def split_out_count_and_percent(d):
    '''
    '''
    better_d = {}
    for k,v in d.items():
        new_sub_dict = {}
        for subk,subv in v.items():
            subk1 = "{}{}".format(subk,"_c") #should be okay if subgroups are integers by using `.format()`
            subk2 = "{}{}".format(subk,"_p") #should be okay if subgroups are integers by using `.format()`
            new_sub_dict[subk1] = subv[0]
            new_sub_dict[subk2] = subv[1]
        better_d[k] = new_sub_dict
    return better_d


def is_number(s):
    '''
    check if a string can be cast to a float or numeric (integer).

    Takes a string.

    Returns True or False
    fixed from https://www.pythoncentral.io/how-to-check-if-a-string-is-a-number-in-python-including-unicode/
    later noted similar code is at https://code-maven.com/slides/python-programming/is-number
    '''
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

def cast_to_number(s):
    '''
    Cast a string to a float or integer. 
    Tries casting to float first and if that works then it tries casting the 
    string to an integer. (I thought I saw suggestion of that order somewhere 
    when searching for what I used as `is_number()` check but cannot find source
    right now.)

    Returns a float, int, or if fails, False. (Where using, it shouldn't ever
    trigger returning `False` because checked all could be converted first.)

    based on fixed code from https://www.pythoncentral.io/how-to-check-if-a-string-is-a-number-in-python-including-unicode/
    '''
    try:
        number = float(s)
        try:
            number = int(s)
            return number
        except ValueError:
            pass
        return number
    except ValueError:
        pass
    try:
        import unicodedata
        num = unicodedata.numeric(s)
        return num
    except (TypeError, ValueError):
        pass
    return False

def put_counts_in_brackets_after_perc(row_items):
    '''
    Takes a row of summarized data where the first column is a total number and 
    each set of two columns after that is a coupled set where the first is the 
    counts and the next is the percent. First column that doesn't get further 
    addressed here; each set of coupled two columns get combined into one where 
    percent and counts in a single new cell that gets the first part of the 
    name of each coupled column set.
    '''
    assert (len(row_items)-1) % 2 == 0, ("There should be an even number of "
        "items in the row, discounting first column.")
    for i in range(1,len(row_items),2):
        assert row_items.index[i].rsplit("_")[0] == row_items.index[i+1].rsplit(
            "_")[0], ("The item names (indices) should be same "
            "before ending `_`.")
        row_items[row_items.index[i].rsplit("_")[0]] = "{:.2%} [{}]".format(
            row_items[i+1],int(row_items[i]))
    return row_items

###--------------------------END OF HELPER FUNCTIONS--------------------------###
###--------------------------END OF HELPER FUNCTIONS--------------------------###



#*******************************************************************************
###------------------------'main' function of script--------------------------##

def df_subgroups_states2summary_df(
    df_file=None, df=None, groups_col=None, subgroups_col=None,order=None,
    only_subgrp_perc=False, bracket_counts=False, 
    save_name_prefix = save_name_prefix):
    '''
    Takes a dataframe with some information on groups and subgroupings/states &
    makes a summary data table the percents for each subgrouping per total and 
    each group.

    The dataframe can also be provided as pickled or text form saved as a file.

    Takes the following:
    - name of a dataframe file (string) or a dataframe
    - text of name of column to use as main grouping. This will become the 
    rows in the resulting summary.
    - text of name of column to use in states/subgroupings . These will 
    determine the groupings shown in the columns with count and percents for
    each one if using default settings.
    - Optionlly specify an order to list the states subgroups by providing a 
    Python list as `order`.
    - Optionally, set things to not show the counts for each state/subgroup and
    instead just leave the percent for each. Set with `only_subgrp_perc=True`.
    - Optionally, make at least one resulting summary that has counts bracketed 
    after the percent for the state/subgroup. This output is only meant for 
    presentation, and so a simpler one ready for further use is also made in 
    this case.

    
    '''
    if df is None:
        #read in dataframe from file since none provided in memory
        assert df_file != None, ("If no dataframe is provided, a file with the "
            "contents of the dataframe as pickled, tab-separated text, or "
            "comma-separated text must be provided and the name of that file "
            "specified when calling the script.")
        # use file extension to decide how to parse dataframe file.
        df = extract_dataframe(df_file)



    # Prepare derivatives of the dataframe that may be needed for collecting the
    # necessary summarizing data
    #---------------------------------------------------------------------------
    tc = df[subgroups_col].value_counts()
    total_state_names = tc.index.tolist()
    total_state_size = tc.tolist()
    grouped = df.groupby(groups_col)
    
    
    # Summarize the data for 'total' and among each individual group:
    #---------------------------------------------------------------------------
    # use `value_counts()` on each group to get the count and name of each state
    list_o_subgroup_names_l = []
    list_o_subgroup_size_l = []
    group_dict = {}
    group_list = []

    for name,group in grouped:
        dfgc = group[subgroups_col].value_counts()
        dfgp = group[subgroups_col].value_counts(normalize=True)
        #if sort_on_subgroup_name:
        #   dfgc = group[subgroups_col].value_counts().sort_index()
        #   dfgp = group[subgroups_col].value_counts(
        #       normalize=True).sort_index()
        list_o_subgroup_names_l.append(dfgc.index.tolist())
        list_o_subgroup_size_l.append(dfgc.tolist())
        group_state_names = dfgp.index.tolist()
        gcount_n_percent = zip(dfgc,dfgp)
        gcount_n_percent_d = dict(zip(group_state_names,gcount_n_percent))
        group_dict[name]= gcount_n_percent_d 
        gcount_n_percent_d_to_tuples = (
            x for y in gcount_n_percent_d.values() for x in y)
        group_list.append((name,*gcount_n_percent_d_to_tuples)) #cannot use this
        # to create dataframe because cannot do `.fillna(0)` to fill in the 
        # empties, I think
    total_subgroup_instances = sum(tc)
    # sanity check
    assert len(df) == total_subgroup_instances, ("The subgroup instances should"
        " be length of original dataframe.")

    tp = df[subgroups_col].value_counts(normalize=True)
    total_state_names = tp.index.tolist()
    tp_d = dict(zip(df[subgroups_col].value_counts(
        normalize=True),df[subgroups_col].value_counts()))
    count_n_percent = zip(df[subgroups_col].value_counts(
        ),df[subgroups_col].value_counts(normalize=True))
    count_n_percent_d = dict(zip(total_state_names,count_n_percent))
    # adjust group dict to split out count and percent in a way to make them 
    # ultimately columns in dataframe
    better_group_dict = split_out_count_and_percent(group_dict)
    # Make a dataframe from the 'better' group dict
    almostdf = pd.DataFrame.from_dict(
        better_group_dict, orient='index').fillna(0,downcast='infer') #downcast
    # use added to avoid it making the integer counts into floats; tried 'infer'
    # to see what would happen since 
    # https://stackoverflow.com/questions/27066412/using-fillna-downcast-and-pandas
    # didn't actually seem to take a dictionary.
    # Need to adjust the 'total' one similarly, can tag with 'ALL' name at 
    # same time
    better_total_d = split_out_count_and_percent({"ALL":count_n_percent_d})
    # Make a dataframe from the 'better'TOTAL dict
    totaldf = pd.DataFrame.from_dict(better_total_d, orient='index').fillna(0)
    # impose order to 'total',if specified, since it will be on top
    if order:
        order = list(itertools.chain.from_iterable(
            ( "{}_c".format(x),"{}_p".format(x) ) for x in order)) # see 
        # https://stackoverflow.com/a/11868996/8508004
        totaldf = totaldf[order] 
    # combine the dataframes
    almostfinal_df = pd.concat([totaldf,almostdf], sort= False) # see 
    # https://stackoverflow.com/a/50501889/8508004 about addition of 
    # `sort= False` because I want to keep columns in the order established 
    # prior.
    #add total count across each row, which are the groups
    the_c_cols = [x for x in almostfinal_df.columns if x.endswith('_c')]
    almostfinal_df.insert(0, '[n]', almostfinal_df[the_c_cols].sum(1) )
    #Replace the column names in almostfinal_df with the multiindex with counts
    #and percent
    tuples = [("",almostfinal_df.columns[0])] + list(zip([x.rsplit(
        "_")[0] for x in almostfinal_df.columns[1:]],itertools.cycle(
        ["count","%"])))
    the_multiindex = pd.MultiIndex.from_tuples(tuples)
    df2 = almostfinal_df.set_axis(the_multiindex, axis=1, inplace=False)#merging
    # the multiindex into the already created dataframe based on 
    # https://stackoverflow.com/a/49909924/8508004

    # leave only percents or bracket the counts for presentation if specified
    if only_subgrp_perc:
        df2 = df2.iloc[:, df2.columns.get_level_values(
        1).isin({"[n]","%"})] #based on 
        # https://stackoverflow.com/a/18470819/8508004; related to 
        # https://stackoverflow.com/a/25190070/8508004
        new_col = list(df2.columns.get_level_values(0))
        new_col[0] = df2.columns.get_level_values(1)[0]
        df2.columns = new_col # collapse levels of column names, applying the 
        # `states_col` name as the column name for the percent
    elif bracket_counts:
        # this will make df3
        bc_df = almostfinal_df.copy() # go back to this one because no 
        # multiindex yet and all columns are distinct names;could collapse 
        # column levels of df2 but then non-uniuqe names
        df3 = bc_df.apply(put_counts_in_brackets_after_perc, axis=1)
        subset_list = [x for x in df3.columns if x[-2:] not in ['_c', '_p']]
        df3 = df3[subset_list]
        

    # Returning or Saving
    #--------------------------------------------------------------------
    #using `if __name__ == "__main__"` to customize handling depending if script 
    # called from command line.
    if __name__ == "__main__" and df_file:
        if bracket_counts:
            output_file_name = generate_output_file_name(
                df_file,save_name_prefix)
            pkl_nom = output_file_name+".pkl"
            txt_nom = output_file_name+".tsv"
            df3.to_csv(txt_nom, sep='\t')
            sys.stderr.write("Summary dataframe saved as a text table easily "
                "opened in\ndifferent software; file named: `{}`. This version "
                "meant for presenation only.\n".format(txt_nom))
            df3.to_pickle(pkl_nom)
            sys.stderr.write("\nSummary dataframe saved in pickled form for ease "
                "of use within\nPython; file named: `{}`. This version meant "
                "for\npresentation only.\n".format(pkl_nom))
            # set up for saving the 'basic' version too
            sys.stderr.write("\n\n**Also saving data table as forms easier to "
                "handle for subsequent steps:**\n")
            save_name_prefix = "{}_{}".format(
                save_name_prefix,simple_summary_additional_tag)
        # if called from the command line, save as pandas dataframe and as a
        # text-based table; the latter being for more portability
        output_file_name = generate_output_file_name(df_file,save_name_prefix)
        pkl_nom = output_file_name+".pkl"
        txt_nom = output_file_name+".tsv"
        df2.to_csv(txt_nom, sep='\t')
        sys.stderr.write("Summary dataframe saved as a text table easily "
            "opened in\ndifferent software; file named: `{}`\n".format(txt_nom))
        df2.to_pickle(pkl_nom)
        sys.stderr.write("\nSummary dataframe saved in pickled form for ease "
            "of use within\nPython; file named: `{}`. This will retain the "
            "column headers/names formatting best.".format(pkl_nom))

    else:
        if bracket_counts:
            sys.stderr.write("Summary dataframes returned. First is for "
                "presentation only with percent and counts as text in a "
                "single cell; second returned is basics with counts and "
                "percent data as integer and floats, respectively.")
            return df3, df2
        sys.stderr.write("Summary dataframe returned.")
        return df2


###--------------------------END OF MAIN FUNCTION----------------------------###
###--------------------------END OF MAIN FUNCTION----------------------------###










#*******************************************************************************
###------------------------'main' section of script---------------------------##
def main():
    """ Main entry point of the script """
    # placing actual main action in a 'helper'script so can call that easily 
    # with a distinguishing name in Jupyter notebooks, where `main()` may get
    # assigned multiple times depending how many scripts imported/pasted in.
    kwargs = {}
    kwargs['order'] = order
    kwargs['only_subgrp_perc'] = args.only_subgrp_perc
    kwargs['bracket_counts'] = args.bracket_counts

    df_subgroups_states2summary_df(
        df_file=args.df_file,groups_col=args.groups_col,
        subgroups_col=args.subgroups_col,**kwargs)
    # using https://www.saltycrane.com/blog/2008/01/how-to-use-args-and-kwargs-in-python/#calling-a-function
    # to build keyword arguments to pass to the function above
    # (see https://stackoverflow.com/a/28986876/8508004 and
    # https://stackoverflow.com/a/1496355/8508004 
    # (maybe https://stackoverflow.com/a/7437238/8508004 might help too) for 
    # related help). Makes it easy to add more later.





if __name__ == "__main__":
    ###-----------------for parsing command line arguments-------------------###
    import argparse
    parser = argparse.ArgumentParser(prog='df_subgroups_states2summary_df.py',
        description="df_subgroups_states2summary_df.py \
        takes a dataframe, and some information about columns in the dataframe \
        and makes a summary data table with the percents for each subgrouping \
        / state per total and each group. \
        **** Script by Wayne Decatur   \
        (fomightez @ github) ***")

    parser.add_argument("df_file", help="Name of file containing the \
        dataframe. Whether it is in the form of a pickled dataframe, \
        tab-separated text, or comma-separated text needs to be indicated by \
        the file extension. So `.pkl`, `.tsv`, or `.csv` for the file \
        extension. \
        ", metavar="DF_FILE")

    parser.add_argument("groups_col", help="Text indicating column in \
        dataframe to use as main grouping categories.\
        ", metavar="GROUPS")

    parser.add_argument("subgroups_col", help="Text indicating column in \
        dataframe to use as subgroupings / states for the groups.\
        ", metavar="SUBGROUPS")

    parser.add_argument('-ord', '--order', action='store', type=str, 
        help="This flag is used to specify that you want to control the order \
        of the subgroups to read from left to right. Follow the flag with an \
        order listing, left to right, \
        of the subgroup identifiers separated by \
        commas, without spaces or quotes. For example `-ord yes,maybe,no`. \
         ")# based on https://stackoverflow.com/a/24866869/8508004

    parser.add_argument("-olsp", "--only_subgrp_perc",help=
        "add this flag to only leave states/percentage data in produced data \
        table. No counts will be included for each state/subgrouping.",
        action="store_true")

    parser.add_argument("-bc", "--bracket_counts",help=
        "add this flag to display counts in brackets AFTER the percent listing \
        This is only meant for generating presentation style dataframes as the \
        percent & count data will be combined into one cell as a string which \
        is not suitable for further use. Because of that this option will also \
        produce a more basic summary table to be used for further efforts. Use \
        of  `--only_subgrp_perc` renders this argument moot as nothing \
        concerning counts is displayed in that case.",
        action="store_true")



    #I would also like trigger help to display if no arguments provided because 
    # need at least one for url
    if len(sys.argv)==1:    #from http://stackoverflow.com/questions/4042452/display-help-message-with-python-argparse-when-script-is-called-without-any-argu
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    order = args.order
    #process to a python list if it exists
    if order:
        order = args.order.split(',')
        #if they hapen to be integers or floats, convert so will match type in 
        # dataframe
        if all([is_number(s) for s in order]):
            order = [cast_to_number(s) for s in order]
            # make sure all float if any are float, because line above will 
            # cast to integer if possible
            if any(isinstance(x, float) for x in order):
                order = [float(x) for x in order]
    




    main()

#*******************************************************************************
###-***********************END MAIN PORTION OF SCRIPT***********************-###
#*******************************************************************************