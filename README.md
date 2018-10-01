# ObjectRocket Dev Test

[Problem description](https://gist.github.com/keithhigbee/0473b604b067a0b945ceea845dde419e)

## Running the solution

### 1. Clone the repo
```sh
git clone https://github.com/felixtan/objectrocket-dev-test.git farmers-market
```
### 2. Build the docker image
```sh
cd farmers-market
docker build -t checkout .
```
### 3. Run the container
```sh
docker run -it --rm checkout
```
### 4. Enter input
```sh
# space or comma-separated
# ex.
> Basket: AP1, AP1, CH1, AP1
> Total: $16.61
```