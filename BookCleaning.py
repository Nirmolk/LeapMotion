# !/usr/bin/python
# coding=utf-8

import re
import numpy as np
from epub_conversion.utils import open_book, convert_epub_to_lines

def mylinetoclean(theline):

    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', theline)
    return cleantext #Get rid of HTML tags on the book.

def linesFromBook(bookTitle):

    book = open_book(bookTitle)

    lines = convert_epub_to_lines(book) #Convert lines in book from epub into a textfile

    allMyRealLines = list()  #Obtain allMyRealLines

    for line in lines:
        cleanline = mylinetoclean(line)  # mylinetoclean is run. (Tags removed)
        cleanline = "\r" + cleanline + "\r" # The tagless lines are formatted on seperate lines.
        print(cleanline)
        allMyRealLines.append(cleanline) #Add the clean formatted lines into a new list called allMyRealLines

    return allMyRealLines


if __name__ == '__main__':

    allMyRealLines = linesFromBook("hamlet.epub") #Hamlet epub is displayed in allMyRealLines

    for cleanline in allMyRealLines:
        print(cleanline)







    print (len(allMyRealLines))

    print (allMyRealLines[int(len(allMyRealLines) / 2)])

    print ("")

    for i in range(1000, 1010):
        print (i, " :", allMyRealLines[i] + "  Line equals")

