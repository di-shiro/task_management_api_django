from rest_framework import serializers
from .models import Task, Category, Profile
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password'] # Userモデルの中から取り扱いたい属性
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    # DBにPasswordを保存する際、ハッシュ化して保存する必要があるため、createメソッドをOverRideする。
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)   # このcreate_user関数でハッシュ化したPasswordをuserに渡す。
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user_profile', 'img']
        extra_kwargs = {'user_profile': {'read_only': True}}
        # ProfileはDjangoが自動で作成するように設定したので(models.pyに)、read_onlyに設定している。




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'item']


class TaskSerializer(serializers.ModelSerializer):
    # ここに記載しているのは全て read_only なので、React側からGETメソッドでアクセスした時にかえしてくれる処理。
    ''' models.py の中で、ForeignKeyで参照しているモデル(Table)は、通常そのPrimaryKeyしか読み取れない。
    例えば、Taskモデルの中にcategory要素として、ForeignKeyでCategoryモデルを参照しているが、
    このCategoryモデルのitem要素を参照する場合は次のようにする。
    '''
    category_item = serializers.ReadOnlyField(source='category.item', read_only=True)
    owner_username = serializers.ReadOnlyField(source='owner.username', read_only=True)
    responsible_username = serializers.ReadOnlyField(source='responsible.username', read_only=True)
    status_name = serializers.CharField(source='get_status_display', read_only=True)
    ''' get_status_display は、models.pyに定義した下の、dict構造を示している。
    例えば、statusは「STATUS」のことで、displayはvalue部分の「Not started」のことを示している。
    # STATUS = {
    #     ('1', 'Not started'),
    #     ('2', 'On going'),
    #     ('3', 'Done'),
    # }
    '''
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    # 日時のデータ形式をシリアル形式から人が理解しやすいYMD形式にフォーマットを変えている。

    class Meta:
        model = Task
        fields = ['id', 'task', 'description', 'criteria', 'status', 'status_name', 'category', 'category_item',
                  'estimate', 'responsible', 'responsible_username', 'owner', 'owner_username', 'created_at', 'updated_at']
        extra_kwargs = {'owner': {'read_only': True}}
        ''' 上記の owner は、React側でTaskを作成する際のUserのことであり、それはログインUserのこと。
        そのため owner には、Djangoの内部でログインUserを自動で認識して、
        ログインUser割り当ててからTaskを作成するため、read_onlyに設定している。
        '''

