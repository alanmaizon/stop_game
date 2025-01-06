# Unit 10 Walk through
## Pagination

In this walkthrough, we will implement pagination for our blog posts, allowing users to navigate through multiple pages of posts. We'll also add a new feature to view all posts created by a particular user.

1.  Enable Pagination on the home page.

Open `blog/views.py`.
-   In the `PostListView` class, add `paginate_by = 5`. This tells Django to fetch only 5 posts each time the user makes a request, fetching the first page by default, and other pages if a `page=` parameter was provided. Setting this attribute also makes the ListView class inject the additional pagination variables `is_paginated` and `page_obj` into the template, which we'll use for our buttons.

```python
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5 # New line here
```

2.  Add cross-page navigation links.

We'll add navigation links in our `blog/templates/blog/home.html` to traverse the pages.

- Inside the `{% block content %}` block, add the pagination code below the `{% for post in posts %}` loop:
```html
{% if is_paginated %}
<div class='post-pagination'>
    {% if page_obj.has_previous %}
    <a class='btn btn-outline-info mb-4' href='?page=1'>First</a>
    <a class='btn btn-outline-info mb-4' href='?page={{ page_obj.previous_page_number }}'>Previous</a>
    {% endif %}

    {% for num in page_obj.paginator.page_range %}
    {% if page_obj.number == num %}
        <a class='btn btn-info mb-4' href='?page={{ num }}'>{{ num }}</a>
    {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
        <a class='btn btn-outline-info mb-4' href='?page={{ num }}'>{{ num }}</a>
    {% endif %}
    {% endfor %}

    {% if page_obj.has_next %}
    <a class='btn btn-outline-info mb-4' href='?page={{ page_obj.next_page_number }}'>Next</a>
    <a class='btn btn-outline-info mb-4' href='?page={{ page_obj.paginator.num_pages }}'>Last</a>
    {% endif %}
</div>
{% endif %}
```

- Note that the `add` template filter helps us do basic arithmetic and is used by our pagination code to dynamically set the previous/next pages.

The full `home.html` template should now be:
```html
{% extends "blog/base.html" %}
{% block content %}
    {% for post in posts %}
        <article class="media content-section">
            <img class="rounded-circle article-img" src="{{ post.author.profile.image.url }}">
            <div class="media-body">
            <div class="article-metadata">
                <a class="mr-2" href="#">
                {{ post.author }}
                </a>
                <small class="text-muted">{{ post.date_posted|date:'dS, F, Y' }}</small>
            </div>
            <h2><a class="article-title" href="{% url 'post-detail' post.id %}">{{ post.title }}</a></h2>
            <p class="article-content">{{ post.content }}</p>
            </div>
        </article>
    {% endfor %}

    {% if is_paginated %}
    <div class='post-pagination'>
    {% if page_obj.has_previous %}
        <a class='btn btn-outline-info mb-4' href='?page=1'>First</a>
        <a class='btn btn-outline-info mb-4' href='?page={{ page_obj.previous_page_number }}'>Previous</a>
    {% endif %}

    {% for num in page_obj.paginator.page_range %}
        {% if page_obj.number == num %}
        <a class='btn btn-info mb-4' href='?page={{ num }}'>{{ num }}</a>
        {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
        <a class='btn btn-outline-info mb-4' href='?page={{ num }}'>{{ num }}</a>
        {% endif %}
    {% endfor %}

    {% if page_obj.has_next %}
        <a class='btn btn-outline-info mb-4' href='?page={{ page_obj.next_page_number }}'>Next</a>
        <a class='btn btn-outline-info mb-4' href='?page={{ page_obj.paginator.num_pages }}'>Last</a>
    {% endif %}
    </div>
    {% endif %}
{% endblock content %}
```

Here's what's happening with the pagination code:
-  `{% if is_paginated %}`: This checks if pagination is enabled for the current view.
-  `{% if page_obj.has_previous %}`: This checks if there is a previous page. If there is, it displays "First" and "Previous" links.
-  `{% for num in page_obj.paginator.page_range %}`: This loops through the available page numbers, displaying a link for each, with the current page highlighted, and links surrounding the current page also shown.
-  `{% if page_obj.has_next %}`: This checks if there is a next page. If there is, it displays "Next" and "Last" links.
-  We also use some custom Bootstrap classes to layout the pagination links.

Note that this pagination markup is intentionally quite comprehensive for the sake of this example, while in many typical projects, you can do with much simpler navigation.

3.  Test home page pagination.

Run the development server, create some more posts, and navigate to your homepage at http://127.0.0.1:8000/. You should now see only 5 posts per page, with pagination links at the bottom.

### User-Specific Posts

4.  Update the Post model to add related_name.

Update `blog/models.py` to add `related_name='posts'` to the `author` field in the `Post` model:

```python
class Post(models.Model):
    ...
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    ...
```

This change will make it easy to access a user's posts directly from an instance of the User model by using `.posts`, which will make our query in the view simpler.

5.  Create `UserPostListView`.

We'll create a new view, for a page where we can see posts of an individual user.

- Open `blog/views.py` and add a new class `UserPostListView` as follows:

```python
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post

User = get_user_model()

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return user.posts.order_by('-date_posted')
```

-   `template_name` specifies the template file to render which we will make next.
-   `context_object_name = 'posts'` specifies the name to use in the template for the data we'll retrieve.
-  `paginate_by` means that we will also paginate our user posts.
-   `get_queryset`: This method retrieves the posts for a specific user. We are using `get_object_or_404` which will fetch the user object. The `kwargs` is a dictionary that holds the named parameters from your URLs, here we are getting the 'username'. We then use this user to filter the Post objects. The `order_by` orders them by date with the most recent at the top.

Note that in this case we have to override the `get_queryset`, rather than just the `queryset` attribute, since our queryset depends on the username, which is only available after the request is made - so we need a function to generate the queryset dynamically.

6.  Create the new page's template.

Under `blog/templates/blog`, create a new file called `user_posts.html` and add the following code:
```html
{% extends "blog/base.html" %}
{% block content %}
    <h1 class='mb-3'>
    Posts by {{ view.kwargs.username }} ({{ page_obj.paginator.count }})
    </h1>
    {% for post in posts %}
    <article class="media content-section">
        <img
        class='rounded-circle article-img'
        src='{{ post.author.profile.image.url }}'
        alt='User profile image'>
        <div class="media-body">
        <div class="article-metadata">
            <a class="mr-2" href="{% url 'user-posts' post.author.username %}">
            {{ post.author }}
            </a>
            <small class="text-muted">{{ post.date_posted|date:'F d, Y' }}</small>
        </div>
        <h2>
            <a class="article-title" href="{% url 'post-detail' post.id %}">
            {{ post.title }}
            </a>
        </h2>
        <p class="article-content">{{ post.content }}</p>
        </div>
    </article>
    {% endfor %}
    {% if is_paginated %}

    <div class='post-pagination'>
        {% if page_obj.has_previous %}
        <a class='btn btn-outline-info mb-4' href='?page=1'>First</a>
        <a class='btn btn-outline-info mb-4' href='?page={{ page_obj.previous_page_number }}'>Previous</a>
        {% endif %}

        {% for num in page_obj.paginator.page_range %}
        {% if page_obj.number == num %}
            <a class='btn btn-info mb-4' href='?page={{ num }}'>{{ num }}</a>
        {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
            <a class='btn btn-outline-info mb-4' href='?page={{ num }}'>{{ num }}</a>
        {% endif %}
        {% endfor %}

        {% if page_obj.has_next %}
        <a class='btn btn-outline-info mb-4' href='?page={{ page_obj.next_page_number }}'>Next</a>
        <a class='btn btn-outline-info mb-4' href='?page={{ page_obj.paginator.num_pages }}'>Last</a>
        {% endif %}
    </div>

    {% endif %}
{% endblock content %}
```

- This template is very similar to `home.html`, with the most important changes being that it's accessing `view.kwargs.username` and that it's using the same pagination as before.
- Note that the pagination code is shared here to keep the code DRY. We could further DRY the code by making a separate template specifically for the pagination.

7.  Add the new url pattern.

Update `blog/urls.py` to add a URL pattern to map the new view, and also update the import statements:

```python
from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView, # Added to imports
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'), # New path
    path('about/',views.about, name='blog-about'),
]
```

Here we have added the new URL:
-   `path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),`
    -   `user/<str:username>` this is a dynamic path that will take the user to a specific author page. The `<str:username>` argument is used to dynamically fetch the username from the url string.
    -  `UserPostListView.as_view()` is the view we created earlier.
    - `name='user-posts'` is the name we can use in other templates to link here


8. Add a link so that we can navigate to a given user's posts from the home page.

- In `blog/templates/blog/home.html` find the following line:
    ```html
        <a class="mr-2" href="#">{{ post.author }}</a>
    ```
- Update the line to the following:
    ```html
        <a class="mr-2" href="{% url 'user-posts' post.author.username %}">
        {{ post.author }}
        </a>
    ```
    This will now bring the user to the author page for that post.

9.  Test User-Specific Posts

Run the development server and navigate to a user's post page e.g http://127.0.0.1:8000/user/stevek. Replace 'stevek' with the username of one of your users. You should see the posts for that user, with pagination, similar to the home page.

10. Extra UX improvement - Distinguish between the Create and Update pages.

As shown last time, by default, the CreateView and UpdateView share the same template (in our case post_form.html). This is typically the way to go, but sometimes we want to make small changes. In particular, it is often a good idea to change the name of the submit button, to clarify the operation being performed.

An easy way to do so is by checking whether the form object is bound or not, which we can do via `if form.instance.pk` - if there is an instance with a primary key, that means we're in UpdateView, and if it's missing, that means we're in CreateView.

Open `blog/templates/blog/post_form.html` and change the submit button to distinguish between create and update by adding the following condition to the submit button:

```html
    <button class="btn btn-outline-info" type="submit">
        {% if form.instance.pk %}
            Update Post
            {% else %}
            Create Post
            {% endif %}
    </button>
```

This change will display different text on the button depending on if we are updating or creating the Post. Feel free to make additional changes to further distinguish the pages, or if you need them to be entirely different templates, you can always use separate `template_name` attributes on each of the classes.

<hr>
We're done. With these changes, the blog now supports pagination, making it more user-friendly as we grow the number of posts.
