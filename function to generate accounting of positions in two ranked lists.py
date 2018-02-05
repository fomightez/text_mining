#!/usr/bin/env python3
# function to generate accounting of positions in a ranked list.py
__author__ = "Wayne Decatur" #fomightez on GitHub
__license__ = "MIT"
__version__ = "0.1.0"

# Originally written for comparing ranked gene lists but should work on any list
# where the order provided was a result of rank and the two lists are same
# length and CONTAIN NO DUPLICATES.
# Content & Arrangement of output inspired in a significant way by 'Rank list' 
# accessible clicking `Hide sample files and parameters [-]` at [Rank Rank Hypergeometric Overlap:Graeber Lab Homepage:Simple Version(RRHO)](http://systems.crump.ucla.edu/rankrank/rankranksimple.php)

# Output meant to complement similarity metric calculation as first used in 
# `Examining Enrichment in Purified Mitochondria Samples Directly from the Salmon-Quantified Data.ipynb`

# Right now drafting to work for loading into a Jupyter notebook cell since I
# have been working a lot there and have need for this ability now. Could always
# expand into a stand-alone `runnable` or importable function/script later.

def generate_reports_for_ranked_lists_pos(lizt1,
                                        lizt2,
                                        return_dataframes = False,
                                        save_as = "tsv",
                                        output_file1 = "ranked list accounting.tsv",
                                        output_file2 = "ranked list row shift amounts.tsv"):
    """
    function to generate reports accounting for positions in two ranked lists.
    Provided lists should be equal in length WITH NO DUPLICATES.

    Takes:
    two lists to be compared.    * REQUIRED *
    Optional parameters may also be provided.

    Returns:
    either nothing or two dataframes depending on options user supplies when 
    function called.
    Typically, when it runs, it creates output tables in a user-defined 
    format that given an accounting of the postions in the two ranked lists.
    The default output is tsv.

    Output 1: 
    A table with the items in list one in order with the rank in list 1 and
    then the rank in list 2. The fourth column records the shift of the item in
    list 2 realtive list 1.
    For example if the first item in list 1 shifts to position 10 in list 2, 
    then the first half of the line would be:
    YDR190C 1   10  9

    Similar data makes up the second half of each line. The fifth column will be
    the id of the ranked list at that position with the other columns similar
    to the first half. 
    There is a header line so this would be the first two lines in this example:

    item_l1 pos_l1  pos_l2  ∆l1>l2  item_l2 pos_l2  pos_l1  ∆l2>l1
    YDR190C 1   10  9   Q0160   1   3   2


    Output 2:
    A table of the shifts is also produced. Highlights of this can be subsequently
    viewed with `df.describe()` or the distribution of shifts easily plotted 
    from this with pandas histograms.


    To make this easy, natural language is used to describe and number the items
    so that the first item is number 1 and so on. (No zero indexing.)

    OPTIONS:
    return_dataframes   Set this to True to return two dataframes.
    save_as             OPTIONS: 'do_not','excel','tsv','csv'. 'do_not' is for
                        when you don't want the output files saved and most 
                        likely would be used in conjunction with the 
                        `return_dataframes =  True` option.


    Typical exmple uses:
    generate_reports_for_ranked_lists_pos(l1,l2,save_as = "tsv")

    -OR-

    df1,df2 = generate_reports_for_ranked_lists_pos(l1,l2,return_dataframes = True)

    The latter being for the case where return dataframes.


    """


    # HELPER PARTS FOR FUNCTION
    def save_and_report(df, file_main,save_as):
        '''
        save df in desired format.
        Takes:
        DataFrame
        file main part of name, without extension
        format designator string

        Tries tsv if nothing matches allowed settings.

        returns: nothing, just does and reports
        '''
        if save_as.lower() == 'excel':
            try:
                import openpyxl
            except ImportError as iE:
                sys.stderr.write("Python Excel module 'openpyxl' not found. \nIf working in Jupyter notebook, run `!pip install openpyxl` without quotes in another cell.\nElse run on your command line without exclmation point.")
                sys.exit(1)
            df.to_excel(file_main+".xlsx",index = False) # after openpyxl installed
            sys.stderr.write("\nResults saved as "+file_main+".xlsx.")
        elif save_as.lower() == 'csv':
            df.to_csv(file_main+"csv",index = False)
            sys.stderr.write("\nResults saved as "+file_main+".csv.")
        elif save_as.lower() == 'do_not':
            sys.stderr.write("\nResults not saved as file since `do_not` assigned for `save_as`.")
        else:
            # if `tsv` or any other setting
            df.to_csv(file_main+".tsv", sep='\t',index = False)
            sys.stderr.write("\nResults saved as "+file_main+".tsv.")



    # MAIN PART OF FUNCTION
    # Preliminary check of lists.
    # The lists must be equal in length for this to work as written for now. 
    # (Duplicates will be checked for below.)
    assert len(lizt1) == len(lizt2), "The ranked lists must be equal in size. The provided lists are not equal in length."
    import sys
    if 'pd' not in sys.modules:
        import pandas as pd
    # First part is accounting:
    # Specify list of dataframes, and columns to use for later
    dfs_to_make = []
    col_headers_for_each_df = [
                            (
                            'item_l1',
                            'pos_l1',
                            'pos_l2',
                            '∆l1>l2'
                            ),
                            (
                            'item_l2',
                            'pos_l2',
                            'pos_l1',
                            '∆l2>l1'
                            )
                            ]
    # Process each list
    the_2_lists = [lizt1,lizt2]
    for indx, curr_lizt in enumerate(the_2_lists):
        # Verify no duplicates in each list
        len(curr_lizt) == len(set(curr_lizt))
        assert len(curr_lizt) == len(set(
            curr_lizt)), "Lists cannot contain duplicates. The provided list #{} contains duplicates".format(indx)
        other_lizt = the_2_lists[not indx] #works since 0 and 1 are equivalent
        # to True and False booleans; I cannot recall where I saw a trick like
        # this but useful here for toggle.
        # Make lists for recording accounting
        item_list = []
        item_pos_in_the_list = []
        item_pos_in_other_list = []
        item_change_relative_the_list = []
        #collect data relative current list
        for iindx, item in enumerate(curr_lizt):
            item_list.append(item)
            item_pos_in_the_list.append(iindx+1) #`+1` to keep number in report 
            #matching natural language where first item is numbered 1
            pos_in_other_list = other_lizt.index(item)
            item_pos_in_other_list.append(pos_in_other_list+1) #`+1` to keep 
            #number in report matching natural language where first item #1
            #print((pos_in_other_list - iindx)) # FOR DEBUNGGING ONLY
            item_change_relative_the_list.append((pos_in_other_list - iindx))
        #store results as dataframe
        dfs_to_make.append(pd.DataFrame(list(zip(
            item_list,
            item_pos_in_the_list,
            item_pos_in_other_list, 
            item_change_relative_the_list)),
            columns=col_headers_for_each_df[indx])
                        )
    # Concatenate dataframes side-by-side
    df_account = pd.concat((dfs_to_make[0], dfs_to_make[1]),axis=1)
    # Save dataframe
    import os
    output_file1_main = os.path.splitext(output_file1)[0] #gets without 
    # extension so that I can handle setting without relying on user
    save_and_report(df_account, output_file1_main,save_as)

    # Second part is making an accounting of the distribution of shifts:
    # focus relative first list because shifts considered from other direction 
    # will just be negative direction shifts for the same items.
    df_shifts = dfs_to_make[0][["∆l1>l2"]]
    df_shifts = df_shifts.rename(columns={'∆l1>l2':'shift'})
    df_shifts.sort_values('shift', ascending=True, inplace=True)
    df_shifts = df_shifts.reset_index(drop=True) #set index to match re-sorted
    #print (df_shifts) #FOR DEBUGGING
    # Save dataframe
    output_file2_main = os.path.splitext(output_file2)[0] #gets without 
    # extension so that I can handle setting without relying on user
    save_and_report(df_shifts, output_file2_main,save_as)


    

    if return_dataframes:
        return df_account, df_shifts
        #return df_account, df_distribution

def main():
    """ Main entry point of the script """
    pass

if __name__ == "__main__":
    """ This is executed when run from the command line """
    pass

'''
# FOR TESTING
l1 = ["a","c","b"]
l2 = ["a","b","c"]
generate_reports_for_ranked_lists_pos(l1,l2)

l3 = ["a","c","b","d","e","f","g","h"]
l4 = ["a","b","d","e","f","g","h","c"]
df_r1,df_r2 = generate_reports_for_ranked_lists_pos(l3,l4,output_file1 = "oth_ranked list accounting.tsv",return_dataframes = True)
df_r2.describe()
dffreq = df_r2['shift'].value_counts().reset_index() # column 'amount of rows shifted' in 
# this case were integers but strings and maybe even floats if unique, see https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.value_counts.html
dffreq.columns = ['shift', 'count']
dffreq
# But frequency dataframe not needed as can just visualize directly from shifts dataframe
ax = df_r2.hist();
ax[0][0].set_xlabel("shift") # from https://stackoverflow.com/a/43239901/8508004
ax[0][0].set_ylabel("count") # from https://stackoverflow.com/a/43239901/8508004
ax[0][0].set_title("Distribution of shifts") #just tried it based on matplotlib and how set labels of axes above
# or as shown in current documentation, and combining with matplotlib settings
ax = df_r2.plot.hist(ec=(0.3,0.3,0.3,0.65),legend=False)
ax.set_xlabel("shift")
ax.set_ylabel("frequency")
ax.set_title("Distribution of shifts");
''';



