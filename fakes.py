from bluebb.models import Admin, Category, Post, Comment
from bluebb.extensions import db
from faker import Faker

faker = Faker()

def fake_admin():
    admin = Admin(
        username = 'admin',
        blog_title ='Bluelog',
        blog_sub_title ="No, I'm the real thing",
        name = 'Mima Kirigoe',
        about = 'Um, I, Mima Kirigoe, had a fun time',
    )
    admin.set_password('helloflask')
    db.session.add(admin)
    db.session.commit()

def fake_categories(count=10):
    category = Category(name='Default')
    db.session.add(category)
    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

# TODO
deg fake_posts(count=50):
    post = Post(title='Default')
    db.session.add(post)
    for i in range(count):
        pass

def fake_comments(count=500):
    for i in range(count):
        comment1 = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),           
            body=fake.sentence(),            timestamp=fake.date_time_this_year(),            
            reviewed=True,             
            post=Post.query.get(random.randint(1, Post.query.count()))
            )         
        db.session.add(comment1)
                 
    salt = int(count * 0.1)     
    for i in range(salt):         # 未审核评论
        comment2 = Comment(             
            author=fake.name(),             
            email=fake.email(),             
            site=fake.url(),             
            body=fake.sentence(),   
            timestamp=fake.date_time_this_year(),   
            reviewed=False,             
            post=Post.query.get(random.randint(1, Post.query.count()))
            )
        db.session.add(comment2)
    #  管理员评论
    comment3 = Comment(
                author='Mima Kirigoe',             
                email='mima@example.com',             
                site='example.com',             
                body=fake.sentence(),             
                timestamp=fake.date_time_this_year(),             
                from_admin=True,             
                reviewed=True,             
                post=Post.query.get(random.randint(1, Post.query.count()))
    )
    db.session.add(comment3)
    # 回复
    for i in range(salt):
        comment4 = Comment(
            author=fake.name(),             
            email=fake.email(),             
            site=fake.url(),             
            body=fake.sentence(),             
            timestamp=fake.date_time_this_year(),             
            reviewed=True,             
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment4)
    
    db.session.commit()
    



