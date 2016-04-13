# HCDD-Methods 
URAP spring 2016

Nancy Li - linanc@github.com

My advisor and her research team has previously assembled a data set of scholarly papers written by designers who are working on solving global development challenges through human-centered design projects. We want to leverage this data set in order to understand what the community of authors looks like. Who is publishing together? Who is publishing the most? Who is working with international co-authors? The goal is to complete the quantitative analysis with network analysis, and graph visualization techniques, and to pair this analysis with qualitative insight in order to better understand what the research landscape of design for development looks like.

-preprocess.py: counts unique number of authors in authors.txt, organizes them into csv file by authorship position
  
   -uses Python 3.4; to run in command line, input: python preprocess.py <inputfile.txt> <output.csv> 

   -assumes input file is a list of authors, where each line is a paper and authors on the same line are co-authors listed in order
  
-graphdraft.py: constructs networkX graph object for visualization; nodes represent authors and edges are co-authorship relations. Each paper's authors represent a complete subgraph.

   -see graph.png and zoom1.png, zoom2.png for png previews
