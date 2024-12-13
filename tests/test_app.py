import invent.app
import invent.ui
import upytest
import json
import umock


def test_initialise_app():
    """
    Test that the App class can be initialised with the correct attributes.
    """
    app = invent.app.App(
        name="Test App",
        icon="test-icon",
        description="A test app",
        author="Test Author",
        license="MIT",
    )
    assert app.name == "Test App"
    assert app.icon == "test-icon"
    assert app.description == "A test app"
    assert app.author == "Test Author"
    assert app.license == "MIT"
    # The app won't start unless it has at least one page.
    with upytest.raises(ValueError) as error:
        app.go()
        assert str(error.value) == "No pages in the app!"


def test_initialise_app_with_pages():
    """
    Test that the App class can be initialised with pages.
    """
    page1 = invent.ui.Page(name="Page 1")
    page2 = invent.ui.Page(name="Page 2")
    app = invent.app.App(name="Test App", pages=[page1, page2])
    assert len(app.pages) == 2
    assert app.pages[0] == page1
    assert app.pages[1] == page2


def test_initialise_app_with_media_root():
    """
    Test that the App class can be initialised with a media root.
    """
    app = invent.app.App(name="Test App", media_root="media")
    root = invent.get_media_root()
    assert root == "media", f"{root} is not 'media'"


def test_app_pages():
    """
    Test that the App class can add and remove pages.
    """
    app = invent.app.App(name="Test App")
    page1 = invent.ui.Page()
    page2 = invent.ui.Page()
    app.append(page1, page2)
    assert len(app.pages) == 2
    assert app.pages[0] == page1
    assert app.pages[1] == page2
    app.remove(page1.id)
    assert len(app.pages) == 1
    assert app.pages[0] == page2


def test_app_as_dict():
    """
    Test that the App class can be serialised to a dictionary that can be
    serialised to JSON.
    """
    app = invent.app.App(
        name="Test App",
        icon="test-icon",
        description="A test app",
        author="Test Author",
        license="MIT",
    )
    page1 = invent.ui.Page(name="Page 1")
    page2 = invent.ui.Page(name="Page 2")
    app.append(page1, page2)
    data = app.as_dict()
    assert data["name"] == "Test App"
    assert data["icon"] == "test-icon"
    assert data["description"] == "A test app"
    assert data["author"] == "Test Author"
    assert data["license"] == "MIT"
    assert len(data["pages"]) == 2
    assert data["pages"][0]["properties"]["name"] == "Page 1"
    assert data["pages"][1]["properties"]["name"] == "Page 2"
    assert json.dumps(data), "Could not serialise to JSON."


def test_app_singleton():
    """
    Test that the App class is a singleton.
    """
    my_app = invent.app.App(name="Test App")
    app1 = invent.app.App.app()
    app2 = invent.app.App.app()
    assert my_app is app1, f"{my_app} is not {app1}"
    assert app1 is app2, f"{app1} is not {app2}"


def test_app_get_page():
    """
    Test that the App class can retrieve a page by id.
    """
    app = invent.app.App(name="Test App")
    page = invent.ui.Page(name="Page 1")
    app.append(page)
    assert app.get_page(page.id) == page
    with upytest.raises(KeyError) as error:
        app.get_page("non-existent")
        assert str(error.value) == "No page with the id: non-existent"


def test_app_show_page():
    """
    Test that the App class can show a page by id, while hiding the current
    page.
    """
    page1 = invent.ui.Page(name="Page 1")
    page1.show = umock.Mock()
    page1.hide = umock.Mock()
    page2 = invent.ui.Page(name="Page 2")
    page2.show = umock.Mock()
    app = invent.app.App(page1, page2, name="Test App")
    app.show_page(page1.id)
    page1.show.assert_called_once()
    app.show_page(page2.id)
    page2.show.assert_called_once()
    page1.hide.assert_called_once()
    assert app._current_page == page2
    with upytest.raises(KeyError) as error:
        app.show_page("non-existent")
        assert str(error.value) == "No page with the id: non-existent"


def test_app_go():
    """
    Test that the App class start app.
    """
    page1 = invent.ui.Page(name="Page 1")
    page1.show = umock.Mock()
    page2 = invent.ui.Page(name="Page 2")
    page2.show = umock.Mock()
    app = invent.app.App(page1, page2, name="Test App")
    with umock.patch("invent.app:load_translations") as mock_lt:
        app.go()
        mock_lt.assert_called_once()
        page1.show.assert_called_once()
        page2.show.not_called()
        assert app._current_page == page1
