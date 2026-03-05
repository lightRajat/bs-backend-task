from app.schemas import IdentifyRequest, IdentifyResponse
from fastapi import FastAPI

app = FastAPI()

@app.post("/identify", response_model=IdentifyResponse)
def identify(identity: IdentifyRequest):
    response = {
        "contact": {
            "primaryContatctId": 1,
            "emails": ["light.rajat@gmail.com"],
            "phoneNumbers": ["123456"],
            "secondaryContactIds": [],
        }
    }
    return response

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
