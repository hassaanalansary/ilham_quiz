from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import timedelta


class Sura(models.Model):
    name = models.CharField(max_length=100)
    page_count = models.IntegerField()


class Plan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sura = models.ForeignKey(Sura, on_delete=models.CASCADE)
    pace = models.FloatField()  # number of pages per day
    start_date = models.DateField()

    # there should be something related to hefz and moraga3a (memorizing and revision)
    # but it's unclear what is the business logic

    @property
    def finish_in_days(self):
        """:returns how many days till finishing this sura based on pace"""
        return self.sura.page_count / self.pace

    @property
    def expected_finish_date(self):
        """:returns date expected finishing date"""
        return self.start_date + timedelta(days=self.finish_in_days)
