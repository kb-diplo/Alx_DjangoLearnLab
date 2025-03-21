# Django Blog Project

This is a Django-based blog application that includes user authentication and profile management.

## Features

- **User Registration**: Users can register with a username, email, and password.
- **User Login**: Registered users can log in to access their profile.
- **Profile Management**: Authenticated users can update their email address.
- **User Logout**: Users can log out to end their session.

## Blog Post Management

- **List Posts**: Go to `/posts/` to view all blog posts.
- **View Post**: Click on a post title to view its details.
- **Create Post**: Go to `/posts/new/` to create a new post (requires login).
- **Edit Post**: Go to `/posts/<post_id>/edit/` to update a post (requires login and author permission).
- **Delete Post**: Go to `/posts/<post_id>/delete/` to delete a post (requires login and author permission).

## Comment Functionality

- **Add a Comment**: Go to a blog post detail page and use the comment form.
- **Edit a Comment**: Click the "Edit" link on a comment you authored.
- **Delete a Comment**: Click the "Delete" link on a comment you authored.

## Tagging and Search Functionality

- **Add Tags**: When creating or updating a post, add tags to categorize it.
- **Search**: Use the search bar to find posts by title, content, or tags.
- **View Tagged Posts**: Click on a tag to view all posts with that tag.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Alx_DjangoLearnLab/django_blog.git

