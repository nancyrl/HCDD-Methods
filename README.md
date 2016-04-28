# Human Centered Design for Development - Analysis of Methods 
URAP spring 2016

We have previously assembled a data set of scholarly papers written by designers who are working on solving global development challenges through human-centered design projects. We want to leverage this data set in order to understand what the community of authors looks like. Questions to be answered: Who is publishing together? Who is publishing the most? Who is working with international co-authors? The goal is to complete the quantitative analysis with network analysis and graph visualization techniques, and pair it with qualitative insight in order to better understand what the research landscape of design for development looks like.

Files use Python 3.4 and the networkX package. 

Working code: 

-preprocess.py: counts unique number of authors in authors.txt (made manually), organizes them into csv file by authorship position
  
   -to run in command line, input: python preprocess.py <inputfile.txt> <output.csv> 

   -assumes input file is a list of authors where each line is a paper and authors on the same line are co-authors listed in order
  
-graphdraft.py: constructs networkX graph object for visualization; nodes represent authors and edges are co-authorship relations

   -see graph.png and zoom1.png, zoom2.png inside the graphs folder for views

-countries.py: constructs tables listing countries and number of authors publishing per country, or number of mentions as the primary work place
