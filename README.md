# dico-A6-02

## Overview
This project is a distributed system developed as part of my Computer Science Bachelor's degree (Year 2). It allows remote dictionary management through a multi-tier Client-Server architecture using TCP Sockets. The system handles hierarchical communication between standard clients, local servers, and a Master server.

## Key Features
__Custom Application Protocol__: Defined a robust protocol for data exchange (GET, SET, DEL, PREF) with full technical specifications in protocol_dico.md.

__Hierarchical Architecture__: Implemented a Master/Slave logic where local servers query a Master server for missing keys.

__Security & SSL/TLS__: Secured administrative operations with certificate-based authentication (SSL/TLS) to ensure data integrity and encrypted communication.

__Concurrency Management__: Handled multiple simultaneous connections and concurrent access for write operations (set, del).

__Data Persistence__: Managed dictionary storage and transmission using JSON serialization.

## Technical Stack
Language: Python 3 

Networking: TCP Sockets 

Security: SSL/TLS (OpenSSL certificates) 

Serialization: JSON 

Testing: Automated command testing with a Python file 

Version Control: GitLab 

## Project Structure
```protocol_dico.md```: Detailed technical specifications of the communication protocol.

```protocol_dico.py```: Core library containing shared logic and command implementations (get, set, del, pref). This module ensures consistency across clients and servers by providing unified data processing functions.

```dico_server_maitre.py```: Centralized Master server managing the authoritative dictionary.

```dico_server.py```: Local server-side logic managing data caching and master communication.

```dico_admin.py```: Administrative client for authenticated and secured operations.

```dico_client.py```: Standard client for remote dictionary consultation.

```certif/```: Contains SSL/TLS certificates and keys for secure communication.

```tests/```: Automated test suite for command validation and system robustness.

## Authors 
BERNADET Laurent
WAKLATSI Elly