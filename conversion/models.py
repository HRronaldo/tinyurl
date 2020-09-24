from django.db import models

from tinyurl.settings import TinyurlDOMIAN


class Long2Short(models.Model):
    long_url = models.CharField(max_length=1000)
    short_key = models.CharField(max_length=10, db_index=True, unique=True)
    create_date = models.DateTimeField("date create")
    ip_address = models.CharField(max_length=100, null=True)

    def __str__(self):
        content = """
            long_url: {} ==> short_url: {}/tinyurl/{}
        """.format(self.long_url, TinyurlDOMIAN, self.short_key)

        return content


class Long2ShortV2(models.Model):
    long_url = models.CharField(max_length=1000)
    create_date = models.DateTimeField("date create")
    ip_address = models.CharField(max_length=100, null=True)

    def __str__(self):
        content = """
                long_url: {} 
            """.format(self.long_url)

        return content

