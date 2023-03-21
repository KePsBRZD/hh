from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length=255)

class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    position = models.IntegerField(default=0)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True, blank=True, related_name='items')

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title