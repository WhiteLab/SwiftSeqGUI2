from django.contrib import admin
from swiftseqgui2.models import *

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Step)
admin.site.register(Program)
admin.site.register(Parameter)
admin.site.register(PrebuiltWorkflow)
admin.site.register(SoftwareVersion)