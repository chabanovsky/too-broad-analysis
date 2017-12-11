### Analysis (clustering) of the questions that have been closed as too broad on Stack Overflow in Russian. 

This a small helper tool that assists in an initiative on Stack Overflow in Russian that proposes the comunity builds set of wiki questions. This tools should help to test an idea that some of such questions could be based on the questions that have been closed as too broad. For more info, please check [a meta post](https://ru.meta.stackoverflow.com/questions/6420/).


### What is this tool about?

This little app does the following:

1. The app gets a cvs–file of the questions that have been closed as too broad. The file downloaded from [SEDE](https://data.stackexchange.com/).
2. Each question is a document. Literally a document contains a question's bodyl, title, and tags.
3. The app builds one global dictionary of words from all documents.
4. Additionally it builds a dictionary per document.
5. The app calculates a TF parapetr for each word in a documnet (per document) and an IDF for all words in the global dictionary ([more info on Wikipedia](https://en.wikipedia.org/wiki/Tf%E2%80%93idf)).
6. The app creates a vector representation for each document.
7. The app creates set of closed vectors based on cosine between them with the threshold of 0.91.

### Results

Results are availble in a [meta post]() and on [our exeprimental server](http://assets.rudevs.ru/experiments/too-broad-analysis).
