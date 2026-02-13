# StuddyBuddy

**StuddyBuddy** is a Django web application where people can learn together by joining **common study rooms** based on different topics.

It allows users to discuss, share ideas, and collaborate openly instead of learning alone.

---

## Features

* User authentication (Email & Password)
* Social login with **Google** and **GitHub**
* User profiles with avatar support
* Topic-based **public study rooms**
* Real-time style message discussions
* File sharing inside rooms
* Search rooms by topic or keyword
* Fully responsive (mobile & desktop)
* Deployed on **PythonAnywhere**

---

## Important Concept

> **All rooms and topics are public.**
> There are **no private rooms** on StuddyBuddy.

This design encourages **open learning**, discovery of discussions, and community-driven knowledge sharing.

---

## Tech Stack

### Backend

* **Python**
* **Django**
* **SQLite** (For scaling, it can be replaced with PostgreSQL)
* **Django Allauth** (authentication & social login)

### Frontend

* HTML
* CSS (custom)
* Bootstrap icons
* Responsive layout

### Deployment

* PythonAnywhere
* Whitenoise (static files)

---

## Project Structure

```
Project_StuddyBuddy/
│
├── base/               # Core app (rooms, topics, messages)
├── users/              # Custom user model & profiles
├── studdybuddy/        # Project settings
├── templates/          # HTML templates
├── static/             # Static assets (CSS, images)
├── staticfiles/        # Collected static files (deployment)
├── manage.py
├── requirements.txt
└── README.md
```

---

## Installation & Setup (Local)

### Clone the repository

```bash
git clone https://github.com/your-username/studdybuddy.git
cd studdybuddy
```

### Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Environment variables

Create a `.env` file and add:

```env
SECRET_KEY=your_secret_key
DEBUG=True

OAUTH_GOOGLE_CLIENT_ID=your_google_client_id
OAUTH_GOOGLE_SECRET=your_google_secret

OAUTH_GITHUB_CLIENT_ID=your_github_client_id
OAUTH_GITHUB_SECRET=your_github_secret
```

---

### Run migrations

```bash
python manage.py migrate
```

### Create superuser

```bash
python manage.py createsuperuser
```

### Run the server

```bash
python manage.py runserver
```

Open:
 `http://127.0.0.1:8000`

---

## Authentication

StuddyBuddy supports:

* Email & password login
* Google OAuth
* GitHub OAuth

Powered by **django-allauth**.

---

## Who Is This For?

* Students
* Beginners
* Developers
* Anyone who wants to learn **together instead of alone**

---

## Is StuddyBuddy Free?

Yes — completely free to use.

---

## Future Improvements

* Real-time WebSocket chat
* Notifications
* Pagination for large rooms
* Better file management
* PostgreSQL for production

---

## Acknowledgements

Inspired by community-driven learning and open discussion platforms.

Built with ❤️ using Django.

---

## License

This project is open-source and free to use for learning purposes.

---

## Final Note

If you find this project helpful, consider giving it a ⭐ on GitHub!

Happy learning 

---
