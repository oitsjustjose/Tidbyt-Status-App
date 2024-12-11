load("render.star", "render")
load("encoding/base64.star", "base64")

ICON = base64.decode("<IMAGE>")


def main():
    return render.Root(
        delay=250,
        child=render.Column(
            expanded=True,
            main_align="space_around",
            cross_align="center",
            children=[
                render.Marquee(
                    width=60,
                    child=render.Text(
                        "<START_DATE> - <END_DATE>",
                        color="#66ded2",
                        font="tom-thumb",
                    ),
                ),
                render.Marquee(
                    width=60,
                    child=render.Text(
                        "<STAGE>",
                        color="#fc9c66",
                        font="tom-thumb",
                    ),
                ),
                render.Image(ICON),
            ],
        ),
    )
