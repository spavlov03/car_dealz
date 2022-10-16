from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Car: 
    DB = "car_dealz"

    def __init__(self,data):
        self.id = data['id']
        self.price = data['price']
        self.model = data['model']
        self.make = data['make']
        self.year = data['year']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.seller_id = data['seller_id']
        self.buyer_id = data['buyer_id']
        self.seller = None

    @classmethod
    def post_car(cls,car_data):
        query = "INSERT INTO cars (price,model,make,year,description,seller_id) VALUES (%(price)s,%(model)s,%(make)s,%(year)s,%(description)s,%(seller_id)s);"
        result = connectToMySQL(cls.DB).query_db(query,car_data)
        #print("___ADDING NEW CAR----",result)
        return result

    @classmethod
    def delete_car(cls,car_data):
        query = "DELETE FROM cars WHERE id= %(id)s;"
        return connectToMySQL(cls.DB).query_db(query,car_data)
    
    @classmethod
    def get_all_cars_with_sellers(cls):
        query = """
        SELECT * FROM cars 
        JOIN users ON seller_id = users.id
        """
        results = connectToMySQL(cls.DB).query_db(query)
        cars = []
        for row in results:
            car = cls(row)
            car_seller_info = {
                "id":row['users.id'],
                    "first_name": row['first_name'],
                    "last_name": row['last_name'],
                    "email": row['email'],
                    "password": row['password'],
                    "created_at": row['users.created_at'],
                    "updated_at": row['users.updated_at']
            }
            seller = user.User(car_seller_info)
            car.seller = seller
            cars.append(car)
        return cars

    @classmethod
    def get_one_car_with_seller(cls,data):
        query = """
        SELECT * FROM cars 
        JOIN users ON seller_id = users.id
        WHERE cars.id = %(id)s;
        """
        results = connectToMySQL(cls.DB).query_db(query,data)
        cars = []
        for row in results:
            car = cls(row)
            car_seller_info = {
                "id":row['users.id'],
                    "first_name": row['first_name'],
                    "last_name": row['last_name'],
                    "email": row['email'],
                    "password": row['password'],
                    "created_at": row['users.created_at'],
                    "updated_at": row['users.updated_at']
            }
            seller = user.User(car_seller_info)
            car.seller = seller
            cars.append(car)
        return cars[0]

    @classmethod
    def get_car_by_id(cls,data):
        query = "SELECT * FROM cars WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query,data)
    
    @classmethod
    def edit_car(cls,data):
        query = "UPDATE cars SET price=%(price)s,model=%(model)s,make=%(make)s,year=%(year)s,description=%(description)s WHERE id=%(id)s;"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def car_purcahse(cls,data): 
        query = "UPDATE cars SET buyer_id=%(buyer_id)s WHERE id=%(id)s;"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def get_all_cars_of_buyer(cls,data): 
        query = """
        SELECT * FROM cars 
        JOIN users ON buyer_id = users.id
        WHERE buyer_id = %(buyer_id)s;
        """
        return connectToMySQL(cls.DB).query_db(query,data)

    @staticmethod
    def car_validation(car):
        is_valid = True
        if len(car['price']) < 1:
            flash("Price must be greater than 0.","car")
            is_valid = False
        if len(car['model']) < 1:
            flash("Model must be entered.","car")
            is_valid = False
        if len(car['make']) < 1:
            flash("Make must be entered.","car")
            is_valid = False
        if len(car['year']) < 1:
            flash("Year must be greater than 0.","car")
            is_valid = False
        if len(car['description']) < 1:
            flash("Description must be entered.","car")
            is_valid = False
        return is_valid
