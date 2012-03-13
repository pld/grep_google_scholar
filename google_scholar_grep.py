import re
import time
import urllib2

BOOK_CODES = {
  'An American Dilemma': 4823972273427955690,
  'Black Metropolis': 3009150511129356197,
}

URL_PREFIX = 'http://scholar.google.com/scholar?num=100&q=&cites='
RANGE_Q = '&as_ylo='

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/9.0')]

book_code = BOOK_CODES['Black Metropolis']
counts = dict()

def year_counts(url, sleep=0):
    time.sleep(sleep)
    body = opener.open(url).read()
    m = re.search(r'of about\s*<b>(.+)</b>\..+', body)
    if not m:
      print 'Request rejected for: %s\nRetrying...' % url
      opener.addheaders = [('User-agent', 'Mozilla/9.%d' % (sleep + 1))]
      return year_counts(url, sleep + 1) if sleep < 3 else m
    return m

for i in range(1993, 2012 + 1):
    url = "%s%d%s%d" % (URL_PREFIX, book_code, RANGE_Q, i)
    m = year_counts(url)
    if m:
        n = m.group(1)
        n = int(n.replace(',', ''))
        print "%d, %d" % (i, n)
        counts[i] = n
    else:
      print 'No match for year %d' % i

print counts
