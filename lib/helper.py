# stl
class Styler:
    def __init__(self, mth):
        self._mth = mth

    def hashed_style(self, cont_str):
        self._mth.say("#" * 30)
        self._mth.say("# " + cont_str + " #")
        self._mth.say("#" * 30)

    def dashed_style(self, cont_str):
        self._mth.say("-" * 30)
        self._mth.say("- " + cont_str + " -")
        self._mth.say("-" * 30)


# pgd
class PlanarGrid:
    def __init__(self, width_i, height_i):
        # _init_data(self) - puts (int) data
        self._init_data(width_i, height_i)

    def _init_data(self, width_i, height_i):
        self.width_i = int(width_i)
        self.height_i = int(height_i)
        self.area_i = int(width_i * height_i)
        self.grid_any_any_dic = {}

    def append(self, itmkey_any, itmval_any):
        if not itmkey_any or not itmval_any:
            raise TypeError(f"helper.PlanarGrid: 31 - Parameters Can Not Be Empty.")
        self.grid_any_any_dic[itmkey_any] = itmval_any

    def get_size(self):
        return self.area_i

    def has_item(self, itmkey_any):
        return itmkey_any in self.grid_any_any_dic


# spg
class SlottedPlanarGrid:
    def __init__(self, width_i, height_i):
        self.pgd = PlanarGrid(width_i, height_i)
        spgsize_i = width_i * height_i
        self.occupied_b_li = [False] * spgsize_i

    def _is_tuple(self, i_tup):
        return type(i_tup) is tuple

    def grid_slot_is_available(self, slotidx_i_tuple):
        if not slotidx_i_tuple:
            return True

        if not self._is_tuple(i_tup=slotidx_i_tuple):
            raise TypeError(
                f"helper.SlottedPlanarGrid: 56 - Tuple expected type: {type(slotidx_i_tuple)} given."
            )

        # idx is a tuple. (0, 0)
        tpgidxx_i = slotidx_i_tuple[0]
        tpgidxy_i = slotidx_i_tuple[1]

        occidx_i = tpgidxx_i * tpgidxy_i

        #
        isvalididx_b = occidx_i < len(self.occupied_b_li)

        if isvalididx_b:
            return self.occupied_b_li[occidx_i]
        else:
            return True  # If it doesn't know, it doesn't fuck with it. It is occupied.

    def occupy(self, itmkey_i_tup, itmval_any):
        if self.grid_slot_is_available(itmkey_i_tup):
            self.occupied_b_li[itmkey_i_tup] = True
            self.pgd.append(itmkey_i_tup, itmval_any)
            print("Plane has been occupied")


# Import Item system in progress


def init_witcot_place(mth):
    from lib.logic import Place

    toybox_itm = init_toybox_item()
    wsw_itm = init_woodsword_item()

    witcab_itup_itm_dic = {}
    witcab_itup_itm_dic[(5, 0)] = toybox_itm
    witcab_itup_itm_dic[(4, 0)] = wsw_itm

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
        itup_itm_dic=witcab_itup_itm_dic,
        mth=mth,
        width_i=5,
        height_i=5,
    )


def init_wakeup_cinematic():
    from lib.logic import Cinematic

    wakeup_id = "0x10000"
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
        cin_id=wakeup_id,
        name_str=wakeupname_str,
        candy_str=wakeupcandy_str,
        cinaction_str=wakeup_id_action,
        leavcond_fn=wakeupleavcond_b,
    )


def init_toybox_item():
    from lib.logic import Item

    tybid_str = "0x30000"
    tybname_str = "a toy box"
    tybdesc_str = """
    The toybox looks old and weary. 
    However... Surprisingly sturdy as well."""

    return Item(itm_id=tybid_str, name_str=tybname_str, candy_str=tybdesc_str)


def init_woodsword_item():
    from lib.logic import Item

    tybid_str = "0x30001"
    tybname_str = "a wooden sword"
    tybdesc_str = """
    Looks sturdy, smells rotten."""

    return Item(itm_id=tybid_str, name_str=tybname_str, candy_str=tybdesc_str)


def is_key_in_dict(id, dict):
    return id in dict
