# STL: A class to apply different styles (hash and dash) to text
class Styler:
    def __init__(self, mth):
        self.mth = mth
        self.hashedstl_str = "#" * 30
        self.dashedstl_str = "-" * 30

    def hashed_style(self, cont_str):
        self.mth.say(self.hashedstl_str)
        self.mth.say("# " + cont_str + " #")
        self.mth.say(self.hashedstl_str)

    def dashed_style(self, cont_str):
        self.mth.say(self.dashedstl_str)
        self.mth.say("- " + cont_str + " -")
        self.mth.say(self.dashedstl_str)


# PGD: A class to manage a basic planar grid (2D grid)
class PlanarGrid:
    def __init__(self, width_i, height_i):
        # Initializes the grid with given width and height
        self._init_data(width_i, height_i)

    def _init_data(self, width_i, height_i):
        # Converts width and height to integers and calculates area
        self.width_i = int(width_i)
        self.height_i = int(height_i)
        self.area_i = int(width_i * height_i)
        self.grid_any_any_dic = (
            {}
        )  # Initializes an empty dictionary to store grid items

    # Adds a new item to the grid
    def append(self, itmkey_any, itmval_any):
        # Raises an error if the item key or value is empty
        if not itmkey_any or not itmval_any:
            raise TypeError(f"helper.PlanarGrid: 33 - Parameters Can Not Be Empty.")
        # Add the item to the grid dictionary
        self.grid_any_any_dic[itmkey_any] = itmval_any

    # Returns the size of the grid (total area)
    def get_size(self):
        return self.area_i

    # Checks if a particular item exists in the grid
    def has_item(self, itmkey_any):
        return itmkey_any in self.grid_any_any_dic


# SPG: A class to manage a slotted planar grid, which is essentially a grid with slots
class SlottedPlanarGrid:
    def __init__(self, width_i, height_i):
        # Creates a PlanarGrid object and initializes slot occupation list
        self.pgd = PlanarGrid(width_i, height_i)
        spgsize_i = width_i * height_i
        # Keeps track of occupied slots, initialized to 'False' (not occupied)
        self.occupied_b_li = [False] * spgsize_i

    # Helper method to check if an input is a tuple
    def _is_tuple(self, i_tup):
        return type(i_tup) is tuple

    # Checks if a given slot in the grid is available (unoccupied)
    def grid_slot_is_available(self, slotidx_i_tuple):
        # If no slot index is provided, assume it's unavailable
        if not slotidx_i_tuple:
            return False
        # Ensures the provided slot index is a tuple
        if not self._is_tuple(i_tup=slotidx_i_tuple):
            raise TypeError(
                f"helper.SlottedPlanarGrid: 56 - Tuple expected type: {type(slotidx_i_tuple)} given."
            )

        # Unpacks the tuple into coordinates
        tpgidxx_i = slotidx_i_tuple[0]
        tpgidxy_i = slotidx_i_tuple[1]

        occidx_i = tpgidxx_i * tpgidxy_i

        isvalididx_b = occidx_i < len(self.occupied_b_li)

        # If index is valid, return the occupation status of the slot
        if isvalididx_b:
            return self.occupied_b_li[occidx_i]
        else:
            return True  # If it doesn't know, it doesn't fuck with it. It is occupied.

    # Occupies a slot with an item if the slot is available
    def occupy(self, itmkey_i_tup, itmval_any):
        # Check if the slot is available
        if self.grid_slot_is_available(itmkey_i_tup):
            self.occupied_b_li[itmkey_i_tup] = True
            # Add the item to the grid
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


# Function to check if a key exists in a dictionary
def is_key_in_dict(id, dict):
    return id in dict
