from django.db import models
import uuid
import os
from django.conf import settings


class Survey(models.Model):
    """
    Model representing a survey.
    """
    name = models.CharField(
        max_length=50,
        null=True,
        help_text='Name of survey.'
    )
    desc = models.CharField(
        max_length=250,
        null=True,
        help_text='Description of survey.'
    )

    def __str__(self):
        """String for representing the Survey object."""
        return str(self.name)

class Response(models.Model):
    """
    Model representing a exhibit reseponse.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text='Unique ID for this response.'
    )
    q = models.ForeignKey(
        'Question',
        on_delete=models.SET_NULL,
        null=True,
        help_text='Survey question.'
    )
    a = models.ManyToManyField(
        'Answer',
        help_text='Survey response.'
    )

    NULL = ''
    N = 'nonbinary'
    F = 'female'
    M = 'male'

    GENDERS = (
        (NULL, ''),
        (N, 'Nonbinary'),
        (F, 'Female'),
        (M, 'Male'),
    )

    gender = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        choices=GENDERS,
        default=None,
        help_text='Gender identity.')

    A = 'under-18'
    B = '18-24'
    C = '25-34'
    D = '35-44'
    E = '45-54'
    F = '55-64'
    G = '65-plus'

    AGES = (
        (NULL, ''),
        (A, 'Under 18.'),
        (B, '18-24'),
        (C, '25-35'),
        (D, '36-44'),
        (E, '45-54'),
        (F, '55-64'),
        (G, '65+.')
    )

    age = models.CharField(max_length=20,
        blank=True,
        null=True,
        choices=AGES,
        default=None,
        help_text='Age classes.')

    zip_code = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        default=None,
        help_text='ZIP code.'
    )

    U = 'urban'
    S = 'suburban'
    R = 'rural'

    HOMES = (
        (NULL, ''),
        (U, 'Urban'),
        (S, 'Suburban'),
        (R, 'Rural'),
    )

    home = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        choices=HOMES,
        default=None,
        help_text='Type of location respondant calls home.'
    )
    free_q = models.ForeignKey(
        'FreeQuestion',
        on_delete=models.SET_NULL,
        null=True,
        help_text='Free response question.'
    )
    free_resp = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text='Text of free response.'
    )
    survey = models.ForeignKey(
        'Survey',
        on_delete=models.SET_NULL,
        null=True,
        help_text='Survey name.'
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text='Timestamp of scan.'
    )
    front = models.FilePathField(
        path=os.path.join(settings.STATIC_URL, 'cards/fg2/'),
        match='.*-front\.png$',
        recursive=True,
        null=True,
        help_text='Path to card front scan.')
    back = models.FilePathField(
        path=os.path.join(settings.STATIC_URL, 'cards/fg2/'),
        match='.*-back\.png$',
        recursive=True,
        null=True,
        help_text='Path to card back scan.'
    )

    def __str__(self):
        """String for representing the Question Model object."""
        return str(self.timestamp)

class Question(models.Model):
    """
    Model representing a question.
    """
    MULT = 'multiple-choice'
    TF = 'true-false'
    SELECT_MULTIPLE = 'select-multiple'
    LIKERT = 'likert'

    QUESTION_TYPES = (
        (MULT, 'Multiple Choice'),
        (TF, 'True/False'),
        (SELECT_MULTIPLE, 'Select Multiple'),
        (LIKERT, 'Likert'),
    )

    question = models.CharField(
        max_length=200,
        help_text='Question text.'
    )
    question_type = models.CharField(
        max_length=200,
        choices=QUESTION_TYPES,
        default=MULT,
        help_text='Question type.'
    )

    def __str__(self):
        """String for representing the Question Model object."""
        return self.question

    def get_absolute_url(self):
        """Returns the url to access a detail record for this question."""
        return reverse('question-detail', args=[str(self.id)])

class FreeQuestion(models.Model):
    """
    Model representing a question.
    """
    free_question = models.CharField(
        max_length=200,
        help_text='Free response question text.'
    )

    def __str__(self):
        """String for representing the Question Model object."""
        return self.free_question

class Answer(models.Model):
    """
    Model representing an answer.
    """
    q = models.ManyToManyField(
        Question,
        help_text='Associated question.'
    )
    answer = models.CharField(
        max_length=200,
        help_text='Answer.'
    )

    def __str__(self):
        """String for representing the Question Model object."""
        return self.answer
