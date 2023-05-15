import sqlite3

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id):
        with self.connection:
            query = '''INSERT INTO users (user_id)
            VALUES (?)'''
            return self.cursor.execute(query,(user_id,))

    def user_exists(self, user_id):
        with self.connection:
            query = '''SELECT *
            FROM users
            WHERE user_id = ?
            '''
            result = self.cursor.execute(query, (user_id,)).fetchall()
            print(bool(len(result)))
            return bool(len(result))

    def set_experience(self, experience, user_id):
        try:
            with self.connection:
                print("sql", experience, user_id)
                query = '''UPDATE users
                            SET experience = ?
                            WHERE user_id = ?
                        '''
                return self.cursor.execute(query, (experience, user_id))

        except Exception as e:
            print(e)

    def get_signup(self, user_id):
        with self.connection:
            query = '''SELECT signup
            FROM users
            WHERE user_id = ?'''
            result = self.cursor.execute(query, (user_id,)).fetchall()
            for row in result:
                signup = str(row[0])
            return signup

    def set_signup(self, user_id, signup):
        with self.connection:
            query = '''UPDATE users
                        SET signup = ?
                        WHERE user_id = ?
            '''
            return self.cursor.execute(query, (signup, user_id))

    def get_admin(self, user_id):
        with self.connection:
            query = '''SELECT admin
            FROM users
            WHERE user_id = ?'''
            result = self.cursor.execute(query, (user_id,)).fetchall()
            for row in result:
                admin = str(row[0])
            return admin

    def get_applications(self):
        with self.connection:
            name_query = '''SELECT user_id
            FROM users
            WHERE signup = 'notapproved'
            '''
            exp_query = '''SELECT experience
            FROM users
            WHERE signup = 'notapproved'
            '''
            name_result = list(self.cursor.execute(name_query).fetchall())
            # name_result_string = '\n'.join(' \n'.join(x) for x in name_result)
            exp_result = list(self.cursor.execute(exp_query).fetchall())
            # exp_result_string = '\n'.join(' \n'.join(y) for y in exp_result)
            result = [None]*(len(name_result)+len(exp_result))
            result[::2] = name_result
            result[1::2] = exp_result
            return result

    def get_applications_number(self):
        pass
        # with self.connection:
        #     rows_amount = '''SELECT COUNT(signup)
        #     FROM users
        #     WHERE signup = 'notapproved'
        #     '''
        #     result = self.cursor.execute(rows_amount).fetchall()
        #     for x in result:
        #         resultList =
        #     print("sup")
        #     return ''.join(result)







#set admin, check if admin to approve; when approved send "You were accepted!" and change status to registered