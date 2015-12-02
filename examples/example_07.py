#################################################################
# Example 07: Rename labels and merge
#################################################################

set cwd /Users/mauriceling/Dropbox/MyProjects/tapps/data

load csv STI_2015.csv as STI

cast Open in STI as nonalpha

select from STI as L where Open < 820

select from L as LA

select from L as LB

select from L as LC

select from STI as A where Open < 880

merge labels from A to LA

rename labels in A from '1/11/1988' to dummydate

merge labels from A to LB

merge replace labels from A to LC

show dataframe
