#!/usr/bin/env python3
"""
Pokemon MCP Server - Entry Point
A Model Context Protocol server for Pokemon information queries using FastMCP.
"""

import asyncio
import argparse
import logging
import sys
from pokemon_mcp import mcp

def setup_logging(level: str = "INFO") -> None:
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stderr)
        ]
    )

def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Pokemon MCP Server - A Model Context Protocol server for Pokemon information queries",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Start server with default settings
  %(prog)s --log-level DEBUG  # Enable debug logging
  %(prog)s --help             # Show this help message
        """
    )

    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Set the logging level (default: INFO)"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )

    return parser

def main() -> None:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    # Setup logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)

    # Print startup banner
    logger.info("=" * 60)
    logger.info("🎮 Pokemon MCP Server v1.0.0")
    logger.info("=" * 60)
    logger.info("🔗 PokéAPI Integration: https://pokeapi.co")
    logger.info("📋 Available Tools:")
    logger.info("   • get_pokemon_info - Get detailed Pokemon information")
    logger.info("   • get_pokemon_species - Get Pokemon species data")
    logger.info("   • get_pokemon_types - List all Pokemon types")
    logger.info("   • get_pokemon_by_type - Get Pokemon by type")
    logger.info("   • search_pokemon - Search Pokemon by name")
    logger.info("   • get_pokemon_evolution_chain - Get evolution chains")
    logger.info("=" * 60)

    # Run the server
    try:
        logger.info("🚀 Starting Pokemon MCP Server...")
        logger.info("📡 Connecting to PokéAPI...")
        logger.info("🎮 MCP Server ready to accept Pokemon queries!")

        # Run the FastMCP server
        mcp.run(transport='stdio')

    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()