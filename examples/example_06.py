#################################################################
# Example 06: Rename series and merge
#################################################################

set cwd /Users/mauriceling/Dropbox/MyProjects/tapps/data

load csv STI_2015.csv as STI

cast Open in STI as nonalpha

select from STI as L where Open < 820

select from L as L1

rename series in L1 from Open to OpenDup

merge series OpenDup from L1 to L

show dataframe
 