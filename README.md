# dico-A6-02

# Distributed Client-Server Dictionary System #
## Overview
This project is a distributed system developed as part of my Computer Science Bachelor's degree (Year 2). It allows users to manage a dictionary remotely through a Client-Server architecture using TCP Sockets. The system is designed to handle hierarchical communication between standard clients, local servers, and a Master server.

## Key Features
__Custom Application Protocol__: Defined and implemented a robust protocol for data exchange, including commands like GET, SET, DEL, and PREF (prefix search).

__Hierarchical Architecture__: Implemented a Master/Slave server logic where local servers can query a Master server if a key is not found locally.

__Concurrency & Security__: Developed an Admin Client capable of modifying data with authentication mechanisms and handling concurrent access to the dictionary.

__Data Persistence__: Used JSON serialization to store and transmit dictionary data across the network.

## Technical Stack
Language: Python 3

Networking: TCP Sockets

Serialization: JSON

Version Control: GitLab/GitHub 

## Project Structure
```protocol_dico.md```: Detailed technical specifications of the communication protocol.

```dico_server.py```: Server-side logic managing local data and Master server communication.

```dico_client.py```: Standard client for remote dictionary consultation.

```dico_admin.py```: Administrative client for authenticated write/delete operations.
