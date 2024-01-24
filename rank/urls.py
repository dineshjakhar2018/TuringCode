from django.urls import path
from . import views

urlpatterns = [
    path('ugcnet-rank-predictor/',views.ugcnetrankpredictor,name="ugcnetrankpredictor"),
    path('ugcnet-student-save/',views.UgcNetStudentData,name="ugcnetstudentsave"),
    path('verify-email-otp/',views.verify_email_otp,name="verify_email_otp"),
    path('ugcnet-response/', views.examrank, name='ugcnet_response'),

    path('gate-rank-predictor/',views.gate_rank_predictor,name="gaterankpredictor"),
    path('gate-student-response/',views.GateStudentResponse,name="GateStudentResponse"),
    path('gate-verify-email-otp/',views.gate_verify_email_otp,name="gate_verify_email_otp"),
    path('gate-response/', views.GateResponseSolution, name='gate_response'),
]