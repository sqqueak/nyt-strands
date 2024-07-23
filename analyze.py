import json
from pprint import pprint
from collections import defaultdict, Counter
import matplotlib.pyplot as plt


class Word:
  def __init__(self, word: str, locations: list[int], length: int):
    self.word = word
    self.locations = locations
    self.length = length

  def __str__(self):
    return f'{self.word} ({self.length}): {self.locations}'

  def __repr__(self):
    return self.__str__()

class Game:  
  def __init__(self):
    self.words = []

  # def __init__(self, spangram: Word, words: list[Word]):
  #   self.spangram = spangram
  #   self.words = words

  def __str__(self):
    s = f'{self.spangram}\n'
    for word in self.words:
      s += f'  * {word}\n'
    return s
  
  def __repr__(self):
    return self.__str__()


mymap = {
    '0-1': 1,
    '1-2': 3,
    '2-3': 5,
    '3-4': 7,
    '4-5': 9,

    '0-6': 11,
    '0-7': 12, '1-6': 12,
    '1-7': 13,
    '1-8': 14, '2-7': 14,
    '2-8': 15,
    '2-9': 16, '3-8': 16,
    '3-9': 17,
    '3-10': 18, '4-9': 18,
    '4-10': 19,
    '4-11': 20, '5-10': 20,
    '5-11': 21,

    '6-7': 23,
    '7-8': 25,
    '8-9': 27,
    '9-10': 29,
    '10-11': 31,

    '6-12': 33,
    '6-13': 34, '7-12': 34,
    '7-13': 35,
    '7-14': 36, '8-13': 36,
    '8-14': 37,
    '8-15': 38, '9-14': 38,
    '9-15': 39,
    '9-16': 40, '10-15': 40,
    '10-16': 41,
    '10-17': 42, '11-16': 42,
    '11-17': 43,

    '12-13': 45,
    '13-14': 47,
    '14-15': 49,
    '15-16': 51,
    '16-17': 53,

    '12-18': 55,
    '12-19': 56, '13-18': 56,
    '13-19': 57,
    '13-20': 58, '14-19': 58,
    '14-20': 59,
    '14-21': 60, '15-20': 60,
    '15-21': 61,
    '15-22': 62, '16-21': 62,
    '16-22': 63,
    '16-23': 64, '17-22': 64,
    '17-23': 65,

    '18-19': 67,
    '19-20': 69,
    '20-21': 71,
    '21-22': 73,
    '22-23': 75,

    '18-24': 77,
    '18-25': 78, '19-24': 78,
    '19-25': 79,
    '19-26': 80, '20-25': 80,
    '20-26': 81,
    '20-27': 82, '21-26': 82,
    '21-27': 83,
    '21-28': 84, '22-27': 84,
    '22-28': 85,
    '22-29': 86, '23-28': 86,
    '23-29': 87,

    '24-25': 89,
    '25-26': 91,
    '26-27': 93,
    '27-28': 95,
    '28-29': 97,

    '24-30': 99,
    '24-31': 100, '25-30': 100,
    '25-31': 101,
    '25-32': 102, '26-31': 102,
    '26-32': 103,
    '26-33': 104, '27-32': 104,
    '27-33': 105,
    '27-34': 106, '28-33': 106,
    '28-34': 107,
    '28-35': 108, '29-34': 108,
    '29-35': 109,

    '30-31': 111,
    '31-32': 113,
    '32-33': 115,
    '33-34': 117,
    '34-35': 119,

    '30-36': 121,
    '30-37': 122, '31-36': 122,
    '31-37': 123,
    '31-38': 124, '32-37': 124,
    '32-38': 125,
    '32-39': 126, '33-38': 126,
    '33-39': 127,
    '33-40': 128, '34-39': 128,
    '34-40': 129,
    '34-41': 130, '35-40': 130,
    '35-41': 131,

    '36-37': 133,
    '37-38': 135,
    '38-39': 137,
    '39-40': 139,
    '40-41': 141,

    '36-42': 143,
    '36-43': 144, '37-42': 144,
    '37-43': 145,
    '37-44': 146, '38-43': 146,
    '38-44': 147,
    '38-45': 148, '39-44': 148,
    '39-45': 149,
    '39-46': 150, '40-45': 150,
    '40-46': 151,
    '40-47': 152, '41-46': 152,
    '41-47': 153,

    '42-43': 155,
    '43-44': 157,
    '44-45': 159,
    '45-46': 161,
    '46-47': 163,
}


###############  GETTING INFORMATION  ###############
def getSpangrams(data: dict):
  spangrams = []
  for day in data:
    spangrams.append(list(map(int, day["solutions"][day["spangram"]].split("|"))))
  return spangrams


###############  INFORMATION ANALYSIS  ###############
def getSizeFrequency(words: list[list[int]]):
  sizes = [len(word) for word in words]
  return dict(Counter(sizes))

def getEdgesTouchedPerSize(words):
  sizes = defaultdict(lambda: defaultdict(int))
  for word in words:
    touched = 0
    for cell in word:
        if cell <= 5 or cell >= 42 or (cell % 6) == 5 or (cell % 6) == 0:
            touched += 1
    
    sizes[len(word)][touched] += 1
  return sizes

def getMostCommonCells(words):
  count = defaultdict(int)
  for word in words:
    for cell in word:
      count[cell] += 1
  return count

def getMostCommonEdges(words):
  cx = defaultdict(int)

  for word in words:
    for a, b in zip(word, word[1:]):
      if a < b:
        cx[f'{a}-{b}'] += 1
      else:
        cx[f'{b}-{a}'] += 1

  return cx


###############  LOCATION  ###############
def livesInMiddle2Columns(words):
  enclosed = []
  area = {2, 3, 8, 9, 14, 15, 20, 21, 26, 27, 32, 33, 38, 39, 44, 45}

  for word in words:
    if all([c in area for c in word]):
      enclosed.append(word)

  return enclosed

def livesInMiddle4Columns(words):
  enclosed = []
  area = {1, 2, 3, 4, 7, 8, 9, 10, 13, 14, 15, 16, 19, 20, 21, 22, 25, 26, 27, 28, 31, 32, 33, 34, 37, 38, 39, 40, 43, 44, 45, 46}

  for word in words:
    if all([c in area for c in word]):
      enclosed.append(word)

  return enclosed

def livesInMiddle2Rows(words):
  enclosed = []
  area = {i for i in range(18, 30)}

  for word in words:
    if all([c in area for c in word]):
      enclosed.append(word)

  return enclosed

def livesInMiddle4Rows(words):
  enclosed = []
  area = {i for i in range(12, 36)}

  for word in words:
    if all([c in area for c in word]):
      enclosed.append(word)

  return enclosed

def livesInMiddle6Rows(words):
  enclosed = []
  area = {i for i in range(6, 42)}

  for word in words:
    if all([c in area for c in word]):
      enclosed.append(word)

  return enclosed


###############  VISUALIZERS  ###############

def visualizeCells(data):
  grid = [[0 for i in range(6)] for j in range(8)]
  for cell in data:
    rn = cell // 6
    cn = cell % 6

    grid[rn][cn] += data[cell]
  # return grid
  plt.imshow( grid ) 
  plt.show() 

def visualizeConnections(data):
  grid = [[0 for x in range(11)] for y in range(15)]
  for c in data:
    rn = mymap[c] // 11
    cn = mymap[c] % 11

    grid[rn][cn] += data[c]
  # return grid
  plt.imshow( grid ) 
  plt.show() 



def spangramsLongerThanAllOthers(data):
  eq = 0
  gt = 0
  lt = 0
  for day in data:
    wordSizes = [len(list(map(int, day["solutions"][x].split("|")))) for x in day["solutions"] if x != day["spangram"]]
    spangramSize = len(list(map(int, day["solutions"][day["spangram"]].split("|"))))


    if max(wordSizes) == spangramSize:
      eq += 1
    elif max(wordSizes) > spangramSize:
      print(day)
      gt += 1
      print()
    else:
      lt += 1

  return (lt, eq, gt)

  

def getData():
  with open("raw.json") as f:
    data = json.load(f)["solns"]

  games = [Game() for _ in range(len(data))]

  for i, day in enumerate(data):
    for word in day["solutions"]:
      locations = list(map(int, day["solutions"][word].split("|")))
      if word != day["spangram"]:
        games[i].words.append(Word(word, locations, len(locations)))
      else:
        games[i].spangram = Word(word, locations, len(locations))

  return games


def main():
  games = getData()
  spangrams = [game.spangram for game in games]
  words = []
  for game in games:
    words.append(game.words)

  pprint(spangrams)
  
  

  

        

  # spangrams = getSpangrams(data)
  # g1 = visualizeCells(getMostCommonCells(spangrams))
  # g2 = visualizeConnections(getMostCommonEdges(spangrams))

  # print(spangramsLongerThanAllOthers(data))

  # print(len(spangrams))
  # print()
  # print(len(livesInMiddle2Columns(spangrams)) / len(spangrams))
  # print(len(livesInMiddle4Columns(spangrams)) / len(spangrams))
  # print()
  # print(len(livesInMiddle2Rows(spangrams)) / len(spangrams))
  # print(len(livesInMiddle4Rows(spangrams)) / len(spangrams))
  # print(len(livesInMiddle6Rows(spangrams)) / len(spangrams))


  # grid = [[0 for i in range(6)] for j in range(8)]
  # for i in range(8):
  #   for j in range(6):
  #     grid[i][j] = g1[i][j] + g2[i][j]
  # plt.imshow( grid ) 
  # plt.show() 





if __name__ == '__main__':
  main()