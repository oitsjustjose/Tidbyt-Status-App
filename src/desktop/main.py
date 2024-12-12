from os import getenv
import psutil


def main() -> None:
    backend_uri = getenv("TIDBYT_SERVER_URI", "http://172.16.1.6")
    for p in psutil.process_iter():
        print(p)


if __name__ == "__main__":
    main()
