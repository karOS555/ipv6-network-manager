# Network Documentation

## Topology
The network is designed as a hybrid IPv6 environment containing physical and simulated nodes.

* **Management Node (Laptop):** `2001:db8:1::100` (Host)
* **Router (Raspberry Pi):** `2001:db8:1::1` (Provides SLAAC via radvd)
* **Simulated Clients (Docker):** `2001:db8:1::10` - `::20` (Dynamic)

## Addressing Scheme
I'm using the documentation prefix `2001:db8:1::/64`.
* **Subnet:** `2001:db8:1::/64`
* **Multicast Scope:** `ff02::1` (Link-Local All Nodes)

## Routing
The Raspberry Pi acts as the logical gateway. Even though the internet connection is provided via a external network (IPv4/IPv6 dual stack), the internal project network relies on the Pi for Neighbor Discovery (NDP) and Router Advertisements (RA).