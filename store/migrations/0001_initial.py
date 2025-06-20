# Generated by Django 5.2.1 on 2025-05-16 23:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(upload_to='categories/images')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('code', models.CharField(help_text='Hex code like #FF0000', max_length=9)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products/images')),
            ],
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('unit', models.CharField(blank=True, max_length=50, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='features', to='store.category')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(max_length=1500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='store.category')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ProductFeatureValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_value', models.CharField(max_length=255)),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_values', to='store.feature')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feature_values', to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('sale_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('status', models.CharField(choices=[('AV', 'Available'), ('DF', 'Draft')], default='AV', max_length=2)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('sku', models.CharField(max_length=100, unique=True)),
                ('barcode', models.CharField(blank=True, max_length=100, null=True)),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variations', to='store.color')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variations', to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='VariationImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_variations', to='store.image')),
                ('variation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variation_images', to='store.variation')),
            ],
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['id', 'slug'], name='store_produ_id_2abda1_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['name'], name='store_produ_name_5e57da_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['-created_at'], name='store_produ_created_0fbdf8_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='productfeaturevalue',
            unique_together={('product', 'feature')},
        ),
    ]
