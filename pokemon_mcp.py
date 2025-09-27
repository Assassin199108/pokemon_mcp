import httpx
from typing import Dict, List, Any, Optional
from fastmcp import FastMCP

# Create FastMCP instance
mcp = FastMCP("Pokemon MCP Server")

# Pokemon client for API interactions
class PokemonClient:
    """Client for interacting with the PokéAPI."""

    def __init__(self, base_url: str = "https://pokeapi.co/api/v2"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

    async def get_pokemon(self, identifier: str) -> Dict[str, Any]:
        """Get Pokemon information by name or ID."""
        try:
            response = await self.client.get(f"{self.base_url}/pokemon/{identifier.lower()}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise Exception(f"Failed to fetch Pokemon {identifier}: {str(e)}")

    async def get_pokemon_species(self, identifier: str) -> Dict[str, Any]:
        """Get Pokemon species information by name or ID."""
        try:
            response = await self.client.get(f"{self.base_url}/pokemon-species/{identifier.lower()}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise Exception(f"Failed to fetch Pokemon species {identifier}: {str(e)}")

    async def get_pokemon_types(self) -> Dict[str, Any]:
        """Get all Pokemon types."""
        try:
            response = await self.client.get(f"{self.base_url}/type")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise Exception(f"Failed to fetch Pokemon types: {str(e)}")

    async def get_pokemon_by_type(self, type_name: str) -> Dict[str, Any]:
        """Get Pokemon by type."""
        try:
            response = await self.client.get(f"{self.base_url}/type/{type_name.lower()}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise Exception(f"Failed to fetch Pokemon by type {type_name}: {str(e)}")

    async def get_pokemon_evolution_chain(self, chain_id: int) -> Dict[str, Any]:
        """Get Pokemon evolution chain by ID."""
        try:
            response = await self.client.get(f"{self.base_url}/evolution-chain/{chain_id}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise Exception(f"Failed to fetch evolution chain {chain_id}: {str(e)}")

    async def search_pokemon(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for Pokemon by name."""
        try:
            response = await self.client.get(f"{self.base_url}/pokemon?limit={limit}")
            response.raise_for_status()
            data = response.json()

            # Filter results based on query
            results = []
            for pokemon in data.get('results', []):
                if query.lower() in pokemon['name'].lower():
                    results.append(pokemon)

            return results[:limit]
        except httpx.HTTPError as e:
            raise Exception(f"Failed to search Pokemon: {str(e)}")

    def format_pokemon_info(self, pokemon_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format Pokemon information for display."""
        return {
            "id": pokemon_data.get("id"),
            "name": pokemon_data.get("name").capitalize(),
            "height": pokemon_data.get("height"),
            "weight": pokemon_data.get("weight"),
            "base_experience": pokemon_data.get("base_experience"),
            "types": [t["type"]["name"].capitalize() for t in pokemon_data.get("types", [])],
            "abilities": [a["ability"]["name"].capitalize() for a in pokemon_data.get("abilities", [])],
            "stats": {
                stat["stat"]["name"].replace("-", "_"): stat["base_stat"]
                for stat in pokemon_data.get("stats", [])
            },
            "sprites": {
                "front_default": pokemon_data.get("sprites", {}).get("front_default"),
                "back_default": pokemon_data.get("sprites", {}).get("back_default"),
                "front_shiny": pokemon_data.get("sprites", {}).get("front_shiny"),
                "back_shiny": pokemon_data.get("sprites", {}).get("back_shiny")
            }
        }

# Global Pokemon client instance
pokemon_client = PokemonClient()

# Tool 1: Get Pokemon Info
@mcp.tool()
async def get_pokemon_info(identifier: str) -> str:
    """Get detailed Pokemon information by name or ID.

    Args:
        identifier: Pokemon name or ID (e.g., 'pikachu' or 25)

    Returns:
        Formatted Pokemon information including stats, types, abilities, and sprites
    """
    try:
        pokemon_data = await pokemon_client.get_pokemon(identifier)
        formatted_info = pokemon_client.format_pokemon_info(pokemon_data)

        output = f"""🎮 Pokemon Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name: {formatted_info['name']} (#{formatted_info['id']})
Height: {formatted_info['height']/10}m
Weight: {formatted_info['weight']/10}kg
Base Experience: {formatted_info['base_experience']}

Types: {', '.join(formatted_info['types'])}
Abilities: {', '.join(formatted_info['abilities'])}

Stats:
  HP: {formatted_info['stats']['hp']}
  Attack: {formatted_info['stats']['attack']}
  Defense: {formatted_info['stats']['defense']}
  Sp. Attack: {formatted_info['stats']['special_attack']}
  Sp. Defense: {formatted_info['stats']['special_defense']}
  Speed: {formatted_info['stats']['speed']}

Sprites:
  Front: {formatted_info['sprites']['front_default']}
  Back: {formatted_info['sprites']['back_default']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

        return output
    except Exception as e:
        return f"Error: {str(e)}"

# Tool 2: Get Pokemon Species
@mcp.tool()
async def get_pokemon_species(identifier: str) -> str:
    """Get Pokemon species information including evolution details.

    Args:
        identifier: Pokemon name or ID (e.g., 'pikachu' or 25)

    Returns:
        Species data, flavor text, and evolution chain information
    """
    try:
        species_data = await pokemon_client.get_pokemon_species(identifier)

        # Get flavor text in English
        flavor_text = ""
        for entry in species_data.get('flavor_text_entries', []):
            if entry.get('language', {}).get('name') == 'en':
                flavor_text = entry.get('flavor_text', '').replace('\n', ' ').replace('\f', ' ')
                break

        # Get evolution chain URL
        evolution_chain_url = species_data.get('evolution_chain', {}).get('url')
        evolution_info = "No evolution chain available"

        if evolution_chain_url:
            try:
                chain_id = evolution_chain_url.split('/')[-2]
                evolution_data = await pokemon_client.get_pokemon_evolution_chain(int(chain_id))
                evolution_info = f"Evolution Chain ID: {chain_id}"
            except:
                evolution_info = "Evolution chain data unavailable"

        output = f"""🔬 Pokemon Species Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name: {species_data.get('name', '').capitalize()}
Generation: {species_data.get('generation', {}).get('name', 'Unknown')}
Habitat: {species_data.get('habitat', {}).get('name', 'Unknown') if species_data.get('habitat') else 'Unknown'}
Growth Rate: {species_data.get('growth_rate', {}).get('name', 'Unknown')}
Capture Rate: {species_data.get('capture_rate', 'Unknown')}

Flavor Text:
{flavor_text}

Evolution: {evolution_info}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

        return output
    except Exception as e:
        return f"Error: {str(e)}"

# Tool 3: Get Pokemon Types
@mcp.tool()
async def get_pokemon_types() -> str:
    """Get all available Pokemon types.

    Returns:
        List of all Pokemon types available in the PokéAPI
    """
    try:
        types_data = await pokemon_client.get_pokemon_types()
        types = [t['name'].capitalize() for t in types_data.get('results', [])]

        output = f"""🏷️ Available Pokemon Types:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Types: {len(types)}

{', '.join(types)}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

        return output
    except Exception as e:
        return f"Error: {str(e)}"

# Tool 4: Get Pokemon by Type
@mcp.tool()
async def get_pokemon_by_type(type_name: str) -> str:
    """Get all Pokemon of a specific type.

    Args:
        type_name: Pokemon type name (e.g., 'fire', 'water', 'grass')

    Returns:
        List of Pokemon belonging to the specified type
    """
    try:
        type_data = await pokemon_client.get_pokemon_by_type(type_name)
        pokemon_list = [p['pokemon']['name'].capitalize() for p in type_data.get('pokemon', [])]

        output = f"""🔍 Pokemon of Type '{type_name.capitalize()}':
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Pokemon: {len(pokemon_list)}

{', '.join(pokemon_list[:20])}{'...' if len(pokemon_list) > 20 else ''}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

        return output
    except Exception as e:
        return f"Error: {str(e)}"

# Tool 5: Search Pokemon
@mcp.tool()
async def search_pokemon(query: str, limit: int = 10) -> str:
    """Search for Pokemon by name.

    Args:
        query: Search query for Pokemon names
        limit: Maximum number of results to return (default: 10)

    Returns:
        List of Pokemon matching the search query
    """
    try:
        results = await pokemon_client.search_pokemon(query, limit)
        pokemon_names = [p['name'].capitalize() for p in results]

        output = f"""🔎 Search Results for '{query}':
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Found {len(pokemon_names)} Pokemon:

{', '.join(pokemon_names) if pokemon_names else 'No results found'}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

        return output
    except Exception as e:
        return f"Error: {str(e)}"

# Tool 6: Get Pokemon Evolution Chain
@mcp.tool()
async def get_pokemon_evolution_chain(chain_id: int) -> str:
    """Get evolution chain by chain ID.

    Args:
        chain_id: Evolution chain ID

    Returns:
        Formatted evolution chain showing evolutionary stages
    """
    try:
        evolution_data = await pokemon_client.get_pokemon_evolution_chain(chain_id)

        def format_evolution_stage(stage, level=0):
            indent = "  " * level
            species_name = stage.get('species', {}).get('name', 'Unknown').capitalize()
            output = f"{indent}• {species_name}"

            if stage.get('evolves_to'):
                for next_stage in stage['evolves_to']:
                    output += "\n" + format_evolution_stage(next_stage, level + 1)

            return output

        chain_output = format_evolution_stage(evolution_data.get('chain', {}))

        output = f"""🧬 Evolution Chain #{chain_id}:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{chain_output}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

        return output
    except Exception as e:
        return f"Error: {str(e)}"

# Note: FastMCP handles cleanup automatically