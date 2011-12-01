# Tate Larsen
# Programming in Python
# Homework # 2

import urllib.request,re,html.entities,time,sys,string
from html.parser import HTMLParser
from urllib.parse import urlparse
from collections import OrderedDict

numcrawled = 0

class ContentParser(HTMLParser):
    """ Parses links from a webpage """
    def __init__(self):
        HTMLParser.__init__(self)
        self.extract = 0
        self.links = []
        self.temp = ['','']
        self.plaintext = ""
        
    def handle_starttag(self,tag,attrs):
        attr = dict(attrs)
        if tag == 'a' and 'href' in attr:
            self.temp[0] = attr['href']
            self.extract = 1
    
    def handle_data(self,data):
        self.plaintext += " " + data + " "
        if self.extract:
            self.temp[1] += data            
           
    def handle_endtag(self,tag):
        if tag == 'a':
            self.links.append(self.temp)
            self.temp = ['','']
            self.extract = 0

            
def replace_entityrefs(content):
    """ Replace any entitryrefs with their unicode translations """
    def replaceallrefs(match):
        content = match.group(0)
        if content[:2] == '&#':
            try:
                if content[:3] == '&#x':
                    return chr(int(content[3:-1],16))
                else:
                    return chr(int(content[2:-1]))
            except Exception as e:
                #print(str(e))
                pass
        else:
            try:
                content = chr(html.entities.name2codepoint[content[1:-1]])
            except Exception as e:
                pass
        return content
        
    return re.sub("&#?\w+;",replaceallrefs,content)  

def wordFrequency(input):
    """
        Calculate the frequency with which words appear in a string.
    """   
    
    # Split the string at any non-letter
    a = re.split(r'[^a-zA-Z]', input)
    # Remove empty strings from the list (Artifact of re.split)
    a = [s for s in a if s]
    d = {}
    l = 0
    # Generate the dictionary
    for i in a:
        l += 1
        # If the string is in the dict, increase counter
        if i.lower() in d:
            d[i.lower()] += 1
        # Else add it to the dict
        else:
            d[i.lower()] = 1
    if 'n' in d:
        del d['n']
    return d
    
def crawlURL(url):
    try:
        # Handle empty url string
        if not url:
            return -1
            
        # get the page raw html
        page = urllib.request.urlopen(url)
        contents = str(page.read())
        
        # Find number of bytes retrieved
        bytesread = sys.getsizeof(contents)
        
        # Replace entity references (&...;)
        contents = replace_entityrefs(contents)
        
        # Parse the links
        parser = ContentParser()
        parser.feed(contents)
        parser.close()
        links = parser.links
        
        # Fix incomplete urls
        baseparseresult = urlparse(url)
        for i in links:
            o = urlparse(i[0])
            if o.netloc == '' and o.scheme == '':
                newlink = baseparseresult.scheme + "://" + baseparseresult.netloc + "" + baseparseresult.path[:baseparseresult.path.rfind("/")] + "/" + o.path
                #print(i[0] + "   ==>   " +baseparseresult.path[:baseparseresult.path.rfind("/")] + ":::" + o.path)
                if o.params:
                    newlink += ";" + o.params 
                if o.query:
                    newlink += "?" + o.query
                if o.fragment:
                    newlink += "#" + o.fragment
                i[0] = newlink
    
        # Remove invalid/unwanted urls
        for i in links:
            o = urlparse(i[0])
            if (o.scheme != 'http' and o.scheme != 'https'):
                links.remove(i)
        
        # Convert to tuples
        for i in links:
            i = tuple(i)
            
        # Calculate word frequencies outside tags
        wordcounts = wordFrequency(re.sub(r'<.*?>',' ', contents))
        
        # Return
        return bytesread,links,wordcounts
    except Exception as e:
        # Handle any exceptions
        #print(str(e))
        return -1,-1,-1
        
        
def crawlSite(rootURL):
    """ Crawl a URL and any linked pages on the same site """
    crawledURLs = []
    unvisitedURLs = [rootURL]
    bytesread = 0
    wordcounts = {}
    links = {}
    
    # Reset number of crawled pages to zero (for multiple calls)
    global numcrawled
    numcrawled = 0
    
    # Keep track of rootURL parts
    baseURL = urlparse(rootURL)
    
    # Keep going until all queued pages are visited
    while unvisitedURLs:
        # Grab the first unvisited page
        url = unvisitedURLs[0]
        
        # Crawl that URL
        b_temp,l_temp,w_temp = crawlURL(url)
        
        # If crawl succeded
        if b_temp != -1:
            # Increment values and keep track of url
            numcrawled += 1
            crawledURLs.append(url)
            bytesread += b_temp
            
            # Merge word count dicts
            for w,c in w_temp.items():
                if w in wordcounts:
                    wordcounts[w] += c
                else:
                    wordcounts[w] = c
            
            # Merge link lists
            for l in l_temp:
                if l[0] in links:
                    if l[1] not in links[l[0]]:
                        links[l[0]].append(l[1])
                else:
                    links[l[0]] = [l[1]]
                # queue unvisited links found this round
                if urlparse(l[0]).netloc == baseURL.netloc and baseURL.path[:baseURL.path.rfind("/")] == urlparse(l[0]).path[:urlparse(l[0]).path.rfind("/")] and l[0] not in unvisitedURLs and l[0] not in crawledURLs:
                    unvisitedURLs.append(l[0])
                    
        # Unqueue url and wait 2 seconds            
        unvisitedURLs.remove(url)
        time.sleep(2)
    
    # Convert link list to list of tuples
    l_list = []
    for l,t in links.items():
        if (urlparse(l).scheme == 'http' or urlparse(l).scheme == 'https'):
            l_list.append(tuple([l,tuple(t)]))
    
    # Return
    return bytesread,l_list,wordcounts
        
def analyzeStats(bytesread,links,wordcounts):
    # Print number of pages crawled
    print("total pages crawled successfully: %d" % numcrawled)
    
    # Sum number of words found and print
    totalwords = 0
    for w,c in wordcounts.items():
        totalwords += c
        
    print("totalwords: %d" % totalwords)
    print("")
    
    # Sort the links and words
    links = (sorted(links,key=lambda t: t[0]))
    wordcounts = OrderedDict(sorted(wordcounts.items(),key=lambda t: t[1]))
    
    # Print the URLs (handling multiple links to the same page)
    #   Justify output by longest link
    print("URLs and Link-Text:")
    print("-------------------")
    
    longestword = max([len(x[0]) for x in links])
    
    for i in links:
        for j in i[1]:
            print(i[0].ljust(longestword, " ") + "  ==>  \'" + j + "\'")
    
    # Print the word counts
    #   justify by longest word
    longestword = max([len(x) for x in wordcounts])
    
    print("")
    
    out = "Word Counts (total of %d words):" % totalwords
    print(out)
    print("".ljust(len(out), "-"))
    
    for w,c in wordcounts.items():
        print(w.ljust(longestword, " ") + "  ==>  %d" % c)
    
        
def main():
    crawlURL("http://cs.strose.edu/goldschd/")
    a,b,c = crawlSite("http://cs.strose.edu/goldschd/")
    analyzeStats(a,b,c)

if __name__ == "__main__":
    main()