import sys

from urlparse import urlparse, urljoin
from random import randint
import urllib

debug = 0
        
def headers(url):
    hdrs = getHeaders(url)    
    for header in hdrs:
        if header.startswith('Server') \
            and header.find('Zope') > 0:
            if debug: print "Zope HTTP Header found"  
            return 1
          
def copyright(url):
    """ Get the copyright page """
    url = urljoin(url, '/manage_copyright')
    data = urllib.urlopen(url).read()
    if data.find('Zope Corporation') > 0:
        if debug: print "Copyright page found"
        return 1
                
def error(url):
    """ Get an error page (hopefully) and examine output """
    url = urljoin(url, '/testing404.' + str(randint(0, 1000)))
    hdrs = getHeaders(url)    
    for header in hdrs:
        if header.startswith('Bobo-Exception'):
            if debug: print "Bobobase errors found in header"            
            return 1

def getHeaders(url):    
    """ Get headers convenience function """
    opener = urllib.FancyURLopener({})
    page  = opener.open(url)
    return page.headers.headers               
                      
def usage():
    print """Usage: iszope.py URL"""
    sys.exit()

def examine(url):
    p = list(urlparse(url))
    if not p[0]:
        url = 'http://' + url

    return headers(url) or copyright(url) or error(url)

def test():
    urls = [
        ['www.zope.org', 1],
        ['www.zopezen.org', 1],
        ['www.plone.org', 1],
        ['www.perl.com', 0],
        ['www.slashdot.com', 0],
        # ones that use Zope in the backend but
        # front in a way that we can't detect yet 
        # (and may never be able to)
        ['www.boston.com', 0],
        ['www.activestate.com', 0],
        ]
        
    for url, result in urls:
        print "** Testing", url
        if result:
            assert examine(url), "%s is not showing as a Zope site"
        else:
            assert not examine(url), "%s is showing as a Zope site"
    
if __name__=='__main__':
    #test()
    debug = 1
    if len(sys.argv) < 2: usage()
    url = sys.argv[1]
    examine(url)
