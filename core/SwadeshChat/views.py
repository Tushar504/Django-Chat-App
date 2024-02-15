from django.shortcuts import render, redirect
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