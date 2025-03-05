import requests
from bs4 import BeautifulSoup
from googlesearch import search

response = requests.get("https://www.tiobe.com/tiobe-index/")
if response.status_code != 200:
    response.raise_for_status()

content = response.text
soup = BeautifulSoup(content, 'html.parser')

table = soup.table.tbody
tds_with_img = table.find_all('td', class_="td-top20")
imgs = ["https://www.tiobe.com" + td.img.get("src") for td in tds_with_img]
td_languages = [td.next_sibling for td in tds_with_img]
percentage = [language.next_sibling.text for language in td_languages]
languages = [x.text for x in td_languages]

urls = []
for language in languages:
    url = list(search(language, stop=1))[0]
    urls.append(url)
    print("Appended url")

md_file = """---
title: Most popular programming languages
---\n"""

for i in range(len(languages)):
    md_file += f"\n## {languages[i]}\n"
    md_file += f"[![image]({imgs[i]})]({urls[i]})"
    md_file += f"\n     - Percentage of popularity: {percentage[i]}"


# print(md_file)
with open("docs/index.md", "w") as file:
    file.write(md_file)

print("File written")
