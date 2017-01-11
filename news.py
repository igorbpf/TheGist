import feedparser
import nltk
import requests
from bs4 import BeautifulSoup as bs
from sklearn.feature_extraction.text import TfidfVectorizer
import networkx as nx
import numpy as np
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk import word_tokenize
from string import punctuation
from detection import detect_language

def rss_to_links(rssurl):
    """Input: url of the rss.
        Output: list of links to news."""
    feed = feedparser.parse(rssurl)
    return [link['link'] for link in feed['entries']]

def scrape_page(url):
    """Input: url of news.
        Output: Text from the page."""
    page = requests.get(url).text
    tree = bs(page, "html.parser")
    title = tree.title.string
    for script in tree(["script","style"]):
        script.extract()
    all_p = tree.find_all('p')
    t0 = None
    for tag in all_p:
        if t0 == None:
            t0 = tag
        else:
            t1 = tag.parent
            if t1 == t0.parent:
                content = t1
                break
            else:
                t0 = tag

    paragraphs = content.find_all('p')
    filtered_paragraphs = [paragraph.get_text() for paragraph in paragraphs]
    size_paragraphs = [len(para) for para in filtered_paragraphs]
    size_cut = int(sum(size_paragraphs)/len(size_paragraphs))
    texts = [text for text in filtered_paragraphs if len(text) > int(size_cut)]
    final_text = []
    for text in texts:
        if False:
            break
        final_text.append(text)
    return title, " ".join(final_text)


def textrank(document, language):

    #print document
    nltk.data.path.append('./nltk_data/')
    sentence_tokenizer = nltk.data.load("tokenizers/punkt/" + language + ".pickle")
    sentences = sentence_tokenizer.tokenize(document)

    stopword = stopwords.words(language)
    punct = list(punctuation)
    non_words = stopword + punct
    non_words = set(non_words)

    # Stemmer
    stemmer = SnowballStemmer(language)
    filtered_sentences = []

    if language != "turkish":
        for sentence in sentences:
            words = word_tokenize(sentence)
            words = [stemmer.stem(word.lower()) for word in words if word not in non_words]
            #words = [(word.lower()) for word in words if word not in non_words]
            sentence = " ".join(words)
            filtered_sentences.append(sentence)
    else:
        for sentence in sentences:
            words = word_tokenize(sentence)
            #words = [stemmer.stem(word.lower()) for word in words if word not in non_words]
            words = [(word.lower()) for word in words if word not in non_words]
            sentence = " ".join(words)
            filtered_sentences.append(sentence)

    normalized = TfidfVectorizer(ngram_range=(1,1)).fit_transform(filtered_sentences)
    similarity_graph = normalized * normalized.T

    nx_graph = nx.from_scipy_sparse_matrix(similarity_graph)
    scores = nx.pagerank(nx_graph)
    return sorted(((scores[i], i, s) for i,s in enumerate(sentences)),
                  reverse=True)

def summarization(ranked):
    cut = 3
    size = len(ranked)
    if size >= cut:
        shrink =  int(size ** 0.55) #int(0.40*size)#size/cut
        most_relevant = ranked[:shrink]
    else:
        most_relevant = ranked
    most_relevant.sort(key=lambda x:x[1])
    sentences = []
    for ranks in most_relevant:
        sentences.append(ranks[2])
    return " ".join(sentences)


def get_summary(url):
    """Input: url
    Output: summary"""

    title, document = scrape_page(url)
    language = detect_language(document)
    ranked = textrank(document, language)
    summary = summarization(ranked)
    return title, summary.strip(), language

def wordrank(document, language):

    #print document
    nltk.data.path.append('./nltk_data/')
    sentence_tokenizer = nltk.data.load("tokenizers/punkt/" + language + ".pickle")
    sentences = sentence_tokenizer.tokenize(document)

    stopword = stopwords.words(language)
    punct = list(punctuation)
    non_words = stopword + punct
    non_words = set(non_words)

    # Stemmer
    #stemmer = RSLPStemmer()
    filtered_sentences = []

    for sentence in sentences:
        words = word_tokenize(sentence)
        #words = [stemmer.stem(word.lower()) for word in words if word not in non_words]
        words = [(word.lower()) for word in words if word not in non_words]
        sentence = " ".join(words)
        filtered_sentences.append(sentence)
    vectorizer = TfidfVectorizer(ngram_range=(1,1))
    normalized = vectorizer.fit_transform(filtered_sentences)
    similarity_graph = normalized.T * normalized

    nx_graph = nx.from_scipy_sparse_matrix(similarity_graph)
    scores = nx.pagerank(nx_graph)
    wordrank = []
    for word, feature in vectorizer.vocabulary_.iteritems():
        wordrank.append((scores[feature], word))
    wordrank.sort(key=lambda x: x[0], reverse=True)
    return wordrank

def keyword_extraction(ranked):

    keywords = [word[1] for word in ranked]
    return keywords[:5]

def get_keywords(url):
    """Input: url
    Output: summary"""

    _, document = scrape_page(url)
    language = detect_language(document)
    ranked = wordrank(document, language)
    keywords = keyword_extraction(ranked)
    return keywords


# TODO: deal with pages with small content like: http://gshow.globo.com/novelas/rock-story/Vem-por-ai/noticia/2017/01/banda-44-ganha-nova-integrante.html
# TODO: french codification