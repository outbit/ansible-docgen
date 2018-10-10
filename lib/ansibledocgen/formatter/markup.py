""" Markup Formatter Module """
import re
import os
import codecs


class MarkupFormatter(object):
    """ Format Annotations as Markup Documentation """

    def __init__(self, parserdata, project, params):
        """ @parserdata is an array of dictionaries
            @project is the path to the project
        """
        self.parserdata = parserdata
        self.project = project
        self.params = params
        self.supported_attributes = ["author", "description", "task_info"]
        """ Example parserdata:
        [ { "author": "test",
        "description": "test2",
        "task_names": ["str1", "str2"],
        "rolename" : None,
        "relative_path" : "./myplaybook.yml"}, ] """
        self.role_outfiles = {}
        self.playbook_outfiles = {}

    def parse_data(self):
        """ Write Each Individual Markup File """
        for sourcefile in self.parserdata:
            self.write_doc(sourcefile)
            
    def __create_task_info_structure__(self, sourcefile):
        '''
        @author: Y_mil        
        @contact: lylinquiman@gmail.com
        @param sourcefile: sourcefile type
        @return: All task name and tags in order for create markup
        @rtype: list
        This Function go through all taks and create the list for create markup        
        '''
        list_data = []        
        for task_info in sourcefile['task_info']:
            print(task_info['task_name'])
            list_data.append(
                u"> **Task:** %s\n\n" % task_info['task_name'])
            if not task_info['task_tags'] == None and self.params['show_tags']:
                 list_data.append(u"> - **Tags:** %s\n\n" % \
                                  (", ".join(task_info['task_tags'])))
        return list_data
            
    def write_doc(self, sourcefile):
        """ @sourcefile is a dictionary, example:
              { "author": "", "description": "", "task_names": "", .....}
        """
        # Detect Attributes
        attributes = []
        for attribute in self.supported_attributes:
            if attribute in sourcefile:
                attributes.append(attributes)
        # Skip Playbooks With No Annotation or Tasks
        if len(attributes) <= 0:
            return

        # Parse a Role
        if sourcefile["rolename"] is not None:
            m = re.match("^(.*?)%s/tasks" %
                         sourcefile["rolename"], sourcefile["relative_path"])
            if m:
                roledir = m.group(1)
                if roledir not in self.role_outfiles:
                    self.role_outfiles[roledir] = []
                self.role_outfiles[roledir].append(
                    u"## Role: [%s](%s)\n" %
                    (sourcefile["rolename"], sourcefile["rolename"]))
                self.write_attribute(
                    sourcefile, roledir, "author", is_role=True)
                self.write_attribute(
                    sourcefile, roledir, "description", is_role=True)
                if "task_info" in sourcefile:
                    self.role_outfiles[roledir] += self.__create_task_info_structure__(sourcefile)
                        
            self.role_outfiles[roledir].append("\n")
        # Parse a Playbook
        else:
            playbookpath = self.project
            if playbookpath not in self.playbook_outfiles:
                self.playbook_outfiles[playbookpath] = []
            self.playbook_outfiles[playbookpath].append(
                u"## Playbook: [%s](%s)\n" %
                (sourcefile["relative_path"].replace(
                    playbookpath, ""), sourcefile["relative_path"].replace(
                    playbookpath, "")))
            self.write_attribute(sourcefile, playbookpath, "author")
            self.write_attribute(sourcefile, playbookpath, "description")
            if "task_info" in sourcefile:
                self.playbook_outfiles[playbookpath] += self.__create_task_info_structure__(sourcefile)                             
            self.playbook_outfiles[playbookpath].append("\n")

    def write_attribute(self, sourcefile, path, attribute, is_role=False):
        """ Write a comment attribute to sourcefile """
        if attribute in sourcefile:
            if sourcefile[attribute] is not None and sourcefile[
                    attribute] is not "":
                # Make First Letter Capital and end with an :
                pretty_attribute = attribute.capitalize()

                # Add to Output File
                if is_role:
                    self.role_outfiles[path].append(
                        u"> **%s:** %s\n\n" %
                        (pretty_attribute, sourcefile[attribute]))
                else:
                    self.playbook_outfiles[path].append(
                        u"> **%s:** %s\n\n" %
                        (pretty_attribute, sourcefile[attribute]))

    def write_files(self):
        """ Write Formatted Markup Files """
        # Write Role Markup Files
        for rolepath in self.role_outfiles:
            # Make sure there is a trailing /
            playbookpath = os.path.join(rolepath, "")
            # Open Output File
            filename = os.path.join(rolepath, "README.md")
            with codecs.open(filename, "w", encoding="utf-8") as p:
                for line in self.role_outfiles[rolepath]:
                    p.write(line)
                p.write("\n")
                p.write(
                    "Generated by [ansible-docgen](https://www.github.com/starboarder2001/ansible-docgen)")
                p.write("\n")
            print("Generated Markup File %s" % filename)

        # Write Playbook Markup Files
        for playbookpath in self.playbook_outfiles:
            # Make sure there is a trailing /
            playbookpath = os.path.join(playbookpath, "")
            # Open Output File
            filename = os.path.join(playbookpath, "README.md")
            with codecs.open(filename, "w", encoding="utf-8") as p:
                for line in self.playbook_outfiles[playbookpath]:
                    p.write(line)
                p.write("\n")
                p.write(
                    "Generated by [ansible-docgen](https://www.github.com/starboarder2001/ansible-docgen)")
                p.write("\n")
            print("Generated Markup File %s" % filename)
