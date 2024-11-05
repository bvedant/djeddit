from django.db import migrations, models
from django.utils.text import slugify

def shorten_existing_slugs(apps, schema_editor):
    Post = apps.get_model('posts', 'Post')
    for post in Post.objects.all():
        # Get the UUID suffix from existing slug
        uuid_suffix = post.slug[-8:]
        
        # Create new shorter slug from title
        base_slug = slugify(post.title)
        truncated_slug = base_slug[:40].rstrip('-')
        
        # Combine with existing UUID suffix
        post.slug = f"{truncated_slug}-{uuid_suffix}"
        post.save()

class Migration(migrations.Migration):
    dependencies = [
        ('posts', '0003_alter_post_id_and_slug'),
    ]

    operations = [
        # First make the field nullable temporarily
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=50, unique=True, null=True),
        ),
        # Run the data migration
        migrations.RunPython(shorten_existing_slugs, reverse_code=migrations.RunPython.noop),
        # Make the field required again
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=50, unique=True),
        ),
    ] 