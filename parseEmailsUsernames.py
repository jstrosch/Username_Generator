import re

from burp import IBurpExtender, IContextMenuFactory

from javax.swing import JMenuItem
from java.util import List, ArrayList
from java.net import URL
from datetime import datetime
from HTMLParser import HTMLParser

#based off of https://docs.python.org/2/library/htmlparser.html
class MyHTMLParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.content = []

	def handle_data(self,data):
		self.content.append(data)

	def handle_comment(self,data):
		self.handle_data(data)

	def get_content(self, html):
		self.feed(html)
		return " ".join(self.content)

class BurpExtender(IBurpExtender, IContextMenuFactory):
	def registerExtenderCallbacks(self, callbacks):
		self._callbacks = callbacks
		self._helpers = callbacks.getHelpers()
		self.contexgt = None

		self.hosts = set()
		self.emails = set()
		self.user_names = set()

		callbacks.setExtensionName("0xEvilCode EMail Parse & Username Generator")
		callbacks.registerContextMenuFactory(self)

		return

	def createMenuItems(self, context_menu):
		self.context = context_menu
		menu_list = ArrayList()
		menu_list.add(JMenuItem("Get Emails",actionPerformed=self.email_menu))
		menu_list.add(JMenuItem("Generate Usernames",actionPerformed=self.users_menu))

		return menu_list

	def users_menu(self, event):

		# Gets the requests the user selected
		http_requests = self.context.getSelectedMessages()

		for request in http_requests:
			http_service = request.getHttpService()
			host = http_service.getHost()

			self.hosts.add(host)

			http_response = request.getResponse()

			if http_response:
				self.generate_usernames(http_response)

		self.display_user_names()
		return

	def generate_usernames(self, http_response):

		self.user_names = set()

		if not self.emails:
			self.get_emails(http_response)

		for email in sorted(self.emails):
			email_parts = email.split('@')

			# Add the email address
			self.user_names.add(email_parts[0].lower())

			# Look for first.last style email address
			if "." in email_parts[0]:
				first,last = email_parts[0].lower().split('.')

				self.user_names.add(first)
				self.user_names.add(last)
				self.user_names.add(last + "."+ first)

				self.user_names.add(first[:1] + last)
				self.user_names.add(last + first[:1])

		return

	def display_user_names(self):

		print "[!] Usernames for site(s) %s" % ", ".join(self.hosts)

		for user_name in sorted(self.user_names):
			print user_name

		return

	def email_menu(self,event):

		# Clear Emails
		self.emails = set()
		self.hosts = set()

		# Gets the requests the user selected
		http_requests = self.context.getSelectedMessages()

		for request in http_requests:
			http_service = request.getHttpService()
			host = http_service.getHost()

			self.hosts.add(host)

			http_response = request.getResponse()

			if http_response:
				self.get_emails(http_response)

	    #Displays results in Extender tab -> Output Window
		self.display_emails()
		return

	def get_emails(self, http_response):

		headers,body = http_response.tostring().split('\r\n\r\n',1)

		if headers.lower().find("content-type: text") == -1:
			return

		parser = MyHTMLParser()
		content = parser.get_content(body)

		# REGEX for emails, generous matching
		emails = re.findall("[\w\.-]+@[\w\.-]+", content)

		for email in emails:
			if len(email) > 7:
				self.emails.add(email.lower())

	def display_emails(self):

		print "[!] Emails for site %s" % ", ".join(self.hosts)

		for email in sorted(self.emails):
			print email

		return