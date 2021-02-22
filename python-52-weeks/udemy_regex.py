import re

pattern = re.compile(r'\d{3} \d{3}-\d{4}')

result = pattern.search('Call me at 089 988-8913! or 023 255-4569')
print(result.group())

print(pattern.findall('Call me at 089 988-8913! or 023 255-4569'))

m = pattern.finditer('Call me at 089 988-8913! or 023 255-4569')
for i in m:
    print(i.group())