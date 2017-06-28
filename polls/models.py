from django.db import models
import datetime
from django.utils import timezone

#이렇게 클래스 인자값으로 모델을 주게 되면 얘는 테이블로 인식
#생성자로 객체 생성해서 .save() 하게 되면 그것이 곧 인설트 ㅋ
class Question(models.Model):
    question_text = models.CharField(max_length=200, )
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        #파이선은 이거 됨 둘다 만족시키길 원할때 거의 수학수준
        #하나라도 false 면 그냥 false 리턴함!!이건 리얼 혁명
        return now - datetime.timedelta(days=1) <= self.pub_date <= now



class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
