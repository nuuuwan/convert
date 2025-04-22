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

        if text == "...":
            text = "\\sep"

        for before, after in [
            ("%", "\\%"),
            ("&", "\\&"),
            ("$", "\\$"),
            (" - ", "---"),
            ("...", "\\ldots"),
        ]:
            text = text.replace(before, after)

        text = TexDoc.replace_quotes_with_say(text)
        while "\n\n\n" in text:
            text = text.replace("\n\n\n", "\n\n")

        return text

    @staticmethod
    def get_latex_tag(tag: str) -> str:
        if tag == "h1":
            return "chapter"
        if tag == "h2":
            return "section"
        if tag == "h3":
            return "subsection"
        return ""

    @staticmethod
    def write_line(paragraph: Paragraph) -> str:
        text = TexDoc.clean(paragraph.text)
        md_tag = TexDoc.get_latex_tag(paragraph.tag)

        # \chapter*{Preface}
        # \addcontentsline{toc}{chapter}{Preface}
        if md_tag:
            return "".join(
                [
                    f"\\{md_tag}*{{{text}}}\n",
                    f"\\addcontentsline{{toc}}{{{md_tag}}}{{{text}}}\n",
                ]
            )
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

    def compile(self, file_path: str) -> None:
        dir_output = os.path.dirname(file_path)
        cmd = (
            "pdflatex"
            + " -interaction=nonstopmode"
            + " -quiet"
            + f" -output-directory={dir_output}"
            + f" {file_path}"
        )
        for i in range(2):
            log.debug(f"Running Compile {i + 1}")
            os.system(cmd)

        for ext in [".aux", ".log", ".out", ".toc"]:
            remove_file_path = file_path.replace(".tex", ext)
            if os.path.exists(remove_file_path):
                os.remove(remove_file_path)
        log.info(f"Compiled {file_path}")
