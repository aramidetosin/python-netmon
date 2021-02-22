import re
url_regex = re.compile(r'(https?)://(www\.[A-za-z-]{2,256}\.[a-z]{2,6})([-a-zA-Z0-9@:%_\+.~#?&//=]*)')

m = url_regex.search("https://www.my-website.com/bio?data=blah&dog=yes")
print(m.groups())
print(m.group())

print(m.group(0))
print(m.group(1))
print(m.group(2))
print(m.group(3))


fd = '''<?xml version="1.0" encoding="utf-8"?>
<mydocument has="an attribute">
  <and>
    <many>elements</many>
    <many>more elements</many>
  </and>
  <plus a="complex">
    element as well
  </plus>
</mydocument>'''

import xmltodict
from pprint import pprint
doc = xmltodict.parse(fd, dict_constructor=dict)

pprint(doc)

print(xmltodict.unparse(doc, pretty=True))

print(fd == xmltodict.unparse(xmltodict.parse(fd)))


def parase_name(input):
  name_regex = re.compile(r'^(Mr\.|Mrs\.|Ms\.|Miss\.|Mdme\.) (?P<last>[A-Za-z]*) (?P<first>[A-Za-z]*)')
  matches = name_regex.search(input)
  print(matches.group())
  return matches.group('last'), matches.group('first')
  
print(parase_name('Mr. Aramide Oluwatosin'))
print(parase_name('Ms. Akande Oluwafunmito'))


def parse_date(date):
    pattern = re.compile(r'^(?P<day>\d\d)[,/.](?P<month>\d\d)[,/.](?P<year>\d{4})$')
    match = pattern.search(date)
    if match:
        return {
            "d": match.group('day'),
            "m": match.group('month'),
            "y": match.group('year'),
        }
    return None
  
print(parse_date("12/12/2012"))
print(parse_date('12.22.2020'))


def parse_email(input):
  pattern = re.compile(r'''
                       ^([a-z0-9_\.-]+)
                       @
                       ([0-9a-z\.-]+)
                       \.
                       ([a-z\.]{2,6})$
                       ''',re.X | re.IGNORECASE)
  match = pattern.search(input)
  
  return match.group(), match.group(0) ,match.group(1), match.group(2), match.groups()

print(parse_email('Aoluwatosin10@gmail.com'))




new_string = "fuck you"

print(new_string.replace('fuck', 'xxxx'))


text = "Last night Mrs. Daisy and Mr. White murdered Ms. Chow"
pattern  = re.compile(r'(Mr.|Mrs.|Ms.) ([a-z])[a-z]+', re.IGNORECASE)

# print(pattern.search(text).group())
# result = pattern.sub("REDACTED", text)

# result = pattern.sub("\g<1> REDACTED", text)
result = pattern.sub("\g<1> \g<2>", text)

print(result)


import re

def censor(word):
    pattern = re.compile(r"(frack[a-z]*)",re.I)
    new_word = pattern.sub("CENSORED", word)
    return new_word
  
print(censor('I hope you fracking die'))


from pprint import pprint

titles = [
    "Significant Others (1987)",
    "Tales of the City (1978)",
    "The Days of Anna Madrigal (2014)",
    "Mary Ann in Autumn (2010)",
    "Further Tales of the City (1982)",
    "Babycakes (1984)",
    "More Tales of the City (1980)",
    "Sure of You (1989)",
    "Michael Tolliver Lives (2007)"
]


fixed_titles = []


# pattern = re.compile(r'([\w ]+) \((\d{4})\)')
pattern = re.compile(r'(?P<title>^[\w ]+) \((?P<year>\d{4})\)')


for i in titles:
      result = pattern.sub("\g<year> - \g<title>", i)
      # result = pattern.sub("\g<2> - \g<1>", i)
      fixed_titles.append(result)

fixed_titles.sort()

pprint(fixed_titles)
