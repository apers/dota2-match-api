import urllib
import json
import dota2
from dota2Error import Dota2APIError
from Match import Match

class APIConnection:
    def __init__(self):
        
        # Raise exception if no API key was provided
        if dota2.api_key is None:
            raise Dota2APIError('No API key provided')

        # Determine what api version to use
        if dota2.test_api is True:
            apiID = '205790'
        else:
            apiID = '570'
            
        self.api_key = dota2.api_key
        
        self.match_history_url = 'https://api.steampowered.com/IDOTA2Match_'+apiID+'/GetMatchHistory/V001/?key='+self.api_key
        self.match_detail_url= 'https://api.steampowered.com/IDOTA2Match_'+apiID+'/GetMatchDetails/V001/?key='+self.api_key


    def _getData(self, url):
        try:
            data =  json.load(urllib.urlopen(url))
            return data
        except IOError as e: 
            if e.args[1] == 401:
                raise Dota2APIError('Invalid API key')
            else:
                raise e

    def searchMatch(self, player_name=None, hero_id=None, game_mode=None, skill=None, date_min=None, 
            date_max=None, min_players=None, account_id=None, leauge_id=None, start_at_match_id=None,
            matches_requested=None, tournament_games_only=None):
            
        # Get arguments
        args = locals()

        # Set request url
        req_url = self.match_history_url

        # Delete reference to self
        del(args['self'])

        # Build url string
        for arg in args.items():
            if arg[1] is not None:
                req_url += '&'+arg[0]+'='+str(arg[1])

        # Get match data
        #jsondata = self._getData(self.match_history_url)
        jsondata = json.load(open('matches.json'))

        # Check result
        if jsondata['result']['status'] != 1:
            raise Dota2APIError(jsondata['result']['statusDetail'])

        # Create dict for result info
        result = {'num_results' : jsondata['result']['num_results'], 'total_results' : jsondata['result']['total_results'], 'results_remaining' : jsondata['result']['results_remaining']};
    

        # Create matches from match data
        matches = list()

        for m in jsondata['result']['matches']:
            matches.append(Match(m))

        # Return result and matches
        return result, matches

    def _getMatchDetails(self, matchID):
        req_url = self.match_detail_url+'&match_id='+str(matchID)

        # Get match data
        #jsondata = self._getData(req_url)
        jsondata = json.load(open('detail.json'))
        return jsondata['result']
