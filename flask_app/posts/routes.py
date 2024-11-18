from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import current_user, login_required

from ..forms import PostForm, CommentForm
from ..models import User, Post, Comment
from ..utils import current_time, get_b64_img
from werkzeug.utils import secure_filename

posts = Blueprint("posts", __name__)

@posts.route("/", methods=["GET", "POST"])
def index():
    posts = Post.objects().order_by('-date')
    return render_template("index.html", results=posts)

@posts.route("/add_post", methods=["GET", "POST"])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        if Post.objects().count() > 0:
            id = Post.objects().order_by('-date').first().post_id + 1
        else:
            id = 1
        post = Post(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            date=current_time(),
            post_title=form.title.data,
            post_id= id,
            meal_type=form.meal_type.data,
            home_rest=form.home_rest.data
        )
        img = form.image.data
        if img:
            filename = secure_filename(img.filename)
            content_type = f'images/{filename[-3:]}'
            post.image.put(img.stream, content_type=content_type)
        post.save()
        return redirect(url_for("posts.index"))
    return render_template("add_post.html", title="Add a post", form=form)

@posts.route("/user/<username>")
def user_posts(username):
    user = User.objects(username=username).first()
    if user:
        user = User.objects(username=username).first()
        posts = Post.objects(commenter=user).order_by('-date')
        count = len(posts)
        return render_template("user_posts.html", title=username+"'s posts", username=username, posts=posts, count=count, user=user)
    else:
        return render_template("user_posts.html", error_msg = "User does not exist.")

@posts.route("/post/<post_id>", methods=["GET", "POST"])
def post_detail(post_id):
    post = Post.objects(post_id=post_id).first()
    if post:
        form = CommentForm()
        img = get_b64_img(post)
        if form.validate_on_submit() and current_user.is_authenticated:
            comment = Comment(
                commenter=current_user._get_current_object(),
                content=form.text.data,
                date=current_time(),
                post_id=post.post_id
            )
            comment.save()
            return redirect(request.path)
        
        comments = Comment.objects(post_id=post_id)
        return render_template("post_detail.html", post=post, form=form, image=img, comments=comments)
    return render_template("404.html")

@posts.route("/about")
def about():
    return render_template("about.html", title="About")

