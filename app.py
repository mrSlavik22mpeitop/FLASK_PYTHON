from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Movie

app = Flask(__name__)

engine = create_engine('sqlite:///books-collection.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/movies')
def showMovies():
    movies = session.query(Movie).all()
    return render_template("movies.html", movies=movies)


@app.route('/movies/new/', methods=['GET', 'POST'])
def newMovie():
    if request.method == 'POST':
        newMovie = Movie(title=request.form['name'], author=request.form['author'], cast=request.form['cast'], price=request.form['price'])
        session.add(newMovie)
        session.commit()
        return redirect(url_for('showMovies'))
    else:
        return render_template('newMovie.html')

    # Эта функция позволит нам обновить книги и сохранить их в базе данных.
@app.route("/movies/<int:movie_id>/edit/", methods=['GET', 'POST'])
def editMovie(movie_id):
    editedMovie = session.query(Movie).filter_by(id=movie_id).one()
    if request.method == 'POST':
        if request.form['name'] or request.form['author'] or request.form['cast'] or request.form['price']:
            editedMovie.title = request.form['name']
            editedMovie.author = request.form['author']
            editedMovie.cast = request.form['cast']
            editedMovie.price = request.form['price']
            return redirect(url_for('showMovies'))
    else:
        return render_template('editMovie.html', movie=editedMovie)

    # Эта функция для удаления книг
@app.route('/movies/<int:movie_id>/delete/', methods=['GET', 'POST'])
def deleteMovie(movie_id):
    movieToDelete = session.query(Movie).filter_by(id=movie_id).one()
    if request.method == 'POST':
        session.delete(movieToDelete)
        session.commit()
        return redirect(url_for('showMovies', movie_id=movie_id))
    else:
        return render_template('deleteMovie.html', movie=movieToDelete)





if __name__ == '__main__':
    app.debug = True
    app.run(port=4996)