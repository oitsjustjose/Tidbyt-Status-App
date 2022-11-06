load("render.star", "render")
load("encoding/base64.star", "base64")


ICON = base64.decode(
    "UklGRl4AAABXRUJQVlA4TFEAAAAvD8ADEBcgEEhy2p9tDYFAkr/LjAsEkpz2Z3v+A/4VMGojyVFrnwNl+GxEsyT2Hy4X0MMQ0f/QNAnUIUywt13+puHEyP+bhr/t8gnWIQikaQIA"
)


def main():
    return render.Root(
        child=render.Column(
            expanded=True,
            main_align="space_around",
            cross_align="center",
            children=[
                render.Image(src=ICON),
                render.Marquee(width=64, child=render.Text("Now Recording :)")),
            ],
        )
    )
