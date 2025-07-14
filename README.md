# Backend Web Development with Django

## What is Backend Development?

Backend development refers to the server-side of a web application — the logic, database interactions, authentication, and communication that users don’t see directly.

It involves:
- Writing code that handles data storage and processing
- Creating APIs and services
- Interacting with databases
- Managing user authentication and authorization
- Handling business logic

In Django, backend development focuses on writing views, models, managing URLs, working with databases, and connecting to front-end templates or APIs.

---

## Common Django Vocabulary and Concepts

### 1. **Project**
A Django *project* is the entire application — it contains settings, URLs, and configuration for one or more apps.

### 2. **App**
A Django *app* is a modular component of a project. For example, a blog, accounts system, or store can be separate apps.

### 3. **Model**
Defines the structure of your database. Models are Python classes that map to database tables.

### 4. **View**
A view handles the request logic and returns an HTTP response. It connects the model (data) with the template (presentation).

### 5. **Template**
HTML files that render data from views. They use the Django Template Language (DTL) to display dynamic content.

### 6. **URLconf (urls.py)**
Defines the routes/URLs that map to views. Django uses this to determine what to show for each requested URL.

### 7. **Admin Site**
A built-in backend interface for managing your database objects. Easily customizable.

### 8. **ORM (Object-Relational Mapping)**
Django's ORM lets you interact with the database using Python classes and methods, rather than SQL.

### 9. **Migration**
Migrations are scripts Django uses to apply changes to your database schema, like creating tables or modifying fields.

### 10. **Form**
A way to handle input from users. Django forms can be manually created or automatically generated from models.

### 11. **Authentication**
Built-in system for managing users — login, logout, password management, and permissions.

### 12. **Static Files**
CSS, JavaScript, and images that are not dynamically generated. Handled separately from dynamic templates.

### 13. **Media Files**
Uploaded user content such as profile pictures or documents.

### 14. **QuerySet**
A collection of database records retrieved through a model. You can filter, sort, and manipulate them using Python code.

### 15. **Context**
A dictionary passed from the view to the template, containing the data to be rendered.

### 16. **Superuser**
An admin-level user who has all permissions in the Django admin site.

### 17. **Middleware**
Hooks into Django’s request/response processing. Used for things like authentication, security, and request modification.

---

## Getting Started with Django Backend

1. `django-admin startproject mysite` – Create a new Django project.
2. `python manage.py startapp blog` – Create a new app inside your project.
3. `python manage.py runserver` – Run the development server.
4. `python manage.py makemigrations` – Prepare changes to the database schema.
5. `python manage.py migrate` – Apply schema changes to the database.
6. `python manage.py createsuperuser` – Create an admin user for the Django admin panel.


# Django Model Relationship Field Types

Django ORM provides powerful ways to define relationships between models. Understanding model field relationships is essential for building structured, normalized databases.

---

## 1. ForeignKey (One-to-Many)

### Description:
Defines a **one-to-many** relationship. A single object of the related model can be associated with many objects of this model.

### Syntax:
```python
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
```

### Meaning:
- One author can write many books.
- Each book belongs to one author.

### `on_delete` Options:
- `CASCADE`: Deletes related books if the author is deleted.
- `SET_NULL`: Sets the field to NULL on delete (requires `null=True`).
- `PROTECT`: Prevents deletion of the related object.
- `SET_DEFAULT`: Sets a default value when related object is deleted.
- `DO_NOTHING`: Does nothing (not recommended without custom handling).

---

## 2. OneToOneField (One-to-One)

### Description:
Defines a **one-to-one** relationship. Each object of one model is related to only one object of another model.

### Syntax:
```python
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
```

### Use Case:
- Extending built-in `User` model with additional fields like bio, profile picture, etc.

---

## 3. ManyToManyField

### Description:
Defines a **many-to-many** relationship. Each object of one model can relate to many objects of another, and vice versa.

### Syntax:
```python
class Student(models.Model):
    name = models.CharField(max_length=100)
    courses = models.ManyToManyField(Course)
```

### Meaning:
- A student can enroll in multiple courses.
- A course can have multiple students.

### Extra Options:
- `through`: Define an intermediate model to customize the join table.
- `related_name`: Reverse accessor name from the related model.

---

##  Summary Table

| Relationship      | Field Type       | Reverse Accessor Example      |
|-------------------|------------------|--------------------------------|
| One-to-Many       | `ForeignKey`     | `author.book_set.all()`        |
| One-to-One        | `OneToOneField`  | `user.userprofile`             |
| Many-to-Many      | `ManyToManyField`| `student.courses.all()`        |

---

##  Best Practices

- Always specify `on_delete` when using `ForeignKey` or `OneToOneField`.
- Use `related_name` to avoid reverse accessor name conflicts.
- Use `null=True` and `blank=True` for optional relations.
- Use `through` if you need additional fields in many-to-many relationships.

---

## Example: Complete Relationship

```python
class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

class BookDetail(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    summary = models.TextField()

class Reader(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)
```

---

## Bonus: Use `select_related` and `prefetch_related`

To optimize queries involving relationships:

- `select_related`: For ForeignKey and OneToOne
- `prefetch_related`: For ManyToMany and reverse ForeignKey

```python
Book.objects.select_related('author').all()
Reader.objects.prefetch_related('books').all()
```

---

## Common Methods for Fetching Data from a Django Model

Django provides a powerful ORM (Object Relational Mapper) that allows you to interact with the database using Python code. Below are the most commonly used methods for retrieving data.

### 1. `.all()`
Retrieves all records from a model.
```python
students = Student.objects.all()
```

---

### 2. `.get()`
Returns a single object matching the query. Raises `DoesNotExist` if no result, or `MultipleObjectsReturned` if more than one.
```python
student = Student.objects.get(id=1)
```

---

### 3. `.filter()`
Returns a queryset matching given lookup parameters.
```python
students = Student.objects.filter(course='Python')
```

---

### 4. `.exclude()`
Returns a queryset excluding the specified parameters.
```python
students = Student.objects.exclude(status='inactive')
```

---

### 5. `.order_by()`
Orders the results by specified field(s). Use `-` for descending order.
```python
students = Student.objects.order_by('-created_at')
```

---

### 6. `.values()` / `.values_list()`
Returns dictionaries or tuples instead of model instances.
```python
# Dicts
students = Student.objects.values('id', 'name')

# Tuples
students = Student.objects.values_list('id', 'name')
```

---

### 7. `.first()` / `.last()`
Returns the first or last record in a queryset.
```python
first_student = Student.objects.first()
last_student = Student.objects.last()
```

---

### 8. `.exists()`
Returns `True` if the queryset contains any results.
```python
Student.objects.filter(email='john@example.com').exists()
```

---

### 9. `.count()`
Returns the number of records in the queryset.
```python
Student.objects.filter(course='Python').count()
```

---

### 10. `.distinct()`
Removes duplicates from the queryset.
```python
courses = Student.objects.values('course').distinct()
```


### 11: Chaining Queries
You can chain these methods together:
```python
students = Student.objects.filter(course='Python').exclude(status='inactive').order_by('name')
```

---



