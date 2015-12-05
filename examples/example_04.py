#################################################################
# Example 04: Data frame duplication and deletion
#################################################################

@include example_03.py

select from STI as STI_D

show dataframe

select from STI as STI_D1

delete dataframe STI_D1

describe STI
