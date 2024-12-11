load("render.star", "render")
load("encoding/base64.star", "base64")


ICON = base64.decode(
    "UklGRmAAAABXRUJQVlA4TFMAAAAvD8ADEBcgEEiC33sNgUCS2f5UCwkS/g+2Ov8B/woYtY0kqTTPhtJ8isNoUAyJ/s/eu+G5HCL6H1ohgSa0BfFCdl85XN+wf/W9rnwhF8SEJpBWCAA="
)


def main():
    return render.Root(
        child=render.Column(
            expanded=True,
            main_align="space_around",
            cross_align="center",
            children=[
                render.Image(src=ICON),
                render.Marquee(width=64, child=render.Text("In a Zoom Meeting")),
            ],
        )
    )
