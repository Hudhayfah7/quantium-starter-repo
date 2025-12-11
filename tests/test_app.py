import os
import sys
import pytest

# Make sure Python can import app.py from the project root
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import app  # now this should work


@pytest.mark.parametrize("path", ["/"])
def test_header_present(dash_duo, path):
    """Check that the main header is present and has the right text."""
    dash_duo.start_server(app)

    header = dash_duo.find_element("h1")
    assert "Pink Morsel Sales Dashboard" in header.text


@pytest.mark.parametrize("path", ["/"])
def test_visualisation_present(dash_duo, path):
    """Check that the line chart / graph component renders."""
    dash_duo.start_server(app)

    # Wait for the graph container with id='sales-chart' to appear
    graph = dash_duo.wait_for_element("#sales-chart")
    assert graph is not None
    # Basic sanity check that it is the right element
    assert graph.get_attribute("id") == "sales-chart"


@pytest.mark.parametrize("path", ["/"])
def test_region_picker_present(dash_duo, path):
    """Check that the region radio buttons are rendered with 5 options."""
    dash_duo.start_server(app)

    # The radio component has id='region-radio'
    radio = dash_duo.wait_for_element("#region-radio")
    assert radio is not None

    # The inputs inside the radio component correspond to the options
    options = dash_duo.find_elements("#region-radio input")
    assert len(options) == 5  # All, North, East, South, West