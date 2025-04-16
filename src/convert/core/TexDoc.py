import os
import re

from utils import File, Log

from convert.core.AbstractDoc import AbstractDoc, Paragraph

log = Log("TexDoc")


class TexDoc(AbstractDoc):
    @classmethod
    def get_ext(cls) -> str:
        return ".tex"

    @staticmethod
    def replace_quotes_with_say(text):
        def replacer(match):
            content = match.group(1)
            return f"\\say{{{content}}}"

        pattern = r'"(.*?)"'
        text = re.sub(pattern, replacer, text, flags=re.DOTALL)
        return text

    @staticmethod
    def clean(text: str) -> str:
        text = text.encode("ascii", "ignore").decode("ascii")

        for before, after in [
            ("%", "\\%"),
            ("&", "\\&"),
            ("$", "\\$"),
        ]:
            text = text.replace(before, after)

        if text == "...":
            text = "\\centerline{...}"

        text = TexDoc.replace_quotes_with_say(text)

        return text

    @staticmethod
    def write_line(paragraph: Paragraph) -> str:
        text = TexDoc.clean(paragraph.text)
        if paragraph.tag == "h1":
            return f"\\chapter*{{{text}}}\n"
        if paragraph.tag == "h2":
            return f"\\section*{{{text}}}\n"
        if paragraph.tag == "h3":
            return f"\\subsection*{{{text}}}\n"
        return f"{text}\n"

    def to_file(self, file_path: str) -> None:
        lines = File(
            os.path.join("src", "convert", "core", "tex.preamble.tex")
        ).read_lines()
        for paragraph in self.paragraphs:
            line = TexDoc.write_line(paragraph)
            lines.append(line)

        lines += [
            "\\end{document}\n",
        ]

        File(file_path).write_lines(lines)
        log.info(f"Wrote {file_path}")

        # compile
        dir_output = os.path.dirname(file_path)
        os.system(
            "pdflatex"
            + " -interaction=nonstopmode"
            + " -quiet"
            + f" -output-directory={dir_output}"
            + f" {file_path}"
        )

        for remove_file_path in [
            file_path.replace(".tex", ".log"),
            file_path.replace(".tex", ".aux"),
        ]:
            if os.path.exists(remove_file_path):
                os.remove(remove_file_path)
        log.info(f"Compiled {file_path}")
