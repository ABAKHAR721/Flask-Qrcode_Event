from flask import Flask, render_template, request, jsonify, redirect, url_for
import qrcode
import hashlib
import os
import firebase_admin
from firebase_admin import credentials, db
from flask_cors import CORS
import pandas as pd
from flask import send_file
from openpyxl import load_workbook

app = Flask(__name__)
CORS(app)

# Load Firebase credentials (Download JSON from Firebase console)
cred = credentials.Certificate("firebase_cred.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://qrcode-72c3c-default-rtdb.firebaseio.com/'
})

ORGANISER_PASSWORD = "legend"

# Firebase DB reference
ref = db.reference("/users")  # All users will be stored under `/users`


# 🔹 Utility Function: Hash User Info
def hash_info(data):
    """Generate SHA-256 hash of user information"""
    return hashlib.sha256(data.encode()).hexdigest()


# 🔹 Function: Save Data to Firebase
def save_data(user_data):
    """Save user data to Firebase"""
    ref.push(user_data)  # Firebase auto-generates a unique key
    print("✅ Data saved successfully.")


# 🔹 Function: Load Data from Firebase
def load_data():
    """Load all users from Firebase"""
    users = ref.get()
    return users if users else {}  # Return empty dictionary if no data


# 🔹 Route: Home Page
@app.route("/")
def home():
    """Render the home page"""
    return render_template("index.html")


# 🔹 Route: Register a User and Generate QR Code
@app.route("/register", methods=["GET", "POST"])
def register():
    """Handle user registration and generate QR code"""
    if request.method == "GET":
        return render_template("register.html")

    fullname = request.form.get("fullname")
    phone = request.form.get("phone")
    email = request.form.get("email")
    ticket_category = request.form.get("ticket_category")
    payment = request.form.get("payment")

    if not fullname or not phone or not email or not ticket_category or not payment:
        return jsonify({"error": "All fields are required"}), 400

    user_info = f"{fullname}{phone}{email}{ticket_category}{payment}"
    user_hash = hash_info(user_info)

    # Check if user already exists
    users = load_data()
    for key, entry in users.items():
        if entry["hash"] == user_hash:
            return redirect(url_for('already_registered', user_hash=user_hash))

    new_entry = {
        "hash": user_hash,
        "fullname": fullname,
        "phone": phone,
        "email": email,
        "ticket_category": ticket_category,
        "payment": payment,
        "status": "not scanned"
    }
    save_data(new_entry)

    # Generate QR Code
    qr = qrcode.make(user_hash)
    qr_path = f"static/qr/{user_hash}.png"
    os.makedirs("static/qr", exist_ok=True)
    qr.save(qr_path)

    return render_template("qr_display.html", qr_code=qr_path, hash_value=user_hash)


# 🔹 Route: Show Already Registered User
@app.route("/already_registered")
def already_registered():
    """Show user information if already registered"""
    user_hash = request.args.get("user_hash")
    users = load_data()

    for key, entry in users.items():
        if entry["hash"] == user_hash:
            return render_template("already_registered.html", user=entry)

    return "User not found.", 404


# 🔹 Route: Verify Ticket
@app.route("/verify", methods=["GET"])
def verify():
    """Verify if user exists and update their scanned status"""
    hash_value = request.args.get("hash")

    users = load_data()
    for key, entry in users.items():
        if entry["hash"] == hash_value:
            if entry["status"] == "scanned":
                return jsonify({
                    "status": "already_scanned",
                    "message": f"⚠️ Ticket already used: {entry['fullname']} ({entry['ticket_category']})"
                }), 400

            # Update status to "scanned"
            ref.child(key).update({"status": "scanned"})

            return jsonify({
                "status": "success",
                "message": f"✅ Ticket Verified: {entry['fullname']} ({entry['ticket_category']} Ticket - {entry['payment']} Payment)"
            }), 200

    return jsonify({"status": "not_found", "message": "❌ Ticket Not Found"}), 404


# 🔹 Route: Secure QR Code Scanning Page
@app.route("/scan", methods=["GET", "POST"])
def scan_qr():
    """Secure the QR Code scanning page with a password"""
    if request.method == "POST":
        password = request.form.get("password")
        if password == ORGANISER_PASSWORD:
            return render_template("verify.html")  # Load the scanner page if password is correct
        else:
            return render_template("auth.html", error="Invalid Password")  # Show error message

    return render_template("auth.html")  # Show password input form






@app.route("/users", methods=["GET", "POST"])
def display_users():
    """ Secure the users page with a password and allow real-time search """
    
    query = request.args.get("search", "").strip().lower()
    print(f"🔍 Search query received: '{query}'")  # Debug

    if request.method == "POST":
        password = request.form.get("password")
        if password == ORGANISER_PASSWORD:
            data = load_data()
            print("nbr of users", len(data))
           
            if not isinstance(data, dict):
                print("⚠️ Data is not a dictionary! Resetting to empty list.")
                return render_template("users.html", users=[], search_query=query)

            users_list = list(data.values())

            

           
            if query:
                users_list = [
                    user for user in users_list if (
                        isinstance(user, dict) and (
                            query in user.get("fullname", "").lower() or
                            query in user.get("phone", "").lower() or
                            query in user.get("email", "").lower() or
                            query in user.get("ticket_category", "").lower() or
                            query in user.get("payment", "").lower() or
                            query in user.get("status", "").lower()
                        )
                    )
                ]
            nbr = len(users_list)
            print("nbr of users", len(data))
            # ✅ Vérifie si la requête est AJAX, retourne JSON
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify(users_list)  # 🔹 Retourne JSON pour fetch()

            return render_template("users.html", users=users_list, search_query=query, nbr=nbr)

        return render_template("auth.html", error="Invalid Password")  # Show error message

    return render_template("auth.html")



@app.route("/test_filter")
def test_filter():
    """Debug Route: Vérifie si le filtrage fonctionne"""
    data = load_data()
    query = request.args.get("search", "").strip().lower()

    users_list = list(data.values())
    filtered_users = [
        user for user in users_list if (
            isinstance(user, dict) and (
                query in user.get("fullname", "").lower() or
                query in user.get("phone", "").lower() or
                query in user.get("email", "").lower() or
                query in user.get("ticket_category", "").lower() or
                query in user.get("payment", "").lower() or
                query in user.get("status", "").lower()
            )
        )
    ]
    return jsonify(filtered_users)






@app.route("/users_vip", methods=["GET"])
def export_vip_premium_users():
    """Retrieve VIP & Premium users and provide a downloadable Excel file with formatted columns"""
    users = load_data()

    if not users:
        return jsonify({"message": "No users found"}), 404

    # Filter VIP & Premium users
    filtered_users = [
        user for user in users.values()
        if user.get("ticket_category") in ["VIP", "Premium"]
    ]

    if not filtered_users:
        return jsonify({"message": "No VIP or Premium users found"}), 404

    # Convert to DataFrame
    df = pd.DataFrame(filtered_users)

    # Define file path
    file_path = "vip_premium_users.xlsx"

    # Save to Excel
    df.to_excel(file_path, index=False, engine="openpyxl")

    # Load the workbook and adjust column widths
    wb = load_workbook(file_path)
    ws = wb.active

    for col in ws.columns:
        max_length = 0
        col_letter = col[0].column_letter  # Get the column letter (e.g., A, B, C)

        for cell in col:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass

        ws.column_dimensions[col_letter].width = max_length + 2  # Adjust width

    # Save the formatted file
    wb.save(file_path)

    # Provide the file as a downloadable response
    return send_file(file_path, as_attachment=True, download_name="VIP_Premium_Users.xlsx")







if __name__ == "__main__":
    os.makedirs("static/qr", exist_ok=True)  # Ensure QR directory exists
    app.run(host="0.0.0.0", port=5000, debug=False)

