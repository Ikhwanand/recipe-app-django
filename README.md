# Delicious Recipe Sharing Platform

A feature-rich recipe sharing web application built with Django where users can share, discover, and interact with recipes.

## 🌟 Features

### Recipe Management
- Create, edit, and delete recipes
- Add ingredients and step-by-step instructions
- Upload recipe images
- Categorize recipes
- Set difficulty levels and cooking times
- Toggle recipe publication status

### User Features
- User registration and authentication
- Custom user profiles with avatars
- Social authentication options
- Password reset functionality
- Email notifications

### Social Interaction
- Comment on recipes
- Rate recipes (1-5 stars)
- Favorite recipes
- Share recipes
- Follow other users

### Blog System
- Create and manage blog posts
- Categorize blog posts
- Comment on blog posts
- Newsletter subscription

### Search & Discovery
- Search recipes by title, ingredients, or category
- Filter recipes by difficulty and cooking time
- Browse recipes by category
- View trending and popular recipes

### User Dashboard
- View personal recipe collection
- Manage favorite recipes
- Track recipe ratings and comments
- Monitor user statistics

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Django 5.1.3+
- SQLite (default) or PostgreSQL

### Installation

1. Clone the repository:
```bash
git clone [your-repository-url]
cd recipe-app-django
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the application.

## 🛠️ Technology Stack

### Backend
- Django 5.1.3
- Python 3.12
- SQLite/PostgreSQL
- django-allauth for authentication

### Frontend
- HTML5, CSS3, JavaScript
- Bootstrap 4
- Font Awesome icons
- jQuery

### Features
- Responsive design
- User-friendly interface
- Mobile-first approach
- Modern UI components

## 📁 Project Structure

```
recipe-app-django/
├── recipes/                 # Main application
│   ├── models.py           # Database models
│   ├── views.py            # View logic
│   ├── forms.py            # Form definitions
│   ├── urls.py             # URL routing
│   └── templates/          # HTML templates
├── static/                 # Static files
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript files
│   └── img/               # Images
├── media/                 # User-uploaded content
├── templates/             # Base templates
└── manage.py             # Django management script
```

## 👥 User Roles

### Anonymous Users
- View recipes and blog posts
- Search and filter recipes
- Register an account

### Authenticated Users
- Create and manage recipes
- Comment and rate recipes
- Save favorite recipes
- Create blog posts
- Subscribe to newsletter

### Staff Users
- Manage recipe categories
- Moderate comments
- Edit any recipe
- Manage blog categories

## 🔒 Security Features

- User authentication
- CSRF protection
- Secure password handling
- Permission-based access control
- Form validation
- XSS prevention

## 🎨 Customization

### Theme
The application uses a custom "Delicious" theme with:
- Modern and clean design
- Responsive layout
- Custom components
- Consistent styling

### Configuration
Key settings can be modified in:
- `settings.py` for application settings
- `urls.py` for URL routing
- Template files for layout

## AI-Powered Recipe Assistant

The application includes an intelligent chatbot (Chef AI) that helps users with recipe recommendations and cooking advice. The chatbot uses the Phi-3-mini-4k-instruct model from Azure ML for natural language processing.

### Setting up the Chatbot

1. Get the API Key:
   - Visit [Phi-3-mini-4k-instruct Model](https://github.com/marketplace/models/azureml/Phi-3-mini-4k-instruct)
   - Generate your GitHub token with appropriate permissions
   - Add the token to your `.env` file:
     ```
     GITHUB_TOKEN=your_token_here
     ```

2. Install Required Packages:
   ```bash
   pip install azure-ai-inference azure-core
   ```

3. Features:
   - Personalized recipe recommendations
   - Cooking tips and advice
   - Ingredient-based recipe search
   - Difficulty and cooking time information
   - Multi-turn conversations

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## 📧 Contact

[Your Name] - [your.email@example.com]

Project Link: [https://github.com/yourusername/recipe-app-django]

## 🙏 Acknowledgments

- Django documentation
- Bootstrap team
- Font Awesome
- All contributors

---
Made with ❤️ by ikhwanand
