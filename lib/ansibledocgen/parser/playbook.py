""" Playbook Module """
from ansibledocgen.core.docgenyaml import DocGenYaml
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
        self.parserdata = {}
        self.is_role = is_role
        # basename of playbooks already parsed, to prevent infinate recrusion
        self.already_parsed_playbooks = []

    def parse_playbooks(self):
        """ Parse Each Playbook """
        for playbook in self.playbooks:
            self.parse_playbook(playbook)

    def __get_task_info__(self, tasks):
        '''
        @param tasks: variable task type
        @return: {'task_name': 'xxx', 'task_tags': ['xxx' | None ]} 
            or false in case the no have the name tasks
        @rtype: list of dicts
        This Function go through all task and create the dict with task name \ 
        and tags. In this function is possibly adding more variables.        
        '''
        task_info_list = []
        if isinstance(tasks, list):
            for task in tasks:
                task_info_list += self.__get_task_info__(task)
        else:
            if "name" in tasks:
                task_info = {'task_name': None, 'task_tags': None}
                task_name = tasks["name"]
                task_info["task_name"] = task_name
                if "tags" in tasks:
                    if not tasks["tags"] == None:
                        task_info["task_tags"] = tasks["tags"]
                task_info_list.append(task_info)
            if "always" in tasks:
                task_info_list += self.__get_task_info__(tasks["always"])
            if "block" in tasks:
                task_info_list += self.__get_task_info__(tasks["block"])
            if "rescue" in tasks:
                task_info_list += self.__get_task_info__(tasks["rescue"])

        return task_info_list
    
    def parse_playbook(self, playbook):
        """ Parse an Individual Playbook """
        with codecs.open(playbook, "r", encoding="utf-8") as f:
            # Get Rolename from filepath
            name = None
            if self.is_role:
                name = os.path.basename(
                            os.path.normpath(
                                os.path.join(playbook, "../..")))
                folder_content = os.path.normpath(
                                    os.path.join(playbook, "../../.."))
            else:
                folder_content = os.path.normpath(
                                    os.path.join(playbook, ".."))
                m = re.match(r".*/(.*?).yml", playbook)
                if m:
                    name = m.group(1)
            # Do Not Parse If Its Already been Parsed
            playbook_base = playbook
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
            yamldata = DocGenYaml.load(data)
            # Skip Empty YAML Files
            if yamldata is None:
                return

            # Parase the Yaml
            for yaml_item in yamldata:
                tasks = yaml_item
                # Playbooks have a tasks dict key
                if "tasks" in yaml_item:
                    tasks = yaml_item["tasks"]
                # Loop through tasks
                task_info = self.__get_task_info__(tasks)
                if len(task_info) > 0:
                    playbookentry["task_info"] += task_info
                # Loop through Playbook tasks
            if folder_content not in self.parserdata:
                self.parserdata[folder_content] = []
            self.parserdata[folder_content].append(playbookentry)
