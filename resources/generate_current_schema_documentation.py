#!/usr/bin/python3
""" Dereferences $ref elements in RDE schema files, replacing the $ref with the contents
    of the referenced schema file.

    Assumptions:
    1. $ref elements point only to other RDE schema and vocabulary files.
    2. Every RDE schema and vocabulary file has a $schema element identifying the file as a JSON Schema.
    3. Every RDE schema and vocabulary file has an $id element that can serve as the target of any $ref.
"""
import os
import sys
import json
import yaml
import logging
import argparse
import subprocess
import datetime
import shutil

from glob import glob
from urllib.parse import urlparse, parse_qs

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
log = logging.getLogger()

def get_cli_arguments():
    """ Parse command line arguments and return an object whose members contain the argument values. """
    parser = argparse.ArgumentParser(description="Dereferences $ref elements in RDE schema files")
    parser.add_argument('--source-dir', dest='source_dir', type=str, help='Source directory', required=True)
    #parser.add_argument('--target-dir', dest='docs_dir', type=str, help='Target directory', required=True)
    parser.add_argument('--verbose', dest='verbose', help='Include verbose output', required=False, default=False, action="store_true")
    return parser.parse_args()

def load_cache(root_dir):
    """ Walks the file system from root_dir and loads any RDE schema files into a dict
        keyed by the $id of the schema.
    """
    cache = {} 
    schema_files = glob(os.path.join(root_dir, 'schema', '*.json'), recursive=True)
    yaml_files  = glob(os.path.join(root_dir, 'schema', 'yaml', '*.yaml'), recursive=True)

    for file_name in schema_files + yaml_files:
        try:
            with open(file_name, "r", encoding="utf-8") as f:
                if ".json" in file_name:
                    content = json.load(f)
                elif ".yaml" in file_name:
                    content = yaml.safe_load(f)
                    if content.get('usageNotes'):
                        content['usageNotes'] = content['usageNotes'].replace('\n', '  \n')
                    if content.get('curatorNotes'):
                        content['curatorNotes'] = content['curatorNotes'].replace('\n', '  \n')

            if '$schema' in content: # Use presence of $schema attribute to identify JSON Schema files
                log.debug(f"Loading {file_name} into schema cache")
                if (ident := content['$id']) not in cache:
                    cache[ident] = content
                else:
                    raise ValueError(f"Schema file {file_name} uses an $id value ({ident}) that is already in use by another schema")
        except KeyError as ex:
            raise KeyError(f"Schema file {file_name} does not contain an $id field") from ex
    return cache

def dereference_cache(cache): 
    """ Deferences $ref values in the cache. """
    for key, schema in cache.items():
        log.debug(f"Dereferencing $ref values in schema: {key}")
        cache[key] = resolve(schema, cache)
    return cache

def resolve(obj, cache):
    """ Recursively deferences $ref values in a schema. """
    if isinstance(obj, dict):
        new = {}
        for key, value in obj.items():
            if key == "$ref":
                try:
                    result = resolve(cache[value], cache)
                    new = {**new, **result} # Assumes that $ref always points to a dict
                except KeyError as ex:
                    raise KeyError(f"Cannot find {value} in the schema cache")
            else:
                new[key] = resolve(value, cache)
        return new
    elif isinstance(obj, list):
        return [resolve(item, cache) for item in obj]
    else:
        return obj

def persist_cache(cache, temp_dir):
    """ Persist cache to temp_dir """
    for key, schema in cache.items():
        if (title := schema.get('title')) is not None:
            # path_components = urlparse(key).path.split('/')
            # file_path = os.path.join(*path_components[1:]) # Remove first element, which is the base URI template
            file_name = os.path.join(temp_dir, 'icpsr_study_schema.json')
            os.makedirs(os.path.dirname(file_name), exist_ok=True)

            log.debug(f"Writing {title} schema to {file_name}")

            with open(file_name, 'w', encoding='utf-8') as fp:
                json.dump(schema, fp, indent=4)

        elif 'yaml' not in key:
            raise ValueError(f"Cannot persist schema because it does not contain a title element: {key}")

    return file_name

def main():
    """ Main entrypoint. """
    # source_dir == the main project directory. Must contain a 'schema' folder
    try:
        args = get_cli_arguments()
        if args.verbose:
            log.setLevel(logging.DEBUG)

        if not os.path.exists(args.source_dir):
            print(f"{args.source_dir} does not exist. Please verify path and try again")
            sys.exit(1)

        #set up variables
        site_dir = os.path.join(args.source_dir, 'site')
        schema_markdown_dir = os.path.join(args.source_dir, 'markdown', 'schema')
        resource_dir = os.path.join(args.source_dir, 'resources')
        temp_dir = os.path.join(args.source_dir, 'temp')
        mkdocs_yml = os.path.join(resource_dir, 'mkdocs.yml')
        rtd_css = os.path.join(resource_dir, 'readthedocs_theme.css')
        
        for folder in [temp_dir, site_dir, schema_markdown_dir]:
            if not os.path.exists(folder):
                os.makedirs(folder)
        
        #produce a dereferenced json file
        print("\tProducing cache...")
        cache = dereference_cache(load_cache(args.source_dir))
        print("\tSaving temp file...")
        dereferenced_file = persist_cache(cache, temp_dir)

        #remove extra $id and $schema values
        print("\tRemoving extra $id and $schema values...")
        with open(dereferenced_file, "r", encoding="utf-8") as f:
            content = json.load(f)

        #remove additional $id and $schema entries
        for k, v in content.items():
            for key, value in content['properties'].items():
                content['properties'][key].pop('$id', None)
                content['properties'][key].pop('$schema', None)
            
        #write back to dereferenced json
        with open(dereferenced_file, "w", encoding="utf-8") as f:
            json.dump(content, f, indent=4)
            
        #generate markdown using modified version of JSON Schema for Humans
        print("\tCreating markdown...")
        md_filename = os.path.basename(os.path.splitext(dereferenced_file)[0])
        md_file = os.path.join(schema_markdown_dir, f"{md_filename}.md")

        cmd = "generate-schema-doc --config custom_template_path={} --config show_toc=false --config show_breadcrumbs=false {} {}".format(os.path.join(resource_dir, 'template', 'base.md'), dereferenced_file, md_file)

        subprocess.run(cmd, shell=True, text=True)

        #now read in all our schema markdown to make final improvements 
        print("\tFixing labels...")
        with open(md_file, 'r', encoding='utf-8') as fi:
            content=fi.readlines()

        #update schema description to include date
        descr=[x for x in content if 'Metadata Schema for Curated ICPSR Studies\n' in x][0]
        descr_index=content.index(descr)
        current_date=datetime.datetime.now()
        content[descr_index]="{} as of {}.\n".format(descr.replace('\n', ''), current_date.strftime("%B %d, %Y"))

        #loop through content and fix various issues
        with open(md_file, 'w', encoding='utf-8') as fo:
            for line in content:
                #if '#' in line:
                if any(x in line for x in ['(O)', '(R)']):
                    table_text=line.split(']', 1)
                    table_text[0]=table_text[0].replace('_', ' ').title().replace("To", "to").replace("Of", "of").replace("Id", "ID").replace("Doi", "DOI").replace("IDentifier", "Identifier").replace("Sda ", "SDA ")
                    fo.write(']'.join(table_text))
                elif '</a>' in line and '#' in line:
                    pass
                    text=line.split('</a>')
                    text[1]=text[1].replace('_', ' ').title().replace("To", "to").replace("Of", "of").replace("Id", "ID").replace("Doi", "Digital Object Identifier (DOI)").replace("IDentifier", "Identifier").replace("Sda ", "SDA ")
                    fo.write('</a>'.join(text))
                elif '*Option*' in line and '*Description*' in line:
                    fo.write('\n')
                    fo.write(line)
                elif '**Additional properties**: [[Not allowed]](# "Additional Properties not allowed.")' in line:
                    fo.write('**Additional Properties**: Not Allowed\n')
                else:
                    fo.write(line)

        #generate html; run mkdocs
        cmd = 'mkdocs build -f {} --clean --verbose'.format(mkdocs_yml)
        subprocess.run(cmd, shell=True)

        #add improved CSS
        shutil.copy(rtd_css, os.path.join(site_dir, 'css', 'theme.css'))
            
        #remove temp folder
        print("\n\nRemoving temp folder...")
        shutil.rmtree(temp_dir, ignore_errors=True)
        print("\nAll done!")


    except Exception as ex: # pylint: disable=broad-except
        log.error(ex)
        sys.exit(1)

if __name__=='__main__':
    main()
