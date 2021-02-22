import re
# """
# match()

# Determine if the RE matches at the beginning of the string.

# search()

# Scan through a string, looking for any location where this RE matches.

# findall()

# Find all substrings where the RE matches, and returns them as a list.

# finditer()

# Find all substrings where the RE matches, and returns them as an iterator.

# """

# p = re.compile('[a-zA-Z0-9]+')
# print(p.match(""))

# m= p.match("tempo")
# print(m)

# print(m.group(), m.start(), m.end(), m.span())

# # match always start from zero of the provided string

# k = p.search('::: message')
# print(k, k.span(), k.group(), k.start(), k.end())


# p = re.compile(r'\d+')
# m = p.findall('12 drummers drumming, 11 pipers piping, 10 lords a-leaping')

# print(m)

# m = p.finditer('12 drummers drumming, 11 pipers piping, 10 lords a-leaping')
# for i in m:
#     print(i.span())
    

# txt = "The rain in Spain"
# x = re.search("^The.*Spain$", txt)
# print(x)


# txt = "The rain in Spain"
# x = re.findall("ai", txt)
# print(x)

# txt = "The rain in Spain"
# x = re.findall("Portugal", txt)
# print(x)

# txt = "The rain in Spain"
# x = re.search("\s", txt)

# print("The first white-space character is located in position:", x.start())

# txt = "The rain in Spain"
# x = re.search("Portugal", txt)
# print(x)