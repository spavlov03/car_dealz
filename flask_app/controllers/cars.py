from flask import render_template, redirect, request,session
from flask_app import app
from flask_app.models import car,user

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/logout")
    data = {"id": session['user_id']}
    all_cars = car.Car.get_all_cars_with_sellers()
    #print("ALL CARS---",all_cars)
    return render_template('dashboard.html',user = user.User.get_user_by_id(data),all_cars=all_cars)

@app.route("/new")
def add_car():
    if "user_id" not in session:
        return redirect("/logout")
    user_in_session = session['user_id']
    return render_template('new_car.html',user_in_session=user_in_session)

@app.route("/car_add",methods=["POST"])
def car_add():
    if "user_id" not in session:
        return redirect("/logout")
    if not car.Car.car_validation(request.form):
        return redirect('/new')
    data = {
        "price" : request.form['price'],
        "model" : request.form['model'],
        "make" : request.form['make'],
        "year" : request.form['year'],
        "description" : request.form['description'],
        "seller_id" : request.form['seller_id']
    }
    car.Car.post_car(data)
    return redirect("/dashboard")

@app.route("/delete/<int:id>")
def delete_car(id): 
    if "user_id" not in session:
        return redirect("/logout")
    data = {"id":id}
    car.Car.delete_car(data)
    return redirect("/dashboard")

@app.route("/edit/<int:id>")
def edit_car(id): 
    if "user_id" not in session:
        return redirect("/logout")
    data = {"id":id}
    this_car = car.Car.get_car_by_id(data)[0]
    #print("THIS CAR ---",this_car)
    return render_template("/edit_car.html",this_car = this_car)

@app.route("/car_edit/<int:id>",methods=["POST"])
def car_edit(id):
    if "user_id" not in session:
        return redirect("/logout")
    if not car.Car.car_validation(request.form):
        return redirect('/new')
    data = {
        "price" : request.form['price'],
        "model" : request.form['model'],
        "make" : request.form['make'],
        "year" : request.form['year'],
        "description" : request.form['description'],
        "id": id
    }
    car.Car.edit_car(data)
    return redirect("/dashboard")

@app.route("/show/<int:id>")
def show_car(id):
    if "user_id" not in session:
        return redirect("/logout")
    data = {"id":id}
    this_car = car.Car.get_one_car_with_seller(data)
    return render_template("show_car.html",this_car=this_car)

@app.route("/purchase/<int:id>")
def purcahse_car(id):
    if "user_id" not in session:
        return redirect("/logout")
    data = {"id":id,
            "buyer_id":session['user_id']
    }
    car.Car.car_purcahse(data)
    return redirect("/dashboard")