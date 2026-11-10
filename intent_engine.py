"""Transparent rule-based conversational intent demonstrator (not an LLM)."""
import re
from dataclasses import dataclass, asdict

ACTIVITY = {
    'hiking': (r'\bhik(?:e|ing)\b|\bwalk(?:ing)?\b|\btrail\b|徒步|爬山', 'Hiking'),
    'sightseeing': (r'\bsightsee(?:ing)?\b|\bmuseum\b|\bcity\s+tour\b|\bshops?\b|观光|博物馆', 'City sightseeing'),
}
BUDGET = {'low': r'\b(?:cheap|low budget|budget-friendly|affordable|free)\b|便宜|低预算', 'flexible': r'\b(?:flexible budget|any budget)\b|预算不限'}
DISTANCE = {'nearby': r'\b(?:nearby|near me|near my city|local)\b|附近', '50km': r'\b(?:50\s?km|within 50|up to 50)\b'}

@dataclass
class Intent:
    activity: str | None = None
    budget: str | None = None
    distance: str | None = None
    place: str | None = None
    ambiguous: bool = False
    reasons: list | None = None


def detect(text: str) -> dict:
    """A narrow demonstrator: detect activity only for day-trip prompts, never assert probabilistic confidence."""
    text = (text or '').strip()[:1000]
    if not text:
        raise ValueError('Please enter a request.')
    activities = [label for pattern, label in ACTIVITY.values() if re.search(pattern, text, re.I)]
    activity = activities[0] if len(activities) == 1 else None
    budgets = [k for k, p in BUDGET.items() if re.search(p, text, re.I)]
    distances = [k for k, p in DISTANCE.items() if re.search(p, text, re.I)]
    place_match = re.search(r'\bnear\s+(Birmingham|London|Manchester|Leeds|Bristol)\b', text, re.I)
    place = place_match.group(1).title() if place_match else None
    reasons = []
    if not activities:
        reasons.append('Activity type was not specified.')
    if len(activities) > 1:
        reasons.append('More than one activity type was mentioned.')
    return asdict(Intent(activity, budgets[0] if budgets else None,
                         'Nearby' if 'nearby' in distances else 'Up to 50 km' if '50km' in distances else None,
                         place, bool(reasons), reasons))


def recommend(intent: dict) -> dict:
    """Illustrative fictional examples, not a live recommendation or verified route."""
    activity = intent.get('activity')
    if activity == 'Hiking':
        title = 'A quiet one-day nature walk'
        desc = 'Try a short forest-style trail, take a lunch break, and allow time to return before dusk.'
        details = ['Sample trail length: 6 km', 'Example difficulty: moderate']
    elif activity == 'City sightseeing':
        title = 'A relaxed city sightseeing day'
        desc = 'Consider a museum, a central park and a café, leaving room for breaks.'
        details = ['Activity: sightseeing', 'Flexible indoor/outdoor stops']
    else:
        title = 'A possible city day out (assumption)'
        desc = 'One interpretation is a museum visit, a park and lunch in the city. This may not match your goal.'
        details = ['Assumed activity: city sightseeing', 'Please refine if this is incorrect']
    if intent.get('budget'):
        details.append('Budget preference: ' + str(intent['budget']))
    if intent.get('distance'):
        details.append('Distance preference: ' + str(intent['distance']))
    if intent.get('place'):
        details.append('Area requested: ' + str(intent['place']))
    return {'title': title, 'description': desc, 'details': details, 'disclaimer': 'Illustrative, simulated itinerary — not a verified destination or live route.'}


def process(text: str, previous: dict | None = None) -> dict:
    text = (text or '').strip()
    if not text:
        raise ValueError('Please enter a request.')
    intent = detect(text)
    # The simulator is only a day-trip research scenario, not a general chatbot.
    trip_context = bool(re.search(r'\b(?:day\s?trip|day\s?out|hiking|hike|walking|trail|sightseeing|tour|museum|trip|travel|city|weekend)\b|徒步|旅行|旅游|周末', text, re.I))
    negative_city = bool(re.search(r"\b(?:don'?t|do not|not|never|no)\s+(?:want\s+to\s+)?(?:go\s+to\s+)?(?:the\s+)?city\b|不想去城市|不要城市", text, re.I))
    if negative_city:
        intent['activity'] = None
        intent['ambiguous'] = True
        intent['reasons'] = ['You ruled out the city. Please select the kind of trip you want.']
        return {'input': text[:1000], 'intent': intent,
                'recommendation': {'title':'Understood — no city trip',
                                   'description':'I will not suggest a city tour. Would you prefer hiking or another outdoor activity? Use Refine your request to choose.',
                                   'details':[], 'disclaimer':'Rule-based demo only; not a live AI response.'},
                'needs_clarification':True, 'engine':'deterministic-rule-simulation'}
    if not trip_context:
        return {'input': text[:1000], 'intent': {**intent,'ambiguous':False,'reasons':[]},
                'recommendation': {'title':'Demo mode: limited example',
                                   'description':'This offline demonstration only supports day-trip planning. To ask general questions and receive AI-generated answers, configure an API key and restart the server.',
                                   'details':[], 'disclaimer':'No live AI model is connected.'},
                'needs_clarification':False, 'engine':'deterministic-rule-simulation'}

    if previous and not intent['activity'] and re.search(r'\b(?:same|more|another)\b', text, re.I):
        intent['activity'] = previous.get('activity')
        intent['ambiguous'] = not bool(intent['activity'])
        intent['reasons'] = [] if intent['activity'] else intent['reasons']
    return {'input': text.strip()[:1000], 'intent': intent, 'recommendation': recommend(intent),
            'needs_clarification': intent['ambiguous'], 'engine': 'deterministic-rule-simulation'}


def refine(intent: dict, updates: dict) -> dict:
    allowed = {'activity': {'Hiking', 'City sightseeing'}, 'budget': {'Low', 'Flexible'},
               'distance': {'Nearby', 'Up to 50 km'}}
    new_intent = {key: intent.get(key) for key in ('activity', 'budget', 'distance', 'place')}
    for key, value in updates.items():
        if key not in allowed or value not in allowed[key]:
            raise ValueError('Invalid refinement field or option.')
        new_intent[key] = value
    if not updates:
        raise ValueError('Choose at least one refinement.')
    new_intent['ambiguous'] = new_intent['activity'] is None
    new_intent['reasons'] = ['Activity type was not specified.'] if new_intent['ambiguous'] else []
    return {'intent': new_intent, 'recommendation': recommend(new_intent),
            'needs_clarification': new_intent['ambiguous'], 'engine': 'deterministic-rule-simulation'}
