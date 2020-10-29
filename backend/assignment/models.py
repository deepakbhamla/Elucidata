from django.db import models


class File(models.Model):
    file = models.FileField(blank=False, null=False)
    def __str__(self):
        return self.file.name

class TaskResult(models.Model):
    result_file = models.FileField(blank=False, null=False)
    def __str__(self):
        return self.id

