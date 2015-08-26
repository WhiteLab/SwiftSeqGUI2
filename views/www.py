__author__ = 'dfitzgerald'
from django.shortcuts import render
from swiftseqgui2.models import PrebuiltWorkflow, SoftwareVersion

def index(request):
    return render(request, 'swiftseqgui2/www/home.html')

def prebuilt_workflows(request):
    prebuilts = PrebuiltWorkflow.objects.all()
    context = {'prebuilts': prebuilts}
    return render(request, 'swiftseqgui2/prebuilt_workflows/prebuilt_workflows.html', context)

def download(request):
    softwares = SoftwareVersion.objects.all().order_by('sortable_version_number')
    context = {'softwares': softwares}
    return render(request, 'swiftseqgui2/download/download.html', context)
