from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import student,student_info,course,testseries,test,question,question_answer,question_options,student_answer,test_status,notes_package,notes,video_package,videos,course_notes,course_video,course_enroll,testseries_enroll,TestInstruction,question_solution,PromotionalVideo,IndexContent,AboutUs,ContactForm,student_test_status,Feedback,duplicate_video,WatchHistory
from django import forms
from django.db import models
from ckeditor.widgets import CKEditorWidget

#the following class is use to show student admin add form (show) student info 
class student_infoInline(admin.TabularInline):
    model = student_info

 
class studentAdmin(admin.ModelAdmin):
    list_display = ('id','name','email','join_date','otp','email_verify','status')
    inlines = [student_infoInline]

admin.site.register(student,studentAdmin)


class student_infoAdmin(admin.ModelAdmin):
    list_display = ('student','student_name','mobile','mobile','dob','address','state','profile_pic','qualification')
    #the following raw_id_fields used for student_infoInline
    raw_id_fields = ('student',)

    #the following two function used to show student name and mobile in student_info list
    def student_name(self,obj):
        return obj.student.name
    
    def student_mobile(self, obj):
        return obj.student.mobile

admin.site.register(student_info, student_infoAdmin)


class courseAdmin(admin.ModelAdmin):
    list_display = ('id','name','price','testseries','total_price','date','exam_for','poster','validity','status')

admin.site.register(course,courseAdmin)

#the following class is use to show test add form (show) testseries packages 
class testInline(admin.TabularInline):
    model = test

class testseriesAdmin(admin.ModelAdmin):
    list_display = ('id','title','price','total_price','poster','date','exam','validity','status')
    inlines = [testInline]

admin.site.register(testseries,testseriesAdmin)

#the following class is use to show test add form (show) testseries packages 
class questionInline(admin.TabularInline):
    model = question

class testAdmin(admin.ModelAdmin):
    list_display = ('id','test_name','total_question','duration','total_marks','no_of_paper','report_status','status','premium','testseries_id')
    inlines = [questionInline]

admin.site.register(test,testAdmin)


#the following class is use to show test add form (show) testseries packages 
class question_optionsInline(admin.TabularInline):
    model = question_options

#the following class is use to show test add form (show) testseries packages 
class question_answerInline(admin.TabularInline):
    model = question_answer

#the following class is use to show test add form (show) testseries packages 
class question_solutionInline(admin.TabularInline):
    model = question_solution

class questionAdmin(admin.ModelAdmin):
    list_display = ('id','test_id','paper_name','question_no','question_time','question_text','positive_marks','negative_marks','question_type','status','nat_range','nat_round_decimal_digit')
    inlines = [question_optionsInline,question_answerInline,question_solutionInline]
    list_filter = ('test_id','question_type','positive_marks','paper')
    search_fields = ('test_id','question_type','positive_marks')

admin.site.register(question,questionAdmin)


class question_answerAdmin(admin.ModelAdmin):
    list_display = ('id','question_no','answer','question_id')

admin.site.register(question_answer,question_answerAdmin)


class question_optionsAdmin(admin.ModelAdmin):
    list_display = ('id','question_no','option_name','option','question_id')

admin.site.register(question_options,question_optionsAdmin)

class student_answerAdmin(admin.ModelAdmin):
    list_display = ('id','question_no','answer','time_taken','visited','markforreview','question_id','student_id','test_id','answer_result')

admin.site.register(student_answer,student_answerAdmin)

class test_statusAdmin(admin.ModelAdmin):
    list_display = ('id','incomplete','completed','date','total_time','use_time','rank','total_marks','student_id','test_id')

admin.site.register(test_status,test_statusAdmin)

#the following class is use to show test add form (show) testseries packages 
class notesInline(admin.TabularInline):
    model = notes

class notes_packageAdmin(admin.ModelAdmin):
    list_display = ('id','name','date','exam_for','premium','status')
    inlines = [notesInline]

admin.site.register(notes_package,notes_packageAdmin)


class notesAdmin(admin.ModelAdmin):
    list_display = ('id','title','subject_name','date','file_name','status','notes_package_id')

admin.site.register(notes,notesAdmin)

#the following class is use to show student admin add form (show) student info 
class videosInline(admin.TabularInline):
    model = videos

class video_packageAdmin(admin.ModelAdmin):
    list_display = ('id','package_name','date','status')
    inlines = [videosInline]

admin.site.register(video_package,video_packageAdmin)

class duplicate_videoInline(admin.TabularInline):
    model = duplicate_video

class videosAdmin(admin.ModelAdmin):
    list_display = ('id','package_name','title','subject_name','file_name','thumbnail','date','premium','video_length','status','video_package_id','quality','video_no')
    inlines = [duplicate_videoInline]

    #the following function used to show the package name
    def package_name(self,obj):
        return obj.video_package.package_name

admin.site.register(videos,videosAdmin)


class duplicate_videoAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_title', 'get_subject','file_name','quality')

    def get_title(self, obj):
        return obj.video.title if obj.video else None

    def get_subject(self, obj):
        return obj.video.subject_name if obj.video else None

    get_title.short_description = 'title'
    get_subject.short_description = 'subject_name'

admin.site.register(duplicate_video,duplicate_videoAdmin)


class course_videoAdmin(admin.ModelAdmin):
    list_display = ('id','course_id','video_package_id','status')

admin.site.register(course_video,course_videoAdmin)

'''
class course_testseriesAdmin(admin.ModelAdmin):
    list_display = ('id','course_id','testseries_id','status')

admin.site.register(course_testseries,course_testseriesAdmin)
'''

class course_notesAdmin(admin.ModelAdmin):
    list_display = ('id','course_id','notes_package_id','status')

admin.site.register(course_notes,course_notesAdmin)

class course_enrollAdmin(admin.ModelAdmin):
    list_display = ('id','course_id','student_id','datetime','amount','order_id','status','validity','remaning_days')

admin.site.register(course_enroll,course_enrollAdmin)

class testseries_enrollAdmin(admin.ModelAdmin):
    list_display = ('id','testseries_id','student_id','amount','datetime','order_id','validity','status')

admin.site.register(testseries_enroll,testseries_enrollAdmin)


class TestInstructionAdmin(admin.ModelAdmin):
    list_display = ('id', 'exam', 'instruction_1', 'instruction_2')

admin.site.register(TestInstruction, TestInstructionAdmin)

class question_solutionAdmin(admin.ModelAdmin):
    list_display = ('id','question','question_no','solution_type','solution')

admin.site.register(question_solution,question_solutionAdmin)


class student_test_statusAdmin(admin.ModelAdmin):
    list_display = ('id','student_id','test_id','accuracy','attempted_question','correct_question','incorrect_question','left_question')

admin.site.register(student_test_status,student_test_statusAdmin)

class PromotionalVideoAdmin(admin.ModelAdmin):
    list_display = ('id','caption','video','thumbnail','status')

admin.site.register(PromotionalVideo,PromotionalVideoAdmin)

class IndexContentAdmin(admin.ModelAdmin):
    list_display = ('id','logo','poster','status')

admin.site.register(IndexContent,IndexContentAdmin)

class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('id','about','status')

admin.site.register(AboutUs,AboutUsAdmin)


class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('id','name','mobile','query')

admin.site.register(ContactForm,ContactFormAdmin)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id','student','test','feedback')

admin.site.register(Feedback,FeedbackAdmin)


class WatchHistoryAdmin(admin.ModelAdmin):
    list_display = ('id','student_id','video_id','watch_time','current_status')

admin.site.register(WatchHistory,WatchHistoryAdmin)



