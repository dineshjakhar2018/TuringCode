from django.shortcuts import render
from .models import UgcNetStudent,UgcNetAnswerKey,UgcNetExam,UgcNetExpectedCutOff,GateExam,GateAnswerKey,GateStudent,GateQualifyMarks,GateAIRvsMarks
import random
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Q
from django.core.mail import send_mail
from django.shortcuts import render,redirect
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags



#ugc net rank predictor views
def extract_table_data(table):
    table_data = {}
    rows = table.find_all('tr')

    for row in rows:
        columns = row.find_all(['td', 'th'])
        if len(columns) == 2:
            key = columns[0].text.strip().replace(':', '')
            value = columns[1].text.strip()
            table_data[key] = value

    # Additional check for 'Chosen Option' in case it's in a different structure
    chosen_option_column = table.find('td', string='Chosen Option :')
    if chosen_option_column:
        table_data['Chosen Option'] = chosen_option_column.find_next('td', class_='bold').text.strip()

    return table_data


def examrank(request):
    if request.session.get('rank_predictor_email'):
        try:
            ugcnetstudent = UgcNetStudent.objects.get(email = request.session.get('rank_predictor_email'))
            url = ugcnetstudent.url


            # Make a request to the specified URL
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP errors

            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'lxml')

            response_tables = soup.find_all('table', {'class': 'menu-tbl'})

            AttemptedQuestionPaper1 = 0
            AttemptedQuestionPaper2 = 0
            CorrectQuestionPaper1 = 0
            CorrectQuestionPaper2 = 0
            PositiveMarksinPaper1 = 0
            PositiveMarksinPaper2 = 0
            NegativeMarksinPaper1 = 0
            NegativeMarksinPaper2 = 0



            for response_table in response_tables:
                # Extract data from the table
                table_data = extract_table_data(response_table)

                # Skip saving if the data is empty
                if not any(table_data.values()):
                    continue

                # Print the extracted data for debugging
                #print("Extracted Data:", table_data)

                #get the data of current question
                ugcnetanswerkey = UgcNetAnswerKey.objects.get(question_id=str(table_data.get('Question ID ', '')),ugcnetexam = ugcnetstudent.ugcnetexam)

                CurrentQuesAnswer = ugcnetanswerkey.answer.split(" or ")

                #check if question is attempted or not
                if table_data.get('Status ','') == 'Answered':
                    if ugcnetanswerkey.paper == 1:
                        AttemptedQuestionPaper1 += 1

                        if str(table_data.get('Chosen Option', '')) in CurrentQuesAnswer or str(ugcnetanswerkey.answer) == 'MTA':
                            CorrectQuestionPaper1 += 1
                            PositiveMarksinPaper1 += ugcnetanswerkey.positive_marks
                        else:
                            NegativeMarksinPaper1 += ugcnetanswerkey.negative_marks

                    if ugcnetanswerkey.paper == 2:
                        AttemptedQuestionPaper2 = AttemptedQuestionPaper2 + 1

                        if str(table_data.get('Chosen Option', '')) in CurrentQuesAnswer or str(ugcnetanswerkey.answer) == 'MTA':
                            CorrectQuestionPaper2 += 1
                            PositiveMarksinPaper2 += ugcnetanswerkey.positive_marks
                        else:
                            NegativeMarksinPaper2 += ugcnetanswerkey.negative_marks
                else:
                    if str(ugcnetanswerkey.answer) == 'MTA':
                        if ugcnetanswerkey.paper == 1:
                            CorrectQuestionPaper1 += 1
                            PositiveMarksinPaper1 += ugcnetanswerkey.positive_marks
                        
                        if ugcnetanswerkey.paper == 2:   
                            CorrectQuestionPaper2 += 1
                            PositiveMarksinPaper2 += ugcnetanswerkey.positive_marks

                td_element = soup.find('td',text=str(table_data.get('Question ID ', '')))

                # Check if the td element is found and navigate up to its parent table
                if td_element:
                    table_to_modify = td_element.find_parent('table', class_='menu-tbl')
                    
                    # Check if the table is found
                    if table_to_modify:
                        #print("Question ID = ",str(table_data.get('Question ID ', '')),"   Choice Option = ",str(table_data.get('Chosen Option', '')),"     Correct Answer = ",ugcnetanswerkey.answer)
                        if ugcnetanswerkey.answer == str(table_data.get('Chosen Option', '')) or str(ugcnetanswerkey.answer) == 'MTA':
                            # Change the border color of the table
                            table_to_modify['style'] = 'border: 2px solid green;'

                            # Create a new tr element with the desired content
                            new_tr = soup.new_tag('tr')


                            # Create new td element with text content, align="right" attribute, and style attributes
                            td_marks = soup.new_tag('td', align='right', style='font-size: 16px;font-weight:bold; color: green;')
                            td_marks.append('Your Marks:')
                            
                            # Create new td element with text content, class="bold" attribute, and style attributes
                            td_plus_two = soup.new_tag('td', class_='bold', style='font-size: 16px; font-weight:bold; color: green;')

                            td_plus_two.append('+'+str(ugcnetanswerkey.positive_marks))
                        else:
                            # Change the border color of the table
                            table_to_modify['style'] = 'border: 2px solid red;'

                            # Create a new tr element with the desired content
                            new_tr = soup.new_tag('tr')

                        
                            # Create new td element with text content, align="right" attribute, and style attributes
                            td_marks = soup.new_tag('td', align='right', style='font-size: 16px;font-weight:bold; color: red;')
                            td_marks.append('Your Marks:')
                            
                            # Create new td element with text content, class="bold" attribute, and style attributes
                            td_plus_two = soup.new_tag('td', class_='bold', style='font-size: 16px; font-weight:bold; color: red;')

                            td_plus_two.append('-'+str(ugcnetanswerkey.negative_marks))


                        # Append the new td elements to the new tr element
                        new_tr.append(td_marks)
                        new_tr.append(td_plus_two)

                        # Find the parent tr of the td element
                        td_element = soup.find('td',class_="bold",text=str(table_data.get('Question ID ', '')))
                        parent_tr = td_element.find_parent('tr')

                        # Check if the parent tr is found
                        if parent_tr:
                            # Insert the new tr element after the parent tr
                            parent_tr.insert_after(new_tr)


            # Update image URLs to absolute URLs
            for img_tag in soup.find_all('img'):
                img_src = img_tag.get('src')
                if img_src and not img_src.startswith(('http://', 'https://')):
                    img_tag['src'] = urljoin(url, img_src)
            
            Attempted = AttemptedQuestionPaper1 + AttemptedQuestionPaper2
            TotalMarks = (PositiveMarksinPaper1 + PositiveMarksinPaper2) - (NegativeMarksinPaper1 + NegativeMarksinPaper2)
            TotalCorrect = CorrectQuestionPaper1 + CorrectQuestionPaper2

            #if same data then not save other change 
            if ugcnetstudent.total_marks != TotalMarks or ugcnetstudent.question_attempted != Attempted or ugcnetstudent.correct_question != TotalCorrect:
                ugcnetstudent.total_marks = TotalMarks
                ugcnetstudent.question_attempted = Attempted
                ugcnetstudent.correct_question = TotalCorrect
                ugcnetstudent.save()

            
            RankInStudentCategory = UgcNetStudent.objects.filter(category=ugcnetstudent.category, total_marks__gt=TotalMarks).values('roll_no').distinct().count()
            Rank = UgcNetStudent.objects.filter(total_marks__gt=TotalMarks).values('roll_no').distinct().count()

            TotalStudent = UgcNetStudent.objects.filter(ugcnetexam = ugcnetstudent.ugcnetexam).values('roll_no').distinct().count()
            TotalStudentCategory = UgcNetStudent.objects.filter(category=ugcnetstudent.category,ugcnetexam = ugcnetstudent.ugcnetexam).values('roll_no').distinct().count()
            
            if ugcnetstudent.category == 'UNRESERVED' or ugcnetstudent.category == 'EWS' or ugcnetstudent.category == 'OBC(NCL)' or ugcnetstudent.category == 'SC':
                ExpectedCutoff = UgcNetExpectedCutOff.objects.filter(Q(category='UNRESERVED') | Q(category='OBC(NCL)') | Q(category='EWS') | Q(category='SC') ,ugcnetexam=ugcnetstudent.ugcnetexam)
            else:
                ExpectedCutoff = UgcNetExpectedCutOff.objects.filter(Q(category='UNRESERVED') | Q(category='OBC(NCL)') | Q(category='EWS') | Q(category=str(ugcnetstudent.category)) ,ugcnetexam=ugcnetstudent.ugcnetexam)
            
            #count total question in paper 1 
            TotalQuestionInPaper1 = UgcNetAnswerKey.objects.filter(ugcnetexam=ugcnetstudent.ugcnetexam,paper = 1).count()

            #count total question in paper 2
            TotalQuestionInPaper2 = UgcNetAnswerKey.objects.filter(ugcnetexam=ugcnetstudent.ugcnetexam, paper = 2).count()

            #user category expected cutoff for JRF
            StudentCategoryCutoff = UgcNetExpectedCutOff.objects.get(category=str(ugcnetstudent.category),ugcnetexam=ugcnetstudent.ugcnetexam)

            data = {
                    'AttemptedQuestionPaper1': AttemptedQuestionPaper1,
                    'AttemptedQuestionPaper2' : AttemptedQuestionPaper2,
                    'TotalQuestionAttempted' : Attempted,
                    'CorrectQuestionPaper1' : CorrectQuestionPaper1,
                    'CorrectQuestionPaper2' : CorrectQuestionPaper2,
                    'TotalCorrectQuestion': TotalCorrect,
                    'IncorrectQuestionPaper1' : AttemptedQuestionPaper1 - CorrectQuestionPaper1,
                    'IncorrectQuestionPaper2' : AttemptedQuestionPaper2 - CorrectQuestionPaper2,
                    'TotalMarksPaper1' : PositiveMarksinPaper1 - NegativeMarksinPaper1,
                    'TotalMarksPaper2':PositiveMarksinPaper2 - NegativeMarksinPaper2,
                    'PositiveMarksinPaper1' :PositiveMarksinPaper1,
                    'PositiveMarksinPaper2':PositiveMarksinPaper2,
                    'NegativeMarksinPaper1':NegativeMarksinPaper1,
                    'NegativeMarksinPaper2':NegativeMarksinPaper2,
                    'TotalPositiveMarks':PositiveMarksinPaper1 + PositiveMarksinPaper2,
                    'TotalNegativeMarks':NegativeMarksinPaper1 + NegativeMarksinPaper2,
                    'TotalQuestionInPaper1':TotalQuestionInPaper1,
                    'TotalQuestionInPaper2':TotalQuestionInPaper2,
                    'TotalQuestionInPaper' : TotalQuestionInPaper1 + TotalQuestionInPaper2,
                    'TotalMarks' : TotalMarks,
                    'ExpectedCutoff':ExpectedCutoff,
                    'RankInStudentCategory':RankInStudentCategory + 1,
                    'Rank':Rank + 1,
                    'TotalStudent':TotalStudent,
                    'TotalStudentCategory' : TotalStudentCategory,
                    'StudentCategory':ugcnetstudent.category,
                    'ExpectedNetCutOff': StudentCategoryCutoff.assistant_professor,
                    'ExpectedJrfCutoff' : StudentCategoryCutoff.jrf,
            }


            # Render the modified HTML content
            modified_html = str(soup)
            return render(request, 'ugcnet-response.html', {'data':data,'modified_html': modified_html,})

        except requests.RequestException as e:
            print("ugc net response error = ",e)
            return render(request, 'ugc_rank_predictor.html', {'error_message': ""})

        except Exception as e:
            return render(request, 'ugc_rank_predictor.html', {'error_message': f"Error: {str(e)}"})
    else:
        return render(request,'ugc_rank_predictor.html',{'context':''})


def ugcnetrankpredictor(request):
    #index page of ugc net rank predictor
    return render(request,'ugc_rank_predictor.html',{'context':''})


def UgcNetStudentData(request):
    try:
        request.session.flush()
        if request.method == 'POST':
            # Extract data from the POST request
            email = request.POST.get('email')
            mobile = request.POST.get('mobile')
            category = request.POST.get('category')
            url = request.POST.get('url')
            examname = request.POST.get('examname')
            subject = request.POST.get('subject')
            shift = request.POST.get('shift')

            # Perform additional backend validations if needed

            # Send email verification OTP
            otp = generate_otp()
            #send_otp_email(email, otp)
            
            try:
                UgcNetExam.objects.get(name=examname, subject=subject, shift=shift)
                

                #get the data from url
                response = requests.get(url)
                response.raise_for_status()  # Check for HTTP errors

                    # Parse the HTML content of the page
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract data for UgcNetStudent
                student_table = soup.find('table', {'border': '1', 'cellpadding': '1', 'cellspacing': '1', 'style': 'width:500px'})
                rows = student_table.find_all('tr')

                ugc_net_student_data = {}

                for row in rows:
                    columns = row.find_all('td')
                    if len(columns) == 2:
                        key = columns[0].text.strip()
                        value = columns[1].text.strip()
                        ugc_net_student_data[key] = value
                    
                    
                #getexam id 
                currentexam = UgcNetExam.objects.get(name=examname, subject=subject, shift=shift)

                #check if student already registered
                try:
                    ugcnetstudentregisted = UgcNetStudent.objects.get(email = email)
                    ugcnetstudentregisted.url = url
                    ugcnetstudentregisted.save()
                    #return JsonResponse({'status':'success','email_already_verified':'0'})
                except:
                    #store data in database if user check rank first time
                    # Create UgcNetStudent instance and save to the database
                    ugc_net_student = UgcNetStudent.objects.create(
                        ugcnetexam = currentexam,
                        email = email,
                        mobile = mobile,
                        category = category,
                        url = url,
                        otp = otp,
                        email_verify = 0,
                        application_no=ugc_net_student_data.get('Application No', ''),
                        candidate_name=ugc_net_student_data.get('Candidate Name', ''),
                        roll_no=ugc_net_student_data.get('Roll No', ''),
                        test_date=ugc_net_student_data.get('Test Date', ''),
                        test_time=ugc_net_student_data.get('Test Time', ''),
                        total_marks = 0,
                        question_attempted = 0,
                        correct_question = 0
                        )
            except Exception as e:
                print("something went wrong",e)
                return JsonResponse({'status': 'error'})


            #store email in session for student response view
            request.session['rank_predictor_email'] = email

            #store email in session for student response view
            request.session['rank_predictor_url'] = url

            # Store the OTP in session for verification
            request.session['email_verification_otp'] = otp

            #print("ugc net rank predictor otp is = ",otp)

            send_email('Email Verification for Turing Code UGC NET/JRF Rank Predictor',email,otp,'UGCNET')

            # Return success response
            return JsonResponse({'status': 'success'})
        else:
            print("error")
            return JsonResponse({'status': 'error'})
    except Exception as e:
        print("ugc net form submit error is ",e)

def generate_otp():
    return str(random.randint(100000, 999999))


def verify_email_otp(request):
    if request.method == 'POST':
        user_entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('email_verification_otp')
        print("user_entered_otp = ",user_entered_otp)
        print('stored_otp',stored_otp)
        if user_entered_otp == stored_otp:
            ugcnetstudentregisted = UgcNetStudent.objects.get(email = request.session.get('rank_predictor_email'))
            ugcnetstudentregisted.email_verify = 1
            ugcnetstudentregisted.save()
            # Email verification successful, redirect to another page
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'error': 'Invalid OTP'})
    else:
        return JsonResponse({'status': 'error', 'error': 'Something went wrong please try again.'})
    


def gate_rank_predictor(request):
    #index page of ugc net rank predictor
    return render(request,'gate-rank-predictor.html',{'context':''})


def GateStudentResponse(request):
    request.session.flush()
    if request.method == 'POST':
        # Extract data from the POST request
        email = request.POST.get('email')
        name = request.POST.get('name')
        #mobile = request.POST.get('mobile')
        #category = request.POST.get('category')
        response = request.POST.get('response')
        subject = request.POST.get('subject')
        shift = request.POST.get('shift')

        # Send email verification OTP
        otp = generate_otp()
        #send_otp_email(email, otp)
        try:    
            #getexam id 
            #artificial exam only in one shift 
            if subject == 'Computer Science & Information Technology':
                currentexam = GateExam.objects.get(subject=subject, shift=shift)
            else:
                currentexam = GateExam.objects.get(subject=subject)
            
            #check if student already registered
            try:
                Student = GateStudent.objects.get(email = email,shift=shift,subject=subject)
            except:
                #store data in database if user check rank first time
                # Create UgcNetStudent instance and save to the database
                gate_student = GateStudent.objects.create(
                    exam = currentexam,
                    name = name,
                    email = email,
                    subject = subject,
                    shift = shift,
                    positive_marks = 0,
                    negative_marks = 0,
                    total_marks = 0,
                    attempted = 0,
                    correct = 0,
                    incorrect = 0,
                    gatescore = 0,
                    response = response,
                    )
                print("student data save",gate_student)
        except Exception as e:
            print("something went wrong",e)
            return JsonResponse({'status': 'error'})


        #store email in session for student response view
        request.session['gate_rank_predictor_email'] = email

        #store email in session for student response view
        request.session['gate_rank_predictor_subject'] = subject

        #store email in session for student response view
        request.session['gate_rank_predictor_shift'] = shift

        #store email in session for student response view
        request.session['gate_rank_predictor_response'] = response

        # Store the OTP in session for verification
        request.session['gate_email_verification_otp'] = otp
        
        
        send_email('Email Verification for Turing Code GATE Rank Predictor',email,otp,'GATE')

        # Return success response
        return JsonResponse({'status': 'success'})
    else:
        print("error")
        return JsonResponse({'status': 'error'})
    

def gate_verify_email_otp(request):
    if request.method == 'POST':
        user_entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('gate_email_verification_otp')
        if user_entered_otp == stored_otp:
            # Email verification successful, redirect to another page
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'error': 'Invalid OTP'})
    else:
        return JsonResponse({'status': 'error', 'error': 'Something went wrong please try again.'})


def GateResponseSolution(request):
    if request.session.get('gate_rank_predictor_email') and request.session.get('gate_rank_predictor_response') and request.session.get('gate_rank_predictor_subject') and request.session.get('gate_rank_predictor_shift'):
        try:
            email = request.session.get('gate_rank_predictor_email')
            subject = request.session.get('gate_rank_predictor_subject')
            shift = request.session.get('gate_rank_predictor_shift')
            gatestudent = GateStudent.objects.get(email = email,subject=subject,shift = shift)
            response = request.session.get('gate_rank_predictor_response')

            AttemptedMark1Ques = 0
            AttemptedMark2Ques = 0
            CorrectMark1Ques = 0
            CorrectMark2Ques = 0
            Positive1Marks = 0
            Positive2Marks = 0
            Negative1Marks = 0
            Negative2Marks = 0

            if response:
                lines = response.split('\n')
                for line in lines:
                    values = line.split()
                    for i in range(0, len(values), 3):
                        qno, your_ans, q_type = values[i:i+3]
                        #print(qno,  your_ans, q_type)

                        if not qno.isdigit():
                            continue


                        #get the data of current question
                        gateanswerkey = GateAnswerKey.objects.get(q_no=int(qno),exam = gatestudent.exam)

                        #split answer because one question have multiple answer like (2 or 4)
                        QuesAns = gateanswerkey.answer.split(" or ")

                        #check if question is attempted or not
                        #-- means question not attempted
                        if '--' not in your_ans:
                                if q_type == 'MCQ' or q_type == 'MSQ':
                                    if your_ans in QuesAns or gateanswerkey.answer == 'MTA':
                                        #if question is 1 marks
                                        if gateanswerkey.marks == 1:
                                            AttemptedMark1Ques += 1
                                            CorrectMark1Ques += 1
                                            Positive1Marks += 1
                                        else:
                                            AttemptedMark2Ques +=  1
                                            CorrectMark2Ques += 1
                                            Positive2Marks += 2
                                    else:
                                        #if question is 1 marks
                                        if gateanswerkey.marks == 1:
                                            AttemptedMark1Ques += 1
                                            Negative1Marks += gateanswerkey.negative_marks
                                        else:
                                            AttemptedMark2Ques += 1
                                            Negative2Marks +=  gateanswerkey.negative_marks
                                else:
                                    #Question is NAT
                                    if 'to' in gateanswerkey.answer:
                                        NatAnswer = gateanswerkey.answer.split(' to ')
                                        #correct answer
                                        if float(your_ans) >= float(NatAnswer[0])  and float(your_ans) <= float(NatAnswer[1]):
                                            #if question is 1 marks
                                            if gateanswerkey.marks == 1:
                                                AttemptedMark1Ques += 1
                                                CorrectMark1Ques += 1
                                                Positive1Marks +=  1
                                            else:
                                                AttemptedMark2Ques += 1
                                                CorrectMark2Ques += 1
                                                Positive2Marks += 2
                                        else:   
                                            #if question is 1 marks
                                            if gateanswerkey.marks == 1:
                                                AttemptedMark1Ques += 1
                                                Negative1Marks += gateanswerkey.negative_marks
                                            else:
                                                AttemptedMark2Ques += 1
                                                Negative2Marks += gateanswerkey.negative_marks

                                    elif your_ans in QuesAns or gateanswerkey.answer == 'MTA':
                                        #if question is 1 marks
                                        if gateanswerkey.marks == 1:
                                            AttemptedMark1Ques += 1
                                            CorrectMark1Ques += 1
                                            Positive1Marks += 1
                                        else:
                                            AttemptedMark2Ques += 1
                                            CorrectMark2Ques += 1
                                            Positive2Marks += 2
                                    else:
                                        #if question is 1 marks
                                        if gateanswerkey.marks == 1:
                                            AttemptedMark1Ques += 1
                                            Negative1Marks += gateanswerkey.negative_marks
                                        else:
                                            AttemptedMark2Ques += 1
                                            Negative2Marks += gateanswerkey.negative_marks

                        else:
                            #question not attempted but check MTA (Mark to All)
                            if gateanswerkey.answer == 'MTA':
                                if gateanswerkey.marks == 1:
                                    CorrectMark1Ques += 1
                                    Positive1Marks += 1
                                else:
                                    CorrectMark2Ques += 1
                                    Positive2Marks += 1
            
            #total student check this rank till now
            total_current_student = GateStudent.objects.filter(exam=gatestudent.exam).exclude(attempted = 0).count()

            #Total 1 marks questions
            total_1_marks_questions = GateAnswerKey.objects.filter(exam = gatestudent.exam,marks = 1).count()

            #Total 2 marks questions
            total_2_marks_questions = GateAnswerKey.objects.filter(exam=gatestudent.exam,marks=2).count()

            #total questions
            total_question_in_paper = total_1_marks_questions + total_2_marks_questions

            #total attempted questions
            total_attempted = AttemptedMark1Ques + AttemptedMark2Ques

            #total Correct questions
            total_correct_question = CorrectMark1Ques + CorrectMark2Ques

            #attempted %
            attempted_avg = total_attempted / total_question_in_paper
            attempted_avg = round(attempted_avg, 2)
            
            #accuracy
            accuracy = total_correct_question / total_attempted 
            accuracy = round(accuracy,2)

            #total marks 
            TotalMarks = (Positive1Marks + Positive2Marks) - (Negative1Marks + Negative2Marks)

            #normalization marks 

            #gate score 

            #estimate air rank 

            #current rank


            data = {
                'AttemptedMark1Ques':AttemptedMark1Ques,
                'AttemptedMark2Ques':AttemptedMark2Ques,
                'total_attempted':total_attempted,
                'total_1_marks_questions':total_1_marks_questions,
                'total_2_marks_questions':total_2_marks_questions,
                'total_question_in_paper':total_question_in_paper,
                'CorrectMark1Ques':CorrectMark1Ques,
                'CorrectMark2Ques':CorrectMark2Ques,
                'total_correct_question':total_correct_question,
                'Positive1Marks':Positive1Marks,
                'Positive2Marks':Positive2Marks,
                'total_positive_marks':Positive1Marks + Positive2Marks,
                'Negative1Marks':Negative1Marks,
                'Negative2Marks':Negative2Marks,
                'total_negative':Negative1Marks + Negative2Marks,
                'total_1_mark':Positive1Marks - Negative1Marks,
                'total_2_mark':Positive2Marks - Negative2Marks,
                'TotalMarks':TotalMarks,
                'current_rank' : '1',
                'total_current_student':total_current_student,
                'air':'1454 - 1972',
                'subject' : gatestudent.subject, 
            }

            gatestudent.attempted = total_attempted
            gatestudent.positive_marks = Positive1Marks + Positive2Marks
            gatestudent.negative_marks = Negative1Marks + Negative2Marks
            gatestudent.total_marks = TotalMarks
            gatestudent.correct = total_correct_question
            gatestudent.incorrect = total_attempted - total_correct_question
            gatestudent.save()


            '''
            print("TotalMarks = ",TotalMarks)
            print("Attempted 1 Mark Question",AttemptedMark1Ques)
            print("Attempted 2 Mark Question",AttemptedMark2Ques)
            print("Correct 1 Mark Question",CorrectMark1Ques)
            print("Correct 2 Mark Question",CorrectMark2Ques)
            print("Positive 1 Marks",Positive1Marks)
            print("Positve 2 Marks",Positive2Marks)
            print("Negative 1 Marks",Negative1Marks)
            print("Negative 2 Marks",Negative2Marks)
            '''

            print("yes")

            return render(request,'gate-response.html',{'data':data})
        except Exception as e:
            print("the error is = ",e)
            return redirect('gaterankpredictor')
    else:
        return redirect('gaterankpredictor')
    


def send_email(Subject,StudentEmail,Otp,EmailType):
    
    try:
        if EmailType == 'UGCNET':
            Student = UgcNetStudent.objects.get(email = StudentEmail)
            # Assuming you have a user or username to personalize the email
            StudentName = Student.candidate_name

            html_message = render_to_string('email.html', {'StudentName': StudentName,'otp':Otp,'email_type':EmailType})
        
        else:
            Student = GateStudent.objects.get(email = StudentEmail)
            # Assuming you have a user or username to personalize the email
            StudentName = Student.name

            html_message = render_to_string('email.html', {'StudentName': StudentName,'otp':Otp,'email_type':EmailType})

        # Create a plain text version of the HTML content
        plain_message = strip_tags(html_message)

        # Create the EmailMultiAlternatives object
        email = EmailMultiAlternatives(
            str(Subject),#email subject
            plain_message,  # Plain text message
            settings.EMAIL_HOST_USER,  # Sender's email address
            [str(StudentEmail)],  # List of recipient email addresses
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
    except Exception as e:
        print("email not send because ",e)
        return False