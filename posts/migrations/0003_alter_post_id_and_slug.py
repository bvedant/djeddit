from django.db import migrations, models
import uuid
from django.utils.text import slugify

def generate_uuid_and_slug(apps, schema_editor):
    Post = apps.get_model('posts', 'Post')
    for post in Post.objects.all():
        # Generate new UUID
        post.id = uuid.uuid4()
        # Create slug from title
        base_slug = slugify(post.title)
        truncated_slug = base_slug[:91].rstrip('-')
        uuid_slice = str(post.id)[:8]
        post.slug = f"{truncated_slug}-{uuid_slice}"
        post.save()

class Migration(migrations.Migration):
    dependencies = [
        ('posts', '0002_comment_edited_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False),
        ),
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=100, unique=True, blank=True, null=True),
        ),
        migrations.RunPython(generate_uuid_and_slug, reverse_code=migrations.RunPython.noop),
        # After data migration, make slug required
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
    ] 