from django.db import models


class Long2Short(models.Model):
    long_url = models.CharField(max_length=2000)
    short_key = models.CharField(max_length=50)
    create_date = models.DateTimeField("date create")
    modified_data = models.DateTimeField("date modified", null=True)
    visit_sum = models.IntegerField(default=0)
    ip_address = models.CharField(max_length=100, null=True)

    def __str__(self):
        content = """
            long_url: {} ==> short_url: https://192.168.33.10:8080/tinyurl/{}
        """.format(self.long_url, self.short_key)

        return content
