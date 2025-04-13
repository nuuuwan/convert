from utils import File
import os


from convert.core.AbstractDoc import AbstractDoc, Paragraph


class TexDoc(AbstractDoc):
    @classmethod
    def get_ext(cls) -> str:
        return ".tex"

    @staticmethod
    def clean(text: str) -> str:
        # Remove non-ascii
        text = text.encode("ascii", "ignore").decode("ascii")
        return text

    @staticmethod
    def write_line(paragraph: Paragraph) -> str:
        text = TexDoc.clean(paragraph.text)
        if paragraph.tag == "h1":
            return f"\\section{{{text}}}\n"
        if paragraph.tag == "h2":
            return f"\\subsection{{{text}}}\n"
        if paragraph.tag == "h3":
            return f"\\subsubsection{{{text}}}\n"
        return f"{text}\n"

    def to_file(self, file_path: str) -> None:
        lines = [
            "\\documentclass{article}\n",
            "\\usepackage[utf8]{inputenc}\n",
            "\\begin{document}\n",
        ]
        for paragraph in self.paragraphs:
            line = TexDoc.write_line(paragraph)
            lines.append(line)

        lines += [
            "\\end{document}\n",
        ]

        File(file_path).write_lines(lines)

        # compile
        dir_output = os.path.dirname(file_path)
        os.system(
            "pdflatex "
            + "-interaction=nonstopmode "
            + f"-output-directory={dir_output} "
            + f"{file_path}"
        )
