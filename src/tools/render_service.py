import jinja2
import os
import subprocess
import json
from typing import Dict, Union
from pydantic import BaseModel

class ResumeRenderer:
    def __init__(self, templates_dir: str = "templates", output_dir: str = "output"):
        self.templates_dir = templates_dir
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(self.templates_dir))

    def render_resume(
        self, 
        data: Union[Dict, BaseModel], 
        template_name: str = "modern_resume.tex"
    ) -> str:
        if isinstance(data, BaseModel):
            data = json.loads(data.model_dump_json())
        if isinstance(data.get("skills"), list):
            data["skills"] = ", ".join(data["skills"])
        template = self.env.get_template(template_name)
        rendered_tex = template.render(**data)
        tex_path = os.path.join(self.output_dir, "resume.tex")
        pdf_path = os.path.join(self.output_dir, "resume.pdf")
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(rendered_tex)
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-output-directory", self.output_dir, tex_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return pdf_path
