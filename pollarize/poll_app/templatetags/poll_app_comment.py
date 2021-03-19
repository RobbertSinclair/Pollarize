from django import template
from poll_app.models import Comment, Poll

register = template.Library()

@register.inclusion_tag("poll_app/comment.html")
def get_comments(poll_slug):
    the_poll = Poll.objects.get(poll_slug=poll_slug)
    comments = Comment.objects.filter(poll=the_poll, parent=None)
    return {"poll": the_poll,
    "comment": comments}