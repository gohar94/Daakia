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

	print "Fetching mails..."
	for i in range(1, number+1):
		percentage = int((i*100/number))
		sys.stdout.write('\r')
		sys.stdout.write("[%-100s] %d%%" % ('='*percentage, percentage))
		sys.stdout.flush()
		messages.append(popConn.retr(i))
	
	print "\nMailed fetched. Saving.\n"
	# Concat message pieces:
	messages = ["\n".join(mssg[1]) for mssg in messages]

	#Parse message into an email object:
	messages = [parser.Parser().parsestr(mssg) for mssg in messages]

	for message in messages:
		counter = 1
		for part in message.walk():
			# multipart/* are just containers
			if part.get_content_maintype() == 'multipart':
				continue
			
			foldername = message['date']
			"".join([c for c in foldername if c.isalpha() or c.isdigit() or c == ' ']).rstrip()
			print foldername

			createDir = directory+"/"+foldername
			try:
				os.mkdir(createDir)
				print("Directory created = " + os.getcwd() + "/" + createDir)
			except OSError as e:
				if e.errno == errno.EEXIST:
					print("Directory not created, it already exists = " + os.getcwd() + "/" + createDir)
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
			print filename
			
			if part.get_content_type() == 'text/plain':
				fp.write("From: " + message['from'] + "\n")
				fp.write("Subject: " + message['subject'] + "\n")
				fp.write("Contents: \n")
				fp.write(part.get_payload())
			else:
				counter += 1
				fp.write(part.get_payload(decode=True))

			print "\n"
			fp.close()
	popConn.quit()

def write_to_file(message):
	directory = message['date']
	if not os.path.exists(directory):
		os.makedirs(directory)
	filename = message['from']
	"".join([c for c in filename if c.isalpha() or c.isdigit() or c==' ']).rstrip()
	filename = directory + "/" + filename + ".txt"
	file = open(filename, "w")
	file.write(message['_payload'])
	file.close()

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