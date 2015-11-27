show plugin list
show plugin template
show session
show environment

set cwd /Users/mauriceling/Dropbox/MyProjects/tapps/data
set separator ,
set fillin None
show environment

load csv STI_20151111_19871228.csv as STI
new template parameters as testingA

pythonshell
