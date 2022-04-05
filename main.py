import uvicorn
import os
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers import mainpage_router
from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = mainpage_router.app
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])


if __name__ == "__main__":
    print(os.environ["DATABASE_URL"])
    uvicorn.run(app, host="0.0.0.0", port=8000)

# if __name__ == "__main__":
#     app = mainpage_router.app
#     origins = ["*"]
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=origins,
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )
#     app.mount("/app", StaticFiles(directory="static"), name="static")
#     uvicorn.run(app, host="127.0.0.1", port=8000)
