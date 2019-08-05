from django.urls import path,re_path
from . import views
from django.conf.urls import url
from FBA import settings
from django.conf.urls.static import static

app_name = 'app_name'
urlpatterns = [
    url('^webApp/$',views.webApp,name="webApp"),
    url("^webAppcont/$",views.webAppcont,name="webAppcont"),
    url('^download/(?P<hash_str>[a-zA-Z0-9]{32})/$',views.download, name='download'),
    url('^cont/$', views.cont, name='cont'),
    url('^result/$',views.result,name="result"),
    url("^resultcont/(?P<hash_str>.*)/$",views.resultcont,name="resultcont"),
    url("^view/$",views.view,name="view"),
    url('^downloadimage/$',views.downloadimage,name="downloadimage"),
    url("^search/(?P<hash_str>[a-zA-Z0-9]{32})/$",views.search,name="search"),
    url("^searchcont/$",views.searchcont,name="searchcont"),
    url("^searchresult/(?P<hash_str>[a-zA-Z0-9]{32})/$",views.searchresult,name="searchresult"),
    url("^help/$",views.help,name="help")
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)