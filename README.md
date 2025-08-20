Pet Adoption API

Welcome to the Pet Adoption API — a Django-based backend application for managing pet adoptions, users, and adoption requests.

Features
	•	Custom User Model: CustomUser in userz app for authentication and user management.
	•	Adoption Requests: Users can submit adoption requests for pets.
	•	Home View: Basic home endpoint returning a welcome message.
	•	RESTful Endpoints: Structured views ready for API expansion.
	•	Modular Structure: Separate apps for userz, pets, and adoptions for scalability.

Installation
	1.	Clone the repository
       git clone <repository-url>
       cd pet-adoption-api

	2.	Create and activate a virtual environment
       python3 -m venv .venv
       source .venv/bin/activate  # macOS/Linux
       .venv\Scripts\activate     # Windows

	3.	Install dependencies
       pip install -r requirements.txt

	4.	Apply migrations
       python manage.py makemigrations
       python manage.py migrate

	5.	Run the development server
      python manage.py runserver

  6.	Test the home endpoint
      Visit http://127.0.0.1:8000/

Project Structure
pet-adoption-api/
├── adoptions/       # Adoption requests app
├── pets/            # Pets management app
├── userz/           # Custom user management app
├── config/          # Project settings & URLs
├── manage.py
└── requirements.txt
