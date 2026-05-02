# Al Meeran Upholstery — Enterprise Management System

> Premium bespoke furniture restoration, custom upholstery, and luxury interiors.
> Full-stack web application with AI-powered fabric visualizer, quote management, and admin dashboard.

---

## 📁 Project Structure

```
al-meeran/
├── run.py                          ← 🚀 Main entry point (always run this)
│
├── backend/                        ← Flask API (Python)
│   ├── app.py                      ← Flask app setup & routing
│   ├── config.py                   ← All configuration & paths
│   ├── .env                        ← Secret keys & API keys
│   ├── requirements.txt            ← Python dependencies
│   │
│   ├── controllers/                ← Request handling logic
│   ├── models/                     ← Database models
│   ├── routes/                     ← API route definitions
│   ├── services/                   ← Upload, validation, chatbot
│   ├── utils/                      ← JWT auth utilities
│   └── database/
│       ├── db_connection.py        ← MySQL connection pool
│       ├── schema.sql              ← Create tables
│       └── seed_data.sql           ← Sample data
│
├── frontend/                       ← HTML Pages
│   ├── index.html                  ← Homepage
│   ├── shop.html                   ← Fabric shop
│   ├── gallery.html                ← Project gallery
│   ├── visualizer.html             ← AI fabric visualizer
│   ├── quote.html                  ← Request a quote
│   ├── about.html                  ← About page
│   ├── services.html               ← Services page
│   ├── checkout.html               ← Checkout
│   └── static/
│       ├── assets/
│       │   ├── fabrics/            ← Fabric sample images
│       │   └── images/             ← General site images
│       ├── css/                    ← Stylesheets
│       └── js/
│           ├── components/         ← global-loader, cart, assistant
│           └── pages/              ← Page-specific scripts
│
└── documentation/                  ← Project docs & FYP proposal

---

## ⚙️ Prerequisites — Pehle Yeh Install Hona Chahiye

| Tool | Version | Download |
|------|---------|----------|
| Python | 3.10+ | https://www.python.org/downloads/ |
| XAMPP | Latest | https://www.apachefriends.org/ |
| Git | Any | https://git-scm.com/ |

> **Note:** XAMPP ka MySQL (MariaDB 10.4) use hota hai is project mein.

---

## 🚀 Setup & Run — Step by Step

### Step 1 — XAMPP MySQL Start Karo

1. **XAMPP Control Panel** kholo
2. **MySQL** ke saamne **Start** button dabao
3. Status `Running` hona chahiye (green)

> ⚠️ **Important:** Flask server chalane se PEHLE MySQL start karna zaroori hai.
> Agar MySQL baad mein start karo to server restart karna hoga.

---

### Step 2 — Database Setup Karo

XAMPP ka MySQL terminal use karo ya phpMyAdmin (http://localhost/phpmyadmin):

```sql
-- Database aur tables banao
source C:/Users/Administrator/Desktop/al-meeran/backend/database/schema.sql
```

Ya phpMyAdmin se:
1. `http://localhost/phpmyadmin` kholo
2. **Import** tab mein jao
3. `backend/database/schema.sql` file select karo
4. **Go** dabao

---

### Step 3 — Python Dependencies Install Karo

```bash
# Project folder mein jao
cd C:\Users\Administrator\Desktop\al-meeran

# Virtual environment banao (recommended)
python -m venv venv
venv\Scripts\activate

# Dependencies install karo
pip install -r backend/requirements.txt
```

---

### Step 4 — Environment Variables Set Karo

`backend/.env` file already bani hui hai. Agar customize karna ho:

```env
GEMINI_API_KEY=your_gemini_api_key_here
JWT_SECRET=meeran_super_secret_key_2026
ADMIN_PASSWORD=admin123
DB_HOST=127.0.0.1
DB_USER=root
DB_PASSWORD=
DB_NAME=al_meeran_upholstery
```

> Gemini API key ke liye: https://aistudio.google.com/apikey

---

### Step 5 — Server Chalao

```bash
# Project root mein run karo (al-meeran folder se)
python run.py
```

Yeh dikhega:
```
--- Al Meeran Upholstery: Enterprise Management System ---
Backend API: http://localhost:5000
Frontend: http://localhost:5000
-----------------------------------------------------------
 * Running on http://127.0.0.1:5000
```

---

### Step 6 — Browser Mein Kholo

| Page | URL |
|------|-----|
| 🏠 Homepage | http://127.0.0.1:5000 |
| 🧵 Fabric Shop | http://127.0.0.1:5000/shop.html |
| 🖼️ Gallery | http://127.0.0.1:5000/gallery.html |
| 🎨 AI Visualizer | http://127.0.0.1:5000/visualizer.html |
| 📝 Get a Quote | http://127.0.0.1:5000/quote.html |
| 🔐 Admin Login | http://127.0.0.1:5000/admin/login.html |
| 📊 Admin Dashboard | http://127.0.0.1:5000/admin/dashboard.html |

---

## 🔐 Admin Access

```
URL:      http://127.0.0.1:5000/admin/login.html
Username: admin
Password: admin123
```

Admin dashboard se yeh kar sakte ho:
- ✅ Fabric products add/delete
- ✅ Gallery items manage
- ✅ Customer quotes dekho
- ✅ Orders track karo
- ✅ Analytics report

---

## 🛠️ API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products` | Sab fabrics list |
| POST | `/api/products` | Naya fabric add (admin) |
| DELETE | `/api/products/<id>` | Fabric delete (admin) |
| GET | `/api/gallery` | Gallery items |
| POST | `/api/gallery` | Gallery item add (admin) |
| GET | `/api/quotes` | Sab quotes (admin) |
| POST | `/api/quotes` | Quote submit (customer) |
| POST | `/api/auth/login` | Admin login |
| POST | `/api/chat` | AI chatbot |
| GET | `/api/analytics` | Site analytics (admin) |

---

## ❗ Common Issues & Fixes

### ❌ "Can't connect to MySQL server"
```
Solution: XAMPP Control Panel se MySQL Start karo, phir server restart karo
```

### ❌ "Module not found" error
```bash
# Backend folder mein jao aur install karo
pip install -r backend/requirements.txt
```

### ❌ Fabric grid empty hai
```
1. MySQL chal raha hai check karo (XAMPP)
2. Database mein data hai check karo: http://localhost/phpmyadmin
3. Server restart karo: Ctrl+C phir python run.py
```

### ❌ Admin login nahi ho raha
```bash
# Backend folder mein jao aur password reset karo
cd backend
python reset_admin.py
```

### ❌ Port 5000 already in use
```bash
# Windows mein port free karo
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F
```

---

## 🗄️ Database Tables

| Table | Description |
|-------|-------------|
| `products` | Fabric samples catalogue |
| `gallery` | Project portfolio images |
| `orders` | Customer fabric sample orders |
| `quotes` | Upholstery quote requests |
| `admins` | Admin accounts |

---

## 📦 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, TailwindCSS (CDN), Vanilla JS |
| Backend | Python 3, Flask, Flask-CORS |
| Database | MySQL / MariaDB (via XAMPP) |
| Auth | JWT (PyJWT) |
| AI | Google Gemini API |
| Image Processing | rembg, Pillow |

---

## 👨‍💻 Development Notes

- **Always run `python run.py`** from the project root — `backend/app.py` seedha mat chalao
- **MySQL pehle start karo** — Flask server start ke waqt MySQL band ho to connection fail ho jata hai
- Static files Flask ke through serve hoti hain `/static/` URL path se
- Image paths DB mein `assets/fabrics/filename.jpg` format mein store hote hain
- Frontend `global-loader.js` navbar, footer aur cart dynamically inject karta hai

---

*Al Meeran Upholstery — FYP Project 2026*
