from tld import get_tld
root = "http://" + get_tld("http://www.google.co.uk/news")
print root
