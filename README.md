Pet Adoption API

A Django REST Framework–based backend for managing pet adoptions.
This API connects shelters with adopters, allowing shelters to list pets and adopters to submit adoption requests.

Built with:
	•	Django
	•	Django REST Framework
	•	drf-yasg (Swagger/OpenAPI docs)
	•	django-filter

⸻

Features
	•	User registration & authentication (Shelter or Adopter)
	•	Pet management
	•	Shelters can create, update, and delete pets
	•	Adopters can view pets, search, filter, and order results
	•	Adoption requests
	•	Adopters can submit requests for pets
	•	Shelters can approve, reject, or keep requests pending
	•	Role-based permissions
	•	Only shelters can manage pets
	•	Adopters cannot apply to their own pets
	•	Interactive API documentation at /swagger/

⸻

Installation

1. Clone the repo
   git clone https://github.com/JohnBonge/pet-adoption-api.git
cd pet-adoption-api

2. Create and activate virtual environment
   python3 -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows

3. Install dependencies
   pip install -r requirements.txt

4. Set up database
   python manage.py makemigrations
python manage.py migrate

5. Create superuser (admin)
   python manage.py createsuperuser

6. Run server
   python manage.py runserver

API Endpoints

Authentication
	•	POST /api/register/ → Register new user (adopter or shelter)
	•	POST /api/token/ → Obtain JWT access & refresh tokens
	•	POST /api/token/refresh/ → Refresh JWT token

Pets
	•	GET /api/pets/ → List pets (search, filter, order supported)
	•	POST /api/pets/ → Create pet (shelter only)
	•	PUT/PATCH /api/pets/{id}/ → Update pet (shelter owner only)
	•	DELETE /api/pets/{id}/ → Delete pet (shelter owner only)

Adoption Requests
	•	GET /api/adoptions/ → List adoption requests
	•	Adopters see their own requests
	•	Shelters see requests for their pets
	•	POST /api/adoptions/ → Create adoption request (adopter only)
	•	PATCH /api/adoptions/{id}/ → Update status (shelter only: approve/reject/pending)

⸻

Example Request

Register adopter

POST /api/register/
{
  "username": "john_doe",
  "password": "mypassword",
  "email": "john@example.com",
  "is_shelter": false
}

Register shelter

POST /api/register/
{
  "username": "happy_shelter",
  "password": "mypassword",
  "email": "shelter@example.com",
  "is_shelter": true
}

API Docs

Interactive Swagger UI is available at:
http://127.0.0.1:8000/swagger/

⸻

Running Tests
python manage.py test

Roadmap
	•	✅ Basic shelter & adopter roles
	•	✅ Pet management & adoption requests
	•	⏳ Notifications for approved/rejected adoptions
	•	⏳ Image uploads for pets

 Contributing
	1.	Fork the repo
	2.	Create a feature branch:
 git checkout -b feature/my-feature
 	3.	Commit changes:
 git commit -m "feat: add my feature"
 	4.	Push branch and open a PR

License

This project is licensed under the MIT License.
