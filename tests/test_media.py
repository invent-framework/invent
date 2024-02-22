import invent


def test_get_set_media_root():
    """
    The media root, a path under which all media assets are found, can be
    set and get'd.
    """
    assert invent.get_media_root() == "."
    invent.set_media_root("/foo")
    assert invent.get_media_root() == "/foo"
    invent.set_media_root(".")
    assert invent.get_media_root() == "."


def test_media_paths():
    """
    Ensure the expected path is created by a chain of Media objects hanging
    off the "root" invent.media object (representing the media root).
    """
    media_asset = invent.media.images.picture.jpg
    assert str(media_asset) == "./media/images/picture.jpg"
    # Pretend we're in a PyScript.com app.
    invent.set_media_root("/@username/my-pyscript-app/latest")
    assert (
        str(media_asset)
        == "/@username/my-pyscript-app/latest/media/images/picture.jpg"
    )
    invent.set_media_root(".")
