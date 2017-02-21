import feedparser
import nltk
import requests
from bs4 import BeautifulSoup as bs
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
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
    """
    Input: url
    Output: title, text, top image and its caption.
    """
    page = requests.get(url).text
    tree = bs(page, 'html.parser')

    # Remove script and style tags
    for script in tree(['script','style']):
        script.extract()

    # Get title
    title = tree.title.string

    # Get top image if there is any
    try:
        content_images = tree.find_all('figure')
        content_image = content_images[0]
        top_image = content_image.find_all('img')
        top_image = re.findall(r'src="\S+"',str(top_image[0]))[0][4:]
        image_caption = content_image.find_all('figcaption')[0].get_text()
    except:
        top_image = None
        image_caption = None

    # Geta all p tags
    ps = tree.find_all('p')

    text = []
    # Get parents of the p tags
    parents = set([p.parent for p in ps])
    # Iterate over the parents and try to get the p tags with depth of 1.
    for parent in parents:
        pss = [p for p in parent.find_all('p', recursive=False) if len(p.get_text().split()) > 10]
        text.append(pss)
    # Get only list with length greater than one.
    useful = [txt for txt in text if len(txt) > 1]
    news = []
    for dummy in useful:
        news = news + [use.get_text() for use in dummy]
    # join into a single string
    plain_text = " ".join(news)

    return title, plain_text, top_image, image_caption


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
    #rows, columns = normalized.shape
    #svd = TruncatedSVD(n_components=100, n_iter=10, random_state=42)
    #normalized = svd.fit_transform(normalized)
    #print normalized.shape
    #print type(normalized)
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

    title, document, _, _ = scrape_page(url)
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

    _, document, _, _ = scrape_page(url)
    language = detect_language(document)
    ranked = wordrank(document, language)
    keywords = keyword_extraction(ranked)
    return keywords


# TODO: deal with pages with small content like: http://gshow.globo.com/novelas/rock-story/Vem-por-ai/noticia/2017/01/banda-44-ganha-nova-integrante.html
# TODO: french codification