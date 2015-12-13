#################################################################
# Example 08: Rename labels and merge
#################################################################

set rcwd data

load csv STI_2015.csv as STI

cast Open in STI as nonalpha

select from STI as STI_Low where Open < 820
select from STI as STI_High where Open > 2000

select from STI_Low as STI_A
merge labels from STI_High to STI_A

new summarize parameter as testingA
set parameter analysis_name in testingA as trialA
set parameter analytical_method in testingA as by_series
set parameter dataframe in testingA as STI_A

runplugin testingA

new STI_summarize dataframe from testingA results

show dataframe
describe STI_summarize

set ocwd
set rcwd examples

save dataframe STI_A as csv STI_A.csv
save session as tapps_manuscript.txt
