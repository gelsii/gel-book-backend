from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseClient:
    def __init__(self):
        URI =   f'mongodb+srv://{os.getenv('USERNAME_DB')}:{os.getenv('PASSWORD_DB')}@cluster0.jcw95cy.mongodb.net/?appName=Cluster0'
        
        self.client = MongoClient(URI)
    
        self.db_collection_users = self.client.get_database('users_products')
    
        self.db_documents_user = self.db_collection_users['users_products']

        self.db_documents_tokens_expired = self.db_collection_users.get_collection('expired_tokens')

        self.db_documents_users_posts = self.db_collection_users.get_collection('users_post')

        self.db_documents_used_tokens = self.db_collection_users.get_collection("used_tokens")

        self.db_documents_global_chats = self.db_collection_users.get_collection("global_chats_users")
