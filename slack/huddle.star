load("render.star", "render")
load("encoding/base64.star", "base64")


ICON = base64.decode(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAASCAYAAABSO15qAAAACXBIWXMAAC4jAAAuIwF4pT92AAACQklEQVQ4jaWUQWgTQRSGv5ndJLubNG2JtlpiPPSi1lsPCiJexN70VAQVVBAvHvRSKEJB1JNeiqeKiHfBg/QiQgUVCx70ZNWDoVrSojZRk2yS3e3ujIdsq7ZBCn3weG9mfn7mzf/mCa01WzHzwGx1/d5h4IEQdlOr6hGvftfTqvpSCLsXuAjM/EPQgXQKGIzzk0ATGI7Xd4Chv8GyA8F0O2jAKIBMt3MAwg0ldCAYBx4jjC6tG/No75zA+C/BQWAMcAAFeMBnMIta/XqKagiktYpvxXEiLmvSBJ4DyQ330CtIo9/H6FnSqoYQNkAZOARcj1EnzHpXpgwMKClI+QGWF9BI26hEAsKs23TteXQLRJKaSL1J6bDfISRCAFTMvu/lPcBoYiXMVXK9O0v5bHL3lx+fHE8UQ+lO+8olFN6oCd3H1ML9b6RZEJkxi+gn8MicunS1DrQsz/cWdg2MFwfzwfDb92ec5UBHfRp74h3kwq/SlT15XbtZE5ZRxiolUD5QF5Xe43PAPiUNbK91Ot3wnGo2cy9oJTH7gpHMZFEYufBJ5Bo0SZAkIkWEapdQMutdmb2r79ZI26VyjlMA2jSQ6eT+iFRdItGxlCEmzT/q503gKHADmANeAJcBhKOIFq1C9DFzxRhZ3qZdYwgoABbtBmwBt03gWeyrlgXQgUB2r2i53S9oX76O5Z5dr3anVm5bIBA94bzY4Z/FN2aAV8CtzRA4ayehCAnkEnLtL1zYDME1YBEoAg9j/wAsAefXg8VWB8pv0SnWrEYYD8cAAAAASUVORK5CYII="
)


def main():
    return render.Root(
        child=render.Column(
            expanded=True,
            main_align="space_around",
            cross_align="center",
            children=[
                render.Image(src=ICON),
                render.Row(
                    expanded=True,
                    main_align="space_around",
                    cross_align="center",
                    children=[render.Text("In a Huddle"),]
                )
            ],
        )
    )
