import requests
from bs4 import BeautifulSoup
from googlesearch import search
import time


response = requests.get("https://www.tiobe.com/tiobe-index/")
if response.status_code != 200:
    response.raise_for_status()

content = response.text
soup = BeautifulSoup(content, 'html.parser')

table = soup.table.tbody
tds_with_img = table.find_all('td', class_="td-top20")

imgs = ["https://www.tiobe.com" + td.img.get("src") for td in tds_with_img][:8]
td_languages = [td.next_sibling for td in tds_with_img][:8]
percentages = [language.next_sibling.text for language in td_languages][:8]
languages = [x.text.strip().replace("/", "-") for x in td_languages][:8]

urls = []
for language in languages:
    time.sleep(1)
    url = list(search(language, stop=1))[0]
    urls.append(url)
    print("Appended url")

md_file = ""

for i in range(len(languages)):
    md_file += f"## {languages[i]}\n"
    md_file += f"![{languages[i]}]({imgs[i]})\n"
    md_file += f"- [Learn more about {languages[i]}](/{languages[i]})\n"
    md_file += f"- **Percentage of popularity:** {percentages[i]}\n\n"

md_subpages = []

for i in range(len(languages)):
    subpage = "---\n"
    subpage += f"permalink: {languages[i]}\n"
    subpage += "---\n"
    subpage += f"## {languages[i]}\n"
    subpage += f"{languages[i]}'s popularity in the whole world is {percentages[i]}"
    subpage += f"If you want to see more about python click [here](/{languages[i]})\n"
    filename = f"docs/{languages[i]}.md"
    with open(filename, "w") as file:
        file.write(subpage)

# Save as index.md inside 'docs' folder
with open("docs/index.md", "w", encoding="utf-8") as file:
    file.write(md_file)


print("Markdown file successfully generated: docs/index.md")
