# Project Name

**Todo Application**

## Description
This project is a Todo Application built using Python and FastAPI. The application allows users to manage their tasks efficiently by providing functionality for creating, updating, deleting, and viewing todos. The project also includes user authentication, ensuring that each user's data is secure and accessible only to them.

## Features
- User authentication and secure access to personal tasks.
- CRUD operations for managing todos: Create, Read, Update, and Delete.
- Administrative features for managing users and todos.
- Built with FastAPI for high performance and ease of development.

## Project Structure
Here's the basic structure of the project:

```
todoapp3/
├── alembic/                  # Database migration scripts
├── routers/                  # Directory for different API route files
│   ├── admin.py              # Routes for admin-related operations
│   ├── auth.py               # Routes for authentication
│   ├── todos.py              # Routes for todo-related operations
│   └── users.py              # Routes for user-related operations
├── static/                   # Static files (JavaScript, CSS, images)
│   └── js/
│       └── dashboard.js      # JavaScript for dashboard functionality
├── templates/                # HTML templates for rendering web pages
│   ├── base.html             # Base template for inheritance
│   ├── dashboard.html        # User dashboard page
│   ├── home.html             # Home page
│   ├── login.html            # Login page
│   ├── modals.html           # Modal dialogs for various actions
│   └── register.html         # User registration page
│   └── todo_list.html        # Page displaying list of todos
├── test/                     # Test scripts for different modules
│   ├── test_admin.py         # Tests for admin functionality
│   ├── test_auth.py          # Tests for authentication
│   ├── test_main.py          # General application tests
│   ├── test_todos.py         # Tests for todo operations
│   ├── test_users.py         # Tests for user operations
│   └── utils.py              # Utility functions for tests
├── alembic.ini               # Alembic configuration file
├── database.py               # Database connection setup
├── dependencies.py           # Project dependencies and common utilities
├── main.py                   # Main application script
├── models.py                 # Database models
├── todosapp.db               # SQLite database file
└── README.md                 # Project documentation
```

## Requirements
Below are the dependencies required to run the Todo application:

```
aiofiles==24.1.0
annotated-types==0.7.0
anyio==4.6.2.post1
bcrypt==3.2.0
certifi==2024.8.30
cffi==1.17.1
click==8.1.7
ecdsa==0.19.0
fastapi==0.115.4
greenlet==3.1.1
h11==0.14.0
httpcore==1.0.6
httpx==0.27.2
idna==3.10
iniconfig==2.0.0
Jinja2==3.1.4
jose==1.0.0
MarkupSafe==3.0.2
packaging==24.2
passlib==1.7.4
pluggy==1.5.0
psycopg2-binary==2.9.10
pyasn1==0.6.1
pycparser==2.22
pydantic==2.9.2
pydantic_core==2.23.4
pytest==8.3.3
pytest-asyncio==0.24.0
python-jose==3.3.0
python-multipart==0.0.17
rsa==4.9
six==1.16.0
sniffio==1.3.1
SQLAlchemy==2.0.36
starlette==0.41.2
typing_extensions==4.12.2
uvicorn==0.32.0
```

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/username/todo-app.git
   ```

2. Navigate to the project directory:
   ```
   cd todo-app
   ```

3. Create and activate a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

4. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
- To run the main script and start the FastAPI server:
  ```
  uvicorn todoapp3.main:app --reload
  ```
- Once the server is running, you can access the API at `http://127.0.0.1:8000`.
- The application provides endpoints for managing todos, user authentication, and administrative tasks.

## Contribution
Feel free to submit pull requests, create issues, or make suggestions to improve the project. Contributions are welcome!

## License
This project is open-source and available under the [MIT License](LICENSE).

## Author
**Ivan Berg**  
Contact: [ivkoberg@gmail.com](mailto:ivkoberg@gmail.com)
