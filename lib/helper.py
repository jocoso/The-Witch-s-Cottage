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

    def grid_slot_is_available(self, slotidx_i_tuple):
        if not slotidx_i_tuple:
            return True

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


def init_toybox_item():
    from lib.logic import Item

    tybid_str = "0x30000"
    tybname_str = "a toy box"
    tybdesc_str = """
    The toybox looks old and weary. 
    However... Surprisingly sturdy as well."""

    return Item(id_str=tybid_str, name_str=tybname_str, candy_str=tybdesc_str)


def init_woodsword_item():
    from lib.logic import Item

    tybid_str = "0x30001"
    tybname_str = "a wooden sword"
    tybdesc_str = """
    Looks sturdy, smells rotten."""

    return Item(id_str=tybid_str, name_str=tybname_str, candy_str=tybdesc_str)


def is_key_in_dict(id, dict):
    return id in dict
