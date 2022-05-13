from rest_framework import permissions


class OwnerPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS は GETメソッド等、データの値を変更しないメソッドのこと。
        # つまり、GETなどデータの変更をしないメソッドでのアクセスならばTrueを返す。
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner.id == request.user.id
        ''' ログインUserの場合のみ、PUTやDELETEなどのデータを変更するメソッドを許可する。
            owner.id は、ログインUser、
            request.user.idは、React側からPUTメソッド等でアクセスしてきたUser
        '''




