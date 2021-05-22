"""
Exception classes are used to indicate that something has gone wrong with
the program at runtime. Functions use the `raise` keyword, if an error is
anticipated, and specify the exception class they intend to throw. This module
defines a handful of custom exception classes and
shows how they can be used in context of a function"""

class CustomError(Exception):
	"""Custom class of errors.

	This is a custom exception for any issues that arise in the module.
	One of the reasons why developers design a class like thisis for
	consumption by downstream services and command line tools.

	If we designed a standalone application with no downstream consumers, then
	it makes little sense to define a custom heirarchy of exceptions. In that case we should use the 
	existing heirarchy of exceptions.
	"""

class DivisionError(CustomError):
	"""
	Any division error that results from invalid input.
	-ZeroDivisionError
	-NegativeDivisionError
	"""

def divide_positive_numbers(dividend, divisor):
	if dividend <= 0:
		raise DivisionError(f"Non-positive dividend: {dividend}")
	elif divisor <= 0:
		raise DivisionError(f"Non-positive divisor: {divisor}")
	return dividend // divisor


def main():
	assert issubclass(DivisionError, CustomError)


	for dividend, divisor in [(0,1), (1,0), (-1,1), (1,-1)]:
		division_failed = False
		try:
			divide_positive_numbers(dividend, divisor)
		except DivisionError as e:
			division_failed = True
			assert str(e).startswith("Non-positive")
			print(e)
		assert division_failed is True

	result = divide_positive_numbers(1,1)
	assert result == 1


if __name__ == "__main__":
	main()