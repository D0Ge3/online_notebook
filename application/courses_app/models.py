from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime


class User(AbstractUser):
    role = models.CharField("Роль", max_length=15, default='student')
    tel = models.CharField("Телефон", max_length=15, blank=True)
    group = models.ForeignKey(
        'StudentGroup', on_delete=models.PROTECT, null=True, blank=True,
        related_name='members'
    )

    REQUIRED_FIELDS = [
        'first_name', 'last_name', 'email', 'role', 'tel', 'group'
    ]

    def __str__(self):
        return self.username


class StudentStream(models.Model):
    title = models.CharField(max_length=60)

    def __str__(self):
        return self.title


class StudentGroup(models.Model):
    title = models.CharField(max_length=255)
    number = models.CharField(max_length=15)
    year_of_receipt = models.IntegerField()
    streams = models.ManyToManyField(
        StudentStream, through='GroupInStream', related_name='groups'
    )

    class Meta:
        unique_together = ['number', 'year_of_receipt']

    def add_member(self, user_id):
        user_to_add = User.objects.get(id=user_id)
        user_to_add.group = self
        user_to_add.save()

    def __str__(self):
        return self.title


class GroupInStream(models.Model):
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE)
    stream = models.ForeignKey(StudentStream, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.stream.title} {self.group.number}'


class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    LESSON_TYPES = [
        ('1', 'Lecture'),
        ('2', 'Practical work'),
        ('3', 'Laboratory work')
    ]

    group_in_stream = models.ForeignKey(GroupInStream, on_delete=models.CASCADE, blank=True, null=True)
    student_group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson_type = models.CharField(choices=LESSON_TYPES, default='1', max_length=1)
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return 'Course: {} Group: {}, {}'.format(self.course, self.group_in_stream, self.get_lesson_type_display())


class StudentLessonResult(models.Model):
    MARKS = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    ]

    VISIT_TYPES = [
        ('1', 'Visited'),
        ('2', 'Missed')
    ]
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    mark = models.CharField(choices=MARKS, default='1', max_length=1)
    visit = models.CharField(choices=VISIT_TYPES, default='1', max_length=1)
    comment = models.CharField(max_length=255)

    def __str__(self):
        return 'Student {}. Mark: {}. {}'.format(self.student, self.get_mark_display(), self.get_visit_display())


class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)

    def __str__(self):
        return 'Course {}, Section: {}'.format(self.course, self.title)


class TaskWithTick(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)

    def __str__(self):
        return '{}, Task: {}'.format(self.section, self.title)


class TaskWithTickOption(models.Model):
    task_with_tick = models.ForeignKey(TaskWithTick, on_delete=models.CASCADE)
    description = models.CharField(max_length=1024)

    def __str__(self):
        return '{}, Description: {}'.format(self.task_with_tick, self.description)


class TaskWithTickStudentResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_with_tick_option = models.ForeignKey(TaskWithTickOption, on_delete=models.CASCADE)
    perform = models.BooleanField(default=False)

    def __str__(self):
        return '{}, Is performed? {}'.format(self.task_with_tick_option, self.perform)
