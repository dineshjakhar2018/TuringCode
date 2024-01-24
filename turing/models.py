from django.db import models
from autoslug import AutoSlugField
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.core.exceptions import PermissionDenied


SubjectName = (
    ('Computer Science','Computer Science'),
    ('Paper - 1','Paper - 1'),
    ('Paper - 2','Paper - 2'),
    ('Computer Science and Applications','Computer Science and Applications'),
    ('Data Science and Artificial Intelligence','Data Science and Artificial Intelligence'),
    ('Programming and Data Structures','Programming and Data Structures'),
    ('Computer Organization & Architecture','Computer Organization & Architecture'),
    ('Theory of Computation','Theory of Computation'),
    ('Compiler Design','Compiler Design'),
    ('Database Management System','Database Management System'),
    ('Digital Logic','Digital Logic'),
    ('Computer Networks','Computer Networks'),
    ('Operating System','Operating System'),
    ('Algorithms','Algorithms'),
    ('Discrete and Engineering Mathematics','Discrete and Engineering Mathematics'),
    ('General Aptitude','General Aptitude'),
    ('Discrete Structures and Optimization','Discrete Structures and Optimization'),
    ('Computer System Architecture','Computer System Architecture'),
    ('Programming Languages and Computer Graphics','Programming Languages and Computer Graphics'),
    ('System Software and Operating System','System Software and Operating System'),
    ('Software Engineering',' Software Engineering'),
    ('Data Structures and Algorithms','Data Structures and Algorithms'),
    ('Theory of Computation and Compilers','Theory of Computation and Compilers'),
    ('Data Communication and Computer Networks','Data Communication and Computer Networks'),
    ('Artificial Intelligence (AI)','Artificial Intelligence (AI)'),
    ('Python','Python'),
)

ExamName = (
    ('GATE CS/IT','GATE CS/IT'),
    ('GATE DS&AI','GATE DS&AI'),
    ('UGC NET/JRF','UGC NET/JRF'),
)

QuestionType = (
    ('NAT','NAT'),
    ('MCQ','MCQ'),
    ('MSQ','MSQ'),
)

OptionName = (
    ('A','A'),
    ('B','B'),
    ('C','C'),
    ('D','D'),
)

Exam = (
    ('GATE','GATE'),
    ('NET','NET')
)

Paper = (
    (1,1),
    (2,2),
)
Quality = {
    (1080,1080),
    (720,720),
    (480,480),
    (360,360)
}

student_profile_img_path = 'images/'
question_path = 'images/testseries/quesiton'
option_path = 'images/testseries/options'
course_poster_path = 'images/'
testseries_poster_path = 'images/'
video_thumbnail_path = 'images/'
notes_path = 'pdf/'
video_path = 'videos/'
solution_path = "solution/"

class student(models.Model):
    name = models.CharField(max_length=80,null=False)
    email = models.EmailField(max_length=254,null=False,default='turingcodecse@gmail.com')
    password = models.CharField(max_length=100,null=False)
    otp = models.IntegerField(null=False)
    join_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    email_verify = models.BooleanField(null=False)
    status =  models.BooleanField(null=False)

    #def __str__(self):
        #show name and mobile in student_info student field 
        #return f"{self.name} {self.mobile}"
    

class student_info(models.Model):
    student = models.ForeignKey(student,on_delete=models.CASCADE,null=False)
    mobile = models.CharField(max_length=10,null=True)
    dob = models.DateField(auto_now=False, auto_now_add=False)
    address = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=50,null=True)
    profile_pic = models.FileField(upload_to=student_profile_img_path,validators=[FileExtensionValidator( ['jpg','jpeg','png']) ])
    qualification = models.CharField(max_length=200,null=True)
    #passing_year = models.CharField(max_length=200,null=True)

    def __str__(self):
        return f"Image {self.id}"

class testseries(models.Model):
    title = models.CharField(max_length=200,null=False)
    price = models.IntegerField(null=False)
    total_price = models.IntegerField(null=False)
    poster = models.FileField(upload_to=testseries_poster_path,validators=[FileExtensionValidator( ['jpg','jpeg','png']) ])
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
    #expire_date  = models.DateField(auto_now=False, auto_now_add=False)
    validity = models.IntegerField(null=False)
    about = models.TextField()
    exam = models.CharField(max_length=60,null=False,choices=Exam,default='GATE')
    status = models.BooleanField(null=False)
    slug = AutoSlugField(populate_from='title',null=True,unique=True,default=None)

    #def __str__(self):
        #show id and title in test testseries field 
        #return f"{self.id} {self.title} {self.price}"

class course(models.Model):
    name = models.CharField(max_length=150,null=False)
    price = models.IntegerField(null=False)
    total_price = models.IntegerField(null=False)
    date = models.DateField(auto_now=False, auto_now_add=True)
    exam_for = models.CharField(max_length=50,choices=ExamName)
    poster = models.FileField(upload_to=course_poster_path,validators=[FileExtensionValidator( ['jpg','jpeg','png']) ])
    about = models.TextField()
    #expire_date = models.DateField(auto_now=False, auto_now_add=False)
    testseries = models.ForeignKey(testseries,null=True,blank=True,on_delete=models.DO_NOTHING)
    validity = models.IntegerField(null=False)
    status = models.BooleanField(null=False)
    slug = AutoSlugField(populate_from='name',null=True,unique=True,default=None)
    
class video_package(models.Model):
    package_name = models.CharField(max_length=200,null=False)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    status = models.BooleanField(null=False)
    slug = AutoSlugField(populate_from='package_name',null=True,unique=True,default=None)

    #def __str__(self):
        #show id and package name and in videos student field 
        #return f"{self.id} {self.package_name}"

class videos(models.Model):
    video_package = models.ForeignKey(video_package, on_delete=models.CASCADE)
    title = models.CharField(max_length=200,null=False)
    subject_name = models.CharField(max_length=60,null=False,choices=SubjectName)
    file_name = models.FileField(upload_to=video_path,validators=[FileExtensionValidator( ['mp4']) ])
    thumbnail = models.FileField(upload_to=video_thumbnail_path,validators=[FileExtensionValidator( ['jpg','jpeg','png']) ])
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    premium = models.BooleanField(null=False)
    video_length = models.CharField(null=False,max_length=20)
    status = models.BooleanField(null=False)
    video_no = models.IntegerField(null=False,default = 0)
    quality = models.IntegerField(null=False,choices=Quality)
    slug = AutoSlugField(populate_from='title',null=True,unique=True,default=None)

class duplicate_video(models.Model):
    video = models.ForeignKey(videos,on_delete=models.CASCADE)
    file_name = models.FileField(upload_to=video_path,validators=[FileExtensionValidator( ['mp4']) ])
    quality = models.IntegerField(null=False,choices = Quality)
    slug = AutoSlugField(populate_from='file_name',null=True,unique=True,default=None)

class WatchHistory(models.Model):
    student_id = models.ForeignKey(student, on_delete=models.CASCADE)
    video_id = models.ForeignKey(videos, on_delete=models.CASCADE)
    watch_time = models.IntegerField(default=0)  # in seconds
    current_status = models.CharField(max_length=50, blank=True, null=True)


class test(models.Model):
    testseries = models.ForeignKey(testseries, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=200,null=False)
    total_question = models.IntegerField(null=False)
    duration = models.IntegerField(null=False)
    total_marks = models.IntegerField(null=False)
    no_of_paper = models.IntegerField(null=False,choices=Paper,default='1')
    report_status = models.BooleanField(null=False)
    premium = models.BooleanField(null=False)
    total_question_in_paper_1 = models.IntegerField(default=0,null=False)
    total_question_in_paper_2 = models.IntegerField(default=0,null=False)
    status = models.BooleanField(null=False)
    difficulty_level = models.IntegerField(null=True)
    mode_rate_level = models.IntegerField(null=True)
    easy_level = models.IntegerField(null=True)
    slug = AutoSlugField(populate_from='test_name',null=True,unique=True,default=None)

    #def __str__(self):
        #show id and test name and question in question in test  field 
        #return f"{self.id} {self.test_name} {self.total_question} {self.total_marks}"

    '''def save(self, *args, **kwargs):
        questions_sum = question.objects.filter(test=self).aggregate(total_marks=models.Sum('positive_marks'))['total_marks']
        question_count = question.objects.filter(test=self).count()
        has_false_status = question.objects.filter(test=self, status=False).exists()

        if (questions_sum != self.total_marks or question_count != self.total_question or has_false_status):
            pass
            #self.status = 0

        super().save(*args, **kwargs)'''
   

class question(models.Model):
    test = models.ForeignKey(test, on_delete=models.CASCADE)
    paper_name = models.CharField(max_length=200,null=False,choices=SubjectName)
    question_no = models.IntegerField(null=False)
    question_time = models.IntegerField(null=False)
    #question_img = models.FileField(upload_to=question_path,validators=[FileExtensionValidator( ['jpg','jpeg','png']) ])
    question_text = models.TextField()
    positive_marks = models.IntegerField(null=False)
    negative_marks = models.CharField(null=False,max_length=20)
    question_type = models.CharField(max_length=20,null=False,choices=QuestionType)
    paper = models.IntegerField(null=False,choices=Paper,default=1)
    status  = models.BooleanField(null=False)
    nat_range = models.BooleanField(null=False,default=False)
    nat_round_decimal_digit = models.IntegerField(null=False,default=0) 
    slug = AutoSlugField(populate_from='question_no',null=True,unique=True,default=None)

    '''class Meta:
        unique_together = ('test', 'question_no','paper')

    def clean(self):
        if self.question_type in ['MCQ', 'MSQ']:
            option_count = question_options.objects.filter(question=self).count()
            if option_count != 4:
                self.status = '0'

        super().clean()

    def save(self, *args, **kwargs):
        if not question_answer.objects.filter(question=self).exists():
            self.status = '0'
        
        super().save(*args, **kwargs)
    

    # Fields and relationships for Question model
    def delete(self, *args, **kwargs):
        if self.test.status == 1:
            raise PermissionDenied("Cannot delete a question when there is an associated test with status 1.")

        super().delete(*args, **kwargs)'''


class question_options(models.Model):
    question = models.ForeignKey(question, on_delete=models.CASCADE)
    question_no = models.IntegerField(null=False)
    option_name = models.CharField(max_length=255,choices=OptionName)
    #option_img = models.FileField(upload_to=option_path,validators=[FileExtensionValidator( ['jpg','jpeg','png']) ])
    option = models.TextField()

    class Meta:
        unique_together = ('question', 'question_no','option_name')

class question_answer(models.Model):
    question = models.ForeignKey(question, on_delete=models.CASCADE)
    question_no = models.IntegerField(null=False)
    answer = models.CharField(max_length=20,null=False)

class student_answer(models.Model):
    test = models.ForeignKey(test, on_delete=models.CASCADE)
    question = models.ForeignKey(question, on_delete=models.CASCADE)
    student = models.ForeignKey(student, on_delete=models.CASCADE)
    question_no = models.IntegerField(null=False)
    answer = models.CharField(max_length=30,null=False)
    time_taken = models.IntegerField(null=False)
    visited = models.BooleanField(null=False)
    paper = models.IntegerField(choices=Paper,default=1)
    markforreview = models.BooleanField(null=False)
    answer_result = models.CharField(null=False,default='UnAttempted',max_length=25)

class test_status(models.Model):
    test = models.ForeignKey(test, on_delete=models.CASCADE)
    student = models.ForeignKey(student, on_delete=models.CASCADE)
    current_question_paper_1 = models.IntegerField(null=False)
    current_question_paper_2 = models.IntegerField(null=False)
    incomplete = models.BooleanField(null=False)
    completed = models.BooleanField(null=False)
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
    total_time = models.IntegerField(null=False)
    use_time = models.IntegerField(null=False)
    rank = models.IntegerField(null=False)
    total_marks = models.CharField(max_length=30,null=False)
    current_paper = models.IntegerField(default=1,null=False)
    #total_attempted = models.IntegerField(default=0,null=False)
    #leftQuestion = models.IntegerField(default=0,null=False)
    #correct_question = models.IntegerField(default=0,null=False)
    #incorrect_question = models.ImageField(default=0,null=False)
    #time_taken = models.CharField(null=False,max_length=20,default="00:00:00")
    #percentage = models.CharField(null=False,max_length=20,default='0')
    #positive_marks = models.IntegerField(null=False,default=0)
    #negative_marks = models.IntegerField(null=False,default=0)

    class Meta:
        unique_together = ('test', 'student')

class notes_package(models.Model):
    name = models.CharField(max_length=150,null=False)
    date =  models.DateTimeField(auto_now=False, auto_now_add=False)
    exam_for = models.CharField(max_length=150,null=False,choices=ExamName)
    premium = models.BooleanField(null=False)
    status = models.BooleanField(null=False)
    slug = AutoSlugField(populate_from='name',null=True,unique=True,default=None)

class notes(models.Model):
    notes_package = models.ForeignKey(notes_package, on_delete=models.CASCADE)
    title = models.CharField(max_length=255,null=False)
    subject_name = models.CharField(max_length=150,null=False,choices=SubjectName)
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
    file_name = models.FileField(upload_to=notes_path,validators=[FileExtensionValidator( ['pdf']) ])
    premium = models.BooleanField(null=False)
    status = models.BooleanField(null=False)
    slug = AutoSlugField(populate_from='title',null=True,unique=True,default=None)

class course_video(models.Model):
    video_package = models.ForeignKey(video_package, on_delete=models.CASCADE)
    course = models.ForeignKey(course, on_delete=models.CASCADE)
    status = models.BooleanField(null=False)

    class Meta:
        unique_together = ('video_package', 'course')

'''
class course_testseries(models.Model):
    testseries = models.ForeignKey(testseries,on_delete=models.CASCADE)
    course = models.ForeignKey(course, on_delete=models.CASCADE)
    status = models.BooleanField(null=False)

    class Meta:
        unique_together = ('testseries', 'course')
'''

class course_notes(models.Model):
    notes_package = models.ForeignKey(notes_package,on_delete=models.CASCADE)
    course = models.ForeignKey(course, on_delete=models.CASCADE)
    status = models.BooleanField(null=False)

    class Meta:
        unique_together = ('notes_package', 'course')

CourseStatus = (
    ('Success','Success'),
    ('Pending','Pending'),
    ('Expire','Expire'),
    ('Failed','Failed'),
)
class course_enroll(models.Model):
    course = models.ForeignKey(course,on_delete=models.CASCADE,null=False)
    student = models.ForeignKey(student,on_delete=models.CASCADE,null=False)
    datetime = models.DateTimeField(null=True,auto_now_add=False)
    order_id = models.CharField(null=False,max_length=30,default='ORDS569845')
    #txn_id = models.CharField(null=False,max_length=50,default='TXN24568955')
    amount = models.CharField(null=False,max_length=20,default='5000')
    remaning_days = models.IntegerField(null=False,default=0)
    validity = models.IntegerField(null=False,default=0)
    status = models.CharField(null=False,max_length=20,default='Pending',choices=CourseStatus)


class testseries_enroll(models.Model):
    testseries = models.ForeignKey(testseries,on_delete=models.CASCADE,null=False)
    student = models.ForeignKey(student,on_delete=models.CASCADE,null=False)
    datetime = models.DateTimeField(null=True,auto_now_add=False)
    order_id = models.CharField(null=False,max_length=30,default='ORDS569845')
    #txn_id = models.CharField(null=False,max_length=50,default='TXN24568955')
    amount = models.CharField(null=False,max_length=20)
    remaning_days = models.IntegerField(null=False,default=0)
    validity = models.IntegerField(null=False,default=0)
    status = models.CharField(null=False,max_length=20,default='Pending',choices=CourseStatus)

    class Meta:
        unique_together = ('testseries', 'student')

class TestInstruction(models.Model):
    exam = models.CharField(max_length=60,null=False,choices=Exam)
    instruction_1 = models.TextField()
    instruction_2 = models.TextField()

class Feedback(models.Model):
    student = models.ForeignKey(student,on_delete=models.CASCADE,null=True)
    test = models.ForeignKey(test,on_delete=models.CASCADE,null=True)
    feedback = models.TextField()

SolutionType = (
    ('Video','Video'),
    ('Image','Image'),
)

class question_solution(models.Model):
    question = models.ForeignKey(question,on_delete=models.CASCADE,null=False)
    question_no = models.IntegerField(null=False)
    solution_type = models.CharField(max_length=255,null=False,choices=SolutionType)
    solution = models.FileField(null=True,upload_to=solution_path,validators=[FileExtensionValidator( ['jpg','jpeg','png','mp4'])])
    #text_solution = HTMLField(default='Not Found')

    class Mets:
        unique_together = ('question','question_no','solution_type')

class student_test_status(models.Model):
    test_status = models.ForeignKey(test_status,on_delete=models.CASCADE,null=False)
    test = models.ForeignKey(test,on_delete=models.CASCADE,null=False)
    student = models.ForeignKey(student,on_delete=models.CASCADE,null=False)
    accuracy = models.FloatField(null=False)
    attempted_question = models.IntegerField(null=False)
    correct_question = models.IntegerField(null=False)
    incorrect_question = models.IntegerField(null=False)
    left_question = models.IntegerField(null=False)

    class Meta:
        unique_together = ('test_status','test','student')

class PromotionalVideo(models.Model):
    caption = models.CharField(max_length=255,null=False)
    video = models.FileField(upload_to='videos/promotion/',validators=[FileExtensionValidator( ['mp4']) ])
    thumbnail = models.FileField(upload_to='images/',validators=[FileExtensionValidator( ['jpeg','jpg','png'])])
    status = models.BooleanField(null=False)

class IndexContent(models.Model):
    logo = models.FileField(upload_to='images/',validators=[FileExtensionValidator( ['jpeg','jpg','png'])])
    poster = models.FileField(upload_to='images/',validators=[FileExtensionValidator( ['jpeg','jpg','png'])])
    status = models.BooleanField(default=0,null=False)

class AboutUs(models.Model):
    about = models.TextField()
    status = models.BooleanField(default=0,null=False)


class ContactForm(models.Model):
    name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=80,null=False)
    query = models.TextField()

