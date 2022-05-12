from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static    # 画像ファイルの場所を設定

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('authen/', include('djoser.urls.jwt')),    # JWTの認証関係のサイトに移動
]
# JIRA_API直下のmediaディレクトリの場所。MEDIA_URL, MEDIA_ROOT は settings.py に記載。
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
