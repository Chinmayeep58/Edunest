# 📝 EduNest - A Smart Learning Management System  

EduNest is a **Django-based** platform designed to help students efficiently manage their study materials, take notes, and track progress. With **user authentication, note-taking features, and activity tracking**, EduNest makes learning more structured and engaging.  

---

## 🚀 Features  

✅ **User Authentication** – Sign up, log in, and manage your profile.  
✅ **Notes Management** – Create, edit, and delete notes easily.  
✅ **User Activity Tracking** – Monitors login count, last login time, and notes accessed.  
✅ **Database-Driven** – Uses **MySQL** for data storage.  
✅ **Secure & Scalable** – Built with Django’s best practices.  

---

## 🔧 Tech Stack  

- **Backend:** Django, Django ORM, MySQL  
- **Frontend:** HTML, CSS, JavaScript   
- **Database:** MySQL  

---

## 🛠️ Installation & Setup  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/your-username/edunest.git
cd edunest
```

### 2️⃣ Create a Virtual Environment  
```bash
python -m venv venv
source venv/bin/activate   # For macOS/Linux
venv\Scripts\activate      # For Windows
```

### 3️⃣ Install Dependencies  
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure MySQL Database  
- Create a MySQL database named **`edunest_db`**.  
- Update the **`DATABASES`** section in `settings.py` with your MySQL credentials.

### 5️⃣ Apply Migrations  
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6️⃣ Create a Superuser (Optional)  
```bash
python manage.py createsuperuser
```

### 7️⃣ Run the Development Server  
```bash
python manage.py runserver
```
- Open **`http://127.0.0.1:8000/`** in your browser. 🎉  

