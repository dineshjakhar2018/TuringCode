from django.db import models

ExamShift = (
    ('Morning','Morning'),
    ('Afternoon','Afternoon'),
)
ExamSession = (
    ('June','June'),
    ('December','December'),
)

ExamPaper = (
    (1,1),
    (2,2),
)

QuestionType = (
    ('MCQ','MCQ'),
    ('MSQ','MSQ'),
    ('NAT','NAT')
)

Subject = (
    ('Computer Science & Information Technology','Computer Science & Information Technology'),
    ('Data Science and Artificial Intelligence','Data Science and Artificial Intelligence')
)

TotalShift = (
    (1,1),
    (2,2)
)

Marks = (
    (1,1),
    (2,2)
)

NegativeMarks = (
    (0,0),
    (0.33,0.33),
    (0.33,0.33)
)

Category = (
    ('GENERAL','GENERAL'),
    ('OBC(NCL)','OBC(NCL)'),
    ('EWS','EWS'),
    ('SC','SC'),
    ('ST','ST'),
    ('PWD','PWD'),
)

class UgcNetExam(models.Model):
    name = models.CharField(null=False,max_length=60)
    subject = models.CharField(null=False,max_length=60)
    shift = models.CharField(choices=ExamShift,null=False,max_length=50)
    session = models.CharField(choices=ExamSession,null=False,max_length=50)
    year = models.IntegerField(null=False)



class UgcNetAnswerKey(models.Model):
    ugcnetexam = models.ForeignKey(UgcNetExam,on_delete=models.CASCADE,null=False)
    question_id = models.CharField(null=False,max_length=30)
    answer = models.CharField(max_length=10,null=False)
    paper = models.IntegerField(null=False,choices=ExamPaper)
    positive_marks = models.IntegerField(null=False,default=0)
    negative_marks = models.IntegerField(null=False,default=0)

class UgcNetStudent(models.Model):
    ugcnetexam = models.ForeignKey(UgcNetExam,on_delete=models.CASCADE,null=False)
    email = models.EmailField(null=False,default="dinesh@turingcode.in")
    mobile = models.IntegerField(null=False)
    otp = models.IntegerField(null=False)
    email_verify = models.BooleanField(default=0)
    application_no = models.CharField(max_length=50)
    candidate_name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=50)
    test_date = models.CharField(max_length=50)
    test_time = models.CharField(max_length=50)
    url = models.TextField()
    total_marks = models.IntegerField(default=0)
    question_attempted = models.IntegerField(default=0)
    correct_question = models.IntegerField(default=0)
    category = models.CharField(max_length=20,null=False)

class UgcNetExpectedCutOff(models.Model):
    ugcnetexam = models.ForeignKey(UgcNetExam,on_delete=models.CASCADE,null=False)
    category = models.CharField(null=False,max_length=50)
    jrf = models.CharField(null=False,max_length=15)
    assistant_professor = models.CharField(null=False,max_length=15)


class GateExam(models.Model):
    subject = models.CharField(null=False,max_length=255,choices=Subject)
    noofshift = models.IntegerField(null=False,default=1,choices=TotalShift)
    shift = models.CharField(null=False,max_length=10,choices=ExamShift)
    year = models.IntegerField(null=True)

    class Meta:
        unique_together = ('subject','shift')

class GateStudent(models.Model):
    exam = models.ForeignKey(GateExam,on_delete=models.CASCADE,null=False)
    name = models.CharField(null=False,max_length=100)
    email = models.CharField(null=False,max_length=100)
    subject = models.CharField(null=False,max_length=100,choices=Subject)
    shift = models.CharField(null=False,max_length=10,choices=ExamShift)
    positive_marks = models.FloatField(null=False,max_length=100,default=0)
    negative_marks = models.FloatField(null=False,max_length=100,default=0)
    total_marks = models.FloatField(null=False,max_length=100,default=0)
    attempted = models.IntegerField(null=False,default=0)
    correct = models.IntegerField(null=False,default=0)
    incorrect = models.IntegerField(null=False,default=0)
    gatescore = models.IntegerField(null=False)
    response = models.TextField()

    class Meta:
        unique_together = ('email', 'subject', 'shift')

class GateAnswerKey(models.Model):
    exam = models.ForeignKey(GateExam,on_delete=models.CASCADE,null=False)
    q_no = models.IntegerField(null=False)
    q_type = models.CharField(null=False,max_length=5,choices=QuestionType)
    answer = models.CharField(null=False,max_length=20)
    marks = models.IntegerField(null=False,choices=Marks)
    negative_marks = models.FloatField(null=False,choices=NegativeMarks)

    class Meta:
        unique_together = ('exam','q_no')

class GateQualifyMarks(models.Model):
    exam = models.ForeignKey(GateExam,on_delete=models.CASCADE,null=False)
    category = models.CharField(null=False,max_length=20,choices=Category)
    marks = models.FloatField(null=False)

class GateAIRvsMarks(models.Model):
    exam = models.ForeignKey(GateExam,on_delete=models.CASCADE,null=False)
    marks = models.IntegerField(null=False)
    min_air = models.IntegerField(null=False)
    max_air = models.IntegerField(null=False)


