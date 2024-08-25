# app/routes.py
from datetime import datetime
import os
import json
import secrets
from PIL import Image
from flask import Blueprint, current_app, flash, redirect, render_template, url_for

from app.forms import PostForm


main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    with open(POSTS_FILE, 'r') as json_file:
        posts = json.load(json_file)
    return render_template('home.html', posts = posts)



POSTS_FILE = 'posts.json'

def initialize_posts_file():
    if not os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, 'w') as f:
            json.dump([], f)  # Initialize with an empty array

initialize_posts_file()
@main.route("/create_post", methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post_data = {
            'title': form.title.data,
            'content': form.content.data,
            'date_posted': datetime.utcnow().isoformat(),
            'image': save_post_picture(form.image.data) if form.image.data else None
        }

        # Load existing posts
        try:
            with open(POSTS_FILE, 'r') as json_file:
                posts = json.load(json_file)
        except FileNotFoundError:
            posts = []
        except json.JSONDecodeError:
            posts = []

        # Add new post
        posts.append(post_data)

        # Save back to the file
        with open(POSTS_FILE, 'w') as json_file:
            json.dump(posts, json_file, indent=4)

        flash('Post created successfully!', 'success')
        return redirect(url_for('main.home'))

    return render_template('create_post.html', title='Create Post', form=form)

def save_post_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/post_pics', picture_fn)
    
    # Ensure the directory exists
    if not os.path.exists(os.path.dirname(picture_path)):
        os.makedirs(os.path.dirname(picture_path))
    
    # Resize image if needed
    output_size = (400, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

