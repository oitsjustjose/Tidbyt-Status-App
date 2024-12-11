load("render.star", "render")
load("encoding/base64.star", "base64")

ICON = base64.decode("<IMAGE>")


def main():
    return render.Root(
        delay=0,
        child=render.Column(
            expanded=True,
            main_align="space_around",
            cross_align="center",
            children=[
                render.Row(
                    expanded=True,
                    main_align="space_evenly",
                    cross_align="center",
                    children=[
                        render.Image(ICON, width=16, height=16),
                        render.Marquee(
                            width=40,
                            child=render.Text(
                                "<SERVER-NAME>",
                                color="#a3be8c",
                                font="tom-thumb",
                            ),
                        ),
                    ],
                ),
                render.Marquee(
                    width=60,
                    child=render.Text(
                        "<ONLINE-PLAYERS> of <MAX-PLAYERS> Players",
                        color="#8fbcbb",
                        font="tom-thumb",
                    ),
                ),
            ],
        ),
    )
