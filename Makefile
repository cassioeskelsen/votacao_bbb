#!make
export host=https://bbbpython.azurewebsites.net
export containter_registry=creskelsen.azurecr.io
export image_name=votacao_bbb
export container_name=votacao_container

acr_login:
	az acr login --name creskelsen

run_local:
	sanic app.main:app --host=0.0.0.0 --port=80 --fast

curl:
	curl -d "param1=xxx" -X POST http:/0.0.0.0/vote

clean_redis:
	redis-cli --scan --pattern votos* |xargs redis-cli del

build:
	DOCKER_BUILDKIT=1 docker image build --tag $(container_registry)/$(image_name)latest -f Dockerfile .

run:
	docker run --name $(container_name) --platform linux/amd64 -p 8000:80  $(container_registry)/$(image_name)latest

push:
	docker push $(container_registry)/$(image_name)latest

stop:
	docker rm --force $(container_name)

run_test:
	 wrk -t290 -c800 -d60s -s post.lua $(host)/vote

bp_locust:
	cd locust &&  docker buildx build --platform linux/amd64 --push --tag $(container_registry)/locust_bbb:latest -f Dockerfile .

run_locust:
	docker run --name locust_bbb -p 8089:8089 creskelsen.azurecr.io/locust_bbb:latest

stop_locust:
	docker rm --force locust_bbb
