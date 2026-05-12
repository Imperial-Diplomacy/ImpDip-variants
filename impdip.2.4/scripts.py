import random
from DiploGM.models.turn import PhaseName
from DiploGM.models.province import ProvinceType
if (board.data.get("conway") == "enabled"
    and board.turn.phase in (PhaseName.SPRING_MOVES, PhaseName.FALL_MOVES)):
    old_units = {}
    for u in board.units:
        old_units[u.province.name] = u.player
    for p in board.provinces:
        if p.is_impassable:
            continue
        neighbours = {u for u in p.adjacencies.get_all() if u.name in old_units}
        if p.unit is not None and (len(neighbours) < 2 or len(neighbours) > 3):
            board.delete_unit(p)
        if p.unit is None and len(neighbours) == 3:
            owners = [old_units[n.name] for n in neighbours]
            if len(set(owners)) == 1:
                new_owner = owners[0]
            elif len(set(owners)) == 2:
                new_owner = owners[0] if owners.count(owners[0]) > 1 else owners[1]
            else:
                new_owner = None
            board.create_unit(board.unit_types["Y"], new_owner, p, None, None)
