from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy,session


app=Flask('__name__')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:2345@localhost/application'
app.config['SQLALCHEMY_TRACK_CONFIGURATION'] = False
db =SQLAlchemy(app)

class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"


  

@app.route('/')
def index():
    return "heloo"


@app.route('/drinks')
def drinks():
    drinks=Drink.query.all()
    output = []
    for drink in drinks:
        drink_data = {'name': drink.name, 'description':drink.description}

    output.append(drink_data)
    return {'drinks': output}
    
 
@app.route('/drinks/<id>', methods=["GET"])
def get_drink(id):
    drink = Drink.query.get_or_404(id)
    return {"name": drink.name, "description": drink.description}

@app.route('/drinks', methods=['POST'])
def add_drink():
    new_drink = Drink(name = request.json['name'], description = request.json['description'])
    db.session.add(new_drink)
    try:
        db.session.commit()
        return {'id': new_drink.id}, 201
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500
    finally:
        db.session.close()

app.route('/drinks/<id>', methods=["DELETE"])
def delete_drink(id):
    drink = Drink.query.get(id)
    if drink is None:
        return {'error': 'Drink not found'}, 404  
    db.session.delete(drink)
    try:
        db.session.commit()  
        return {"message": 'Deleted'}, 200 
    except Exception as e:
        db.session.rollback()  
        return {'error': str(e)}, 500  
    finally:
        db.session.close()  
        
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)