from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('bookshelf', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookshelf.customuser')),
            ],
            options={
                'permissions': [
                    ('can_view', 'Can view article'),
                    ('can_create', 'Can create article'),
                    ('can_edit', 'Can edit article'),
                    ('can_delete', 'Can delete article'),
                ],
            },
        ),
    ]