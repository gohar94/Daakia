#!/usr/bin/python
"""
Author: Gohar Irfan Chaudhry
Website: http://goharirfan.me
Description: This script can be used to backup emails in a POP mail server inbox.
Date: 11th January 2016
"""
import thread
import poplib
import os
import sys
import math
import errno
import mimetypes
from email import parser
from argparse import ArgumentParser
from optparse import OptionParser

def fetch(server, email, password, directory, number):
	popConn = poplib.POP3_SSL(server)
	popConn.user(email)
	popConn.pass_(password)

	#Get messages from server:
	print "Number of mails in the inbox = " + str(len(popConn.list()[1]))
	
	if number == -1:
		number = len(popConn.list()[1])
	
	messages = []

	print "Fetching and saving mails..."
	for i in range(1, number+1):
		percentage = int((i*100/number))
		sys.stdout.write('\r')
		sys.stdout.write("[%-100s] %d%%" % ('='*percentage, percentage))
		sys.stdout.flush()
		message = popConn.retr(i)
		messages.append(message)
	
		# Concat message pieces:
		message = "\n".join(message[1])

		#Parse message into an email object:
		message = parser.Parser().parsestr(message)

		counter = 1
		for part in message.walk():
			# multipart/* are just containers
			if part.get_content_maintype() == 'multipart':
				continue
			
			foldername = message['date']
			"".join([c for c in foldername if c.isalpha() or c.isdigit() or c == ' ']).rstrip()

			createDir = directory+"/"+foldername
			try:
				os.mkdir(createDir)
			except OSError as e:
				if e.errno == errno.EEXIST:
					pass
				else:
					raise

			filename = part.get_filename()
			if not filename:
				if part.get_content_type() == 'text/plain':
					ext = '.txt'
				else:
					ext = mimetypes.guess_extension(part.get_content_type())
					if not ext:
						ext = '.bin'
				filename = 'part-%03d%s' % (counter, ext)

			fp = open(os.path.join(directory+"/"+foldername, filename), 'wb')
			
			if part.get_content_type() == 'text/plain':
				fp.write("From: " + message['from'] + "\n")
				fp.write("Subject: " + message['subject'] + "\n")
				fp.write("Contents: \n")
				fp.write(part.get_payload())
			else:
				counter += 1
				fp.write(part.get_payload(decode=True))
			fp.close()
	popConn.quit()

if __name__ == "__main__":
	optParser = ArgumentParser(description="""Open-source e-mail backup utility from POP Servers. Bare minimum features.""")
	optParser.add_argument('-d', '--directory', required=True, help="""Unpack the messages into the named directory, which will be created if it doesn't already exist.""")
	optParser.add_argument('-s', '--server', required=True, help="""Contact the given POP server to fetch the emails from.""")
	optParser.add_argument('-e', '--email', required=True, help="""Email address to download Inbox from.""")
	optParser.add_argument('-p', '--password', required=True, help="""Password of the email address to download Inbox from.""")
	optParser.add_argument('-n', '--number', required=False, help="""Number of mails to retrieve from the first mail.""", default=-1, type=int)
	args = optParser.parse_args()

	try:
		os.mkdir(args.directory)
		print("Directory created = " + os.getcwd() + "/" + args.directory)
	except OSError as e:
		if e.errno == errno.EEXIST:
			print("Directory not created, it already exists = " + os.getcwd() + "/" + args.directory)
		else:
			raise
    
	fetch(args.server, args.email, args.password, args.directory, args.number)
	print "All done."
