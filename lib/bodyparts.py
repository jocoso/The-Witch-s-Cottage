import os
from lib.logic import GameMap, Cinematic, Place, MoveAction
from lib.helper import init_woodsword_item, init_toybox_item


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
        # Collections
        self._cin_dic = {}
        self._cinid_lis = []
        self._gmp = GameMap()
        # Flags
        self._nextcin_b = True
        self._quit = True
        self.usr_response_str = ""
        # ---------
        self.start()

    # Actions
    def quit(self):
        self._quit = True

    def start(self):
        self._quit = False

    # Integrators
    def integrate_cinematic(self, cin):
        self._cinid_lis.append(cin.get_id())
        self._cin_dic[cin.get_id()] = cin

    def integrate_place(self, plc, gridcoord_i_tup):
        placeadded_b = self._gmp.add_place(plc, gridcoord_i_tup)
        self._gmp.add_pointer(plc)

        if not placeadded_b:
            raise ValueError(
                f"bodyparts.Brain: 63 - Unable to add Place. name: {plc.get_name()} id: {plc.get_id()}"
            )

    def _init_wakeup_cinematic(self):
        wakeupid_str = "0x10000"
        wakeupname_str = "wakeup_cinematic"
        wakeupcandy_str = "First Cinematic."
        wakeup_id_action = """
        You wake up in a strange place. Your mouth is dry, your head is throbing,
        and your mouth is full with the metallic taste of blood.
    
        "Ah! You are awake."

        A weak, creakly voice utters beyond your eyes reach.
        "You are almost ready love, don't spoil the surprise!"
        A figure appears to your right, a smiling shadow. 
        Her index finger playfully lays
        at the tip of your nose and you feel the burning sensation of a cold touch. 
        Her eyes are completely white. You are staring at two moons, and they stare
        right back at your.

        "Go to sleep sweetheart. You will feel better tomorrow, I promise."

        You feel your eyes closing. You try to resist it, but it's futile.
        The need to rest takes ahold...

        ...

        You can't tell how long it took you to regain consiensness.
        When you eyes open once more you indeed feel better but also...
        the shadow is gone...

        You are alone.
        Input 'c' to continue...
        """

        wakeupleavcond_b = lambda a: a == "c"

        return Cinematic(
            id_str=wakeupid_str,
            name_str=wakeupname_str,
            candy_str=wakeupcandy_str,
            cinematic_str=wakeup_id_action,
            leavcond_fn=wakeupleavcond_b,
        )

    def _init_witcot_place(self, mth):

        tyb_itm = init_toybox_item()
        wsw_itm = init_woodsword_item()

        itms_lis = []
        itms_lis.append(tyb_itm)
        itms_lis.append(wsw_itm)

        witcab_plc_id_str = "0x20000"
        witcab_plc_name_str = "Witch's Cottage"
        witcab_plc_desc_str = """
        A small cozy environ.
        Light rushes in from every window, drawing circles on the cottage's
        stone floor.
        The walls are wooden, green vines slithering on their surface like snakes."""

        return Place(
            plc_id=witcab_plc_id_str,
            plcname_str=witcab_plc_name_str,
            plcdesc_str=witcab_plc_desc_str,
            itms_lis=itms_lis,
            mth=mth,
            width_i=10,
            height_i=10,
        )

    def load_places_and_cinematics(self, mth):
        # Places & Cinematics
        wakeup_cin = self._init_wakeup_cinematic()
        witcab_plc = self._init_witcot_place(mth)
        self.integrate_cinematic(wakeup_cin)
        self.integrate_place(plc=witcab_plc, gridcoord_i_tup=(0, 0))

    def load_actions(self, gmp):
        self._mva = MoveAction(gbl_gmp=gmp)

    def _input_controller(self):
        in_str = self.eas.listen(">: ")
        if in_str:
            usrin_str = in_str.split()

            verb_str = usrin_str[0]
            data_str_li = usrin_str[1:]

            if verb_str == "quit":
                self.quit()
            else:
                self.mth.say(self._mva.process_input(verb_str, data_str_li))

    # Runner
    def run(self):
        # Init
        self.load_places_and_cinematics(self.mth)
        self.load_actions(self._gmp)
        # Item

        # Helper Funcs
        nextcinauth_n_cininqueue = lambda: self._nextcin_b and self._cinid_lis
        cin_id_in_cin_lis = lambda: self._cinid_lis[0] in self._cinid_lis

        # Main Loop runs for as long as there are places to go
        while not self._quit:
            # Cinematic logic
            if nextcinauth_n_cininqueue():
                if cin_id_in_cin_lis():
                    cur_cin = self._cin_dic[self._cinid_lis.pop()]
                    while not cur_cin.play(self.mth, self.eas):
                        pass
                    self._nextcin_b = False

            self._input_controller()
            self._gmp.present_current_place()
