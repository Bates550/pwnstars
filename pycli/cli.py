#! python2
from __future__ import print_function
import sys
import cmd
import subprocess

import mysql.connector

class Client(cmd.Cmd):
	def __init__(self):
		cmd.Cmd.__init__(self)
		self.prompt = '> '

		# Probably should connect to the server here

	def do_INSERT(self, line):
		args = self.string_value_to_array(line)
		length = len(args)
		if (length == 1 and args[0] == ''):
			print('INSERT takes 3 arguments. You gave 0')
			return
		elif (length != 3):
			print('INSERT takes 3 arguments. You gave {}'.format(length))
			return
		else:
			(emp_id, emp_age, emp_salary) = args
			# Encrypt emp_salary
			print(encrypt(emp_salary))

	def do_SELECT(self, line):
		pass

	def do_exit(self, line):
		print('Exiting.')
		sys.exit()

	# This converts a single string of space separated values into an array
	# Ex: 'Boeing-747 Airbus-A300' -> ['Boeing-747', 'Airbus-A300']
	def string_value_to_array(self, string_value):
	  return string_value.split(' ')

	def encrypt(self, message):
		proc = subprocess.Popen(['./pailler', 'enc', str(message)], stdout=subprocess.PIPE)
		(stdout, stderr) = proc.communicate()
		return stdout

# Fill this in with your own configuration values
config = {
  'user': 'root',
  'password': '',
  'host': '127.0.0.1', # Localhost. If your MySQL Server is running on your own computer.
  'port': '3306', # Default port on Windows/Linux is 3306. On Mac it may be 3307.
  'database': 'airport',
}

#try:
#  cnx = mysql.connector.connect(**config)
#  cursor = cnx.cursor()
#except mysql.connector.Error as err:
#  print("Connection Error: {}".format(err))
#  sys.exit(1)

def execute(query, values):
  your_query = query % values
  print("Executing: {} ... ".format(query % values), end="")
  try:
    cursor.execute(query, values)
  except mysql.connector.Error as err:
    print("ERROR\nMySQL Error: {}\n".format(err))
    sys.exit(1)
  else:
    print("Success")

if __name__ == '__main__':
	Client().cmdloop()

# Commit data
#cnx.commit()
#cursor.close()
#cnx.close()