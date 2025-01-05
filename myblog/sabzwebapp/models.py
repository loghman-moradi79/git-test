from django.db import models
from django.contrib.auth.models import User
from django.forms import ImageField, ChoiceField
from django.template.context_processors import request
from django.template.defaultfilters import default, title
from django.utils import timezone
from django.urls import reverse
from django_jalali.db import models as jmodels
from django.template.defaultfilters import slugify
from django_resized import ResizedImageField

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"
        REJECTED = "RJ", "Rejected"

    CATEGORY_CHOICE = (
        ("تکنولوژی", "تکنولوژی"),
        ("هوش مصنوعی", "هوش مصنوعی"),
        ("برنامه نویسی", "برنامه نویسی"),
        ("سایر", "سایر")
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts", verbose_name="نویسنده")
    title = models.CharField(max_length=250, verbose_name="عنوان")
    description = models.TextField(max_length=500, verbose_name="توضیحات")
    slug = models.CharField(max_length=50, verbose_name="اسلاگ")
    publish = jmodels.jDateTimeField(default=timezone.now, verbose_name="تاریخ انتشار")
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT, verbose_name="وضعیت")
    reading_time = models.PositiveBigIntegerField(verbose_name="زمان مطالعه")
    category = models.CharField(choices=CATEGORY_CHOICE, default="سایر", verbose_name="دسته بندی",
                                blank=True, null=True)

    objects = jmodels.jManager()
    published = PublishedManager()



    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]

        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('sabzwebapp:post_detail', args=[self.id])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Ticket(models.Model):
    message = models.TextField(max_length=250, verbose_name="متن")
    name = models.CharField(max_length=50, verbose_name="نام")
    email = models.EmailField(max_length=50, verbose_name="ایمیل")
    phone = models.CharField(max_length=11, verbose_name="تلفن")
    subject = models.CharField(max_length=250, verbose_name="موضوع")

    class Meta:
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت ها'

    def __str__(self):
        return self.subject


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", verbose_name="پست")
    name = models.CharField(max_length=50, verbose_name="نام")
    body = models.TextField(max_length=250, verbose_name="متن")
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated = jmodels.jDateTimeField(auto_now=True, verbose_name="بروزرسانی")
    status = models.BooleanField(default=False, verbose_name="وضعیت")

    class Meta:
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'

    def __str__(self):
        return f"{self.name}: {self.body}"


def upload_to(instance, file_name):
    username = instance.post.author.username
    return f"image/{username}/{file_name}"


class Image(models.Model):
    post = models.ForeignKey(Post, models.CASCADE, related_name="images", verbose_name="پست")
    file_image = ResizedImageField(upload_to=upload_to, size=[200, 200], quality=75, crop=['middle', 'center'])
    title = models.CharField(max_length=250, verbose_name="عنوان", null=True, blank=True)
    description = models.TextField(max_length=250, verbose_name="توضیحات", null=True, blank=True)
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]

        verbose_name = "تصویر"
        verbose_name_plural = "تصویر ها"

    def __str__(self):
        return self.title if self.title else self.file_image.name

    def get_absolute_url(self):
        return reverse('sabzwebapp:post_detail', args=[self.post.id])


class Account(models.Model):
    user = models.OneToOneField(User, models.CASCADE, related_name="account", verbose_name="اکانت")
    date_of_birth = jmodels.jDateField(verbose_name="تاریخ تولد", blank=True, null=True)
    bio = models.TextField(verbose_name="توضیحات", blank=True, null=True)
    job = models.CharField(max_length=50, verbose_name="شغل", blank=True, null=True)
    photo = ResizedImageField(upload_to="account/image", verbose_name="تصویر", null=True, blank=True,
                              size=[100, 100], quality=75, crop=['middle', 'center'])

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'اکانت'
        verbose_name_plural = 'اکانت ها'





















