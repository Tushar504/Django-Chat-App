from .models import *
from django.db.models import Q
def get_conditional_data(data, add_contact, request):
    if data == "groups":
        data = Group.objects.all()
    elif data == "contacts":
        data = Contact.objects.filter(Q(user_id=request.user.id) | Q(contact_id=request.user.id))
    elif data == 'add_contact':
        add_contact = True
        users = User.objects.all()
        user_contacts = Contact.objects.filter(Q(user_id=request.user.id) | Q(contact_id=request.user.id))
        data = []
        if len(user_contacts) > 0:
            for user in users:
                for contact in user_contacts:
                    if user != contact.user_id and user != contact.contact_id and user != request.user:
                        data.append(user)
        else:
            for user in users:
                if user != request.user:
                    data.append(user)
    
    return {"data": data, "add_contact": add_contact}