from pydantic import BaseModel, Field
from typing import Union, Literal, Optional

class TextUpload(BaseModel):
    file_type: Literal["text"] = Field(default="text")
    prompt: str = Field(description="User prompt for text analysis")
    description: str = Field(description="Description of the text content")

class PDFUpload(BaseModel):
    file_type: Literal["pdf"] = Field(default="pdf")
    prompt: str = Field(description="User prompt for PDF analysis")
    # File is handled separately in the endpoint, not in schema

class UploadRequest(BaseModel):
    upload: Union[TextUpload, PDFUpload] = Field(discriminator="file_type")
