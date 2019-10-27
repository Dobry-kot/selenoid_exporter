## Installation

1) Add the variables "url" and "type":
    ```bash
    url     - url to the selenoid node or router.
    example: export url=https://example.com:8080/status

    type    - "node" or "router" for the labels metrics.
    example: selenoid_{type}_browser_running ---> | selenoid_node_browser_running | selenoid_router_browser_running
    ```
    
    or change the variables in the docker-compose file to static.

2) Start docker-compose.
    ```bash
    docker-compose up -d
    ```
    