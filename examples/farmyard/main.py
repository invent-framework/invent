import invent
from invent.ui import export
from invent.ui import *


# Datastore ############################################################################


# invent.datastore.setdefault("number_of_honks", 0)
# invent.datastore.setdefault("number_of_oinks", 0)

invent.datastore["number_of_honks"] = 0
invent.datastore["number_of_oinks"] = 0


# Code #################################################################################


def navigate(message):
    if message.button.name == "to_lucy":
        invent.show_page("Lucy")
    elif message.button.name == "to_percy":
        invent.show_page("Percy")
    elif message.button.name == "to_code":
        invent.show_page("Code")


def make_honk(message):
    invent.datastore["number_of_honks"] = (
        invent.datastore["number_of_honks"] + 1
    )
    invent.play_sound(invent.media.sounds.honk.mp3)


def make_oink(message):
    invent.datastore["number_of_oinks"] = (
        invent.datastore["number_of_oinks"] + 1
    )
    invent.play_sound(invent.media.sounds.oink.mp3)


def make_geese(number_of_honks):
    return [TextBox(text="🪿") for _ in range(number_of_honks)]


def make_pigs(number_of_oinks):
    return [TextBox(text="🐖") for _ in range(number_of_oinks)]


# Channels #############################################################################


invent.subscribe(navigate, to_channel="navigate", when_subject=["press"])
invent.subscribe(make_honk, to_channel="honk", when_subject=["press", "touch"])
invent.subscribe(make_oink, to_channel="oink", when_subject=["press", "touch"])


# User Interface #######################################################################


app = App(
    name="Farmyard!",
    content=[
        Page(
            name="Lucy",
            content=[
                Slider(
                    value=from_datastore("number_of_honks"),
                    name="Honk Slider",
                    position="FILL",
                    step=1,
                ),
                Column(
                    content=[
                        Image(
                            image=invent.media.images.goose.png,
                            channel="honk",
                            position="MIDDLE-CENTER",
                        ),
                        Row(
                            position="CENTER",
                            content=[
                                Button(
                                    name="button honk",
                                    label="HONK!",
                                    channel="honk",
                                    position="FILL",
                                ),
                                Button(
                                    name="to_percy",
                                    label="Visit Percy",
                                    channel="navigate",
                                    position="FILL",
                                ),
                                TextBox(
                                    name="number_of_honks",
                                    text=from_datastore("number_of_honks"),
                                    position="MIDDLE-CENTER",
                                ),
                            ],
                        ),
                        Row(
                            id="geese",
                            position="CENTER",
                            content=from_datastore(
                                "number_of_honks", with_function=make_geese
                            ),
                        ),
                        Button(
                            name="to_code",
                            label="Show Code",
                            channel="navigate",
                            position="FILL",
                        ),
                    ]
                ),
            ],
        ),
        Page(
            name="Percy",
            content=[
                Column(
                    content=[
                        Image(
                            image=invent.media.images.pig.png,
                            channel="oink",
                            position="MIDDLE-CENTER",
                        ),
                        Row(
                            position="CENTER",
                            content=[
                                Button(
                                    name="button oink",
                                    label="OINK!!",
                                    channel="oink",
                                ),
                                Button(
                                    name="to_lucy",
                                    label="Visit Lucy",
                                    channel="navigate",
                                    position="FILL",
                                ),
                                TextBox(
                                    name="number_of_oinks",
                                    text=from_datastore("number_of_oinks"),
                                    position="MIDDLE-CENTER",
                                ),
                            ],
                        ),
                        Row(
                            id="pigs",
                            position="CENTER",
                            content=from_datastore(
                                "number_of_oinks", with_function=make_pigs
                            ),
                        ),
                        Button(
                            name="to_code",
                            label="Show Code",
                            channel="navigate",
                            position="FILL",
                        ),
                    ],
                ),
            ],
        ),
    ],
)


# Add a page that shows the code! ######################################################


# app.content.append(
#     Page(
#         name="Code",
#         content=[
#             Row(
#                 content=[
#                     Button(
#                         name="to_lucy",
#                         label="Visit Lucy",
#                         channel="navigate",
#                         position="FILL",
#                     ),
#                     Button(
#                         name="to_percy",
#                         label="Visit Percy",
#                         channel="navigate",
#                         position="FILL",
#                     ),
#                 ]
#             ),
#             #Code(code=export.as_pyscript_app(app)[0]),
#             Code(code=export.as_dict(app)),
#         ],
#     )
# )


def to_minified_json(obj):
    import zlib
    import base64
    import json

    # Serialized JSON string
    serialized_json = json.dumps(obj)
    print("JSON length:", len(serialized_json))

    # Convert the serialized JSON string to bytes
    json_bytes = serialized_json.encode('utf-8')

    # Compress the bytes using gzip
    compressed_data = zlib.compress(json_bytes)#, level=zlib.Z_BEST_COMPRESSION)

    # Encode the compressed data using Base64
    encoded_data = base64.b64encode(compressed_data)

    result = encoded_data.decode('utf-8')
    print("MINIFIED length:", len(result))
    return result

def from_minified_json(minified_json):
    import zlib
    import base64

    encoded_data = minified_json#.decode('utf-8')
    # Base64-encoded string
    #encoded_data = "eJwzTcc0tTK3dPFSyC9LKE7MzlVLzs8FAA+A1YU="

    # Decode the Base64-encoded data
    decoded_data = base64.b64decode(encoded_data)

    # Decompress the data using zlib
    decompressed_data = zlib.decompress(decoded_data)

    # Print the decompressed data
    import json
    return json.loads(decompressed_data.decode('utf-8'))


from pprint import pprint
app_as_dict = export.as_dict(app)
pprint(app_as_dict)

print("*"*40)
minified_json = to_minified_json(app_as_dict)
print(minified_json, len(minified_json), type(minified_json))

print("-"*40)
app_dict = from_minified_json(minified_json)
print(app_dict, type(app_dict))

print(app_dict == app_as_dict)

# GO! ##################################################################################


invent.go()
