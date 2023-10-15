content = '''Geolife trajectory
WGS 84
Altitude is in Feet
Reserved 3
0,2,255,My Track,0,0,2,8421376
0
$GPGLL,39.9969565304313,N,6.325752588842,E,232153,A,*hh
$GPGLL 39.9968456435550 N 116.325752307088 E 232158 A *hh
$GPGLL;39.9944232779075;N;116.326964907300;E;232203;A;*hh
'''
import re
p = re.compile(r'(\$GPGLL)[,; ](\d+\.*\d*)[,; ]([N,S])[,; ](\d+\.*\d*)[,; ]'
               r'([E,W])[,; ](\d{6})[,; ]([A,V])[,; ](\*hh)', re.MULTILINE)
for gps_data in  p.findall(content):
    print(gps_data)


