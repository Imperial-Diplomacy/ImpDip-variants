from DiploGM.models.turn import PhaseName
if (board.data.get("conway") == "enabled" and board.turn.phase in (PhaseName.SPRING_MOVES, PhaseName.FALL_MOVES)):
    lonely_units = {}
    crowded_units = {}
    spawned_units = {}
    old_units = {}
    for u in board.units:
        old_units[u.province.name] = u.player
    for p in board.provinces:
        if p.is_impassable:
            continue
        neighbours = {u for u in p.adjacencies.get_all() if u.name in old_units}
        if p.unit is not None and len(neighbours) < 2:
            lonely_units.setdefault(p.unit.player.get_name() if p.unit.player is not None else "Neutral", []).append(p)
            board.delete_unit(p)
        elif p.unit is not None and len(neighbours) > 3:
            crowded_units.setdefault(p.unit.player.get_name() if p.unit.player is not None else "Neutral", []).append(p)
            board.delete_unit(p)
        elif p.unit is None and len(neighbours) == 3:
            owners = [old_units[n.name] for n in neighbours]
            if len(set(owners)) == 1:
                new_owner = owners[0]
            elif len(set(owners)) == 2:
                new_owner = owners[0] if owners.count(owners[0]) > 1 else owners[1]
            else:
                new_owner = None
            spawned_units.setdefault(new_owner.get_name() if new_owner is not None else "Neutral", []).append(p)
            board.create_unit(board.unit_types["Y"], new_owner, p, None, None)

    message = "## Conway Phase results:\n"
    if lonely_units:
        message += "\n__Lonely units removed:__\n"
        for player in sorted(lonely_units.keys(), key=lambda p: p if p != "Neutral" else ""):
            message += f"- **{player}**: {', '.join([u.name for u in lonely_units[player]])}\n"
    if crowded_units:
        message += "\n__Crowded units removed:__\n"
        for player in sorted(crowded_units.keys(), key=lambda p: p if p != "Neutral" else ""):
            message += f"- **{player}**: {', '.join([u.name for u in crowded_units[player]])}\n"
    if spawned_units:
        message += "\n__New units spawned:__\n"
        for player in sorted(spawned_units.keys(), key=lambda p: p if p != "Neutral" else ""):
            message += f"- **{player}**: {', '.join([u.name for u in spawned_units[player]])}\n"
    if not lonely_units and not crowded_units and not spawned_units:
        message += "No changes"
