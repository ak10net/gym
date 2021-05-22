"""
Decorators add new functionality to a function or class at runtime.
This module shows how a simple "encryption" function for one string can
be decorated to work with a collection of string. 
"""

from functools import wraps

# Module-level constants
_MASKING = "*"

def run_with_stringy(fn):
	"""Run a string function with a string or a collection of strings

	We define a custom decorator that allows us to convert a function
	whose input is a single string into a function whose input can be
	a string or a collection of string

	A function decorator consists of the following:
	- An input function to run with
	- A wrapper function thtat uses the input function
	"""
	@wraps(fn)
	def wrapper(obj):
		"""Apply wraped funciton to a string or a collection"""
		if isinstance(obj,str):
			return fn(obj)
		elif isinstance(obj,dict):
			return {key: wrapper(value) for key, value in obj.items()}
		elif isinstance(obj, (list, set, tuple)):
			sequence_kls = type(obj)
			return sequence_kls(wrapper(value) for value in obj)
		raise ValueError(f"Found an invalid items: {obj}")

	return wrapper

@run_with_stringy
def hide_content(content):
	"""Hide half of the string content"""
	start_point = len(content) // 2
	num_of_asterisks = len(content) // 2 + len(content) % 2
	return content[:start_point] + _MASKING * num_of_asterisks


def _is_hidden(obj):
	"""Check whether string or collection is hidden"""
	if isinstance(obj, str):
		return _MASKING in obj
	elif isinstance(obj, dict):
		return all(_is_hidden(value) for value in obj.values())
	return all(_is_hidden(value) for value in obj)


def main():
	# There is so much plain data out in the open
	insecure_data = [
		{"username": "johndoe", "country": "USA"},
		["123-456-7890", "123-456-7891"],
		[("johndoe", "janedoe"), ("bobdoe", "marydoe")],
		"secretLaunchCode123"
	]

	secure_data = hide_content(insecure_data)

	for insecure_item, secure_item in zip(insecure_data, secure_data):
		assert insecure_item != secure_item
		assert not _is_hidden(insecure_item)
		assert _is_hidden(secure_item)


	# Throw an error on a collection with non-string objects
	input_failed = False
	try:
		hide_content([1])
	except ValueError:
		input_failed = True
	assert input_failed is True


if __name__ == "__main__":
	main()