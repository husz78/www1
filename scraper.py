import requests
from bs4 import BeautifulSoup
from googlesearch import search
import os


response = requests.get("https://www.tiobe.com/tiobe-index/")
if response.status_code != 200:
    response.raise_for_status()

content = response.text
soup = BeautifulSoup(content, 'html.parser')

table = soup.table.tbody
tds_with_img = table.find_all('td', class_="td-top20")

imgs = ["https://www.tiobe.com" + td.img.get("src") for td in tds_with_img]
td_languages = [td.next_sibling for td in tds_with_img]
percentages = [language.next_sibling.text for language in td_languages]
languages = [x.text.strip() for x in td_languages]

urls = []
for language in languages:
    url = list(search(language, stop=1))[0]
    urls.append(url)

md_file = """---
title: Most Popular Programming Languages
---

"""
for i in range(len(languages)):
    md_file += f"## {languages[i]}\n"
    md_file += f"![{languages[i]}]({imgs[i]})\n"
    md_file += f"[Learn more about {languages[i]}]({urls[i]})\n"
    md_file += f"- **Percentage of popularity:** {percentages[i]}\n\n"

# Save as index.md inside 'docs' folder
with open("docs/index.md", "w", encoding="utf-8") as file:
    file.write(md_file)

print("Markdown file successfully generated: docs/index.md")
