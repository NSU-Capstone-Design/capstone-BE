from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):
    def _create_user(self, user_id, password, email, level='0', expert_user=False, nickname=None):
        """
            슈퍼유저생성시 필요함다
        """
        if not user_id:
            raise ValueError('The given email must be set')
        print("model create")
        user = self.model(
            user_id=user_id,
            email=email,
            nickname=nickname,
            level=level,
            expert_user=expert_user
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, email, password, nickname=None):
        user = self._create_user(
            user_id=user_id,
            email=email,
            password=password,
            nickname=nickname,
        )
        user.is_superuser = True  # 나중에 지우자
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(verbose_name="아이디", max_length=64, unique=True)
    email = models.EmailField(verbose_name="이메일", max_length=255, unique=True, null=True)
    nickname = models.CharField(verbose_name="닉네임", max_length=50, null=True, blank=True, default='user')
    level = models.CharField(verbose_name="레벨", max_length=20, null=True, default=None)
    expert_user = models.BooleanField(verbose_name="전문가여부", default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['email', 'nickname']

    def __str__(self):
        return self.user_id

    @property
    def is_expert(self):
        """전문가계정인지 확인할때 사용 할 메소드"""
        return self.expert_user

    @property
    def is_staff(self):
        """superuser인지 확인할때 사용 할 메소드"""
        return self.is_admin

    def has_perm(self, perm, obj=None):
        if perm == "admin":
            return self.is_admin
        else:
            return True
