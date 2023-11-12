from django.db import models

from utils.snowflakes import SnowflakeIDField, SnowflakeGenerator

from authentication.models import User


class Form(models.Model):
    # Identifiers
    id = SnowflakeIDField(primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Meta
    title = models.CharField(max_length=100, default="Untitled Form")
    description = models.TextField(max_length=1000, blank=True, null=True)
    question_count = models.IntegerField(default=0)

    # Settings
    quiz = models.BooleanField(default=False)
    require_account = models.BooleanField(default=False)

    # Time records
    creation_timestamp = models.FloatField()
    last_edit_timestamp = models.FloatField()

    def save(self, *args, **kwargs):
        if self.id == "unset":
            self.id = str(SnowflakeGenerator().generate_id())

        super().save(*args, **kwargs)

    def to_dict(self) -> dict:
        return {
            'form_id' : self.id,
            'user_id' : self.user.id,
            'title' : self.title,
            'description' : self.description,
            'question_count' : self.question_count,
            'quiz' : self.quiz,
            'require_account' : self.require_account,
            'creation_timestamp' : self.creation_timestamp,
            'last_edit_timestamp' : self.last_edit_timestamp
        }
    

# QUESTION TYPES
class TextType(models.Model):
    # Meta
    answer = models.TextField(max_length=5000, blank=True, null=True)

    min_length = models.IntegerField(default=0)
    max_length = models.IntegerField(default=5000)


class IntegerType(models.Model):
    # Meta
    answer = models.BigIntegerField(blank=True, null=True)

    min_value = models.BigIntegerField(default=0)
    max_value = models.BigIntegerField(default=9223372036854775807)


class Choice(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text
    

class MultipleChoiceType(models.Model):
    # Meta
    answer = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name="correct_choice", blank=True, null=True)
    choices = models.ManyToManyField(Choice, related_name="multiple_choices")

    min_choices = models.IntegerField(default=0)
    max_choices = models.IntegerField(default=5)


class Question(models.Model):
    # Identifiers
    id = SnowflakeIDField(primary_key=True, unique=True)

    form = models.ForeignKey(Form, on_delete=models.CASCADE)

    index = models.IntegerField()

    # Settings
    required = models.BooleanField(default=False)

    # Meta
    question = models.TextField(max_length=1000)
    question_type = models.IntegerField()

    string_question = models.ForeignKey(TextType, on_delete=models.CASCADE, related_name="string_question", blank=True, null=True)
    integer_question = models.ForeignKey(IntegerType, on_delete=models.CASCADE, related_name="integer_question", blank=True, null=True)
    multiple_choice_question = models.ForeignKey(MultipleChoiceType, on_delete=models.CASCADE, related_name="multiple_choice_question", blank=True, null=True)

    # Time records
    creation_timestamp = models.FloatField()
    last_edit_timestamp = models.FloatField()

    def save(self, *args, **kwargs):
        if self.id == "unset":
            self.id = str(SnowflakeGenerator().generate_id())

        super().save(*args, **kwargs)

    def to_dict(self, form: bool=True, answers: bool=False) -> dict:
        data = {
            'question_id' : self.id,
            'form_id' : self.form.id,
            'index' : self.index,
            'question_type' : self.question_type,
            'required' : self.required, 
            'question' : self.question,
        }

        if form:
            data['form'] = Form.objects.get(id=self.form.id).to_dict()

        if answers: 
            data['answers'] = []

            for answer in Answer.objects.filter(form_id=self.form.id, question_id=self.id):
                data['answers'].append(answer.to_dict(False))

        return data
    

class Answer(models.Model):
    # Identifiers
    id = SnowflakeIDField(primary_key=True, unique=True)

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    
    track_id = models.TextField(max_length=256, blank=True, null=True)

    # Meta
    question_type = models.IntegerField()

    string_answer = models.ForeignKey(TextType, on_delete=models.CASCADE, related_name="string_answer", blank=True, null=True)
    integer_answer = models.ForeignKey(IntegerType, on_delete=models.CASCADE, related_name="integer_answer", blank=True, null=True)
    multiple_choice_answers = models.ForeignKey(MultipleChoiceType, on_delete=models.CASCADE, related_name="multiple_choice_answer", blank=True, null=True)

    # Time records
    creation_timestamp = models.FloatField()

    def save(self, *args, **kwargs):
        if self.id == "unset":
            self.id = str(SnowflakeGenerator().generate_id())

        super().save(*args, **kwargs)

    def to_dict(self, question: bool=False) -> dict:
        if self.question_type == 1:
            answer = self.string_answer

        elif self.question_type == 2:
            answer = self.integer_answer

        elif self.question_type == 3:
            answer = []

            for choice in self.multiple_choice_answers.choices.all(): # type: ignore
                answer.append(choice)
        else:
            answer = None

        if not answer:
            answer = self.integer_answer

        if question:
            return {
                'answer_id' : str(self.id),
                'form_id' : str(self.form.id),
                'track_id' : str(self.track_id),
                'question' : Question.objects.get(id=self.question.id).to_dict(False, False),
                'answer' : answer
            }

        return {
            'answer_id' : str(self.id),
            'form_id' : str(self.form.id),
            'track_id' : str(self.track_id),
            'question_id' : str(self.question.id),
            'answer' : answer
        }