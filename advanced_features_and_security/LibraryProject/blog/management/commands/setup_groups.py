from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from blog.models import Post

class Command(BaseCommand):
    help = 'Set up permission groups'

    def handle(self, *args, **options):
        # Create groups
        viewer_group, created = Group.objects.get_or_create(name='Viewers')
        editor_group, created = Group.objects.get_or_create(name='Editors')
        admin_group, created = Group.objects.get_or_create(name='Admins')
        
        # Get content type for the Post model
        content_type = ContentType.objects.get_for_model(Post)
        
        # Get permissions
        view_permission = Permission.objects.get(
            codename='can_view',
            content_type=content_type,
        )
        create_permission = Permission.objects.get(
            codename='can_create',
            content_type=content_type,
        )
        edit_permission = Permission.objects.get(
            codename='can_edit',
            content_type=content_type,
        )
        delete_permission = Permission.objects.get(
            codename='can_delete',
            content_type=content_type,
        )
        
        # Assign permissions to groups
        viewer_group.permissions.add(view_permission)
        
        editor_group.permissions.add(view_permission)
        editor_group.permissions.add(create_permission)
        editor_group.permissions.add(edit_permission)
        
        admin_group.permissions.add(view_permission)
        admin_group.permissions.add(create_permission)
        admin_group.permissions.add(edit_permission)
        admin_group.permissions.add(delete_permission)
        
        self.stdout.write(self.style.SUCCESS('Successfully set up permission groups'))