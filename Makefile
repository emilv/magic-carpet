.PHONY: weather_icons

weathericons:
	mkdir weathericons/
	cd weathericons; \
	curl -X GET --header 'Accept: application/x-download' \
	-o icons.tar.gz \
	'https://api.met.no/weatherapi/weathericon/2.0/data'; \
	tar -zxvf icons.tar.gz; \
	rm icons.tar.gz
