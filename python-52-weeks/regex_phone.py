import re

def extract_phone(input):
    pattern = re.compile(r'\b\d{3} \d{3}-\d{4}\b')
    m = pattern.search(input)
    
    if m:
        return m.group()
    return None

def extract_all_phones(input):
    pattern = re.compile(r'\b\d{3} \d{3}-\d{4}\b')
    m = pattern.findall(input)
    return m

print(extract_phone("my number is 432 567-9900"))
print(extract_phone("my number is 445 555-8888frffvf"))
print(extract_phone("my number is 432 567-990044"))
print(extract_phone("432 567-9900"))
print(extract_phone("432 567-9900 iorirr"))


print(extract_all_phones("my number is 432 567-9900 or 089 988-8913"))
print(extract_all_phones("my number is 445 555-8888frffvf"))



def is_valid_phone(input):
    pattern = re.compile(r'^\d{3} \d{3}-\d{4}$')
    m = pattern.search(input)
    
    if m:
        return True
    return False

print(is_valid_phone('555 444-6666'))
print(is_valid_phone("hhfd 555 444-6666"))



def is_valid_phone(input):
    pattern = re.compile(r'\b\d{3} \d{3}-\d{4}\b')
    m = pattern.fullmatch(input)
    
    if m:
        return True
    return False

print(is_valid_phone('555 444-6666'))
print(is_valid_phone("hhfd 555 444-6666"))