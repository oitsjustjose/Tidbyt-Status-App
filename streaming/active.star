load("render.star", "render")
load("encoding/base64.star", "base64")


ICON = base64.decode(
    "UklGRlgAAABXRUJQVlA4TEsAAAAvD8ADEBcgEEiy259oDSFBwv/oYed//gP+AmoiWa3eUCIFP/n28REdqSiZ0xkREf0PpUugC5bgBVGtBa3BWX9rVGtRm8iHXzCBlC4A"
)


def main():
    return render.Root(
        child=render.Column(
            expanded=True,
            main_align="space_around",
            cross_align="center",
            children=[
                render.Image(src=ICON),
                render.Marquee(width=64, child=render.Text("Now Streaming")),
            ],
        )
    )
