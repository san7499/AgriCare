import os
import math
import base64, uuid
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import requests

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import (
    LoginManager, UserMixin,
    login_user, login_required,
    logout_user, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from flask_pymongo import PyMongo
from bson.objectid import ObjectId

# ------------------ APP CONFIG ------------------
app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mongo = PyMongo(app)

# ------------------ LOGIN MANAGER ------------------
login_manager = LoginManager(app)
login_manager.login_view = "login"

# ------------------ FILE CHECK ------------------
def allowed_file(filename):
    return filename and "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ------------------ USER CLASS ------------------
class User(UserMixin):
    def __init__(self, user):
        self.id = str(user["_id"])
        self.username = user["username"]
        self.password = user["password"]
        self.role = user["role"]
        self.latitude = user.get("latitude")
        self.longitude = user.get("longitude")

# ------------------ USER LOADER ------------------
@login_manager.user_loader
def load_user(user_id):
    try:
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        return User(user) if user else None
    except:
        return None

# ------------------ API ------------------
API_URL = "https://sonu74swami-agricare.hf.space/predict"

# ------------------ PREDICTION ------------------
def predict_disease(img_path):
    try:
        with open(img_path, "rb") as f:
            response = requests.post(API_URL, files={"image": f}, timeout=60)

        result = response.json()

        return (
            result.get("disease", "Unknown"),
            result.get("confidence", 0),
            result.get("treatment", {
                "Fertilizer": ["Fallback"],
                "Pesticide": ["Fallback"],
                "Organic": ["Fallback"]
            })
        )
    except Exception as e:
        print("ERROR:", e)
        return "Error", 0, {
            "Fertilizer": ["API error"],
            "Pesticide": ["API error"],
            "Organic": ["API error"]
        }

# ------------------ DISTANCE ------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    a = (math.sin(d_lat/2)**2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(d_lon/2)**2)

    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

# ------------------ SIGNUP ------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        if mongo.db.users.find_one({"username": request.form["username"]}):
            flash("Username already exists")
            return redirect(url_for("signup"))

        mongo.db.users.insert_one({
            "username": request.form["username"],
            "password": generate_password_hash(request.form["password"]),
            "role": request.form["role"]
        })

        flash("Account created")
        return redirect(url_for("login"))

    return render_template("signup.html")

# ------------------ LOGIN ------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = mongo.db.users.find_one({"username": request.form["username"]})

        if user and check_password_hash(user["password"], request.form["password"]):

            lat = request.form.get("latitude")
            lon = request.form.get("longitude")

            mongo.db.users.update_one(
                {"_id": user["_id"]},
                {"$set": {
                    "latitude": float(lat) if lat else None,
                    "longitude": float(lon) if lon else None
                }}
            )

            login_user(User(user))

            return redirect(
                url_for("shop_dashboard") if user["role"] == "shop" else url_for("index")
            )

        flash("Invalid credentials")

    return render_template("login.html")

# ------------------ LOGOUT ------------------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# ------------------ HOME ------------------
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if current_user.role == "shop":
        return redirect(url_for("shop_dashboard"))

    if request.method == "POST":
        file = request.files.get("file")

        if not file or not allowed_file(file.filename):
            flash("Invalid image")
            return redirect(url_for("index"))

        filename = secure_filename(file.filename)
        path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(path)

        prediction, confidence, treatment = predict_disease(path)

        mongo.db.history.insert_one({
            "user_id": str(current_user.id),
            "filename": f"uploads/{filename}",
            "prediction": prediction,
            "confidence": confidence,
            "fertilizer": ", ".join(treatment["Fertilizer"]),
            "pesticide": ", ".join(treatment["Pesticide"]),
            "organic": ", ".join(treatment["Organic"])
        })

        return render_template("index.html",
            file=f"uploads/{filename}",
            prediction=prediction,
            confidence=confidence,
            fertilizer=treatment["Fertilizer"],
            pesticide=treatment["Pesticide"],
            organic=treatment["Organic"]
        )

    return render_template("index.html")

# ------------------ HISTORY ------------------
@app.route("/history")
@login_required
def history():
    records = list(mongo.db.history.find({"user_id": str(current_user.id)}).sort("_id", -1))
    return render_template("history.html", records=records)

@app.route("/history/delete/<record_id>", methods=["POST"])
@login_required
def delete_record(record_id):
    mongo.db.history.delete_one({
        "_id": ObjectId(record_id),
        "user_id": str(current_user.id)
    })
    flash("Record deleted")
    return redirect(url_for("history"))

# ------------------ SHOPS ------------------
@app.route("/shops")
@login_required
def shops():
    if not current_user.latitude:
        flash("Location not available")
        return redirect(url_for("index"))

    nearby = []

    for shop in mongo.db.shops.find():
        dist = haversine(
            current_user.latitude,
            current_user.longitude,
            shop["latitude"],
            shop["longitude"]
        )

        if dist <= 15:
            shop["distance"] = round(dist, 2)
            nearby.append(shop)

    nearby.sort(key=lambda x: x["distance"])
    return render_template("shops.html", shops=nearby)

# ------------------ SHOP DASHBOARD ------------------
@app.route("/shop/dashboard")
@login_required
def shop_dashboard():
    shop = mongo.db.shops.find_one({"owner_id": str(current_user.id)})
    return render_template("shop_dashboard.html", shop=shop)

# ------------------ ADD SHOP ------------------
@app.route("/shop/add", methods=["GET", "POST"])
@login_required
def add_shop():
    if mongo.db.shops.find_one({"owner_id": str(current_user.id)}):
        flash("You already have a shop")
        return redirect(url_for("shop_dashboard"))

    if request.method == "POST":
        mongo.db.shops.insert_one({
            "owner_id": str(current_user.id),   # ✅ FIX
            "shop_name": request.form["shop_name"],
            "phone": request.form["phone"],
            "address": request.form["address"],
            "latitude": float(request.form["latitude"]),
            "longitude": float(request.form["longitude"])
        })

        flash("Shop added")
        return redirect(url_for("shop_dashboard"))

    return render_template("shop_add.html")

# ------------------ ADD PRODUCT ------------------
@app.route("/shop/products/add", methods=["GET", "POST"])
@login_required
def add_product():
    shop = mongo.db.shops.find_one({"owner_id": str(current_user.id)})

    if not shop:
        flash("Add shop first")
        return redirect(url_for("add_shop"))

    if request.method == "POST":
        mongo.db.products.insert_one({
            "shop_id": str(shop["_id"]),
            "name": request.form["name"],
            "category": request.form["category"],
            "price": float(request.form["price"]),
            "description": request.form["description"]
        })

        flash("Product added")
        return redirect(url_for("shop_products"))

    return render_template("add_product.html")

# ------------------ SHOP PRODUCTS (SHOP OWNER) ------------------
@app.route("/shop/products")
@login_required
def shop_products():
    # Find shop of current logged-in shop owner
    shop = mongo.db.shops.find_one({"owner_id": str(current_user.id)})

    # If no shop exists → force user to create one
    if not shop:
        flash("Please add your shop first")
        return redirect(url_for("add_shop"))

    # Fetch products of this shop
    products = list(
        mongo.db.products.find({"shop_id": str(shop["_id"])})
    )

    return render_template(
        "shop_products.html",
        products=products,
        shop=shop
    )


# ------------------ VIEW SHOP PRODUCTS (FARMER SIDE) ------------------
@app.route("/shop/<shop_id>/products")
@login_required
def view_shop_products(shop_id):
    try:
        # Convert shop_id to ObjectId safely
        shop = mongo.db.shops.find_one({"_id": ObjectId(shop_id)})
    except Exception:
        flash("Invalid shop ID")
        return redirect(url_for("shops"))

    # If shop not found
    if not shop:
        flash("Shop not found")
        return redirect(url_for("shops"))

    # Fetch products for this shop
    products = list(
        mongo.db.products.find({"shop_id": shop_id})
    )

    return render_template(
        "shop_products_user.html",
        shop=shop,
        products=products
    )
# ------------------ RUN ------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
