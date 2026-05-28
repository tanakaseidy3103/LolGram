from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_remove_comment_champion_alter_comment_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='face_image',
            field=models.ImageField(blank=True, null=True, upload_to='face_recognition'),
        ),
        migrations.AddField(
            model_name='profile',
            name='face_recognition_enabled',
            field=models.BooleanField(default=False),
        ),
    ]