from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session
)

try:
    from flask_sqlalchemy import SQLAlchemy
except ImportError as exc:
    raise SystemExit(
        "Flask-SQLAlchemy is not installed in this Python environment.\n"
        "Activate the virtual environment and install it, or run:\n"
        "    .venv\\Scripts\\python.exe -m pip install Flask-SQLAlchemy"
    ) from exc

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from sklearn.cluster import (
    KMeans,
    DBSCAN
)

from sklearn.preprocessing import StandardScaler

from sklearn.metrics import silhouette_score

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

app = Flask(__name__)

# Secret Key
app.secret_key = "customer_segmentation_secret"

# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db = SQLAlchemy(app)

# Store dataframe globally
df_global = None


# User Table
class User(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100),
        unique=True
    )

    password = db.Column(
        db.String(200)
    )


# Create Database
with app.app_context():
    db.create_all()


# Home Route
@app.route("/")
def home():

    if "user" not in session:
        return redirect("/login")

    global df_global

    columns = []

    # If dataset already uploaded
    if df_global is not None:

        columns = df_global.select_dtypes(
            include=['int64', 'float64']
        ).columns.tolist()

    return render_template(
        "index.html",
        uploaded=False,
        show_images=False,
        columns=columns
    )


# Signup
@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        hashed_password = generate_password_hash(
            password
        )

        user = User(
            username=username,
            password=hashed_password
        )

        db.session.add(user)

        db.session.commit()

        return redirect("/login")

    return render_template("signup.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        user = User.query.filter_by(
            username=username
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            session["user"] = username

            return redirect("/")

        return render_template("login.html",error="Invalid Username or Password")

    return render_template("login.html")


# Logout
@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/login")


# Upload CSV
@app.route("/upload", methods=["POST"])
def upload():

    global df_global

    if "user" not in session:
        return redirect("/login")

    file = request.files["file"]

    df_global = pd.read_csv(file)

    numeric_columns = df_global.select_dtypes(
        include=['int64', 'float64']
    ).columns.tolist()

    return render_template(
    "index.html",
    uploaded=True,
    columns=numeric_columns,
    show_images=False,
    selected_algorithm="K-Means"
)


# Run Model
@app.route("/run", methods=["POST"])
def run_model():

    global df_global

    if "user" not in session:
        return redirect("/login")
    if df_global is None:
        return redirect("/")
    algorithm = request.form["algorithm"]

    col1 = request.form["col1"]

    col2 = request.form["col2"]

    # Feature Selection
    data = df_global[[col1, col2]]

    # Scaling
    scaler = StandardScaler()

    scaled_data = scaler.fit_transform(data)

    # Elbow Method
    inertia = []

    optimal_k = None

    k_values = range(2, 9)

    for k in k_values:

        model = KMeans(
            n_clusters=k,
            random_state=42
        )

        model.fit(scaled_data)

        inertia.append(model.inertia_)

    # Optimal K
    drops = []

    for i in range(len(inertia)-1):

        drops.append(
            inertia[i] - inertia[i+1]
        )

    optimal_k = drops.index(max(drops)) + 2

    # Elbow Plot
    plt.figure(figsize=(6,4))

    plt.plot(
        k_values,
        inertia,
        marker='o'
    )

    plt.xlabel("K")

    plt.ylabel("Inertia")

    plt.title(
        f"Elbow Method (Optimal K = {optimal_k})"
    )

    plt.savefig("static/elbow.png")

    plt.close()

    # KMeans
    if algorithm == "kmeans":

        model = KMeans(
            n_clusters=optimal_k,
            random_state=42
        )

        clusters = model.fit_predict(
            scaled_data
        )

        score = round(
    silhouette_score(
        scaled_data,
        clusters
    ),
    3
)

        plt.figure(figsize=(7,5))

        plt.scatter(
            data[col1],
            data[col2],
            c=clusters
        )

        plt.xlabel(col1)

        plt.ylabel(col2)

        plt.title(
            f"KMeans Clustering (K={optimal_k})"
        )

        plt.savefig("static/result.png")

        plt.close()

        selected_algorithm = "K-Means"

    # DBSCAN
    else:

        model = DBSCAN(
            eps=0.5,
            min_samples=5
        )

        clusters = model.fit_predict(
            scaled_data
        )

        score = "Not Applicable"
        optimal_k = "N/A"

        plt.figure(figsize=(7,5))

        plt.scatter(
            data[col1],
            data[col2],
            c=clusters
        )

        plt.xlabel(col1)

        plt.ylabel(col2)

        plt.title("DBSCAN Clustering")

        plt.savefig("static/result.png")

        plt.close()

        selected_algorithm = "DBSCAN"

    numeric_columns = df_global.select_dtypes(
        include=['int64', 'float64']
    ).columns.tolist()

    return render_template(
        "index.html",
        uploaded=True,
        columns=numeric_columns,
        show_images=True,
        selected_algorithm=selected_algorithm,
        optimal_k=optimal_k,
        score=score
    )


if __name__ == "__main__":
    app.run(debug=True)