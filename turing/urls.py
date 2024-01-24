from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path('contact', views.ContactUs, name = 'contact_us'),
    path('contact-form',views.Contact_Form,name='contact_form'),
    path('about' , views.About_US, name = 'about_us'),
    path('test-series-content/<slug:testseries_slug>',views.Test_Series_Content,name = 'test_series_content'),
    path('course-details/<slug:course_slug>',views.Course_Content,name="course_content"),
    path('privacy-policy',views.PrivacyPolicy,name='privacy-policy'),
    path('terms&conditions',views.TermsAndCondition,name="terms&conditions"),
    path('refund-policy',views.RefundPolicy,name='refund-policy'),


    path('home/',views.home,name='home'),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('email-verify/',views.email_verify,name='email-verify'),
    path('otp-resend/',views.otp_resend,name='otp-resend'),
    path('forgot/',views.forgot,name='forgot'),
    path('forgot-verify/',views.forgot_verify,name='forgot-verify'),
    path('forgot-otp-resend/',views.forgot_otp_resend,name='forgot-otp-resend'),
    path('forgot-pass/',views.forgot_pass,name='forgot-pass'),
    path('logout/',views.logout,name='logout'),
    path('courses/',views.courses,name='courses'),
    path('courses/course-details/<course_slug>',views.course_details,name='course-details'),
    path('courses/course-details/<slug:course_slug>/play-video/<slug:video_slug>',views.play_video,name='play-video'),
    path('courses/course-details/<slug:course_slug>/notes-view/<slug:notes_slug>',views.view_notes,name='notes-view'),
    path('notes/',views.notes_,name='notes'),
    path('notes/notes-list/<slug:notes_package_slug>',views.notes_list,name='notes-list'),
    path('notes/notes-list/<slug:notes_package_slug>/notes-view-1/<slug:notes_slug>',views.view_free_notes,name='notes-view-1'),
    path('courses/course-details/checkout/<slug:slug_1>/<slug:slug_2>',views.checkout,name='checkout'),
    path('courses/course-details/checkout/course-enroll/',views.course_enrolled,name='course-enroll'),
    path('courses/course-details/checkout/course-enroll/invoice/<slug:slug_1>/<slug:slug_2>',views.invoice,name='invoice'),
    path('courses/invoice/<slug:slug_1>/<slug:slug_2>',views.invoice,name='print-invoice'),

    path('test-series/',views.TestSeries,name='test-series'),
    path('test-series/test-series-details/<slug:testseries_slug>',views.testseries_details,name='test-series-details'),
    path('test-series/test-series-details/checkout/<slug:slug_1>/<slug:slug_2>',views.checkout,name='test-checkout'),
    path('test-series/invoice/<slug:slug_1>/<slug:slug_2>',views.invoice,name='test-series-print-invoice'),
    
    path('test-instruction-1/<slug:exam_slug>/<slug:test_slug>',views.TestInstruction_1,name='instruction-1'),
    path('test-instruction-2/<slug:exam_slug>/<slug:test_slug>',views.TestInstruction_2,name='instruction-2'),
    #path('teststart/',views.test_start,name="test-start"),
    path('api/save-elapsed-time/', views.save_elapsed_time_to_database, name='save_elapsed_time'),
    path('api/save-answer/', views.AnswerSave, name='save_answer_next_question'),
    path('api/clear-answer/', views.ClearAnswer, name='clear_answer'),
    #path('api/save-next/', views.SaveNext, name='save_and_next'),
    #path('api/question-reload/', views.QuesReload, name='question_reload'),
    path('api/mark-for-review/', views.MarkForReview, name='mark_for_review'),
    path('api/paper-change/', views.PaperChange, name='paper_change'),
    #path('api/paper-change-2/', views.PaperChange_2, name='paper_change_2'),
    path('api/question-change/', views.QuestionChange, name='question_change'),
    path('api/previous-question/', views.PreviousQuestion, name='previous_question'),
    path('test-submit/', views.TestSubmit, name='test_submit'),
    path('new-test/test-submit/', views.TestSubmit, name='teststart_test_submit'),
    path('test-error/', views.TestError, name='test_error'),
    path('test-feedback/', views.TestFeedback, name='test_feedback'),

    path('test-series/test-series-details/test-comparison-report/<slug:testseries_slug>/<slug:test_slug>',views.TestComparisonReport,name="test_comparision_report"),
    path('test-series/test-series-details/test-comparison-report/test-question-analysis/<slug:testseries_slug>/<slug:test_slug>',views.TestQuestionAnalysis,name="test_question_analysis"),
    path('test-series/test-series-details/test-comparison-report/solutions/<slug:testseries_slug>/<slug:test_slug>',views.Solutions,name="solutions"),

    path('profile/',views.Profile,name="profile"),

    path('new-test/',views.NewTestSeries,name="new_test"),

    path('api/check-current-answer/', views.CurrentQuesAnswer, name='check_current_answer'),

    path('watch_history/', views.watch_history, name='watch_history'),
    path('get_watch_history/', views.get_watch_history, name='get_watch_history'),

    path('pyp/<slug:exam_name>/', views.pyp, name='pyp'),
    path('pyp-solution/<slug:test_slug>',views.pyp_solution,name='pyp_solution'),

]   

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
