# Advanced API Project

This project is a Django REST Framework (DRF) API designed to manage books and authors. It includes CRUD operations, filtering, searching, ordering, and unit testing. Below is an overview of the tasks completed and how to set up and use the project.

---

## **Tasks Completed**

### **1. Setting Up a New Django Project with Custom Serializers**
- **Objective**: Set up a Django project with DRF and create custom serializers for complex data structures and nested relationships.
- **Steps**:
  - Installed Django and DRF.
  - Created models for `Author` and `Book` with a one-to-many relationship.
  - Implemented custom serializers (`BookSerializer`, `AuthorSerializer`) with nested relationships and validation (e.g., ensuring `publication_year` is not in the future).
  - Documented the models and serializers in `models.py` and `serializers.py`.

---

### **2. Building Custom Views and Generic Views**
- **Objective**: Implement custom and generic views for CRUD operations on the `Book` model.
- **Steps**:
  - Created generic views (`ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`) for the `Book` model.
  - Configured URL patterns in `api/urls.py` to map to these views.
  - Added permissions to restrict `CreateView`, `UpdateView`, and `DeleteView` to authenticated users.
  - Tested the views using tools like Postman and documented their configurations.

---

### **3. Implementing Filtering, Searching, and Ordering**
- **Objective**: Enhance the API with filtering, searching, and ordering capabilities.
- **Steps**:
  - Integrated `DjangoFilterBackend` to filter books by `title`, `author`, and `publication_year`.
  - Added `SearchFilter` to enable searching by `title` and `author`.
  - Configured `OrderingFilter` to allow ordering by `title` and `publication_year`.
  - Updated `BookListView` to include these features and tested them using API tools.

---

### **4. Writing Unit Tests**
- **Objective**: Ensure the API behaves as expected by writing comprehensive unit tests.
- **Steps**:
  - Wrote unit tests in `api/tests.py` to test CRUD operations, filtering, searching, ordering, and permissions.
  - Used Django’s test framework to simulate API requests and verify response data and status codes.
  - Documented the testing strategy and provided guidelines for running tests.

---

## **Installation and Setup**

### **Prerequisites**
- Python 3.x
- Django
- Django REST Framework
- Django Filter

### **Steps**
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Alx_DjangoLearnLab.git
   ```
2. Navigate to the project directory:
   ```bash
   cd advanced-api-project
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```

---

## **Running the Tests**
To run the unit tests, use the following command:
```bash
python manage.py test api
```

---

## **API Endpoints**
- **List Books**: `GET /api/books/`
- **Retrieve a Book**: `GET /api/books/<int:pk>/`
- **Create a Book**: `POST /api/books/create/`
- **Update a Book**: `PUT /api/books/update/`
- **Delete a Book**: `DELETE /api/books/delete/`

### **Filtering, Searching, and Ordering**
- **Filter by Title**: `GET /api/books/?title=Test Book`
- **Search by Title or Author**: `GET /api/books/?search=Test`
- **Order by Publication Year**: `GET /api/books/?ordering=-publication_year`

---

## **Documentation**
- **Models**: Described in `api/models.py`.
- **Serializers**: Documented in `api/serializers.py`.
- **Views**: Detailed in `api/views.py`.
- **Tests**: Explained in `api/tests.py`.

---

## **Contributing**
Feel free to contribute to this project by opening issues or submitting pull requests. Ensure all tests pass before submitting changes.

---

## **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

