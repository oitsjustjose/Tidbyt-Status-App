load("render.star", "render")
load("encoding/base64.star", "base64")


ICON = base64.decode(
    "UklGRlQAAABXRUJQVlA4TEcAAAAvD8ADEBcgEEhy2p9tDYFAkr/LjAsEkpz2Z3v+A/4VqIkkRdoiRAoqUbExITU279EQ0f/QpARqiIFcuw42/7XrDGRDCKRJAQA="
)


def main():
    return render.Root(
        child=render.Column(
            expanded=True,
            main_align="space_around",
            cross_align="center",
            children=[
                render.Image(src=ICON),
                render.Marquee(
                    width=64, child=render.Text("Taking a break between recordings (?)")
                ),
            ],
        )
    )
