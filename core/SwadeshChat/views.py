from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.db.models import Q
from .utils import get_conditional_data
def home(request):
    if not request.user.is_authenticated:
        return redirect("/api/auth/login")
    
    base_url = request.get_full_path().split('?')[0]
    data = request.GET.get("data")
    add_contact = False
    data = get_conditional_data(data, add_contact, request)


    
    return render(request, "home.html", {"groups": data["data"], "base_url": base_url, "add_contact": data["add_contact"]})


def chatbox(request, slug):
    if not request.user.is_authenticated:
        return redirect("/api/auth/login")
    
    base_url = request.get_full_path().split('?')[0]
    data = request.GET.get("data")
    add_contact = False
    data = get_conditional_data(data, add_contact, request)
    receiver_type = request.GET.get("receiver_type")
    if receiver_type == "User":
        receiver = Contact.objects.get(slug=slug)

    elif receiver_type == "Group":
        receiver = Group.objects.get(slug=slug)
    
    messages = Message.objects.filter(slug=slug).order_by('created_at')

    context = {"slug": slug, "receiver": receiver, "messages": messages, "groups": data["data"],  "add_contact": data["add_contact"],  "base_url": base_url}
    return render(request, "chatbox.html", context=context)


def add_contact(request, user_id):
    user = User.objects.get(id=user_id)
    add_contact = False
    data = request.GET.get("data")
    data = get_conditional_data(data, add_contact, request)
    base_url = request.get_full_path().split('?')[0]
    if request.method == 'POST':
        receiver_type = ReceiverType.objects.get(name="User")
        contact = Contact.objects.create(user_id = request.user, 
                                         slug = request.user.username+user.username,
                                         contact_id = user,
                                         receiver_type = receiver_type)
        
        return redirect("/?data=contacts")
    
    return render(request, "add_contact.html", {"user": user, "groups": data["data"], "base_url": base_url, "add_contact": data["add_contact"] })


def create_group(request):
    if request.method == 'POST':
        receiver_type = ReceiverType.objects.get(name="Group")
        group_name = request.POST.get('group_name')
        selected_members = request.POST.get('selected_members').split(',')
    
        if not len(selected_members) > 0 or selected_members[0] == "":
            messages.info(request, "Please select atleast one member")
            return redirect(request.path)
        
        slug = request.user.username + ''.join(group_name.split(" "))
        try:
            group = Group.objects.get(slug=slug).all()

            if group:
                messages.info(request, "This Group is already in use")
                return redirect(request.path)
        except:
            group = Group.objects.create(slug=slug, name=group_name, receiver_type=receiver_type)

            member_type_for_participant = MemberType.objects.get(name="PARTICIPANT")
            for member in selected_members:
                group_member = GroupMember.objects.create(group=group, user=User.objects.get(username=member), member_type=member_type_for_participant)

            member_type_for_admin = MemberType.objects.get(name="GROUP_ADMIN")
            add_group_admin = GroupMember.objects.create(group=group, user=request.user, member_type=member_type_for_admin)

            return redirect("/?data=groups")
        
    
    add_contact = False
    data = request.GET.get("data")
    data = get_conditional_data(data, add_contact, request)
    base_url = request.get_full_path().split('?')[0]
    
    users_to_add = User.objects.exclude(id=request.user.id).all()
    print(users_to_add)

    return render(request, "create_group.html", {"users_to_add": users_to_add,"groups": data["data"], "base_url": base_url, "add_contact": data["add_contact"]})