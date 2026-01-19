# Network Simulation Guide

To test the IPv6 Manager without physical Raspberry Pis, this project uses Docker to simulate network nodes.

## Architecture

The simulation consists of a dedicated virtual IPv6 bridge network and multiple Linux containers running an SSH server to act as managed nodes.

## Setup Instructions

1. Build the Node Image: The image is based on Alpine Linux and includes SSH and networking tools.
    "docker build -t my-ipv6-node ."
2. Create the IPv6 Network: A custom bridge network is required to assign specific IPv6 addresses.
    "docker network create --ipv6 --subnet=2001:db8:1::/64 lab_network"
3. Deploy Nodes: Run multiple containers with assigned static IPv6 addresses:
    "docker run -d --name node1 --network lab_network --ip6 2001:db8:1::10 my-ipv6-node"
    "docker run -d --name node2 --network lab_network --ip6 2001:db8:1::20 my-ipv6-node"
    ...

## Verification

To verify that the internal IPv6 routing is functional, run a ping between two containers:
    "docker exec -it node1 ping 2001:db8:1::20"