from lib.helper import Styler, SlottedPlanarGrid


# gob
class GameObject:
    # Component classes (bodyparts, Cinematics, Place) don't use this
    # Game-Related classes (GameItem, GameAction) use this
    def __init__(self, id_str, name_str, candy_str):
        self._id_str = id_str
        self._name_str = name_str
        self._candy_str = candy_str

    def get_id(self):
        return self._id_str

    def get_name(self):
        return self._name_str

    def get_candy_description(self):
        return self._candy_str


# mva
class MoveAction(GameObject):
    def __init__(self, gbl_gmp):
        GameObject.__init__(
            self,
            id_str="0x40000",
            name_str="move_forward_action",
            candy_str="Move one grid forward.",
        )
        self.ALL_DIRECTIONS = ["f", "b", "l", "r"]
        self._gmp = gbl_gmp

    def _is_valid_input(self, in_str):
        return in_str in self.ALL_DIRECTIONS  # True if in_str is 'f', 'b', 'l', or 'r'

    def _dir_to_coordinates(self, dir_str):
        if dir_str == "f":  # Forwards
            return (1, 0)
        elif dir_str == "b":  # Backwards
            return (-1, 0)
        elif dir_str == "r":  # Right
            return (0, 1)
        elif dir_str == "l":  # Left
            return (0, -1)

    def _check_direction(self, dir_str):
        if self._is_valid_input(dir_str):
            tocoord_i_tup = self._dir_to_coordinates(dir_str)

            self._gmp.move_in(tocoord_i_tup)
            return f"You moved {dir_str}."
        else:
            return "You rethink your directions. Do you want to `move`, fordward(f), backwards(b), to the left (l), or to the right(r)?"

    def process_input(self, verb_str, data_str_li):
        if verb_str == "move":
            if not data_str_li:
                return "You rethink your action: Where... Were you moving?"
            else:
                return self._check_direction(data_str_li[0])
            # self._gmp = GameMap()


# itm
class Item(GameObject):
    def __init__(self, id_str, name_str, candy_str):
        GameObject.__init__(self, id_str=id_str, name_str=name_str, candy_str=candy_str)


# cin
class Cinematic(GameObject):
    def __init__(self, id_str, name_str, candy_str, cinematic_str, leavcond_fn=None):
        GameObject.__init__(self, id_str, name_str, candy_str)
        self.cinematic_str = cinematic_str
        self.leavcond_fn = leavcond_fn

    def play(self, mth, eas):  # Play cinematic
        mth.say(self.cinematic_str)
        if self.leavcond_fn:
            usrres_str = eas.listen(">: ")
            return self.leavcond_fn(usrres_str)
        return True


# plc
class Place:
    def __init__(
        self,
        plc_id,
        plcname_str,
        plcdesc_str,
        width_i,
        height_i,
        mth,
        itms_lis=[],
    ):
        # --
        self._init_class_variables(plc_id, plcname_str, plcdesc_str, mth, itms_lis)

    def _init_bodyparts(self, mth):
        self.plc_stl = Styler(mth)  # Styler's Mouth
        self.mth = mth

    def _init_class_variables(self, plc_id, plcname_str, plcdesc_str, mth, item_li=[]):
        # Init
        self.id = plc_id
        self.grid = SlottedPlanarGrid(5, 5)
        self.name_str = plcname_str
        self.desc_str = plcdesc_str
        self._init_bodyparts(mth)
        self.item_li = item_li

    # TODO: Use this.
    def _validate_data(self):
        validsize_b = True
        # Logic to validat data goes here
        if not validsize_b:
            raise RuntimeError('f"logic.GameMap: 201 - Under Construction."')

    def add_item_to(self, gridcoord_i_tup, plc):
        if self.is_grid_empty(gridcoord_i_tup):
            self._grid.occupy(itmkey_i_tup=gridcoord_i_tup, itmval_any=plc)
            return True
        else:
            return False

    def is_valid_list_index(self, idx_i):
        return idx_i > 0 and idx_i < len(self._occupied_li)

    def is_valid_grid_index(self, idx_i):
        return idx_i < len(self.gbdid_lis) and idx_i > 0

    def is_grid_occupied(self, grid_id):
        return self.occupied_b_lis[grid_id]

    def occupy_grid(self, grid_id, occupant_gbj):
        if self.is_valid_grid_id(grid_id=grid_id):
            if self.is_grid_occupied(grid_id=grid_id):
                return False
            else:
                self.grid_djb_id_lis[grid_id] = occupant_gbj.get_id()
                self.occupied_b_lis[grid_id] = True
                return True

    def unoccupy_grid(self, grid_id):
        if self.is_valid_grid_id(grid_id=grid_id):
            if self.is_grid_occupied(grid_id=grid_id):
                self.grid_dgb_id_lis[grid_id] = None
                self.occupied_b_lis[grid_id] = False

    def get_id(self):
        return self.id

    def _present_place(self):
        self.plc_stl.hashed_style(self.name_str)
        self.plc_stl.dashed_style("Morning")

    def _present_sing_item(self):
        if self._item_li[0] is not None:
            return f"{self.item_li[0].get_name()}."  # Display sole item.
        else:

            raise NameError("Error: Incorrect function selected by the program.")

    def _present_mult_items(self, range_i):
        out_str = ""
        for x in range(range_i):
            out_str += self.item_li[x].get_name() + ", "

        itm = self.item_li[range_i]
        itmname_str = itm.get_name()

        out_str += f"and {itmname_str}."

        return out_str

    def _present_items(self):
        self.mth.say("    In the room, you can see")
        out_str = "    "

        if self.item_li:
            lastitm_idx = len(self.item_li)

            # Single Item
            if lastitm_idx == 1:
                out_str += self.present_sing_item()
            # Multiple items
            else:
                out_str += self._present_mult_items(range_i=(lastitm_idx - 1))
        else:
            out_str += "nothing."

        self.mth.say(out_str)

    def present(self):
        self._present_place()
        self.mth.say(self.desc_str)
        self._present_items()


# gmp
class GameMap:
    def __init__(self, plcid_plc_dic={}):
        self._allplcs_plcid_plc_dic = plcid_plc_dic  # All places by id
        self.init_grid()

    # Initialize the Grid
    def init_grid(self):
        self._gridarea_i = 5 * 5
        self._plyloc_i_tup = (0, 0)  # top, right-most.
        self._gridwh_i_tup = (5, 5)  # total w and h of grid

        self._grid_plccoord_plcid_dic = {}  # All Id places by coordinate in map
        self._gridoccupied = [False] * self._gridarea_i

        for x in range(self._gridwh_i_tup[0]):
            for y in range(self._gridwh_i_tup[1]):
                self._grid_plccoord_plcid_dic[(x, y)] = None

    def valid_direction(self, gridcoord_i_tup):
        coordx_i = gridcoord_i_tup[0]
        coordy_i = gridcoord_i_tup[1]
        validx_b = coordx_i >= 0 and coordx_i < self._gridwh_i_tup[0]
        validy_b = coordy_i >= 0 and coordy_i < self._gridwh_i_tup[1]

        return validx_b and validy_b

    def add_place(self, plc, gridcoord_i_tup):

        if not self.valid_direction(gridcoord_i_tup):
            raise TypeError(
                f"logic.GameMap: 233 - Improper Coordinate. Coordinate given: {gridcoord_i_tup}"
            )

        gridexists_b = gridcoord_i_tup in self._grid_plccoord_plcid_dic
        if gridexists_b:
            gridisempty_b = self._grid_plccoord_plcid_dic[gridcoord_i_tup] == None
            if gridisempty_b:  # Grid has something in it
                plc_id = plc.get_id()
                self._allplcs_plcid_plc_dic[plc_id] = plc
                self._grid_plccoord_plcid_dic[gridcoord_i_tup] = plc_id
                return True
            else:
                return False

    def add_pointer(self, plc):
        self._plyloc_id = plc.get_id()

    def move_in(self, tocoord_i_tup):
        if not tocoord_i_tup:
            raise TypeError("logic.GameMap: 252 - Improper Coordinate")

        if tocoord_i_tup in self._grid_plccoord_plcid_dic:
            curplc_id = self._grid_plccoord_plcid_dic[tocoord_i_tup]

            if curplc_id:

                cur_plc = self._allplcs_plcid_plc_dic[curplc_id]
                self._plyloc_id = cur_plc.get_id()
                self.present_current_place(cur_plc)

                return True
            else:
                return False
        else:
            return False

    def present_current_place(self, plc=None):

        if plc is None:

            if self._plyloc_id in self._allplcs_plcid_plc_dic:
                plc = self._allplcs_plcid_plc_dic[self._plyloc_id]
            else:
                raise KeyError("logic.GameMap: 268 - Empty Grid Can't Present.")

        plc.present()
