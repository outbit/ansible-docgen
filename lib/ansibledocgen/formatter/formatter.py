from jinja2 import Template
import os
import codecs
class Formatter(object):
    def __init__(self, style, parserdata, paths, project, params):
        
        self.parserdata = parserdata
        self.paths = paths
        self.project = project
        self.params = params
        self.render_files = dict(
            playbook=dict(),
            roles=dict(),
            host=dict()
           ) 
        self.templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
        self.templates_files = {
                "playbook": "{}_playbook.j2".format(style),
                "role": "{}_role.j2".format(style),
                "host": "{}_host.j2".format(style)
            }
        
    def parse_data(self):
        self.__make_playbook_template__()
        self.__make_role_template__()
        self.__make_host_vars__()
    
    def write_files(self, filename="README"):
        for type_, content in self.render_files.items():            
            for path_content, render_file in content.items():
                readme_top = os.path.join(path_content, "README-TOP.md")
                readme_bottom = os.path.join(path_content, "README-BOTTOM.md")
                readme_top_content = ""
                readme_bottom_content = ""
                ''' README-TOP: if this file exists it's concatenated at the top of 
                    README.md created by ansibledocgen'''
                if os.path.exists(readme_top):
                    with codecs.open(readme_top, "r", encoding="UTF-8") as f:
                        readme_top_content = f.read()
                if os.path.exists(readme_bottom):
                    with codecs.open(readme_bottom, "r", encoding="UTF-8") as f:
                        readme_bottom_content = f.read()
                file_dest = os.path.join(path_content, f"{filename}.md")
                if os.path.isdir(path_content):
                    with codecs.open(file_dest, "w", encoding="utf-8") as f:
                        f.write(readme_top_content)
                        f.write("\n")
                        f.write(render_file)
                        f.write("\n")
                        f.write(readme_bottom_content)
                
    def __make_playbook_template__(self):
        with open(os.path.join(self.templates_dir,self.templates_files['playbook'])) as file_:
            template = Template(file_.read())
        for content in self.parserdata['playbooks']:
            self.render_files['playbook'][content] = template.render(data=self.parserdata['playbooks'][content], params=self.params) 
    
    def __make_role_template__(self):
        with open(os.path.join(self.templates_dir,self.templates_files['role'])) as file_:
            template = Template(file_.read())
        for content in self.parserdata['roles']:
            self.render_files['roles'][content] = template.render(data=self.parserdata['roles'][content], params=self.params) 
    
    def __make_host_vars__(self):
        with open(os.path.join(self.templates_dir,self.templates_files['host'])) as file_:
            template = Template(file_.read())
        self.render_files['host'][self.paths['host'][0]] = template.render(data=self.parserdata['host_vars'], params=self.params) 
