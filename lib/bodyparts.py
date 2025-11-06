import os
from lib.logic import GameMap, Place, MoveAction
from lib.helper import (
    init_woodsword_item,
    init_toybox_item,
    init_wakeup_cinematic,
    init_witcot_place,
)


# Logic
# mth
class Mouth:
    def __init__(self):
        pass

    def say(self, str):
        print(str)

    def forget(self):
        if os.name == "nt":  # Win
            os.system("cls")
        else:  # Linux and Mac
            os.system("clear")


class Ears:
    def __init__(self):
        pass

    def listen(self, str):
        usin_str = input(str)
        return usin_str


class Brain:
    def __init__(self, mth, eas):
        self.mth = mth
        self.eas = eas
        self._init_class_variables()

    def _init_class_variables(self):
        # Collections
        self._cin_dic = {}
        self._cinid_lis = []
        self._usrin_str_lis = []
        self.gmp = GameMap()
        # Flags
        self.nextcin_b = True
        self.quit = True
        self.usr_response_str = ""
        # ---------
        self._start()

    def _add_user_input(self, usrin_str):
        self._usrin_str_lis.insert(0, usrin_str)

    # Actions
    def _quit(self):
        self.quit = True

    def _start(self):
        self.quit = False

    # Integrators
    def _integrate_cinematic(self, cin):
        self._cinid_lis.append(cin.get_id())
        self._cin_dic[cin.get_id()] = cin

    def _integrate_place(self, plc, gridcoord_i_tup):
        placeadded_b = self.gmp.add_place(plc, gridcoord_i_tup)
        self.gmp.add_pointer(plc)

        if not placeadded_b:
            raise ValueError(
                f"bodyparts.Brain: 71 - Unable to add Place. name: {plc.get_name()} id: {plc.get_id()}"
            )

    def load_places_and_cinematics(self, mth):
        # Places & Cinematics
        wakeup_cin = init_wakeup_cinematic()
        witcab_plc = init_witcot_place(mth)
        self._integrate_cinematic(wakeup_cin)
        self._integrate_place(plc=witcab_plc, gridcoord_i_tup=(0, 0))

    def load_actions(self, gmp):
        self.mva = MoveAction(gbl_gmp=gmp)

    def _input_controller(self):
        in_str = self.eas.listen(">: ")
        if in_str:
            usrin_str = in_str.split()

            verb_str = usrin_str[0]
            data_str_li = usrin_str[1:]

            if verb_str == "quit":
                self._quit()
            else:
                return self.mva.process_input(verb_str, data_str_li)

    # Runner
    def run(self):
        # Init
        self.load_places_and_cinematics(self.mth)
        self.load_actions(self.gmp)
        # Item

        # Helper Funcs
        nextcinauth_n_cininqueue = lambda: self.nextcin_b and self._cinid_lis
        cin_id_in_cin_lis = lambda: self._cinid_lis[0] in self._cinid_lis
        usrout_str = ""
        # Main Loop runs for as long as there are places to go
        while not self.quit:

            # Cinematic logic
            if nextcinauth_n_cininqueue():
                if cin_id_in_cin_lis():
                    cur_cin = self._cin_dic[self._cinid_lis.pop()]
                    while not cur_cin.play(self.mth, self.eas):
                        pass
                    self.nextcin_b = False

            self.gmp.present_current_place()
            if self._usrin_str_lis:
                nextusrin_str = self._usrin_str_lis[0]
                self.mth.say(nextusrin_str)
            usrout_str = self._input_controller()
            self._add_user_input(usrout_str)
