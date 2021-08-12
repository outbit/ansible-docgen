""" Playbook Module """
from ansibledocgen.core.docgenyaml import DocGenYaml
import re
import os
import codecs


class HostVarsParser(object):
    def __init__(self, paths):
        """
        @param paths: list of paths with hosts
        """
        self.paths = paths
        self.parserdata = {}
    
    def parse_hosts_vars(self):
        """
        @return: dict with all host
                { 
                    host_name1: dic_parse_host_vars,
                    host_name2: dic_parse_host_vars,
                    ...
                }
        @rtype: dict
        """
        for path in self.paths:
            if os.path.isdir(path):
                for folder in os.listdir(path):
                    path_full_folder = os.path.join(path, folder)
                    host_vars = self.parse_host_vars(path_full_folder)
                    if host_vars:
                        self.parserdata[folder] = host_vars
    
    def parse_host_vars(self, path):
        """
        @return: dict with all file the one host with structure 
            { 
                file_host_var1: dict
                {'author': string, 
                'description': string, 
                'relative_path': string, 
                'variables': dic {
                    'var1': xxx,
                    'var2': xxx,
                    ...
                    }
                },                
                file_host_var2: ...
            }
        @rtype: dict
        """
        structure = {}
        if os.path.isdir(path):
            for file_host_var in os.listdir(path):
                if file_host_var[0] == "." or 'swp' in file_host_var:
                    continue                
                path_full = os.path.join(path, file_host_var)
                structure[file_host_var] = {}                
                structure[file_host_var]['relative_path'] = str(path_full)
                with codecs.open(path_full, "r", encoding="utf-8", errors='ignore') as f:
                    data = f.read()
                    for line in data.splitlines():
                        m = re.match(r"^[ ]*#[ ]*(.*?)[ ]*:[ ]*(.*?)$", line)
                        if m:
                            attribute = m.group(1)
                            value = m.group(2)
        
                            # Set An Attribute
                            if attribute.lower() == "author" or attribute.lower() == "description":
                                 structure[file_host_var][attribute.lower()] = value
                                 
                    yamldata = DocGenYaml.load(data)
                    
                    if yamldata == None:
                        del structure[file_host_var]
                        continue
                    structure[file_host_var]['variables'] = {}
                    for var in yamldata:
                        structure[file_host_var]['variables'][var] = yamldata[var]
                    
            if len(structure) > 0:
                return structure
        return False
