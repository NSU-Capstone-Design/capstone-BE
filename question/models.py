from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from account.models import User
from problemInfo.models import ProblemInfo


class Question(models.Model):
    user_id = models.ForeignKey(User, verbose_name='작성자', on_delete=models.SET_NULL,
                                null=True, related_name='questions')
    prob_num = models.ForeignKey(ProblemInfo, verbose_name="문제고유번호", on_delete=models.SET_NULL, null=True)
    subject = models.CharField(verbose_name="제목", max_length=200)
    content = models.TextField(verbose_name="내용")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성시간")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정시간")
    post_hit = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.subject

    @property
    def update_counter(self):
        self.post_hit += 1
        self.save()


class Answer(models.Model):
    user_id = models.ForeignKey(User, verbose_name='작성자', on_delete=models.SET_NULL, null=True, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField(verbose_name="내용")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성시간")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정시간")

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.content


class Comment(models.Model):
    user_id = models.ForeignKey(User, verbose_name='작성자', on_delete=models.SET_NULL, null=True, related_name='comments')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name="부모 글")
    object_id = models.PositiveIntegerField()
    post_object = GenericForeignKey('content_type', 'object_id')
    reply_to = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL,
                                 related_name='replies', verbose_name="부모 댓글")
    content = models.TextField(verbose_name="내용")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성시간")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정시간")

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.content
