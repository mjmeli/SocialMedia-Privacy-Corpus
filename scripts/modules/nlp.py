"""
    nlp.py
    Responsible for the NLP and summarizer using a tf-idf algorithm.
"""
import math
import nltk
import spacy
import heapq
import string
from collections import Counter, OrderedDict

# Start spacy
print("Loading NLP model...")
nlp = spacy.load('en')

# Download nltk if necessary
print("Downloading nltk (if necessary)...")
nltk.download("stopwords")

# A custom stoplist
STOPLIST = set(nltk.corpus.stopwords.words('english') + ["n't", "'s", "'m", "ca", "’s", "n’t"])

# List of symbols we don't care about
SYMBOLS = " ".join(string.punctuation).split(" ") + ["-----", "---", "...", "“", "”", "'ve", "’"]

# Summarize an article by returning a list of the n best sentences
def summarize(title, text, nLargest=10):
    # Process
    doc = nlp(text)
    title_doc = nlp(title)

    # Extract unique tokens from the document.
    # Filter out stop words, puncutation, and whitespace. If a word is part of a
    # named entity, consider the entire entity, not the individual words.
    tokens = [str(t.lemma_).lower() for t in doc if t.ent_type == 0 and not t.is_stop and not t.is_punct and t.is_space] + [str(e.lemma_).lower() for e in doc.ents]

    # additional filtering of stopwords and puncutation that spacy didn't catch
    tokens = [t for t in tokens if t not in STOPLIST]
    tokens = [t for t in tokens if t not in SYMBOLS]

    # Count the occurrences of each unique lemma in the text
    # Filter out stop words, puncutation, and whitespace
    lemma_counts = Counter()
    for token in tokens:
        lemma_counts[token] += 1

    # Score the sentences
    sentence_scores = {}
    title_lemmas = [str(w.lemma_).lower() for w in title_doc if w.ent_type == 0 and not w.is_stop and not w.is_punct and w.is_space] + [str(e.lemma_).lower() for e in title_doc.ents]
    for i, sent in enumerate(doc.sents):
        score = 0
        sent_doc = nlp(sent.text)
        sent_tokens = [str(t.lemma_).lower() for t in sent_doc if t.ent_type == 0] + [str(e.lemma_).lower() for e in sent_doc.ents]
        for token in sent_tokens:
            # tf --> Use raw relative frequencies
            tf = lemma_counts[token] / float(sum(lemma_counts.values()))
            # Give a bonus to this word if it appears in the title
            if token in title_lemmas:
                tf *= 1.1
            score += tf
        sentence_scores[i] = score

    # Print out top N sentences in order
    sentences = [s.text.strip() for s in doc.sents]
    best_sentences = heapq.nlargest(nLargest, sentence_scores, key=sentence_scores.get)
    return "\n".join([sentences[i] for i in sorted(best_sentences)])

# Pull out the top words from text, where the words are not stopwords or
# puncutation or whitespace.
def top_words(text, n=None):
    doc = nlp(text)

     # lemmatize
    tokens = [str(t.lemma_).lower() for t in doc if not t.is_stop and not t.is_punct and not t.is_space]

    # additional filtering of stopwords and puncutation that spacy didn't catch
    tokens = [t for t in tokens if t not in STOPLIST]
    tokens = [t for t in tokens if t not in SYMBOLS]

    # Take the most frequent
    freq_counts = Counter(tokens)
    if n is None:
        return list(freq_counts.keys())
    else:
        return [x[0] for x in freq_counts.most_common(n)]
