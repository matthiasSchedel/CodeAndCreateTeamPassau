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

    def time_helper(self, time):
        snippet = ""
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
        #dispatcher.utter_message("QueryVeranstaltung started")
        vtype = tracker.get_slot('vtype')
        genre = tracker.get_slot('genre')
        time = tracker.get_slot('time')
        sql = "SELECT * FROM veranstaltung WHERE "
        if vtype is None:
            #dispatcher.utter_message("Vtype none")
            return
        sql += "vtype == '" + vtype + "' "
        if genre is not None:

            sql += " AND genre == '" + genre + "' "
        if time is not None:
            timesql = self.time_helper(time)
            print("time", time)
            print("timesql", timesql[19:29])
            sql += " AND date == '" + timesql[19:29] + "' "
        sql += " LIMIT 100;"
        # sql = "SELECT t.* From veranstaltung t WHERE date == slots['date'] AND genre == slots['genre'] AND vtype == slots['vtype'] LIMIT 100";
        be = Backend()
        res = be.eval(sql)
        if len(res) == 0:
            # dispatcher.utter_template("utter_")
            dispatcher.utter_template("utter_nothing_found")

        elif len(res) == 1:
            dispatcher.utter_template("utter_one_found")
            dispatcher.utter_message(str(res))
            result = res[0]
            dispatcher.utter_template("utter_result", filled_slots=None, name=result[0], vtype=result[1],
                                      time=result[3], genre=result[2])
        elif len(res) > 1 & len(res) < 100:
            dispatcher.utter_template("utter_more_found")
            for result in res:
                dispatcher.utter_template("utter_result", filled_slots=None, name=result[0], vtype=result[1],
                                          time=result[3], genre=result[2])
                print(res)
        ## else:
        tracker._reset()
        print('reset')
        pass
