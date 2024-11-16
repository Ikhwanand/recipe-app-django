# Recipe Sharing App

A Django-based web application for sharing and discovering recipes. Users can create accounts, share their favorite recipes, and explore recipes shared by others.

## Features

- User Authentication (Login, Register, Password Reset)
- Recipe Management (Create, Read, Update, Delete)
- Recipe Categories
- User Profiles
- Responsive Design
- Email Verification

## Technologies Used

- Python 3.x
- Django 5.1.3
- Bootstrap 4
- SQLite (Development)
- django-allauth for authentication

## Installation

1. Clone the repository
   ```bash
   git clone <repository-url>
   cd recipe-app-django
   ```

2. Create a virtual environment and activate it
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your environment variables:
   ```
   EMAIL_HOST_USER=your_email@gmail.com
   EMAIL_HOST_PASSWORD=your_app_password
   ```

5. Run migrations
   ```bash
   python manage.py migrate
   ```

6. Create a superuser (admin)
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server
   ```bash
   python manage.py runserver
   ```

## Usage

1. Register a new account or login with existing credentials
2. Create and share your recipes
3. Browse recipes shared by other users
4. Update or delete your own recipes
5. View user profiles and their shared recipes

## Project Structure

```
recipe-app-django/
├── recipe_sharing_app/     # Main project directory
│   ├── settings.py        # Project settings
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py           # WSGI configuration
├── recipes/              # Main app directory
│   ├── models.py         # Database models
│   ├── views.py          # View functions
│   ├── urls.py          # App URL configuration
│   └── forms.py         # Forms
├── templates/           # HTML templates
│   ├── recipes/        # Recipe templates
│   └── account/        # Authentication templates
├── static/             # Static files (CSS, JS, images)
├── media/             # User-uploaded files
├── requirements.txt   # Project dependencies
└── manage.py         # Django management script
```

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## Environment Variables

The following environment variables are required:

- `EMAIL_HOST_USER`: Gmail address for sending emails
- `EMAIL_HOST_PASSWORD`: Gmail app password for authentication

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Django Documentation
- Bootstrap Documentation
- django-allauth Documentation
