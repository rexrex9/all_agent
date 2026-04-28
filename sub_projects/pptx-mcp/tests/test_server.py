import pytest
import os
from pathlib import Path

# Adjust the import path based on the project structure
# Assuming server.py is in the root directory and tests/ is a subdirectory
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent)) # Add project root to path

from server import (
    create_or_clear_presentation,
    add_slide,
    add_shape,
    add_connector,
    delete_shape,
    modify_shape,
    get_slide_content_description,
    get_slide_image,
    SAVE_DIR,
    get_pptx_file,
    batch_update,
)

# Define the test filename
TEST_FILENAME = "test_basic_create.pptx"
TEST_FILE_PATH = SAVE_DIR / TEST_FILENAME

def test_create_or_clear_presentation():
    """
    Tests if create_or_clear_presentation successfully creates a new file
    and returns the correct message.
    """
    # Ensure the file doesn't exist before the test
    if TEST_FILE_PATH.exists():
        os.remove(TEST_FILE_PATH)

    try:
        # --- Execute ---
        result = create_or_clear_presentation(TEST_FILENAME)

        # --- Verify ---
        # 1. Check if the file was created
        assert TEST_FILE_PATH.exists(), f"File '{TEST_FILE_PATH}' was not created."
        assert TEST_FILE_PATH.is_file(), f"'{TEST_FILE_PATH}' is not a file."

        # 2. Check the return message
        expected_message = f"Presentation '{TEST_FILENAME}' created/cleared successfully in '{SAVE_DIR}'."
        assert result == expected_message, f"Unexpected return message: {result}"

    finally:
        # --- Cleanup ---
        # Remove the test file after the test runs
        if TEST_FILE_PATH.exists():
            try:
                os.remove(TEST_FILE_PATH)
                # Optional: print statement for visibility during test runs
                # print(f"\nCleaned up test file: {TEST_FILE_PATH}")
            except OSError as e:
                print(f"Error removing test file {TEST_FILE_PATH}: {e}")

@pytest.mark.asyncio
async def test_add_slide_with_shapes():
    """
    Tests if we can create a slide with shapes and text.
    Verifies the shapes and their text content are added correctly.
    """
    # Ensure the file doesn't exist before the test
    if TEST_FILE_PATH.exists():
        os.remove(TEST_FILE_PATH)

    try:
        # --- Setup ---
        # Create a new presentation
        create_or_clear_presentation(TEST_FILENAME)
        
        # --- Execute ---
        # Add a blank slide (layout_index=6 is blank)
        add_slide(TEST_FILENAME, layout_index=6)
        
        # Add a rectangle with text
        add_shape(
            filename=TEST_FILENAME,
            slide_index=0,
            shape_type_name="RECTANGLE",
            left_inches=1.0,
            top_inches=1.0,
            width_inches=2.0,
            height_inches=1.0,
            text="Rectangle Text"
        )
        
        # Add an oval with text
        add_shape(
            filename=TEST_FILENAME,
            slide_index=0,
            shape_type_name="OVAL",
            left_inches=4.0,
            top_inches=1.0,
            width_inches=2.0,
            height_inches=1.0,
            text="Oval Text"
        )
        
        # --- Verify ---
        # Get the slide description to verify shapes and text
        description = await get_slide_content_description(TEST_FILENAME, "0")
        
        # Check if both shapes are present
        assert "Shape 0: Type=AUTO_SHAPE" in description, "Rectangle shape not found"
        assert "Shape 1: Type=AUTO_SHAPE" in description, "Oval shape not found"
        
        # Check if text content is correct
        assert "Text='Rectangle Text'" in description, "Rectangle text not found"
        assert "Text='Oval Text'" in description, "Oval text not found"
        
        # Check if positions are correct (within description)
        assert "Left=1.00\", Top=1.00\"" in description, "Shape position not correct"
        assert "Width=2.00\", Height=1.00\"" in description, "Shape dimensions not correct"

    finally:
        # --- Cleanup ---
        if TEST_FILE_PATH.exists():
            try:
                os.remove(TEST_FILE_PATH)
            except OSError as e:
                print(f"Error removing test file {TEST_FILE_PATH}: {e}")

@pytest.mark.asyncio
async def test_get_slide_image():
    """
    Tests if we can successfully get an image of a slide.
    Verifies that the image is returned and has valid PNG data.
    """
    # Ensure the file doesn't exist before the test
    if TEST_FILE_PATH.exists():
        os.remove(TEST_FILE_PATH)

    try:
        # --- Setup ---
        # Create a new presentation
        create_or_clear_presentation(TEST_FILENAME)
        
        # Add a blank slide (layout_index=6 is blank)
        add_slide(TEST_FILENAME, layout_index=6)
        
        # Add some shapes to make the slide visually interesting
        add_shape(
            filename=TEST_FILENAME,
            slide_index=0,
            shape_type_name="RECTANGLE",
            left_inches=1.0,
            top_inches=1.0,
            width_inches=2.0,
            height_inches=1.0,
            text="Test Rectangle"
        )
        
        add_shape(
            filename=TEST_FILENAME,
            slide_index=0,
            shape_type_name="OVAL",
            left_inches=4.0,
            top_inches=1.0,
            width_inches=2.0,
            height_inches=1.0,
            text="Test Oval"
        )
        
        # --- Execute ---
        # Get the image of the slide
        image = get_slide_image(TEST_FILENAME, 0)
        
        # --- Verify ---
        # Check that we got an Image object
        assert image is not None, "Image object should not be None"
        
        # Check that the image data is not empty
        assert len(image.data) > 0, "Image data should not be empty"
        
        # Check that the image format is PNG
        assert image._format == "png", "Image format should be PNG"
        
        # Check that the image data starts with PNG signature
        assert image.data.startswith(b'\x89PNG\r\n\x1a\n'), "Image data should be a valid PNG file"

    finally:
        # --- Cleanup ---
        if TEST_FILE_PATH.exists():
            try:
                os.remove(TEST_FILE_PATH)
            except OSError as e:
                print(f"Error removing test file {TEST_FILE_PATH}: {e}")

@pytest.mark.asyncio
async def test_add_connector():
    """
    Tests adding a connector between two shapes.
    """
    if TEST_FILE_PATH.exists():
        os.remove(TEST_FILE_PATH)

    try:
        # Setup
        create_or_clear_presentation(TEST_FILENAME)
        add_slide(TEST_FILENAME, layout_index=6)
        # Add shapes and get their IDs from the return message
        msg1 = add_shape(TEST_FILENAME, 0, "RECTANGLE", 1, 1, 1, 1, "Start")
        msg2 = add_shape(TEST_FILENAME, 0, "OVAL", 4, 1, 1, 1, "End")

        start_id = int(msg1.split("(ID: ")[1].split(")")[0])
        end_id = int(msg2.split("(ID: ")[1].split(")")[0])

        # Execute
        conn_msg = add_connector(TEST_FILENAME, 0, start_id, end_id)

        # Verify
        description = await get_slide_content_description(TEST_FILENAME, "0")
        # Connectors often appear as Type=LINE or might be counted in total shapes
        assert "Shape 2: Type=LINE" in description or "Number of Shapes: 3" in description, "Connector shape not found in description"
        assert f"Added ELBOW connector" in conn_msg
        assert f"from shape {start_id}" in conn_msg
        assert f"to shape {end_id}" in conn_msg

    finally:
        if TEST_FILE_PATH.exists():
            try: os.remove(TEST_FILE_PATH)
            except OSError as e: print(f"Error removing test file {TEST_FILE_PATH}: {e}")


@pytest.mark.asyncio
async def test_delete_shape():
    """
    Tests deleting a shape from a slide.
    """
    if TEST_FILE_PATH.exists():
        os.remove(TEST_FILE_PATH)

    try:
        # Setup
        create_or_clear_presentation(TEST_FILENAME)
        add_slide(TEST_FILENAME, layout_index=6)
        msg1 = add_shape(TEST_FILENAME, 0, "RECTANGLE", 1, 1, 1, 1, "Keep")
        msg2 = add_shape(TEST_FILENAME, 0, "OVAL", 4, 1, 1, 1, "DeleteMe")
        keep_id = int(msg1.split("(ID: ")[1].split(")")[0])
        delete_id = int(msg2.split("(ID: ")[1].split(")")[0])

        # Execute
        delete_msg = delete_shape(TEST_FILENAME, 0, delete_id)

        # Verify
        description = await get_slide_content_description(TEST_FILENAME, "0")
        assert f"ID={delete_id}" not in description, "Deleted shape ID still found in description"
        assert "DeleteMe" not in description, "Deleted shape text still found"
        assert f"ID={keep_id}" in description, "Kept shape ID not found"
        assert "Keep" in description, "Kept shape text not found"
        assert "Number of Shapes: 1" in description, "Shape count after deletion is not 1"
        assert f"Deleted shape with ID {delete_id}" in delete_msg

    finally:
        if TEST_FILE_PATH.exists():
            try: os.remove(TEST_FILE_PATH)
            except OSError as e: print(f"Error removing test file {TEST_FILE_PATH}: {e}")


@pytest.mark.asyncio
async def test_modify_shape():
    """
    Tests modifying properties of an existing shape.
    """
    if TEST_FILE_PATH.exists():
        os.remove(TEST_FILE_PATH)

    try:
        # Setup
        create_or_clear_presentation(TEST_FILENAME)
        add_slide(TEST_FILENAME, layout_index=6)
        msg1 = add_shape(TEST_FILENAME, 0, "RECTANGLE", 1, 1, 2, 1, "Original Text")
        shape_id = int(msg1.split("(ID: ")[1].split(")")[0])

        # Execute modifications
        mod_msg1 = modify_shape(
            filename=TEST_FILENAME,
            slide_index=0,
            shape_id=shape_id,
            text="New Text",
            left_inches=0.5,
            top_inches=0.5
        )
        mod_msg2 = modify_shape(
            filename=TEST_FILENAME,
            slide_index=0,
            shape_id=shape_id,
            width_inches=3.0,
            height_inches=1.5,
            # fill_color_rgb=(255, 0, 0) # Verifying color via description is hard
        )

        # Verify
        description = await get_slide_content_description(TEST_FILENAME, "0")

        # Check modification messages (order-independent, without repeating 'updated')
        assert "text content" in mod_msg1
        assert "position (left)" in mod_msg1
        assert "position (top)" in mod_msg1
        assert "size (width)" in mod_msg2
        assert "size (height)" in mod_msg2

        # Check final state via description
        assert "Original Text" not in description, "Original text still found after modify"
        assert "Text='New Text'" in description, "New text not found after modify"
        assert "Left=0.50" in description, "Left position not modified correctly"
        assert "Top=0.50" in description, "Top position not modified correctly"
        assert "Width=3.00" in description, "Width not modified correctly"
        assert "Height=1.50" in description, "Height not modified correctly"

    finally:
        if TEST_FILE_PATH.exists():
            try: os.remove(TEST_FILE_PATH)
            except OSError as e: print(f"Error removing test file {TEST_FILE_PATH}: {e}")

@pytest.mark.asyncio
async def test_get_pptx_file():
    """
    Tests if get_pptx_file returns a valid FileResource for a created presentation.
    """
    # Ensure the file doesn't exist before the test
    if TEST_FILE_PATH.exists():
        os.remove(TEST_FILE_PATH)

    try:
        # --- Setup ---
        create_or_clear_presentation(TEST_FILENAME)

        # --- Execute ---
        resource = await get_pptx_file(TEST_FILENAME)

        # --- Verify ---
        # Check that the resource is a FileResource
        from fastmcp.resources import FileResource
        assert isinstance(resource, FileResource), "Returned resource is not a FileResource"
        # Check that the file exists
        assert resource.path.exists(), f"File {resource.path} does not exist"
        # Check the mime type
        assert resource.mime_type == "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        # Check the file signature (PPTX files are zip files, start with PK\x03\x04)
        file_bytes = resource.path.read_bytes()
        assert file_bytes[:4] == b'PK\x03\x04', "PPTX file does not start with correct ZIP signature"
    finally:
        # --- Cleanup ---
        if TEST_FILE_PATH.exists():
            try:
                os.remove(TEST_FILE_PATH)
            except OSError as e:
                print(f"Error removing test file {TEST_FILE_PATH}: {e}")

@pytest.mark.asyncio
async def test_batch_update_flow():
    """
    Tests the batch_update tool with a sequence of operations:
    - Create a slide
    - Add two shapes to the slide using temporary IDs
    - Modify one shape
    - Add a connector between them
    - Verifies the final slide content and batch replies.
    """
    test_batch_filename = "test_batch_presentation.pptx"
    test_batch_filepath = SAVE_DIR / test_batch_filename

    if test_batch_filepath.exists():
        os.remove(test_batch_filepath)

    try:
        # 1. Initial presentation creation (can be part of batch, but good to separate concerns for test clarity)
        create_or_clear_presentation(test_batch_filename)

        # 2. Define the batch requests
        requests = [
            {
                "create_slide": {
                    "layout_index": 6,  # Blank layout
                    "slide_object_id": "mySlide1"
                }
            },
            {
                "add_shape": {
                    "page_object_id": "mySlide1",
                    "shape_type_name": "RECTANGLE",
                    "left_inches": 1.0, "top_inches": 1.0, "width_inches": 2.0, "height_inches": 1.0,
                    "text": "Initial Box 1",
                    "shape_object_id": "box1"
                }
            },
            {
                "add_shape": {
                    "page_object_id": "mySlide1",
                    "shape_type_name": "OVAL",
                    "left_inches": 4.0, "top_inches": 1.0, "width_inches": 2.0, "height_inches": 1.5,
                    "text": "Box 2",
                    "shape_object_id": "box2"
                }
            },
            {
                "modify_shape": {
                    "page_object_id": "mySlide1",
                    "shape_object_id": "box1",
                    "text": "Modified Box 1 Text",
                    "fill_color_rgb": [255, 0, 0] # Red
                }
            },
            {
                "add_connector": {
                    "page_object_id": "mySlide1",
                    "start_shape_object_id": "box1",
                    "end_shape_object_id": "box2",
                    "connector_type_name": "ELBOW",
                    "shape_object_id": "connector1"
                }
            }
        ]

        # 3. Execute batch_update
        batch_result = batch_update(test_batch_filename, requests)

        # 4. Verify batch_update response
        assert batch_result is not None, "Batch result should not be None"
        assert batch_result.get("presentation_id") == test_batch_filename
        replies = batch_result.get("replies", [])
        assert len(replies) == len(requests), "Number of replies should match number of requests"

        assert "create_slide" in replies[0] and replies[0]["create_slide"].get("object_id") == "mySlide1"
        assert "add_shape" in replies[1] and replies[1]["add_shape"].get("object_id") == "box1"
        assert "add_shape" in replies[2] and replies[2]["add_shape"].get("object_id") == "box2"
        assert "modify_shape" in replies[3] and replies[3]["modify_shape"].get("object_id") == "box1"
        assert "add_connector" in replies[4] and replies[4]["add_connector"].get("object_id") == "connector1"

        # 5. Verify actual slide content
        # The new slide will be at index 0 as it's the first one added after creation
        description = await get_slide_content_description(test_batch_filename, "0")

        assert "Number of Shapes: 3" in description # Two shapes + one connector
        assert "Text='Modified Box 1 Text'" in description
        assert "Text='Box 2'" in description
        # Check for connector - its type might be AUTO_SHAPE or LINE depending on pptx interpretation
        # Check based on IDs from description to be more robust
        # We expect 3 shapes total. Their specific IDs are assigned by python-pptx, not our temporary IDs.

        # Example of a more robust check if needed (requires parsing shape IDs from description):
        # shape_ids_in_desc = [int(s.split("ID=")[1].split(",")[0]) for s in description.split("\n") if "ID=" in s]
        # assert len(shape_ids_in_desc) == 3

    finally:
        # --- Cleanup ---
        if test_batch_filepath.exists():
            try:
                os.remove(test_batch_filepath)
            except OSError as e:
                print(f"Error removing test file {test_batch_filepath}: {e}")
