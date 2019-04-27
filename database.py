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
            lastAlter INTEGER NOT NULL,
            regType INTEGER NOT NULL,
            blocked INTEGER DEFAULT 0,
            name TEXT NOT NULL,
            birthFun TEXT NOT NULL,
            sex INTEGER NOT NULL,
            cpfcnpj TEXT NOT NULL UNIQUE,
            rgie TEXT,
            cell1op TEXT,
            cell1 TEXT,
            cell2op TEXT,
            cell2 TEXT,
            tel TEXT,
            email TEXT,
            cep TEXT,
            adress TEXT,
            number TEXT,
            adress2 TEXT,
            district TEXT,
            city TEXT,
            state TEXT,
            contry TEXT DEFAULT 'Brasil',
            FOREIGN KEY(lastAlter) REFERENCES users(id) ON UPDATE CASCADE);
            '''
            )

        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS service_order (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idCli INTEGER NOT NULL,
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
            partTotalValue REAL,
            serviceValue REAL,
            total REAL,
            obs2 TEXT,
            status TEXT NOT NULL,
            FOREIGN KEY(idCli) REFERENCES clients(id) ON UPDATE CASCADE,
            FOREIGN KEY(lastAlter) REFERENCES users(id) ON UPDATE CASCADE);
            '''
            )

        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS company (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            logo TEXT,
            name TEXT NOT NULL,
            slogan TEXT,
            tel TEXT,
            cell1 TEXT,
            cell2 TEXT,
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
            CREATE TABLE IF NOT EXISTS os_itens (
            osId INTEGER NOT NULL PRIMARY KEY,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            value REAL NOT NULL,
            subTotal REAL NOT NULL);
            '''
        )

        self.cursor.execute(
            '''
            INSERT INTO users (name, login, passwd)
            VALUES ('Admininstrator', 'admin', 'admin')
            '''
        )
        self.cursor.execute(
            '''
            INSERT INTO company (logo, name, slogan, tel, cell1, cell2, email, site, cep, adress, number, adress2, district, city, state)
            VALUES ('/home/alset/Hotep/IMG/logoblack.png', 'HL INFORMÁTICA', 'Assistência Técnica', '(21) 2617-4353', '(21) 98584-5457', '(21) 98584-5417', 'contato@hlinformatica.com', 'www.hlinformatica.com', '24753-660', 'Rua Manuel Gonçalves do Monte', '39', 'Loja 2', 'Rio do Ouro', 'São Gonçalo', 'Rio de Janeiro')
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
