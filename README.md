# iForm

This Django-based video-sharing platform provides preliminary form analysis and is a starting point for other users to comment on weightlifting form. iForm enables users to upload, share, and comment on workout videos, similar to popular social media platforms, to decrease the likelihood of form-related injuries while weightlifting. It includes features such as user authentication, video uploads, comments, likes, and a follower system.

<img width="1508" alt="Screenshot 2024-05-29 at 5 42 44 PM" src="https://github.com/vikranthnara/iForm/assets/64695750/2a6e00f3-3cb1-4d56-952b-9e81492c8ddd">
<img width="1506" alt="Screenshot 2024-05-29 at 5 44 27 PM" src="https://github.com/vikranthnara/iForm/assets/64695750/10ae76f1-dc4f-4df7-9fd9-7217c7406385">


# Features
- User Authentication: Register, login, and manage user profiles.
- Video Uploads: Users can upload videos. 
- Comments and Likes: Users can comment on videos and like comments.
- Follow System: Users can follow other users to see their videos on the homepage. Notification Requests for private users. 
- Privacy Settings: Users can set their profiles to private or public.

# Technologies
Django: The project uses Django as the web framework.

SQLite: Default database for development.

Bootstrap: For styling and responsive design.


# Usage
Initialize the database:
python manage.py makemigrations
python manage.py migrate

Run: 
python manage.py runserver

Accessing the Application
Open your web browser and go to http://127.0.0.1:8000/ to start using the application.


# Contribution
Contributions to this project are welcome! To contribute, please fork the repository, make your changes, and submit a pull request.

#License
This project is licensed under the MIT License - see the LICENSE file for details.
