import datetime
from django.utils import timezone
from django.test import TestCase
from polls.models import Question
from django.core.urlresolvers import reverse

class QuestionMethodTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        time = timezone.now()+datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        #지금 이부분은 쿼리를 뽑아오는게 아니라 새로운 객체를 생성하는거임
        #생성한 상태에서 save를 하게되면 그때 insert가되고 그 다음부터 사용할 수 있는 거다
        #헷갈리지 말자 쿼리문 얻어오는 거하고
        self.assertEqual(future_question.was_published_recently(),False)
        #그니까 난 이렇게 넣으면 false를 원한다고 넣었음
        #근데 원래 메서드가 트루를 리턴해버리면 테스트가 틀렸다고 말해줌
        #만약 정상적으로 리턴하면 아무런 익셉션없이 잘돌아감 지린다

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)


        self.assertEqual(old_question.was_published_recently(),False)

    def test_was_published_recently_with_recently_question(self):
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)

        self.assertEqual(recent_question.was_published_recently(), True)

def create_question(question_text, days):
    time = timezone.now() + datetime.timezone(days=days)
    return Question.objects.create(question_text = question_text ,
                                   pub_date=time)

class QuestionViewTests(TestCase):

    #self는 이걸 의미 크 클라스 TestCase 클래스
    def test_index_view_with_no_question(self):

        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code,200)
        self.assertContains(response,"No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_index_view_with_a_past_question(self):
        create_question(question_text="Past question",days=-30)

        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: Past question.>'])


