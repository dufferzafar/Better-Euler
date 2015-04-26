from __future__ import division

import os
import json
import math

from textblob import TextBlob as tb


def tf(word, blob):
    """
    Text Frequency.

    Find normalized occurrence of a word in a blob.
    """
    return blob.words.count(word) / len(blob.words)


def n_containing(word, bloblist):
    """ Find number of blobs which contain a particular word. """
    return sum(1 for blob in bloblist if word in blob)


def idf(word, bloblist):
    """
    Inverse Document Frequency.

    The inverse document frequency is a measure of how much
    information the word provides, that is, whether the term
    is common or rare across all documents.
    """
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))


def tfidf(word, blob, bloblist):
    """
    Text Frequency Inverse Document Frequency.

    http://en.wikipedia.org/wiki/Tf-idf
    """
    return tf(word, blob) * idf(word, bloblist)


# Create a bloblist of all the problems
bloblist = []
for f in range(1, 502):
    with open("data/" + str(f) + ".json") as fp:
        bloblist.append(tb(json.load(fp)["text"]))

# A set of all tags
tags = set()

for i, blob in enumerate(bloblist):
    # Tf-Idf of every word
    scores = {word: tfidf(word, blob, bloblist) for word in blob.words
              if (len(word) > 4) and (not any(i.isdigit() for i in word))}

    # Sort the dictionary based on scores
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # Print the top 5 words of every blob
    for word, score in sorted_words[:1]:
        tags.add(word.lower())

print(tags)
