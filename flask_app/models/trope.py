from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session

#Trope class for playing games
class Trope:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.is_flagged = data['is_flagged']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #method to get all tropes in database
    @classmethod
    def get_all_tropes(cls):
        query = "SELECT * FROM tropes;"
        results = connectToMySQL('htb_schema').query_db(query)
        db_tropes = []
        for trope in results:
            db_tropes.append(cls(trope))
        return db_tropes

    #method to get 24 random tropes in database
    @classmethod
    def get_random_tropes(cls):
        query = "SELECT * FROM tropes ORDER BY RAND() LIMIT 24;"
        results = connectToMySQL('htb_schema').query_db(query)
        random_tropes = []
        for trope in results:
            random_tropes.append(cls(trope))
        return random_tropes

    #method to get information from a single trope in the db based on id
    @classmethod
    def get_single_trope(cls, data):
        query = "SELECT * FROM tropes WHERE id = %(id)s;"
        results = connectToMySQL('htb_schema').query_db(query, data)
        db_single_trope = Trope(results[0])
        return db_single_trope

    #method to add trope to db
    @classmethod
    def add_to_db(cls, data):
        query = "INSERT INTO tropes (content, is_flagged, user_id) VALUES (%(content)s, %(is_flagged)s, %(user_id)s);"
        results = connectToMySQL('htb_schema').query_db(query, data)
        return results

    #method to update trope in db
    @classmethod
    def update_trope(cls, data):
        query = "UPDATE tropes SET content = %(content)s WHERE id = %(id)s;"
        results = connectToMySQL('htb_schema').query_db(query, data)
        return results

    #TODO: method to search for a trope
    @classmethod
    def searchTropes(cls, data):

        # query = "SET @search = %(search)s; SELECT * FROM tropes WHERE content LIKE CONCAT("%",@search,"%");"
        # query = "SET @search = %(search)s; SELECT * FROM tropes WHERE content LIKE "%"+@search+"%";"
        # query = "SELECT * FROM tropes WHERE content LIKE CONCAT('%', %(search)s, '%');"
        # query = "SELECT * FROM tropes WHERE content LIKE %(search)s;"
        # query = 'SELECT * FROM tropes WHERE content LIKE CONCAT(%(search)s,"%");'
        # query = "SELECT * FROM tropes WHERE content LIKE "%"+%(search)s+"%";"

        # works for isolated words, need to run ALTER TABLE tropes ADD FULLTEXT(content); before search will work
        query = "SELECT * FROM tropes WHERE MATCH (content) AGAINST (%(search)s IN BOOLEAN MODE);"
        results = connectToMySQL('htb_schema').query_db(query, data)
        return results

    #TODO method to flag trope with an issue
    @classmethod
    def flag_in_db(cls, data):
        query = "UPDATE tropes SET is_flagged = 1 WHERE id = %(id)s;"
        results = connectToMySQL('htb_schema').query_db(query, data)
        return results

    #method to delete trope from db
    @classmethod
    def delete_from_db(cls, data):
        query = "DELETE FROM tropes WHERE user_id = %(user_id)s AND id = %(id)s;"
        results = connectToMySQL('htb_schema').query_db(query, data)
