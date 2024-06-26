import auto_prefetch
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models import (CASCADE, SET_NULL, BooleanField, CharField,
                              DecimalField, SlugField)
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager

from acctmarket.utils.models import (ImageTitleTimeBaseModels,
                                     TitleTimeBasedModel)

# Create your models here.


class BlogCategory(ImageTitleTimeBaseModels):
    slug = SlugField(default="", blank=True)
    sub_category = auto_prefetch.ForeignKey(
        "self",
        on_delete=CASCADE,
        blank=True,
        null=True,
        related_name="subcategories",
    )

    class Meta:
        verbose_name_plural = "Blog Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Post(ImageTitleTimeBaseModels):
    user = auto_prefetch.ForeignKey(
        "users.User",
        verbose_name=_("User Post"),
        on_delete=SET_NULL,
        null=True,
    )
    slug = SlugField(default="", blank=True)
    category = auto_prefetch.ForeignKey(
        BlogCategory,
        verbose_name=_("Blog Category"),
        on_delete=SET_NULL,
        null=True,
    )

    tags = TaggableManager(blank=True, help_text="A comma-separated list of tags.")
    content = RichTextUploadingField("Description", default="", null=True)

    class Meta:
        verbose_name_plural = "Posts"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return self.slug

    def __str__(self):
        return self.title


class Banner(ImageTitleTimeBaseModels):
    category = auto_prefetch.ForeignKey(
        "ecommerce.Category",
        verbose_name="Banner category",
        on_delete=SET_NULL,
        null=True,
    )
    slug = SlugField(default="", blank=True)
    sub_title = CharField(max_length=50, default="", blank=True)
    price = DecimalField(max_digits=100, decimal_places=2)
    oldprice = DecimalField(max_digits=100, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Announcement(TitleTimeBasedModel):
    content = RichTextUploadingField("Description", default="", null=True)
    active = BooleanField(default=True)

    class Meta:
        verbose_name = "Announcement"
        verbose_name_plural = "Announcements"

    def __str__(self):
        return self.title
