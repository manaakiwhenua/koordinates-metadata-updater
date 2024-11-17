#!/usr/bin/python3

################################################################################
#
# Copyright 2018 Crown copyright (c)
# Land Information New Zealand and the New Zealand Government.
# All rights reserved
#
# This program is released under the terms of the new BSD license. See the
# LICENSE file for more information.
#
################################################################################

import koordinates
import os
import sys
import fileinput
import yaml
import re
import requests
import logging
import shutil
import argparse
import _locale
import hashlib
from lxml import etree as ET
from xml.dom.minidom import parse, parseString

from .utils.xml_to_excel import parse_xml_file, write_to_excel, record_missing_metadata

_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])


# current solution for setup.py
try: 
    import log
except:
    from . import log
    
logger = logging.getLogger(__name__)
ERRORS = 0
NAMESPACES = {
    'gmd': 'http://www.isotc211.org/2005/gmd',
    'gco': 'http://www.isotc211.org/2005/gco',
    #'srv': 'http://www.isotc211.org/2005/srv',
    #'gml': 'http://www.opengis.net/gml',
    #'xlink': 'http://www.w3.org/1999/xlink'
}

for prefix, uri in NAMESPACES.items():
    ET.register_namespace(prefix, uri)

class ConfigReader():
    """
    Create a config object that can
    be passed to the scripts methods
    """

    def __init__(self, cwd = None):
        # READ CONFIG

        # get config path
        if not cwd:
            cwd = os.getcwd()
            regex = re.compile(r'(\\|\/)(metadata_updater)$')
            cwd = regex.sub('', cwd)
            cwd = os.path.join(os.sep, cwd, 'metadata_updater', 'config.yaml')

        #check config exists
        if not os.path.exists(cwd):
            raise FileNotFoundError('Can not find config file')

        with open(cwd, 'r') as f:
            config = yaml.safe_load(f)

        # CONNECTION
        if 'Connection' in config:
            if os.getenv('LDS_APIKEY', None):
                self.api_key = os.environ['LDS_APIKEY']
            else:
                self.api_key = config['Connection']['Api_key']
            if not self.api_key:
                raise SystemExit('No LDS API Key Provided')
            self.domain = config['Connection']['Domain']
        else:
            raise SystemExit('CONFIG ERROR: No "Connection" section')
        
        # FIND AND REPLACE TEXT
        if 'Text' in config:
            self.text_mapping = config['Text']['Mapping']
        else:
            raise SystemExit('CONFIG ERROR: No "Text" section')

        # OUTPUT DIR
        if 'Output' in config:
            self.destination_dir = config['Output']['Destination']
        else:
            self.destination_dir = os.getcwd()  + os.path.sep

        # DATA TO PROCESS
        if 'Datasets' in config:
            self.layers = config['Datasets']['Layers']
        else:
            raise SystemExit('CONFIG ERROR: No "Datasets" section')

        # TEST AND DEV CONFIG
        if 'Test' in config:
            self.test_dry_run = config['Test']['Dry_run']
            if self.test_dry_run not in (True, False):
                raise SystemExit('CONFIG ERROR: "Test Dry Run" must be ' \
                '"True" or "False". Got:"{}" instead'.format(self.test_dry_run))

            self.test_overwrite = config['Test']['Overwrite_files']
            if self.test_overwrite not in (True, False):
                raise SystemExit('CONFIG ERROR: "test_overwrite" must be ' \
                '"True" or "False". Got:"{}" instead'.format(self.test_overwrite))
        else:
            raise SystemExit('CONFIG ERROR: No "Test" section')
        
        # IF SUMMARISE
        if 'Summarise' in config:
            self.summarise = config['Summarise']['Summarise_metadata']
            

def post_metadata(draft, file):
    """
    Update the Data Service draft version for the 
    layer with the edited metadata
    """

    global ERRORS

    try:
        xml = open(file).read()
        draft.set_metadata(xml.encode('utf-8'), version_id=draft.version.id)
        return True
    except koordinates.exceptions.ServerError as e:
        ERRORS += 1
        logger.critical('metadata update for {0} fail with {1}'.format(draft.version.id,
                                                                        str(e)))
        return False

def remove_illegal_chars(title):
    """
    Removes illegal (unix + win) path chars
    """

    for illegal in ['<', '>', ':', '"', '/', '\\', '|', '?', '*', ',']: 
        if illegal in title:
             title = title.replace(illegal, '')
    return title

def get_metadata(layer, dir, overwrite):
    """
    Download the layers metadata file
    """

    global ERRORS

    title = remove_illegal_chars(layer.title)
    file_destination = os.path.join(dir,'{0}_{1}_{2}.iso.xml'.format(layer.type,
                                                                                        layer.id, 
                                                                                        title))

    if overwrite:
        file_exists(file_destination)
    
    try: 
        layer.metadata.get_xml(file_destination)
    except AttributeError as e:
        logger.critical(f"Failed to get XML for layer with ID {layer.id}: {str(e)}")
        ERRORS += 1
        return None

    # The koordiantes get_xml method dumps the 
    # xml as a single line :(
    # this the below
    with open(file_destination, 'r') as file:
        xml_content = file.read()

    # Parse and pretty print the XML
    xml_dom = parseString(xml_content)
    pretty_xml_as_string = xml_dom.toprettyxml()

    # Write the pretty-printed XML back to a file
    with open(file_destination, 'w') as file:
        file.write(pretty_xml_as_string)
    
    return file_destination



def update_metadata(dest_file, mapping):
    """
    Update the metadata file. If target_element is not None in the
    config it will do this only targeting said XML element. Else, 
    a regex find and replace will be performed across the entire file.
    """
    tree = ET.parse(dest_file)
    root = tree.getroot()
    
    # Extract namespaces and create a namespace dictionary
    namespaces = {node[0]: node[1] for _, node in ET.iterparse(dest_file, events=['start-ns'])}
    target_element = mapping.get('target_element')
    search_text = mapping['search']
    replace_text = mapping['replace']
    ignore_case = mapping['ignore_case']
    replace_entry = mapping.get('replace_entry')
    name_space = mapping.get('name_space')
    code_list = mapping.get('code_list')
    code_space = mapping.get('code_space')
    code_list_value = mapping.get('code_list_value')
    new_tag = mapping.get('new_tag')
    # Check if `search_text` contains capture groups (i.e., parentheses)
    has_capture_group = re.search(r'\((?!\?:|\?!|\?<=|\?<!).+?\)', search_text) is not None
        
    # Define a replacement function if capture groups are used
    def wrap_with_character_string(match):
        return f"<gmd:useLimitation>\n  <gco:CharacterString>{match.group(1)}</gco:CharacterString>\n</gmd:useLimitation>"



    

    if file_has_text(search_text, ignore_case, dest_file, target_element) or replace_entry:

 
        # If target_element is provided, target the specified XML element
        if target_element and replace_entry:
            # Find the target element, e.g., gco:CharacterString
            target_element_obj = root.find(target_element, namespaces)
            
            if target_element_obj is not None:
                # Get the parent element (e.g., gmd:country)
                parent_element = target_element_obj.getparent()

                if parent_element is not None:
                    # Remove the existing gco:CharacterString element
                    parent_element.remove(target_element_obj)

                    # Set up attributes for the new element
                    attributes = {}
                    if code_list:
                        attributes['code_list'] = code_list
                    if code_space:
                        attributes['code_space'] = code_space
                    if code_list_value:
                        attributes['code_list_value'] = code_list_value

                    # Create the new element with specified tag and attributes
                    new_element = ET.SubElement(parent_element, f'{{{namespaces["gmd"]}}}{new_tag.split(":")[1]}', attrib=attributes)
                    new_element.text = code_list_value

                    print(f"Replacement successful for {new_tag}.")
                else:
                    print("No parent element found for the target element.")
            else:
                print(f"Target element not found: {target_element}")

        elif target_element:
            # Target specific elements in the XML
            elements = root.findall(target_element, namespaces)
            for element in elements:
                if element is not None and element.text:
                    if ignore_case:
                        search_pattern = re.compile(search_text, flags=re.IGNORECASE | re.DOTALL)
                    else:
                        search_pattern = re.compile(search_text, flags=re.DOTALL)
                    
                    # Use `wrap_with_character_string` for capture groups; otherwise, direct replace_text
                    if has_capture_group:
                        element.text = re.sub(search_pattern, wrap_with_character_string, element.text)
                    else:
                        element.text = re.sub(search_pattern, replace_text, element.text)
        else:
            # Perform a generic find and replace in the entire file
            with fileinput.FileInput(dest_file, inplace=True) as file:
                for line in file:
                    if ignore_case:
                        search_pattern = re.compile(search_text, flags=re.IGNORECASE)
                    else:
                        search_pattern = re.compile(search_text)

                    # Use `wrap_with_character_string` if capture group exists; otherwise, replace_text
                    if has_capture_group:
                        line = re.sub(search_pattern, wrap_with_character_string, line.rstrip())
                    else:
                        line = re.sub(search_pattern, replace_text, line.rstrip())
                    
                    print(line)
            return

    # Register namespaces to ensure correct prefixes
    for prefix, uri in namespaces.items():
        if prefix:  # Skip empty prefixes
            ET.register_namespace(prefix, uri)

    tree.write(dest_file, encoding='utf-8', xml_declaration=True)


# def update_metadata(dest_file, mapping):
#     """
#     Update the metadata file. If target_element is not None in the
#     config it will do this only targeting said XML element. Else, 
#     a regex find and replace will be performed across the entire file.

#     Note, if using target_element regex ".*" can be used to replace
#     all values of an xml element. It is not safe to use this for the
#     when not using target_element and targeting the entire file
#     """
#     tree = ET.parse(dest_file)
#     root = tree.getroot()
    
#     # Extract namespaces and create a namespace dictionary
#     namespaces = {node[0]: node[1] for _, node in ET.iterparse(dest_file, events=['start-ns'])}
#     target_element = mapping.get('target_element')
#     search_text = mapping['search']
#     replace_text = mapping['replace']
#     ignore_case = mapping['ignore_case']

#     if file_has_text(search_text, ignore_case, dest_file, target_element):
#         if target_element:
#             # Target specific elements in the XML
#             elements = root.findall(target_element, namespaces)
#             for element in elements:
#                 if element is not None and element.text:
#                     if ignore_case:
#                         search_pattern = re.compile(search_text, flags=re.IGNORECASE | re.DOTALL)
#                     else:
#                         search_pattern = re.compile(search_text, flags=re.DOTALL)
                    
#                     # Ensure replacement is done only once
#                     element.text = re.sub(search_pattern, replace_text, element.text, count=1)
#         else:
#             # Perform a generic find and replace
#             with fileinput.FileInput(dest_file, inplace=True) as file:
#                 for line in file:
#                     if ignore_case:
#                         line = re.sub(search_text, replace_text, line.rstrip(), flags=re.IGNORECASE)
#                     else:
#                         line = re.sub(search_text, replace_text, line.rstrip())
#                     print(line)
#             return

#     # Register namespaces to ensure correct prefixes
#     for prefix, uri in namespaces.items():
#         if prefix:  # Skip empty prefixes
#             ET.register_namespace(prefix, uri)

#     tree.write(dest_file, encoding='utf-8', xml_declaration=True, pretty_print=True)


def set_metadata(layer, file, publisher):
    """
    Wraps several update methods.
    Gets Draft version of the layer, updates the metadata, 
    imports the draft and adds it to the publish group
    """

    # GET A DRAFT VERSION OF THE LAYER
    draft = get_draft(layer)
    if not draft:
        return False
    # UPDATE METADATA
    success = post_metadata(draft, file)
    # IMPORT DRAFT  File 
    if success:
        add_to_pub_group(publisher, draft)
    return success

def delete_draft(layer, version):
    """
    Delete a draft version 
    """
    global ERRORS

    try:
        layer.delete_version(version)
        logger.info('A draft already exists for {0}. This draft ' \
                'was deleted and a new one created '.format(layer.id))
        return True
    except koordinates.exceptions.ServerError as e:
        logger.critical('{0}'.format(e))
        ERRORS += 1
        return False

def get_draft(layer):
    """
    If no draft exists, create one. 
    Else return the current draft. 
    """
    
    global ERRORS

    if not draft_exists(layer):
        # Create new draft
        draft = layer.create_draft_version()
        return draft
    # A draft already exists for the layer
    draft = layer.get_draft_version()
    if hasattr(draft, 'active_publish'):
        if draft.active_publish:
            # and someone has attempted to publish it
            #TODO // automate deletion of publish group and then draft
            ERRORS += 1
            logger.critical('A draft already exists for {0} and is in a ' \
                            'publish group. THIS HAS NOT BEEN UPDATED '.format(layer.id))
            return None
        else:
            del_draft = delete_draft(layer, draft.version)
            if not del_draft:
                return None
            draft = layer.create_draft_version()
            return draft
    else:   #A draft exists but we know nothing of its state/ history
        del_draft = delete_draft(layer, draft.version)
        if not del_draft:
            return None
        draft = layer.create_draft_version()
        return draft
    

def draft_exists(layer):
    """
    Test if the published layer version is the
    most current. If not the most current version, 
    a draft version therefore already exists 
    """

    published_ver = str(layer.version.id)
    latest_ver = layer.latest_version
    m = re.search('versions\/([0-9]*)\/', latest_ver)
    latest_ver = m.group(1)
    if latest_ver == published_ver:
        return False
    return True

def add_to_pub_group(publisher, draft):
    """
    Add the draft version to the group 
    of layers to be published
    """

    if draft.type == 'layer':
        publisher.add_layer_item(draft)
    elif draft.type == 'table':
        publisher.add_table_item(draft)

def file_exists(file):
    """
    Remove file if duplicate.
    Useful for developers and testers. 
    """

    if os.path.isfile(file):
        os.remove(file)

def get_layer(client, id):
    """
    Get an object representing the layer as
    per the layer id parameter
    """

    global ERRORS

    # FETCH LAYER OBJECT AND METADATA FILE
    logger.info('Processing dataset: {0}'.format(id))

    try:
        layer = client.layers.get(str(id))
        return layer
    except koordinates.exceptions.ServerError as e:
        logger.critical('{0}'.format(e))
        ERRORS += 1
# 
# def update_doc():
#     """ 
#     TODO// Due to the current small number of CC licensed
#     documents this is out of scope 
#     """
#     pass
# 
# def update_set():
#     """ 
#     TODO// Currently out of development scope
#     """
#     pass

def iterate_all(client):
    """
    Iterate through the entire Data Service catalog.
    Returns a generator of all layer / table ids
    *Currently only layers and tables are handled
    """

    for item in client.catalog.list():
        if type(item) == type(koordinates.layers.Layer()):
            yield item.id
        else:
            try:
                logger.warning('Dataset {0}: Data is of "{1}" type. \
                This process only handles tables/layers'.format(item.id, type(item)))
            except:
                pass

def iterate_selective(layers): 
    """
    Iterate through user supplied (via config.yaml)
    dataset IDs. Returns a generator of layer ids to process
    """

    for layer_id in layers:
        yield layer_id

# def file_has_text(search_text, ignore_case, file):
#     """
#     Test for the search text in the file...
#     Because there is no point updating and posting a file
#     if there are no changes to be made.
#    """

def file_has_text(search_text, ignore_case, file,  target_element=None):
    """
    Test for the search text in the file or within a specified XML element.
    Because there is no point updating and posting a file
    if there are no changes to be made.
    """

    if target_element:
        # Parse the XML file
        tree = ET.parse(file)
        root = tree.getroot()
        element = root.find(target_element, NAMESPACES)
        if element is not None and element.text:
            flags = re.IGNORECASE if ignore_case else 0
            if re.search(search_text, element.text, flags=flags):
                return True
        elif not element: # if the element is there but is none, populate it
            return True
        return False
    else:
        # Generic text search in the file
        with open(file, 'r') as f:
            for line in f:
                if ignore_case:
                    match = re.search(search_text, line, flags=re.IGNORECASE)
                else:
                    match = re.search(search_text, line)
                if match:
                    return True
            return False

def element_is_present(file, element):
    tree = ET.parse(file)
    root = tree.getroot()
    namespaces = {
        'gmd': 'http://www.isotc211.org/2005/gmd',
        'gco': 'http://www.isotc211.org/2005/gco'   
    }

    # Search for the element using the specified path
    element_result = root.find(element, namespaces)

    if element_result is None:
        return False
    return True



def add_element(file, element_path, new_text=""):
    # Parse the XML file
    tree = ET.parse(file)
    root = tree.getroot()

    # Split the element path and filter out any initial "."
    path_parts = [part for part in element_path.split('/') if part and part != "."]
    parent = root

    for part in path_parts:
        # Parse the namespace and tag
        if ':' in part:
            namespace, tag = part.split(':')
            full_tag = f"{{{NAMESPACES.get(namespace, '')}}}{tag}"
        else:
            full_tag = part  # Use tag directly if no namespace is provided

        # Check for valid tag
        if not full_tag.strip():
            raise ValueError("Invalid tag or namespace in path")

        # Find or create the element
        next_element = parent.find(full_tag, NAMESPACES)
        if next_element is None:
            next_element = ET.SubElement(parent, full_tag)
        parent = next_element

    # Set the text for the final element in the path
    parent.text = new_text

    # Save the updated XML back to the file
    tree.write(file, encoding='utf-8', xml_declaration=True)


def create_backup(file, overwrite=False):
    """
    Create backup of metadata file to be edited
    """
    # Split the filename to insert `_BAK`
    backup_file = file.replace('.iso.xml', '_BAK.iso.xml')
    if overwrite:
        file_exists(backup_file)
    # Create a backup without altering the XML structure
    shutil.copyfile(file, backup_file)


def get_tree_hash(tree):
    """Generate a hash for the given XML tree."""
    xml_string = ET.tostring(tree.getroot(), encoding='utf-8')
    return hashlib.md5(xml_string).hexdigest()

# def ensure_path_exists(root, path, namespaces):
#     """Ensure that the entire path exists, creating any missing elements."""
#     elements = path.strip('./').split('/')
#     current_element = root
#     for elem in elements:
#         ns_prefix, tag = elem.split(':')
#         full_tag = f'{{{namespaces[ns_prefix]}}}{tag}'
#         next_element = current_element.find(full_tag)
        
#         if next_element is None:
#             # Create the missing element if it doesn't exist
#             next_element = ET.SubElement(current_element, full_tag)
#         current_element = next_element  # Move down to the next level
#     return current_element

def wrap_use_limitation_with_character_string(tree, namespaces):
    # Find all gmd:useLimitation elements
    for use_limitation in tree.findall('.//gmd:useLimitation', namespaces):
        # Check if it contains direct text
        if use_limitation.text and use_limitation.text.strip():
            # Store the current text
            text_content = use_limitation.text.strip()
            use_limitation.text = None  # Clear the direct text

            # Create a gco:CharacterString element and set its text
            character_string = ET.SubElement(use_limitation, f"{{{namespaces['gco']}}}CharacterString")
            character_string.text = text_content

    return tree

def delete_element(tree, target_path, namespaces):
    """Delete an element specified by the target path if it exists."""
    # Get the root of the tree
    root = tree.getroot()
    
    # Find the parent path and the tag to delete
    parent_path, tag_to_delete = target_path.rsplit('/', 1)
    
    # Ensure the parent element exists
    parent_element = ensure_path_exists(root, parent_path, namespaces)
    
    # Define the full tag for the element to delete
    ns_prefix, tag_name = tag_to_delete.split(':')
    full_tag = f'{{{namespaces[ns_prefix]}}}{tag_name}'
    
    # Find and remove the target element if it exists
    element_to_delete = parent_element.find(full_tag)
    if element_to_delete is not None:
        parent_element.remove(element_to_delete)
    
    return tree

def ensure_path_exists(root, path, namespaces):
    """Ensure that the entire path exists, creating any missing elements."""
    elements = path.strip('./').split('/')
    current_element = root

    for elem in elements:
        # Skip empty segments (if any)
        if not elem:
            continue

        # Ensure the element contains a namespace prefix and tag
        if ':' not in elem:
            raise ValueError(f"Element '{elem}' does not have a namespace prefix.")
        
        ns_prefix, tag = elem.split(':', 1)  # Only split on the first occurrence of ':'
        
        # Check if the namespace prefix exists in the namespaces dictionary
        if ns_prefix not in namespaces:
            raise ValueError(f"Namespace prefix '{ns_prefix}' not found in namespaces dictionary.")
        
        full_tag = f'{{{namespaces[ns_prefix]}}}{tag}'
        next_element = current_element.find(full_tag)
        
        if next_element is None:
            # Create the missing element if it doesn't exist
            next_element = ET.SubElement(current_element, full_tag)
        
        current_element = next_element  # Move down to the next level

    return current_element


def overwrite_element_value(tree, target_path, value, namespaces, tag_type='gco:CharacterString', attributes=None):
    """Overwrite or create an element's value, supporting both gco:CharacterString and gmd:LanguageCode with attributes."""
    # Ensure the full path exists up to the target element
    target_element = ensure_path_exists(tree.getroot(), target_path, namespaces)
    
    # Clear all existing children of the target element
    for child in list(target_element):
        target_element.remove(child)
    
    # Determine the namespace and tag for the inner element (e.g., gco:CharacterString or gmd:LanguageCode)
    ns_prefix, tag_name = tag_type.split(':')
    full_tag = f'{{{namespaces[ns_prefix]}}}{tag_name}'
    
    # Create the specified tag element within the target element with optional attributes
    if attributes and tag_type == 'gmd:LanguageCode':
        inner_element = ET.SubElement(target_element, full_tag, attrib=attributes)
    else:
        inner_element = ET.SubElement(target_element, full_tag)
    
    # Set or overwrite the text in the inner element
    inner_element.text = value
    
    return tree



def overwrite_or_add_element_with_code_list(tree, target_path, new_tag, attributes, text_content, namespaces):
    """
    Overwrite an existing element with a new element using code list attributes if it exists,
    or add it if missing. The wrapper element is inferred from the target_path.
    """
    # Extract the wrapper path and wrapper tag from the target path
    wrapper_path, wrapper_tag = target_path.rsplit('/', 1)
    parent_element = ensure_path_exists(tree.getroot(), wrapper_path, namespaces)

    # Define the wrapper element (e.g., <gmd:country>)
    ns_prefix, wrapper_name = wrapper_tag.split(':')
    full_wrapper_tag = f'{{{namespaces[ns_prefix]}}}{wrapper_name}'

    # Locate or create the wrapper element (e.g., <gmd:country>)
    wrapper_element = parent_element.find(full_wrapper_tag)
    if wrapper_element is None:
        wrapper_element = ET.SubElement(parent_element, full_wrapper_tag)

    # Clear any existing child elements within the wrapper element (e.g., remove <gco:CharacterString/>)
    for child in list(wrapper_element):
        wrapper_element.remove(child)

    # Define the new inner element (e.g., <gmd:Country>)
    ns_prefix, tag_name = new_tag.split(':')
    full_tag = f'{{{namespaces[ns_prefix]}}}{tag_name}'

    # Correct attribute names for code list standards
    corrected_attributes = {
        'codeList': attributes.get('code_list'),
        'codeSpace': attributes.get('code_space'),
        'codeListValue': attributes.get('code_list_value')
    }

    # Add the new <new_tag> (e.g., <gmd:Country>) inside the <wrapper_tag> (e.g., <gmd:country>)
    new_element = ET.SubElement(wrapper_element, full_tag, attrib=corrected_attributes)
    new_element.text = text_content

    return tree


def get_client(domain, api_key):
    """
    Return Koordinates API client
    """
    
    return koordinates.Client(domain, api_key)


def parse_args(args):
    cli_parser = argparse.ArgumentParser()
    cli_parser.add_argument('--config_file', 
                            default=None,
                            nargs='?',
                            help="Path to config file")
    return cli_parser.parse_args()

def main():
    """
    Script for updating LDS Metadata. Written for the purpose
    of replacing CC3 text with CC4 text but with scope for 
    extending to other metadata updating tasks     
    """

    global ERRORS

    cli_parser = parse_args(sys.argv[1:])
    config_file = cli_parser.config_file

    layer_count, layers_edited_count = 0,0

    # CONFIG LOGGING
    log.conf_logging('root')

    #CHECK PYTHON VERSION
    if sys.version_info<(3,3):
        raise SystemExit('Error, Python interpreter must be 3.3 or higher')

    # READ CONFIG IN
    config = ConfigReader(config_file)
    mapping = config.text_mapping
    # CREATE DATA OUT DIR
    os.makedirs(config.destination_dir, exist_ok = True) 
    # API CLIENT
    client = get_client(config.domain, config.api_key)
    # PUBLISHER
    publisher = koordinates.Publish()

    #SUMMARISED DATA
    xml_data = [] 
    missing_metadata = []

    if config.test_dry_run:
        logger.info('RUNNING IN TEST DRY RUN MODE')

    # ITERATE OVER LAYERS
    if config.layers in ('ALL', 'all', 'All'):
        layer_ids = iterate_all(client)
    else: 
        layer_ids = iterate_selective(config.layers)

    for layer_id in layer_ids:
        layer_count += 1
        get_layer_attempts = 0

        # GET LAYER OBJECT
        # lds is returning 504s (issue #15)
        while get_layer_attempts <= 3:
            get_layer_attempts += 1 
            layer = get_layer(client, layer_id) 
            if layer: 
                break
        if not layer:
            ERRORS += 1
            logger.critical('Failed to get layer {0}. THIS LAYER HAS NOT BEEN PROCESSED'. format(layer_id))
            continue

        # GET METADATA
        file = get_metadata(layer, config.destination_dir, config.test_overwrite)
        if not file:
            # Metadata does not exist for this entry - it has been logged as CRITICAL
            missing_metadata.append({'layer_id': layer.id, 
                                     'layer_title': layer.title, 
                                     'layer_url': layer.url,
                                      '__license_type': layer.license.type if layer.license and layer.license.type else None,
                                      '__license_url': layer.license.url if layer.license and layer.license.url else None, 
                                      '__is_public': 'True' if layer.public_access is not None else 'False'})
            continue

        # IF SUMMARISE, STORE ORIGINAL METADATA 
        if config.summarise:
            data = parse_xml_file(file)
            # Adding a few non-metadata fields to the summary
            data['__layer_id'] = layer_id
            data['__license_type'] = layer.license.type if layer.license and layer.license.type else None
            data['__license_url'] =layer.license.url if layer.license and layer.license.url else None
            data['__num_downloads'] =layer.num_downloads
            data['__first_published_at'] =layer.first_published_at.strftime('%Y-%m-%d')
            data['__is_public'] = True if layer.public_access is not None else False

            xml_data.append(data)

        # TEST IF SEARCH TEXT IN FILE (IN ORDER OF PRIORITY)

        ### With changes in requirements this needs a re think. 
        ## need function for each actions
        ## Blanket overwrite of element
        ## FInd and replace of element
        ## Blanket overwrite of element code list

        create_backup(file, config.test_overwrite)
        tree = ET.parse(file)
        initial_hash = get_tree_hash(tree)
        tree = wrap_use_limitation_with_character_string(tree, NAMESPACES)
        text_found, backup_created = False, False
        for i in range(1,len(mapping)+1):
            ## The element is missing from the file
            ## Leaving this out for now. Should create a flag to create element if does not exist
            # if mapping[i]['target_element'] and not element_is_present(file,  mapping[i]['target_element']) and not  mapping[i].get('replace_entry',False) :
            #     add_element(file,  mapping[i]['target_element'], mapping[i]['replace'])
            #     text_found = True
            
            target_element = mapping[i].get("target_element")

            if mapping[i].get("action") == "overwrite_element_code_list":
                code_list_value =  mapping[i].get("code_list_value")
                attributes_code_list = {
                    'code_list':  mapping[i].get("code_list"),
                    'code_space':  mapping[i].get("code_space"),
                    'code_list_value':  code_list_value
                }
                new_tag =  mapping[i].get("new_tag")
                text_content_code_list = code_list_value

                # Overwrite element with a code list
                tree = overwrite_or_add_element_with_code_list(tree, 
                                                                target_element, 
                                                                new_tag, 
                                                                attributes_code_list, 
                                                                text_content_code_list, 
                                                                NAMESPACES)

                # tree = overwrite_element_with_code_list(tree, 
                #                                 target_element, 
                #                                 new_tag,
                #                                 attributes_code_list,
                #                                 text_content_code_list, 
                #                                 NAMESPACES)
            if mapping[i].get("action") == "overwrite_element_str":
                new_value = mapping[i].get("new_value")
                tree = overwrite_element_value(tree, 
                                                target_element, 
                                                new_value, 
                                                NAMESPACES)
        # HACK
        delete_element(tree, './gmd:language/gco:CharacterString', NAMESPACES)
        tree_edited = initial_hash != get_tree_hash(tree)
        if tree_edited:
            print("The XML tree has been modified.")
            # Save the modified XML
            for prefix, uri in NAMESPACES.items():
                if prefix:  # Skip empty prefixes
                    ET.register_namespace(prefix, uri)
            tree.write(file, encoding='utf-8', xml_declaration=True)
        else:
            print("No changes were made to the XML tree.")



    #         # Just over ride the element with out looking at it. 
    #         # if mapping[i]['target_element'] and not element_is_present(file,  mapping[i]['target_element']) and mapping[i].get('code_list_value',False) :
    #         #     create_code_list_element(file,mapping[i]['target_element'],  mapping)
    #         #     text_found = True
    #         # elif  file_has_text(mapping[i]['search'], mapping[i]['ignore_case'], file, mapping[i]['target_element']):
    #         #     text_found = True
    #         # # elif mapping[i].get('replace_entry',False):
    #         # #     text_found = True
    #         #     # Only creating a backup if the original is edited 
    #         # if not backup_created and text_found:
    #         #     create_backup(file, config.test_overwrite)
    #         #     backup_created = True
    #         #     update_metadata(file, mapping[i])



        if not tree_edited:
            # remove the file and only keep those that were modified 
            base_dir = os.path.dirname(file)

            # Define the path for the new directory 'not_modified' within the base directory
            new_dir = os.path.join(base_dir, 'not_modified')

            # Create the 'not_modified' directory only if it doesn't exist
            os.makedirs(new_dir, exist_ok=True)

            # Define the destination path and copy the file
            new_file_path = os.path.join(new_dir, os.path.basename(file))
            shutil.move(file, new_file_path)
            logger.info('Dataset {0}: Skipping, no changes to be made'. format(layer_id))
            continue


            

        if config.test_dry_run:
            # i.e Do not update data service metadata
            continue

        if set_metadata(layer, file, publisher):
            layers_edited_count +=1
    
    # SUMMARISE WRITE METADATA TO XML 
    if config.summarise:
        workbook_file = os.path.join(config.destination_dir, 'metadata_summary.xlsx')
        write_to_excel(xml_data, workbook_file)

        # Those entries with no metadata associated
        missing_metadata_file =os.path.join(config.destination_dir, 'layers_missing_metadata.xlsx')
        record_missing_metadata(missing_metadata, missing_metadata_file)
        
 
    # PUBLISH
    if layers_edited_count > 0 and not config.test_dry_run:
        try:
            r = client.publishing.create(publisher)
            logger.info('{0} layer(s) processed | {1} layer(s) edited'. format(layer_count, 
                                                                               layers_edited_count))
        except koordinates.exceptions.ServerError as e:
            logger.critical('Publishing failed with fail with {0}'.format(str(e)))
            ERRORS += 1 
        except koordinates.exceptions.BadRequest as e:
            logger.critical('Publishing failed with fail with {0}'.format(str(e)))
            ERRORS += 1

    if ERRORS > 0:
        # print as well as log out
        print ('Process failed with {0} error(s). Please see log for critical messages'.format(ERRORS))
        logger.critical('Process failed with {0} error(s)'.format(ERRORS))
    else: 
        print('COMPLETE. No errors')
        logger.info('COMPLETE. No errors')

if __name__ == "__main__":
    main() 
