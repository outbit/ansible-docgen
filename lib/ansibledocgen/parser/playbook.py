import yaml

class PlaybookParser(object):
	def __init__(self, filename):
		self.filename = filename
		self.comments = {}
		self.tasks = []

	def parse_playbooks(self):
		# TESTING FOR NOW JUST USE FIRST ELEMENT
		with open(self.filename[0]) as f:
			data = f.read()
			for task in yaml.load(data):
				for key in task:
					if key == "name":
						self.tasks.append(task[key])

	def debug(self):
		print(self.comments)
		print(self.tasks)