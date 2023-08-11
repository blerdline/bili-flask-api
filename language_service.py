class LanguageService:
    def __init__(self, database):
        self.database = database

    def update_language(self, customer_id, language):
        language_data = {"langPref": language}
        cust_ref = self.database.db.collection('users').document(customer_id)
        cust_ref.set(language_data, merge=True)
        return f'Language updated to {language}'