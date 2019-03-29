import click

def register_commands(app):
    @app.cli.command()
    @click.option('--category', default=10, help='Quantity of categories, default is 10')
    @click.option('--post', default=50, help='Quantity of posts, default is 50')
    @click.option('--comment', default=500, help='Quantity of comments, default is 500')
    def forge(category, post, comment):
        '''Generates the fake data
        '''
        from bluebb.fakes import fake_admin, fake_categories, fake_comments, fake_posts

        db.drop_all()
        db.creat_all()

        click.echo('Generating the administrator..')
        fake_admin()

        click.echo('Generating %d categories ..' %category)
        fake_categories()

        click.echo('Generating %d posts ..' %post)
        fake_posts()

        click.echo('Generating %d comments...' %comment)
        fake_comments()

        click.echo('Done.')
