from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
    
    
# def test_upload_text():
#     response = client.post(
#         "/upload",
#         data={"file_type": "text", "prompt": "What is AI?"}
#     )
    
#     assert response.status_code == 201
#     assert "message" in response.json()
#     assert response.json()["message"] == "Text upload received"
#     assert "query_result" in response.json()    
    
    
# def test_upload_pdf():
#     with open("test/DockerGuide.pdf", "rb") as pdf_file:
#         response = client.post(
#             "/upload",
#             data={"file_type": "pdf", "prompt": "Summarize the document."},
#             files={"file": ("DockerGuide.pdf", pdf_file, "application/pdf")}
#         )
    
#     assert response.status_code == 201
#     assert "message" in response.json()
#     assert response.json()["message"] == "PDF upload received"
#     assert "query_result" in response.json() 
    