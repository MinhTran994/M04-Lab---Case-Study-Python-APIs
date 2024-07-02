from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


#this is database for sqllite
#this is config option create sql server using just file. data is just the name
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///data.db"
#grab the database using sqlalchemy and bind it to app
db= SQLAlchemy(app)


@app.route('/')
def index():
    return "Hello"

#grab all books from database
@app.route('/books')
def get_books():
    #grab all with this .query.all()
    books = Book.query.all()
    #using empty list to display
    output=[]
    for book in books:
        book_data= {"book name": book.book_name, "author": book.author, "publisher": book.publisher}
        output.append(book_data)
    return {"books": output}


@app.route('/books/<id>')
def get_book(id):
    #grab 1 book with get_or_404
    book= Book.query.get_or_404(id)
    return {"book name": book.book_name, "author": book.author, "publisher": book.publisher}


#add book
@app.route('/books', methods=['POST'])
def add_book():
    book = Book(book_name=request.json['book name'],author=request.json['author'],publisher=request.json['publisher'])
    db.session.add(book)
    db.session.commit()
    return {'id':book.id}

#delete book
@app.route('/books/<id>',methods=['DELETE'])
def del_book(id):
    book =Book.query.get(id)
    if book is None:
        return {"error":"none"}
    db.session.delete(book)
    db.session.commit()
    return {"messg":"1 book deleted"}





#database tables:rows and collumns
#tables are created in sqlalchemy naming columns and data types
class Book(db.Model):
    #column w parameters (type), primary_key=true will auto increment
    id=db.Column(db.Integer,primary_key=True)#column w parameters (type)
    #string w 80 chars, unique means book_name cannot have same name
    #nullable means cannot be empty
    book_name = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(80))
    publisher = db.Column(db.String(80))
    #this function will rreturn evething to read
    def __repr__(self):
        return f"{self.book_name} - {self.author} - {self.publisher}"
