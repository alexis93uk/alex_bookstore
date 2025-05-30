# Alex Bookstore

## Table of Contents

- [Project Overview](#project-overview)  
- [Features](#features)  
- [Technologies Used](#technologies-used)  
- [Installation](#installation)  
- [Deployment](#deployment)  
- [Database and Data Structure](#database-and-data-structure)  
- [Testing](#testing)  
- [Usage](#usage)  
- [Project Structure](#project-structure)  
- [Environment Variables](#environment-variables)  
- [Known Issues](#known-issues)  
- [Future Improvements](#future-improvements)  
- [Author](#author)  
- [License](#license)  

---

## Project Overview

Alex Bookstore is a subscription-based web application built with Django that allows users to browse, read, and manage a collection of books categorized by genres. Premium content access is restricted to subscribed users. The application is deployed on Heroku, uses PostgreSQL as the database, and manages media files such as book covers using AWS S3.

---

## Features

- User registration and authentication  
- Subscription management with access control  
- Book browsing by categories  
- Support for free and premium books  
- Admin interface for content and user management  
- Responsive UI with Bootstrap  
- Cloud deployment on Heroku with AWS S3 media storage  

---

## Technologies Used

- Python 3.13  
- Django 5.1  
- PostgreSQL  
- AWS S3 for media storage  
- Heroku for cloud deployment  
- Bootstrap 5 for UI  
- Gunicorn WSGI server  
- Whitenoise for static files  

---

## Installation

### Prerequisites

- Python 3.13+  
- PostgreSQL  
- AWS account with S3 bucket setup  

### Setup Instructions

1. Clone the repository  
2. Create and activate a virtual environment  
3. Install dependencies via `pip install -r requirements.txt`  
4. Configure environment variables (see [Environment Variables](#environment-variables))  
5. Run database migrations  
6. Create a superuser  
7. Collect static files  
8. Run the development server  

---

## Deployment

Deployment is done on Heroku with the following steps:

1. Login to Heroku CLI  
2. Create or use an existing Heroku app  
3. Set required environment variables on Heroku  
4. Push the code to Heroku’s Git remote  
5. Run migrations on Heroku  
6. Access the live app via the Heroku URL  

---

## Database and Data Structure

### Database System

- The project uses **PostgreSQL**, a robust relational database system, to store all data persistently.

### Django Models and Relationships

The database schema is represented by the following Django models and their relations:

#### 1. **Category**

- Stores book categories or genres.
- Fields:
  - `id`: Primary key (auto-generated)  
  - `name`: String, name of the category  
  - `description`: Text, optional description  

#### 2. **Book**

- Stores books with metadata and content.
- Fields:
  - `id`: Primary key  
  - `title`: String, book title  
  - `author`: String, author’s name  
  - `description`: Text, book synopsis  
  - `category`: ForeignKey to Category (one-to-many)  
  - `is_premium`: Boolean, if the book requires subscription  
  - `image`: ImageField, book cover stored on AWS S3  
  - `full_text`: TextField, full book content (optional)  

#### 3. **UserProfile**

- Extends Django’s built-in User model for additional info.
- Fields:
  - `user`: OneToOneField to User  
  - `bio`: Text, optional user biography  

#### 4. **Subscription**

- Manages user subscription periods.
- Fields:
  - `user`: ForeignKey to User (one user can have multiple subscriptions)  
  - `start_date`: DateTimeField, subscription start  
  - `end_date`: DateTimeField, subscription end  

### Relationships Overview

| Model       | Relationship          | Related Model | Cardinality     |
|-------------|-----------------------|---------------|-----------------|
| Book        | ForeignKey (category) | Category      | Many books to one category |
| UserProfile | OneToOneField (user)  | User          | One-to-one      |
| Subscription| ForeignKey (user)     | User          | Many subscriptions to one user |

### Entity-Relationship Diagram (ERD)

*(Insert your ERD image here to visually represent these relationships)*

---

## Testing

- Automated tests cover models, views, and utilities.  
- Run tests locally with:  
  ```bash
  python manage.py test


*************

  # Presentation of Project 4 - alex bookstore
## Briefing
Alex Bookstore is a Django-based web application that enables users to browse categorized books, view detailed information, and access premium content through subscriptions, with integrated Stripe payments and AWS S3 for media.

## Structured layout:
Alex Bookstore features a clean, responsive layout with a persistent header and navigation bar. The home page presents a carousel highlighting featured books, followed by organized sections for categories and recent books. Each category page displays an overlay with a category image, description, and a list of related books, while individual book detail pages showcase cover images, book details, and a premium “Read Full Text” option for subscribers. Additionally, the site includes user authentication pages, subscription flows via Stripe, and an admin panel for managing content. The design, built with Bootstrap 5, ensures intuitive navigation and a consistent experience across devices.

## Manual Testing Procedures
### 1. User Registration and Authentication
#### Registration:
Navigate to the registration page (/users/register/) and create a new account by entering a unique username and password.
Confirm that a success message is displayed and that you are redirected appropriately (e.g., to the login page).
#### Login/Logout:
Log in with your newly registered account using the login page (/users/login/).
Verify that the navbar updates to show links for "Profile" and "Logout" once logged in.
Log out and ensure you’re redirected to the home page with the correct navigation links for unauthenticated users.

### 2. Browsing Book Categories
#### Homepage Categories:
On the homepage, check that all book categories are displayed with their corresponding images and descriptions.

#### Responsive Design:
Resize the browser window (or use browser developer tools) to ensure that the categories and their images adjust appropriately across various screen sizes.

### 3. Viewing Books in a Category
#### Category Detail Page:
Click on a category to view its detail page (/books/category/<id>/).
Confirm that the category detail page displays a smaller, well-sized category image along with the category description.
Check that each book in the category is listed in a Bootstrap card format, showing its cover image (from media/book_covers/), title, author, and a "Details" button.
Verify that if a book lacks an uploaded cover, a placeholder image is displayed instead.

### 4. Subscription and Payment Flow
#### Subscription Process:
Log in and click the "Subscribe" button.
On the subscription page, use Stripe’s test card number 4242 4242 4242 4242 with any valid future expiration date and any 3-digit CVC to simulate payment.
Confirm that after a successful payment, you see a success message and that your subscription status is updated on your profile.

#### Prevent Duplicate Subscriptions:
Try clicking the subscribe button again while your subscription is active.
Verify that the system informs you that you are already subscribed (or simply prevents duplicate subscriptions).

#### Cancellation and Resubscription:
Use the “Cancel Subscription” option on your profile page to cancel your current subscription.
Confirm that the subscription status changes to expired or canceled.
Then, reinitiate the subscription process to resume or extend your subscription, and verify that the system resets the subscription start and end dates accordingly.

### 5. Profile and Subscription Management
#### Profile Page:
Visit the profile page (/users/profile/) and check that your user information (username, email) is displayed along with your subscription status.
Ensure that when you have an active subscription, a "Cancel Subscription" link is visible.
After canceling, verify that the subscription status updates and the "Subscribe Now" button becomes available.

### 6. Data Management and Error Handling
#### Error Conditions:
Attempt to subscribe when you already have an active subscription and confirm that an informative message is shown.
If you cancel your subscription, ensure that re-subscribing correctly resumes the subscription (using the logic implemented in your views).

#### Media File Checks:
Use browser developer tools to verify that all media files (especially book cover images) load correctly and that there are no 404 errors.