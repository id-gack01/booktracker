from flask import Flask, request, make_response, render_template
from markupsafe import escape

# a flask app to just track the book I'm reading, who wrote it,  the pages I'm on, and percentage complete
# store the book into a database
# each user can have many book
#flask --app book_tracker run to run the app

app = Flask(__name__)

#i really thought it would be an easy project...


#make a class of book with title (string), author (string), NumOfPages(int)
class Book:
    def __init__(self, title, author, numofpages, currentpage):
        self.title = title
        self.author = author
        self.numofpages = numofpages
        self.currentpage = currentpage


list_of_books = []
list_of_books.append(Book("Gravity's Rainbow", "Thomas Pynchon", 902, 620))


#each profile is associated with a list of book
#hellos is where users get a profile and some book associated with them
@app.route("/", methods=['GET', 'POST'])
def helloReader():

    #a name for the user
    #is there a name in the request, get that, otherwise, call the user User
    get_name = str(request.args.get('name', 'User'))

    get_title = str(request.args.get('title', 'Book Title'))
    get_author = str(request.args.get('author', 'Book Author'))
    get_numofpages = int(request.args.get('numofpages', 'Page Length'))
    get_currentpagenum = int(request.args.get('currentpagenum', 'Current Page'))

    outtext = '<center><h2>Book List</h2><h3>Book</h3>'
    outtext += '<form><table>'
    outtext += '<tr><td>Name: </td><td><input type="text" name="name"></td></tr>'
    outtext += '<tr><td>Title: </td><td><input type="text" name="title"></td></tr>'
    outtext += '<tr><td>Author: </td><td><input type="text" name="author"></td></tr>'
    outtext += '<tr><td>Number of Pages: </td><td><input type="int" name="numofpages"></td></tr>'

    outtext += '</td></tr>'
    outtext += '<tr><td></td><td><input type="submit" value="Enter Book"></td></tr></table></form>'

    booktitle = get_title
    bookauthor = get_author
    numofpages = get_numofpages
    currentpagenum = get_currentpagenum

    #have to get the program to enter booktitle, bookauthor, numofpages, and currentpagenum into a Book object
    # append Book object into list of book
    pagestillend = numofpages - currentpagenum
    outtext += "Pages left: " + str(pagestillend)

    bookform = outtext

    response = make_response(bookform)
    if not get_name:
        return "<p>Hello Reader</p>"
    return response

#shows the book everyone has, has a trailing slash
@app.route("/book/")
def showBooks():
    return list_of_books

#I can use the flask.url_for function to get a url for each book
