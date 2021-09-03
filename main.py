from Map import Map_Obj

map_obj = Map_Obj(task=1)
maps = map_obj.get_maps()
current_map = maps[0]
start_potition = map_obj.start_pos
goal_position = map_obj.end_goal_pos
