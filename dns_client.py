import dns.resolver

SERVER = "192.168.235.128"#your DNS server
PORT = 53#DNS server port
dns_query = dns.message.make_query("chen.test.com", "A")
response = dns.query.udp(dns_query, SERVER, port = PORT)

for i in response.answer:
    print(i)
 #   print(i.to_text())


#resolver = dns.resolver.Resolver(configure=False)
#resolver.nameservers = ['10.101.6.11']
#answer = resolver.query('api.cloud.bz', 'A')
#print('The nameservers are:')
#for rr in answer:
#    print(rr)

#from __future__ import print_function

#import dns.reversename
#n = dns.reversename.from_address("10.101.6.11")
#print(n)
#print(dns.reversename.to_address(n))

import dns.tsigkeyring
import dns.update
import dns.query

#ZONE = "cloud.bz.hosts"

#keyring = dns.tsigkeyring.from_text({'default.any': 'xxxxxxxxxxxxxxx'})
#update_query = dns.update.Update(ZONE, keyring=keyring)
#update_query = dns.update.Update(ZONE)
#for i in range(1,101):
# #update_query.add("testqa" + str(i), 60, "1.1.1.1")
#