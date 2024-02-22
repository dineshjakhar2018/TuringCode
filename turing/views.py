from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import student,course,testseries,videos,course_video,notes,course_notes,test,notes_package,course_enroll,student_info,testseries_enroll,TestInstruction,test_status,student_answer,question,question_options,question_answer,Feedback,student_test_status,PromotionalVideo,IndexContent,AboutUs,ContactForm,duplicate_video,WatchHistory
from django.http import HttpResponse
from django.template import loader
import re,random,datetime
from .decorators import login_required, anonymous_required
from django.db.models import Count,Max
from datetime import date
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Q, Subquery, OuterRef
from django.db.models import F, FloatField
from django.db.models.functions import Cast
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.http import StreamingHttpResponse
import subprocess
import requests
from django.core.files.storage import FileSystemStorage
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import razorpay
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def index(request):
    try:
        Courses = course.objects.filter(status = 1).order_by('-id')
        TestSeries = testseries.objects.filter(status = 1).order_by('-id')
        Content = IndexContent.objects.filter(status=1).order_by('-id').first()
        return render(request, 'index.html',{'Courses' : Courses,'TestSeries' : TestSeries,'Content' : Content})
    except:
        return render(request,'index.html')


def About_US(request):
    AboutContent = AboutUs.objects.get(status=1)
    return render(request, 'about.html',{'AboutContent' : AboutContent})

def ContactUs(request):
    return render(request,'contact.html')

def Contact_Form(request):
    try:
        if request.method == 'POST':
            name = request.POST.get('Name')
            mobile = request.POST.get('Mobile')
            query = request.POST.get('Query')
            
            if len(name) == 0:
                messages.error(request,"Name is required")
                error = 1
            elif not re.match(r'^[ a-zA-Z]+$', name):
                messages.error(request,"Only alphabetic characters are allowed in the name")
                error = 1
            
            if not mobile.isdigit() or len(mobile) != 10:
                messages.error(request,'Invalid Mobile Number')

            else:
                Form = ContactForm(name=name,mobile=mobile,query=query)
                Form.save()
                messages.success(request,'Your query send successfully.')
        return render(request, 'contact.html')
    except:
        return redirect('contact_us')

def pyp(request,exam_name):
    try:
        gate_cs_pyq = testseries.objects.get(slug=exam_name)
        return render(request,'pyp.html',{'exam' :gate_cs_pyq})
    except:
        return redirect('')

def pyp_solution(request,test_slug):
    try:
        Test = test.objects.get(slug=test_slug)
        Questions = question.objects.filter(test_id=Test.id).order_by('question_no')
        return render(request,'pyp-solution.html',{'test':Test,'questions':Questions})
    except:
        pass

def Test_Series_Content(request,testseries_slug):
    try:
        TestSeries = testseries.objects.get(slug=testseries_slug)
        Tests = test.objects.filter(testseries_id = TestSeries.id)
        #Test_Features = TestFeature.objects.filter(status = 1)
        return render(request, 'test-series-content.html',{'TestSeries':TestSeries,'Tests' : Tests,'Title' : TestSeries.title,'About' : TestSeries.about})
    except:
        return render(request, 'test-series-content.html')#return 404

def TermsAndCondition(request):
    return render(request,'terms&conditions.html')

def RefundPolicy(request):
    return render(request,'refund.html')

def PrivacyPolicy(request):
    return render(request,'privacy_policy.html')

def Course_Content(request,course_slug):
    try:
        courses = course.objects.get(slug = course_slug)
        course_id = courses.id

        queryset = videos.objects.filter(
            status=1,
            video_package_id__in=list(
                course_video.objects.filter(course_id=course_id, status=1).values_list("video_package_id", flat=True)
            )
        )

        video_subjects = list(videos.objects.filter(
                status=1,
                video_package_id__in=list(
                    course_video.objects.filter(course_id=course_id, status=1).values_list("video_package_id", flat=True)
                )
            ).values_list("subject_name", flat=True)
        )
        
        notes_list = notes.objects.filter(
            status=1,
            notes_package_id__in=list(
                course_notes.objects.filter(course_id=course_id, status=1).values_list("notes_package_id", flat=True)
            )
        )

        notes_subject = list(notes.objects.filter(
            status=1,
            notes_package_id__in=list(
                course_notes.objects.filter(course_id=course_id, status=1).values_list("notes_package_id", flat=True)
            )
         ).values_list("subject_name", flat=True)
        )

        subjects = list(set(video_subjects + notes_subject))


        return render(request, 'course-content.html',{'courses' : courses,'videos' : queryset,'subjects' : subjects,'notes' : notes_list,'CourseName' : courses.name })

    except:
        return redirect('courses')#remember to redicrect to 404






#user panel start here
@anonymous_required
def login(request):
     # Clear the session data for the current user
    request.session.clear()

    #if post is set
    if request.method == 'POST':
        email = request.POST.get("Email")
        password = request.POST.get("Password")

        try:
            students = student.objects.get(email=email)

            if students.email == email and students.password == password and students.email_verify == 1:
                request.session['email'] = email
                return redirect('home')
            
            elif students.email == email and students.password == password and students.email_verify == 0:
                otp = random.randrange(100000,999999)
                students.otp = otp 
                students.save()
                request.session['email'] = email
                send_email('Account Registration - Email Verification',email,'email-verify','None')
                return redirect('email-verify')
            
            else:
                messages.error(request, 'Invalid email address and password')
                template = loader.get_template('login.html')
                context = {'email' : email, 'password' : password}
                return HttpResponse(template.render(context,request))
                #return render(request, 'login.html', {'mobile': mobile, 'password': password})
        
        except:
            messages.error(request, 'Invalid email address')
            return render(request, 'login.html', {'email': email, 'password': password})

    return render(request, 'login.html')

def validate_email(email):
    pattern = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    return True if re.match(pattern, email) else False

def register(request):
    # Clear the session data for the current user
    request.session.clear()

    #if post is set
    if request.method == 'POST':
        fullname = request.POST.get('Fullname')
        email = request.POST.get('Email')
        password = request.POST.get('Password')
    
        try:
            error = 0 #initially error is 0

            if validate_email(email) == False:
                messages.error(request,'Invalid Email Address')
                error = 1

            if len(password) < 6:
                messages.error(request, "Password must be at least 6 characters long")
                error = 1

            if len(fullname) == 0:
                messages.error(request,"Fullname is required")
                error = 1
            elif not re.match(r'^[ a-zA-Z]+$', fullname):
                messages.error(request,"Only alphabetic characters are allowed in the fullname")
                error = 1

            if error:
                return render(request, 'register.html',{'fullname' : fullname,'email' : email,'password':password})
            else:
                students = student.objects.get(email=email)
                if student.objects.get(email=email):#it is true means student already registered
                    messages.error(request,'Email address already exist')
                    return render(request, 'register.html',{'fullname' : fullname,'email' : email,'password':password})
                
        except student.DoesNotExist: #if student not exist
                #otp for mobile verification
                otp = random.randrange(100000,999999)
                current_datetime = datetime.datetime.now()
                current_datetime_str = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
                try:
                    students = student(name=fullname,email=email,password=password,otp = otp,join_date = current_datetime_str,email_verify=0,status=1)
                    students.save()

                    request.session['email'] = email
                    send_email('Account Registration - Email Verification',email,'email-verify','None')
                    return redirect('email-verify')
                except:
                    messages.error(request,'Something went wrong please try again later')
                    return render(request, 'register.html',{'fullname' : fullname,'email' : email,'password':password})
        except:
            messages.error(request,'Something went wrong please try again later')
            return render(request, 'register.html',{'fullname' : fullname,'email' : email,'password':password})


    return render(request, 'register.html')

def email_verify(request):
    email = request.session.get('email')
    if email:
        students = student.objects.get(email=email)
        if request.method == 'POST':
            otp = request.POST.get('Otp')
            if str(students.otp) == otp:
                messages.success(request,'congratulations, your account has been successfully created.')
                students.email_verify = 1
                students.save()
                request.session.clear()
                request.session['email'] = email
                #registration success email send
                send_email('Welcome to Turing Code - Registration Successful!',email,'register-success','None')
                return redirect('home')
            else:
                messages.error(request, 'Invalid Otp please enter valid otp')
                return render(request, 'email-verify.html')
        else:
            return render(request,'email-verify.html')
        
    return redirect('login')

def otp_resend(request):
    email = request.session.get('email')
    if email:
        # regenrate otp for email verification
        otp = random.randrange(100000,999999)
        students = student.objects.get(email=email)
        students.otp = otp
        students.save()
        #resend otp email 
        send_email('Account Registration - Resending OTP for Email Verification',email,'email-verify-resend','None')
        messages.success(request,'OTP resent successfully to your email address.')
        
        return redirect('email-verify')
    
    messages.error(request,'Failed to resend OTP. Please try again later.')
    return redirect('email-verify')



def forgot(request):
    # Clear the session data for the current user
    request.session.clear()
    
    #if post is set
    if request.method == 'POST':
        email = request.POST.get('Email')
        students = None
        try:
            students = student.objects.get(email=email)
            if students is None:
                messages.error(request,'Please check the email address and try again')
                return render(request,'forgot-1.html')
            else:
                otp = random.randrange(100000,999999)
                students.otp = otp
                students.save()
                request.session['email'] = email
                send_email(' Password Reset OTP - Turing Code',email,'reset-password','None')
                return redirect('forgot-verify')

        except:
            if students is None:
                messages.error(request,'Please check the email address and try again')
                return render(request,'forgot-1.html')
            else:
                messages.error(request,'Something went wrong please try again later')
                return render(request,'forgot-1.html')
        
    return render(request, 'forgot-1.html')


def forgot_verify(request):
    email = request.session.get('email')
    if email:
        students = student.objects.get(email=email)
        if request.method == 'POST':
            otp = request.POST.get('Otp')
            if str(students.otp) == otp:
                return redirect('forgot-pass')
            else:
                messages.error(request, 'Invalid Otp please enter valid otp')
                return render(request, 'forgot-2.html')
        else:
            return render(request,'forgot-2.html')
        
    return render('forgot')

def forgot_otp_resend(request):
    email = request.session.get('email')
    if email:
        # regenrate otp for email verification
        otp = random.randrange(100000,999999)
        students = student.objects.get(email=email)
        students.otp = otp
        students.save()
        messages.success(request,'OTP resent successfully to your email address.')
        send_email('Password Reset OTP - Turing Code',email,'reset-password','None')
        return redirect('forgot-verify')
    
    messages.error(request,'Failed to resend OTP. Please try again later.')
    return redirect('forgot-verify')

def forgot_pass(request):
    email = request.session.get('email')
    students = None
    try:
        if email:
            students = student.objects.get(email=email)

            if request.method == 'POST':
                password = request.POST.get('Password')
                confirm_password = request.POST.get('ConfirmPassword')

                if len(password) < 6:
                    messages.error(request,'Password must be at least 6 characters long')
                    return render(request, 'forgot-3.html')
                elif password != confirm_password:
                    messages.error(request,'Passwords do not match.')
                    return render(request, 'forgot-3.html')
                else:
                    students.password = password
                    students.save()
                    messages.success(request, 'Password changed successfully.')
                    request.session.clear()
                    return redirect('login')
            else:
                return render(request, 'forgot-3.html')
    except:
        if students is None:
            messages.error(request,'Please check the email address and try again')
            return redirect('forgot')
        else:
            messages.error(request,'Something went wrong please try again later')
            return render(request, 'forgot-3.html')
    
    return redirect('login')

def logout(request):
    request.session.clear()
    return redirect('login')



@login_required
def home(request):
    try:
        Student = student.objects.get(email=request.session.get('email'))
        video = PromotionalVideo.objects.get(status=1)
        EnrollCourses = course_enroll.objects.filter(student_id=Student.id,status='Success')
        EnrollTestSeries = testseries_enroll.objects.filter(student_id=Student.id)

        #course validity update
        try:
            CourseEnroll = course_enroll.objects.filter(student_id=Student.id,status='Success')
            for item in CourseEnroll:
                #calculate validity (remaning days)
                current_date = date.today()
                past_date = item.datetime.date()
                days_difference = (current_date - past_date).days
                #calculate remaning days
                validity = item.validity - days_difference
                if item.remaning_days >= 0:
                    item.remaning_days = validity
                    item.save()
        except:
            pass

        #test series validity update
        try:
            TestSeriesEnroll = testseries_enroll.objects.filter(student_id=Student.id)
            for item in TestSeriesEnroll:
                #calculate validity (remaning days)
                current_date = date.today()
                past_date = item.datetime.date()
                days_difference = (current_date - past_date).days
                #calculate remaning days
                validity = item.validity - days_difference
                if item.remaning_days >= 0:
                    item.remaning_days = validity
                    item.save()
        except:
            pass
        return render(request,'home.html',{'StudentName' : Student.name,'student':Student,'video' : video,'EnrollCourses' : EnrollCourses,'EnrollTestSeries' :  EnrollTestSeries})
    except Exception as e:
        print("home page error occur due to ",e)
        return render(request,'home.html',{'student':Student})

@login_required
def courses(request):
    not_enrolled_courses = [] 
    email = request.session.get('email')
    Student = student.objects.get(email=email)
    try:
        # Get IDs of courses enrolled by the logged-in student
        enrolled_course_ids = course_enroll.objects.filter(student_id=Student.id,status='Success').values_list('course_id', flat=True).order_by('-id')
        
         # Query for active courses not enrolled by the student
        not_enrolled_courses = course.objects.filter(status=1).exclude(id__in=enrolled_course_ids).order_by('-id')

        try:
            CourseEnroll = course_enroll.objects.filter(student_id=Student.id,status='Success')
            for item in CourseEnroll:
                #calculate validity (remaning days)
                current_date = date.today()
                past_date = item.datetime.date()
                days_difference = (current_date - past_date).days
                #calculate remaning days
                validity = item.validity - days_difference
                if item.remaning_days >= 0:
                    item.remaning_days = validity
                    item.save()
        except:
            pass

        return render(request,'courses.html',{'not_enrolled_courses':not_enrolled_courses,'enroll_courses' : CourseEnroll,'StudentName' : Student.name,'student':Student})
    except:
        CourseEnroll = []
        return render(request,'courses.html',{'not_enrolled_courses':not_enrolled_courses,'enroll_courses' : CourseEnroll,'StudentName' : Student.name,'student':Student})

@login_required
def course_details(request,course_slug):
    try:
        courses = course.objects.get(slug = course_slug)
        course_id = courses.id

        queryset = videos.objects.filter(
            status=1,
            video_package_id__in=list(
                course_video.objects.filter(course_id=course_id, status=1).values_list("video_package_id", flat=True)
            )
        )

        # Order the queryset by the 'video_no' field
        queryset = queryset.order_by('video_no')


        '''
        Group_by
        subjects = videos.objects.filter(
                status=1,
                video_package_id__in=list(
                    course_video.objects.filter(course_id=course_id, status=1).values_list("video_package_id", flat=True)
                )
            ).values('subject_name').annotate(video_count=Count('id'))
        '''
        #filter 
        video_subjects = list(videos.objects.filter(
                status=1,
                video_package_id__in=list(
                    course_video.objects.filter(course_id=course_id, status=1).values_list("video_package_id", flat=True)
                )
            ).values_list("subject_name", flat=True)
        )
        
        notes_list = notes.objects.filter(
            status=1,
            notes_package_id__in=list(
                course_notes.objects.filter(course_id=course_id, status=1).values_list("notes_package_id", flat=True)
            )
        )

        notes_subject = list(notes.objects.filter(
            status=1,
            notes_package_id__in=list(
                course_notes.objects.filter(course_id=course_id, status=1).values_list("notes_package_id", flat=True)
            )
         ).values_list("subject_name", flat=True)
        )

        subjects = list(set(video_subjects + notes_subject))


        #enroll list of all enroll course by a particular student
        enroll = ['Not Enroll']#if student not enroll in this course then list first item is Not Enroll
        try:
            students = student.objects.get(email=request.session.get('email'))
            #retrive max id because fetch latest enroll (some time renew course then fetch latest records)
            enroll_details = course_enroll.objects.get(student_id=students.id,course_id=course_id,status='Success')
            
            #calculate course validity in days
            course_enrolled_date = enroll_details.datetime.date()
            if course_enrolled_date:
                current_date = date.today()
                past_date = course_enrolled_date
                days_difference = (current_date - past_date).days
                #calculate remaning days
                validity = enroll_details.validity - days_difference
                enroll = ['Enrolled',validity] #if student enrolled in this course then first item is Enrolled and second item is Remaning Days 
            return render(request, 'course-details.html',{'courses' : courses,'videos' : queryset,'subjects' : subjects,'notes' : notes_list,'enroll':enroll,'StudentName' : students.name,'student':students})
        
        except:
            students = student.objects.get(email=request.session.get('email'))
            return render(request, 'course-details.html',{'courses' : courses,'videos' : queryset,'subjects' : subjects,'notes' : notes_list,'enroll':enroll,'StudentName' : students.name,'student':students})
    

    except:
        return redirect('courses')#remember to redicrect to 404

@login_required
def play_video(request,course_slug,video_slug):
    try:
        courses = course.objects.get(slug = course_slug)
        video = videos.objects.get(slug=video_slug)
        duplicate_videos = 10
        try:
            duplicate_videos = duplicate_video.objects.filter(video = video.id)
        except:
            pass

        premium = video.premium
        course_id = courses.id
        video_list = videos.objects.filter(
            status=1,subject_name=video.subject_name,
            video_package_id__in=list(
                course_video.objects.filter(course_id=course_id, status=1).values_list("video_package_id", flat=True)
            )
        )

        #video order by based on 'video_no' field
        video_list = video_list.order_by('video_no')

        
        enroll = ['Not Enroll']
        #check video is demo video or if not demo then only watch only enrolled student
        try:
                #if student enrolled in this course then execute this portion (try)
                #retrive current login student
                students = student.objects.get(email=request.session.get('email'))

                #fetch enroll details if student is already enroll in this course
                enroll_details = course_enroll.objects.get(student_id=students.id,course_id=course_id,status='Success')
                
                #calculate course validity in days
                course_enrolled_date = enroll_details.datetime.date()
                if course_enrolled_date:
                    current_date = date.today()
                    past_date = course_enrolled_date
                    days_difference = (current_date - past_date).days
                    #calculate remaning days
                    validity = courses.validity - days_difference
                    enroll = ['Enrolled',validity]
                
                if premium == 1:
                    if validity > -1:
                        #if student is enrolled in this course and  course is not expire
                        return render(request, 'play-video.html', {'courses':courses,'video':video,'video_list' : video_list,'enroll':enroll,'StudentName' : students.name,'student':students,'duplicate_videos':duplicate_videos })
                    else:
                        #if course is expire
                        return redirect('courses')
                else:
                    if validity > -1:
                        #if student is enrolled in this course and  course is not expire
                        return render(request, 'play-video.html', {'courses':courses,'video':video,'video_list' : video_list,'enroll':enroll,'StudentName' : students.name,'student':students,'duplicate_videos':duplicate_videos })
                    else:
                        enroll = ['Not Enroll']
                        #if student isenrolled in this course and  course is not expire
                        return render(request, 'play-video.html', {'courses':courses,'video':video,'video_list' : video_list,'enroll':enroll,'StudentName' : students.name,'student':students,'duplicate_videos':duplicate_videos})
                    
        except:
            #if student is not enroll in this course then execute this except portion
            if premium == 1:
                #student is 
                return redirect('courses')
            else:
                #if student is enrolled in this course and  course is not expire
                #reuse enroll because some time other error in try portion (execute enroll then create problem)
                Student = student.objects.get(email=request.session.get('email'))
                enroll = ['Not Enroll'] 
                return render(request, 'play-video.html', {'courses':courses,'video':video,'video_list' : video_list,'enroll':enroll,'StudetName' : Student.name,'student':Student,'duplicate_videos':duplicate_videos})
    except:
        return redirect('courses')

@login_required
def view_notes(request,course_slug,notes_slug):
    try:
        courses = course.objects.get(slug = course_slug)
        note_view = notes.objects.get(slug=notes_slug)
        course_id = courses.id
        premium = note_view.premium
        notes_list = notes.objects.filter(
            status=1,subject_name=note_view.subject_name,
            notes_package_id__in=list(
                course_notes.objects.filter(course_id=course_id, status=1).values_list("notes_package_id", flat=True)
            )
        )


        enroll = ['Not Enroll']
        #check video is demo video or if not demo then only watch only enrolled student
        try:
                #if student enrolled in this course then execute this portion (try)
                #retrive current login student
                students = student.objects.get(email=request.session.get('email'))

                #retrive course enroll details if student is enroll in this course
                enroll_details = course_enroll.objects.get(student_id=students.id,course_id=course_id,status='Success')
                
                #calculate course validity in days
                course_enrolled_date = enroll_details.datetime.date()
                if course_enrolled_date:
                    current_date = date.today()
                    past_date = course_enrolled_date
                    days_difference = (current_date - past_date).days
                    #calculate remaning days
                    validity = enroll_details.validity - days_difference
                    enroll = ['Enrolled',validity]
                
                if premium == 1:
                    if validity > -1:
                        #if student is enrolled in this course and  course is not expire
                        return render(request, 'notes-view.html', {'courses':courses,'notes':note_view,'notes_list' : notes_list,'enroll' : enroll, 'StudentName' : students.name,'student':students})
                    else:
                        #if course is expire
                        return redirect('courses')
                else:
                    if validity > -1:
                        #if student is enrolled in this course and  course is not expire
                        return render(request, 'notes-view.html', {'courses':courses,'notes':note_view,'notes_list' : notes_list,'enroll' : enroll, 'StudentName' : students.name,'student':students})
                    else:
                        enroll = ['Not Enroll']
                        #if student is enrolled in this course and  course is not expire
                        return render(request, 'notes-view.html', {'courses':courses,'notes':note_view,'notes_list' : notes_list,'enroll' : enroll, 'StudentName' : students.name,'student':students})
                    
        except:
            #if student is not enroll in this course then execute this except portion
            if premium == 1:
                #student is 
                return redirect('courses')
            else:
                #if student is enrolled in this course and  course is not expire
                #reuse enroll because some time other error in try portion (execute enroll then create problem)
                Student = student.objects.get(email=request.session.get('email'))
                enroll = ['Not Enroll'] 
                return render(request, 'notes-view.html', {'courses':courses,'notes':note_view,'notes_list' : notes_list,'enroll' : enroll, 'StudentName' : Student.name,'student':Student})

    except:
        return redirect('courses')



#free notes code start here
@login_required
def notes_(request):
    try:
        Student = student.objects.get(email = request.session.get('email'))
        notes_list = notes_package.objects.filter(premium=0)
        return render(request,'notes.html',{'notes': notes_list,'StudentName' : Student.name,'student':Student})
    except Exception as e:
        print("notes error = ",e)
        return redirect('home')#return 404
    

@login_required
def notes_list(request,notes_package_slug):
    try :
        exam = notes_package.objects.get(slug=notes_package_slug)
        notes_list = notes.objects.filter(premium=0,notes_package_id=exam.id,status=1)
        subject_list = list(set(notes.objects.filter(premium=0,notes_package_id=exam.id,status=1).values_list("subject_name", flat=True)))
        Student = student.objects.get(email = request.session.get('email'))
        return render(request, 'notes-list.html', {'exam' : exam, 'notes' : notes_list,'subjects': subject_list,'StudentName' : Student.name,'student':Student})
    except:
        return redirect('notes')#return 404

@login_required
def view_free_notes(request,notes_package_slug,notes_slug):
    try :
        exam = notes_package.objects.get(slug=notes_package_slug)
        pdf = notes.objects.get(premium=0,slug=notes_slug,status=1)
        notes_list = notes.objects.filter(premium=0,notes_package_id=exam.id,status=1,subject_name=pdf.subject_name)
        Student = student.objects.get(email = request.session.get('email'))
        return render(request, 'notes-view-1.html', {'exam' : exam, 'pdf' : pdf,'notes_list': notes_list,'StudentName' : Student.name,'student':Student})
    except:
        return redirect('notes')#rediret to 404

#free notes code end here

@login_required
def checkout(request,slug_1,slug_2):
    #slug_1 represent either coure or test-series
    #slug_2 if course then course slug or if test-series then testseries_slug
    try:
        #retrive student id
        email = request.session.get('email')
        students = student.objects.get(email=email)

        #current date and time
        current_datetime = datetime.datetime.now()
        current_datetime_str = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        
        if slug_1 == 'course':
            courses = course.objects.get(slug=slug_2)
            price = courses.price
            total_price = courses.total_price
            discount = total_price - price

            
            #check if user already enroll and expire or not
            try:
                enroll_details = False
                #if student enrolled in this course then execute this portion (try)
                #retrive current login student
                students = student.objects.get(email=request.session.get('email'))

                #retrive enroll details if student is enrolled in this course
                enroll_details = course_enroll.objects.get(student_id=students.id,course_id=courses.id,status='Success')
                
                if enroll_details is not False:
                    return redirect('home') 
                else:
                    return render(request,'checkout.html', {'course': courses,'discount' : discount,'type' : slug_1})
                    
            except:
                amount = int(price)*100  # Convert amount to paise
                #price is grater than or equal to 1 then goto razorpay otherwise not goto razorpay
                if price >= 1:
                    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

                    # Create a Razorpay order
                    response = client.order.create({'amount': amount, 'currency': 'INR','payment_capture' : 1})


                    order_id = response['id']
                    enroll = course_enroll(course_id=courses.id,student_id=students.id,amount=int(amount/100),validity=0,datetime=current_datetime_str,order_id=order_id,status = 'Pending',remaning_days=0)
                    enroll.save()

                    return render(request,'checkout.html', {'course': courses,'discount' : discount,'type' : slug_1,'response':response,'razorpay_key_id':settings.RAZORPAY_KEY_ID,'student':students})
                else:
                    #if price is less than 1 rupees
                    order_id = 'ORDS'+str(random.randrange(10000,99999))
                    enroll = course_enroll(course_id=courses.id,student_id=students.id,amount=0,validity=courses.validity,datetime=current_datetime_str,order_id=order_id,status = 'Success',remaning_days=0)
                    enroll.save()
                    url = '/courses/course-details/'+str(courses.slug)
                    return redirect(url)

                
        elif slug_1 == 'test-series':
            TestSeries = testseries.objects.get(slug=slug_2)
            price = TestSeries.price
            total_price = TestSeries.total_price
            discount = total_price - price
            #check if user already enroll and expire or not
            try:
                enroll_details = False
                #if student enrolled in this course then execute this portion (try)
                #retrive current login student
                students = student.objects.get(email=request.session.get('email'))

                #retrive enroll details if student is enrolled in this course
                enroll_details = testseries_enroll.objects.get(student_id=students.id,testseries_id_id=TestSeries.id)

                if enroll_details is not False:
                    return redirect('home') 
                else:
                    return render(request,'checkout.html', {'course': TestSeries,'discount' : discount,'type' : slug_1})
                    
            except:
                if price >= 1:
                    amount = int(price)*100  # Convert amount to paise
                    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

                    # Create a Razorpay order
                    response = client.order.create({'amount': amount, 'currency': 'INR','payment_capture' : 1})

                    order_id = response['id']
                    enroll = testseries_enroll(testseries_id=TestSeries.id,student_id=students.id,amount=int(amount/100),validity=0,datetime=current_datetime_str,order_id=order_id,status = 'Pending',remaning_days=0)
                    enroll.save()

                    return render(request,'checkout.html', {'course': TestSeries,'discount' : discount,'type' : slug_1,'response':response,'razorpay_key_id':settings.RAZORPAY_KEY_ID,'student':students})
                else:
                    order_id = 'ORDS'+str(random.randrange(10000,99999))
                    enroll = testseries_enroll(testseries_id=TestSeries.id,student_id=students.id,amount=0,validity=TestSeries.validity,datetime=current_datetime_str,order_id=order_id,status = 'Success',remaning_days=0)
                    enroll.save()
                    url = '/test-series/test-series-details/'+str(TestSeries.slug)
                    return redirect(url)

      
        else:
            return redirect('home')
    except Exception as e:
        print("checkout page not open because",e)
        if slug_1 == 'course':
            return redirect('courses')
        elif slug_1 == 'test-series':
            return redirect('test-series') 
        else:
            return redirect('home1')


#course enroll 
@login_required
def course_enrolled(request):
    if request.method =='POST':
        try:
            package_type = request.POST.get('PackageType')
            if package_type == 'course':
                #if package is course
                course_slug = request.POST.get('CourseSlug')
                courses = course.objects.get(slug = course_slug)
                email = request.session.get('email')
                students = student.objects.get(email=email)
                current_datetime = datetime.datetime.now()
                current_datetime_str = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
                validity = courses.validity

                
                try:
                    enrolled = course_enroll.objects.get(order_id=request.POST.get('order_id'))
                    enrolled.status = 'Success'
                    enrolled.validity = validity
                    enrolled.save()

                    #check course + testseres
                    if courses.testseries:
                        TestSeries = testseries.objects.get(id = courses.testseries.id)
                        TestSeriesEnroll = testseries_enroll(testseries_id=TestSeries.id,student_id = students.id,datetime=current_datetime_str,amount=0,order_id=request.POST.get('order_id'),status = 'Success',remaning_days=validity,validity=validity)
                        TestSeriesEnroll.save()

                        #email data
                        data = {
                            'package_type' : 'çourse+testseries',
                            'package_name' : str(courses.name) + ' + ' +str(TestSeries.title),
                            'date' : enrolled.datetime,
                            'order_id' : enrolled.order_id,
                            'item1' : {
                                'description' : courses.name,
                                'price': courses.total_price,
                                'discount' : int(courses.total_price) - int(courses.price),
                                'total_price' : courses.price
                                },
                            'item2' : {
                                'description' : TestSeries.title,
                                'price': TestSeries.total_price,
                                'discount' : TestSeries.total_price,
                                'total_price' : 0
                                },
                            'subtotal': enrolled.amount,
                            'tax' : '--',
                            'total_price' : enrolled.amount,
                            'course_slug' :course_slug,

                        }
                        send_email(' Enrollment Successful - '+ str(courses.name) + ' + ' + str(TestSeries.title) + ' - Turing Code',email,'course_testseries_enroll',data)
                    else:
                        data = {
                            'package_type' : 'çourse',
                            'package_name' : courses.name,
                            'date' : enrolled.datetime,
                            'order_id' : enrolled.order_id,
                            'item1' : {
                                'description' : courses.name,
                                'price': courses.total_price,
                                'discount' : int(courses.total_price) - int(courses.price),
                                'total_price' : courses.price
                                },
                            'item2' : None,
                            'subtotal': enrolled.amount,
                            'tax' : '--',
                            'total_price' : enrolled.amount,
                            'course_slug' :course_slug,

                        }
                        send_email(' Enrollment Successful - '+ str(courses.name) +' - Turing Code',email,'course_enroll',data)
                except:
                    return redirect('home')#redirect to 404
                
                url = 'invoice/course/' + str(course_slug)
                return JsonResponse({'status':'Success','url':url})
            
            elif package_type == 'test-series':
                #if package is test-series
                testseries_slug = request.POST.get('CourseSlug')
                TestSeries = testseries.objects.get(slug = testseries_slug)
                current_datetime = datetime.datetime.now()
                current_datetime_str = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
                txn_id = 'TXN' + str(random.randrange(10000,9999999))
                validity = TestSeries.validity

                try:
                    enrolled = testseries_enroll.objects.get(order_id=request.POST.get('order_id'))
                    enrolled.status = 'Success'
                    enrolled.validity = validity
                    enrolled.save()
                except:
                    return redirect('home')
                
                
                url = 'invoice/test-series/' + str(testseries_slug)
                data = {
                            'package_type' : 'testseries',
                            'package_name' : TestSeries.title,
                            'date' : enrolled.datetime,
                            'order_id' : enrolled.order_id,
                            'item1' :  {
                                'description' : TestSeries.title,
                                'price': TestSeries.total_price,
                                'discount' : int(TestSeries.total_price) - int(TestSeries.price),
                                'total_price' : TestSeries.price,
                                },
                            'item2': None,
                            'subtotal': enrolled.amount,
                            'tax' : '--',
                            'total_price' : enrolled.amount,
                            'course_slug' :testseries_slug,

                        }
                send_email(' Enrollment Successful -' + str(TestSeries.title) + ' - Turing Code',request.session.get('email'),'testseries_enroll',data)
                return JsonResponse({'status':'Success','url':url})
            else:
                #if package is neither course nor test series
                return JsonResponse({'status':'error'})
        except Exception as e:
            print("course enroll error are ",e)
            return redirect('home')#redirect to 404
    else:
        return redirect('home')#redirect to 404


@login_required
def invoice(request,slug_1,slug_2):
    #slug_1 represent either coure or test-series
    #slug_2 if course then course slug or if test-series then testseries_slug
    if slug_1 == 'course':
        try:
            courses = course.objects.get(slug=slug_2)
            course_id = courses.id
            email = request.session.get('email')
            students = student.objects.get(email=email)
            student_name = students.name

            #retrive enroll information 
            CourseEnroll = course_enroll.objects.get(student_id=students.id,course_id=courses.id,status='Success')

            #count no of time enroll
            #count_of_enroll = course_enroll.objects.filter(student_id=students.id,course_id=courses.id).count()
            
            #print('CourseEnroll-1 = ',CourseEnroll)
            order_id = CourseEnroll.order_id
            #print('CourseEnroll-2 = ',CourseEnroll)
            txn_date = CourseEnroll.datetime
            amount = CourseEnroll.amount
            try:
                #profile update
                StudentInfo = student_info.objects.get(student_id=students.id) 
                student_mobile = StudentInfo.mobile
                student_address = StudentInfo.address
                student_state = StudentInfo.state
                student_profile_pic = StudentInfo.profile_pic
                student_qualification = StudentInfo.qualification
            except:
                student_mobile = student_address = student_state = student_profile_pic = student_qualification = 'Not Available'
            
            context = {
                'package_name' : courses.name,
                'order_id' : order_id,
                'txn_date' : txn_date,
                'amount' : amount,
                'name' : student_name,
                'mobile' : student_mobile,
                'email' : email,
                'address' : student_address,
                'state' : student_state,
                'profile' : student_profile_pic,
                'qualification' : student_qualification,
                'type' : 'course',
                'package_slug' : slug_2,
                'validity' : CourseEnroll.validity,
            }
            return render(request,'invoice.html',{'context':context})
        except Exception as e:
            print("invoice request error",e)
            return redirect('courses')
    elif slug_1 == 'test-series':
        try:
            TestSeries = testseries.objects.get(slug=slug_2)
            testseries_id = TestSeries.id
            email = request.session.get('email')
            students = student.objects.get(email=email)
            student_name = students.name

            #retrive enroll information 
            TestSeriesEnroll = testseries_enroll.objects.get(student_id=students.id,testseries_id=testseries_id)

            #count no of time enroll
            #count_of_enroll = course_enroll.objects.filter(student_id=students.id,course_id=courses.id).count()

            order_id = TestSeriesEnroll.order_id
            txn_date = TestSeriesEnroll.datetime
            amount = TestSeriesEnroll.amount
            try:
                #profile update
                StudentInfo = student_info.objects.get(student_id=students.id) 
                student_mobile = StudentInfo.mobile
                student_address = StudentInfo.address
                student_state = StudentInfo.state
                student_profile_pic = StudentInfo.profile_pic
                student_qualification = StudentInfo.qualification
            except:
                student_mobile = student_address = student_state = student_profile_pic = student_qualification = 'Not Available'
            
            context = {
                'package_name' : TestSeries.title,
                'order_id' : order_id,
                'txn_date' : txn_date,
                'amount' : amount,
                'name' : student_name,
                'mobile' : student_mobile,
                'email' : email,
                'address' : student_address,
                'state' : student_state,
                'profile' : student_profile_pic,
                'qualification' : student_qualification,
                'type' : 'test-series',
                'package_slug' : slug_2,
                'validity' : TestSeriesEnroll.validity,
            }
            return render(request,'invoice.html',{'context':context})
        except:
            return redirect('test-series')
    else:
        return redirect('home')



#test series start here
@login_required
def TestSeries(request):
    if 'TestId' in request.session:
            request.session.pop('TestId', None)
    not_enrolled_testseries = [] 

    try:
        email = request.session.get('email')
        Student = student.objects.get(email=email)

        # Get IDs of courses enrolled by the logged-in student
        enrolled_testseries_ids = testseries_enroll.objects.filter(student_id=Student.id).values_list('testseries_id', flat=True).order_by('-id')
        
         # Query for active courses not enrolled by the student
        not_enrolled_testseries = testseries.objects.filter(status=1).exclude(id__in=enrolled_testseries_ids).order_by('-id')

        try:
            TestSeriesEnroll = testseries_enroll.objects.filter(student_id=Student.id)
            for item in TestSeriesEnroll:
                #calculate validity (remaning days)
                current_date = date.today()
                past_date = item.datetime.date()
                days_difference = (current_date - past_date).days
                #calculate remaning days
                validity = item.validity - days_difference
                if item.remaning_days >= 0:
                    item.remaning_days = validity
                    item.save()
        except:
            pass

        return render(request,'test-series.html',{'not_enrolled_testseries':not_enrolled_testseries,'enroll_testseries' : TestSeriesEnroll,'StudentName' : Student.name,'student':Student})
    except:
        try:
            TestSeriesEnroll = []
            Student = student.objects.get(email = request.session.get('email'))
            return render(request,'test-series.html',{'not_enrolled_testseries':not_enrolled_testseries,'enroll_testseries' : TestSeriesEnroll,'StudentName'  : Student.name,'student':Student})
        except:
            return redirect("home") #redirect to 404


@login_required
def testseries_details(request,testseries_slug):
    #request.session.pop('TestId', None) is used for test start
    if 'TestId' in request.session:
            request.session.pop('TestId', None)

    try:
        TestSeries = testseries.objects.get(slug = testseries_slug,status=1)
        students = student.objects.get(email=request.session.get('email'))
        testseries_id = TestSeries.id

        #retrive not attempted test
        UnAttemptedTest = test.objects.filter(~Q(id__in=list(
                test_status.objects.filter(student_id=students.id).values_list("test_id", flat=True)
            )
        ),testseries_id = testseries_id,status=1
        )

        #retrive attempted test
        AttemptedTest = test.objects.filter(id__in=list(
                test_status.objects.filter(student_id=students.id).values_list("test_id", flat=True)
            ),testseries_id = testseries_id,status=1
        )

        TestStatus = test_status.objects.filter(student_id=students.id,test_id__in = list(
            test.objects.filter(testseries_id=testseries_id)
        )
        )

        #enroll list of all enroll testseries by a particular student
        enroll = ['Not Enroll']#if student not enroll in this course then list first item is Not Enroll
        try:
            #retrive max id because fetch latest enroll (some time renew course then fetch latest records)
            enroll_details = testseries_enroll.objects.get(student_id=students.id,testseries_id=testseries_id)
            
            #calculate course validity in days
            testseries_enrolled_date = enroll_details.datetime.date()
            if testseries_enrolled_date:
                current_date = date.today()
                past_date = testseries_enrolled_date
                days_difference = (current_date - past_date).days
                #calculate remaning days
                validity = enroll_details.validity - days_difference
                enroll = ['Enrolled',validity] #if student enrolled in this course then first item is Enrolled and second item is Remaning Days 

            return render(request, 'test-series-details.html',{'testseries' : TestSeries,'UnAttemptedTest' : UnAttemptedTest,'AttemptedTests':AttemptedTest,'enroll' : enroll,'TestStatus':TestStatus,'StudentName' : students.name,'student':students})
        
        except:
            try:
                Student = student.objects.get(email = request.session.get('email'))
                return render(request, 'test-series-details.html',{'testseries' : TestSeries,'UnAttemptedTest' : UnAttemptedTest,'AttemptedTests':AttemptedTest,'enroll':enroll,'TestStatus' : TestStatus,'StudentName' : Student.name,'student':students})
            except:
                return redirect("home")#redirect to 404

    except Exception as e:
        #print("error = ", e)
        return redirect('test-series')#remember to redicrect to 404


@login_required
def TestInstruction_1(request,exam_slug,test_slug):
    try:
        try:
            Student = student.objects.get(email=request.session.get('email'))
            Test = test.objects.get(slug = test_slug)
            

            #premium test security (if student is not enrolled and try to access premium test using direct url)
            try:
                if Test.premium == 1:
                    TestSeries = testseries.objects.get(id=Test.testseries_id)
                    TestEnroll = testseries_enroll.objects.get(student_id=Student.id,testseries_id=TestSeries.id)
            except:
                return render(request,'test-error.html')

            TestStatus = test_status.objects.get(test_id = Test.id,student_id = Student.id,completed = 1)
            return render(request,'test-error.html')
        
        except:
            try:
                testinstruction = TestInstruction.objects.get(exam=exam_slug)
                Student = student.objects.get(email = request.session.get('email'))
                return render(request,'test-instructions.html',{'testinstruction' : testinstruction,'exam' : exam_slug,'test_slug':test_slug,'StudentName' : Student.name,'student':Student})
            except:
                return render(request,'test-error.html')
    except:
        return render(request,'test-error.html')

@login_required
def TestInstruction_2(request,exam_slug,test_slug):
    try:

        #premium test security (if student is not enrolled and try to access premium test using direct url)
        Student = student.objects.get(email=request.session.get('email'))
        Test = test.objects.get(slug = test_slug)
    
        #premium test security (if student is not enrolled and try to access premium test using direct url)
        try:
            if Test.premium == 1:
                TestSeries = testseries.objects.get(id=Test.testseries_id)
                TestEnroll = testseries_enroll.objects.get(student_id=Student.id,testseries_id=TestSeries.id)
        except:
            return render(request,'test-error.html')
            

        testinstruction_2 = TestInstruction.objects.get(exam=exam_slug)
        return render(request,'test-instructions-2.html',{'testinstruction_2' : testinstruction_2,'exam' : exam_slug,'test_slug':test_slug,'StudentName' : Student.name,'student':Student})
    except:
        return render(request,'test-error.html')
    

#elapsed time save in database
@login_required
def save_elapsed_time_to_database(request):
    try:
        if request.method == 'POST':
            # Get the elapsed time in seconds from the request data (you can adjust this depending on how the data is sent from the frontend)
            elapsed_time = request.POST.get('elapsed_time', None)
            # Save the elapsed time to the database (you need to define your model and field for this)
            # Example assuming you have a model named 'TestSeries' with a field named 'elapsed_time_in_seconds'
            
            #print("current question = ",request.POST.get('CurrentQuestion'))
            Student = student.objects.get(email=request.session.get('email'))
            StudentAnswer = student_answer.objects.get(question_no=request.POST.get('CurrentQuestion'),student_id=Student.id,test_id = request.POST.get('TestId'))
            TestStatus = test_status.objects.get(test_id=request.POST.get('TestId'),student_id=Student.id)
            TestStatus.use_time = TestStatus.use_time + 2 
            TestStatus.save()

            StudentAnswer.time_taken = StudentAnswer.time_taken + 2
            StudentAnswer.save()

            if TestStatus.completed == 1:
                return JsonResponse({'status': 'error','completed' : '1','message': 'Something went wrong please restart your test'})
            else:
                return JsonResponse({'status': 'success'})
            
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    except Exception as e:
        print("problem = ", e)
        return render(request,'test-error.html')


#save mcq answer
@login_required
def AnswerSave(request):
    try:
        if request.method == 'POST':

            MarkForReviewQuestion = question.objects.get(question_no = request.POST.get('QuestionNo'),test_id = request.POST.get('TestId'))
            # Save the form data to the database using the FormDataModel
            Student = student.objects.get(email=request.session.get('email'))
            StudentAnswer = student_answer.objects.get(question_no=request.POST.get('QuestionNo'),student_id=Student.id,test_id = request.POST.get('TestId'))
            StudentAnswer.visited = 1
            StudentAnswer.markforreview = 0
            StudentAnswer.save()

            if MarkForReviewQuestion.question_type == 'NAT':
                answer = request.POST.get('Nat')
                if answer == '':
                    answer = 'e'
                StudentAnswer.answer = answer.strip()
                StudentAnswer.save()

            elif MarkForReviewQuestion.question_type == 'MCQ':
                answer = request.POST.get('form_data')
                if answer == None:
                    answer = 'e'
                StudentAnswer.answer = answer
                StudentAnswer.save()

            else:
                option1 = request.POST.get('option1')
                option2 = request.POST.get('option2')
                option3 = request.POST.get('option3')
                option4 = request.POST.get('option4')

                if option1 == None and option2 == None and option3 == None and option4 == None:
                    answer = 'e'
                else :
                    answer = ''
                    if option1 != None:
                        answer = option1
                    if option2 != None:
                        answer = answer+option2
                    if option3 != None:
                        answer = answer+option3
                    if option4 != None:
                        answer = answer+option4
                
                    StudentAnswer.answer = answer
                    StudentAnswer.save()
            
            TestId = request.POST.get('TestId')
            Test = test.objects.get(id = TestId)

            Student = student.objects.get(email=request.session.get('email'))
            TestStatus = test_status.objects.get(test_id=TestId,student_id=Student.id)

            #no of paper either 1 or 2
            NoOfPaper = Test.no_of_paper
            TestName = Test.test_name

            #current question 
            QuestionNo = int(request.POST.get('QuestionNo'))

            #fetch paper name
            if NoOfPaper == 1:
                #if check last question or not
                if QuestionNo == Test.total_question_in_paper_1:
                    TestStatus.current_question_paper_1 = 1
                    TestStatus.save()
                else:
                    TestStatus.current_question_paper_1 = QuestionNo + 1
                    TestStatus.save()
                
            if NoOfPaper == 2:
                if QuestionNo < Test.total_question_in_paper_1:
                    TestStatus.current_paper = 1
                    TestStatus.current_question_paper_1 = QuestionNo + 1
                    TestStatus.save()
                else:
                    if QuestionNo == Test.total_question:
                        TestStatus.current_paper = 2
                        TestStatus.current_question_paper_2 = Test.total_question_in_paper_1 + 1
                        TestStatus.save()
                    else:
                        TestStatus.current_paper = 2
                        TestStatus.current_question_paper_2 = QuestionNo + 1
                        TestStatus.save()

            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error'})
    except Exception as e:
        print("answer save error is = ", e)
        return render(request,'test-error.html')


#save mcq answer
@login_required
def ClearAnswer(request):
    try:
        if request.method == 'POST':
            Student = student.objects.get(email=request.session.get('email'))
            StudentAnswer = student_answer.objects.get(question_no=request.POST.get('QuestionNo'),student_id=Student.id,test_id = request.POST.get('TestId'))
            StudentAnswer.answer = 'e'
            StudentAnswer.markforreview = 0
            StudentAnswer.save()

            print("exit success")
            
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error'})
    except:
        return render(request,'test-error.html')


#paper change
@login_required
def PaperChange(request):
    try:
        if request.method == 'POST':
            # Save the form data to the database using the FormDataModel
            Test = test.objects.get(id=request.POST.get('TestId'))
            Student = student.objects.get(email=request.session.get('email'))
            TestStatus = test_status.objects.get(test_id=request.POST.get('TestId'),student_id=Student.id)
            TestStatus.current_paper = int(request.POST.get('Paper'))
            TestStatus.save()

            if TestStatus.current_paper == 1:
                StudentAnswer = student_answer.objects.get(test_id=request.POST.get('TestId'),student_id=Student.id,question_no = 1,paper = TestStatus.current_paper)
                StudentAnswer.visited = 1
                StudentAnswer.save()
            if TestStatus.current_paper == 2:
                CurrentQuestion = Test.total_question_in_paper_1 + 1
                StudentAnswer = student_answer.objects.get(test_id=request.POST.get('TestId'),student_id=Student.id,question_no = CurrentQuestion,paper = TestStatus.current_paper)
                StudentAnswer.visited = 1
                StudentAnswer.save()

            
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error'})
    except Exception as e:
        print("paper change problem arrived",e)
        return render(request,'test-error.html')



#save mcq answer
@login_required
def MarkForReview(request):
    try:
        if request.method == 'POST':

            MarkForReviewQuestion = question.objects.get(question_no = request.POST.get('QuestionNo'),test_id = request.POST.get('TestId'))
            # Save the form data to the database using the FormDataModel
            Student = student.objects.get(email=request.session.get('email'))
            StudentAnswer = student_answer.objects.get(question_no=request.POST.get('QuestionNo'),student_id=Student.id,test_id = request.POST.get('TestId'))
            StudentAnswer.visited = 1
            StudentAnswer.markforreview = 1
            StudentAnswer.save()

            if MarkForReviewQuestion.question_type == 'NAT':
                answer = request.POST.get('Nat')
                if answer == '':
                    answer = 'e'
                StudentAnswer.answer = answer.strip()
                StudentAnswer.save()

            elif MarkForReviewQuestion.question_type == 'MCQ':
                answer = request.POST.get('form_data')
                if answer == None:
                    answer = 'e'
                StudentAnswer.answer = answer
                StudentAnswer.save()

            else:
                option1 = request.POST.get('option1')
                option2 = request.POST.get('option2')
                option3 = request.POST.get('option3')
                option4 = request.POST.get('option4')

                if option1 == None and option2 == None and option3 == None and option4 == None:
                    answer = 'e'
                else :
                    answer = ''
                    if option1 != None:
                        answer = option1
                    if option2 != None:
                        answer = answer+option2
                    if option3 != None:
                        answer = answer+option3
                    if option4 != None:
                        answer = answer+option4
                
                    StudentAnswer.answer = answer
                    StudentAnswer.save()
            
            TestId = request.POST.get('TestId')
            Test = test.objects.get(id = TestId)

            Student = student.objects.get(email=request.session.get('email'))
            TestStatus = test_status.objects.get(test_id=TestId,student_id=Student.id)

            #no of paper either 1 or 2
            NoOfPaper = Test.no_of_paper
            TestName = Test.test_name

            #current question 
            QuestionNo = int(request.POST.get('QuestionNo'))

            #fetch paper name
            if NoOfPaper == 1:
                #if check last question or not
                if QuestionNo == Test.total_question_in_paper_1:
                    TestStatus.current_question_paper_1 = 1
                    TestStatus.save()
                else:
                    TestStatus.current_question_paper_1 = QuestionNo + 1
                    TestStatus.save()
                
            if NoOfPaper == 2:
                if QuestionNo < Test.total_question_in_paper_1:
                    TestStatus.current_paper = 1
                    TestStatus.current_question_paper_1 = QuestionNo + 1
                    TestStatus.save()
                else:
                    if QuestionNo == Test.total_question:
                        TestStatus.current_paper = 2
                        TestStatus.current_question_paper_2 = Test.total_question_in_paper_1 + 1
                        TestStatus.save()
                    else:
                        TestStatus.current_paper = 2
                        TestStatus.current_question_paper_2 = QuestionNo + 1
                        TestStatus.save()

            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error'})
    except Exception as e:
        print("marked for review = ", e)
        return render(request,'test-error.html')


@login_required
def PreviousQuestion(request):
    try:
        if request.method == 'POST':
            # Save the form data to the database using the FormDataModel
            QuestionNo = int(request.POST.get('QuestionNo'))
            TestId = request.POST.get('TestId')
            Test = test.objects.get(id = TestId)
            Student = student.objects.get(email=request.session.get('email'))
            TestStatus = test_status.objects.get(test_id=TestId,student_id=Student.id)
            StudetnAnswer = student_answer.objects.get(test_id=TestId,student_id=Student.id,question_no = QuestionNo)
            StudetnAnswer.visited = 1
            StudetnAnswer.save()

            if Test.no_of_paper == 1:
                TestStatus.current_question_paper_1 = QuestionNo
                TestStatus.save()
            
            if Test.no_of_paper == 2:
                if QuestionNo <= Test.total_question_in_paper_1:
                    TestStatus.current_question_paper_1 = QuestionNo
                    TestStatus.save()
                else:
                    TestStatus.current_question_paper_2 = QuestionNo
                    TestStatus.save()
            
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error'})
    except Exception as e:
        print("previous page error =",e)
        return render(request,'test-error.html')


#save and next 
@login_required
def QuestionChange(request):
    try:
        if request.method == 'POST':
            Student = student.objects.get(email=request.session.get('email'))
            StudentAnswer = student_answer.objects.get(question_no=request.POST.get('QuestionNo'),student_id=Student.id,test_id = request.POST.get('TestId'))
            StudentAnswer.visited = 1
            StudentAnswer.save()

            TestId = request.POST.get('TestId')
            Test = test.objects.get(id = TestId)

            Student = student.objects.get(email=request.session.get('email'))
            TestStatus = test_status.objects.get(test_id=TestId,student_id=Student.id)

            #no of paper either 1 or 2
            NoOfPaper = Test.no_of_paper
            TestName = Test.test_name

            #current question 
            QuestionNo = int(request.POST.get('QuestionNo'))

            if NoOfPaper == 1:
                TestStatus.current_question_paper_1 = QuestionNo
                TestStatus.current_paper = 1
                TestStatus.save()
            
            if NoOfPaper == 2:
                if QuestionNo <= Test.total_question_in_paper_1:
                    TestStatus.current_question_paper_1 = QuestionNo
                    TestStatus.current_paper = 1
                    TestStatus.save()
                else:
                    TestStatus.current_question_paper_2 = QuestionNo
                    TestStatus.current_paper = 2
                    TestStatus.save()

            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error'})
    except:
        return render(request,'test-error.html')


#test submit
@login_required
def TestSubmit(request):
    if request.method == 'GET':
        try:
            Test = test.objects.get(slug = request.GET.get('test'))
            TestId = Test.id
            Student = student.objects.get(email=request.session.get('email'))
            TestStatus = test_status.objects.get(test_id = TestId,student_id = Student.id)
            TestStatusId = TestStatus.id
            TestCompletedStatus = TestStatus.completed
            #calculate total marks 
            PositiveMarks = 0
            NegativeMarks = 0
            TotalCorrectQuestion = 0
            TotalIncorrectQuestion = 0

            Questions = question.objects.filter(test_id = TestId)

            for Ques in Questions:
                StudentAnswer = student_answer.objects.get(question_id = Ques.id,student_id=Student.id,test_id=TestId)
                #some time more than one answer in mcq,msq,nat so questionAnswer store in list and check student answer in list
                #retrive option of question
                QuestionAnswer = list(question_answer.objects.filter(question_id = Ques.id).values_list('answer',flat=True))

                if str(StudentAnswer.answer) in QuestionAnswer and 'MTA' not in QuestionAnswer:
                    #if answer is correct
                    PositiveMarks = PositiveMarks + Ques.positive_marks
                    TotalCorrectQuestion = TotalCorrectQuestion + 1

                    #if question is correct then answer_
                    # result is Correct
                    StudentAnswer.answer_result = 'Correct'
                    StudentAnswer.save()

                elif StudentAnswer.answer != 'e' and 'MTA' not in QuestionAnswer:
                    #Question is NAT type then check range 
                    if Ques.question_type == 'NAT' and Ques.nat_range:
                        #if more than one answer given (range given)
                        RoundTo = Ques.nat_round_decimal_digit #in exam given round to 2 decimal digit so use the variable RoundTo 
                        StuAns = float(StudentAnswer.answer)
                        StuAns == round(StuAns, RoundTo)

                        if len(QuestionAnswer) == 2:
                            if StuAns >= float(QuestionAnswer[0]) and StuAns <= float(QuestionAnswer[1]):
                                #if answer is correct
                                PositiveMarks = PositiveMarks + Ques.positive_marks
                                TotalCorrectQuestion = TotalCorrectQuestion + 1

                                #if question is correct then answer_
                                # result is Correct
                                StudentAnswer.answer_result = 'Correct'
                                StudentAnswer.save()
                        else:
                            #if answer is given but answer is incorrect
                            NegativeMarks = NegativeMarks + float(Ques.negative_marks)
                            TotalIncorrectQuestion = TotalIncorrectQuestion + 1

                            #if question is correct then answer_result is Correct
                            StudentAnswer.answer_result = 'InCorrect'
                            StudentAnswer.save()
                    else:
                        #if answer is given but answer is incorrect
                        NegativeMarks = NegativeMarks + float(Ques.negative_marks)
                        TotalIncorrectQuestion = TotalIncorrectQuestion + 1

                        #if question is correct then answer_result is Correct
                        StudentAnswer.answer_result = 'InCorrect'
                        StudentAnswer.save()

                elif 'MTA' in QuestionAnswer:
                    PositiveMarks = PositiveMarks + Ques.positive_marks
                    StudentAnswer.answer_result = 'Correct'
                    StudentAnswer.save()
                else:
                    pass
            

            #count total attempted question
            TotalLeftQuestion = student_answer.objects.filter(test_id = TestId,student_id = Student.id,answer = 'e').count()

            #total left question
            TotalAttemptQuestion = Test.total_question - TotalLeftQuestion


            #calculate percentage 
            #GetTotalMarks = PositiveMarks - NegativeMarks
            #Percentage = (GetTotalMarks / Test.total_marks)*100
            #Percentage = round(Percentage,2)

            #store total marks,positive marks,negative marks,attempted question,left questions store in database
            #TestStatus.positive_marks = PositiveMarks
            #TestStatus.negative_marks = NegativeMarks
            #TestStatus.total_attempted = TotalAttemptQuestion
            #TestStatus.leftQuestion = TotalLeftQuestion
            #TestStatus.correct_question = TotalCorrectQuestion
            #TestStatus.incorrect_question = TotalIncorrectQuestion
            #TestStatus.percentage = Percentage


            #calculate total marks in this paper 
            GetTotalMarks = PositiveMarks - NegativeMarks
            TestStatus.total_marks = round(GetTotalMarks,2)
            TestStatus.save()
            
            
            #second to time format function
            def seconds_to_time_format(seconds):
                hours = seconds // 3600
                minutes = (seconds % 3600) // 60
                seconds = seconds % 60

                return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            
            #total time taken in test convert into time format
            TotalUseTime = seconds_to_time_format(TestStatus.use_time)
            TotalTime = Test.duration * 60
            TotalTime = seconds_to_time_format(TotalTime)


            #calculate rank 
            rank = 1
            TestStatus = test_status.objects.filter(test_id=TestId).annotate(
                    total_marks_numeric=Cast(F('total_marks'), output_field=FloatField())
                ).order_by('-total_marks_numeric')
            
            for x in TestStatus:
                if x.completed == 1 or x.student.id == Student.id:
                    x.rank = rank
                    x.save() 
                    rank = rank + 1
                
                
            #calculate other info 

            #Accuracy = round((TotalCorrectQuestion / TotalAttemptQuestion) * 100 ,2)
            #StudentTestStatus = student_test_status(test_id = TestId,student_id = Student.id,test_status_id = TestStatusId,accuracy = Accuracy,attempted_question=TotalAttemptQuestion,correct_question = TotalCorrectQuestion,incorrect_question = TotalIncorrectQuestion,left_question = TotalLeftQuestion)
            #StudentTestStatus.save()

            TestStatus = test_status.objects.get(test_id = TestId,student_id = Student.id)

            #accuracy and other detail submit
            StudentTestStatusCheck = student_test_status.objects.filter(test_id=TestId,student_id=Student.id,test_status_id = TestStatus.id)            

            if not StudentTestStatusCheck.exists():
                if TotalAttemptQuestion > 0:
                    Accuracy = int((TotalCorrectQuestion / TotalAttemptQuestion) * 100)
                    StudentTestStatus = student_test_status(test_id = TestId,student_id = Student.id,test_status_id = TestStatus.id,accuracy = Accuracy,attempted_question=TotalAttemptQuestion,correct_question = TotalCorrectQuestion,incorrect_question = TotalIncorrectQuestion,left_question = TotalLeftQuestion)
                    StudentTestStatus.save()
                else:
                    StudentTestStatus = student_test_status(test_id = TestId,student_id = Student.id,test_status_id = TestStatus.id,accuracy = 0,attempted_question=TotalAttemptQuestion,correct_question = TotalCorrectQuestion,incorrect_question = TotalIncorrectQuestion,left_question = TotalLeftQuestion)
                    StudentTestStatus.save()

            #save completed 
            TestStatus.incomplete = 0
            TestStatus.completed = 1
            TestStatus.save()

            TestSeries = testseries.objects.get(id=Test.testseries_id)
            
            return render(request,'test-feedback.html',{'TestSlug' : Test.slug,'TestSeriesSlug' : TestSeries.slug,'TotalQuestion' : Test.total_question,'MaximumMarks' : Test.total_marks,'TotalAttemptQuestion':TotalAttemptQuestion,'TotalLeftQuestion': TotalLeftQuestion,'TotalTime' : TotalTime,'TotalUseTime' : TotalUseTime})
            #print("Test Submit Successfully - 2")
        except Exception as e:
            print("new test submit error = ",e)
            return render(request,'test-error.html')
    else:
        return render(request,'test-error.html')


@login_required
def TestFeedback(request):
    try:
        if request.method == 'POST':
            Test = test.objects.get(slug = request.POST.get('test'))
            #print("Test Feedback now = ",request.POST.get('student_feedback'))
            StudentFeedback = request.POST.get('student_feedback')
            Student = student.objects.get(email=request.session.get('email'))
            TestFeedback = Feedback(test_id = Test.id, student_id = Student.id,feedback=StudentFeedback)
            TestFeedback.save()
        
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error'})
    except Exception as e:
        #print("this is feebback error =",e)
        return render(request,'test-error.html')

@login_required
def CurrentQuesAnswer(request):
    try:
        if request.method == 'POST':
            Test = test.objects.get(id = request.POST.get('TestId'))
            Student = student.objects.get(email=request.session.get('email'))
            StudentAnswer = student_answer.objects.get(test_id=Test.id,question_no=request.POST.get('CurrentQuestionNo'),student_id=Student.id)        
            return JsonResponse({'status': 'success','CurrentAnswer':StudentAnswer.answer})
        return JsonResponse({'status': 'error'})
    except Exception as e:
        #print("this is feebback error =",e)
        return render(request,'test-error.html')

def TestError(request):
    return render(request,'test-error.html')


@login_required
def TestComparisonReport(request,testseries_slug,test_slug):
        try:
            Testseries = testseries.objects.get(slug=testseries_slug)
            Test = test.objects.get(slug=test_slug)
            TestId = Test.id
            Student = student.objects.get(email=request.session.get('email'))
            TestStatus = test_status.objects.get(test_id = TestId,student_id = Student.id,completed=1)

            #calculate total marks 
            PositiveMarks = 0
            NegativeMarks = 0
            TotalCorrectQuestion = 0
            TotalIncorrectQuestion = 0

            Questions = question.objects.filter(test_id = TestId)

            for Ques in Questions:
                StudentAnswer = student_answer.objects.get(question_id = Ques.id,student_id=Student.id,test_id=TestId)
                #some time more than one answer in mcq,msq,nat so questionAnswer store in list and check student answer in list
                #retrive option of question
                QuestionAnswer = list(question_answer.objects.filter(question_id = Ques.id).values_list('answer',flat=True))

                if str(StudentAnswer.answer) in QuestionAnswer and 'MTA' not in QuestionAnswer:
                    #if answer is correct
                    PositiveMarks = PositiveMarks + Ques.positive_marks
                    TotalCorrectQuestion = TotalCorrectQuestion + 1
                    #print("Question No = ",Ques.question_no,"Student Answer = ",StudentAnswer.answer,"Question Answer",QuestionAnswer)

                    #if question is correct then answer_result is Correct but already completed this process at time of submit
                    if str(StudentAnswer.answer_result) != 'Correct':
                        StudentAnswer.answer_result = 'Correct'
                        StudentAnswer.save()
                    
                elif StudentAnswer.answer != 'e' and 'MTA' not in QuestionAnswer:
                    #Question is NAT type then check range 
                    if Ques.question_type == 'NAT' and Ques.nat_range:
                        #if answer update then re check
                        #if more than one answer given (range given)
                        RoundTo = Ques.nat_round_decimal_digit #in exam given round to 2 decimal digit so use the variable RoundTo 
                        StuAns = float(StudentAnswer.answer)
                        StuAns == round(StuAns, RoundTo)

                        if len(QuestionAnswer) == 2:
                            if StuAns >= float(QuestionAnswer[0]) and StuAns <= float(QuestionAnswer[1]):
                                #if answer is correct
                                PositiveMarks = PositiveMarks + Ques.positive_marks
                                TotalCorrectQuestion = TotalCorrectQuestion + 1

                                #if question is correct then answer_
                                # result is Correct
                                if str(StudentAnswer.answer_result) != 'Correct':
                                    StudentAnswer.answer_result = 'Correct'
                                    StudentAnswer.save()
                        else:
                            #if answer is given but answer is incorrect
                            NegativeMarks = NegativeMarks + float(Ques.negative_marks)
                            TotalIncorrectQuestion = TotalIncorrectQuestion + 1

                            #if question is correct then answer_result is Correct
                            if str(StudentAnswer.answer_result) != 'InCorrect':
                                StudentAnswer.answer_result = 'InCorrect'
                                StudentAnswer.save()
                    else:
                        #if answer is given but answer is incorrect 
                        NegativeMarks = NegativeMarks + float(Ques.negative_marks)
                        TotalIncorrectQuestion = TotalIncorrectQuestion + 1

                        #if answer is given but answer is incorrect but already completed this process at time of test submit
                        if str(StudentAnswer.answer_result) != 'InCorrect':
                            StudentAnswer.answer_result = 'InCorrect'
                            StudentAnswer.save()

                elif 'MTA' in QuestionAnswer:
                    PositiveMarks = PositiveMarks + Ques.positive_marks
                    StudentAnswer.answer_result = 'Correct'
                    StudentAnswer.save()
                else:
                    pass
            
            #negative marks roundof because float value
            NegativeMarks = round(NegativeMarks,2)

            #count total attempted question
            TotalLeftQuestion = student_answer.objects.filter(test_id = TestId,student_id = Student.id,answer = 'e').count()

            #total left question
            TotalAttemptQuestion = Test.total_question - TotalLeftQuestion

            #calculate total marks in this paper 
            GetTotalMarks = PositiveMarks - NegativeMarks
            GetTotalMarks = round(GetTotalMarks,2)

            #calculate percentage
            Percentage = (GetTotalMarks / Test.total_marks)*100
            Percentage = round(Percentage,2)
            
            #second to time format function
            def seconds_to_time_format(seconds):
                hours = seconds // 3600
                minutes = (seconds % 3600) // 60
                seconds = seconds % 60

                return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            
            #total time taken in test convert into time format
            TotalUseTime = seconds_to_time_format(TestStatus.use_time)
            TotalTime = Test.duration * 60
            TotalTime = seconds_to_time_format(TotalTime)

            #retrive rank of student
            Rank = TestStatus.rank

            #calculate no of student appear in this test
            RankOutOf = test_status.objects.filter(test_id=TestId,completed=1).count()

            #MAXIMUM MARKS IN THIS TEST
            MaxMarks = Test.total_marks

            #student accuracy and other details insert if not insert at the time of test submit
            StudentTestStatusCheck = student_test_status.objects.filter(test_id=TestId,student_id=Student.id,test_status_id = TestStatus.id)            

            if not StudentTestStatusCheck.exists():
                if TotalAttemptQuestion > 0:
                    Accuracy = int((TotalCorrectQuestion / TotalAttemptQuestion) * 100)
                    StudentTestStatus = student_test_status(test_id = TestId,student_id = Student.id,test_status_id = TestStatus.id,accuracy = Accuracy,attempted_question=TotalAttemptQuestion,correct_question = TotalCorrectQuestion,incorrect_question = TotalIncorrectQuestion,left_question = TotalLeftQuestion)
                    StudentTestStatus.save()
                else:
                    StudentTestStatus = student_test_status(test_id = TestId,student_id = Student.id,test_status_id = TestStatus.id,accuracy = 0,attempted_question=TotalAttemptQuestion,correct_question = TotalCorrectQuestion,incorrect_question = TotalIncorrectQuestion,left_question = TotalLeftQuestion)
                    StudentTestStatus.save()
            
            context = {
                'Rank': Rank,
                'RankOutOf' : RankOutOf,
                'TotalUseTime' : TotalUseTime,
                'TotalTime' : TotalTime,
                'Percentage' : Percentage,
                'GetTotalMarks' : GetTotalMarks,
                'MaxMarks' : MaxMarks,
                'PositiveMarks' : PositiveMarks,
                'NegativeMarks' : NegativeMarks,
                'TotalAttemptQuestion' : TotalAttemptQuestion,
                'TotalCorrectQuestion' : TotalCorrectQuestion,
                'TotalIncorrectQuestion' : TotalIncorrectQuestion,
                'TotalLeftQuestion' : TotalLeftQuestion,
                'TestName' : Test.test_name,
                'TestSeries_Slug' : testseries_slug,
                'Test_Slug' : test_slug,
                'd_level' : Test.difficulty_level,
                'm_level' : Test.mode_rate_level,
                'e_level' : Test.easy_level,
            }
            

            TestStatus = test_status.objects.filter(rank__lte=10,test_id=TestId,completed=1).order_by('rank')[:10]
            return render(request,'test-comparison-report.html',{'context' : context,'TestStatus' : TestStatus,'StudentName' : Student.name,'student':Student})

        except Exception as e:
            print("test comparision report error = ",e)
            url = 'http://127.0.0.1:8000/test-series/test-series-details/' + str(testseries_slug)
            return redirect(url)#redirect 404

@login_required
def TestQuestionAnalysis(request,testseries_slug,test_slug):
    try:
        Test = test.objects.get(slug=test_slug)
        TestId = Test.id
        Student = student.objects.get(email=request.session.get('email'))
        TestStatus = test_status.objects.get(test_id=TestId,student_id=Student.id,completed = 1)
        StudentAnswer = student_answer.objects.filter(test_id=TestId,student_id=Student.id).order_by('paper','question_no')

        return render(request,'test-question-analysis.html',{'StudentAnswer' : StudentAnswer,'testseries_slug':testseries_slug,'test_slug':test_slug,'TestName':Test.test_name,'StudentName' : Student.name,'student':Student})
    except Exception as e:
        print("test-question-analysis-error", e)
        return render(request,'test-series.html')#return 404

@login_required
def Solutions(request,testseries_slug,test_slug):
    try:
        Test = test.objects.get(slug=test_slug)
        TestId = Test.id
        Questions = question.objects.filter(test_id=Test).order_by('paper','question_no')
        Student = student.objects.get(email=request.session.get('email'))
        TestStatus = test_status.objects.get(test_id=TestId,student_id=Student.id,completed = 1)
        StudentAnswer = student_answer.objects.filter(test_id=TestId,student_id=Student.id).order_by('paper','question_no')

        return render(request,'question-solution.html',{'StudentAnswer':StudentAnswer,'testseries_slug':testseries_slug,'test_slug':test_slug,'TestName' : Test.test_name,'StudentName' : Student.name,'student':Student})
    except:
        return render(request,'test-series.html')#return to 404

@login_required
def Profile(request):
    if request.method == 'POST':
        try:
            Student = student.objects.get(email = request.session.get('email'))
            dob = request.POST.get('Dob')
            address = request.POST.get('Address')
            state = request.POST.get('State')
            qualification = request.POST.get('Qualification')
            mobile = request.POST.get('Mobile')
            uploaded_file = request.FILES['image']
            student_id = Student.id

            Student_info = student_info.objects.get(student_id=student_id)
            #update student info
            Student_info.dob = dob
            Student_info.address = address
            Student_info.state = state
            Student_info.qualification = qualification
            Student_info.mobile = mobile
            Student_info.profile_pic=uploaded_file
            Student_info.save()
            print("thik h")
            Student_info = student_info.objects.get(student_id=student_id)
            return render(request,'profile.html',{'student':Student,'student_info':Student_info,'StudentName' : Student.name})
        except:
            dob = request.POST.get('Dob')
            address = request.POST.get('Address')
            state = request.POST.get('State')
            qualification = request.POST.get('Qualification')
            mobile = request.POST.get('Mobile')
            uploaded_file = request.FILES['image']
            Student = student.objects.get(email = request.session.get('email'))
            student_id = Student.id

            StudentInfo = student_info(
                dob=dob,
                address=address,
                state=state,
                qualification=qualification,
                student_id=student_id,
                mobile=mobile,
                profile_pic=uploaded_file
                )
            StudentInfo.save()

            Student_info = student_info.objects.get(student_id=student_id)

            return render(request,'profile.html',{'student':Student,'student_info':Student_info,'StudentName' : Student.name})
    else:  
        try:
            Student = student.objects.get(email=request.session.get('email'))
            try:
                Student_info = student_info.objects.get(student_id=Student.id)
            except:
                Student_info = []
            return render(request, 'profile.html', {'student':Student,'student_info' : Student_info,'StudentName' : Student.name})
        except:
            return redirect('home')#404

@login_required
def NewTestSeries(request):
    if request.method == 'GET':
        current_datetime = datetime.datetime.now()
        current_datetime_str = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        try:
            Student = student.objects.get(email=request.session.get('email'))
            Test = test.objects.get(slug=request.GET.get('test'))
            TestId = Test.id
            

            #check if test status exists or not
            TestStatus = test_status.objects.filter(test_id=TestId,student_id=Student.id,completed=0)
            
            #premium test security (if student is not enrolled and try to access premium test using direct url)
            try:
                if Test.premium == 1:
                    TestSeries = testseries.objects.get(id=Test.testseries_id)
                    TestEnroll = testseries_enroll.objects.get(student_id=Student.id,testseries_id=TestSeries.id)
            except:
                return render(request,'test-error.html')

            
            if not TestStatus.exists():
                total_time = (Test.duration) * 60
                if Test.no_of_paper == 1:
                    TestStatus = test_status(current_question_paper_1=1,current_question_paper_2=1,incomplete=1,completed=0,date = current_datetime_str,total_time = total_time,use_time = 0,rank = -1,student_id=Student.id,test_id = Test.id,current_paper=1)
                    TestStatus.save()
                
                if Test.no_of_paper == 2:
                    TotalQues_Paper1 = Test.total_question_in_paper_1 + 1
                    TestStatus = test_status(current_question_paper_1=1,current_question_paper_2=TotalQues_Paper1,incomplete=1,completed=0,date = current_datetime_str,total_time = total_time,use_time = 0,rank = -1,student_id=Student.id,test_id = Test.id,current_paper=1)
                    TestStatus.save()
                
                Questions = question.objects.filter(test_id=TestId).order_by('question_no')
                for Ques in Questions:
                    print("Quesiton No = ",Ques.question_no)
                    StuAns = student_answer(question_no = Ques.question_no,answer='e',time_taken=0,visited=0,markforreview=0,question_id=Ques.id,student_id=Student.id,test_id=TestId,paper=Ques.paper)
                    StuAns.save()
            else:
                Questions = question.objects.filter(test_id=TestId).order_by('question_no')
                StudentAnswer = student_answer.objects.filter(test_id=TestId,student_id=Student.id).order_by('question_no')
                if StudentAnswer.count() != Questions.count():
                    for Ques in Questions:
                        CurrentAnswer =  student_answer.objects.filter(question_id=Ques.id)
                        if not CurrentAnswer.exists(): 
                            print("Quesiton No (if some already exists) = ",Ques.question_no)
                            StuAns = student_answer(question_no = Ques.question_no,answer='e',time_taken=0,visited=0,markforreview=0,question_id=Ques.id,student_id=Student.id,test_id=TestId,paper=Ques.paper)
                            StuAns.save()

            
            
            TestStatus = test_status.objects.get(test_id = TestId,student_id = Student.id,completed = 0)
            
            Questions = question.objects.filter(test_id = TestId).order_by('question_no')

            #count total question in current paper
            No_Of_Paper = Test.no_of_paper

            #fetch paper name
            if Test.no_of_paper == 1:
                #fetch the name of paper
                Paper_1_Name = list(set(question.objects.filter(test_id=TestId,paper=1).values_list('paper_name',flat=True)))
                Paper_2_Name = [None] #if only one paper then second paper is none

                #if current paper is one then calculate total no of question
                total_question_in_current_paper = Test.total_question_in_paper_1

                #visited is 1
                CurrentQuestion = question.objects.get(test_id = TestId,paper = 1,question_no = TestStatus.current_question_paper_1)
                CurrentAnswer = student_answer.objects.get(question_id = CurrentQuestion,student_id = Student.id)
                CurrentAnswer.visited = 1
                CurrentAnswer.save()
            
            if Test.no_of_paper == 2:
                Paper_1_Name = list(set(question.objects.filter(test_id=TestId,paper=1).values_list('paper_name',flat=True)))
                Paper_2_Name = list(set(question.objects.filter(test_id=TestId,paper=2).values_list('paper_name',flat=True)))
                total_question_in_current_paper = Test.total_question_in_paper_2


            PaperName = [Paper_1_Name[0],Paper_2_Name[0]]

            StudentAnswer = student_answer.objects.filter(test_id = TestId, student_id = Student.id).order_by('question_no')
            
            try:
                #do current question in both is visited
                if Test.no_of_paper == 1:
                    StudentAns = student_answer.objects.get(question_no = TestStatus.current_question_paper_1,test_id = TestId,student_id = Student.id)
                    StudentAns.visited = 1
                    StudentAns.save()
                
                if Test.no_of_paper == 2:
                    StudentAns = student_answer.objects.get(question_no = TestStatus.current_question_paper_1,test_id = TestId,student_id = Student.id)
                    StudentAns.visited = 1
                    StudentAns.save()

                    StudentAns = student_answer.objects.get(question_no = TestStatus.current_question_paper_2,test_id = TestId,student_id = Student.id)
                    StudentAns.visited = 1
                    StudentAns.save()
            except:
                pass

            TestSeries = testseries.objects.get(id=Test.testseries_id)
            #print("EXAM FOR = ",TestSeries.exam)
            context = {
                'Questions' : Questions,
                'No_Of_Paper' : No_Of_Paper,
                'total_question_in_current_paper' : total_question_in_current_paper,
                'StudentAnswer' : StudentAnswer,
                'StudentName' : Student.name,
                'Current_Paper' : TestStatus.current_paper,
                'CurrentQuestionInPaper1' : int(TestStatus.current_question_paper_1),
                'CurrentQuestionInPaper2' : int(TestStatus.current_question_paper_2),
                'no_of_paper' : Test.no_of_paper,
                'PaperName' : PaperName,
                'TotalQuestionInPaper1' : int(Test.total_question_in_paper_1),
                'TestId' : TestId,
                'StudentId' : Student.id,
                'TestName' : Test.test_name,
                'TestRemaningTime' : TestStatus.total_time - TestStatus.use_time,
                'TestSlug' : Test.slug,
                'exam' : TestSeries.exam,
                'student':Student,
                'TestSeriesSlug' : TestSeries.slug,
            }

            request.session['TestId'] = TestId
            
            return render(request,'new-test.html',context)
        except Exception as e:
            print("problem = ",e)
            return redirect('test_error')


# views.py
@login_required
def watch_history(request):
    try:
        Student = student.objects.get(email=request.session.get('email'))

        try:
            # Check if the user has an existing watch history for the video
            watch_history = WatchHistory.objects.get(student_id=Student.id, video_id=request.POST.get('video_id'))

            if request.method == 'POST':
                watch_history.watch_time = int(request.POST.get('watch_time')) + int(watch_history.watch_time)
                watch_history.current_status = request.POST.get('current_status')
                watch_history.save()
        except Exception as e:
            StudentId = get_object_or_404(student, id=Student.id)
            video = get_object_or_404(videos, id=request.POST.get('video_id'))
            watchhistory = WatchHistory(student_id=StudentId,video_id=video,watch_time=request.POST.get('watch_time'),current_status=request.POST.get('current_status'))
            watchhistory.save()

        return JsonResponse({'status': 'success'})
    except Exception as e:
        print("problem to save watch video history is", e)
        return JsonResponse({'status': 'error'})



def get_watch_history(request):
    try:
        Student = student.objects.get(email=request.session.get('email'))
        
        if request.method == 'POST':
            watch_history = WatchHistory.objects.get(student_id=Student.id, video_id = request.POST.get('video_id'))

            data = {
                'watch_time': watch_history.watch_time,
                'current_status': watch_history.current_status,
            }
            return JsonResponse({'status': 'success','data' : data})
        else:
            return JsonResponse({'status': 'error'})
    except Exception as e:
        print("problem to get watch video history is", e)
        return JsonResponse({'status': 'error'})
    

def send_email(Subject,StudentEmail,EmailType,EnrollInfo):
    
    try:
        Student = student.objects.get(email = StudentEmail)
        # Assuming you have a user or username to personalize the email
        username = Student.name
        
        html_message = render_to_string('email.html', {'username': username,'otp':Student.otp,'email_type':EmailType,'data':EnrollInfo})

        # Create a plain text version of the HTML content
        plain_message = strip_tags(html_message)

        # Create the EmailMultiAlternatives object
        email = EmailMultiAlternatives(
            str(Subject),#email subject
            plain_message,  # Plain text message
            settings.EMAIL_HOST_USER,  # Sender's email address
            [str(Student.email)],  # List of recipient email addresses
            #reply_to=['turingcodecse@gmail.com'],  # Optional reply-to email address
        )

        # Attach the HTML version of the email
        email.attach_alternative(html_message, 'text/html')

        # Send the email
        try:
            email.send()
            #if email send successfully then return true other return false
            print("email send success")
            return True
        except Exception as e:
            return False
    except:
        return False