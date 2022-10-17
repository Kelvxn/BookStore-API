# Generated by Django 4.0 on 2022-10-17 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0024_author_subscribers_alter_publisher_subscribers'),
        ('accounts', '0004_alter_myuser_bookmark_alter_myuser_groups_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='bookmark',
            field=models.ManyToManyField(null=True, related_name='bookmark', to='books.Book'),
        ),
    ]