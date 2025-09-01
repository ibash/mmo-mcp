# Release Checklist for MMO MCP

## Critical -- fix before launch

1. Missing "say" command
  - Prompts promise chat but it's completely unimplemented
  - Players literally can't communicate - breaks core multiplayer
  - FIX: Implement basic say tool that broadcasts to room

2. Ghost players accumulate forever
  - No activity tracking or cleanup
  - Rooms fill with disconnected players, making game feel dead  
  - FIX: Add last_action_at timestamp, filter inactive players

3. Claude Desktop connection setup
  - No clear way for players to connect via Claude Desktop
  - Players can't actually join the game
  - FIX: Create clear connection instructions for hosted server URL

4. Test in Cursor
  - Many players will try connecting via Cursor
  - Need to ensure MCP server works with Cursor's implementation
  - FIX: Test connection and gameplay in Cursor, document any differences

## High priority -- should fix for good experience

5. Authentication/Security
  - Anyone can connect as any player_id with no password
  - Account hijacking, impersonation possible
  - FIX: Add basic password/token authentication

6. Generic character creation
  - Prompts encourage cliché fantasy names like "Zephyr" or "Whisper"
  - Boring, repetitive character pool
  - FIX: Update prompts to encourage diverse, creative characters

7. Only 4 rooms
  - Content exhausted in minutes, overcrowding in spawn room
  - No exploration, everyone bunched together
  - FIX: Add more rooms (10-20 minimum), distribute spawn points

8. No push notifications
  - HTTP transport means no real-time updates
  - Miss all events happening around you
  - FIX: Document this limitation, consider workarounds

## Manageable -- can handle manually

9. Unbounded API costs
  - Every do action calls Claude API with no rate limiting
  - SOLUTION: Using Anthropic's budget limits to cap costs

10. Griefing vulnerabilities
  - No limits on destructive actions (spam items, deface rooms)
  - SOLUTION: Will manually reset world state if griefing occurs

## Post-launch improvements

11. Missing moderation tools
  - No admin commands, rollback, or ban/kick functionality

12. No character progression
  - Everyone functionally identical
  - No skills, stats, or advancement

13. Session management issues
  - Every request re-authenticates
  - No proper session handling

14. Effect spam
  - Room and player effects arrays grow infinitely
  - No cleanup mechanism

15. Fantasy bias in prompts
  - Prompts heavily push medieval/fantasy themes
  - Should allow modern, sci-fi, surreal elements

## Release priority order

Absolute Minimum:
1. Create connection instructions for hosted server
2. Test in Cursor
3. Implement say command 
4. Add last_action_at tracking

High Priority:
5. Basic authentication
6. Update character creation prompts
7. Expand to 10+ rooms
8. Spawn distribution

Medium Priority:
9. Rate limiting (managed via Anthropic budget)
10. Effect limits (can manually reset)
11. Item limits (can clean up manually)

Post-Launch:
12. Activity indicators
13. Admin tools
14. Character progression
15. Push notifications

## Notes

- Since you're hosting the server, players just need the connection URL
- Focus on preventing abuse/griefing since it's a public server
- Communication (say command) is absolutely critical for multiplayer
- Rate limiting managed via Anthropic budget limits
- Can manually reset world if griefing occurs