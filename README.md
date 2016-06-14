# text_mining
my general text mining and text manipulation Python scripts



## Description of each script

- `find_overlap_in_lists.py`

> lists --> list of shared items  
Takes files with items listed one item to a line and determines items that occur in all the lists. Thus, it identifies only those items shared by all the lists of items. It was intended to be used for lists of genes, it but can work for any type of list with the caveat that the case of the shared items will be converted to all uppercase in the produced results unless an optional flag `--nochange` is used to override this change which is done to make comparison more robust.  
A file listing the shared items (genes) will be produced.  
Note, if using with yeast genes, probably best to use my script `geneID_list_to_systematic_names.py`, found in [my yeastmine-related code repository](https://github.com/fomightez/yeastmine) to convert all to yeast systematic names so that the lists are standardized before running `find_overlap_in_lists.py`.  
A related script, `find_overlap_in_lists_with_Venn.py`, will do all this script will do plus when comparing 2, 3, or 4 lists it depict the relationships among the lists in a Venn diagram.

---

-`find_overlap_in_lists_with_Venn.py`
>  lists --> list of shared items and a diagram showing relationships between lists  
Like `find_overlap_in_lists.py` (see above) but for comparisons involving 2, 3, or 4 list documents it produces in an image file a Venn diagram depicting the relationships of the items in the lists.  
To produce a Venn diagram for comparing lists found in four separate documents, it requires `venn4_from_github.py` (see below) in the same directory to produce a Venn diagram for comparing lists found in four separate documents. This additional script is not needed in the cases comparing two or three lists.
Note: this will not work to produce a Venn diagram on [mybinder.org](http://mybinder.org) because issues with `matplotlib` despite the fact the image is set to be saved as a file be default.

---


- `pull_MATCHING_data_from_files_in_directory.py`

> pertinent lines in several files --> all those lines in one file  
`pull_MATCHING_data_from_files_in_directory.py` takes a directory as an argument and mines for lines in thar file matching the text of interest. It only mines the files that match constraints set for the file names. All the lines get saved to ine file.

For the current version, the text of interest to match and the file name constraints are set as user set values in the code.

---


- `venn4_from_github.py`

> slightly modified from the original by Kristoffer Sahlin [here](https://github.com/ksahlin/pyinfor/blob/master/venn.py) to be used with `find_overlap_in_lists_with_Venn.py`  



Related scripts
---------------

Since data mining and text manipulations are at the heart of most of my computational endeavors, several other of my code repositories hold code related to text mining/text manipulation. Here are some:

- [My YeastMine code repository](https://github.com/fomightez/yeastmine) 

- [My sequence work repository](https://github.com/fomightez/sequencework)

- [My structure work repository](https://github.com/fomightez/structurework)
