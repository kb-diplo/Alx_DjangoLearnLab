# bookshelf/migrations/0003_create_groups_and_permissions.py
from django.db import migrations
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

def create_groups_and_permissions(apps, schema_editor):
    # Get the article model
    Article = apps.get_model('bookshelf', 'Article')
    content_type = ContentType.objects.get_for_model(Article)
    
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
    
    # Create groups
    viewers_group, created = Group.objects.get_or_create(name='Viewers')
    editors_group, created = Group.objects.get_or_create(name='Editors')
    admins_group, created = Group.objects.get_or_create(name='Admins')
    
    # Assign permissions to groups
    viewers_group.permissions.add(view_permission)
    
    editors_group.permissions.add(view_permission)
    editors_group.permissions.add(create_permission)
    editors_group.permissions.add(edit_permission)
    
    admins_group.permissions.add(view_permission)
    admins_group.permissions.add(create_permission)
    admins_group.permissions.add(edit_permission)
    admins_group.permissions.add(delete_permission)

def reverse_func(apps, schema_editor):
    # Delete groups
    Group.objects.filter(name__in=['Viewers', 'Editors', 'Admins']).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('bookshelf', '0002_article'),
    ]

    operations = [
        migrations.RunPython(create_groups_and_permissions, reverse_func),
    ]