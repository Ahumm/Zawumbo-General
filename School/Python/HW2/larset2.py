# Tate Larsen
# Programming in Python
# Homework # 2

import urllib.request
import re

def crawlURL(url):
    try:
        if not url:
            return -1
        page = urllib.request.urlopen(url)
        contents = str(page.read())
        f = open("./out.txt", "w")
        f.write(contents)
        f.close()
        
        links = re.findall(r'<a href=[\'"]?([^\'" >]+)?([^<])', contents)
        print(str(links))
    except Exception:
        return -1
        
        
def main():
    crawlURL("http://cs.strose.edu/goldschd/")

if __name__ == "__main__":
    main()