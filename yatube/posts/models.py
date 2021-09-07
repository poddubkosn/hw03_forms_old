from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name='имя группы',
                             help_text='Поле для ввода группы')
    slug = models.SlugField(max_length=200, unique=True, db_index=True,
                            verbose_name='slug',
                            help_text='Поле для ввода slug')
    description = models.TextField(verbose_name='Описание группы',
                                   help_text='Поле для ввода описания группы')

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of the model.
        """
        return reverse('posts:group_list', args=[str(self.slug)])

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    text = models.TextField(verbose_name='Пост',
                            help_text='Поле для ввода поста')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации',
                                    help_text='Дата публикации')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts', verbose_name='Автор публикации',
        help_text='автор публикации'
    )
    group = models.ForeignKey(Group, on_delete=models.SET_NULL,
                              related_name='posts', blank=True, null=True,
                              verbose_name='Группа постов',
                              help_text='Поле для ввода группы постов')

    class Meta:
        ordering = ('-pub_date',)
        permissions = (("can_read_this", "permission for post"),)

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of the model.
        """
        return reverse('posts:post_detail', args=[str(self.id)])

    def __str__(self) -> str:
        return self.text[:15]
