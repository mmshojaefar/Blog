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

        # Like/dislike doesn't need permissions! It is enough to check user is logged in or not!

        # Leaving comment does not need premissions (of course logged in user can leave comment) but editting comment
        # need permissions(writer of comment/edittor/admin can edit a comment). Needless to say everyone can see all
        # comments although logged in or not 
        add_comment = Permission.objects.filter(codename='add_comment')
        edit_comment = Permission.objects.filter(name='change_comment')
        delete_comment = Permission.objects.filter(name='delete_comment')
        view_comment = Permission.objects.filter(name='view_comment')

        # Leaving and editting post need premissions(writer/editor/admin user can leave post and admin/editor can edit 
        # all post and writer user can edit her/his post), so we set all permissions. Needless to say everyone can see
        # all comments although logged in or not
        add_post = Permission.objects.filter(name='add_post')
        edit_post = Permission.objects.filter(name='change_post')
        delete_post = Permission.objects.filter(name='delete_post')
        view_post = Permission.objects.filter(name='view_post')

        # Only admin user can add/edit/delete category but every writer can select the category for their post and everyone
        # (although logged in or not) can see all post of a category so everyone has permission for viewnig categories!  
        add_category = Permission.objects.filter(name='add_category')
        edit_categry = Permission.objects.filter(name='change_category')
        delete_category = Permission.objects.filter(name='delete_category')
        view_category = Permission.objects.filter(name='view_category')
        
        #only editor/admin user can accept post for public view!
        accept_post = Permission.objects.filter(name='accept_post')

        #only editor/admin user can accept comment for public view!
        accept_post = Permission.objects.filter(name='accept_comment')
        self.stdout.write(self.style.SUCCESS('Successfully created 4 groups!'))
