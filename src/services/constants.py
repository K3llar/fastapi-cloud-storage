import pathlib

"""TEMPLATES"""
EMPTY_FIELD = 'Field <{}> must be filled'
EXIST_FILE = 'File <{}> already exists'
NOT_FOUND = '<{}> not found'
BAD_FOLDER = 'Folder <{}> can`t be create'
BAD_W_FILE = 'Error with writing <{}>'

"""MESSAGES"""
INPUT_FILE = 'Select file to upload'
BAD_FILE = 'File can`t be read'

"""SCHEMAS"""
USER_FOLDER = 'storage\\{}\\'  # input user_id
BASE_FOLDER = pathlib.Path.cwd()
