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

import multiprocessing

debug_bool = False

stop_words = ["0o", "0s", "3a", "3b", "3d", "6b", "6o", "a", "a1", "a2", "a3", "a4", "ab", "able", "about", "above", "abst", "ac", "accordance", "according", "accordingly", "across", "act", "actually", "ad", "added", "adj", "ae", "af", "affected", "affecting", "affects", "after", "afterwards", "ag", "again", "against", "ah", "ain", "ain't", "aj", "al", "all", "allow", "allows", "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "amoungst", "amount", "an", "and", "announce", "another", "any", "anybody", "anyhow", "anymore", "anyone", "anything", "anyway", "anyways", "anywhere", "ao", "ap", "apart", "apparently", "appear", "appreciate", "appropriate", "approximately", "ar", "are", "aren", "arent", "aren't", "arise", "around", "as", "a's", "aside", "ask", "asking", "associated", "at", "au", "auth", "av", "available", "aw", "away", "awfully", "ax", "ay", "az", "b", "b1", "b2", "b3", "ba", "back", "bc", "bd", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "begin", "beginning", "beginnings", "begins", "behind", "being", "believe", "below", "beside", "besides", "best", "better", "between", "beyond", "bi", "bill", "biol", "bj", "bk", "bl", "bn", "both", "bottom", "bp", "br", "brief", "briefly", "bs", "bt", "bu", "but", "bx", "by", "c", "c1", "c2", "c3", "ca", "call", "came", "can", "cannot", "cant", "can't", "cause", "causes", "cc", "cd", "ce", "certain", "certainly", "cf", "cg", "ch", "changes", "ci", "cit", "cj", "cl", "clearly", "cm", "c'mon", "cn", "co", "com", "come", "comes", "con", "concerning", "consequently", "consider", "considering", "contain", "containing", "contains", "corresponding", "could", "couldn", "couldnt", "couldn't", "course", "cp", "cq", "cr", "cry", "cs", "c's", "ct", "cu", "currently", "cv", "cx", "cy", "cz", "d", "d2", "da", "date", "dc", "dd", "de", "definitely", "describe", "described", "despite", "detail", "df", "di", "did", "didn", "didn't", "different", "dj", "dk", "dl", "do", "does", "doesn", "doesn't", "doing", "don", "done", "don't", "down", "downwards", "dp", "dr", "ds", "dt", "du", "due", "during", "dx", "dy", "e", "e2", "e3", "ea", "each", "ec", "ed", "edu", "ee", "ef", "effect", "eg", "ei", "eight", "eighty", "either", "ej", "el", "eleven", "else", "elsewhere", "em", "empty", "en", "end", "ending", "enough", "entirely", "eo", "ep", "eq", "er", "es", "especially", "est", "et", "et-al", "etc", "eu", "ev", "even", "ever", "every", "everybody", "everyone", "everything", "everywhere", "ex", "exactly", "example", "except", "ey", "f", "f2", "fa", "far", "fc", "few", "ff", "fi", "fifteen", "fifth", "fify", "fill", "find", "fire", "first", "five", "fix", "fj", "fl", "fn", "fo", "followed", "following", "follows", "for", "former", "formerly", "forth", "forty", "found", "four", "fr", "from", "front", "fs", "ft", "fu", "full", "further", "furthermore", "fy", "g", "ga", "gave", "ge", "get", "gets", "getting", "gi", "give", "given", "gives", "giving", "gj", "gl", "go", "goes", "going", "gone", "got", "gotten", "gr", "greetings", "gs", "gy", "h", "h2", "h3", "had", "hadn", "hadn't", "happens", "hardly", "has", "hasn", "hasnt", "hasn't", "have", "haven", "haven't", "having", "he", "hed", "he'd", "he'll", "hello", "help", "hence", "her", "here", "hereafter", "hereby", "herein", "heres", "here's", "hereupon", "hers", "herself", "hes", "he's", "hh", "hi", "hid", "him", "himself", "his", "hither", "hj", "ho", "home", "hopefully", "how", "howbeit", "however", "how's", "hr", "hs", "http", "hu", "hundred", "hy", "i", "i2", "i3", "i4", "i6", "i7", "i8", "ia", "ib", "ibid", "ic", "id", "i'd", "ie", "if", "ig", "ignored", "ih", "ii", "ij", "il", "i'll", "im", "i'm", "immediate", "immediately", "importance", "important", "in", "inasmuch", "inc", "indeed", "index", "indicate", "indicated", "indicates", "information", "inner", "insofar", "instead", "interest", "into", "invention", "inward", "io", "ip", "iq", "ir", "is", "isn", "isn't", "it", "itd", "it'd", "it'll", "its", "it's", "itself", "iv", "i've", "ix", "iy", "iz", "j", "jj", "jr", "js", "jt", "ju", "just", "k", "ke", "keep", "keeps", "kept", "kg", "kj", "km", "know", "known", "knows", "ko", "l", "l2", "la", "largely", "last", "lately", "later", "latter", "latterly", "lb", "lc", "le", "least", "les", "less", "lest", "let", "lets", "let's", "lf", "like", "liked", "likely", "line", "little", "lj", "ll", "ll", "ln", "lo", "look", "looking", "looks", "los", "lr", "ls", "lt", "ltd", "m", "m2", "ma", "made", "mainly", "make", "makes", "many", "may", "maybe", "me", "mean", "means", "meantime", "meanwhile", "merely", "mg", "might", "mightn", "mightn't", "mill", "million", "mine", "miss", "ml", "mn", "mo", "more", "moreover", "most", "mostly", "move", "mr", "mrs", "ms", "mt", "mu", "much", "mug", "must", "mustn", "mustn't", "my", "myself", "n", "n2", "na", "name", "namely", "nay", "nc", "nd", "ne", "near", "nearly", "necessarily", "necessary", "need", "needn", "needn't", "needs", "neither", "never", "nevertheless", "new", "next", "ng", "ni", "nine", "ninety", "nj", "nl", "nn", "no", "nobody", "non", "none", "nonetheless", "noone", "nor", "normally", "nos", "not", "noted", "nothing", "novel", "now", "nowhere", "nr", "ns", "nt", "ny", "o", "oa", "ob", "obtain", "obtained", "obviously", "oc", "od", "of", "off", "often", "og", "oh", "oi", "oj", "ok", "okay", "ol", "old", "om", "omitted", "on", "once", "one", "ones", "only", "onto", "oo", "op", "oq", "or", "ord", "os", "ot", "other", "others", "otherwise", "ou", "ought", "our", "ours", "ourselves", "out", "outside", "over", "overall", "ow", "owing", "own", "ox", "oz", "p", "p1", "p2", "p3", "page", "pagecount", "pages", "par", "part", "particular", "particularly", "pas", "past", "pc", "pd", "pe", "per", "perhaps", "pf", "ph", "pi", "pj", "pk", "pl", "placed", "please", "plus", "pm", "pn", "po", "poorly", "possible", "possibly", "potentially", "pp", "pq", "pr", "predominantly", "present", "presumably", "previously", "primarily", "probably", "promptly", "proud", "provides", "ps", "pt", "pu", "put", "py", "q", "qj", "qu", "que", "quickly", "quite", "qv", "r", "r2", "ra", "ran", "rather", "rc", "rd", "re", "readily", "really", "reasonably", "recent", "recently", "ref", "refs", "regarding", "regardless", "regards", "related", "relatively", "research", "research-articl", "respectively", "resulted", "resulting", "results", "rf", "rh", "ri", "right", "rj", "rl", "rm", "rn", "ro", "rq", "rr", "rs", "rt", "ru", "run", "rv", "ry", "s", "s2", "sa", "said", "same", "saw", "say", "saying", "says", "sc", "sd", "se", "sec", "second", "secondly", "section", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sensible", "sent", "serious", "seriously", "seven", "several", "sf", "shall", "shan", "shan't", "she", "shed", "she'd", "she'll", "shes", "she's", "should", "shouldn", "shouldn't", "should've", "show", "showed", "shown", "showns", "shows", "si", "side", "significant", "significantly", "similar", "similarly", "since", "sincere", "six", "sixty", "sj", "sl", "slightly", "sm", "sn", "so", "some", "somebody", "somehow", "someone", "somethan", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "sp", "specifically", "specified", "specify", "specifying", "sq", "sr", "ss", "st", "still", "stop", "strongly", "sub", "substantially", "successfully", "such", "sufficiently", "suggest", "sup", "sure", "sy", "system", "sz", "t", "t1", "t2", "t3", "take", "taken", "taking", "tb", "tc", "td", "te", "tell", "ten", "tends", "tf", "th", "than", "thank", "thanks", "thanx", "that", "that'll", "thats", "that's", "that've", "the", "their", "theirs", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "thered", "therefore", "therein", "there'll", "thereof", "therere", "theres", "there's", "thereto", "thereupon", "there've", "these", "they", "theyd", "they'd", "they'll", "theyre", "they're", "they've", "thickv", "thin", "think", "third", "this", "thorough", "thoroughly", "those", "thou", "though", "thoughh", "thousand", "three", "throug", "through", "throughout", "thru", "thus", "ti", "til", "tip", "tj", "tl", "tm", "tn", "to", "together", "too", "took", "top", "toward", "towards", "tp", "tq", "tr", "tried", "tries", "truly", "try", "trying", "ts", "t's", "tt", "tv", "twelve", "twenty", "twice", "two", "tx", "u", "u201d", "ue", "ui", "uj", "uk", "um", "un", "under", "unfortunately", "unless", "unlike", "unlikely", "until", "unto", "uo", "up", "upon", "ups", "ur", "us", "use", "used", "useful", "usefully", "usefulness", "uses", "using", "usually", "ut", "v", "va", "value", "various", "vd", "ve", "ve", "very", "via", "viz", "vj", "vo", "vol", "vols", "volumtype", "vq", "vs", "vt", "vu", "w", "wa", "want", "wants", "was", "wasn", "wasnt", "wasn't", "way", "we", "wed", "we'd", "welcome", "well", "we'll", "well-b", "went", "were", "we're", "weren", "werent", "weren't", "we've", "what", "whatever", "what'll", "whats", "what's", "when", "whence", "whenever", "when's", "where", "whereafter", "whereas", "whereby", "wherein", "wheres", "where's", "whereupon", "wherever", "whether", "which", "while", "whim", "whither", "who", "whod", "whoever", "whole", "who'll", "whom", "whomever", "whos", "who's", "whose", "why", "why's", "wi", "widely", "will", "willing", "wish", "with", "within", "without", "wo", "won", "wonder", "wont", "won't", "words", "world", "would", "wouldn", "wouldnt", "wouldn't", "www", "x", "x1", "x2", "x3", "xf", "xi", "xj", "xk", "xl", "xn", "xo", "xs", "xt", "xv", "xx", "y", "y2", "yes", "yet", "yj", "yl", "you", "youd", "you'd", "you'll", "your", "youre", "you're", "yours", "yourself", "yourselves", "you've", "yr", "ys", "yt", "z", "zero", "zi", "zz"]
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
    try:
        page = requests.get(url, timeout=10)
    except requests.exceptions.Timeout:
        return {}
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
                if not any(_.isdigit() for _ in s):
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
    print("webscraping", url)

    sample = grab_text(url)
    if not sample:
        return [[], [], [], [], []]
    # input()
    sample = [[k, v] for k, v in sample.items()]  # convert dictionary into a sortable list

    # range(a, b, c)
    # a = start, b = end, c = increment
    # slicing -- [a:b:c]

    # types of sorts
    #sample = sorted(sample, key=lambda x: x[0])  # sorted alphabetically
    # sample = sorted(sample, key=lambda x: x[0])[::-1] #sorted alphabetically in reverse
    # sample = sorted(sample, key=lambda x: x[1]) #sorted based on most used(least to greatest)
    # sample = sorted(sample, key=lambda x: x[1])[::-1] #sorted based on most used in reverse
    sample = sorted(sample, key=lambda x: len(x[0]))[::-1] #sorted by word length

    average = 0
    size = 0
    biggest = ""
    common = ["", 0]
    for k, v in sample:
        print(k, ":", v)
        average += len(k)

        if k not in stop_words:
            size += v
            if v > common[1]:
                common = [k, v]
        if len(k) > len(biggest):
            biggest = k



    print("")
    print("Average Word Count:", average/size)
    print("biggest word:      ", biggest)
    print("Most common word:  ", common[0])
    print("\twith occurence:", common[1])

    temp = [sample, average/size, biggest, common[0], common[1]]
    return temp

# input()
def timeoutscrape():
    pass

if __name__ == "__main__":
    urls = ["https://www.cfr.org/global-conflict-tracker/conflict/conflict-ukraine",
            "https://www.smithsonianmag.com/science-nature/what-math-180975882/",
            "https://science.howstuffworks.com/transport/engines-equipment/maglev-train.htm",
            'https://www.cnn.com/style/article/pokemon-design-25/index.html',
            'https://www.minecraft.net/en-us'
            ]
    webscrape(urls[-1])
