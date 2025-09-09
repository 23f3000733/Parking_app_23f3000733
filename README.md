# 🚗 Vehicle Parking Management System

A modern, full-featured vehicle parking management system built with Flask that enables seamless parking spot booking and management.

## 🌐 Live Demo
**[Parking App on Render](https://parking-app-23f3000733.onrender.com/)**

---

## 📖 Project Overview

This comprehensive parking management application provides users with the ability to search, book, and manage parking spots while offering administrators a powerful dashboard to oversee lots, spots, and system analytics. The system features real-time availability checking, user authentication, booking history tracking, and a responsive design optimized for all devices.

## 📺 Project Resources

- 🎥 **Video Walkthrough**: [Watch on Google Drive](https://drive.google.com/file/d/13J7nNYf6mK0Yp_p5avZYGeLsLgGcnaRh/view?usp=drive_link)
- 📄 **Detailed Report**: [View on Google Docs](https://docs.google.com/document/d/1-cdEpn6cOKBGVtIIlv8XHtrBqDfTrJKRM-Do9Yf1kRA/edit?usp=sharing)

---

## ✨ Key Features

### 👥 User Features
- 🔑 **User Authentication**: Secure registration and login system
- 📍 **Smart Search**: Real-time parking spot availability search
- ⏱️ **Time-Aware Booking**: Time-window based spot availability
- 📜 **Booking Management**: Complete booking history with status tracking
- ⭐ **Feedback System**: Rate and review parking experiences
- 🔔 **Real-time Notifications**: Stay updated with booking status changes

### 👨‍💼 Admin Features
- 🛠️ **Comprehensive Dashboard**: Manage lots, spots, and users
- 📊 **Analytics & Monitoring**: Track system usage and performance
- 🏗️ **Lot Management**: Create and configure parking lots
- 🚘 **Spot Control**: Add, modify, and manage individual parking spots

### 🎨 Technical Features
- 📱 **Responsive Design**: Modern UI that works on all devices
- ⚡ **Real-time Updates**: Live availability and booking status
- 🔒 **Secure Authentication**: Protected user sessions and admin access

---

## 🏗️ Project Structure

```
app/
├── 📁 static/           # CSS, JavaScript, and image assets
├── 📁 templates/        # Jinja2 HTML templates
├── 📁 instance/         # Local database files (git-ignored)
├── 🐍 app.py           # Application entry point
├── 🔐 auth.py          # Authentication routes and logic
├── 👤 user.py          # User-facing routes
├── 👨‍💼 admin.py         # Admin dashboard routes
├── 🗄️ models.py         # SQLAlchemy database models
├── 🛠️ utils.py          # Utility functions and decorators
├── ⚙️ config.py         # Application configuration
└── 📦 requirements.txt  # Python dependencies
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.8+ installed
- Git installed
- Virtual environment support

### Step-by-Step Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/vehicle-parking-app.git
   cd vehicle-parking-app/app
   ```

2. **Create Virtual Environment**
   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   
   # On Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration (Optional)**
   
   Create a `.env` file in the app directory:
   ```env
   SECRET_KEY=your-secret-key-here
   ADMIN_USERNAME=your-admin-username
   ADMIN_PASSWORD=your-admin-password
   ```

5. **Run the Application**
   ```bash
   flask run
   ```

6. **Access the Application**
   - 🌐 **Local URL**: http://127.0.0.1:5000
   - 👤 **Default Admin**: Username: `admin`, Password: `admin123`

---

## 🚀 Usage Guide

### For Users
1. **Register/Login**: Create an account or sign in to access the system
2. **Search Parking**: Browse available spots by location and time
3. **Book Spots**: Reserve parking spaces for your desired time slots
4. **Manage Bookings**: View history, current reservations, and provide feedback
5. **Notifications**: Stay updated with real-time booking notifications

### For Administrators
1. **Admin Dashboard**: Access comprehensive system management tools
2. **Lot Management**: Create and configure parking lots
3. **Spot Control**: Manage individual parking spaces and availability
4. **User Management**: Monitor user accounts and booking patterns
5. **Analytics**: Review system performance and usage statistics

---

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Modern responsive CSS framework
- **Authentication**: Flask-Login
- **Deployment**: Render-ready configuration

---

## 🤝 Contributing

We welcome contributions to improve the Vehicle Parking Management System!

### How to Contribute

1. **Fork the Repository**
   ```bash
   git fork https://github.com/yourusername/vehicle-parking-app.git
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-amazing-feature
   ```

3. **Make Changes**
   - Write clean, commented code
   - Follow existing code style
   - Test your changes thoroughly

4. **Commit Changes**
   ```bash
   git commit -m "Add: Your descriptive commit message"
   ```

5. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-amazing-feature
   ```

### Contribution Guidelines
- Ensure code follows PEP 8 standards
- Add appropriate comments and documentation
- Test all new features thoroughly
- Update README if adding new functionality

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📞 Support & Contact

- 🐛 **Issues**: [GitHub Issues](https://github.com/23f3000733/Parking_app_23f3000733/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/23f3000733/Parking_app_23f3000733/discussions)
- 📧 **Email**: sangalkartik4@gmail.com

---

## 🙏 Acknowledgments

- Flask community for excellent documentation
- Contributors who helped improve the system
- Beta testers who provided valuable feedback

---

<div align="center">

**⭐ Star this repository if you found it helpful!**

</div>