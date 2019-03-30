from threading import Thread
from flask import url_for, current_app
from flask_mail import Message
from bluebb.extensions import mail

def send_email(subject, to, html):
    pass
#! async sending
def _send_async_mail(app, message):
    with app.app_context(): #? http://flask.pocoo.org/docs/1.0/appcontext/
        mail.send(message)

def send_async_mail(subject, to, html):
    app = current_app._get_current_object()
    message = Message(subject, recipients=[to], html=html)
    thr = Thread(target=_send_async_mail, args=[app, message])
    thr.start()
    return thr

def send_new_comment_email(post):
    post_url = url_for('blog.show_post', post_id=post.id, _external=True) + '#comments'
    send_email(subject='New comment', to=current_app.config['BLUEBB_ADMIN_EMAIL'], html='<p>New comment in post <i>%s</i>, click the link below to check:</p>'
    '<p><a href="%s">%s</a></p>'
    '<p><small style="color: #868e96">Do not reply this email.</small></p>' %(post.title, post_url, post_url)
    )

def send_new_reply_email(comment):
    post_url = url_for('blog.show_post', post_id=comment.post.id, _external=True) + '#comments' #? comment.post.id or comment.post_id
    send_email(subject='New reply', to=comment.email, html='<p>New reply for the comment you left in post <i>%s</i>, click the link below to check:</p>' #? to=comment.email or current_app.config['BLUEBB_ADMIN_EMAIL']
    '<p><a href="%s">%s</a></p>'
    '<p><small style="color: #868e96">Do not reply this email.</small></p>' %(post.title, post_url, post_url)
    ) 


