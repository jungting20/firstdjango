from django.conf.urls import url,include
from polls import views



urlpatterns = [
        # ex: /polls/
        #as_view()를 보면 이건 딱 제네릭이구나 생각하자
        #제네릭이니까 클래스로 해줘야함
        url(r'^$',views.IndexView.as_view() , name='index'),
        # ex: /polls/5/
        #디테일 뷰로 받을때는 pk를 꼭 넘겨줘야한다 안그럼 에러남 ㅋ 
        #이 pk를 받아서 모델만 등록해주면 거기서 pk로 검색 때림
        url(r'^(?P<pk>\d+)/$',views.DetailView.as_view(),name='detail'),
        # ex: /polls/5/results
        url(r'^(?P<pk>\d+)/results/$',views.ResultsView.as_view(),name='results'),
        # ex: /polls/5/vote
        url(r'^(?P<pk>\d+)/vote/$',views.vote,name='vote')

]
