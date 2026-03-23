def get_todos(filepath):
    """
    Read a text file and return the list of to-do items.
    :param filepath:
    :return:
    """
    with open(filepath, "r", encoding="utf-8") as file_local:
        todos_local = file_local.readlines()
    return todos_local


def write_todos(todos_arg, filepath):
    """
    Write the to-do items list in the text file.
    :param todos_arg:
    :param filepath:
    :return:
    """
    with open(filepath, "w", encoding="utf-8") as file_local:
        file_local.writelines(todos_arg)

