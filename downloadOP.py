# Download particular One Piece Manga Chapter
# Chapters < 100 are named XXX via URL (e.g. Chapter 9 is 009)
import requests, os, sys, bs4

# Recording the URL as a string with the chapter number removed at the end of it.
URL = 'https://ww10.readonepiece.com/chapter/one-piece-chapter-'

# Checking the number of command line arguments passed to the script, only 1 should be allowed
# for the link to work. This 1 argument is the chapter number.
if len(sys.argv) == 2:
    chapterlnk = ''.join(sys.argv[1])   #0th index is the name of the script itself.
elif len(sys.argv) > 2:
    print("Too many entries. Only one entry required.")
    exit()
else:
    print("No chapter specified.")
    exit()

# Creating directory name based off chapter number. If it already exists it's fine (no OSError).
dirname = 'One Piece ' + str(chapterlnk)
os.makedirs(dirname, exist_ok=True)

# Concatenating incomplete URL to command-line argument to make complete URL.
chapterURL = URL + chapterlnk
print('Downloading page %s...' % chapterURL)
res = requests.get(chapterURL)  # Getting response object from URL - contains headers, body etc.
res.raise_for_status()  # Checking if response object was successfully retrieved.

# Saving a BeautifulSoup object to variable soup. BeautifulSoup is used for extracting
# information from an HTML page.
soup = bs4.BeautifulSoup(res.text, 'html.parser')
imgElem = soup.select('div img')    # Using the select() method to locate/match all elements
# named <img> that are within an element named <div>.

# Iterating through all the appropriate <img> elements and downloading their links (jpeg)
# which is the image file ultimately.
for i in range(len(imgElem)):
    imgDL = imgElem[i].get('src')
    print(imgDL)
    res2 = requests.get(imgDL)
    res2.raise_for_status()

# Opening directory file, writing to it and closing it after.
    imageFile = open(os.path.join(dirname, os.path.basename(imgDL)), 'wb')
    for chunk in res2.iter_content(6000000):
        imageFile.write(chunk)
    imageFile.close()

print('Done.')

