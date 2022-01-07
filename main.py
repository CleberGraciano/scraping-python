'''
REFERENCES:
    BEAUTIFULSOUP: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    REGEX: https://docs.python.org/3/library/re.html
'''

from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import re
import csv

csvFileName = 'IMDBRatingTop250.csv'
regexMovieYear = re.compile('(\d{4})')
regexUserRating = re.compile('\ ((\d{1,3})((\,|\.)\d{1,3})*)')

try:
    url = urlopen("https://www.imdb.com/chart/top?ref_=nv_mv_250")
except HTTPError as error:
    print(error)
except URLError as error:
    print(error)
else:
    html = BeautifulSoup(url.read(), "html.parser")
    contentTitleYear = html.find_all("td", {"class": "titleColumn"})
    contentRating = html.find_all("td", {"class": "imdbRating"})

    with open(csvFileName, 'w') as csvfile:
        # criando o arquivo csv com o delimitador
        fileWriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        # Escrevendo cabeçalho no arquivo
        fileWriter.writerow(['TITLE', 'YEAR', 'IMDB RATING', 'USER RATINGS'])  # HEADER

        for cty, cr in zip(contentTitleYear, contentRating):

            # titulo do filme
            movieTitle = (cty.a).text

            # ano de lançamento, com regex para pegar o valor numerico
            movieYear = re.search(regexMovieYear, (cty.span).text)

            # avaliação do IMDB
            imdbRating = cr.strong.text

            # avaliações dos usuarios, com regex para pegar apenas valor numerico, excluindo o texto da string obtida.
            userRating = re.search(regexUserRating, cr.strong['title'])

            # Com os valores salvo nas variaveis escrevo elas no arquivo
            fileWriter.writerow([movieTitle, movieYear.group(0), imdbRating, userRating.group(0)])  # CONTENT

            print(movieTitle, movieYear.group(0), imdbRating, userRating.group(0))

            # print(movieTitle,movieYear.group(0),imdbRating,userRating.group(0))
            print('Arquivo ', csvFileName, 'gerado com sucesso!')