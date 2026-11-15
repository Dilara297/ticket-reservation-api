# High-Concurrency Bus Ticket Reservation API

A highly concurrent API built with Django and Redis, designed to handle race conditions and ensure data integrity during simultaneous booking requests.

## 🚀 Engineering Challenges Solved

* **Race Condition Prevention:** Implemented **Pessimistic Locking** using Django's `select_for_update()` and `transaction.atomic()` to ensure that a single seat cannot be purchased by multiple users requesting it at the exact same millisecond.
* **Temporary Seat Holding (TTL):** Integrated **Redis** to create a 10-minute temporary lock (Time-To-Live) when a user adds a seat to their cart. This eliminates the need for heavy background tasks; if the payment is not completed within 600 seconds, the lock automatically expires and the seat becomes available.
* **Optimized Database Queries:** Kept the database load minimal by verifying Redis cache locks before executing heavy PostgreSQL/SQLite queries.

## 🛠️ Tech Stack
* **Backend:** Python, Django, Django REST Framework
* **In-Memory Cache / TTL:** Redis
* **Database:** SQLite (Development) / PostgreSQL (Ready for Production)