from django.shortcuts import render
from rest_framework import status, permissions, generics, viewsets
from .serializers import UserSerializer, CategorySerializer, TaskSerializer, ProfileSerializer
from rest_framework.response import Response
from .models import Task, Category, Profile
from django.contrib.auth.models import User
from . import custompermissions


'''
ModelViewSetは、CRUDの全機能をまるごと提供する。
一方でgenericsは、ある特定のメソッドに特化したもの。
'''
# Userを作成する事だけに特化したViewを作る
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
    '''
    現在、settings.py にてViewsにアクセスできるのはログインUserのみという設定を、
    全てのViewsに対して設定している。
    しかし、CreateUser の場合は未だアカウントを作成していない利用者がアクセスできるようにする必要がある。
    そのため、アクセス権限を変更する。
    '''

# リストの取得に特化したView
class ListUserView(generics.ListAPIView):
    queryset = User.objects.all()   # 全てのオブジェクトを取得
    serializer_class = UserSerializer



# Retrieveが特定のオブジェクトを検索して返してくれる
class LoginUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    # ログインUserのUserオブジェクトを返す。
    def get_object(self):
        return self.request.user
        # この request.user がログインUserの意味になる


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    # 以下のperform_createがModelViewSetにおいて、CRUDのCreateに当たる。これを編集する。
    # 自動的にログインUserの情報を元にProfileを作成するようにするため。
    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user)

    # CRUDの delete と partial update を無効化する設定
    def destroy(self, request, *args, **kwargs):
        response = {'message': 'DELETE method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST) # responseとして 400 Bad Request を返す。

    def partial_update(self, request, *args, **kwargs):
        response = {'message': 'PATCH method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

# 新規Categoryを作成するエンドポイント
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def destroy(self, request, *args, **kwargs):
        response = {'message': 'DELETE method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        response = {'message': 'PUT method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        response = {'message': 'PATCH method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated, custompermissions.OwnerPermission,)
    ''' このTaskViewSetの権限を上書き(Override)する。
    Overrideで IsAuthenticated, OwnerPermission の２つを適用している。
    custompermissions.py にPUTとDELETEのメソッドはログインUserのみ受け付けるという条件を記載している。 '''

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        response = {'message': 'PATCH method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)







