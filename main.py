from flask import Flask,render_template,request, flash,redirect, url_for, jsonify,send_file
from config_file import client
from models import *
import secrets
import datetime
from bson import ObjectId
# from datetime import datetime
from random import randint
import json

app = Flask(__name__)

app.secret_key='my_key'

@app.route("/",methods=['POST','GET'])
def classBankNavPage():
    return render_template("classbank_nav.html")

@app.route('/houseMasterRegister',methods=['POST','GET'])
def houseMasterRegisterPage():
    houseMasterFirstName = request.form.get('houseMasterFirstName')
    houseMasterLastName = request.form.get('houseMasterLastName')
    houseClass = request.form.get('houseClass')
    emailId = request.form.get('emailId')
    phoneNumber = request.form.get('phoneNumber')
    refLink = secrets.token_urlsafe()
    password = request.form.get("password")
    houseMasterId = request.form.get('houseMasterId')
    compOfLeaves = 0
    paidLeaves = 6
    casualLeaves = 12
    status = 1
    createdOn = datetime.datetime.now()

    if request.method == 'POST':
        try:
            queryset = HouseMaster.objects(emailId__iexact=emailId)
            if queryset:
                flash("Email already Exists!!!")
                return render_template("teacher_register.html")
        except Exception as e:
            pass

        try:
            queryset = HouseMaster.objects(houseClass__iexact=houseClass)
            if queryset:
                flash("Already "+houseClass+" assigned to someone!!!")
                return render_template("teacher_register.html")
        except Exception as e:
            pass
        house_master = HouseMaster(
            houseMasterFirstName=houseMasterFirstName,
            houseMasterLastName=houseMasterLastName,
            houseClass=houseClass,
            emailId = emailId,
            phoneNumber = phoneNumber,
            refLink = refLink,
            houseMasterId = houseMasterId,
            compOfLeaves = compOfLeaves,
            paidLeaves = paidLeaves,
            casualLeaves = casualLeaves,
            password=password,
            status=status,
            createdOn=createdOn
            )
        house_details = house_master.save()
        if house_details:
            flash("Registration Successfully Completed!!!.")
            return redirect(url_for('houseMasterLoginPage'))
    else:
        return render_template("teacher_register.html")

@app.route('/houseMasterLogin',methods=['POST','GET'])
def houseMasterLoginPage():
    emailId = request.form.get('emailId')
    password = request.form.get('password')

    if emailId and password and request.method=='POST':
        try:
            get_logins = HouseMaster.objects.get(emailId__iexact=emailId,password__exact=password,status__in=[1])
            if get_logins:
                refLink = get_logins.refLink
                # house_master = get_logins.houseMasterFirstName +" "+ get_logins.houseMasterLastName
                # print(house_master)
                return redirect(url_for('studentAmountPage',refLink=refLink))
            else:
                flash("Invalid Credentials!!!")
                return render_template("teacher_login.html")
        except HouseMaster.DoesNotExist as e:
            flash("Invalid Credentials!!!")
            return render_template("teacher_login.html")

    return render_template('teacher_login.html')

@app.route('/houseMasterForgotPassword',methods=['POST','GET'])
def houseMasterForgotPasswordPage():
    emailId = request.form.get("emailId")
    newPassword = request.form.get("newPassword")
    confirmPassword = request.form.get("confirmPassword")
    

    if emailId and newPassword and confirmPassword and request.method=="POST":
        if newPassword==confirmPassword:
            get_master_info = HouseMaster.objects.get(emailId=emailId)
            # print(get_student_info["emailId"])
            if get_master_info.emailId:
                updated_password=get_master_info.update(
                    password=newPassword
                    )
                if updated_password:
                    flash("Password Successfully Changed")
                    return redirect(url_for('houseMasterLoginPage'))
            
        else:
            flash("Password Miss Matched")
            return render_template('teacher_forgot_password.html')
    
    return render_template('teacher_forgot_password.html')

@app.route("/houseMasterLogout",methods=['POST','GET'])
def houseMasterLogoutPage():
    return redirect(url_for('houseMasterLoginPage'))


@app.route("/studentAmount/<refLink>",methods=['POST','GET'])
def studentAmountPage(refLink):
    get_students_details = AmountBank.objects()
    students_list=[]
    student_dict={}
    count=0
    total_amount=0
    get_name = HouseMaster.objects.get(refLink=refLink)
    houseMaster = get_name.houseMasterFirstName +" "+ get_name.houseMasterLastName
    
    for s in get_students_details:
        if s.refLink==refLink:
            count=count+1
            total_amount = total_amount+s.studentTotalAmount
            student_dict={
                "rno":count,
                "studentName":s.studentName,
                "className":s.className,
                "studentTotalAmount":s.studentTotalAmount,
                "link":s.link,
            }
            students_list.append(student_dict)
    return render_template('students_view.html',students_info=students_list,refLink=refLink,houseMaster=houseMaster,total_amount=total_amount)

@app.route("/studentRegister/<refLink>",methods=['POST','GET'])
def studentRegPage(refLink):
    studentName = request.form.get('studentName')
    className = request.form.get('className')
    studentTotalAmount = request.form.get('studentTotalAmount')
    link = secrets.token_urlsafe()
    status = 1
    createdOn = datetime.datetime.now()
    createdOn1=createdOn.strftime("%d-%m-%Y %H:%M:%S")
    try:
        if request.method == 'POST':
            get_house_master = HouseMaster.objects.get(refLink=refLink)
            students_details = AmountBank(
                studentName=studentName,
                className=className,
                studentTotalAmount=studentTotalAmount,
                link=link,
                houseMasterName = get_house_master.houseMasterFirstName+" "+get_house_master.houseMasterLastName,
                refLink=get_house_master.refLink,
                status=status,
                createdOn = createdOn1,
                
                )
            students_details_data= students_details.save()

            if students_details_data:
                flash("Successfully Registered!!!")
                return redirect(url_for('studentAmountPage',refLink=refLink))
            else:
                flash("Required fields are missing!!!")
                return render_template('student_register.html')
    except Exception as e:
        print(e)
    return render_template("student_register.html")

@app.route("/amountDebit/<link>",methods=['POST','GET'])
def amountDebitPage(link):
    debitAmount=request.form.get('debitAmount')
    reasonTaking = request.form.get('reasonTaking')
    takenDebitDate = request.form.get('takenDebitDate')
    amountDebitStatus=2
    createdOn = datetime.datetime.now()
    if request.method=="POST":
        get_data=AmountBank.objects.get(link=link)
        if get_data:
            refLink = get_data.refLink
            total_amount=get_data.studentTotalAmount
            debit_amount = total_amount - int(debitAmount)
            student_trans = StudentTransaction(
                studentId=ObjectId(get_data.id),
                studentName = get_data.studentName,
                debitAmount=debitAmount,
                reasonTaking=reasonTaking,
                takenDebitDate=takenDebitDate,
                amountDebitStatus=amountDebitStatus,
                link=get_data.link,
                createdOn=createdOn,
                )
            student_trans_save=student_trans.save()
            if student_trans_save: 
                student_credit=get_data.update(
                    studentTotalAmount=debit_amount
                    )
                if student_credit:
                    flash("{}, Successfully {} rupees Debited from your wallet".format(student_trans_save.studentName,debitAmount))
                    return redirect(url_for('studentAmountPage',refLink=refLink))
    return render_template('debit.html')

@app.route("/amountCredit/<link>",methods=['POST','GET'])
def amountCreditPage(link):
    creditAmount=request.form.get('creditAmount')
    takenCreditDate = request.form.get('takenCreditDate')
    amountCreditStatus=3
    createdOn = datetime.datetime.now()
    if request.method=="POST":
        get_data=AmountBank.objects.get(link=link)
        if get_data:
            refLink = get_data.refLink
            total_amount=get_data.studentTotalAmount
            credit_amount = total_amount + int(creditAmount)
            student_trans = StudentTransaction(
                studentId=ObjectId(get_data.id),
                studentName = get_data.studentName,
                creditAmount=creditAmount,
                takenCreditDate=takenCreditDate,
                amountCreditStatus=amountCreditStatus,
                link=get_data.link,
                createdOn=createdOn
                )
            student_trans_save=student_trans.save()
            if student_trans_save: 
                student_credit=get_data.update(
                    studentTotalAmount=credit_amount
                    )
                if student_credit:
                    flash("{}, Successfully {} rupess Credited to your wallet".format(student_trans_save.studentName,creditAmount))
                    return redirect(url_for('studentAmountPage',refLink=refLink))
    return render_template('credit.html')

@app.route("/viewStudentsTransactionReports/<link>",methods=['POST','GET'])
def viewStudentsTransactionReportsPage(link):
    if request.method=="GET":
        get_transaction=AmountBank.objects.get(link=link)
        if get_transaction.link==link:
            get_students_trans = StudentTransaction.objects(link=link).all()
            # print(get_students_trans)
            trans_list=[]
            trans_dict={}
            count=0
            for st in get_students_trans:
                count=count + 1
                if st.amountDebitStatus == 2 or st.amountCreditStatus== 3:
                    trans_dict={
                        "sno":count,
                        "debitAmount":st.debitAmount,
                        "reasonTaking":st.reasonTaking,
                        "takenDebitDate":st.takenDebitDate,
                        "amountDebitStatus":st.amountDebitStatus,
                        "creditAmount":st.creditAmount,
                        "takenCreditDate":st.takenCreditDate,
                        "amountCreditStatus":st.amountCreditStatus

                    }
                    trans_list.append(trans_dict)

        return render_template('student_reports.html',trans_list=trans_list,link=link)

@app.route("/viewStudentsTransactionDate/<link>",methods=['POST','GET'])
def viewStudentsTransactionDateReportsPage(link):
    if request.method=="POST":
        student_dict={}
        student_list=[]
        fromDate = request.form.get('fromDate')
        toDate = request.form.get('toDate')
        if fromDate and toDate and request.method=='POST':
            
            get_transaction=AmountBank.objects.get(link=link)
            if get_transaction.link==link:
                get_students_trans_details = StudentTransaction.objects.filter(link=link,createdOn__in=[fromDate,toDate])
                if get_students_trans_details:
                    
                    count = 0
                    for st in get_students_trans_details:
                        count=count+1
                        if st.amountDebitStatus == 2 or st.amountCreditStatus== 3:
                            student_dict={
                            "sno":count,
                            "debitAmount":st.debitAmount,
                            "reasonTaking":st.reasonTaking,
                            "takenDebitDate":st.takenDebitDate,
                            "amountDebitStatus":st.amountDebitStatus,
                            "creditAmount":st.creditAmount,
                            "takenCreditDate":st.takenCreditDate,
                            "amountCreditStatus":st.amountCreditStatus
                            }
                        student_list.append(student_dict)
    return render_template('student_reports.html',student_list=student_list,link=link)

if __name__ == '__main__':
    # app.run(debug=True, port=4000)
    app.run(host='0.0.0.0',debug=True, port=4000)