import sys

from convert import Convert


def main(source_path: str, dest_path: str) -> None:
    Convert.convert(
        source_path=source_path,
        dest_path=dest_path,
    )


if __name__ == "__main__":
    main(
        source_path=sys.argv[1],
        dest_path=sys.argv[2],
    )
