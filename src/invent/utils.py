"""
Utility functions.
"""


from pyscript import window
from invent.ui import App


def play_sound(url):
    sound = window.Audio.new(str(url))
    sound.play()


def show_page(page_name):
    App.app().show_page(page_name)


async def read_file(file):
    """
    Read the contents of the specified JS File object as a string.
    """
    array_buffer = await file.arrayBuffer()

    return array_buffer.to_bytes().decode("utf-8")


async def read_files(filenames):
    """
    Read the contents of the files with the specified filenames.

    Returns a list of strings.
    """
    return [
        await read_file(get_file_by_name(filename))

        for filename in filenames or []
    ]


def get_filenames():
    """Return the filenames of all uploaded files."""

    from invent.ui.widgets.fileupload import FileUpload

    return FileUpload.get_filenames()


def get_file_by_name(filename):
    """Get the File object with the specified name."""

    from invent.ui.widgets.fileupload import FileUpload

    return FileUpload.get_file_by_name(filename)