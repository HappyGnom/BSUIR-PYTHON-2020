from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')

#     def __str__(self):
#         return self.question_text

#     def was_published_recently(self):
#         now = timezone.now()
#         return now - datetime.timedelta(days=1) <= self.pub_date <= now


# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)

#     def __str__(self):
#         return self.choice_text


class Review(models.Model):
    company = models.CharField(max_length=20)
    comment = models.CharField(max_length=100)
    rating = models.FloatField(default=0, validators=[
                               MinValueValidator(0.0), MaxValueValidator(10.0)])
    image = models.ImageField()

    def __str__(self):
        return f'\"{self.company}\" - {self.comment}'


class Project(models.Model):
    name = models.CharField(max_length=20)
    client = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    image = models.ImageField()

    def __str__(self):
        return f'{self.name} ({self.client}) - {self.description}'
