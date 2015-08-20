from django.db import models


class Question(models.Model):
    name = models.CharField(max_length=1024, verbose_name='Question Name')
    programmatic_name = models.CharField(max_length=1024, verbose_name='Programmatic Question Name')

    def __unicode__(self):
        return self.name


class Answer(models.Model):
    name = models.CharField(max_length=128, verbose_name='Answer Name')
    programmatic_name = models.CharField(max_length=1024, verbose_name='Programmatic Answer Name')
    question = models.ForeignKey(Question)

    def __unicode__(self):
        return self.name + ' | Answer to Question: ' + self.question.name


class Step(models.Model):
    name = models.CharField(max_length=128, verbose_name='Step Name')
    allowed_answers = models.ManyToManyField(Answer)
    required = models.BooleanField(default=False)
    multiple_programs = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    def get_programmatic_name(self):
        return self.name.replace(' ', '_')


class Program(models.Model):
    name = models.CharField(max_length=128, verbose_name='Program Name')
    step = models.ForeignKey(Step)
    walltime = models.CharField(max_length=64, verbose_name='Walltime')
    help_url = models.CharField(max_length=512, verbose_name='Help URL')

    def __unicode__(self):
        return self.name + ' | Program for Step: ' + self.step.name


class Parameter(models.Model):
    name = models.CharField(max_length=128, verbose_name='Parameter Name')
    program = models.ForeignKey(Program)

    def __unicode__(self):
        return self.name + ' | Parameter for Program: ' + self.program.name
