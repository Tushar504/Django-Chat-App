from django.contrib import admin
from .models import *


admin.site.register(Group)
admin.site.register(ReceiverType)
admin.site.register(Message)
admin.site.register(Contact)
admin.site.register(MemberType)
admin.site.register(GroupMember)
admin.site.register(MessageStatus)
admin.site.register(Status)