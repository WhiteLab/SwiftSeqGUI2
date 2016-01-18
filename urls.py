from django.conf.urls import url, patterns
from swiftseqgui2.views import (generate_workflow as generate_workflow_views,
                                www as www_views)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Front-end URL Patterns
    url(r'^$', www_views.index, name='index'),
    url(r'^prebuilt-workflows/$', www_views.prebuilt_workflows, name='prebuilt-workflows'),
    url(r'^download/$', www_views.download, name='download'),

    # Generate Workflow URL Patterns
    url(r'^generate-workflow/$', generate_workflow_views.index, name='questions'),
    url(r'^generate-workflow/questions/$', generate_workflow_views.questions, name='questions'),
    url(r'^generate-workflow/generate/$', generate_workflow_views.generate, name='generate'),
    url(r'^generate-workflow/process-workflow/$', generate_workflow_views.process_workflow, name='process-workflow'),
    url(r'^generate-workflow/generate/get-parameters-for-program/(?P<program_id>\d+)/$',
    # Ajax URLs for generate-workflow
        generate_workflow_views.get_parameters_for_program, name='get-parameters-for-program'),
    url(r'^generate-workflow/generate/get-program-set/(?P<step_id>\d+)/(?P<program_set_id>\d+)/$',
        generate_workflow_views.get_program_set, name='get-program-set'),
    url(r'^generate-workflow/generate/get-parameters-line/(?P<parameter_name>[\w\-]+)/$',
        generate_workflow_views.get_parameters_line, name='get-parameters-line'),
    url(r'^generate-workflow/generate/get-program-attrs/(?P<program_id>\d+)/$',
        generate_workflow_views.get_program_attrs, name='get-program-attrs'),
    url(r'^generate-workflow/download-complete/$', generate_workflow_views.download_complete,
        name='download-complete')


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)