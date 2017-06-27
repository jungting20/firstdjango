from django.conf.urls import url,include
from polls import views

urlpatterns = [
        # ex: /polls/
        url(r'^$',views.index , name='index'),
        # ex: /polls/5/
        url(r'^(?P<question_id>\d+)/$',views.detail,name='detail'),
        # ex: /polls/5/results
        url(r'^(?P<question_id>\d+)/results/$',views.detail,name='results'),
        # ex: /polls/5/vote
        url(r'^(?P<question_id>\d+)/vote/$',views.vote,name='vote')

]
