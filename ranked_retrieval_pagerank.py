# homework 3
# goal: ranked retrieval, PageRank, crawling
# exports:
#   student - a populated and instantiated cs525.Student object
#   PageRankIndex - a class which encapsulates the necessary logic for
#     indexing and searching a corpus of text documents and providing a
#     ranked result set

# ########################################
# first, create a student object
# ########################################

import cs525
MY_NAME = "Weishun Chen"
MY_ANUM  = 863846968 # put your UID here
MY_EMAIL = "wchen5@wpi.edu"

# the COLLABORATORS list contains tuples of 2 items, the name of the helper
# and their contribution to your homework
COLLABORATORS = [ 
    ('Kyumin Lee', 'I tried to borrow part of code at tokenize part from HW2 written by my Professor'),
    ('Weishun Chen', 'I borrowed some part of code from my previous homework'),
    ]

# Set the I_AGREE_HONOR_CODE to True if you agree with the following statement
# "An Aggie does not lie, cheat or steal, or tolerate those who do."
I_AGREE_HONOR_CODE = True

# this defines the student object
student = cs525.Student(
    MY_NAME,
    MY_ANUM,
    MY_EMAIL,
    COLLABORATORS,
    I_AGREE_HONOR_CODE
    )


# ########################################
# now, write some code
# ########################################

import bs4 as BeautifulSoup  # you will want this for parsing html documents
import urllib.request    # I also want this...
import numpy as np    # I also want this...
import re    # need it to get number in a string

# our index class definition will hold all logic necessary to create and search
# an index created from a web directory
#
# NOTE - if you would like to subclass your original Index class from homework
# 1 or 2, feel free, but it's not required.  The grading criteria will be to
# call the index_url(...) and ranked_search(...) functions and to examine their
# output.  The index_url(...) function will also be examined to ensure you are
# building the index sanely.

class PageRankIndex(object):
    def __init__(self):
        # you'll want to create something here to hold your index, and other
        # necessary data members
        self._inverted_index = {}    # store content of each page
        self._urlname = []    # store url of each page
        self._score = []    # store pagerank score

        pass

    # index_url( url )
    # purpose: crawl through a web directory of html files and generate an
    #   index of the contents
    # preconditions: none
    # returns: num of documents indexed
    # hint: use BeautifulSoup and urllib
    # parameters:
    #   url - a string containing a url to begin indexing at
    def index_url(self, url):
        # ADD CODE HERE
        num_files_indexed = 0

        ## page content and url
        # get all anchor text link in the page
        soup = BeautifulSoup.BeautifulSoup(urllib.request.urlopen(url), "html.parser")

        for link in soup.find_all('a'):
        	self._urlname.append(link.get('href'))

        # get pagerank matrix shape
        n = len(self._urlname)
        A = np.zeros((n, n))
        P = np.zeros((n, n))
        T = np.full((n, n), 1/n)

        # open each link, build inverted index and get anchor text relationship
        for u in self._urlname:
        	url_now = url.replace('index.html', u)
        	soup_now = BeautifulSoup.BeautifulSoup(urllib.request.urlopen(url_now), "html.parser")

        	# build inverted index
        	text = soup_now.get_text()
        	token_list = self.tokenize(text)
        	token_list = list(set(token_list))    # remove duplicated token

        	for token in token_list:
        		if token in self._inverted_index:
        			self._inverted_index[token].append(num_files_indexed)
        		else:
        			self._inverted_index[token] = [num_files_indexed]

        	# pagerank update A
        	for link in soup_now.find_all('a'):
        		page_linked = link.get('href')
        		page_index = int(re.findall('\d+', page_linked)[0])
        		A[num_files_indexed, page_index] = 1

        	num_files_indexed = num_files_indexed + 1

        ## calculate pagerank importance
        # normalize A, so that each row sum = 1
        # print('matrix A is ' + str(A))

        for i in range(n):
        	row_sum = sum(A[i])
        	# print(row_sum)
        	if row_sum != 0:
        		for j in range(n):
        			A[i, j] = A[i, j]/row_sum

        # final probability matrix
        P = 0.9*A + 0.1*T
        # print('matrix P is ' + str(P))
        # print(sum(P[9]))

        # steady status
        # starting from a random page
        x0 = np.zeros(n)
        x = np.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

        while not np.array_equal(x0, x):
        	x0 = x
        	x = np.dot(x, P)

        # print('converged x is ' + str(x))
        # print(sum(x))

        # update score
        self._score = x

        # print(self._score)

        return num_files_indexed

    # tokenize( text )
    # purpose: convert a string of terms into a list of terms 
    # preconditions: none
    # returns: list of terms contained within the text
    # parameters:
    #   text - a string of terms
    def tokenize(self, text):
        # ADD CODE HERE
        token_list = []
        	
        text = text.lower()    # convert to lower case

        for character in text:
        	if not(character.isalpha() or character.isdigit()):
        		text = text.replace(character, ' ')

        token = text.split(' ')

        for i in token:
        	if i not in token_list:
        		token_list.append(i)

        return token_list

    # ranked_search( text )
    # purpose: searches for the terms in "text" in our index and returns
    #   AND results for highest 10 ranked results
    # preconditions: .index_url(...) has been called on our corpus
    # returns: list of tuples of (url,PageRank) containing relevant
    #   search results
    # parameters:
    #   text - a string of query terms
    def ranked_search(self, text):
        # ADD CODE HERE
        result = []
        # print('text = ' + str(text))

        # tokenize query text
        tokens = self.tokenize(text)
        # print('tokens are ' + str(tokens))

        # get documents that include all tokens
        list_of_list = []
        
        for token in tokens:
        	list_of_list.append(self._inverted_index[token])

        # print('list_of_list is ' + str(list_of_list))

        result_index = list_of_list[0]
        for i in range(1, len(list_of_list)):
        	result_index = list(set(result_index) & set(list_of_list[i]))

        # print('result_index is: ' + str(result_index))

        # get pagerank score, return top 10 highest rank
        for index in result_index:
        	result.append((self._urlname[index], self._score[index]))

        # print('unsorted result is' + str(result))
        result = sorted(result, key = lambda x: -x[1])
        result = result[:10]

        return result


# now, we'll define our main function which actually starts the indexer and
# does a few queries
def main(args):
    print(student)
    index = PageRankIndex()
    url = 'http://web.cs.wpi.edu/~kmlee/cs525/new10/index.html'
    num_files = index.index_url(url)
    search_queries = (
       'palatial', 'college', 'palatial college', 'college supermarket', 'famous aggie supermarket'
        )
    for q in search_queries:
        results = index.ranked_search(q)
        print("searching: %s -- results: %s" % (q, results))


# this little helper will call main() if this file is executed from the command
# line but not call main() if this file is included as a module
if __name__ == "__main__":
    import sys
    main(sys.argv)

