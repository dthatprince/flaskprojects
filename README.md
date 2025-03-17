# Flask Blog Application

## Overview

This is a **Flask-based Blog Application** that allows users to **create, read, update, and delete blog posts**. It includes user authentication, session management, and access control using **Flask-Login, Flask-WTF, and SQLAlchemy**.

---

## Features

### Authentication
- User **Signup & Login** with hashed passwords
- **Session Management** using Flask-Login
- **Logout** functionality

### Blog Management
- **Create, Update, and Delete** Blog Posts (Only by the author)
- **View All Posts** (Public)
- **Click on a Blog Post** to view full content

### Security
- **Password Hashing** using `werkzeug.security`
- **CSRF Protection** with Flask-WTF
- **Session Security** with Flask-Login

---

## Technologies Used

- **Python** (Flask, SQLAlchemy, Flask-WTF, Flask-Login)
- **HTML & Jinja2** (Templating)
- **Bootstrap** (Styling & Flash Messages)
- **SQLite** (Database)

---

## Installation & Setup

### 1. Clone the Repository
```sh
git clone https://github.com/dthatprince/flaskproject.git
cd flaskproject
```

### 2. Create & Activate Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Run the Application
```sh
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 5. Run the Application
```sh
flask --app app --debug run
```

The application will run at **`http://127.0.0.1:5000/`**

---

## Usage

### 1. Signup & Login
- Visit `/signup` to **register** a new account.
- Visit `/login` to **log in**.

### 2. Create & Manage Blog Posts
- Once logged in, go to `/create_post` to **add a blog post**.
- Click on a **blog post title** to **view full details**.
- If you're the author, you can **edit or delete** your posts.

### 3. Logout
- Click **Logout** to end your session.

---

## Routes & Endpoints

| Route               | Method      | Description                        |
| ------------------- | ----------- | ---------------------------------- |
| `/signup`           | `GET, POST` | User registration                  |
| `/login`            | `GET, POST` | User authentication                |
| `/logout`           | `GET`       | User logout                        |
| `/dashboard`        | `GET`       | User dashboard (Protected)         |
| `/create_post`      | `GET, POST` | Create a new blog post (Protected) |
| `/posts`            | `GET`       | View all blog posts (Protected)    |
| `/post/<id>`        | `GET`       | View a specific blog post          |
| `/update_post/<id>` | `GET, POST` | Edit a blog post (Protected)       |
| `/delete_post/<id>` | `POST`      | Delete a blog post (Protected)     |
| `/about`            | `GET`       | About page                         |
| `/contact`          | `GET`       | Contact page                       |

---

## Future Improvements

- Implement **password reset via email**
- Add **profile page for users**
- Support **pagination for blog posts**

---

## Author

**[https://github.com/dthatprince](https://github.com/dthatprince)**

