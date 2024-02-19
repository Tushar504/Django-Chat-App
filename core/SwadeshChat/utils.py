from django.db.models import Q
from .models import User, GroupMember, Contact


def get_conditional_data(data, add_contact, request):
    if data == "groups":
        data = GroupMember.objects.filter(user=request.user)
        data = [group.group for group in data]
    elif data == "contacts":
        data = Contact.objects.filter(Q(user_id=request.user.id) | Q(contact_id=request.user.id))
    elif data == 'add_contact':
        add_contact = True
        users = User.objects.all()
        user_contacts = Contact.objects.filter(Q(user_id=request.user.id) | Q(contact_id=request.user.id))
        data = []
        if len(user_contacts) > 0:
            for user in users:
                check = True
                for contact in user_contacts:
                    if user == contact.user_id or user == contact.contact_id:
                        check = False

                if check:
                    data.append(user)
        else:
            for user in users:
                if user != request.user:
                    data.append(user)

    return {"data": data, "add_contact": add_contact}
