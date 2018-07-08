from datetime import datetime
from rasa_core.actions import Action
from backend.backend import Backend


class QueryVeranstaltungenAction(Action):
    """
    action which uses slot/entity values to build an sql string and get and present results
    from database
    """

    def name(self):
        ## dieser Name wird in stories.md angegeben, wenn diese Aktion ausgeführt werden soll.
        return "query_veranstaltung_action"

    def time_helper(self,time):
        ## helper um datetime from duckling in sql zu bringen
        ## returns eine sql snippet
        snippet=""
        if type(time) == type({}):
            frm = time['from']
            frmdate = datetime.strptime(frm, "%Y-%m-%dT%H:%M:%S.000z")
            frmdatestr = str(frmdate.date())
            to = time['to']
            todate = datetime.strptime(to, "%Y-%m-%dT%H:%M:%S.000z")
            todatestr = str(todate.date())
            snippet = "date(date) BETWEEN '" + frmdatestr + "' AND '" + todatestr + "'"
        else:
            frmdate = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.000z")
            # if frmdate > datetime.now():
            frmdatestr = str(frmdate.date())
            snippet = "date(date) > date('" + frmdatestr + "')"
        return snippet

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("QueryVeranstaltung started")

        ## TODO variable aus slot werten holen. Variable Namen und slot namen definieren
        slots = {}
        slots['vtype'] = tracker.get_slot("vtype")
        slots['genre'] = tracker.get_slot("genre")
        slots['time'] = tracker.get_slot("time")
        ## TODO man kann debug Ausgaben erzeugen mit dispatcher.utter_message.
        ## einkommentieren für dbug messages wenn erwünscht
        dispatcher.utter_message("Query empfangen(debug)")
        for s in slots:
            if s is not None:
                dispatcher.utter_message("val "+s)
        ## TODO sql query bauen mit slot werte

        sql = "SELECT * FROM veranstaltung WHERE ";
        if ['vtype'] is None:
            dispatcher.utter_message("Vtype none")
            return
        #filled_slots = ['vtype'];
        sql += "vtype == '" + slots['vtype'] + "' ";
        if slots['genre'] is not None:
            sql += " AND genre == '" + slots['genre'] + "' ";
            #filled_slots.push('genre')
        if slots['time'] is not None:
            timesql = self.time_helper(slots['time'])
            print("timesql", timesql)
            sql += " AND date == '" + timesql + "' ";
            #filled_slots.push('time')

        sql += " LIMIT 100;";


            #sql = "SELECT t.* From veranstaltung t WHERE date == slots['date'] AND genre == slots['genre'] AND vtype == slots['vtype'] LIMIT 100";

        ##TODO bei bedarf time_helper verwenden, um time sql zu bekommen

        #for s in sql:
        dispatcher.utters_message("query string " + sql)
        ## TODO query gegen db ausführen
        be = Backend()
        res = be.eval(sql)
        dispatcher.utters_message("res string " + res)

        ## TODO  ergebnisse als text-prompt ausgeben
        if len(res) == 0:
            ## TODO bot utterance (action) für keine ergebnisse gefünden definieren (domain.yml) und hier referenzieren
            #dispatcher.utter_template("utter_")
            dispatcher.utter_template("utter_nothing_found")

        elif len(res)==1:
            ## TODO bot utterance (action) für ein ergebnis gefünden definieren (domain.yml) und hier referenzieren
            dispatcher.utter_template("utter_one_found")
            dispatcher.utter_message(str(res))
            result = res[0]
            ## TODO template mit params für ergebniss hier definieren und fertig implementieren
            dispatcher.utter_template("utter_result",filled_slots=None,name=result[0],vtype=result[1],time=result[2],genre=result[3])
        ## TODO wie oben aber für meherere ergebnisse
        elif len(res) > 1 & len(res) < 100:
            dispatcher.utter_template("utter_more_found")
            ## TODO utter template
            for result in res:
                dispatcher.utter_template("utter_result", filled_slots=None, name=result[0], vtype=result[1],
                                          time=result[2], genre=result[3])
                print(res)## TODO utter template mit ergebnisse
        ## TODO ??
        ## else:
            ##pass


