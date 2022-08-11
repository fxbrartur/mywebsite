from django.views import generic
from django.shortcuts import get_object_or_404, render

from blog.models import Post
from blog.forms import CommentForm


class PostView(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'


# class PostDetail(generic.DetailView):
#    model = Post
#    template_name = 'post_detail.html'


def post_detail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True).order_by('-created_on')
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Created the comment object, but it's not saved to DB yet.
            new_comment = comment_form.save(commit=False)
            # Assigning the current post to the comment
            new_comment.post = post
            # Saving the attributed comment to the DB.
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(
        request,
        template_name,
        {
            "post": post,
            "comments": comments,
            "new_comment": new_comment,
            "comment_form": comment_form,
        },
    )
