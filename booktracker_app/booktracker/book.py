# import sqlite3
from flask import (
    Blueprint, flash, g, render_template, request, url_for, redirect
)

#trying to make json ready sqlite returns
# import jsonpickle
# import json
import string


from werkzeug.exceptions import abort
# from . import auth

#have to import the functions directly
# keep the database file in the same directory
from .db import get_db

#create the blueprint object and initialize it
bp = Blueprint("book", __name__)

"""

    View Functions: the code I write to respond to requests to my application, patterns are used to match the 
        incoming request URL to the view that should handle it
    Blueprint: a way to organize related views and other code. The functions and such are registered to a blueprint, 
        which is then registered with an app when it available in the factory function.
        
    First thing to test is /, then /add. I'm getting synax errors for these still

 """


#templates = in book folder: add, index, update, completion_status in auth folder: login, register

#maybe i can use the book title and book author as parameters to get the id (like a get_id function)
# then use that idBook Progress
#get all the books in the database and order by author
#registers the view handler for get requests in the url map
#SELECT book_title, book_author, page_numbers FROM BOOKS ORDER BY book_author DESC
#blueprint index, show all books by default
@bp.route("/", methods=['GET'])
def index():
    db = get_db()
    # book = db.execute("SELECT book_title "
    #                   "FROM books").fetchall()

    book = db.execute("SELECT books.book_title, books.book_author, books.book_description, books.page_numbers" +
                      " FROM books" +
                      " ORDER BY books.book_author DESC").fetchall()


    # for i in book:
    #     print(f"Title: {i['book_title']}, Author: {i['book_author']}, Page Numbers: {i['page_numbers']}, "
    #           f"Description: {i['book_description']}")
    #left side is the argument name, used in the placeholder written in the template
    #right side is the variable in the current scope, providing the value for the argument
    return render_template("book/index.html", book=book)




#get a single book, return multiple if there's multiple books with the same title
#methods = ['GET']
#SELECT book_title, book_author, page_numbers, book_description, from the database that match book_title
#write the @bp route("/book")
#post takes the inputs from the requests and assings them to variables

#returns any book with the same name
#/<book_title>
@bp.route("/books/<book_title>")
def get_book(book_title):

    book = get_db().execute("SELECT book_title, book_author, page_numbers, book_description" +
                            " FROM books" +
                            " WHERE book_title = ?",
                            (book_title,)).fetchall()

    if book is None:
        abort(404, f"Book {book_title} can't be found. ")
    #{book['book_title']}, {book['book_author']}, {book['page_numbers']}, {book['book_description']}
    #need a way to make the Objects of Type Row JSON serializable and readable by humans
    return book


#returns specific book with title and author
@bp.route("/authors/<book_author>/<book_title>")
def get_author_book(book_title, book_author):

    author_book = get_db().execute("SELECT book_title, book_author, page_numbers, book_description" +
                            " FROM books" +
                            " WHERE book_title = ? and book_author = ?",
                            (book_title, book_author)).fetchone()

    if author_book is None:
        abort(404, f"Book {book_title} can't be found. ")
    return author_book


#get all the books by a specific author
# if no author, return "no books by that author or smthng"
# remember book_author is the column name
#SELECT * FROM books WHERE book_author = ?
@bp.route("/authors/<book_author>", methods=['GET'])
def get_author(book_author):
    author_work = get_db().execute("SELECT book_author, book_title, book_description, page_numbers FROM books" +
                              " WHERE book_author = ?" +
                              " ORDER BY book_author DESC",
                              book_author,).fetchall()
    if author_work is None:
        abort(404, f"Author: {book_author} can't be found. ")
    return author_work


#list all the authors, remove duplicates
#, methods=['GET'] might not be needed
@bp.route("/authors")
def get_authors():

    authors = get_db().execute('SELECT DISTINCT book_author FROM books'
                               ).fetchall()
    #at a later date, count the number of book titles under each author name and return them under # of titles
    if authors is None:
        abort(404, "No Authors listed")

    return render_template("authors/authors.html", authors=authors)


#make a function to get title and author and return id
def returnIdFromTitleAndAuthor(book_title, book_author):
    db = get_db()
    bookId = db.execute("SELECT books.id FROM books WHERE book_title = ? AND book_author = ? ",
                        (book_title, book_author)).fetchone()
    if bookId is None:
        abort(404, "No bookID listed")

    return bookId


#make a function to get an id and return title and author
def returnTitleAndAuthorFromId(id):
    db = get_db()
    title = db.execute("SELECT books.book_title FROM books WHERE id = ?", (id, )).fetchone()
    author = db.execute("SELECT books.book_author FROM books WHERE id = ?", (id, )).fetchone()

    if title is None:
        abort(404, "No title listed")
    if author is None:
        abort(404, "No author listed")

    #key is _Key, value is value (without underscore)
    titleandauthor = {'_Title': title, '_Author': author}
    return titleandauthor

#post a book
#the request.form["book_title"], request.form["book_author], request.form["page_numbers"]
#require a title, author, and page numbers, description is optional
#check to see if the request.method == ['POST']
#add to the title, author, and page_numbers variable

@bp.route("/add_book", methods=['GET', 'POST'])
def add_book():

    if request.method == "POST":
        title = request.form["Book Title"].strip()
        author = request.form["Book Author"].strip()
        page_nums = request.form["Page Numbers"].strip()
        # include optional book description
        if request.form["Book Description"] is not None:
            book_desc = request.form["Book Description"].strip()
        else:
            book_desc = "..."
        error = None

        if not title:
            error = "Title required, all books should have a title"
        if not author:
            error = "author required, if unknown, put unknown"
        if not page_nums:
            error = "No book has 0 pages, put in the page numbers"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            # title() capitalizes the author name
            db.execute('INSERT INTO books (book_title, book_author, page_numbers, book_description, creator_id)' +
                       ' VALUES (?, ?, ?, ?, ?)',
                       (title, author.title(), page_nums, book_desc, g.user['id'])
                       )
            db.commit()
            return redirect(url_for("book.index"))
    return render_template("book/add.html")


"""
What happens when it's the same book title but a different author? How does the route thing work then?
I want all the book titles to display, regardless of author       
"""

#"/<book_author>/<book_title>/update"
#update an existing book using the book title
@bp.route("/<book_author>/<book_title>/update", methods=('GET', 'POST'))
def update_book(book_title, book_author):
    updated_book = get_author_book(book_title, book_author)
    #print("Before: " + updated_book['book_title'], updated_book['book_author'])
    book_id = returnIdFromTitleAndAuthor(book_title, book_author)
    #print(book_id['id'])

    if request.method == "POST":
        title = request.form["Book Title"].strip()
        author = request.form["Book Author"].strip()
        page_nums = request.form["Page Numbers"].strip()
        # include optional book description
        if request.form["Book Description"] is not None:
            book_desc = request.form["Book Description"].strip()
        else:
            book_desc = None
        error = None

        if not title:
            error = "Title is required"
        if not author:
            error = "Author is required"
        if not page_nums:
            error = "Page Numbers are required"

        if error is not None:
            flash("Something happened bruv: ", str(error))
        else:
            #print("test")
            #.title() capitalizes the author name
            db = get_db()
            db.execute("UPDATE books SET book_title = ?, book_author = ?, page_numbers = ?" +
                       " WHERE id = ?",
                       (title, author.title(), page_nums, book_id['id'])
                       )

            if book_desc is not None:
                db.execute("UPDATE books SET book_description = ?" +
                           " WHERE id = ?",
                           (book_desc, book_id['id'])
                           )
                # db.commit()
            db.commit()

            #print("bleeeeh this must show")
            #print("After: " + updated_book['book_title'], updated_book['book_author'])

            return redirect(url_for("book.index"))
    return render_template("book/update.html", updated_book=updated_book)


#/<book_title>/delete old version
#/<book_author>/<book_title>
#delete a book
"""
"""
@bp.route("/<book_author>/<book_title>/delete", methods=('POST',))
def delete(book_author, book_title):
    #updated_book = get_author_book(book_title, book_author)
    book_id = returnIdFromTitleAndAuthor(book_title, book_author)
    #flash("book_id currently is: " + str(book_id['id']))
    if book_id is None:
        flash("No book of that title + author to delete.")
    db = get_db()
    db.execute("DELETE FROM books WHERE books.id = (?)", (book_id['id'],))
    db.commit()
    #print("Book is outta here")
    #flash("Book Deleted")
    return redirect(url_for("book.index"))

#print(url_for('book.delete', book_author='anonymous', book_title='to be deleted'))

"""



"""




#the user can enter the current page number they're on and the program returns a completion percentage
#check test app in flaskhello to see how to take user input and calculate a progress and then show that progress

#to split this into parts, I'll first look up how to grab from the sql database based off the title and author
#put that into a number
#put insert that number into these functions
#get an input for the current page
#put that input into a number here
#then calculate the completion status and return it in the index.html page
#if I need to do so, use title, author variables from updateBook function as parameters
@bp.route("/<book_author>/<book_title>/completion", methods=['GET', 'POST'])
def getcompletionstatus(book_title, book_author):
    # current_page = int(input("Enter your current page").strip())
    db = get_db()
    page_nums = db.execute("SELECT page_numbers FROM books WHERE book_title = ? AND book_author = ?",
                                 (book_title, book_author,)).fetchone()
    #<input type="number" min="0" id="current_page" name="current_page" value="{{request.form['Current Page']}}>
    title = book_title
    # print(page_nums['page_numbers'])
    if request.method == "POST":
        current_page = request.form["Current Page"]
        current_page = int(current_page)
    else:
        current_page = 0
    #current_page = "275"
    #convert to ints when doing the calculations
    if current_page is not None:
        page_nums = int(page_nums['page_numbers'])

        pages_to_go = page_nums - current_page

        #this gets the percentage complete
        completion_calc = round(100 * (current_page / page_nums), 2)

        completion_rate = ("For " + string.capwords(str(book_title)) + ", you're "
                           + str(completion_calc) + " % complete, " + str(pages_to_go) + " pages left")

        if completion_calc >= 100:
            completion_rate = "You're done with the book."
    else:
        completion_rate = 0
    # return completion_rate
    #current idea is to render template a completion_status page then insert that page via
    # extends 'index.html' into the index where it shows up
    #it'll be a separate page  for now because idk how to send that "up"
    return render_template("book/completion_status.html", completion_rate=completion_rate, title=title)


"""

"""

