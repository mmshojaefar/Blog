# Blog

## Description

In short, this project is a blog that users can register and send post and comments.
Of course there are many features that will be explain below in details.

- There are 4 type of users:
    - Standard User: Can comments and likes and dislikes post and comments
    - Writer User: In addition to the above, this user can add post, edit and archive her/his posts.
    - Editor User: In addition to the above, this user can accept other posts and comments. This user also can edit, active and deactive each post to show and can login to admin page.
    - Admin User: In addition to the above, this user can set categories and manage users and their groups  and can login to admin page.
- Add tags and categories to posts.
- Like and dislike posts and comments.
- Edit posts.
- Schedule a post.
- Search in posts text.
- Advanced search in post text,title, tags and writers.
- Change password, user data and reset password if register with valid email.
- Using great rich-text editor for adding posts.

## Install the project

1- Install requirements

2- Change local_settings.py to settings.py and set name/user/password/host and secret key in settings.py

3- Install the pg_trgm extension in your PostgreSQL database. 

4- Run command below:
```python
python manage.py addgroups
```

Now you can use it like other django projects!

