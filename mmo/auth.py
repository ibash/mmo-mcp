from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.server.dependencies import get_http_request
from mmo.player import Player
from mmo.errors import GameError
from mmo.game_world import world


# AuthMiddleware that extracts authentication from URL query parameters
class AuthMiddleware(Middleware):
    async def on_get_prompt(self, context: MiddlewareContext, call_next):
        self._authenticate(context)
        return await call_next(context)

    async def on_call_tool(self, context: MiddlewareContext, call_next):
        self._authenticate(context)
        return await call_next(context)

    def _authenticate(self, context: MiddlewareContext):
        assert context.fastmcp_context

        request = get_http_request()

        # Extract player_id from query params
        player_id = request.query_params.get("player_id")
        if not player_id:
            raise GameError(
                "Authentication required. Connect with: http://localhost:8000/mcp?player_id=username&password=yourpassword"
            )

        # Validate and normalize player_id
        try:
            player_id = Player.validate_id(player_id)
        except GameError as e:
            raise GameError(f"Invalid player_id: {e}")

        # Extract password from query params
        password = request.query_params.get("password")
        if not password:
            raise GameError(
                "Password is required. Add &password=yourpassword to the URL"
            )

        # If player exists, verify password immediately
        if world.player_exists(player_id):
            player = world.players[player_id]
            if not player.check_password(password):
                raise GameError(f"Invalid password for player_id={player_id}")

        # Store only player_id in context
        context.fastmcp_context.set_state("player_id", player_id)

        # Check for autonomous flag in query params
        autonomous = request.query_params.get("autonomous")
        is_autonomous = bool(
            autonomous and autonomous.lower() != "false" and autonomous.lower() != "0"
        )
        context.fastmcp_context.set_state("autonomous", is_autonomous)
