from pysqlcipher3 import dbapi2 as sqlite3


class Database(object):
    def __init__(self, dbname):
        self.dbname = dbname

    def connDB(self):
        self.conn = sqlite3.connect(self.dbname)
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA key='mypassword'")

    def createDB(self):
        self.connDB()
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            login TEXT NOT NULL,
            passwd TEXT);
            '''
        )

        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS clients (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            regdate TEXT NOT NULL,
            altdate TEXT NOT NULL,
            regType TEXT NOT NULL,
            blocked INTEGER NOT NULL DEFAULT 0,
            name TEXT NOT NULL,
            birthFun TEXT NOT NULL,
            sex TEXT,
            cpfcnpj TEXT NOT NULL UNIQUE,
            rgie TEXT,
            cell1op TEXT,
            cell1 TEXT,
            cell2op TEXT,
            cell2 TEXT,
            tel3 TEXT,
            email TEXT,
            cep TEXT,
            adress TEXT,
            number TEXT,
            adress2 TEXT,
            district TEXT,
            city TEXT,
            state TEXT DEFAULT 'RJ',
            contry TEXT DEFAULT 'Brasil');
            '''
            )

        self.cursor.execute(
            '''
            INSERT INTO users (name, login, passwd)
            VALUES ("Admininstrator", "admin", "admin")
            '''
        )
        self.conn.commit()
        self.conn.close()

    def queryDB(self, sql):
        self.connDB()
        self.cursor.execute(sql)

        if sql[0:6].lower() == 'select':
            result = self.cursor.fetchall()
            self.conn.close()
            return result
        else:
            self.conn.commit()
            self.conn.close()
