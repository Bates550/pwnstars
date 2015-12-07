#! python2
from __future__ import print_function
import sys
import cmd
import subprocess

import mysql.connector

# Fill this in with your own configuration values
config = {
  'user': 'PwnStar',
  'password': 'gettinganA',
  'host': '54.153.92.135', # Localhost. If your MySQL Server is running on your own computer.
  'port': '3306', # Default port on Windows/Linux is 3306. On Mac it may be 3307.
  'database': 'project',
}

try:
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
except mysql.connector.Error as err:
	print("Connection Error: {}".format(err))
	sys.exit(1)

def execute(query, values):
	your_query = query % values
	#print("Executing: {} ... ".format(query % values), end="")
	try:
		cursor.execute(query, values)
	except mysql.connector.Error as err:
		print("MySQL Error: {}\n".format(err))
	else:
		#print("Success")
		pass

class Client(cmd.Cmd):
	def __init__(self):
		cmd.Cmd.__init__(self)
		self.prompt = '> '

		# Probably should connect to the server here

	def precmd(self, line):
		# Convert first token to upper so that entered commands are case insensitive
		args = string_value_to_array(line)
		args[0] = args[0].upper()
		return " ".join(args)

	def do_INSERT(self, line):
		args = string_value_to_array(line)
		length = len(args)
		if (length == 1 and args[0] == ''):
			print('INSERT takes 3 arguments. You gave 0')
			return
		elif (length != 3):
			print('INSERT takes 3 arguments. You gave {}'.format(length))
			return
		# User entered: INSERT emp_id emp_age emp_salary
		else:
			if (args[2] == '0'):
				print('Employee salary must be nonzero... you cheap bastard')
				return
			# Prepare values
			values = {
				'emp_id': args[0],
				'emp_age': args[1],
				'emp_salary': encrypt(args[2]) # Encrypt salary
			}
			# Construct query
			insert_employee = (
				"INSERT INTO Employees(id, age, salary) "
				"VALUES (%(emp_id)s, %(emp_age)s, %(emp_salary)s)"
			)
			execute(insert_employee, values)
			cnx.commit()

	def do_SELECT(self, line):
		args = string_value_to_array(line)
		uargs = string_value_to_array(line.upper())
		length = len(args)
		# User entered: SELECT. Invalid command
		if (length == 1 and args[0] == ''):
			# TODO: make this message more informative
			print('Invalid command: SELECT takes more than 0 arguments.')
			return
		# User entered 'SELECT *'
		elif (length == 1 and args[0] == '*'):
			select_employee = (
				"SELECT id, age, salary "
				"FROM Employees"
			)
			execute(select_employee, {})
			for (id, age, salary) in cursor:
				print('{}, {}, {}'.format(id, age, decrypt(salary)[:-1]))

			# If no employees exist
			if (cursor.rowcount == -1):
				print('Employees table is empty')
		# User entered 'SELECT SUM' and maybe more
		elif (length >= 1 and uargs[0] == 'SUM'):
			if (length > 1):
				# User entered 'SELECT SUM WHERE' and maybe more
				if (uargs[1] == 'WHERE'):
					# User entered 'SELECT SUM WHERE <condition> GROUP BY age' and maybe more
					if ('GROUP' in uargs and 'BY' in uargs and
							uargs.index('GROUP')+1 == uargs.index('BY') and
							length >= uargs.index('BY')+2 and
							args[uargs.index('BY')+1] == 'age'
						):
						# User entered 'SELECT SUM WHERE <condition> GROUP BY age HAVING <condition>'
						if ('HAVING' in uargs and
								uargs.index('BY')+2 == uargs.index('HAVING') and
								length >= uargs.index('HAVING')+2
							):
							where_condition = " ".join(args[2:uargs.index('GROUP')])
							having_condition = " ".join(args[uargs.index('HAVING')+1:])
							select_employee = (
								"SELECT age, SUM_HE(salary) "
								"FROM Employees "
								"WHERE {} "
								"GROUP BY age "
								"HAVING {}".format(where_condition, having_condition)
							)
							execute(select_employee, {})
							for (age, sum) in cursor:
								print('{}, {}'.format(age, decrypt(sum)[:-1]))
							if (cursor.rowcount == -1):
								print('No employees met condition')
						# User entered 'SELECT SUM WHERE <condition> GROUP BY age'
						elif ('HAVING' not in uargs):
							condition = " ".join(args[2:uargs.index('GROUP')])
							select_employee = (
								"SELECT age, SUM_HE(salary) "
								"FROM Employees "
								"WHERE {} "
								"GROUP BY age".format(condition)
							)
							execute(select_employee, {})
							for (age, sum) in cursor:
								print('{}, {}'.format(age, decrypt(sum)[:-1]))
							if (cursor.rowcount == -1):
								print('No employees met condition')
						else:
							print('Invalid command: SELECT {}'.format(" ".join(args)))
					# User entered 'SELECT SUM WHERE <condition>'
					elif ('GROUP' not in uargs and
							length > 2
						):
						condition = " ".join(args[2:])
						select_employee = (
							"SELECT SUM_HE(salary) "
							"FROM Employees "
							"WHERE {}".format(condition)
						)
						execute(select_employee, {})
						for (sum) in cursor:
							sum = sum[0].decode('utf-8')
							print(decrypt(sum)[:-1])
					else:
						print('Invalid command: SELECT {}'.format(" ".join(args)))
				# User entered 'SELECT SUM GROUP BY age' and maybe more
				elif (length > 3 and uargs[1] == 'GROUP' and uargs[2] == 'BY' and args[3] == 'age'):
					# User entered 'SELECT SUM GROUP BY age'
					if (length == 4):
						select_employee = (
							"SELECT age, SUM_HE(salary) "
							"FROM Employees "
							"GROUP BY age"
						)
						execute(select_employee, {})
						for (age, sum) in cursor:
							print('{}, {}'.format(age, decrypt(sum)[:-1]))
					# User entered 'SELECT SUM GROUP BY age HAVING <condition>'
					elif (length > 5 and uargs[4] == 'HAVING'):
						condition = " ".join(args[5:])
						select_employee = (
							"SELECT age, SUM_HE(salary) "
							"FROM Employees "
							"GROUP BY age "
							"HAVING {}".format(condition)
						)
						execute(select_employee, {})
						for (age, sum) in cursor:
							print('{}, {}'.format(age, decrypt(sum)[:-1]))
				else:
					print('Invalid command: SELECT {}'.format(" ".join(args)))
			# User entered 'SELECT SUM'
			else:
				select_employee = (
					"SELECT SUM_HE(salary) "
					"FROM Employees"
				)
				execute(select_employee, {})
				for (sum) in cursor:
					sum = sum[0].decode('utf-8')
					if (sum == '1'): # '1' is '0' encrypted apparently
						print('NULL')
					else:
						print(decrypt(sum)[:-1])
		# User entered 'SELECT AVG' and maybe more
		elif (length >= 1 and uargs[0] == 'AVG'):
			sums = {}
			counts = {}
			if (length > 1):
				# User entered 'SELECT AVG WHERE' and maybe more
				if (uargs[1] == 'WHERE'):
					# User entered 'SELECT AVG WHERE <condition> GROUP BY age' and maybe more
					if ('GROUP' in uargs and 'BY' in uargs and
							uargs.index('GROUP')+1 == uargs.index('BY') and
							length >= uargs.index('BY')+2 and
							args[uargs.index('BY')+1] == 'age'
						):
						# User entered 'SELECT AVG WHERE <condition> GROUP BY age HAVING <condition>'
						if ('HAVING' in uargs and
								uargs.index('BY')+2 == uargs.index('HAVING') and
								length >= uargs.index('HAVING')+2
							):
							where_condition = " ".join(args[2:uargs.index('GROUP')])
							having_condition = " ".join(args[uargs.index('HAVING')+1:])
							select_employee_sum = (
								"SELECT age, SUM_HE(salary) "
								"FROM Employees "
								"WHERE {} "
								"GROUP BY age "
								"HAVING {}".format(where_condition, having_condition)
							)
							execute(select_employee_sum, {})
							for (age, sum) in cursor:
								sums[age] = decrypt(sum)[:-1]

							if (cursor.rowcount == -1):
								print('No employees met condition')
								return

							select_employee_count = (
								"SELECT age, COUNT(salary) "
								"FROM Employees "
								"WHERE {} "
								"GROUP BY age "
								"HAVING {}".format(where_condition, having_condition)
							)
							execute(select_employee_count, {})
							for (age, count) in cursor:
								counts[age] = count

							for age, sum in sums.items():
								print('{}, {}'.format(age, float(sum)/float(counts[age])))
						# User entered 'SELECT AVG WHERE <condition> GROUP BY age'
						elif ('HAVING' not in uargs):
							condition = " ".join(args[2:uargs.index('GROUP')])
							sums = {}
							counts = {}
							select_employee_sum = (
								"SELECT age, SUM_HE(salary) "
								"FROM Employees "
								"WHERE {} "
								"GROUP BY age".format(condition)
							)
							execute(select_employee_sum, {})
							for (age, sum) in cursor:
								sums[age] = decrypt(sum)[:-1]

							if (cursor.rowcount == -1):
								print('No employees met condition')
								return

							select_employee_count = (
								"SELECT age, COUNT(salary) "
								"FROM Employees "
								"WHERE {} "
								"GROUP BY age".format(condition)
							)
							execute(select_employee_count, {})
							for (age, count) in cursor:
								counts[age] = count

							for age, sum in sums.items():
								print('{}, {}'.format(age, float(sum)/float(counts[age])))

						else:
							print('Invalid command: SELECT {}'.format(" ".join(args)))
					# User entered 'SELECT AVG WHERE <condition>'
					elif ('GROUP' not in uargs and
							length > 2
						):
						condition = " ".join(args[2:])
						select_employee_sum = (
							"SELECT SUM_HE(salary) "
							"FROM Employees "
							"WHERE {}".format(condition)
						)
						execute(select_employee_sum, {})
						for (sum) in cursor:
							sum_result = decrypt(sum[0].decode('utf-8'))[:-1]

						if (cursor.rowcount == -1):
							print('No employees met condition')
							return

						select_employee_count = (
							"SELECT COUNT(salary) "
							"FROM Employees "
							"WHERE {}".format(condition)
						)
						execute(select_employee_count, {})
						for (count) in cursor:
							count_result = count[0]
						print('{}'.format(float(sum_result)/float(count_result)))
					else:
						print('Invalid command: SELECT {}'.format(" ".join(args)))
				# User entered 'SELECT AVG GROUP BY age' and maybe more
				elif (length > 3 and uargs[1] == 'GROUP' and uargs[2] == 'BY' and args[3] == 'age'):
					# User entered 'SELECT AVG GROUP BY age'
					if (length == 4):
						select_employee_sum = (
							"SELECT age, SUM_HE(salary) "
							"FROM Employees "
							"GROUP BY age"
						)
						execute(select_employee_sum, {})
						for (age, sum) in cursor:
							sums[age] = decrypt(sum)[:-1]

						if (cursor.rowcount == -1):
							print('No employees met condition')
							return

						select_employee_count = (
							"SELECT age, COUNT(salary) "
							"FROM Employees "
							"GROUP BY age"
						)
						execute(select_employee_count, {})
						for (age, count) in cursor:
							counts[age] = count

						for age, sum in sums.items():
							print('{}, {}'.format(age, float(sum)/float(counts[age])))
					# User entered 'SELECT AVG GROUP BY age HAVING <condition>'
					elif (length > 5 and uargs[4] == 'HAVING'):
						condition = " ".join(args[5:])
						select_employee_sum = (
							"SELECT age, SUM_HE(salary) "
							"FROM Employees "
							"GROUP BY age "
							"HAVING {}".format(condition)
						)
						execute(select_employee_sum, {})
						for (age, sum) in cursor:
							sums[age] = decrypt(sum)[:-1]

						if (cursor.rowcount == -1):
							print('No employees met condition')
							return

						select_employee_count = (
							"SELECT age, COUNT(salary) "
							"FROM Employees "
							"GROUP BY age "
							"HAVING {}".format(condition)
						)
						execute(select_employee_count, {})
						for (age, count) in cursor:
							counts[age] = count

						for age, sum in sums.items():
							print('{}, {}'.format(age, float(sum)/float(counts[age])))
				else:
					print('Invalid command: SELECT {}'.format(" ".join(args)))
			# User entered 'SELECT AVG'
			else:
				select_employee_sum = (
					"SELECT SUM_HE(salary) "
					"FROM Employees"
				)
				execute(select_employee_sum, {})
				for (sum) in cursor:
					sum = sum[0].decode('utf-8')
					if (sum == '1'): # '1' is '0' encrypted apparently
						print('NULL')
					else:
						sum_result = decrypt(sum)[:-1]

				select_employee_count = (
					"SELECT COUNT(salary) "
					"FROM Employees"
				)
				execute(select_employee_count, {})
				for (count) in cursor:
					count_result = count[0]

				print('{}'.format(float(sum_result)/float(count_result)))
		# User entered 'SELECT emp_id'
		elif (length == 1):
			# Prepare values
			values = {
				'emp_id': args[0]
			}
			select_employee = (
				"SELECT id, age, salary "
				"FROM Employees "
				"WHERE id = %(emp_id)s"
			)
			execute(select_employee, values)
			for (id, age, salary) in cursor:
				print('{}, {}, {}'.format(id, age, decrypt(salary)[:-1]))

			# If no employee with emp_id exists
			if (cursor.rowcount == -1):
				print('Employee with emp_id: {} does not exist'.format(args[0]))
		elif (length != 3):
			print("Yeah... that ain't gonna work")
			return
		else:
			print('?')

	def do_ENC(self, line):
		print(encrypt(line))

	def do_DEC(self, line):
		print(decrypt(line))

	def do_EXIT(self, line):
		print('Exiting.')
		sys.exit()

	def do_QUIT(self, line):
		self.do_EXIT(line)

# This converts a single string of space separated values into an array
# Ex: 'Boeing-747 Airbus-A300' -> ['Boeing-747', 'Airbus-A300']
def string_value_to_array(string_value):
  return string_value.split(' ')

# Calls 'paillier <mode> <message>'. paillier binary must be in same directory as this script.
def encdec(mode, message):
	proc = subprocess.Popen(['./paillier', mode, str(message)], stdout=subprocess.PIPE)
	(stdout, stderr) = proc.communicate()
	return stdout

def encrypt(plaintext):
	return encdec('enc', plaintext)

def decrypt(ciphertext):
	return encdec('dec', ciphertext)

if __name__ == '__main__':
	Client().cmdloop()

	cursor.close()
	cnx.close()