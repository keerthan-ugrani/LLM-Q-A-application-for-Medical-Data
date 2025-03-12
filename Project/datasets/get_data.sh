# This File contains the downloads steps needed to download
# the data for our project
#
# Author: Luke Voss
# Email: luke.voss@stud.uni-heidelberg.de
# Created: 04.01.2024
# Last Updated: 05.01.2024
# Version: 1.0.0
#
# Requirements:
# - Unix Environment

# Install Entrez Direct
sh -c "$(curl -fsSL ftp://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh)"

#for Windows User:
cd /mnt/c/
cd #navigate to your dataset folder
# Users/luke/OneDrive/Dokumente/UniHeidelberg/Master/Semester3/INLPT/Project_and_Assignments/Project

# Use esearch to query PubMed for articles containing "intelligence" in the title or abstract
# from 2013 to 2023, then use efetch to retrieve the results in XML format
# and redirect the output to a file named data.xml
#esearch -db pubmed -query "intelligence[Title/Abstract] AND (\"2013/01/01\"[Date - Publication] : \"2023/12/31\"[Date - Publication])" | efetch -format xml > data.xml
#esearch -db pubmed -query "intelligence [TIAB]" |efilter -mindate 2013 -maxdate 2023| efetch -format xml > data_new.xml
esearch -db pubmed -query "intelligence [TIAB]" -datetype PDAT -mindate 2013/01/01 -maxdate 2023/12/31 | efetch -format xml > data_new.xml