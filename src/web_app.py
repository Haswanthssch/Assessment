import os
from flask import Flask, render_template, redirect, url_for

flask_app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates"),
    static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), "static"),
    static_url_path="/static",
)
flask_app.secret_key = os.getenv("FLASK_SECRET_KEY", "flask-inventory-secret-2024")


# ─── Root ─────────────────────────────────────────────────────────────────
@flask_app.route("/")
def index():
    return redirect("/user/products")


# ─── User Routes ──────────────────────────────────────────────────────────
@flask_app.route("/login")
def user_login():
    return render_template("user/login.html")


@flask_app.route("/register")
def user_register():
    return render_template("user/login.html")


@flask_app.route("/user/products")
def user_products():
    return render_template("user/products.html")


@flask_app.route("/user/cart")
def user_cart():
    return render_template("user/cart.html")


@flask_app.route("/user/checkout")
def user_checkout():
    return render_template("user/checkout.html")


# ─── Admin Routes ─────────────────────────────────────────────────────────
@flask_app.route("/admin/login")
def admin_login():
    return render_template("admin/login.html")


@flask_app.route("/admin/dashboard")
def admin_dashboard():
    return render_template("admin/dashboard.html")


@flask_app.route("/admin/users")
def admin_users():
    return render_template("admin/users.html")


@flask_app.route("/admin/products")
def admin_products():
    return render_template("admin/products.html")


@flask_app.route("/admin/orders")
def admin_orders():
    return render_template("admin/orders.html")


@flask_app.route("/admin/inventory")
def admin_inventory():
    return render_template("admin/inventory.html")


@flask_app.route("/admin/logs")
def admin_logs():
    return render_template("admin/logs.html")
