import base64
import os
import re
from uuid import uuid4
from codeboxapi import CodeBox
from configs.setting import MEDIA_DIR

class CodeInterpreter:
    def __init__(self):
        self.output_files = ""
        self.output_codes = ""
        self.codebox = CodeBox(api_key="local")
        self.codebox.start()

    def get_outputs(self):
        return self.output_files,self.output_codes

    def run(self,code:str):
        clean_code = re.sub(r'(```python|```py|```)\s*', '', code, flags=re.IGNORECASE)
        clean_code = clean_code.strip()
        lines = [line for line in clean_code.split('\n') if line.strip()]
        cleaned_code = '\n'.join(lines)

        output = self.codebox.run(cleaned_code)

        if output.type == "image/png":
            filename = f"{MEDIA_DIR}/image-{uuid4()}.png"
            decoded_image = base64.b64decode(output.content)

            with open(filename,'wb') as file:
                file.write(decoded_image)

            image_url = f"/media/{os.path.basename(filename)}"
            self.output_files = image_url
            self.output_codes = code

            return f"Image got send to user."
        else:
            return output.content

code_interpreter = CodeInterpreter()