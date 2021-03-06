import requests
import json
import random
#from place import Place

class Place:
    name= None
    lat = None
    lng = None
    rating = None
    type_of = None
    city = None
    score= None
    photo= None
    place_id = None

    def __init__(self, name, lat, lng, rating, type_of, city, place_id, photo = None):
        self.name= name
        self.lat = lat
        self.lng = lng
        self.rating= rating
        self.type_of= type_of
        self.city= city
        self.place_id = place_id
        self.photo = photo

    def set_score(self, score):
        self.score= score



DONT_INCLUDE= ['travel_agency','shop','shopping_mall','store','market','business','store','complex', 'finance', 'bank', 'park', 'real_estate']
# Google Places API
# Google Geocoding API

new_api = 'https://maps.googleapis.com/maps/api/geocode/json?'
# api_key = 'AIzaSyAD0tsB11_bi7ofAvU-M2S459wmPRkOlYY'	#ANIQ
# api_key = 'AIzaSyCOIE234Jzwqm1a6B-v3pNvdDNaiTyDR1U'	#MODI
# api_key = 'AIzaSyAqwxsqZQbDezGD_V-egxM4kxzm-0bpQ_8'	#DEEKSHA
api_key = 'AIzaSyDZFiMsWnSDFC5b0Vaqu1UY0rfSMYcNtnY'	#PAUL

def get_places(CITY_NAME):
	# INIT  only
	place_request= 'address={}&key={}'.format(CITY_NAME, api_key)

	request = new_api + place_request
	r = requests.get(request)
	print(r)
	f= open('input.json','w+')
	f.write(r.text)
	f.close()

	#using search place api

	with open('input.json','r') as myfile:
		content=json.load(myfile)
	newcontent=content['results'][0]
	more=newcontent['geometry']
	late=more['location']
	latitude = late['lat']
	longitute = late['lng']
	place_id= newcontent["place_id"]


	#api for getting places to visit nearby

	near_by='https://maps.googleapis.com/maps/api/place/nearbysearch/json?'

	category= {}
	category['famous places']='famous'
	category['premise']='monument'
	category['monument']='monument'
	category['places_of_worship']='places_of_worship'
	category['temple']='places_of_worship'
	category['shrine']='places_of_worship'
	category['zoo']='zoo'

	places=['temple','famous places','monument','premise','shrine','zoo']

	for i in range(len(places)):
		#print(places[i])
		nearby_ask = 'key={}&location={},{}&radius={}&keyword={}'.format(api_key,latitude,longitute,'10000',places[i])
		#print(nearby_ask)
		request_4 = near_by + nearby_ask
		#print(request_4)
		r_4=requests.get(request_4)
		f=open('near_places'+str(i)+'.json','w+')
		f.write(r_4.text.encode('ascii', 'ignore').decode('ascii'))
		f.close()



	list_of_places=[]
	for i in range(len(places)):
		with open('near_places'+str(i)+'.json', 'r') as data_file:
			data= json.load(data_file)

		l= len(data['results'])
		for k in range(l):
			place_id = data['results'][k]['place_id']
			name = data['results'][k]['name']
			lat = data['results'][k]['geometry']['location']['lat']
			lng = data['results'][k]['geometry']['location']['lng']
			try:
				rating = data['results'][k]['rating']
			except:
				rating = 1
			type_of_original = data['results'][k]['types']
			type_of = category[places[i]]
			# Creating a Place object and storing it in a list
			flag = True
			if 'establishment' in type_of_original:
				type_of_original.remove('establishment')
			if 'point_of_interest' in type_of_original:
				type_of_original.remove('point_of_interest')

			if len(type_of_original)>0:
				for type_word in type_of_original:
					if type_word in DONT_INCLUDE:
						flag = False
				if flag:
					list_of_places.append(Place(name, lat, lng, rating, type_of, CITY_NAME, place_id))

	print(len(list_of_places))

	no_dupli=[]
	for i in range(len(list_of_places)):
		flag = True
		for j in range(i):
			if list_of_places[i].place_id == list_of_places[j].place_id:
				flag = False
		if flag:
			no_dupli.append(list_of_places[i])

	return no_dupli


def find_distance(name_from, name_to):
	path='https://maps.googleapis.com/maps/api/directions/json?'

	path_var='origin={}&destination={}&key={}&units={}'.format(name_from,name_to,api_key,'metric')

	request_3 = path + path_var
	r_3=requests.get(request_3)
	print(r_3)
	f=open('places.json','w+')
	f.write(r_3.text.encode('ascii', 'ignore').decode('ascii'))
	f.close()

	with open('places.json','r') as myfile:
		content=json.load(myfile)
        if len(content['routes'])==0:
			return random.randint(2000,10000)
	dis_1=content['routes'][0]
	dis_2=dis_1['legs'][0]
	dis_3=dis_2['distance']['text']

	x= dis_3.split()
	if x[1] == 'km':
		return float(x[0])*1000.0
	else:
		return float(x[0])
