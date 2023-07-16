from django.db import models



class Register(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phoneno = models.BigIntegerField(default=0)
    password = models.CharField(max_length=128)
    val = models.IntegerField(default=0)


class TodoTask(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey(Register, on_delete=models.CASCADE)
    taskTest = models.CharField(max_length=400)
    createdTime = models.DateTimeField(auto_now_add=True,null=True)
    updatedTime = models.DateTimeField(auto_now=False,null=True, default=None)
    checkedTime = models.DateTimeField(auto_now=False,null=True, default=None)
    deletedTime = models.DateTimeField(auto_now=False,null=True, default=None)
   # serial = models.IntegerField(default=0)
    status_c = models.BooleanField()
    status_d = models.BooleanField()




# from django.db import models

# class YourModel(models.Model):
#     updatedTime = models.DateTimeField(null=True, default=None)
#     checkedTime = models.DateTimeField(null=True, default=None)
#     deletedTime = models.DateTimeField(null=True, default=None)
