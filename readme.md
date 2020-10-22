# E-commerce Shop

Template of pizza shop, where you can add products to order, use search, add more products by admin panel.
[Web-site](https://) of the project.

## Installation

Python 3 must be installed. Download the code.

### Environment Variables 

Some of settings are taken from environment variables. Create `.env` near `manage.py` and write 2 variables there in this format:`VARIABLE=value`.

- `SECRET_KEY=your secret key`
- `DEBUG=True or False` - (default:`False`) debug mode. Set `True` if you need to debug the project.
- `PASSWORD=password from database`

### Requirements

Install requirements with command:
```
pip install -r requirements.txt
```

## Running Code

Create database with command:
```
python manage.py migrate
```

Run development server with command:
```
python manage.py runserver
```

## Admin panel 

Create superuser with command:
```
python manage.py create superuser
```

Link to the admin panel: `http://127.0.0.1:8000/admin/`. 
You can add products, customers, orders there. 

## Project's Purposes

The code is written like a test task after job interview.
