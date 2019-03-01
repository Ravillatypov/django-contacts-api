from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Company, Contact, Phone, Email

class PhoneSerializer(ModelSerializer):
    class Meta:
        model = Phone
        fields = ('number',)
        extra_kwargs = {
            'number': {'validators': []}
        }
    def create(self, validated_data):
        instance = Phone(**validated_data)
        instance.save()
        return instance

class EmailSerializer(ModelSerializer):
    class Meta:
        model = Email
        fields = ('email',)
    def create(self, validated_data):
        instance = Email(**validated_data)
        instance.save()
        return instance

class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = ('name',)
        extra_kwargs = {
            'name': {'validators': []}
        }
    
    def create(self, validated_data):
        instance = Company(**validated_data)
        instance.save()
        return instance

class ContactSerializer(ModelSerializer):
    phones = PhoneSerializer(many=True)
    emails = EmailSerializer(many=True)
    company = CompanySerializer(many=False)
    class Meta:
        model = Contact
        fields = ('pk','name','company', 'job','note','phones','emails',)

    def phonesUpdate(self, context, newphones):
        contact_id = context.get('contact_id', None)
        company_id = context.get('company_id', None)
        if contact_id is None:
            return
        phones = Phone.objects.all().filter(contact_id=contact_id)
        len_new = len(newphones)
        len_old = len(phones)
        len_min = len_old if len_new > len_old else len_new
        for i in range(len_min):
            new_phone = newphones[i].get('number', '')
            if len(new_phone) > 0:
                phones[i].number = new_phone
                try:
                    phones[i].save()
                except Exception as e:
                    phones[i].delete()
                    phone = Phone.objects.get(number=new_phone)
                    phone.company_id = company_id
                    phone.contact_id = contact_id
                    phone.save()
            else:
                phones[i].delete()
        if len_new > len_old:
            for i in range(len_min, len_new):
                new_phone = newphones[i].get('number', '')
                if len(new_phone) > 0:
                    phone,_ = Phone.objects.get_or_create(number=new_phone)
                    phone.contact_id = contact_id
                    phone.company_id = company_id
                    phone.save()
        elif len_new < len_old:
            for i in range(len_min, len_old):
                phones[i].delete()

    def emailsUpdate(self, context, newemails):
        contact_id = context.get('contact_id', None)
        company_id = context.get('company_id', None)
        if contact_id is None:
            return
        emails = Email.objects.all().filter(contact_id=contact_id)
        len_new = len(newemails)
        len_old = len(emails)
        len_min = len_old if len_new > len_old else len_new
        for i in range(len_min):
            new_email = newemails[i].get('email', '')
            if len(new_email) > 0:
                emails[i].email = new_email
                try:
                    emails[i].save()
                except Exception as e:
                    emails[i].delete()
                    email = Email.objects.get(email=new_email)
                    email.company_id = company_id
                    email.contact_id = contact_id
                    email.save()
            else:
                emails[i].delete()
        if len_new > len_old:
            for i in range(len_min, len_new):
                new_email = newemails[i].get('email', '')
                if len(new_email) > 0:
                    email,_ = Email.objects.get_or_create(email=new_email)
                    email.contact_id = contact_id
                    email.company_id = company_id
                    email.save()
        elif len_new < len_old:
            for i in range(len_min, len_old):
                emails[i].delete()

    def create(self, validated_data):
        name = validated_data.get('name')
        job = validated_data.get('job')
        note = validated_data.get('note')
        instance = Contact(name=name, job=job, note=note)
        instance.save()
        return self.update(instance, validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.job = validated_data.get('job', instance.job)
        instance.note = validated_data.get('note', instance.note)
        company_name = validated_data.get('company',{}).get('name', '')
        company_name = company_name.strip().lower()
        if len(company_name) > 0:
            company, created = Company.objects.get_or_create(name=company_name)
            if created:
                company.save()
            instance.company_id = company.pk             
        else:
            instance.company_id = None
        instance.save()        
        context = {'contact_id': instance.pk, 'company_id': instance.company_id}
        self.phonesUpdate(context, validated_data.get('phones', []))
        self.emailsUpdate(context, validated_data.get('emails', []))
        return instance