import os
import random
import re
import sys

DAMPING = 0.85 # The damping factor is the probability that the random surfer clicks on a link on the current page
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    print(corpus)

    test = transition_model(corpus, "2.html", DAMPING)
    print(test)

    # ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    # print(f"PageRank Results from Sampling (n = {SAMPLES})")
    # for page in sorted(ranks):
    #     print(f"  {page}: {ranks[page]:.4f}")
    # ranks = iterate_pagerank(corpus, DAMPING)
    # print(f"PageRank Results from Iteration")
    # for page in sorted(ranks):
    #     print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

#CORRECT WRONG OUTPUT: {'1.html': 0.037500000000000006, '2.html': 0.8875, '3.html': 0.037500000000000006, '4.html': 0.037500000000000006}

# Dictionary to store the probability distribution
    probability_distribution = {}

# If the page has no outgoing links, then the probability distribution should choose randomly among all pages with equal probability
    if len(corpus[page]) == 0:
        for page in corpus:
            probability_distribution[page] = 1 / len(corpus)
        return probability_distribution

# If the page has outgoing links, then each link should have a probability of being chosen that is proportional to the number of links on that page
    else:
        # Assign the same base probability to each page in the corpus
        for page in corpus:
            probability_distribution[page] = (1 - damping_factor) / len(corpus)
        # Adjust the probability of the links on the current page
        for link in corpus[page]:
            probability_distribution[link] += damping_factor / len(corpus[page])

    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
