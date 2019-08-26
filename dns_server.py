import dns.resolver
import dns.tsigkeyring
import dns.update
import dns.query
import dns.update
import dns.zone

import logging

#pip install dnspython

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

class mydns_api:
    def __init__(self,env):
        if env == 'test':
            self.keyring = dns.tsigkeyring.from_text({
                'local-ddns': 'wkK5hnt8mlUdalIV+Uf/oaUIoYOl4vwYL+7kynmWcG8='
            })
            self.name_server_addr = '10.101.6.11'
        elif env == 'prod':
            self.keyring = dns.tsigkeyring.from_text({
                'local-ddns': 'ASeOyC3PrK2N60JDXAKvwMRIGnchGrvsC4m9cferyIs='
            })
            self.name_server_addr = '10.12.43.11'
        elif env == 'temp':
            self.keyring = dns.tsigkeyring.from_text({
                'local-ddns': 'ASeOyC3PrK2N60JDXAKvwMRIGnchGrvsC4m9cferyIs='
            })
            self.name_server_addr = '192.168.235.128'
        else:
            self.name_server_addr = ''
        self.sha_type = 'hmac-sha256'
        self.name_server_port = 53

    def zone_list(self,zone_name):
        domain_list=[]
        z = dns.zone.from_xfr(dns.query.xfr(self.name_server_addr, zone_name))
        names = z.nodes.keys()
        for n in names:
            record = z[n].to_text(n)
            record=record.split(' ')
            if len(record) == 5:
               domain_list.append(record)
        return domain_list

    def search_record(self,search_record,record_type):
        dns_query = dns.message.make_query(search_record, record_type)
        response = dns.query.udp(dns_query, self.name_server_addr, port=self.name_server_port)
        if response.answer:
           for i in response.answer:
               #print(i)
               return True
        else:
               return False

    def add_record(self,domain_zone,domain_name,ttl,record_type,record_value):
        if self.search_record(domain_name+'.'+domain_zone,record_type):
            return {'code':'1','message':'record aleady exit'}
        else:
            update = dns.update.Update(domain_zone, keyring=self.keyring, keyalgorithm=self.sha_type)
            update.add(domain_name, ttl, record_type, record_value)
            dns.query.tcp(update, self.name_server_addr)
            return {'code': 0,'message':'ok'}

    def edit_record(self,domain_zone,domain_name,ttl,record_type,record_value):
        update = dns.update.Update(domain_zone, keyring=self.keyring, keyalgorithm=self.sha_type)
        update.replace(domain_name, ttl, record_type, record_value)
        dns.query.tcp(update, self.name_server_addr)
        if self.search_record(domain_name + '.' + domain_zone, record_type):
            return {'code': 0, 'message': 'ok'}
        else:
            return {'code': '2', 'message': 'not edit'}

    def del_record(self,domain_zone,domain_name,record_type):
        update = dns.update.Update(domain_zone, keyring=self.keyring, keyalgorithm=self.sha_type)
        update.delete(domain_name)
        dns.query.tcp(update, self.name_server_addr)
        if self.search_record(domain_name + '.' + domain_zone, record_type):
            return {'code': 3, 'message': 'not delete sucess'}
        else:
            return {'code': '0', 'message': 'ok'}

    def __del__(self):
        pass



if __name__ == '__main__':
    pass