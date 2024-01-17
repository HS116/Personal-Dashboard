from sqlalchemy import create_engine


class Engine:
    def __init__(self, user: str, password: str, host: str, port: int, db_type: str, db_name: str):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db_type = db_type
        self.db_name = db_name

        self.db_engine = create_engine(f"{db_type}://{user}:{password}@{host}:{port}/{db_name}")

    def get_db_connection_url(self):
        return f"{self.db_type}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"
