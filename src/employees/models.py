from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Employee(models.Model):
    first_name = models.CharField(max_length=250)
    surname = models.CharField(max_length=250)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.surname} - {self.department.name}"
