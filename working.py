import oom_markdown
import os
import argparse
import robo

#process
#  locations set in working_parts.ods 
#  export to working_parts.csv
#  put components on the right side of the board
#  run this script

def main(**kwargs):
    pass
    #make_readme(**kwargs)
    #run_utility(**kwargs)
    
def run_utility(**kwargs):
    jobs = []

    job = {}
    job["file_output"] = 'working_oomlout_organizing_paper_divider_binder.svg'
    job['utility'] = 'oomlout_utility_text_search_and_replace_jinja'
    job["command_line_args"] = {}
    job["command_line_args"]['directory_iterative'] = 'parts'
    job["command_line_args"]['file_output'] = job["file_output"]
    template = {}
    template['repo'] = 'oomlout_organizing_paper_divider_binder'
    template['path'] = 'template\\template_1'
    job["template"] = template
    jobs.append(job)

    for job in jobs:
        #clone to c:\gh if folder doesnt exist
        utility = job['utility']
        file_output = job.get('file_output', '')
        command_line_args = job.get('command_line_args', {})
        template = job.get('template', None)
        if template is not None:
            template_repo = template['repo']
            template_path = template['path']

        path_utility = f"c:\\gh\\{utility}\\working.py"
        if template is not None:
            path_template = f"c:\\gh\\{template_repo}\\{template_path}"
            extension = os.path.splitext(file_output)[1]
            file_template = f"{path_template}\\working.{extension.lstrip('.')}"
            command_line_args['file_template'] = file_template
        #get repos in
        if True:
            robo.robo_git_clone_repo(repo=utility)
            robo.robo_git_clone_repo(repo=template_repo)
        
        #build the call
        if True:
            #mode = "command_line"
            mode = "python"
            if mode == "command_line":
                command_line = f'python "{path_utility}"'
                for key, value in command_line_args.items():
                    command_line += f' --{key} "{value}"'
                print(command_line)
                os.system(command_line)
            elif mode == "python":
                pass


        #get tempalte repo in
        
        

def make_readme(**kwargs):
    os.system("generate_resolution.bat")
    oom_markdown.generate_readme_project(**kwargs)
    #oom_markdown.generate_readme_teardown(**kwargs)


if __name__ == '__main__':
    # parse arguments
    argparser = argparse.ArgumentParser(description='project description')
    #--file_input -fi
    argparser.add_argument('--file_input', '-fi', type=str, default='', help='file_input')    
    args = argparser.parse_args()
    kwargs = {}
    # update kwargs with args
    kwargs.update(vars(args))

    
    
    
    
    main(**kwargs)