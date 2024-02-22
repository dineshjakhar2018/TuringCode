from django.contrib import admin
from .models import UgcNetStudent,UgcNetAnswerKey,UgcNetExam,UgcNetExpectedCutOff,GateExam,GateAnswerKey,GateStudent,GateQualifyMarks,GateAIRvsMarks,GateNewExam,GateNewAnswerKey,GateNewStudent,GateNewQualifyMarks,GateNewAIRvsMarks

#ugc exam rank predictor

class UgcNetExamAdmin(admin.ModelAdmin):
    list_display = ('id','name','subject','shift','session','year')

admin.site.register(UgcNetExam,UgcNetExamAdmin)

class UgcNetAnswerKeyAdmin(admin.ModelAdmin):
    list_display = ('id','ugcnetexam','question_id','answer','paper','positive_marks','negative_marks')

admin.site.register(UgcNetAnswerKey,UgcNetAnswerKeyAdmin)

class UgcNetStudentAdmin(admin.ModelAdmin):
    list_display = ('id','ugcnetexam','email','mobile','otp','email_verify','application_no','candidate_name','roll_no','test_date','test_time','url','total_marks','question_attempted','correct_question','category')

admin.site.register(UgcNetStudent,UgcNetStudentAdmin)

class UgcNetExpectedCutOffAdmin(admin.ModelAdmin):
    list_display = ('id','ugcnetexam','category','jrf','assistant_professor')

admin.site.register(UgcNetExpectedCutOff,UgcNetExpectedCutOffAdmin)


#gate rank 
class GateExamAdmin(admin.ModelAdmin):
    list_display = ('id','subject', 'noofshift', 'shift', 'year','mean_top_marks')

class GateStudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'shift', 'positive_marks', 'negative_marks', 'total_marks', 'attempted', 'correct', 'incorrect', 'gatescore')
    list_filter = ('exam', 'subject', 'shift')
    search_fields = ('name', 'email')

class GateAnswerKeyAdmin(admin.ModelAdmin):
    list_display = ('id','q_no', 'q_type', 'answer', 'marks', 'negative_marks', 'exam')

class GateQualifyMarksAdmin(admin.ModelAdmin):
    list_display = ('id','category', 'marks', 'exam')

class GateAIRvsMarksAdmin(admin.ModelAdmin):
    list_display = ('id', 'marks','air', 'exam')


# Register your models with the admin site
admin.site.register(GateExam, GateExamAdmin)
admin.site.register(GateStudent, GateStudentAdmin)
admin.site.register(GateAnswerKey, GateAnswerKeyAdmin)
admin.site.register(GateQualifyMarks, GateQualifyMarksAdmin)
admin.site.register(GateAIRvsMarks, GateAIRvsMarksAdmin)


#new gate rank(with url response)
class GateNewExamAdmin(admin.ModelAdmin):
    list_display = ('id','subject', 'noofshift', 'shift', 'year','mean_top_marks')

class GateNewStudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'candidateid', 'subject', 'shift', 'positive_marks', 'negative_marks', 'total_marks', 'attempted', 'correct', 'incorrect', 'gatescore')
    list_filter = ('exam', 'subject', 'shift')
    search_fields = ('name', 'candidateid')

class GateNewAnswerKeyAdmin(admin.ModelAdmin):
    list_display = ('id','q_id', 'q_type', 'answer', 'marks', 'negative_marks', 'exam')

class GateNewQualifyMarksAdmin(admin.ModelAdmin):
    list_display = ('id','category', 'marks', 'exam')

class GateNewAIRvsMarksAdmin(admin.ModelAdmin):
    list_display = ('id', 'marks','air', 'exam')


# Register your models with the admin site
admin.site.register(GateNewExam, GateNewExamAdmin)
admin.site.register(GateNewStudent, GateNewStudentAdmin)
admin.site.register(GateNewAnswerKey, GateNewAnswerKeyAdmin)
admin.site.register(GateNewQualifyMarks, GateNewQualifyMarksAdmin)
admin.site.register(GateNewAIRvsMarks, GateNewAIRvsMarksAdmin)