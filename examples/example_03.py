#################################################################
# Example 03: Type casting and data extraction (selection)
#################################################################

set cwd /Users/mauriceling/Dropbox/MyProjects/tapps/data

load csv STI_2015.csv as STI

cast Open in STI as nonalpha

select from STI as STI_H where Open > 3000

select from STI as STI_L where Open < 820

select from STI as STI_01 where Volume = '0'

cast all in STI as nonalpha

select from STI as STI_02 where Volume = 0
