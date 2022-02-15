from django.db import models



class OtpModel(models.Model):
	otp 			= models.IntegerField()
	email 			= models.EmailField(blank=False, unique=True)
	time 			= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		name = str(self.otp) + ' of ' + str(self.email)
		return name

