# MCP-Server

## About
This repository contains implementations of Model Context Protocol (MCP) server examples for agent-to-agent (A2A) systems. MCP allows AI systems to connect with external tools and data sources.

## Files

### a2a_mcp.py
A web interface that connects to an A2A customer support system. This implementation processes customer support tickets using multiple specialized agents and visualizes the results through a web interface.

### simple_mcp_hello.py (Coming soon)
A minimal example of an MCP server that displays a "Hello World" message using Flask.

## Video Demo
The video demo file (a2a_mcp_sample.mov) is too large to be included in this repository. To view the demo, please download it from [this Google Drive link](https://drive.google.com/file/d/1iWQTcxCYvNFOvxIe6H4clE7e2IFOwZpS/view?usp=sharing).

## How to Run

### Simple MCP Hello World
```bash
python3 simple_mcp_hello.py
```
Then open http://127.0.0.1:5001 in your browser.

### A2A MCP Interface
```bash
python3 a2a_mcp.py
```
Then open http://127.0.0.1:5000 in your browser.