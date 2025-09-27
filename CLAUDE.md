# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Pokemon MCP (Model Context Protocol) server project that provides Pokemon-related knowledge to large language models via the PokéAPI. The project queries Pokemon information through HTTP connections to the PokéAPI and is implemented in Python.

## Development Environment

### Requirements
- Python 3.8+
- Node.js (for some LLM hosts that require it)
- httpx
- mcp[cli]

### Quick Start

#### Using uv (preferred)
```bash
uv init
uv venv
source .venv/bin/activate
```

#### Using Claude Code
```bash
/init
```

## Project Structure

- `main.py` - Entry point that starts the MCP server
- `pokemon_mcp.py` - MCP server implementation with Pokemon tools
- `pyproject.toml` - Python project configuration with dependencies
- `requirements.txt` - Project dependencies
- `.python-version` - Specifies Python version for the project
- `.venv/` - Virtual environment directory

## MCP Server Tools

The server provides the following MCP tools:

1. **get_pokemon_info** - Get detailed Pokemon information by name or ID
   - Input: identifier (string) - Pokemon name or ID
   - Output: Formatted Pokemon data including stats, types, abilities, sprites

2. **get_pokemon_species** - Get species information including evolution details
   - Input: identifier (string) - Pokemon name or ID
   - Output: Species data, flavor text, evolution chain information

3. **get_pokemon_types** - Get all available Pokemon types
   - Input: None
   - Output: List of all Pokemon types

4. **get_pokemon_by_type** - Get all Pokemon of a specific type
   - Input: type_name (string) - Pokemon type name
   - Output: List of Pokemon belonging to the specified type

5. **search_pokemon** - Search for Pokemon by name
   - Input: query (string), limit (integer, default: 10)
   - Output: List of Pokemon matching the search query

6. **get_pokemon_evolution_chain** - Get evolution chain by chain ID
   - Input: chain_id (integer)
   - Output: Formatted evolution chain showing evolutionary stages

## Key Features

- **API Integration**: Seamless integration with PokéAPI (https://pokeapi.co/api/v2)
- **Rich Data Retrieval**: Access to Pokemon stats, types, abilities, evolution chains, species info
- **Formatted Output**: Clean, readable text output
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Async Implementation**: Fully async/await implementation for better performance
- **Clean Architecture**: Separated concerns between API client and MCP server logic

## Project Information

- **Project Name**: "pokemon_mcp" (underscore format)
- **Language**: Chinese project description and documentation
- **Purpose**: Feed LLMs with Pokémon information and knowledge via MCP server

# 要求
每次推理请输出自己的思考，并用中文输出

## MCP Server 构建经验总结

### 1. 项目架构设计
- **分离关注点**: 将API客户端逻辑与MCP服务器逻辑分离，采用专门的Client类来处理所有HTTP请求
- **模块化设计**: 将主要业务逻辑放在独立的功能模块中，入口点单独放在main.py中
- **清晰的文件结构**: 简单明了的项目结构，易于维护和扩展

### 2. 技术选型
- **框架选择**: 使用FastMCP作为MCP服务器框架，提供了简洁的装饰器语法
- **HTTP客户端**: 使用httpx作为异步HTTP客户端，支持async/await，性能更好
- **依赖管理**: 使用pyproject.toml进行现代化的Python项目管理

### 3. 核心组件构建
- **API客户端类**: 封装所有外部API调用，提供统一的错误处理
- **工具装饰器**: 使用`@mcp.tool()`装饰器将函数暴露为MCP工具
- **数据格式化**: 提供专门的格式化方法，确保输出格式一致
- **异步支持**: 全面采用async/await模式，提高并发性能

### 4. 错误处理策略
- **分层错误处理**: 在API客户端层捕获HTTP错误，在工具层处理业务逻辑错误
- **用户友好错误信息**: 将技术性错误转换为用户友好的错误消息
- **异常传播**: 合理的异常传播机制，确保错误能够被正确处理

### 5. 开发最佳实践
- **命令行接口**: 提供完整的命令行参数支持，包括日志级别控制
- **日志记录**: 完善的日志系统，支持不同级别的日志输出
- **文档字符串**: 为每个工具提供详细的文档字符串，包括参数和返回值说明
- **启动横幅**: 友好的启动信息，展示可用工具和系统状态

### 6. 部署和运行
- **虚拟环境**: 使用Python虚拟环境管理依赖
- **依赖安装**: 明确的依赖声明，支持开发和生产环境
- **运行方式**: 通过`mcp.run(transport='stdio')`启动服务器

### 7. 构建步骤总结
1. **环境准备**: 创建Python虚拟环境，安装必要依赖
2. **项目结构**: 创建清晰的目录结构和文件组织
3. **API客户端**: 实现专门的API客户端类，处理所有外部API调用
4. **MCP服务器**: 使用FastMCP创建服务器实例，注册工具函数
5. **工具开发**: 使用装饰器注册各个工具函数，实现具体业务逻辑
6. **错误处理**: 在各层实现适当的错误处理机制
7. **启动入口**: 创建main.py作为服务器启动入口，支持命令行参数
8. **测试验证**: 对各工具进行功能测试，确保正常运行

这个构建模式可以作为其他MCP server项目的参考模板，只需要替换API客户端和工具函数的具体实现即可。