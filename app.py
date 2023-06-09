from flask import Flask, request, jsonify, render_template

from PIL import Image
import io
import base64

from functions import change_background as cb


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/change_background", methods=["POST"])
def change_background():
    data = request.get_json()

    # Parse the image data from the request
    selfie_data = base64.b64decode(data["selfie"].split(",")[1])

    if data["background"] is not None:
        background_data = base64.b64decode(data["background"].split(",")[1])
        background = Image.open(io.BytesIO(background_data))

        # set resize option to what the user chose
        resize_option = data["resize_option"]
    else:
        # convert hex to rgb
        bg_color = data["bg_color"]
        bg_color = bg_color.lstrip("#")
        bg_color = tuple(int(bg_color[i : i + 2], 16) for i in (0, 2, 4))

        # Create image filled with color
        background = Image.new("RGB", (100, 100))
        background.paste(bg_color, (0, 0, background.size[0], background.size[1]))

        # set resize option to "background"
        resize_option = "background"

    # Load the images into PIL
    selfie = Image.open(io.BytesIO(selfie_data))

    # Change background
    result = cb(selfie, background, resize_option)

    # Convert the result to base64 to return in the response
    output_bytes = io.BytesIO()
    result.save(output_bytes, format="JPEG")
    output_bytes.seek(0)
    output_base64 = base64.b64encode(output_bytes.read())

    # Prepend the data type prefix
    output_base64_string = "data:image/jpeg;base64," + output_base64.decode("utf-8")

    # Return the result
    return jsonify({"result": output_base64_string})
