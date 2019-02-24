# TAPPS: Technical (Analysis) and Applied Statistics
TAPPS (pronounced as "taps") is the abbreviation for "Technical (Analysis) and Applied Statistics (System)". TAPPS is an amalgamation of two aspects: (1) the technical analysis (TA) of financial and security analysis, which is a analysis of time-series trends, such as stock and commodity prices; and (2) applied statistical analyses.

## Uses of TAPPS
In essence (short answer), TAPPS is a platform for Load-Dice-Analyze cycle: (1) Load: read in one or more data files into TAPPS, (2) Dice: extract part of the loaded data or merge data segments together, (3) Analyze: perform technical and/or statistical analyses on the original/extracted/merged data.

The long answer will go something like this...

Loading or reading one or more TAPPS-supported data files, as data source, into TAPPS is pretty standard. However, there is nothing to stop a plugin (more specficially, an importer plugin) to read data from a website; such as Yahoo Finance; or use any other data sources; such as social media data, network data, genome sequencing; or decipher some arcane data files. 

Once the data source is loaded, you are not limited to the available data extraction/slicing/merging operations of TAPPS. Nothing stops anyone from developing a plugin to segment a series of images or video clips previously loaded into TAPPS (via importer plugin, of course) into more image frames.

Then, a plugin can collate the segmented image frames into a collage based on adjacent colours and brightness intensities, before applying a border-blurring scheme to smooth out the entire collaged image.

I am sure you can think of more crazy ideas...

The short of the long... Universe is the limit with plugins.

# Driving Implementation Philosophy
The main driving philosophy of TAPPS is to be a thin platform with a multi data frame as the core data structure, and an essential data manipulation language. This implies a few things. Firstly, TAPPS in itself, has no technical analysis nor statistical analysis functions. All analytical functions are made available using plug-ins. Secondly, data frame, which can be visualized as a 2-dimensional data table, is the core data structure. However, many data frames can exist in the same session; hence, a multi data frame structure. Lastly, TAPPS has a very minimal language set for data manipulations and operations. TAPPS language is not meant to be a full or Turing-complete programming language like R.

This makes TAPPS somewhat similar in the underlying philosophy of database management systems (DBMS) and SQL. DBMS are essential platform for multi data frames, which we termed as tables. SQL is a very simple language that is not meant to be a full programming language. In fact, for SQL, with the exception of data/tables creation (the data definition aspect), nearly all of its data manipulation aspect manifest as a SELECT statement.

# License
TAPPS is licensed under GNU General Public License version 3 for non-commercial or academic use only. Separate license must be obtained for commercial, non-academic, or for-profit use.
