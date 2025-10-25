# SEM Herbal Medicine Product API

A simple and modular **FastAPI** project for managing traditional herbal products (*"Jamu"*).  
This project demonstrates how to build a clean and structured REST API using FastAPI, complete with **automatic Swagger documentation**, **typed data models**, and **modular code organization**.

---

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [API Endpoints](#api-endpoints)
- [Project Components](#project-components)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

- **RESTful API** for managing Herbal Medicine products
- **Automatic interactive documentation** (Swagger UI & ReDoc)
- **Type validation** using Pydantic schemas
- **Modular architecture** with separated concerns (models, routers, schemas)
- **Clean code structure** following best practices
- **Fast and lightweight** built on FastAPI framework
- **Easy to extend** and maintain

---

## 📁 Project Structure

```
apipy/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── product_model.py      # Product data models
│   ├── routers/
│   │   ├── __init__.py
│   │   └── product.py             # Product API routes
│   └── schemas/
│       ├── __init__.py
│       └── product_schema.py      # Pydantic schemas for validation
├── LICENSE
├── main.py                        # Application entry point
└── README.md
```

---

## 🔧 Prerequisites

Before running this project, make sure you have the following installed:

- **Python 3.8+**
- **pip** (Python package manager)

---

## 🚀 Installation

1. **Clone the repository**

```bash
git clone https://github.com/rizts/apipy.git
cd apipy
```

2. **Create a virtual environment** (recommended)

```bash
python -m venv venv
```

3. **Activate the virtual environment**

- On Windows:
```bash
venv\Scripts\activate
```

- On macOS/Linux:
```bash
source venv/bin/activate
```

4. **Install dependencies**

```bash
pip install fastapi uvicorn
```

---

## ▶️ Running the Application

Start the development server using Uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at: `http://127.0.0.1:8000`

**Options:**
- `--reload`: Enable auto-reload on code changes (development only)
- `--host 0.0.0.0`: Make server accessible from other devices
- `--port 8080`: Change the port number

---

## 📚 API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

These interfaces allow you to test the API endpoints directly from your browser.

---

## 🛣️ API Endpoints

### Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/products` | Get all products |
| GET | `/products/{product_id}` | Get a specific product by ID |
| POST | `/products` | Create a new product |
| PUT | `/products/{product_id}` | Update an existing product |
| DELETE | `/products/{product_id}` | Delete a product |

### Example Request

**GET** `/products`

Response:
```json
{
  "status": "success",
  "data": [
    {
      "name": "Tamarind Herbal Medicine",
      "category": "Traditional Drinks",
      "price": 15000.0
    },
    {
      "name": "Ginger Herbal Medicine",
      "category": "Traditional Drinks",
      "price": 12000.0
    }
  ]
}
```

**POST** `/products`

Request Body:
```json
{
  "name": "Turmeric Herbal Medicine",
  "category": "Traditional Drinks",
  "price": 18000.0
}
```

Response:
```json
{
  "status": "success",
  "data": {
    "name": "Turmeric Herbal Medicine",
    "category": "Traditional Drinks",
    "price": 18000.0
  }
}
```

---

## 🧩 Project Components

### Models (`app/models/product_model.py`)
Contains the data structure and business logic for products. This is where you define how product data is stored and manipulated.

### Routers (`app/routers/product.py`)
Handles HTTP requests and defines API endpoints. Each router focuses on a specific resource (in this case, products).

### Schemas (`app/schemas/product_schema.py`)
Defines Pydantic models for request/response validation. This ensures data integrity and provides automatic type checking.

**Product Schema:**
- `name`: Product name (string)
- `category`: Product category (string)
- `price`: Product price in IDR (float)

**ProductResponse Schema:**
- `status`: Response status (success/error)
- `data`: Product data or None

### Main (`main.py`)
The entry point of the application. It initializes the FastAPI app and includes all routers.

---

## 🛠️ Technologies Used

- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern, fast web framework for building APIs
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** - Data validation using Python type hints
- **[Uvicorn](https://www.uvicorn.org/)** - Lightning-fast ASGI server

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

Risdy - [@rizts](https://linkedin.com/in/rizts)

Project Link: [https://github.com/rizts/apipy](https://github.com/rizts/apipy)

---

## 🙏 Acknowledgments

- FastAPI community for excellent documentation
- Indonesian SEM sector for inspiration
- Traditional Herbal Medicine makers for preserving cultural heritage

---

**Happy Coding! 🎉**