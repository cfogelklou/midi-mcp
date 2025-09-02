# Claude Instructions

Please follow the instructions outlined in the `AI-INSTRUCTIONS.md` file for all contributions to this codebase.

## API that AI Agents don't understand

When working on the mcp server, if you create any new hardcoded constants, place them in constants.py. If such constants are necessary inputs for an API function, then ensure you add the function to the "help" command and provide its list of accepted input parameters.

