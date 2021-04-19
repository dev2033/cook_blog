from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    """Категория. Может иметь дочернии категории"""
    name = models.CharField('Название категории', max_length=100)
    slug = models.SlugField('URL', max_length=100,
                            help_text='Заполняется автоматически')
    parent = TreeForeignKey(
        'self',
        related_name="children",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']


class Tag(models.Model):
    """Тег"""
    name = models.CharField('Название тега', max_length=100)
    slug = models.SlugField('URL', max_length=100,
                            help_text='Заполняется автоматически')

    def __str__(self):
        return self.name


class Post(models.Model):
    """Пост"""
    author = models.ForeignKey(
        User, related_name="posts",
        on_delete=models.CASCADE,
        verbose_name='Имя автора'
    )
    title = models.CharField('Название поста', max_length=200)
    slug = models.SlugField('URL', max_length=200)
    image = models.ImageField('Изображение', upload_to='articles/')
    text = models.TextField('Текст')
    category = models.ForeignKey(
        Category,
        related_name="post",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    tags = models.ManyToManyField(Tag, related_name="post", verbose_name='Теги')
    create_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_single",
                       kwargs={"slug": self.category.slug,
                               "post_slug": self.slug})

    def get_recipes(self):
        return self.recipes.all()


class Recipe(models.Model):
    """Рецепт"""
    name = models.CharField('Название рецепта', max_length=100)
    serves = models.CharField('Кол-во персон', max_length=50)
    prep_time = models.PositiveIntegerField('Время подготовки', default=0)
    cook_time = models.PositiveIntegerField('Время готовки', default=0)
    ingredients = models.TextField('Индигриенты')
    directions = models.TextField('Указания к приготовлению')
    post = models.ForeignKey(
        Post,
        related_name="recipes",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Пост'
    )


class Comment(models.Model):
    """Комментарий"""
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    website = models.CharField(max_length=150)
    message = models.TextField(max_length=500)
    post = models.ForeignKey(Post, related_name="comment",
                             on_delete=models.CASCADE)
