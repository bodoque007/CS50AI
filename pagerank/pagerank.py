import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


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
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    distribution = {page:(1-damping_factor)/len(corpus) for page in corpus.keys()}
    
    for link in corpus[page]:
        distribution[link] += damping_factor/len(corpus[page])
    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = {page:0 for page in corpus.keys()}
    current_page = random.choice(list(corpus.keys()))
    for i in range(n - 1):
        page_rank[current_page] += 1
        transitions = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(list(transitions.keys()), weights=transitions.values(), k=1)[0]
    
    page_rank2 = {key:val/n for (key, val) in page_rank.items()}
    return page_rank2


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    page_rank = {page:1/N for page in corpus.keys()}
    
    not_converged = True
    while not_converged:
        old_pr = page_rank.copy()
        not_converged = False
        for page in page_rank.keys():
            new_rank  = (1-damping_factor)/N + damping_factor*suma(corpus, page, old_pr)
            if abs(new_rank - page_rank[page]) > 0.001:
                not_converged = True
            page_rank[page] = new_rank
    return page_rank

def suma(corpus, page, page_rank):
    res = 0
    for i, links in corpus.items():
        if page in links:
            res += page_rank[i]/len(links)
        elif len(links) == 0:
            res += page_rank[i]/len(corpus)
    return res
if __name__ == "__main__":
    main()
