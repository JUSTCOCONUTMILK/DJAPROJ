```bash
git clone https://github.com/JUSTCOCONUTMILK/DJAPROJ.git
cd DJAPROJ
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py init_admin
python manage.py runserver
```
