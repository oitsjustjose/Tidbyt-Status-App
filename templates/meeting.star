load("render.star", "render")
load("encoding/base64.star", "base64")


ICON = base64.decode(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAA0lBMVEVHcEzAOSshCghHFxIrDgvJQjS4NinnTDzmSzvAOSutOCxpIhtBFRDHQTPnTDzaRzh0Jh7hSjrIQTTOPzFTGBKxNShVGRNsIBgUBgQzDwsaCAZcHhdRGRN9JRyGLCNnIhqRLCEbCAZZGhREFhGDKB6ILCOsOCwxDgvIQTRTGRLbSDgWBgViHRbAOStdHhg4EQ0VBgSwNCdLFhFXGhTKQjRqHxe8NyrnTDzAOSvmSzvPQDHIPS7hSTndRzfgSTnSQTPJPS7KPi/NPzDcRzfLPi/DOix335QqAAAAN3RSTlMA/gshEbLc+PT7ilAfr/vQTOO2/j/ET2EGHgY1QW5bOoULTx5yXIsZrz/TBk76NyEGx0FSumPlq3smowAAAI9JREFUGNNVzucOglAMBeCigODeeyvDvW0v4Nb3fyVvIia9/dcvzekBgGwmAXyKeUzzvV1CTCUZdAUi5hjULxIKDFoVxLLOQ2pX7ChfGqEwFGiagegrUrVv1kCRnhZYDoA+9yexDOkeGeujbOiOfjK16fmSDaPHOL6ZmUSfd0gr75+zPe00ovOSZ28O+wXAF2g4D32JsaTjAAAAAElFTkSuQmCC"
)


def main():
    return render.Root(
        child=render.Box(
            render.Row(
                expanded=True,
                main_align="space_around",
                cross_align="center",
                children=[
                    render.Image(src=ICON, width=16, height=16),
                    render.Text("On A Call", color="#c83d2e", font="tom-thumb"),
                ],
            )
        )
    )
