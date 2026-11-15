# High-Concurrency Bus Ticket Reservation API
 
A highly concurrent API built with Django and Redis, designed to handle race conditions and ensure data integrity during simultaneous booking requests.
 
## 🚀 Engineering Challenges Solved
 
- **Race Condition Prevention:** Implemented **Pessimistic Locking** using Django's `select_for_update()` and `transaction.atomic()` to ensure that a single seat cannot be purchased by multiple users requesting it at the exact same millisecond.
- **Temporary Seat Holding (TTL):** Integrated **Redis** to create a 10-minute temporary lock (Time-To-Live) when a user adds a seat to their cart. This eliminates the need for heavy background tasks; if the payment is not completed within 600 seconds, the lock automatically expires and the seat becomes available.
- **Optimized Database Queries:** Kept the database load minimal by verifying Redis cache locks before executing heavy PostgreSQL/SQLite queries.
- **Secure Authentication:** Integrated **JWT (JSON Web Tokens)** via Django REST Framework to protect endpoints, ensuring only authenticated users can reserve seats and view their booking history.
## 🛠️ Tech Stack
 
- **Backend:** Python, Django, Django REST Framework
- **Security:** SimpleJWT
- **In-Memory Cache / TTL:** Redis, Docker
- **Database:** SQLite (Development)
## ⚙️ Installation & Setup
 
1. **Clone the repository:**
```bash
git clone https://github.com/Dilara297/ticket-reservation-api.git
cd ticket-reservation-api
```
 
2. **Create and activate a virtual environment:**
```bash
python -m venv venv
source venv/Scripts/activate  # For Windows (Git Bash)
```
 
3. **Install dependencies:**
```bash
pip install django djangorestframework djangorestframework-simplejwt redis
```
 
4. **Start the Redis server (via Docker):**
```bash
docker run -d --name bilet-redis -p 6379:6379 redis
```
 
5. **Apply database migrations and create a superuser:**
```bash
python manage.py migrate
python manage.py createsuperuser
```
 
6. **Run the development server:**
```bash
python manage.py runserver
```
 
## 📡 API Endpoints
 
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/token/` | Obtain JWT access and refresh tokens | No |
| `GET` | `/api/rezerve/<id>/` | Lock a seat for 10 minutes (Redis TTL) | Yes (JWT) |
| `GET` | `/api/satin-al/<id>/` | Complete purchase, drop lock, write to DB | Yes (JWT) |
| `GET` | `/api/biletlerim/` | List all tickets purchased by the user | Yes (JWT) |
 