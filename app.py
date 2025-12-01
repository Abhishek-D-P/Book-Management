from flask import Flask,request,jsonify,render_template,url_for,redirect
import sqlite3

app=Flask(__name__)

def get_db_connection():
    conn=sqlite3.connect('books.db')
    conn.row_factory=sqlite3.Row
    return conn

@app.route("/")
def home():
    conn=get_db_connection()
    cursor=conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS BOOKS(
                   bookId INTEGER PRIMARY KEY AUTOINCREMENT,
                   bookName TEXT NOT NULL,
                   publisher TEXT,
                   status TEXT NOT NULL,
                   pubYear TEXT)
                   """)
    conn.commit()
    table=cursor.execute("SELECT * FROM BOOKS")
    books=table.fetchall()
    

    return render_template('index.html',book_list=books)


@app.route('/add',methods=['GET','POST'])
def add():
    print("request method"+request.method)
    if(request.method=="POST"):
        bookName=request.form.get('bookName')
        publisher=request.form.get('publisher')
        status=request.form.get('status')
        pubYear=request.form.get('pubYear')
        print(bookName)
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute("INSERT INTO BOOKS (bookName,publisher,status,pubYear) VALUES (?,?,?,?)",(bookName,publisher,status,pubYear))
        conn.commit()
        conn.close()
        return redirect("/")
    return render_template('add.html')

@app.route("/delete/<int:bookId>", methods=["POST"])
def delete(bookId):
    conn=get_db_connection()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM BOOKS WHERE bookId="+str(bookId))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/update/<int:bookId>", methods=["GET","POST"])
def update_form(bookId):
    conn=get_db_connection()
    cursor=conn.cursor()   
    result=cursor.execute("SELECT * FROM BOOKS WHERE bookId="+str(bookId))
    
    book=result.fetchone()
    print(book["bookName"])
    conn.close()
    return render_template('update.html',book=book)

@app.route("/update",methods=["POST"])
def update():
    print("in")
    conn=get_db_connection()
    cursor=conn.cursor()
    bookId=request.form.get('bookId')
    bookName=request.form.get('bookName')
    publisher=request.form.get('publisher')
    status=request.form.get('status')
    pubYear=request.form.get('pubYear')
    
    
    cursor.execute("""UPDATE BOOKS SET bookName=(?), publisher=(?), status=(?), pubYear=(?) where bookId=(?)""",(bookName,publisher,status,pubYear,bookId))
    conn.commit()
    conn.close()
    return redirect("/")


if __name__=="__main__":
    app.run(debug=True)