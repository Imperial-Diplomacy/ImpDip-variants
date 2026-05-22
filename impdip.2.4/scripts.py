from DiploGM.models.province import ProvinceType
from DiploGM.models.turn import PhaseName
if (board.data.get("conway") == "enabled" and board.turn.phase in (PhaseName.SPRING_MOVES, PhaseName.FALL_MOVES)):
    lonely_units = {}
    crowded_units = {}
    spawned_units = {}
    old_units = {}
    landlocked_provinces = set(p.name for p in board.provinces if p.is_landlocked())
    sea_provinces = set(p.name for p in board.provinces if p.type == ProvinceType.SEA)
    for u in board.units:
        old_units[u.province.name] = u.player
    for p in board.provinces:
        if p.is_impassable:
            continue
        neighbours = {u for u in p.adjacencies.get_all() if u.name in old_units}
        if p.unit is not None and len(neighbours) < 2:
            lonely_units.setdefault(p.unit.player.get_name() if p.unit.player is not None else "Neutral", set()).add(p.name)
            p.unit.unit_type = board.unit_types["X" + p.unit.unit_type.code]
        elif p.unit is not None and len(neighbours) > 3:
            crowded_units.setdefault(p.unit.player.get_name() if p.unit.player is not None else "Neutral", set()).add(p.name)
            p.unit.unit_type = board.unit_types["X" + p.unit.unit_type.code]
        elif p.unit is None and len(neighbours) == 3:
            owners = [old_units[n.name] for n in neighbours]
            if len(set(owners)) == 1:
                new_owner = owners[0]
            elif len(set(owners)) == 2:
                new_owner = owners[0] if owners.count(owners[0]) > 1 else owners[1]
            else:
                new_owner = None
            spawned_units.setdefault(new_owner.get_name() if new_owner is not None else "Neutral", set()).add(p.name)
            board.create_unit(board.unit_types["Y"], new_owner, p, None, None)

    message = "## Conway Phase results:\n"
    if lonely_units:
        message += "\n__Lonely units removed:__\n"
    for player in sorted(lonely_units.keys(), key=lambda p: p if p != "Neutral" else ""):
        message += f"- **{player}**: {', '.join(sorted(list(lonely_units[player])))}\n"
    if crowded_units:
        message += "\n__Crowded units removed:__\n"
    for player in sorted(crowded_units.keys(), key=lambda p: p if p != "Neutral" else ""):
        message += f"- **{player}**: {', '.join(sorted(list(crowded_units[player])))}\n"
    if spawned_units:
        message += "\n__New units spawned:__\n"
    for player in sorted(spawned_units.keys(), key=lambda p: p if p != "Neutral" else ""):
        message += f"- **{player}**:\n"
        if (armies := spawned_units[player] & landlocked_provinces):
            message += f"  Armies: {', '.join(sorted(list(armies)))}\n"
        if (fleets := spawned_units[player] & sea_provinces):
            message += f"  Fleets: {', '.join(sorted(list(fleets)))}\n"
        if (coastal := spawned_units[player] - landlocked_provinces - sea_provinces):
            message += f"  TBD: {', '.join(sorted(list(coastal)))}\n"
    if not lonely_units and not crowded_units and not spawned_units:
        message += "No changes"
