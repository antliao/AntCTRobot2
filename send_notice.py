import abc
import smtplib
from playsound import playsound
from email.message import EmailMessage

class Notice(metaclass=abc.ABCMeta):
	@abc.abstractmethod
	def send(self, subject, message):
		return NotImplemented

class Gmail_agent(Notice):
	def __init__(self, info):
		self.__info = info
		self.__sender_email = info['gmail_u']

	def __connect(self):
    	# Make sure to give app access in your Google account
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		self.server = server
		server.login(self.__info['gmail_u'], self.__info['gmail_p'])

	def send(self, subject, message):
		self.__connect()

		for r in self.__info['receivers']:
			email = EmailMessage()
			email['From'] = self.__sender_email
			email['Subject'] = subject
			email['To'] = r
			email.set_content(message)
			self.server.send_message(email)

class alarm_sound(Notice):
	def send(self, subject, message):
		if(subject == "Down"):
			playsound("wood_fish.mp3")
		elif(subject == "Up"):
			playsound("bell.mp3")
