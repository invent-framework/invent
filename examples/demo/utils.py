from js import document, window, Uint8Array
from pyodide.ffi.wrappers import add_event_listener


async def read_file(file):
    """Read the contents of the specified File object and return as bytes."""

    array_buffer = await file.arrayBuffer()

    return array_buffer.to_bytes().decode("utf-8")


def get_file_by_name(filename):
    """Get the File object with the specified name."""

    from invent.ui.widgets.fileupload import FileUpload

    return FileUpload.get_file_by_name(filename)