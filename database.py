#from pysqlcipher3 import dbapi2 as sqlite3
import sqlite3, os


class Database(object):
    def __init__(self, dbname):
        self.dbname = dbname

    def connDB(self):
        self.conn = sqlite3.connect(self.dbname)
        self.cursor = self.conn.cursor()
        #self.cursor.execute("PRAGMA key='mypassword'")
        self.cursor.execute("PRAGMA foreign_keys = ON")


    def createDB(self):
        self.connDB()
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            login TEXT NOT NULL,
            passwd TEXT,
            email TEXT UNIQUE,
            position TEXT);
            '''
        )

        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            regdate TEXT NOT NULL,
            altdate TEXT NOT NULL,
            lastAlter INTEGER,
            regType INTEGER NOT NULL,
            blocked INTEGER DEFAULT 0,
            name TEXT NOT NULL,
            birthFun TEXT NOT NULL,
            sex INTEGER NOT NULL,
            cpfcnpj TEXT NOT NULL UNIQUE,
            rgie TEXT UNIQUE,
            phone1op TEXT,
            phone1 TEXT,
            phone2op TEXT,
            phone2 TEXT,
            phone3 TEXT,
            email TEXT UNIQUE,
            cep TEXT,
            adress TEXT,
            number TEXT,
            adress2 TEXT,
            district TEXT,
            city TEXT,
            state TEXT,
            contry TEXT DEFAULT 'Brasil',
            FOREIGN KEY(lastAlter) REFERENCES staff(id) ON UPDATE CASCADE);
            '''
            )

        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS serviceOrders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idCli INTEGER,
            entryDate TEXT NOT NULL,
            altDate TEXT NOT NULL,
            outDate TEXT,
            lastAlter INTEGER,
            deviceType TEXT NOT NULL,
            brand TEXT NOT NULL,
            model TEXT,
            color TEXT NOT NULL,
            ns TEXT,
            barCode TEXT,
            imei1 TEXT,
            imei2 TEXT,
            acessories TEXT,
            deviceStatus TEXT,
            defect TEXT NOT NULL,
            obs1 TEXT,
            defectFound TEXT,
            serviceDone TEXT,
            serviceValue REAL,
            obs2 TEXT,
            status TEXT NOT NULL,
            FOREIGN KEY(idCli) REFERENCES clients(id) ON UPDATE CASCADE,
            FOREIGN KEY(lastAlter) REFERENCES staff(id) ON UPDATE CASCADE);
            '''
            )

        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            logo TEXT,
            name TEXT NOT NULL,
            slogan TEXT,
            phone1 TEXT,
            phone2 TEXT,
            phone3 TEXT,
            email TEXT,
            site TEXT,
            cep TEXT,
            adress TEXT,
            number TEXT,
            adress2 TEXT,
            district TEXT,
            city TEXT,
            state TEXT,
            contry TEXT DEFAULT 'Brasil',
            cnpj TEXT,
            im TEXT,
            ie TEXT);
            '''
        )
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            description TEXT NOT NULL,
            amount INTEGER NOT NULL,
            buyValue REAL NOT NULL,
            sellValue REAL NOT NULL,
            barCode TEXT UNIQUE);
            '''
        )
        # Em edição
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idProduct INTEGER,
            idOs INTEGER,
            idClient,
            dateTime TEXT NOT NULL,
            clientName TEXT NOT NULL,
            saleType TEXT NOT NULL,
            discount REAL DEFAULT 0,
            paid REAL,
            change REAL,
            FOREIGN KEY(idProduct) REFERENCES products(id) ON UPDATE CASCADE,
            FOREIGN KEY(idOs) REFERENCES serviceOrders(id) ON UPDATE CASCADE,
            FOREIGN KEY(idClient) REFERENCES clients(id) ON UPDATE CASCADE);
            '''
        )
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS soProducts (
            soId INTEGER,
            description TEXT NOT NULL,
            amount INTEGER NOT NULL,
            value REAL NOT NULL,
            FOREIGN KEY(soId) REFERENCES serviceOrders(id) ON UPDATE CASCADE);
            '''
        )

        self.cursor.execute(
            '''
            INSERT INTO staff (name, login, passwd)
            VALUES ('Admininstrator', 'admin', 'admin')
            '''
        )
        self.cursor.execute(
            '''
            INSERT INTO companies (logo, name, slogan, phone1, phone2, phone3, email, site, cep, adress, number, adress2, district, city, state)
            VALUES ('/home/alset/Documentos/github/erpy/IMG/logoblack.png', 'HL INFORMÁTICA', 'Assistência Técnica', '(21) 2617-4353', '(21) 98584-5457', '(21) 98584-5417', 'contato@hlinformatica.com', 'www.hlinformatica.com', '24753-660', 'Rua Manuel Gonçalves do Monte', '39', 'Loja 2', 'Rio do Ouro', 'São Gonçalo', 'Rio de Janeiro')
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
            r = self.cursor.lastrowid
            self.conn.close()
            return r
