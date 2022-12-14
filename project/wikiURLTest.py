import blueprintUtils as blueprintUtils
import urllib.request
import re
import time

# Verifies that the wikiHeading of each blueprint is found on its corresponding 
# page.
# appendWikiBlueprints.py must be run before this
# Takes ~ 5-7 minutes

files = {
    'blueprints.xml.append',
    'autoBlueprints.xml.append',
    'dlcBlueprints.xml.append'
}

def getUrls() -> set[str]:
    urlRegex = re.compile('>(https:\/\/.+)<')
    filePath = blueprintUtils.wikiElementsPath
    urlsToTest = set()

    for fileName in files:
        with open(filePath + fileName, encoding='utf-8') as file:
            fileText = file.read()
            urlsToTest.update(urlRegex.findall(fileText))
    return urlsToTest

def getHeading(url: str) -> str:
    heading = url.replace('https://ftlmultiverse.fandom.com/wiki/', '')
    pageEnd = heading.find('#')
    if pageEnd != -1:
        heading = heading[pageEnd + 1:]

    return heading.replace('_', ' ')

if __name__ == '__main__':
    start_time = time.time()
    urlsToTest = getUrls()

    nonFunctioningUrls = []
    badHeadingUrls = []
    notFoundUrls = []

    for url in urlsToTest:
        # make url parsable
        newUrl = url.replace("'", '%27')
        #print(newUrl)
        try:
            with urllib.request.urlopen(newUrl) as f:
                text = f.read().decode('utf-8')

                if 'There is currently no text in this page.' in text:
                    nonFunctioningUrls.append(newUrl)
                else:
                    # determine whether 'heading' is in text
                    heading = getHeading(url)
                    if heading not in text:
                        badHeadingUrls.append(newUrl)

        except urllib.error.HTTPError as e:
            notFoundUrls.append(newUrl)
            pass

    badUrls = '\n'.join(badHeadingUrls)
    notFoundUrls = '\n'.join(notFoundUrls)
    print(f'Non-functioning urls: {nonFunctioningUrls}')
    print(f'Bad urls: {badUrls}')
    print(f'Not found urls: {notFoundUrls}')

    print('--- %s seconds ---' % (time.time() - start_time))
