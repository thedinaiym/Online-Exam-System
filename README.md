# Educational Quiz Platform

## Project Overview

This is a comprehensive educational quiz platform built with Django, allowing users to take quizzes across different subjects, track their performance, and manage quiz content.

## Features

- **Multiple Subject Support**: Create and manage quizzes for different subjects
- **Question Management**: Add, edit, and delete questions with multiple-choice options
- **Leaderboard**: Track user performance across different subjects
- **Fraud Detection**: Built-in mechanism to identify potential fraudulent activities

## Project Structure

### Models

#### 1. Subject
- Stores different subject categories
- Unique name for each subject
- One-to-many relationship with Questions

#### 2. Question
- Contains quiz questions for specific subjects
- Includes question text and four options
- Tracks correct option
- Linked to a specific subject

#### 3. Leaderboard
- Records user scores
- Tracks performance per subject
- Supports multiple user attempts

#### 4. Fraud Model
- Monitors user activities
- Flags potential fraudulent behavior

## Database Management

### Using Python (main.py)

You can manage the database directly using Python. Here's an example of how to interact with the models:

```python
# main.py
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz.settings')
django.setup()

# Import models
from your_app.models import Subject, Question, Leaderboard, FraudModel

# Create a new subject
math_subject = Subject.objects.create(name='Mathematics')

# Add a question to the subject
question = Question.objects.create(
    subject=math_subject,
    qno=1,
    question='What is 2 + 2?',
    o1='3',
    o2='4',
    o3='5',
    o4='6',
    co='4'
)

# Add a leaderboard entry
leaderboard_entry = Leaderboard.objects.create(
    username='student1',
    subject=math_subject,
    score=85
)

# Check for fraud
fraud_check = FraudModel.objects.create(
    username='student1',
    fraud=False
)
```

## Database Relations Visualization

You can view the detailed database relations diagram at:
[Mermaid Chart - Database Relations](https://www.mermaidchart.com/app/projects/b9cf9467-618a-4992-8305-920219ecbb7c/diagrams/804cef43-9343-40ee-858a-f3c7dcee03ac/version/v0.1/edit)

1. If you want to manage database without Django ORM
```bash
python main.py
```

## Prerequisites

- Python 3.8+
- Django 3.2+
- Virtual Environment (recommended)

## Installation

1. Clone the repository
```bash
git clone https://your-repository-url.git
cd your-project-directory
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Setup Database
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create Superuser
```bash
python manage.py createsuperuser
```

6. Run Development Server
```bash
python manage.py runserver
```
## Configuration

### Environment Variables
- `SECRET_KEY`: Django secret key
- `DEBUG`: Development mode toggle
- `DATABASE_URL`: Database connection string

## Testing

Run tests with:
```bash
python manage.py test
```

## Deployment

Recommended platforms:
- Heroku
- AWS Elastic Beanstalk
- DigitalOcean App Platform

## Security Considerations

- Implemented fraud detection mechanism
- Use strong password policies
- Regular security audits
- HTTPS enforcement

## Future Roadmap

- [ ] User authentication system
- [ ] Detailed analytics dashboard
- [ ] Mobile responsive design
- [ ] Internationalization support

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Your Name - dinaiym.dubanaeva@alatoo.edu.kg

Project Link: [https://github.com/thedinaiym/Online-Exam-System.git]