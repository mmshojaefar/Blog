from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
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
        # Create or get groups
        std_user, std_created = Group.objects.get_or_create(name='کاربران عادی')
        writer_user, writer_created = Group.objects.get_or_create(name='نویسندگان')
        editor_user, editor_created = Group.objects.get_or_create(name='ویراستاران')
        admin_user, admin_created = Group.objects.get_or_create(name='مدیران')
        if std_created and writer_created and editor_created and admin_created:
            self.stdout.write(self.style.SUCCESS('Successfully created 4 groups!'))
        else:
            self.stderr.write('Groups created before. Cant to create them again!')
            

        # Create permissions and add them to groups

        # Like/dislike doesn't need permissions! It is enough to check user is logged in or not!

        # Leaving comment does not need premissions (of course logged in user can leave comment) but editting comment
        # need permissions(writer of comment(owner)/edittor/admin can edit a comment). Needless to say everyone can see all
        # comments although logged in or not
        try:
            view_comment = Permission.objects.get(codename='view_comment')
            add_comment = Permission.objects.get(codename='add_comment')
            edit_comment = Permission.objects.get(codename='change_comment')
            delete_comment = Permission.objects.get(codename='delete_comment')
        except:
            self.stdout.write(self.style.ERROR('Probably name of model comment changed! Unable to find some/all permissions of model comment!'))
        else:
            std_user.permissions.add(view_comment)
            writer_user.permissions.add(view_comment)
            editor_user.permissions.add(view_comment)
            admin_user.permissions.add(view_comment)

            std_user.permissions.add(add_comment)
            writer_user.permissions.add(add_comment)
            editor_user.permissions.add(add_comment)
            admin_user.permissions.add(add_comment)

            editor_user.permissions.add(edit_comment)
            admin_user.permissions.add(edit_comment)
            editor_user.permissions.add(delete_comment)
            admin_user.permissions.add(delete_comment)
            self.stdout.write(self.style.SUCCESS('Successfully permissions of model comment added to groups!'))

        # Leaving and editting post need premissions(writer/editor/admin user can leave post and admin/editor can edit 
        # all post and writer user can edit her/his post), so we set all permissions. Needless to say everyone can see
        # all comments although logged in or not
        try:
            view_post = Permission.objects.get(codename='view_post')
            add_post = Permission.objects.get(codename='add_post')
            edit_post = Permission.objects.get(codename='change_post')
            delete_post = Permission.objects.get(codename='delete_post')
        except:
            self.stdout.write(self.style.ERROR('Probably name of model post changed! Unable to find permissions of model post!'))
        else:
            std_user.permissions.add(view_post)
            writer_user.permissions.add(view_post)
            editor_user.permissions.add(view_post)
            admin_user.permissions.add(view_post)

            writer_user.permissions.add(add_post)
            editor_user.permissions.add(add_post)
            admin_user.permissions.add(add_post)

            editor_user.permissions.add(edit_post)
            admin_user.permissions.add(edit_post)
            editor_user.permissions.add(delete_post)
            admin_user.permissions.add(delete_post)
            self.stdout.write(self.style.SUCCESS('Successfully permissions of model post added to groups!'))

        # Only admin user can add/edit/delete category but every writer can select the category for their post and everyone
        # (although logged in or not) can see all post of a category so everyone has permission for viewnig categories!
        try:
            view_category = Permission.objects.get(codename='view_category')
            add_category = Permission.objects.get(codename='add_category')
            edit_categry = Permission.objects.get(codename='change_category')
            delete_category = Permission.objects.get(codename='delete_category')
        except:
            self.stdout.write(self.style.ERROR('Probably name of model category changed! Unable to find permissions of model category!'))
        else:
            std_user.permissions.add(view_category)
            writer_user.permissions.add(view_category)
            editor_user.permissions.add(view_category)
            admin_user.permissions.add(view_category)
            admin_user.permissions.add(add_category)
            admin_user.permissions.add(edit_categry)
            admin_user.permissions.add(delete_category)
            self.stdout.write(self.style.SUCCESS('Successfully permissions of model category added to groups!'))
        
        #only editor/admin user can accept post for public view!
        try:
            accept_post = Permission.objects.get(codename='accept_post')
        except:
            self.stdout.write(self.style.ERROR('Probably name of permission accept_post changed! Unable to find accept_post!'))
        else:
            editor_user.permissions.add(accept_post)
            admin_user.permissions.add(accept_post)
            self.stdout.write(self.style.SUCCESS('Successfully accept_post added to groups!'))

        #only editor/admin user can accept comment for public view!
        try:
            accept_comment = Permission.objects.get(codename='accept_comment')
        except:
            self.stdout.write(self.style.ERROR('Probably name of permission accept_comment changed! Unable to find accept_comment!'))
        else:
            editor_user.permissions.add(accept_comment)
            admin_user.permissions.add(accept_comment)            
            self.stdout.write(self.style.SUCCESS('Successfully accept_comment added to groups!'))     

        try:
            view_tag = Permission.objects.get(codename='view_tag')
            add_tag = Permission.objects.get(codename='add_tag')
            edit_tag = Permission.objects.get(codename='change_tag')
            delete_tag = Permission.objects.get(codename='delete_tag')
        except:
            self.stdout.write(self.style.ERROR('Probably name of model comment changed! Unable to find some/all permissions of model comment!'))
        else:
            std_user.permissions.add(view_tag)
            writer_user.permissions.add(view_tag)
            editor_user.permissions.add(view_tag)
            admin_user.permissions.add(view_tag)

            std_user.permissions.add(add_tag)
            writer_user.permissions.add(add_tag)
            editor_user.permissions.add(add_tag)
            admin_user.permissions.add(add_tag)

            editor_user.permissions.add(edit_tag)
            admin_user.permissions.add(edit_tag)
            editor_user.permissions.add(delete_tag)
            admin_user.permissions.add(delete_tag)
            self.stdout.write(self.style.SUCCESS('Successfully permissions of model tag added to groups!'))  
