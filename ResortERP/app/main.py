import os
import sys
from fastapi import FastAPI
import uvicorn
from app.routers.router import getRouters
from app.config.db import engine, Base
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # Optional: Add project root to Python path

class AppCreator():
    def __init__(self):
        self.app = FastAPI()
        self.app.include_router(getRouters())  # Updated to use getRouters()

# Create the FastAPI app at the module level so that uvicorn can find it.

# Drop all tables with CASCADE
# with engine.connect() as connection:
#     # Disable foreign key checks temporarily
#     connection.execute(text("DROP SCHEMA public CASCADE;"))
#     connection.execute(text("CREATE SCHEMA public;"))
#     connection.execute(text('GRANT ALL ON SCHEMA public TO postgres;'))
#     connection.execute(text('GRANT ALL ON SCHEMA public TO public;'))
#     connection.commit()

# Recreate all tables
Base.metadata.create_all(bind=engine)

app_creator = AppCreator()
app = app_creator.app

if __name__ == "__main__":
    # You can now start the app using the module's "app" attribute.
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
