# 🥝 Fruitables

Fruitables is a modern and user-friendly **online fruit and vegetable store** built with Django. It includes essential e-commerce features such as product management, shopping cart, wishlist, and order placement.

---

## 🚀 Features

- 🔐 User registration and login
- 🛒 Shopping cart functionality
- ❤️ Wishlist support
- 📦 Order placement with checkout
- ✉️ Email subscription
- 🖼️ Full CRUD for products with images
- 🔍 Product search

---

## 🛠 Technologies Used

- Python 3.12.3
- Django 5.2.2
- Django ORM
- Bootstrap 5
- SQLite (or other supported DBs)

---

## 📂 Project Structure

```
Fruitables/
├── accounts/        # User authentication and profiles
├── cart/            # Cart logic
├── orders/          # Order management
├── products/        # Product CRUD and categories
├── wishlist/        # Wishlist handling
├── templates/       # HTML templates
├── static/          # CSS, JS, and images
└── manage.py
```

---

## ⚙️ Getting Started (Local Development)

```bash
git clone https://github.com/turdalihasanboyev/Fruitables.git
cd Fruitables
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## 👤 User Access

```text
Admin panel: /admin
Register/Login: /register or /login
```

---

## 📸 Screenshots

> Optional: Add screenshots of your UI (`/static/img/screenshot.png`) to showcase features.

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## 📧 Author

**Turdali Hasanboyev**  
Backend Developer  
[GitHub Profile](https://github.com/turdalihasanboyev)

---

## 📝 License

This project is licensed under the MIT License.
