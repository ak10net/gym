"""
Iterator classes implement the `__iter__` and `__next__` magic methods.
This module defines an employee iterator class that iterates through 
each employee in a hierarchy one-by-one. This module also shows how a 
similar approach can be achieved with a generator function
"""

# Module-level constants
_ITERATION_MESSAGE = "Cyclic loop detected"

class Employee:
	"""
	Generic employee class
	"""
	def __init__(self, name, title, direct_reports):
		self.name = name
		self.title = title
		self.direct_reports = direct_reports


class IterationError(RuntimeError):
	pass

class EmployeeIterator:
	def __init__(self, employee):
		"""Constructor logic"""
		self.employees_to_visit = [employee]
		self.employees_visited = set()

	def __iter__(self):
		"""Iterator is self by conventions"""
		return self

	def __next__(self):
		"""Return the next employee available"""
		if not self.employees_to_visit:
			raise StopIteration
		employee = self.employees_to_visit.pop()
		if employee.name in self.employees_visited:
			raise IterationError(_ITERATION_MESSAGE)
		self.employees_visited.add(employee.name)
		for report in employee.direct_reports:
			self.employees_to_visit.append(report)
		return employee


def employee_generator(top_employee):
	"""Employee generator"""
	to_visit = [top_employee]
	visited = set()

	while len(to_visit) > 0:
		employee = to_visit.pop()
		if employee.name in visited:
			raise IterationError(_ITERATION_MESSAGE)
		visited.add(employee.name)
		for report in employee.direct_reports:
			to_visit.append(report)
		yield employee


def main():
	# Manager with two direct reports
	manager = Employee("Max Doe", "Engineering Manager", [
			Employee("John Doe", "Software Engineer", []),
			Employee("Jane Doe", "Software Engineer", [])
		])

	employees = [emp for emp in EmployeeIterator(manager)]
	assert employees == [emp for emp in employee_generator(manager)]
	assert len(employees) == 3

	# Make sure that the employees are who we expect them to be
	assert all(isinstance(emp, Employee) for emp in employees)

    # This is not a good day for this company
	hacker = Employee("Unknown", "Hacker", [])
	hacker.direct_reports.append(hacker)

	for iter_obj in (EmployeeIterator, employee_generator):
		call_failed = False
		try:
			list(iter_obj(hacker))
		except IterationError as e:
			call_failed = True
			assert str(e) == _ITERATION_MESSAGE
		assert call_failed is True

if __name__ == "__main__":
	main()