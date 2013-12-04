import urllib
import json
from dota2Error import Dota2APIError
class APIConnection:
    #29135105
    def __init__(self, api_key, test_api=False):
        
        # Raise exception if no API key was provided
        if api_key is None:
            raise Dota2APIError('No API key provided')

        # Determine what api version to use
        if test_api is True:
            apiID = '205790'
        else:
            apiID = '570'

            
        self.api_key = api_key
        
        
        self.url = 'https://api.steampowered.com/IDOTA2Match_'+apiID+'/GetMatchHistory/V001/?key='+self.api_key

    def findMatch(self, player_name=None, hero_id=None, game_mode=None, skill=None, date_min=None, 
            date_max=None, min_players=None, account_id=None, leauge_id=None, start_at_match_id=None,
            matches_requested=None, tournament_games_only=None):
            
        # Get arguments
        args = locals()

        # Set request url
        req_url = self.url

        # Delete reference to self
        del(args['self'])

        # Build url string
        for arg in args.items():
            if arg[1] is not None:
                req_url += '&'+arg[0]+'='+arg[1]
        

        print req_url
        #jsondata = json.load(urllib.urlopen(self.url))
        #return jsondata


