# Book Management REST API with JWT Authentication

**Author**: Avishek Majumder  
**Course**: Ostad Python & Django Development  
**Assignment**: Module 12 Assignment  

A robust Book Management REST API built using Django and Django REST Framework (DRF).

Features included:
- JWT Authentication (djangorestframework-simplejwt)
- Role-based Permissions (Public Read-Only, Authenticated CRUD)
- Filtering by category & author (django-filter)
- Searching by title & author (SearchFilter)
- Ordering by title, price, published_date (OrderingFilter)
- Pagination (5 books per page)
- Throttling (Rate limiting for anonymous and authenticated users)

---

## Requirements & Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Avishek-Majumder/book-management-rest-api-jwt.git
   cd book-management-rest-api-jwt
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

5. Seed sample data & create superuser:
   ```bash
   python manage.py seed_books
   ```
   Creates superuser: `admin` / `adminpassword123` and populates 10 sample books.

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

---

## Authentication (JWT)

| Endpoint | Method | Purpose | Payload Example |
|---|---|---|---|
| `/api/token/` | `POST` | Obtain access & refresh JWT tokens | `{"username": "admin", "password": "adminpassword123"}` |
| `/api/token/refresh/` | `POST` | Refresh an expired access token | `{"refresh": "<YOUR_REFRESH_TOKEN>"}` |

To access protected endpoints (`POST`, `PUT`, `PATCH`, `DELETE`), pass the access token in the `Authorization` header:
```
Authorization: Bearer <YOUR_ACCESS_TOKEN>
```

---

## Book API Endpoints

| Method | Endpoint | Description | Permissions |
|---|---|---|---|
| `GET` | `/books/` | View list of books (Paginated, 5 per page) | Anyone |
| `GET` | `/books/<id>/` | View single book details | Anyone |
| `POST` | `/books/` | Create a new book | Authenticated Users |
| `PUT` | `/books/<id>/` | Update a book | Authenticated Users |
| `PATCH` | `/books/<id>/` | Partially update a book | Authenticated Users |
| `DELETE` | `/books/<id>/` | Delete a book | Authenticated Users |

---

## Features & Query Parameters

### 1. Filtering
Filter books by `category` or `author`:
```http
GET /books/?category=Programming
GET /books/?author=Eric%20Matthes
```

### 2. Searching
Search books by `title` or `author`:
```http
GET /books/?search=Python
```

### 3. Ordering
Order books by `title`, `price`, or `published_date` (Ascending or Descending):
```http
GET /books/?ordering=price
GET /books/?ordering=-price
GET /books/?ordering=-published_date
```

### 4. Pagination
Results are paginated at 5 items per page:
```http
GET /books/?page=1
GET /books/?page=2
```

### 5. Combined Query Example
```http
GET /books/?search=Python&ordering=-price&page=2
```
Searches for books containing "Python", orders them by price from highest to lowest, and returns page 2.

---

## Running Automated Tests

To execute the unit test suite covering JWT authentication, permission guards, CRUD operations, filtering, searching, ordering, pagination, and throttling:

```bash
python manage.py test books
```
