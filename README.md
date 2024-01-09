# Network Project (CS50 Web Programming)

## Project Overview

This project is an implementation of the "Network" assignment from CS50's Web Programming with Python and JavaScript course. It is designed as a simple social network web application that allows users to make posts, follow other users, and "like" posts.

### Features

- **User Authentication:** Users can register, log in, and log out.
- **Post Creation:** Users can create new text-based posts.
- **All Posts Viewing:** A page where users can view all posts from all users, with the most recent posts first.
- **User Profile:** Clicking on a username loads that user's profile page and shows their posts.
- **Following:** Users can follow/unfollow other users. A "Following" stream shows posts from followed users.
- **Pagination:** Posts are paginated, displaying a limited number of posts per page.
- **Edit Post:** Users can edit their own posts.
- **'Like' Functionality:** Users can 'like' and 'unlike' posts.

## Technologies Used

- Frontend: HTML, CSS (Bootstrap), JavaScript
- Backend: Python (Django)
- Database: SQLite

## Setup and Running the Project

1. **Clone the Repository:** `git clone [https://github.com/Fionajiangfj/network]`
2. **Navigate to the project directory:** `cd [network]`
3. **Install Dependencies:** `pip install -r requirements.txt`
4. **Run Migrations:** `python manage.py migrate`
5. **Start the Server:** `python manage.py runserver`
6. **Access the Application:** Open your web browser and navigate to `http://localhost:8000`.

## Additional Notes

- Replace `[your-repository-link]` and `[project-directory]` with your GitHub repository link and project directory name, respectively.
- Make sure to have Python and Django installed in your development environment.

## Contributing

This project is part of an academic course and is not intended for external contributions. However, any feedback or suggestions are welcome.
