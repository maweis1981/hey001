import math
import urllib
import simplejson as json

nauticalMilePerLat = 60.00721
nauticalMilePerLongitude = 60.10793
rad = math.pi / 180.0
milesPerNauticalMile = 1.15078
kilometersPerMiles = 1.60931

def calcDistance(lat1, lon1, lat2, lon2):                      
    """
    Caclulate distance between two lat lons in NM
    """
    yDistance = (lat2 - lat1) * nauticalMilePerLat
    xDistance = (math.cos(lat1 * rad) + math.cos(lat2 * rad)) * (lon2 - lon1) * (nauticalMilePerLongitude / 2)

    distance = math.sqrt( yDistance**2 + xDistance**2 )

    return distance * milesPerNauticalMile * kilometersPerMiles
    
    
def getAround(lat,lon,radius):
    #exchange NM
    radius = (radius/1000)/kilometersPerMiles/milesPerNauticalMile
    print radius
    dpmLat = 1 / nauticalMilePerLat
    radiusLat = dpmLat * radius
    minLat = lat - radiusLat
    maxLat = lat + radiusLat
    
    mpdLng = nauticalMilePerLongitude*math.cos(lat * rad)
    dpmLng = 1 / mpdLng
    radiusLng = dpmLng*radius
    minLng = lon - radiusLng
    maxLng = lon + radiusLng
    return [minLat,maxLng,maxLat,maxLng]

def getAddress(lat,lon,language):
    url = 'http://maps.google.com/maps/api/geocode/json?latlng=%s,%s&sensor=false&language=language' % (lat,lon)
    u = urllib.urlopen(url)
    content = u.read()
    u.close()
    contentObj = json.loads(unicode(content,"UTF-8"))
    return contentObj['results'][0]['formatted_address']

if __name__ == "__main__":
    print calcDistance(32.071774,118.762203,32.146527,118.696345)
    print calcDistance(    32.05915477806914,118.7838363647461,    32.074429228945505,118.76598358154297)
    print calcDistance(32.062788760277918,118.7728065090474,32.071774,118.762203)
    print calcDistance(32.062788760277918, 118.7728065090474,32.080759239722077, 118.7728065090474)
    print getAround(32.071774,118.762203,1000)
    print getAddress(32.14138846520449,118.70135307312012)
