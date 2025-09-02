from .world import World
from .room import Room
from .exit import Exit


def create_seed_world() -> World:
    """Create a seed world with 4 rooms in a 2x2 grid for development."""

    world = World()

    # Create 4 rooms
    room_1 = Room(
        id="room_1",
        name="Forest Clearing",
        description="A peaceful clearing in the forest. Sunlight filters through the canopy above.",
        exits=[
            Exit(keyword="east", target_room_id="room_2", movement_phrase="go east"),
            Exit(keyword="south", target_room_id="room_3", movement_phrase="go south"),
        ],
    )

    room_2 = Room(
        id="room_2",
        name="Cave Entrance",
        description="A dark cave entrance looms before you. Cool air flows from within.",
        exits=[
            Exit(keyword="west", target_room_id="room_1", movement_phrase="go west"),
            Exit(keyword="south", target_room_id="room_4", movement_phrase="go south"),
        ],
    )

    room_3 = Room(
        id="room_3",
        name="River Bank",
        description="A gentle river flows by. You can hear the water babbling over smooth stones.",
        exits=[
            Exit(keyword="north", target_room_id="room_1", movement_phrase="go north"),
            Exit(keyword="east", target_room_id="room_4", movement_phrase="go east"),
        ],
    )

    room_4 = Room(
        id="room_4",
        name="Old Ruins",
        description="Ancient stone ruins covered in moss. There's an air of mystery here.",
        exits=[
            Exit(keyword="north", target_room_id="room_2", movement_phrase="go north"),
            Exit(keyword="west", target_room_id="room_3", movement_phrase="go west"),
        ],
    )

    # Add rooms to world
    world.rooms = {
        "room_1": room_1,
        "room_2": room_2,
        "room_3": room_3,
        "room_4": room_4,
    }

    return world


# Create global instance for development
seed_world = create_seed_world()
