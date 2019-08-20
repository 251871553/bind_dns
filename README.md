# bind_dns
zone "test.com" IN {
        type master;
        file "test.com";
        #allow-update { none; };
        allow-update { key local-ddns; };
};
[root@my named]# cat /run/named/session.key 
key "local-ddns" {
	algorithm hmac-sha256;
	secret "ASeOyC3PrK2N60JDXAKvwMRIGnchGrvsC4m9cferyIs=";
};
[root@my named]#
