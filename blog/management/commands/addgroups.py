from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from django.db.utils import IntegrityError
# from blog.models import *


class Command(BaseCommand):
    '''
        This command must run before running the project.
        In this command 4 groups of user will be created:
            Standard User, Writer User, Editor User, Admin User.
        Standard User: This user can leave comments, like and dislike posts and comments.
        Writer User: In addition to the above permissions, This user can ddd post and edit and archive her/his posts.
            (deactive showing post for others)
            Note: If someone archive her/his posts, NO ONE cant see the post until the post writer/editor/admin active
                  the showing post for others.
        Editor User: In addition to the above permissions, this user can accept other posts and comments. This user 
            also can edit or active or deactive each post to show.
        Admin User: In addition to the above permissions, this user can set categories and manage users and their groups.
    '''
    help = "Create 4 groups of users!"
    def handle(self, *args, **options):
        # Create groups
        try:
            std_user = Group.objects.create(name='کاربران عادی')
            writer_user = Group.objects.create(name='نویسندگان')
            editor_user = Group.objects.create(name='ویراستاران')
            admin_user = Group.objects.create(name='مدیران')
        except IntegrityError:
            self.stderr.write(self.style.ERROR('Groups created before. Cant to create them again!'))
            return

        # Create permissions and add them to groups
        # add_comment = Permission.objects.filter(codename='add_comment')
        # print(add_comment)
        # edit_comment = Permission.objects.get(name='blog.change_comment')
        # delete_comment = Permission.objects.get(name='blog.delete_comment')
        # view_comment = Permission.objects.get(name='blog.view_comment')

        # add_post = Permission.objects.get(name='blog.add_post')
        # edit_post = Permission.objects.get(name='blog.change_post')
        # delete_post = Permission.objects.get(name='blog.delete_post')
        # view_post = Permission.objects.get(name='blog.view_post')

        # add_category = Permission.objects.get(name='blog.add_post')
        # edit_categry = Permission.objects.get(name='blog.change_post')
        # delete_category = Permission.objects.get(name='blog.delete_post')
        # view_category = Permission.objects.get(name='blog.view_post')
        
        # rate_comment = Permission.objects.get(name='blog.add_post')
        # rate_post = Permission.objects.get(name='blog.add_post')
        self.stdout.write(self.style.SUCCESS('Successfully created 4 groups!'))