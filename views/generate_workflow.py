__author__ = 'dfitzgerald'
''' Views file for Generate Workflow '''
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from swiftseqgui2.models import Question, Answer, Step, Program, Parameter

import json
import time


def index(request):
    return HttpResponseRedirect('/swiftseq/generate-workflow/questions/')


def questions(request):
    db_questions = Question.objects.all()
    question_sets = []
    for i, question in enumerate(db_questions):
        answers = question.answer_set.all()
        question_sets.append({
            'question': question,
            'answers': answers,
            'data': {
                'order': i
            }
        })

    context = {
        'question_sets': question_sets,
        'num_questions': len(question_sets),
        'q': db_questions
    }
    return render(request, 'swiftseqgui2/generate_workflow/questions.html', context)


def generate(request):
    context = {'nodata': True}
    if request.method == 'POST':
        context['nodata'] = False

        post_questions = {}
        for post in request.POST:
            if 'question_id' in post:
                post_questions[post] = request.POST[post]

        context['question_sets'] = []
        allowed_answers_ids = []
        for question in post_questions:
            question_id = question.split('_')[2]
            answer_id = post_questions[question]
            db_question = Question.objects.get(pk=question_id)
            db_answer = Answer.objects.get(pk=answer_id)
            context['question_sets'].append({
                'question': db_question,
                'answer': db_answer
            })
            allowed_answers_ids.append(answer_id)

        steps = Step.objects.filter(allowed_answers__in=allowed_answers_ids)
        context['steps'] = steps

    print context
    return render(request, 'swiftseqgui2/generate_workflow/generate.html', context)


def process_workflow(request):
    output_data = {}
    post = request.GET

    # Add questions data to output data
    input_questions = [key for key in post if key.startswith('question-')]
    for input_question in input_questions:
        ques_id = input_question.split('-')[1]
        ques = Question.objects.get(pk=ques_id).programmatic_name
        ans_id = post[input_question]
        ans = Answer.objects.get(pk=ans_id).programmatic_name
        output_data[ques] = ans

    # Get step checkboxes that were checked
    option_checkboxes = [key for key in post if key.startswith('option-checkbox-')]
    checked_steps = []
    for val in option_checkboxes:
        checked_steps.append(val.split('-')[2])

    # Get a set of all programSet IDs
    program_set_ids = set()
    for key in post.keys():
        if key.startswith('programSet-'):
            program_set_ids.add(key.split('__')[0].split('-')[1])

    # Iterate through each programSet
    for program_set_id in program_set_ids:
        program_set_name = 'programSet-' + program_set_id

        # Get step, add to output data
        step_id = post[program_set_name + '__step']
        step_name = Step.objects.get(pk=step_id).name
        if step_name not in output_data:
            output_data[step_name] = {}
        if step_id not in checked_steps:
            continue

        # Get program, add to output data
        program_id = post[program_set_name + '__program']
        program_name = Program.objects.get(pk=program_id).name
        output_data[step_name][program_name] = {}

        # Get program attributes, add to output data
        program_attr_keys = [key for key in post if key.startswith(program_set_name + '__programAttr-')]
        for program_attr_key in program_attr_keys:
            program_attr_name = program_attr_key.split('__')[1].split('-')[1]
            output_data[step_name][program_name][program_attr_name] = post[program_attr_key]

        # Get program parameters, add to output data
        program_parameter_keys = [key for key in post if key.startswith(program_set_name + '__parameter-')]
        num_parameters = len(program_parameter_keys) / 2
        output_data[step_name][program_name]['params'] = {}
        for i in range(num_parameters):
            param_pk = post[program_set_name + '__parameter-' + str(i) + '__key']
            if param_pk == '':
                continue
            param_name = Parameter.objects.get(pk=param_pk).name
            param_val = post[program_set_name + '__parameter-' + str(i) + '__value']
            output_data[step_name][program_name]['params'][param_name] = param_val

    filename = post['download-filename']
    if filename == '':
        filename = 'SwiftSeq_workflow_config_' + time.strftime('%d%b%Y')
    elif filename[-5:] == '.json':
        filename = filename[:-5]
    file_content = json.dumps(output_data)
    download_response = HttpResponse(file_content, content_type='application/json')
    download_response['Content-Disposition'] = 'attachment; filename=' + str(filename) + '.json'
    return download_response


def download_complete(request):
    return render(request, 'swiftseqgui2/generate_workflow/download_complete.html')

# def process_workflow(request):
#     # Get those option checkboxes which were checked
#     output_data = {}
#     checked_steps = [key for key in request.POST if key.startswith('option-checkbox-')]
#     post = request.POST
#     for step in checked_steps:
#         # Get step name and ID
#         step_id = step.split('-')[2]
#         step_name = Step.objects.get(pk=step_id).name
#         # Add key for this step to output data
#         output_data[step_name] = {}
#         # Filter POST array for this step ID
#         filter_on_step = [key for key in post if key.startswith(step_id)]
#         # Get unique program IDs within this step
#         program_ids = set()
#         for elem in filter_on_step:
#             program_ids.add(elem.split('-')[1])
#         # Iterate through program IDs, getting parameters for each one
#         for program_id in program_ids:
#             # Get program name and add key for this program
#             program_name = Program.objects.get(pk=program_id).name
#             output_data[step_name][program_name] = {}
#             # Get all keys that pertain to this program
#             key_startswith = step_id + '-' + program_id + '-'
#             parameter_lines = [key for key in filter_on_step if key.startswith(key_startswith)]
#             # Calculate number of parameters
#             num_parameters = len(parameter_lines) / 2
#             output_data[step_name][program_name]['params'] = {}
#
#             # Iterate through each parameter for this program
#             for i in range(num_parameters):
#                 param_pk = post[key_startswith + str(i) + '_key']
#                 if param_pk == '':
#                     continue
#                 param_name = Parameter.objects.get(pk=param_pk).name
#                 param_val = post[key_startswith + str(i) + '_value']
#                 output_data[step_name][program_name]['params'][param_name] = param_val
#
#     print '===output_data==='
#     print output_data
#     print '===POST==='
#     print request.POST
#     return HttpResponse('hi')

def get_program_attrs(request, program_id):
    program = Program.objects.get(pk=program_id)
    data = {
        'help_url': program.help_url,
        'walltime': program.walltime
    }
    return HttpResponse(json.dumps(data))


def get_parameters_for_program(request, program_id):
    data = []
    parameters = Program.objects.get(pk=program_id).parameter_set.all()
    for parameter in parameters:
        data.append({'id': parameter.id, 'text': parameter.name})
    return HttpResponse(json.dumps(data))


def get_program_set(request, step_id, program_set_id):
    step = Step.objects.get(pk=step_id)
    context = {'step': step, 'program_set_id': program_set_id}
    return render(request, 'swiftseqgui2/ajax/program_set.html', context)


def get_parameters_line(request, parameter_name):
    context = {'parameter_name': parameter_name}
    return render(request, 'swiftseqgui2/ajax/parameters-line.html', context)
