from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Generate the slug from the name field
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


# Ensure that the "Others" category exists
@receiver(post_save, sender=Category)
def ensure_default_category_exists(sender, **kwargs):
    Category.objects.get_or_create(name="Others")


def get_default_category():
    return Category.objects.get_or_create(name="Others")[0]


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(_("Description"), blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET(get_default_category),
        related_name="product_list",
        null=True,
        blank=True,
    )
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    stock = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Generate the slug from the name field
        if not self.slug:
            original_slug = slugify(self.name)
            queryset = Product.objects.all().exclude(pk=self.pk)
            counter = 1
            slug = original_slug
            while queryset.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)
