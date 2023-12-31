from enum import Enum

class Language(Enum):
    ENGLISH = "English",
    SPANISH = "Español"

class LanguageService:
    def __init__(self, database):
        self.database = database

    def update_language(self, customer_id, language):
        if not self.verify_language(language):
            return f'{language} is not a valid language'
        
        language_data = {"langPref": language}
        cust_ref = self.database.db.collection('users').document(customer_id)
        cust_ref.set(language_data, merge=True)
        return f'Language updated to {language}'
    
    def verify_language(self, language: str):
        if language in Language.__members__:
            return True
        else:
            return False