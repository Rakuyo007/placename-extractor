import os

def get_project_root_path():
    """
    Returns the path to the project root directory, which is two levels up from this script's location.
    """
    return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__))))

def get_static_folder_path():
    """
    Returns the path to the 'static' folder located in the same directory as this script.
    """
    return os.path.join(get_project_root_path(), 'static')


if __name__ == '__main__':
    pass
