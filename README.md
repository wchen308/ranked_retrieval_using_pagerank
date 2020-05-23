# ranked_retrieval_using_pagerank
A collection of web pages will be crawled and their PageRank score will be calculated. Given a boolean query operator, query results will be ranked based on these PageRank scores.

## Ranked Search
This component searches for the terms in text in our index, and return at most the 10 highest-ranked results based on their PageRank scores in descending order. The returned url includes all terms in a query.

## Tokenization
Only English alphabet characters or numbers are considered as a valid element. Others are considered as token delimiters.

## Page Rank
Teleportation factor is 0.1, which means that we assume 90% of the time a web surfer follows links on a page and 10% of the time, this surfer gets bored and randomly jumps to any page with equal probability.
