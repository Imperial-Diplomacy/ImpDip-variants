import random
from DiploGM.models.turn import PhaseName
from DiploGM.models.province import ProvinceType
from DiploGM.models.unit import UnitType
if (board.data.get("conway") == "enabled"
    and board.turn.phase in (PhaseName.SPRING_MOVES, PhaseName.FALL_MOVES)):
    old_units = {}
    for u in board.units:
        old_units[u.province.name] = (u.player, u.unit_type)
    for p in board.provinces:
        if p.is_impassable:
            continue
        neighbours = {u for u in p.adjacencies.get_all() if u.name in old_units}
        if p.unit is not None and (len(neighbours) < 2 or len(neighbours) > 3):
            board.delete_unit(p)
        if p.unit is None and len(neighbours) == 3:
            owners = [old_units[n.name][0] for n in neighbours]
            unit_types = [old_units[n.name][1] for n in neighbours]
            if len(set(owners)) == 1:
                new_owner = owners[0]
            elif len(set(owners)) == 2:
                new_owner = owners[0] if owners.count(owners[0]) > 1 else owners[1]
            else:
                new_owner = None
            if p.type == ProvinceType.SEA:
                new_type = UnitType.FLEET
            elif p.is_landlocked():
                new_type = UnitType.ARMY
            elif unit_types.count(UnitType.ARMY) > 1:
                new_type = UnitType.ARMY
            else:
                new_type = UnitType.FLEET
            coast = None
            if new_type == UnitType.FLEET and p.adjacencies.coasts:
                coast = random.choice(list(p.adjacencies.coasts))
            board.create_unit(new_type, new_owner, p, coast, None)
