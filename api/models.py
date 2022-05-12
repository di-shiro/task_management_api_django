from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

import uuid     # 128bitの一意なUniqueIDを作成できる。

def upload_avatar_path(instance, filename):
    # 拡張子の文字列を保持
    ext = filename.split('.')[-1]   # 拡張子なのでリストにの最後
    # avatar画像のファイル名をUserIDとして、media/avatars フォルダに保存する。
    return '/'.join(['avatars', str(instance.user_profile.id)+str('.')+str(ext)])

class Profile(models.Model):
    # このProfileクラスとDjangoのUserモデルを一対一対応で結びつける
    user_profile = models.OneToOneField(
        User,
        related_name='user_profile',
        on_delete=models.CASCADE
    )
    img = models.ImageField(blank=True, null=True, upload_to=upload_avatar_path)

    # このProfileモデルが呼ばれたら、返り値として指定Userのusernameを返す。
    def __str__(self):
        return self.user_profile.username


class Category(models.Model):
    item = models.CharField(max_length=100)

    def __str__(self):
        return self.item


class Task(models.Model):
    STATUS = {
        ('1', 'Not started'),
        ('2', 'On going'),
        ('3', 'Done'),
    }
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    task = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    criteria = models.CharField(max_length=100)
    status = models.CharField(max_length=40, choices=STATUS, default='1')
    # Categoryモデルを参照して要素を使えるようにする。ForeignKeyを使う。
    # CascadeDeleteで、Categoryのデータを削除した際、それに紐づくTaskを芋づる式に削除する。
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # Taskの所要日数は 0日以上なので、最小日数を 0 としている。
    estimate = models.IntegerField(validators=[MinValueValidator(0)])
    # ForeignKeyを使って、DjangoのUserモデルと関連付ける。
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    responsible = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responsible')
    created_at = models.DateTimeField(auto_now_add=True)    # auto_now_add=Trueとすることで、自動的に登録されたときの日時をDBに記録する設定。
    updated_at = models.DateTimeField(auto_now=True)    # auto_now 変更された時の日時

    def __str__(self):
        return self.task








