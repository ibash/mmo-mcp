from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.server.dependencies import get_http_request


# AuthMiddleware that extracts the player_id from the connection url and sets it
# in context.
class AuthMiddleware(Middleware):
    # TODO(ibash) does this need to be on_message instead?
    async def on_request(self, context: MiddlewareContext, call_next):
        assert context.fastmcp_context

        request = get_http_request()
        # TODO(ibash) player_id === user_id
        player_id = request.query_params["player_id"]
        context.fastmcp_context.set_state("player_id", player_id)

        autonomous = request.query_params.get("autonomous")
        is_autonomous = bool(
            autonomous and autonomous.lower() != "false" and autonomous.lower() != "0"
        )
        context.fastmcp_context.set_state("autonomous", is_autonomous)

        result = await call_next(context)

        return result
