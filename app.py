"""Flask app for Cupcakes"""
from flask import Flask, render_template, redirect, flash, jsonify, request
from models import Cupcake, db, db_connect
import keys

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcakes"
app.config["SQLALCHEMY_ECHO"] = True

key_length = 64
app.config["SECRET_KEY"] = keys.key_gen(key_length)

db_connect(app)


@app.route('/api/cupcakes')
def api_list_cupcakes():
    """Provides JSON list of all cupcakes in database"""
    cupcakes = Cupcake.query.all()
    data = [cupcake.serialize_cupcake() for cupcake in cupcakes]

    return jsonify(cupcakes=data)


@app.route('/api/cupcakes/<id>')
def api_cupcake_detail(id):
    """Provides JSON detail of a single cupcake by id"""
    cupcake = Cupcake.query.get_or_404(id)

    return jsonify(cupcake=cupcake.serialize_cupcake())


@app.route('/api/cupcakes', methods=["POST"])
def api_create_cupcake():
    """Create a cupcake via API"""

    try:
        new_cupcake = Cupcake(**request.json)
        db.session.add(new_cupcake)
        db.session.commit()
        serialized_cupcake = new_cupcake.serialize_cupcake()
        return jsonify(cupcake=serialized_cupcake), 201

    except Exception as e:
        return jsonify(error=str(e))


@app.route('/api/cupcakes/<id>', methods=["PATCH"])
def api_update_cupcake(id):
    """Update a cupcake via API"""

    try:
        cupcake = Cupcake.query.get_or_404(id)
        data = request.json

        for key, value in data.items():
            if value == "":
                raise Exception(f"{key} can not be blank")
            else:
                setattr(cupcake, key, value)

        db.session.commit()

        return jsonify(cupcake=cupcake.serialize_cupcake())

    except Exception as e:
        return jsonify(error=str(e))


@app.route('/api/cupcakes/<id>', methods=["DELETE"])
def api_delete_cupcake(id):
    """Deletes cupcake by id"""
    try:
        cupcake = Cupcake.query.get_or_404(id)
        db.session.delete(cupcake)
        db.session.commit()
        return jsonify(message="Deleted")

    except Exception as e:
        return jsonify(error=str(e))


@app.route('/')
def show_index_page():
    return render_template('/index.html')
