from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from account.models import User


class Question(models.Model):
    user_id = models.ForeignKey(User, verbose_name='작성자', on_delete=models.SET_NULL, null=True, related_name='questions')
    # ToDo: 문제 글 번호 추가 필요
    subject = models.CharField(verbose_name="제목", max_length=200)
    content = models.TextField(verbose_name="내용")
    created_at = models.DateTimeField(verbose_name="작성시간")

    def __str__(self):
        return self.subject


class Answer(models.Model):
    user_id = models.ForeignKey(User, verbose_name='작성자', on_delete=models.SET_NULL, null=True, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField(verbose_name="내용")
    created_at = models.DateTimeField(verbose_name="작성시간")

    def __str__(self):
        return self.content


class Comment(models.Model):
    user_id = models.ForeignKey(User, verbose_name='작성자', on_delete=models.SET_NULL, null=True, related_name='comments')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name="부모 글")
    object_id = models.PositiveIntegerField()
    post_object = GenericForeignKey('content_type', 'object_id')
    reply_to = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE,
                                 related_name='replies', verbose_name="부모 댓글")
    content = models.TextField(verbose_name="내용")
    created_at = models.DateTimeField(verbose_name="작성시간")

    def __str__(self):
        return self.content
