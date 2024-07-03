import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import json

ROWS = 8
COLS = 6

def place(letters, loc, grid):
    for i in range(len(letters)):
        letter = letters[i]
        at = int(loc[i])
        rn = at // COLS
        cn = at % COLS
        grid[rn][cn] = letter

def get_info(soup):
    spangram = soup.find('span', id='spangram').get_text().upper()
    spangramloc = soup.find('span', id='spangramloc').get_text()
    words = soup.find('span', id='words').get_text().upper()
    loc = soup.find('span', id='loc').get_text()

    arr_sloc = spangramloc.split("|")
    arr_loc = loc.split("|")
    raw_words = words.replace("|", "")

    grid = [["" for _ in range(COLS)] for _ in range(ROWS)]

    place(spangram, arr_sloc, grid)
    place(raw_words, arr_loc, grid)

    solutions = {}
    arr_words = words.split("|")

    for word in arr_words:
        solutions[word] = []
        for _ in word:
            solutions[word].append(arr_loc.pop(0))
        solutions[word] = "|".join(solutions[word])

    solutions[spangram] = spangramloc

    return grid, solutions, spangram

archive_url = 'https://customstrandsnyt.com/archive'
response = requests.get(archive_url)
out_data = 'raw.json'
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    strands = soup.find_all('a', class_='False')
    strand_urls = ['https://customstrandsnyt.com' + strand['href'] for strand in strands]

    data = []
    for url in tqdm(strand_urls):
        response = requests.get(url)
        if response.status_code == 200:
            sub_soup = BeautifulSoup(response.content, 'html.parser')

            grid, solutions, spangram = get_info(sub_soup)
            data.append({
                'url': url,
                'grid': grid,
                'solutions': solutions,
                'spangram': spangram
            })

    with open(out_data, 'w') as f:
        json.dump({'solns':data}, f)
        print("Data saved to", out_data)
else:
    print("Failed to retrieve the archive page")
