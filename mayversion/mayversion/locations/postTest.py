import urllib
params = urllib.urlencode({'username': 'maven', 'latitude': +32.145219, 'longitude': +118.698866})
f = urllib.urlopen("http://61.155.8.73:7777/locations/submitLocation/", params)
print 'post .....'
print f.read()