from django.db import models
import uuid

class Survey(models.Model):
    """
    Model representing a survey.
    """
    name = models.CharField(max_length=200, null=True,
        help_text='Name of survey.')
    desc = models.CharField(max_length=200, null=True,
        help_text='Description of survey.')

    def __str__(self):
        """String for representing the Survey object."""
        return str(self.name)

class Response(models.Model):
    """
    Model representing a exhibit reseponse.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
        help_text='Unique ID for this response.')
    q = models.ForeignKey('Question', on_delete=models.SET_NULL, null=True,
        help_text='Survey question.')
    a = models.ForeignKey('Answer', on_delete=models.SET_NULL, null=True,
        help_text='Survey response.')

    M = 'male'
    F = 'female'
    N = 'nonbinary'

    GENDERS = (
        (M, 'Male'),
        (F, 'Female'),
        (N, 'Nonbinary'),
    )

    gender = models.CharField(max_length=200, choices=GENDERS,
        default=N, help_text='Gender identity.')

    A = 'under-18'
    B = '18-24'
    C = '25-34'
    D = '35-44'
    E = '45-54'
    F = '55-64'
    G = '65-plus'

    AGES = (
        (A, 'Under 18.'),
        (B, '18-24'),
        (C, '25-34'),
        (D, '35-44'),
        (E, '45-54'),
        (F, '55-64'),
        (G, '65+.')
    )

    age = models.CharField(max_length=25, choices=AGES, default=C, help_text='Age classes.')

    U = 'urban'
    S = 'suburban'
    R = 'rural'

    HOMES = (
        (U, 'Urban'),
        (S, 'Suburban'),
        (R, 'Rural'),
    )

    zip_code = models.CharField(max_length=10, null=True, help_text='ZIP code.')
    home = models.CharField(max_length=10, choices=HOMES, default=U,
        help_text='Type of location respondant calls home.')
    survey = models.ForeignKey('Survey', on_delete=models.SET_NULL, null=True,
        help_text='Survey name.')
    timestamp = models.DateTimeField(auto_now_add=True,
        help_text='Timestamp of scan.')
    front = models.CharField(max_length=200, null=True,
        help_text='Path to full card scan.')
    back = models.CharField(max_length=200, null=True,
        help_text='Path to full card scan.')

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

    question = models.CharField(max_length=200,
        help_text='Question text.')
    type = models.CharField(max_length=200, choices=QUESTION_TYPES, default=MULT, help_text='Question type.')

    def __str__(self):
        """String for representing the Question Model object."""
        return self.question

    def get_absolute_url(self):
        """Returns the url to access a detail record for this question."""
        return reverse('question-detail', args=[str(self.id)])

class Answer(models.Model):
    """
    Model representing an answer.
    """
    q = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True,
        help_text='Associated question.')
    answer = models.CharField(max_length=200,
        help_text='Answer.')

    def __str__(self):
        """String for representing the Question Model object."""
        return self.answer
