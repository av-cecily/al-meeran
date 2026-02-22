# Al Meeran Upholstery - Project Documentation

## Project Overview
**Al Meeran Upholstery** is a modern, AI-powered web platform designed for a bespoke furniture restoration business in Bahrain. It features a responsive customer-facing website, an interactive Fabric Visualizer, a Quote Request system, and a comprehensive Admin Dashboard for managing orders, inventory, and leads.

## Tech Stack
- **Frontend:** HTML5, Tailwind CSS (via CDN), Vanilla JavaScript.
- **Backend:** Python Flask.
- **Database:** MySQL (via XAMPP).
- **Icons:** Lucide Icons.
- **Fonts:** Plus Jakarta Sans (Google Fonts).

## Project Structure

```
al-meeran-upholstery/
├── assets/                  # Static assets (Images, CSS, JS)
│   ├── images/              # All project images (Gallery, Fabrics, UI)
│   │   ├── fabric-samples/  # Fabric textures
│   │   └── gallery/         # Project portfolio images
│   ├── css/                 # (Legacy/Unused)
│   └── js/                  # (Legacy/Unused)
├── backend/                 # Python Flask Backend
│   ├── app.py               # Main Application Entry Point (API Routes)
│   ├── database.py          # Database Connection & Initialization
│   ├── requirements.txt     # Python Dependencies
│   └── __pycache__/         # Compiled Python files
├── css/                     # Main Stylesheets
│   ├── styles.css           # Custom CSS overrides
│   ├── components/          # Component-specific CSS
│   └── pages/               # Page-specific CSS
├── js/                      # Main JavaScript Logic
│   ├── components/          # Reusable UI Components
│   │   ├── global-loader.js # Injects Header/Footer dynamically
│   │   ├── cart.js          # Shopping Cart Logic
│   │   ├── assistant.js     # AI Chatbot Widget
│   │   └── fabric-visualizer.js # Visualizer Logic
│   └── pages/               # Page-specific Scripts
│       ├── home.js          # Homepage Logic (Fabric Grid)
│       ├── gallery.js       # Gallery Grid & Filtering
│       └── request-quote.js # Quote Form Handling
├── index.html               # Homepage
├── about.html               # About Us Page
├── shop.html                # Fabric Shop Page
├── gallery.html             # Portfolio Gallery Page
├── visualizer.html          # AI Fabric Visualizer Tool
├── quote.html               # Request a Quote Page
├── checkout.html            # Checkout Page
├── admin.html               # Admin Dashboard (Protected)
└── PROJECT_DOCUMENTATION.md # This file
```

## Key Files & Functionality

### Frontend
*   **`js/components/global-loader.js`**: The backbone of the frontend. It dynamically injects the Navigation Bar, Mobile Menu, Cart Drawer, and Footer into every HTML page, ensuring consistency without code duplication. It also handles the global Lightbox logic for image zooming.
*   **`js/pages/home.js`**: Fetches the top 6 fabric products from the backend API (`/api/products`) to display on the homepage. Includes a fallback to hardcoded data if the backend is offline.
*   **`js/pages/gallery.js`**: Fetches portfolio items from `/api/gallery`. Implements category filtering (Classic, Modern, Luxury).
*   **`admin.html`**: A comprehensive Single Page Application (SPA) style dashboard for the business owner.
    *   **Features:** View Orders, View Leads, Add/Edit/Delete Fabrics, Add/Edit/Delete Gallery Items.
    *   **Security:** Simple client-side auth (demo) + Token storage.
    *   **UI:** Custom modals for forms, alerts, and confirmations (no native browser alerts).

### Backend
*   **`backend/app.py`**: A Flask server that provides RESTful APIs.
    *   `GET/POST/PUT/DELETE /api/products`: Manage fabric inventory.
    *   `GET/POST/PUT/DELETE /api/gallery`: Manage portfolio images.
    *   `GET/POST /api/orders`: Submit and retrieve orders.
    *   `GET/POST /api/quotes`: Submit and retrieve quote requests.
    *   `POST /api/login`: Admin authentication.
*   **`backend/database.py`**: Handles MySQL connection. Contains an `init_db()` function that automatically creates the database (`al_meeran_upholstery`) and tables (`products`, `gallery`, `orders`, `quotes`, `admins`) if they don't exist, and seeds them with initial data.

## Setup Instructions

### 1. Prerequisites
*   **XAMPP** (or any MySQL Server) installed and running.
*   **Python 3.x** installed.

### 2. Backend Setup
1.  Open your terminal and navigate to the `backend` folder:
    ```bash
    cd backend
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Start the server (ensure XAMPP MySQL is running first):
    ```bash
    python app.py
    ```
    *The server will start at `http://localhost:5000`.*

### 3. Frontend Setup
*   Simply open `index.html` in your browser (or use Live Server in VS Code).
*   The frontend is pre-configured to talk to `http://localhost:5000`.

## Notes
*   **Images:** Uploaded images are stored in `assets/images/fabric-samples` and `assets/images/gallery`.
*   **Offline Mode:** If the backend is not running, the frontend will gracefully fall back to hardcoded demo data so the site remains usable for presentation.
