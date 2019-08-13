import dns.resolver
import dns.tsigkeyring
import dns.update
import dns.query
import dns.update

#ZONE = "cloud.bz.hosts"
keyring = dns.tsigkeyring.from_text({
    'local-ddns': '0Wplza2EE4l15l+fWGl798ZZ3WIflG3hPKYb/0O7TIo='
})

update = dns.update.Update('test.com', keyring=keyring,keyalgorithm='hmac-sha256')
#update.replace('chen', 300, 'a', '1.1.1.1')
update.add('chen',300,'a','2.2.2.2')
#update.add('abc',60,'2.2.2.2')

response = dns.query.tcp(update, '192.168.235.128')
print(response)