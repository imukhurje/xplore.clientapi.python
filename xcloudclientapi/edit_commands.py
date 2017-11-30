import os
import subprocess

def parse_body(body):
    imports = []
    funcs = []
    all_lines = body.splitlines()
    current_function = None
    defs_started = False
    for line in all_lines:
        if not defs_started:
            imports.append(line)
        elif line.startswith('def '):
            e = { 'def' : line, 'lines' : [] }
            current_function = e
            funcs.append(e)
            defs_started = True
        else:
            current_function['lines'].append(line)
    return { 'imports' : imports, 'funcs' : funcs }

def unparse_body(parsed_body):
    imports = parsed_body['imports']
    funcs = parsed_body['funcs']
    imports_section = "\n".join(imports)
    funcs_section = ""
    for f in funcs:
        funcs_section += f['def'] + "\n"
        for l in f['lines']:
            funcs_section += l + "\n"
    body = imports_section + "\n" + funcs_section
    return body
  
def get_settings(jsonData):
    settings_file = '/var/www/xcloudclientapi/xcloudclientapi/settings.py'
    try:
        with open(settings_file, 'r') as f:
            body = f.read()
            result = { 'body' : body, 'language' : 'python' }
    except Exception as error:
        ret = { 'error_code' : 'XCFeatureFileReadError', 'error_msg' : 'ERROR: Could not read s.', 'result' : {} }
        return ret
        
    ret = { 'error_code' : '0', 'error_msg' : 'SUCCESS', 'result' : result }
    return ret

def get_code(jsonData):
    result = {}
    
    ret = { 'error_code' : '0', 'error_msg' : 'SUCCESS', 'result' : result }
    try:
        with open('/var/www/xcloudclientapi/xcloudclientapi/feature_commands/' + jsonData['feature'] + '.py', 'r') as f:
            body = f.read()
            result = { 'body' : body }
    except Exception as error:
        ret = { 'error_code' : 'XCFeatureFileReadError', 'error_msg' : 'ERROR: Could not read feature code.', 'result' : {} }
        return ret
        
    ret = { 'error_code' : '0', 'error_msg' : 'SUCCESS', 'result' : result }
        
    return ret

def save_settings(jsonData):
    result = {}
    ret = { 'error_code' : '0', 'error_msg' : 'SUCCESS', 'result' : result }
    body = jsonData['body']
    body = body.replace('&#39;',"'")
    try:
        with open('/var/www/xcloudclientapi/xcloudclientapi/settings.py', 'w') as f:
            f.write(body)
    except Exception as error:
        ret = { 'error_code' : 'XCFeatureFileWriteError', 'error_msg' : 'ERROR: Could not save feature code.', 'result' : {} }
    
    return ret

def save_code(jsonData):
    result = {}
    ret = { 'error_code' : '0', 'error_msg' : 'SUCCESS', 'result' : result }
    jsonData['body'].replace('&#39;',"'")
    try:
        with open('/var/www/xcloudclientapi/xcloudclientapi/feature_commands/' + jsonData['feature'] + '.py', 'w') as f:
            f.write(jsonData['body'])
    except Exception as error:
        ret = { 'error_code' : 'XCFeatureFileWriteError', 'error_msg' : 'ERROR: Could not save feature code.', 'result' : {} }
        
    return ret

def default_body():
    ret = """
def ceate(jsonData, settings):
    result = {}
    return { 'error_code' : '0', 'error_msg' : '', 'result' : result }

def readall(jsonData, settings):
    result = {}
    return { 'error_code' : '0', 'error_msg' : '', 'result' : result }

def readone(jsonData, settings):
    result = {}
    return { 'error_code' : '0', 'error_msg' : '', 'result' : result }

def remove(jsonData, settings):
    result = {}
    return { 'error_code' : '0', 'error_msg' : '', 'result' : result }

def resync(jsonData, settings):
    result = {}
    return { 'error_code' : '0', 'error_msg' : '', 'result' : result }
""".strip()
    return ret

def add_feature(jsonData):
    result = {}
    ret = { 'error_code' : '0', 'error_msg' : 'SUCCESS', 'result' : result }
    feature_body = default_body()
    try:
        with open('/var/www/xcloudclientapi/xcloudclientapi/feature_commands/' + jsonData['feature'] + '.py', 'w') as f:
            f.write(feature_body)
            subprocess_function()
    except Exception as error:
        ret = { 'error_code' : 'XCFeatureFileWriteError', 'error_msg' : 'ERROR: Could not Create feature.', 'result' : {} }
    return ret

def remove_feature(jsonData):
    result = {}
    ret = { 'error_code' : '0', 'error_msg' : 'SUCCESS', 'result' : result }
    try:
        pyfilename = '/var/www/xcloudclientapi/xcloudclientapi/feature_commands/' + jsonData['feature'] + '.py'
        if os.path.isfile(pyfilename):
            os.remove(pyfilename)
        if os.path.isfile(pyfilename + 'c'):
            os.remove(pyfilename + 'c')
    except Exception as error:
        ret = { 'error_code' : 'XCFeatureFileWriteError', 'error_msg' : 'ERROR: Could not remove feature code.', 'result' : {} }
    
    return ret

def add_function(jsonData):
    result = {}
    
    ret = { 'error_code' : '0', 'error_msg' : 'SUCCESS', 'result' : result }
    return ret

def modify_function(jsonData):
    result = {}
    
    ret = { 'error_code' : '0', 'error_msg' : 'SUCCESS', 'result' : result }
    return ret

def remove_function(jsonData):
    result = {}
    
    ret = { 'error_code' : '0', 'error_msg' : 'SUCCESS', 'result' : result }
    return ret
def subprocess_function():
    dir = '/var/www/xcloudclientapi'
    fileName = 'xcloudclientapi.wsgi'
    xtouch = '/usr/bin/touch ' + dir + '/' + fileName
    p = subprocess.Popen(xtouch, shell=True, stdout=subprocess.PIPE)
    
    
    