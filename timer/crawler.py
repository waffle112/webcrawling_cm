'''
HS - project
Timer - time how long it takes to read an article online
Chrome extension app Timer
Statistics
	users age
	complexity of the words in article
		how to ignore the words in ads
		how to ignore non-related words
		TF-idf = algorithm that gauges the IMPORTANCE of words
		Or just identify where the article starts and ends and only grab the words there

	length of article
	previous time(s) for similar articles

How to gather statistics
	user submission - account or something
	how to start timer?
	how to grab length/words of article ?
	use a server to store data? - flask probs


Plan for class
	review of the basics
	start learning about B4, and maybe regex - handles anything about the article
	Server for storing user data
	chrome extension app - how to handle timer system

'''
import requests  # only use is to grab the website from a url
from bs4 import BeautifulSoup  # webcrawling library
import re  # helps manipulate strings
import string  # help manipulate strings

debug_bool = False


# debug_bool = True
# OLD - DEPRECATED - UNNECESSARY
# grabs ALL text, including ads and extra stuff
def decompose(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    # print(soup)
    for script in soup(["script", "style"]):
        script.decompose()

    strips = list(soup.stripped_strings)
    # print(strips)
    return strips


def grab_text(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    # print(soup)

    # p = soup.find_all(lambda _: _.name in ['p'])
    p = soup.stripped_strings
    # for i in p:
    # 	print(repr(i))
    # input()
    temp = {}  # dictionary that keeps track of word frequency
    for i in p:
        stripped = repr(i)  # strip off all tags
        # print(stripped)
        for ii in stripped.split():
            # use re.sub - regex substitute
            # regex - regular expression
            # ^ = punctation
            # \w = whitespaces
            # \s = spacing symbols such as \n

            # “ was not stripped for some reason
            stripped2 = ii.strip(string.punctuation).lower().strip('“')

            if debug_bool:
                print(1, stripped2)
                input()

            # store the frequency of words

            # identify contraction words or just set them as seperate words
            # check if there is a symbol other than '

            # store contraction words as-is
            contractions = ['\'s', '\'t', '’s', '’t', '\\\'s', '\\\'t', '\\’s', '\\’t']
            # if the word is a contraction -> replace the weird apostraphe with the computers
            if any(c in stripped2 for c in contractions):
                stripped2 = stripped2.replace('\\', '').replace('’', '\'').replace('‘', '\'')
            else:
                stripped2 = re.sub(r'[^\w\s]', ' ', stripped2.lower())

            stripped2 = stripped2.split()
            if debug_bool:
                print(2, stripped2)
                input()

            for s in stripped2:
                try:
                    temp[s] += 1
                except KeyError:
                    temp[s] = 1

        # WARNING - There is memory limit
        # if an article contains way to much words - the program may not function

    return temp


'''
Some websites have prevention measures for bots requesting their website 
This is mainly to prevent DDOS/theft 

"https://www.sciencedirect.com/science/article/pii/S1878535217300990",
"https://history.state.gov/countries/all"

IN addition, lets test out the program by looking at multiple different websites 

Stress testing

1)website with a calendar 
2)website with esoteric words/languages (pokemon, social media, math-related articles)
3)website that may crash the program 

this website is weird
https://www.cnn.com/style/article/pokemon-design-25/index.html
	doesn't use p elements but div with a special class 
	so how to manage this type of website? 

'''


def webscrape(url):
    sample = grab_text(url)

    # input()
    sample = [[k, v] for k, v in sample.items()]  # convert dictionary into a sortable list

    # range(a, b, c)
    # a = start, b = end, c = increment
    # slicing -- [a:b:c]

    # types of sorts
    sample = sorted(sample, key=lambda x: x[0])  # sorted alphabetically
    # sample = sorted(sample, key=lambda x: x[0])[::-1] #sorted alphabetically in reverse
    # sample = sorted(sample, key=lambda x: x[1]) #sorted based on most used(least to greatest)
    # sample = sorted(sample, key=lambda x: x[1])[::-1] #sorted based on most used in reverse
    # sample = sorted(sample, key=lambda x: len(x[0])) #sorted by word length

    for k, v in sample:
        print(k, ":", v)


# input()

if __name__ == "__main__":
    urls = ["https://www.cfr.org/global-conflict-tracker/conflict/conflict-ukraine",
            "https://www.smithsonianmag.com/science-nature/what-math-180975882/",
            "https://science.howstuffworks.com/transport/engines-equipment/maglev-train.htm",
            'https://www.cnn.com/style/article/pokemon-design-25/index.html',

            ]
    webscrape(urls[2])
