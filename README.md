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
