from django.db import models

class Company(models.Model):
    name = models.CharField('name', max_length=255, unique=True)

    def __str__(self):
        return self.name
    
class Contact(models.Model):
    name = models.CharField('name', max_length=150)
    job = models.CharField('job', max_length=75)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True)
    note = models.TextField('note', 'note', False, blank=True, null=True)
    def __str__(self):
        return self.name

class Email(models.Model):
    email = models.EmailField()
    company = models.ForeignKey(Company, related_name='ecompany', on_delete=models.SET_NULL, blank=True, null=True)
    contact = models.ForeignKey(Contact, related_name='emails', on_delete=models.SET_NULL, blank=True, null=True)
    def __str__(self):
        return self.email

class Phone(models.Model):
    number = models.CharField('phone', max_length=12, unique=True)
    company = models.ForeignKey(Company, related_name='company', on_delete=models.SET_NULL, blank=True, null=True)
    contact = models.ForeignKey(Contact, related_name='phones', on_delete=models.SET_NULL, blank=True, null=True)
    def __str__(self):
        return self.number
