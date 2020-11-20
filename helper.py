'''
	Purpose: Download and generate player data(.csv) 
'''
from urllib.parse import quote
import requests
import json
from functools import reduce
from os import path

#Tactics.tools api
DATASRC = "https://legendsapi.com/api/tft/player/na1/"
# Probly should check with check with id not name later
GALAXY_NAMES = {
	'TFT3_GameVariation_FreeSpatula': "Manatee's Delight",
	'TFT3_GameVariation_None': "Normal",
	'TFT3_GameVariation_MidGameFoN': "SuperDense",
	'TFT3_GameVariation_Bonanza': "Treasure Trove",
	'TFT3_GameVariation_ItemsBreak': "Salvage World",
	'TFT3_GameVariation_StartingItems':"Galactic Armory",
	'TFT3_GameVariation_FreeRerolls':"Trade Sector",
	'TFT3_GameVariation_SmallerBoards':"Little Legend",
	'TFT3_GameVariation_TwoItemMax':"Binary Star",
	'TFT3_GameVariation_Dreadnova':"Plunder Planet",
	'TFT3_GameVariation_TwoStarCarousels':"Star Cluster",
	'TFT3_GameVariation_FreeNeekos':"The Neekoverse",
	'TFT3_GameVariation_FourCostFirstCarousel':"Lilac Nebula",
	'TFT3_GameVariation_BigLittleLegends':'Medium Legends',
	'TFT3_GameVariation_LittlerLegends':'Little Legends'
}
def set3_traits_struct():
	return {'Blaster':'None', 'Rebel':'None', 'ManaReaver':'None', 'Demolitionist':'None', 'Cybernetic':'None', 'Infiltrator':'None', 'StarGuardian':'None', 'Paragon':'None', 'Sniper':'None', 'Set3_Celestial':'None', 'MechPilot':'None', 'Set3_Sorcerer':'None', 'Astro':'None', 'Chrono':'None', 'Battlecast':'None', 'Set3_Brawler':'None', 'SpacePirate':'None', 'DarkStar':'None', 'Vanguard':'None', 'Starship':'None', 'Mercenary':'None', 'Protector':'None', 'Set3_Mystic':'None', 'Set3_Blademaster':'None'}
'''
	getData retrieves the player past matches data and return it as a list
'''
def get_data (playerName, useStored=False):
	p = path.join(path.realpath(__file__), '..', 'data','matchhistory', playerName + '.json')
	if (useStored and (path.lexists(p))):
		f = open (p,'r')
		d = json.load(f)
		f.close()
		return d
	url = DATASRC + quote(playerName)
	data = requests.get(url)
	if (not(data)):
		raise Exception('Request data failed')
	f = open (p, 'w')
	json.dump(data.json(),f)
	f.close()
	return data.json()
'''
	get_history will return the player's match data
'''
def get_history(data,playerName):
	# Single out only the given player's history
	gamedata = list(map(lambda x : list(filter(lambda y: y['name'] == playerName, x['info']['participants'])) ,data['matches']))
	galaxydata = list(map(lambda x : x['info']['gameVariation'] ,data['matches']))
	t = map(lambda x: (gamedata[x],galaxydata[x]), range(len(gamedata)))
	return list(t)
def normalize_traits (data):
	traits = set3_traits_struct()
	for trait in data['traits']:
		try:
			#if str(trait['currentTier']) == str(0):
				#continue
			traits[trait['name']] = "Tier " + str(trait['currentTier'])
		except:
			continue
	return list(traits.values())
def normalize_data (data, galaxy):
	data = data.pop()
	# ts = [d['currentTier'] for d in data['traits']]
	ts = normalize_traits(data)
	ddtp = data['totalDamageToPlayers']
	real_galaxy = ""
	try: 
		real_galaxy = GALAXY_NAMES[galaxy]
	except:
		real_galaxy = galaxy
	return [real_galaxy] + ts + [ddtp, data['placement'] <= 4, data['placement'] == 1, data['placement']]
def run (playerName):
	try :
		data = get_data(playerName, useStored=True)
	except:
		return []
	history = get_history(data, playerName)
	dp =  (list(map(lambda x : [playerName] + normalize_data(*x), history))) 
	return dp
def generate_csv(result):
	attr = "Player Name,Galaxy,Blaster,Rebel,ManaReaver,Demolitionist,Cybernetic,Infiltrator,StarGuardian,Paragon,Sniper,Set3_Celestial,MechPilot,Set3_Sorcerer,Astro,Chrono,Battlecast,Set3_Brawler,SpacePirate,DarkStar,Vanguard,Starship,Mercenary,Protector,Set3_Mystic,Set3_Blademaster,DamageToPlayer,Top4,Win,Placement\n"
	f = open('data\\CSV\\tftmatchdata.csv','w')	
	f.write(attr)
	for data in result:
		output = reduce(lambda x,y : str(x) + "," + str(y), data)
		f.write(output)
		f.write('\n')
	f.close()
if __name__ == "__main__":
	fs = open ("data\\playerlist\\goldplayers.txt",'r')
	players = []
	while (1):
		p = fs.readline()
		if not p : break
		players.append(p.splitlines()[0])
	fs.close()
	r = []
	i = 0
	for p in players:
		i +=1
		print (i)
		r += run(p)
	generate_csv((r))
	pass
