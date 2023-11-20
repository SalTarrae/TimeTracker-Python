# Reading Time Tracker System

The Reading Time Tracker System is a Django-based web application that tracks the time spent by users on reading books. The system includes a RESTful API for managing books, reading sessions, and user statistics.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [API Endpoints](#api-endpoints)
  - [Authentication](#authentication)
- [Docker](#docker)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

### Prerequisites

Make sure you have the following installed:

- [Python](https://www.python.org/) (>=3.8)
- [Django](https://www.djangoproject.com/) (>=3.2)
- [PostgreSQL](https://www.postgresql.org/) (or another database of your choice)
- [Redis](https://redis.io/) (for Celery)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/SalTarrae/time_tracker.git
   ```
   
1. Navigate to the project directory:
    
   ```bash
   cd time_tracker
   ```

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
   
1. Apply database migrations:

   ```bash
   python manage.py migrate
   ```
   
1. Run the development server:

   ```bash
   python manage.py runserver
   ```
   
Your application should be accessible at http://localhost:8000.

## Usage

### API Endpoints

- List of Books: GET /api/books/
- Book Detail: GET /api/books/<book_id>/
- Reading Session List: GET /api/reading-sessions/
- Start Reading Session: POST /api/start-reading-session/<book_id>/
- End Reading Session: PATCH /api/end-reading-session/<book_id>/
- Book Reading Time: GET /api/books/<book_id>/reading-time/
- User Statistics: GET /api/user-statistics/

### Authentication
The API requires user authentication using either session authentication or token authentication. Include the token in the Authorization header for token-based authentication.

### Docker
The project can be easily containerized using Docker. Follow the Docker setup instructions to build and run the Docker container.

### Testing
Run the tests using Pytest:
   ```bash
   pytest time_tracker/book/tests.py
   ```

## Acknowledgments

- Thanks to the Django and Django REST Framework communities.

## Authors

- Denis Andriiuk - [SalTarrae](https://github.com/SalTarrae)
