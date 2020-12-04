import datetime
from flask import Flask, request, render_template
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Movie
from database_setup import Base, Branch
from database_setup import Base, Screening
from database_setup import Base, Seat
from database_setup import Base, User
from database_setup import Base, Reservation
from database_setup import Base, Seat_Reserved
from database_setup import Base, Autorization
from flask import g
import sqlite3

DATABASE = './books-collection.db'
app = Flask(__name__)

engine = create_engine('sqlite:///books-collection.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Movie CLASS
# Movie CLASS
# Movie CLASS
# Movie CLASS
# Movie CLASS
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def valid_login(autorization_username, autorization_password):
    print(query_db('select * from autorization'))
    autorization = query_db('select * from autorization where autorization_username = ? and autorization_password = ?', [autorization_username, autorization_password], one=True)
    if autorization is None:
        return False
    else:
        return True

def log_the_user_in(autorization_username):
    return render_template('general.html', autorization_username=autorization_username)


@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['autorization_username'], request.form['autorization_password']):
            return log_the_user_in(request.form['autorization_username'])
        else:
            error = 'Неверное имя пользователя/пароль'

    return render_template('login.html', error=error)



@app.route('/witcher')
def showGeneral():
    now = datetime.date.today()
    now_movie = session.query(Screening, Movie).filter(Screening.date_film == now).filter(Screening.movie_id == Movie.title).all()
    print(now_movie)
    return render_template("general.html", now_movie=now_movie)


@app.route('/movies')
def showMovies():
    movies = session.query(Movie).all()
    return render_template("movies.html", movies=movies)


@app.route('/movies/new/', methods=['GET', 'POST'])
def newMovie():
    if request.method == 'POST':
        print(request.form['name'])
        print(request.form['author'])
        newMovie = Movie(title=request.form['name'], author=request.form['author'], genre=request.form['genre'], price=request.form['price'])
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
        if request.form['name'] or request.form['author'] or request.form['genre'] or request.form['price']:
            editedMovie.title = request.form['name']
            editedMovie.author = request.form['author']
            editedMovie.genre = request.form['genre']
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
# Movie CLASS
# Movie CLASS
# Movie CLASS
# Movie CLASS
# Movie CLASS


# Branch CLASS
# Branch CLASS
# Branch CLASS
# Branch CLASS
# Branch CLASS
@app.route('/branchs')
def showBranchs():
    branchs = session.query(Branch).all()
    return render_template("branch.html", branchs=branchs)


@app.route('/branchs/new/', methods=['GET', 'POST'])
def newBranch():
    if request.method == 'POST':
        newBranch = Branch(name=request.form['name'], seats=request.form['seats'])
        session.add(newBranch)
        session.commit()
        return redirect(url_for('showBranchs'))
    else:
        return render_template('newBranch.html')


@app.route("/branchs/<int:branch_id>/edit/", methods=['GET', 'POST'])
def editBranch(branch_id):
    editedBranch = session.query(Branch).filter_by(id=branch_id).one()
    if request.method == 'POST':
        if request.form['name'] or request.form['seats']:
            editedBranch.name = request.form['name']
            editedBranch.seats = request.form['seats']
            return redirect(url_for('showBranchs'))
    else:
        return render_template('editBranch.html', branch=editedBranch)

@app.route('/branchs/<int:branch_id>/delete/', methods=['GET', 'POST'])
def deleteBranch(branch_id):
    branchToDelete = session.query(Branch).filter_by(id=branch_id).one()
    if request.method == 'POST':
        session.delete(branchToDelete)
        session.commit()
        return redirect(url_for('showBranchs', branch_id=branch_id))
    else:
        return render_template('deleteBranch.html', branch=branchToDelete)
# Branch CLASS
# Branch CLASS
# Branch CLASS
# Branch CLASS
# Branch CLASS


# Screenings CLASS
# Screenings CLASS
# Screenings CLASS
# Screenings CLASS
# Screenings CLASS
@app.route('/screenings')
def showScreenings():
    screenings = session.query(Screening).all()
    return render_template("screenings.html", screenings=screenings)


@app.route('/screenings/new/', methods=['GET', 'POST'])
def newScreening():
    if request.method == 'POST':
        newScreening = Screening(movie_id=request.form['movie_id'], branch_id=request.form['branch_id'], screening_time=request.form['screening_time'], date_film=request.form['date_film'])
        session.add(newScreening)
        session.commit()
        return redirect(url_for('showScreenings'))
    else:
        movies = session.query(Movie).all()
        branchs = session.query(Branch).all()
        return render_template('newScreening.html', branchs=branchs, movies=movies)



@app.route("/screenings/<int:screening_id>/edit/", methods=['GET', 'POST'])
def editScreening(screening_id):
    editedScreening = session.query(Screening).filter_by(id=screening_id).one()
    if request.method == 'POST':
        if request.form['movie_id'] or request.form['branch_id'] or request.form['screening_time'] or request.form['date_film']:
            editedScreening.movie_id = request.form['movie_id']
            editedScreening.branch_id = request.form['branch_id']
            editedScreening.screening_time = request.form['screening_time']
            editedScreening.date_film = request.form['date_film']
            return redirect(url_for('showScreenings'))
    else:
        return render_template('editScreening.html', screening=editedScreening)

@app.route('/screenings/<int:screening_id>/delete/', methods=['GET', 'POST'])
def deleteScreening(screening_id):
    screeningToDelete = session.query(Screening).filter_by(id=screening_id).one()
    if request.method == 'POST':
        session.delete(screeningToDelete)
        session.commit()
        return redirect(url_for('showScreenings', screening_id=screening_id))
    else:
        return render_template('deleteScreening.html', screening=screeningToDelete)
# Screenings CLASS
# Screenings CLASS
# Screenings CLASS
# Screenings CLASS
# Screenings CLASS


# CLASS Seat
# CLASS Seat
# CLASS Seat
# CLASS Seat
# CLASS Seat
@app.route('/seats')
def showSeats():
    seats = session.query(Seat).all()
    return render_template("seats.html", seats=seats)


@app.route('/seats/new/', methods=['GET', 'POST'])
def newSeat():
    if request.method == 'POST':
        newSeat = Seat(row=request.form['row'], number=request.form['number'], branch_id=request.form['branch_id'])
        session.add(newSeat)
        session.commit()
        return redirect(url_for('showSeats'))
    else:
        branchs = session.query(Branch).all()
        return render_template('newSeat.html', branchs=branchs)

@app.route("/seats/<int:seat_id>/edit/", methods=['GET', 'POST'])
def editSeat(seat_id):
    editedSeat = session.query(Seat).filter_by(id=seat_id).one()
    if request.method == 'POST':
        if request.form['row'] or request.form['number'] or request.form['branch_id']:
            editedSeat.row = request.form['row']
            editedSeat.number = request.form['number']
            editedSeat.branch_id = request.form['branch_id']
            return redirect(url_for('showSeats'))
    else:
        return render_template('editSeat.html', seat=editedSeat)


@app.route('/seats/<int:seat_id>/delete/', methods=['GET', 'POST'])
def deleteSeat(seat_id):
    seatToDelete = session.query(Seat).filter_by(id=seat_id).one()
    if request.method == 'POST':
        session.delete(seatToDelete)
        session.commit()
        return redirect(url_for('showSeats', seat_id=seat_id))
    else:
        return render_template('deleteSeat.html', seat=seatToDelete)
# CLASS Seat
# CLASS Seat
# CLASS Seat
# CLASS Seat
# CLASS Seat


# CLASS USERS
# CLASS USERS
# CLASS USERS
# CLASS USERS
# CLASS USERS
@app.route('/users')
def showUsers():
    users = session.query(User).all()
    return render_template("users.html", users=users)


@app.route('/users/new/', methods=['GET', 'POST'])
def newUser():
    if request.method == 'POST':
        newUser = User(username=request.form['username'], password=request.form['password'])
        session.add(newUser)
        session.commit()
        return redirect(url_for('showUsers'))
    else:
        return render_template('newUsers.html')


@app.route("/users/<int:user_id>/edit/", methods=['GET', 'POST'])
def editUser(user_id):
    editedUser = session.query(User).filter_by(id=user_id).one()
    if request.method == 'POST':
        if request.form['username'] or request.form['password']:
            editedUser.username = request.form['username']
            editedUser.password = request.form['password']
            return redirect(url_for('showUsers'))
    else:
        return render_template('editUser.html', user=editedUser)


@app.route('/users/<int:user_id>/delete/', methods=['GET', 'POST'])
def deleteUser(user_id):
    userToDelete = session.query(User).filter_by(id=user_id).one()
    if request.method == 'POST':
        session.delete(userToDelete)
        session.commit()
        return redirect(url_for('showUsers', user_id=user_id))
    else:
        return render_template('deleteUser.html', user=userToDelete)
# CLASS USERS
# CLASS USERS
# CLASS USERS
# CLASS USERS
# CLASS USERS


# CLASS RESERVATIONS
# CLASS RESERVATIONS
# CLASS RESERVATIONS
# CLASS RESERVATIONS
# CLASS RESERVATIONS
@app.route('/reservations')
def showReservations():
    reservations = session.query(Reservation).all()
    return render_template("reservations.html", reservations=reservations)

@app.route('/reservations/new/', methods=['GET', 'POST'])
def newReservation():
    if request.method == 'POST':
        newReservation = Reservation(reserved=request.form['reserved'], user_id=request.form['user_id'], paid=request.form['paid'])
        session.add(newReservation)
        session.commit()
        return redirect(url_for('showReservations'))
    else:
        users = session.query(User).all()
        return render_template('newReservations.html', users=users)

@app.route("/reservations/<int:reservation_id>/edit/", methods=['GET', 'POST'])
def editReservation(reservation_id):
    editedReservation = session.query(Reservation).filter_by(id=reservation_id).one()
    if request.method == 'POST':
        if request.form['reserved'] or request.form['user_id'] or request.form['paid']:
            editedReservation.reserved = request.form['reserved']
            editedReservation.user_id = request.form['user_id']
            editedReservation.paid = request.form['paid']
            return redirect(url_for('showReservations'))
    else:
        return render_template('editReservation.html', reservation=editedReservation)

@app.route('/reservations/<int:reservation_id>/delete/', methods=['GET', 'POST'])
def deleteReservation(reservation_id):
    reservationToDelete = session.query(Reservation).filter_by(id=reservation_id).one()
    if request.method == 'POST':
        session.delete(reservationToDelete)
        session.commit()
        return redirect(url_for('showReservations', reservation_id=reservation_id))
    else:
        return render_template('deleteReservation.html', reservation=reservationToDelete)
# CLASS RESERVATIONS
# CLASS RESERVATIONS
# CLASS RESERVATIONS
# CLASS RESERVATIONS
# CLASS RESERVATIONS


# CLASS SEAT_RESERVEDS
# CLASS SEAT_RESERVEDS
# CLASS SEAT_RESERVEDS
# CLASS SEAT_RESERVEDS
# CLASS SEAT_RESERVEDS
@app.route('/seat_reserveds')
def showSeat_Reserved():
    seat_reserveds = session.query(Seat_Reserved).all()
    return render_template("seat_reserved.html", seat_reserveds=seat_reserveds)

@app.route('/seat_reserveds/new/', methods=['GET', 'POST'])
def newSeat_Reserved():
    if request.method == 'POST':
        newSeat_Reserved = Seat_Reserved(seat_id=request.form['seat_id'], reservation_id=request.form['reservation_id'], screening_id=request.form['screening_id'])
        session.add(newSeat_Reserved)
        session.commit()
        return redirect(url_for('showSeat_Reserved'))
    else:
        seats = session.query(Seat).all()
        reservations = session.query(Reservation).all()
        screenings = session.query(Screening).all()
        return render_template('newSeat_Reserveds.html', seats=seats, reservations=reservations, screenings=screenings)

@app.route("/seat_reserveds/<int:seat_reserveds_id>/edit/", methods=['GET', 'POST'])
def editSeat_Reserved(seat_reserveds_id):
    editedSeat_Reserved = session.query(Seat_Reserved).filter_by(id=seat_reserveds_id).one()
    if request.method == 'POST':
        if request.form['seat_id'] or request.form['reservation_id'] or request.form['screening_id']:
            editedSeat_Reserved.seat_id = request.form['seat_id']
            editedSeat_Reserved.reservation_id = request.form['reservation_id']
            editedSeat_Reserved.screening_id = request.form['screening_id']
            return redirect(url_for('showSeat_Reserved'))
    else:
        return render_template('editSeat_Reserved.html', seat_reserved=editedSeat_Reserved)


@app.route('/seat_reserveds/<int:seat_reserveds_id>/delete/', methods=['GET', 'POST'])
def deleteSeat_Reserved(seat_reserveds_id):
    seat_reservedToDelete = session.query(Seat_Reserved).filter_by(id=seat_reserveds_id).one()
    if request.method == 'POST':
        session.delete(seat_reservedToDelete)
        session.commit()
        return redirect(url_for('showSeat_Reserved', seat_reserveds_id=seat_reserveds_id))
    else:
        return render_template('deleteSeat_Reserved.html', seat_reserved=seat_reservedToDelete)
# CLASS SEAT_RESERVEDS
# CLASS SEAT_RESERVEDS
# CLASS SEAT_RESERVEDS
# CLASS SEAT_RESERVEDS
# CLASS SEAT_RESERVEDS

if __name__ == '__main__':
    app.debug = True
    app.run(port=4996)
