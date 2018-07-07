import sqlite3


class Backend():
    def __init__(self):
        ## datenbank datei name
        self.dbfile = "backend\pveranstaltung.db"

    def eval(self,sql,params=(),doprint=True):
        ## führt sql aus und liefert ergebnisse zurück
        conn = sqlite3.connect(self.dbfile)
        cursor = conn.cursor()
        cursor.execute(sql,params)
        res = cursor.fetchall()
        conn.close()
        if doprint:
            print(str(res))
        return res


    def setup(self):
        ## tear down, create, and populate database
        conn = sqlite3.connect(self.dbfile)
        cursor = conn.cursor()
        ## TODO einkommentieren und fertig implementieren
        print("SETTING up database")
        cursor.execute("DROP TABLE IF EXISTS veranstaltung")
        ## TODO datenbank felder definieren und db erzeugen
        cursor.execute("""CREATE TABLE veranstaltung (name text, vtype text, genre text, date text)""")
        ## TODO db mit beispieldaten befüllen
        cursor.execute("INSERT INTO veranstaltung VALUES('Rihanna', 'Konzert', 'Pop', '2018-07-08')")
        cursor.execute("INSERT INTO veranstaltung VALUES ('Metallica','Konzert','Rock','2018-02-08')")

        cursor.execute("INSERT INTO veranstaltung VALUES ('Lang Lang','Konzert','Klassisch','2018-04-08')")

        cursor.execute("INSERT INTO veranstaltung VALUES('Die Toten Hosen', 'Konzert', 'Rock', '2018-12-08')")

        cursor.execute("INSERT INTO veranstaltung VALUES('Bob Marley Open Air', 'Konzert', 'Klassisch', '2018-06-012')")

        conn.commit()
        ## einkommentieren, um db zu kontrollieren wenn erwünscht
        cursor.execute("SELECT count(*) from veranstaltung")
        print("DONE.. DB hat {} Einträge.".format(cursor.fetchall()[0][0]))
        conn.close()
