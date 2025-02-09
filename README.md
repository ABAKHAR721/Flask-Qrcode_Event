# 🎟️ Flask QR Code Ticketing System
🔗 get your ticket: https://legendxtalk.onrender.com/
## 📌 Project Overview
This project is a **QR Code-based ticketing system** for the **LegendsXtalk** event, built with **Flask** and **Firebase Realtime Database**. It allows users to:
- **Register** for an event and generate a **QR code ticket**.
- **Scan QR codes** for ticket validation on the day of the event.
- **View and manage registrations** via an admin panel.
- **Send confirmation emails** to registered users.
- **Filter users** in real-time with search functionality.

## 🚀 Features
#### ✅ **User Registration** – Participants can register for the event and generate a unique QR code ticket.
#### ✅ **QR Code Generation** – A unique QR code is created for each registered user.
#### ✅ **Ticket Validation** – Organizers can scan QR codes to verify tickets.
#### ✅ **Firebase Realtime Database** – All registrations are stored securely in Firebase.
#### ✅ **Admin Panel** – Organizers can view, search, and manage registrations.
#### ✅ **Delete Users** – Admins can delete a user from the database by ID.
#### ✅ **Email Notifications** – Automatic email confirmation for registered users (optional).

---

## 🛠️ Installation & Setup
### 1️⃣ **Clone the Repository**
```bash
$ git clone https://github.com/your-repo/Flask_QRCode_Ticketing.git
$ cd Flask_QRCode_Ticketing
```

### 2️⃣ **Create & Activate a Virtual Environment**
```bash
$ python -m venv venv  # Create virtual environment
$ source venv/bin/activate  # (Linux/macOS)
$ venv\Scripts\activate  # (Windows)
```

### 3️⃣ **Install Dependencies**
```bash
$ pip install -r requirements.txt
```

### 4️⃣ **Setup Firebase Credentials**
- **Go to** [Firebase Console](https://console.firebase.google.com/)
- **Create a new project** & enable **Realtime Database**.
- **Download** your Firebase Admin SDK JSON file (`firebase_cred.json`).
- **Move** it to the root directory of your project.

### 5️⃣ **Run the Application**
```bash
$ python app.py
```
Server will run on:
```bash
http://127.0.0.1:5000/
```

---

## 📍 Usage Guide
### 🎫 **1. Register for the Event**
- Open the website.
- Fill in **full name, phone, email, ticket category, and payment method**.
- Click **"Get Your Ticket"** to generate a QR code.
- **Take a screenshot** of the QR code.

### 📸 **2. Bring Your QR Code on Event Day**
- Show your **QR code** to the organizer.
- The organizer will **scan** it using the admin panel.
- If valid, the system will **mark the ticket as scanned**.

### 🔍 **3. Admin Features**
- **Secure Login** – Admins must enter a password to access user data.
- **Search & Filter** – Find users by **name, phone, email, ticket category, or payment status**.
- **Delete User** – Remove a user by **Firebase ID**.
- **Send Bulk Emails** – Notify all registered users.

---

## 🔥 API Endpoints
### **User Registration & QR Code**
| Method | Endpoint       | Description |
|--------|---------------|-------------|
| `GET`  | `/register`   | Show registration form |
| `POST` | `/register`   | Submit user details & generate QR code |

### **QR Code Validation**
| Method | Endpoint     | Description |
|--------|-------------|-------------|
| `GET`  | `/verify?hash=<user_hash>` | Verify ticket & update scan status |

### **Admin Panel**
| Method | Endpoint       | Description |
|--------|---------------|-------------|
| `POST` | `/usddssehjjhjrs`      | Secure admin login |
| `GET`  | `/usdsdsddsercdccs?search=<query>` | Search users |
| `DELETE` | `/dcsdelcsdcete_usecdsr/<id>` | Delete user by Firebase ID |
| `POST` | `/send_emails` | Send bulk emails to all users |

---

## 🚀 Deployment
### **🔹 Deploy on Render**
1. **Push code to GitHub**.
2. **Create a new Render web service**.
3. **Connect GitHub repo** and set **Python** as runtime.
4. **Add environment variables** (Firebase credentials, organizer password).
5. **Deploy and get your website link**.

---

## 📩 Contact
👨‍💻 **Developed by**: Abdessamad Abakhar  
📧 **Email**: [abdssamad.abkhar22@gmail.com](mailto:abdssamad.abkhar22@gmail.com)  
🔗 **LinkedIn**: [Connect with me](https://www.linkedin.com/in/abakhar-abdessamad-735b18176/)  
📍 **Event Location**: [Salle Ahmed Boukmakh, Tanger](https://maps.app.goo.gl/SgTbTMuVYfcs8z366)  


---

## 🌟 Support the Project
If you found this project helpful and want to support, you can contribute to my CIH Bank account:

```
🔹 Account Name: CHOUAIB EL MASSAOUDI
🔹 IBAN: MA64 2301 2146 0815 0211 0286 0079
🔹 SWIFT: CIHMMAMC
```

Thank you! 🙌

