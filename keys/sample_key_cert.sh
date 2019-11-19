#!/bin/bash
openssl req -new -x509 -nodes -newkey ec:<(openssl ecparam -name secp384r1) -keyout sample_key.pem -out sample_cert.pem -days 3650