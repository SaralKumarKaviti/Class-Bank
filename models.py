from mongoengine import *

class HouseMaster(Document):
	houseMasterFirstName = StringField(max_length=100)
	houseMasterLastName = StringField(max_length=100)
	houseClass = StringField(max_length=20)
	emailId = StringField(max_length=100)
	phoneNumber = StringField(max_length=50)
	refLink = StringField()
	houseMasterId = StringField()
	password = StringField()
	compOfLeaves = IntField()
	paidLeaves = IntField()
	casualLeaves = IntField()
	status = IntField()
	createdOn = DateTimeField()


class AmountBank(Document):
	studentName = StringField(max_length=100)
	className = StringField(max_length=100)
	houseMasterName = ReferenceField('HouseMaster')
	studentTotalAmount = IntField()
	link = StringField()
	refLink = StringField()
	status = IntField(default=1)
	createdOn = DateTimeField()
	

class StudentTransaction(Document):
	studentId = ReferenceField('AmountBank')
	studentName= StringField()
	creditAmount = IntField()
	debitAmount = IntField()
	reasonTaking = StringField(max_length=100)
	takenCreditDate = DateTimeField()
	takenDebitDate = DateTimeField()
	amountDebitStatus = IntField()
	amountCreditStatus = IntField()
	link=StringField()
	createdOn = DateTimeField()












	



