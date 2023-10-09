import os

from flask import Flask, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Cupcake, DEFAULT_IMAGE_URL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///cupcakes')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.get("/api/cupcakes")
def list_cupcakes():
    """Return JSON {cupcakes: [{id, flavor, size, rating, image_url}, ...]}."""

    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)


@app.get("/api/cupcakes/<int:cupcake_id>")
def get_cupcake_detail(cupcake_id):
    """
    Get details about a particular cupcake.
    Returns: {cupcake: {id, flavor, size, rating, image_url}}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    return jsonify(cupcake=cupcake.serialize())


@app.post("/api/cupcakes")
def create_cupcake():
    """
    Create a new cupcake record.

    Takes JSON: {flavor, size, rating, image_url [optional]}

    Returns JSON with data about added cupcake:
    {cupcake: {id, flavor, size, rating, image_url}}
    """

    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']

    image_url = request.json.get('image_url') or None # In case of empty string.

    new_cupcake = Cupcake(
        flavor=flavor,
        size=size,
        rating=rating,
        image_url=image_url
        )

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)


@app.patch("/api/cupcakes/<int:cupcake_id>")
def update_cupcake(cupcake_id):
    """
    Update an existing cupcake record.

    Takes JSON: {flavor, size, rating, image_url} (all fields optional)

    Returns JSON with data about updated cupcake:
    {cupcake: {id, flavor, size, rating, image_url}}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image_url = request.json.get('image_url') or DEFAULT_IMAGE_URL

    db.session.commit()

    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.delete("/api/cupcakes/<int:cupcake_id>")
def delete_cupcake(cupcake_id):
    """
    Delete a cupcake record.

    Returns JSON with deleted cupcake id:
    {deleted: id}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(deleted=cupcake.id)