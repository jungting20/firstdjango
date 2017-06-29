from django.shortcuts import render,get_object_or_404
from django.views import generic
from polls.models import Question,Choice
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    # model = Question 이게 결국 queryset = Question.objects.all()
    #이거랑 같음
    #만약 넘길때 pk가 지정 되어있지 않으면 그냥 기본으로
    #select * from Question 한게 모델에 저장이 된다
    #결국 위에 주석 4줄이 사실상 같은말 ㅋ 뭐한 거지
    #그리고 모델 속성 값을 지정해 주면 context_object_name = 'latest_question_list'
    #이부분을 해주지 않아도 question 으로 html에서 부를 수 있다
    #지정해주면 저걸로 오버라이딩됨

    #조건 줘서 리스트 뽑을거면 queryset 해서 뽑으면됨
    #def get_queryset도 같음
    #와 장고 엄청나구만
    #ㅋ 작거나 같다 less than or equal 이래서 lte ㅋ
    #너무나도 엄청나다
    #str(Question.objects.filter(pub_date__in=timezone.now()).query)이거해보면
    #select ... 해서 쿼리문 나옴 ㅋ 정말로 엄청남
    queryset = Question.objects.filter(pub_date__lte=timezone.now()
                                       ).order_by('-pub_date')[:5]
    #이걸 써도 같음 ㅋ 이렇게 하는게 더 나은듯 근데 왜 굳이 저렇게 쓰는거지
    # def get_queryset(self):
    #      return Question.objects.order_by('-pub_date')[:5]
    context_object_name = 'latest_question_list'
    #이걸 지정 해준건 def get_queryset 를 오버라이드 해서
    #그 뽑아온 리스트를 저장 할 이름이 필요함 아니면 모르니까 ㅋ
    #그니까 def get_queryset으로 받아온 리스트는 이름을 지정해 줘야한다


#pk로 넘기면 모델만 지정해주면 알아서 pk로 검색해서 쳐넣음 리얼
#장고파워임?
#저 템플릿 네임 오버라이드 안해주면 디폴트값으로 찾아감 디폴트값이 존재하긴하는 듯
class DetailView(generic.DetailView):
    #이거 스프링처럼 컨텍스트 오브젝트 네임 저거 지정 안해주면
    #Question 이면 question으로 리퀘스트 영역에 저장됨!! 크
    #스프링 덕분에 이해가 쉽다
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'



def vote(request,question_id):
    p = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
        #이것의 의미는 얘는 참조키에서 받아오니까
        #현재의 p가 가지고 있는 pk로 참조하는 모든 애들을 불러옴 그중
        #즉 p의 pk가 1이라면 이 polls_choice테이블의 question_id값이
        #polls_question의 id 값을 참조하므로 question_id의 값이 p.id 값인 것을
        #말함 그래서 p.choice_set.all()을 하면 where question_id=p.id 인것을
        #다 불러옴
        #p.choice_set.get(pk=request.POST['choice'])
        #이것의 의미는 question_id=p.id 인것 중에 pk 즉 choice테이블의 id 값이
        #request.POST['choice']값 인것을 찾아라 이 뜻!
        #request.POST[] 이 메서드가 저기 초이스 값이 존재하지 않으면
        #즉 체크를 안하면 value값이 없으니까 KeyError이 발생함
        #사실 포스트 처리 깔끔하게 끝나면 리다이렉트 쳐줘야함 이건 뭐 상식
        #
    except (KeyError,Choice.DoesNotExist):
        return render(request,'polls/detail.html',{
            'question':p,
            'error_message':"You didn't select a choice."
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        #이건 아마도 urls.py에 지정한 그 이름을 넣어주는 클라스 진짜 존나 헷갈리네
        #이렇게 리다이렉트 칠때 리버스를 이용하면 파라미터까지 넘길 수 있음
        #이렇게 안하면 하드코딩으로 직접 유알엘 지정해주는 스트레스 받는일을
        #해야함 보면 알겠지만 유알엘에는 이미 파라미터로쓴다고 지정 되어있음
        #그 값을 저기다 넣어주는거지
        return HttpResponseRedirect(reverse('results',args=(p.id,)))


