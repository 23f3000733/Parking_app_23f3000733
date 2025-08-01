# Vehicle Parking App

A modern, full-featured vehicle parking management system built with Flask.

## 🚗 Project Overview
This application allows users to search, book, and manage parking spots, while providing an admin dashboard for managing lots, spots, and viewing analytics. It features user authentication, booking history, feedback/rating, and a responsive UI.

## ✨ Features
- User registration, login, and dashboard
- Search and book available parking spots
- Time-window aware spot availability
- Booking history and feedback/rating system
- Admin dashboard for managing lots, spots, and users
- Real-time notifications UI
- Responsive, modern design

## 🏗️ Project Structure
```
app/
  ├── admin.py         # Admin routes
  ├── auth.py          # Authentication routes
  ├── user.py          # User routes
  ├── models.py        # SQLAlchemy models
  ├── utils.py         # Utility functions/decorators
  ├── config.py        # Configuration
  ├── app.py           # App entry point
  ├── requirements.txt # Python dependencies
  ├── static/          # CSS, JS, images
  ├── templates/       # Jinja2 templates
  └── instance/        # Local database (ignored)
```

## ⚙️ Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo/app
   ```
2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up environment variables (optional):**
   - Create a `.env` file or set variables for `SECRET_KEY`, `ADMIN_USERNAME`, `ADMIN_PASSWORD` as needed.
5. **Run the app:**
   ```bash
   flask run
   ```
   The app will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 👤 Default Admin Login
- **Username:** `admin`
- **Password:** `admin123`

## 📝 Usage
- Register as a user to book parking spots.
- Log in as admin to manage lots, spots, and view analytics.
- Use the notification bell for real-time updates.

## 🤝 Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Create a new Pull Request

## 📄 License
This project is licensed under the MIT License.
