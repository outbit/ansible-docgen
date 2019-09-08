""" Playbook Module """
import yaml
import re
import os
import codecs


class PlaybookParser(object):
    """ Parse An Individual Playbook """

    def __init__(self, playbooks, is_role=False):
        """ 
        @param playbooks: is a list of paths to playbooks
        @param is_role: is used to determine if the playbook is part of a role
        """
        self.playbooks = playbooks
        self.parserdata = []
        self.is_role = is_role
        # basename of playbooks already parsed, to prevent infinate recrusion
        self.already_parsed_playbooks = []

    def parse_playbooks(self):
        """ Parse Each Playbook """
        for playbook in self.playbooks:
            self.parse_playbook(playbook)

    def __get_task_info__(self, task):
        '''
        @author: Y_mil        
        @contact: lylinquiman@gmail.com
        @param task: variable task type
        @return: {'task_name': 'xxx', 'task_tags': ['xxx' | None ]} 
            or false in case the no have the name task
        @rtype: dict or boolean
        This Function go through all task and create the dict with task name \ 
        and tags. In this function is possibly adding more variables.        
        '''
        if "name" in task:
            task_info = {'task_name': None, 'task_tags': None}
            task_name = task["name"]            
            task_info["task_name"] = task_name
            if "tags" in task:
                if not task["tags"] == None:
                    task_info["task_tags"] = task["tags"]
            return task_info
        return False
    
    def parse_playbook(self, playbook):
        """ Parse an Individual Playbook """
        with codecs.open(playbook, "r", encoding="utf-8") as f:
            # Get Rolename from filepath
            name = None
            if self.is_role:
                m = re.match(r".*/(.*?)/tasks/main.yml", playbook)
                if m:
                    name = m.group(1)
            else:
                m = re.match(r".*/(.*?).yml", playbook)
                if m:
                    name = m.group(1)
            # Do Not Parse If Its Already been Parsed
            playbook_base = os.path.basename(playbook)
            if self.is_role:
                # If Role, prepend rolename to make file unique to role
                playbook_base = "%s/%s" % (name, playbook_base)
            # Check if this file has alread been parsed
            if playbook_base in self.already_parsed_playbooks:
                return
            self.already_parsed_playbooks.append(playbook_base)

            # Setup Playbook Metadata
            playbookentry = {}
            playbookentry["relative_path"] = playbook
            playbookentry["name"] = name
            playbookentry["task_info"] = []
            playbookentry["is_role"] = self.is_role

            # Read file content into data
            data = f.read()

            # Parse Comment Data
            for line in data.splitlines():
                m = re.match(r"^[ ]*#[ ]*(.*?)[ ]*:[ ]*(.*?)$", line)
                if m:
                    attribute = m.group(1)
                    value = m.group(2)

                    # Set An Attribute
                    if attribute.lower() == "author" or attribute.lower() == "description":
                        playbookentry[attribute.lower()] = value

            # Parse Task Names from playbook
            yamldata = yaml.load(data, Loader=yaml.SafeLoader)
            # Skip Empty YAML Files
            if yamldata is None:
                return

            # Parase the Yaml
            for task in yamldata:
                # Playbooks have a tasks dict key
                if "tasks" in task:
                    task = task["tasks"]
                # Loop through Role tasks
                if isinstance(task, dict) and self.is_role:
                    task_info = self.__get_task_info__(task)
                    if not task_info == False:
                        playbookentry["task_info"].append(task_info)
                # Loop through Playbook tasks
                elif isinstance(task, list) and not self.is_role:
                    tasks = task
                    for task in tasks:
                        task_info = self.__get_task_info__(task)
                        if not task_info == False:
                            playbookentry["task_info"].append(task_info)
                # Loop through Playbook tasks
            self.parserdata.append(playbookentry)
