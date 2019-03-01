from .models import Contact, Company, Phone, Email
from .serializer import CompanySerializer, ContactSerializer, PhoneSerializer, EmailSerializer
from rest_framework import viewsets

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer