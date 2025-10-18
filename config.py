import os

class Config:
   MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://wissaltalbi65:eL1HHxlm6yHEsxo2@cluster0.qi2niyh.mongodb.net/?retryWrites=true&w=majority")
   MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "CORRECTOR")
