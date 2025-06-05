

# ------------------------------------------------------------------ #
# ------------------------- Original symptom ----------------------- #
# ------------------------------------------------------------------ #
# Original symptom list with potential duplicates
symptom_list = [
'fever', 'cold', 'runny nose', 'sneezing', 'rash', 'dizziness', 'weakness', 'loss of appetite', 'cough',
'constipation', 'diarrhea', 'flu', 'shortness of breath', 'rapid breathing','migraine',
'itching', 'swelling', 'vomiting', 'infection', 'inflammation', 'cramp', 'bleeding', 'irritation', 'anxiety', 'depression','congestion',
'nausea', 'swollen lymph nodes', 'insomnia', 'cancer', 'diabetes', 'allergy', 'weight loss', 'weight gain', 'hair loss', 'blurred vision',
'numbness', 'dry mouth', 'frequent urination', 'acne', 'confusion', 'memory loss', 'difficulty swallowing', 'restlessness', 'bloating',
'gas', 'indigestion', 'acidity', 'nosebleed', 'urine issues', 'blood in stool', 'high blood pressure', 'weight fluctuation',
'low blood pressure', 'excessive thirst', 'dehydration', 'skin burning', 'sweat', 'jaundice',
'hearing loss', 'balance problem', 'irregular heartbeat', 'fainting', 'tremor', 'nervousness', 'panic attack', 'mood swing', 'difficulty concentrating',
'hallucination', 'lack of motivation', 'exhaustion',  'sprain', 'strain', 'arthritis', 'gout', 'headache', 'injury', 'chills',
'sleepy', 'bone fracture','back bone issue','fatigue',
'female issue', 'menopause', 'thyroid', 'piles', 'asthma','pneumonia','sugar',  'tingling', 'difficulty speaking',
'brittle nails', 'more hungry', 'obesity', 'seizures', 'hiccups', 'ulcers', 'dysentery', 'malaria', 'dengue', 'covid','typhoid', 'chickenpox', 'kidney issue',
#'waist pain','bone pain','pelvic pain', 'elbow pain', 'calf pain','hip pain',
'caesarean section','pregnancy', 'pediatric symptoms', 'blood in urine','broken voice', 'wound', 'cold intolerance', 'goiter','slow reflexes',
'male reproductive issues', 'female reproductive issues', 'dandruff','blister',''
]

# ------------------------------------------------------------------ #
# ------------------------- Mapping symptom ------------------------ #
# ------------------------------------------------------------------ #
symptom_synonyms = {
    'headache': [
        'throbbing headache', 'pounding head', 'cranial ache', 'head pressure', 'pressure on the head', 'pressure in the head', 'head pounding',
        'hammering pain in skull', 'aching brain', 'full-head ache', 'stabbing head sensation', 'skull-crushing pressure', 'nagging ache in head',
        'relentless cranial pounding', 'forehead-tightening discomfort', 'vice-like grip on head', 'pulsating headache', 'dull throb', 'piercing head agony', 'continuous headache hum', 'low-level head strain',
        'top-of-head soreness', 'subcranial ache', 'stabbing darts of pain in scalp', 'brain-squeezing feeling', 'top-heavy ache', 'all-encompassing head discomfort', 'band-like pressure around head',
        'persistent noggin ache', 'head tenderness', 'scalp-aching feeling', 'sensitive head region', 'brainache', 'mind-throbbing torment', 'front-lobe pressure', 'crown-of-head tension',
        'behind-the-eyes ache', 'skull-tight discomfort', 'never-ending head throb', 'grating ache inside skull', 'sinus-pressured ache', 'temple pounding', 'brain pulsation pain', 'cephalic torment',
        'oppressive ache under cranium', 'subtle persistent ache', 'head discomfort', 'dull pounding drumbeat in head', 'hammering inside skull walls', 'unyielding head tension', 'rote ache cycling through head',
        'cranium under siege', 'deep-set head pang', 'anchor-like pressure in head','head pounding like drums','issue with head','head aches','head is aching','head aches'
    ],
    'migraine': [
        'intense one-sided headache', 'migraine aura', 'pulsating pain in head', 'photophobia-associated headache', 'debilitating headache', 'migraine attack', 'searing half-skull ache', 'throbbing temple migraine',
        'light-sensitive head torture', 'migraine episode', 'crippling one-sided ache', 'sharp lancing head pain', 'skull-splitting half-side ache', 'throbbing migraine pulse', 'debilitating cranial assault',
        'severe sensory headache', 'disabling one-sided throb', 'catastrophic temple pounding',  'half-head agony', 'sharp lancing head pain', 'stabbing head sensation', 'pulsating migraine',
        'tension-triggered migraine', 'blinding headache', 'brain-splitting side ache', 'overwhelming migraine pressure', 'incapacitating headache event', 'shattering unilateral head pain', 'sensitive to slightest sound',
        'migraine meltdown', 'severe sensitivity headache', 'hammering half-head ache', 'aura shimmer leading to pain', 'throbbing unilateral agony', 'needle-like head stab', 'crushing half-skull sensation',
        'crippling light-triggered pain', 'tidal wave of head torment', 'incapacitating halo of pain', 'ear-to-temple throbbing on one side'
    ],
    'allergy': [
        'allergies',  'pollen sensitivity', 'allergic','sensitive to allergens', 
        'swollen nasal passages', 'eczema flare-up', 'itchy skin from allergens','allergic reactions in skin', 'excessive histamine release', 'increased mucus production',
        'blocked sinuses', 'allergy', 'anaphylactic reaction', 'anaphylaxis'
    ],
    'fever': [
        'high temperature', 'elevated body temperature', 'feeling feverish', 'fevering', 'running a fever', 'burning up', 'feeling internally hot', 'having a temperature', 'spiking a fever', 'febrile state',
        'raised core temperature', 'overheated body', 'intense body heat', 'thermal imbalance', 'body overheating', 'raging fever', 'heated condition', 'abnormally warm body', 'pyrexia', 'uncontrolled internal heat',
        'feeling aflame', 'body heat surging', 'hot to the touch', 'internal ignition of warmth', 'body temperature surging', 'excessive warmth inside', 'bodily heat overload', 'intense flush', 'thermometer reading high',
        'scorching internal climate', 'burning sensation from within', 'sweltering body feel', 'thermal elevation', 'heated bloodstream', 'furnace-like feeling', 'feeling like an oven', 'heat radiating under skin',
        'internal fire', 'ignited from the inside', 'excessive internal warmth', 'body boiling over', 'intense internal glow', 'unrelenting heat', 'blazing warmth',
        'molten interior heat', 'near boiling point', 'incapacitating heat', 'relentless feverishness', 'sizzling body temp', 'heat wave inside me', 'sweating due to internal heat',
        'red-hot core', 'smoldering embers of warmth', 'furnace-like core', 'pulsating heat', 'unremitting temperature rise', 'searing body condition', 'fire coursing through veins', 'endlessly hot', 'elevated reading on the thermometer',
        'no relief from heat', 'intense internal burning', 'volcanic warmth', 'torched from inside', 'superheated body', 'radical temperature spike', 'roasting sensation', 'tropical internal climate', 'heat-induced misery',
        'stoked internal fires', 'hothouse conditions inside', 'stifling fever fire', 'blazing internal inferno', 'relentless temperature climb', 'fever wave', 'bookar', 'booker','bukhar','bokhar','ukar','ukhar'
    ],
    'cough': [
        'Persistent cough', 'hacking cough', 'dry cough', 'wet cough', 'productive cough (with phlegm)', 'barking cough', 'non-productive cough', 'chronic cough',
        'coughing up mucus/sputum/blood', 'irritating cough', 'scratchy cough', 'whooping cough-like sound', 'continuous throat clearing', 'raspy hacking', 'chesty cough',
        'rattling cough', 'deep-chested cough', 'shallow annoying cough', 'tickling cough', 'lingering throat hack', 'spasm-like coughs', 'throaty expulsions',
        'repetitive cough bursts', 'phlegmy hacking', 'coughing', 'dry tickling cough', 'persistent throat tickle',
        'strangling cough', 'wheezing cough', 'loud barking cough', 'cracking cough', 'sputum-laden cough', 'cough with gagging', 'spasmodic cough', 'stubborn dry cough',
        'overwhelming coughing sensation', 'violent coughing fits', 
        'chronic phlegm cough', 'intense wheezing cough', 'grating cough', 'wet chesty cough', 'gurgling cough','khasi','kansi'
    ],
    'sore throat': [
        'scratchy throat', 'painful throat', 'burning throat', 'irritated throat', 'swollen throat', 'inflamed throat', 'throat discomfort', 'throat scratchiness',
        'raw throat', 'tight throat', 'feeling of something stuck in throat', 'hoarse throat', 'swollen tonsils', 'throat inflammation', 'red throat', 'sore and swollen throat',
        'gritty throat', 'tender throat', 'raspy throat', 'dry throat', 'throat burning sensation', 'feeling of throat swelling', 'pain on swallowing', 'raw feeling in throat',
        'sore feeling when talking', 'throat soreness', 'painful swallowing', 'constant throat irritation', 'throat muscle soreness', 'tight feeling in throat',
        'throat dryness', 'itchy throat', 'burning sensation in throat', 'scratching feeling in throat', 'tenderness in throat', 'chronic throat discomfort', 'raspiness in voice',
        'feeling like throat is closing', 'constant need to clear throat', 'sore throat with hoarseness', 'throat is sore','mucus in throat', 'mucus in mouth'
    ],

   'weakness': [
    'low energy', 'feeling sluggish', 'debilitating tiredness', 'drowsiness', 'chronic fatigue syndrome',
    'feeling lethargic', 'mental sluggishness', 'difficulty keeping eyes open', 'lack of vitality', 'feeling disconnected',
    'constant tiredness', 'fatigued muscles', 'endless tiredness', 'lethargic movements', 'lacking strength', 
    'body feels heavy', 'brain fog', 'struggling to stay awake', "can’t focus due to fatigue", 'slow to move', 'slow to think',
    'exhausted no matter how much I sleep', 'general weakness', 'barely functioning', 'worn out', "can’t get out of bed",
    'out of energy', 'lack of strength in limbs', 'sluggish reaction time','trouble keeping eyes open during the day', 
    'body feels like lead', "can’t finish daily tasks", 'short bursts of energy followed by crashes',
    'muscle weakness without exertion', 'tired even after sleeping well'
],

    'nausea': [
        'feeling nauseous', 'queasy', 'stomach turning', 'sick feeling', 'gagging sensation', 'discomfort in stomach', 'unsettled stomach',
        'vomit-like sensation', 'stomach churn', 'sick to stomach', 'nauseous feeling', 'spinning stomach', 'gagging feeling', 'feeling on the verge of throwing up',
        'uneasy stomach', 'intense queasiness', 'morning sickness feeling','feel like vomiting',
        'stomach discomfort', 'stomach churn', 'puking feeling', 'feeling like you could throw up',
        'unsettled feeling in stomach', 'feeling lightheaded with nausea', 'stomach unease','nauseous',
        'sick feeling after meals', 'swirling stomach', 'nauseous waves', 'gag reflex activated'
    ],
    'dizziness': [
        'Lightheadedness', 'woozy sensation', 'spinning feeling', 'off-balance', 'unsteady', 'giddy feeling', 'vertiginous sensation', 
        'wobbly feeling', 'swaying in mind', 'head swimming', 'feeling as if room is turning', 'disoriented equilibrium', 'teetering sense', 'tipsy sensation without alcohol',
        'floating head', 'unstable ground feeling', 'swirling environment', 'sense of being on a boat', 'loss of spatial orientation', 'drifting balance',
        'feeling like I might topple', 'wavy floor sensation', 'heady unsteadiness', 'murky equilibrium', 'airy head sensation', 'constant near-tip-over feeling', 'mental wobble',
        'gravity shifting under feet', 'seasick feeling on land', 'fuzzy-headed instability', 'dizzy', 
        'wavy-field-of-view sensation', 'lurching environment', 'faltering steadiness', 'delicately balanced but slipping', 'rubbery legs feeling', 'giddy swirl in head',
        'tilting world', 'swaying sensation', 'imbalance feeling', 'shaky equilibrium', 'spinning sensation', 'feeling off-kilter'
    ],
'shortness of breath': [
    'shortness of breath', 'breathlessness', 'difficulty breathing', 'feeling air hunger', 'shallow breathing', 'gasping for air', 'less breath happening',
    'lower breathing', 'labored breathing', 'struggling to breathe', 'feeling suffocated', 'cannot catch my breath', 'panting heavily', 'air feeling thin',
    'breathing struggle', 'lack of oxygen', 'lungs working overtime', 'chest feels restricted', 'fighting for each breath', 'difficulty in breathing',
    'strained respiration', 'feeling smothered', 'desperate for oxygen', 'winded easily', 'constant puffing', 'breathing feels blocked', 'inhaling with effort',
    'forced breathing', 'breathless', 'sensation of drowning in open air', 'chest heaviness on breathing', 'incomplete lung expansion',
    'inadequate airflow', 'lungs not filling properly', 'needing to breathe harder', 'stuck in half-breath', 'breath cut short', 'huffing and puffing',
    'shallow panting', 'frantic search for air', 'hyperventilating feeling', 'feeling as if air is too thick', 'minimal air exchange',
    'muscle effort just to breathe', 'chest oppression', 'suffocating sensation even in open space', 'feeling strangled by lack of air',
    'restrictive breathing pattern', 'breathing feels like pushing through a straw', 'air-starved lungs', 'cannot take a deep breath',
    'strained oxygen intake', 'feeling like each breath is a struggle', 'never fully satisfied inhalation', 'gasping between words',
    'needy breathing pattern', 'barely pulling in enough air', 'lungs working at half capacity', 'respiratory distress',
    'continuous short-windedness', 'lack of breath', 'shortage of breath', 'breath shortage', 'light breathing', 'mild breathing',
    'unable to breathe', 'wheezing', 'lacking breath', "can’t breathe deeply", "can’t take my breath", "can’t breathe", 'breathing rate is low',
    'breathing rate is slow', 'dyspnea', 'trouble breathing', 'painful when breathing',
    "can’t catch my breath", "can’t get enough air", "can’t breathe properly", 'cannot breathe deeply', "can’t take a full breath",
    'breath is shallow', 'breath feels stuck', 'breath is short', 'breath is labored', 'breath is heavy', 'breath feels blocked',
    'breath feels cut off', 'breath feels tight', 'breath feels restricted', 'breath feels painful', 'breath feels difficult',
    'breathing is hard work', 'breathing is a struggle', 'breathing is painful', 'breathing feels tight', 'breathing feels heavy',
    'breathing feels like pushing through resistance', 'breathing feels shallow and fast', 'breathing feels shallow and weak',
    'lungs feel tight', 'lungs feel heavy', 
    'lungs are not expanding fully', "lungs don’t fill properly", 'lungs feel air starved', 'lungs feel empty',
    'feeling like suffocating', 'feeling like air is too thick to breathe', 'feeling strangled by lack of air',
    'feeling smothered', 'feeling choked', 'feeling like air is not enough', 'feeling like chest is tight',
    'chest feels heavy', 'chest feels tight', 'chest feels restricted', "chest feels like it’s being squeezed",
    'chest oppression when breathing', 'chest pain on breathing', 'chest discomfort when breathing',
    'muscles feel strained just to breathe', 'muscle effort just to breathe', 'muscle tiredness when breathing',
    'need to breathe harder', 'need to take deeper breaths', 'need to gasp for air', 'need to gasp between words',
    'panting like after exercise', 'panting heavily', 'panting and gasping', 'huffing and puffing',
    'gasping for air', 'gasping between sentences', 'short winded after slight effort', 'winded easily',
    'hyperventilating feeling', 'feeling like I’m breathing too fast', 'breathing too fast but can’t get enough air',
    'incomplete lung expansion', 'inadequate airflow', 'reduced air exchange', 'minimal air intake',
    'breathing feels blocked', 'breathing feels obstructed', 'airflow feels restricted', 'airflow feels limited',
    "can’t take a deep breath", 'cannot draw a full breath', 'never fully satisfied with breath', 'breath never feels enough',
    'constant puffing', 'continuous shortness of breath', 'constant need to catch breath', 'feeling out of breath',
    'lack of oxygen in blood', 'feeling oxygen deprived', 'feeling desperate for oxygen', 'lungs working overtime',
    "feeling like chest can’t expand", 'respiratory distress', 'difficulty inhaling', 'difficulty exhaling',
    'feeling breathless', 'feeling suffocated even when sitting still', 'feeling smothered in open air',
    'cannot breathe deeply', 'cannot breathe properly', 'unable to breathe normally',
    'painful breathing', 'pain when breathing', 'sharp pain with breath', 'burning sensation when breathing',
    'tightness in chest on breathing', 'chest tightness with breath', 'chest pressure when breathing',
    'struggling for each breath', 'fighting for air', 'feeling strangled by breathlessness',
    'air feels thin', 'air feels insufficient', 'air feels difficult to inhale',
    'breathing rate is slow and shallow', 'breathing rate is low and weak', 'breathing rate is irregular',
    'breath cut short', 'stuck in half-breath', 'needy breathing pattern',
    'barely pulling in enough air', 'lungs working at half capacity', 'shortness of breath after mild exertion',
    'noisy breathing', 'wheezing when breathing', 'whistling sound when breathing',
    'stridor', 'respiratory wheeze', 'breath sounds abnormal'
],
   'rapid breathing': [
    'heavy breathing', 'fast breathing', 'heart skipping beats', 'heart begins to beat faster', 'heart begins to beat fast',
    'breathing feels rushed', 'breathing heavily after little effort',
    'quickened breath', 'rapid chest movement', 'breathing faster', 'increased breathing rate', 'breathing rate is high',
    'feeling winded', 'hyperventilating', 'hard to slow down breathing', 'chest rising quickly', 'labored rapid breaths',
    'breathing feels out of control', 'feeling like I’m suffocating',  'lungs working overtime', 'breathing feels unnatural',
    'breathing in short bursts', 'breathing too fast to speak properly', 'racing heart and fast breathing', 
    'anxious breathing', 'fluttering heartbeat with fast breath', 'heart pounding and rapid breath'
],

    'insomnia': [
        'difficulty sleeping', 'trouble sleeping', 'sleeplessness', 'restlessness at night', 'inability to fall asleep', 'waking up during the night', 'frequent wake-ups',
        'early morning wakefulness', 'poor sleep quality', 'sleep deprivation', 'sleep disturbance', 'trouble staying asleep', 'sleep interruptions', 'unable to sleep through the night',
        'insufficient sleep', 'lack of sleep', 'unrefreshing sleep', 'tossing and turning', 'unsettled sleep', "can’t sleep", 'sleep not coming',
        'waking up too early', 'difficulty with sleep onset', 'difficulty getting comfortable at night', 'sleeping problems', 'frequent nighttime awakenings', 'irregular sleep cycle',
        'waking up exhausted', 'sleep cycle disruption', 'sleep onset difficulty', 'mental hyperactivity preventing sleep', 'cannot sleep', 'unable to sleep','not able to sleep',
        'unable to fall asleep', 'not able to fall asleep','not getting sleepy','not feel sleepy','not sleepy','not getting sleep'
    ],
    'rash': [
        'skin rash', 'redness on skin', 'skin irritation', 'skin inflammation', 'skin breakout', 'hives', 'blotchy skin', 'skin eruption', 'skin lesions',
        'red bumps on skin', 'inflamed skin', 'patchy rash', 'discolored skin', 'eczema', 'psoriasis patches', 'contact dermatitis', 'hives breakout', 'heat rashes'
        'welts on skin', 'itchy patches on skin', 'skin redness', 'rash with pus', 'pimple-like rash', 'rash caused by allergic reaction', 'rashes', 'skinrash', 'hives',
        'rashes from medication', 'painful itching on skin'
    ],
    'congestion': [
        'nasal congestion', 'blocked nose', 'stuffy nose', 'clogged nasal passages', 'nasal obstruction', 'sinus blockage', 'stuffy sinuses', 'pressure in sinuses',
        'nasal blockage', 'swollen nasal passages', 'congested sinuses', 'nose congestion', 'nasal stuffiness', 'head congestion', 'nose got blocked', 'nose is blocked',
        'swelling of nasal tissues', 'sinus pressure', 'stuffy feeling in head', 'congestion in sinus cavities', 'nasal stuffy feeling',
        'inflamed nasal passages', 'feeling of a blocked nose', 'swollen nostrils', 'nasal airway blockage', 'sinus drainage blockage',
        'clogged airways', 'excess mucus in nose', 'thick mucus in nostrils', 'nasal obstruction from mucus', 'inability to breathe through nose',
        'nasal phlegm buildup', 'blocked airways', 'increased mucus production', 'congested nasal lining', 'swelling in nasal cavity', 'sinus problem',
        'nasal fullness', 'pressure behind the eyes from congestion', 'nasal sinus blockage', 'nasal breathing difficulties', 'nose is closed'
    ],
    'runny nose': [
        'nasal discharge', 'drippy nose', 'clear runny nose', 'watery nose', 'excessive mucus secretion', 'nose dripping', 'watery nasal discharge', 'mucus from nose',
        'frequent nose blowing', 'excessive snot', 'thin nasal discharge', 'clear mucus', 'constant nose drip', 'streaming nose', 'watery runny nose', 'mucus dripping down from nose',
        'nose running uncontrollably', 'sticky nasal discharge', 'clear discharge from nostrils', 'frequent nasal wiping', 'constant nasal leaks', 'draining sinuses',
        'constant nasal secretions', 'wet nose', 'nose discharge', 'sinus leakage', 'flowing nose', 'uncontrolled nasal discharge', 'nose leakage', 'mucus leaking',
        'dripping from nostrils', 'clogged but dripping nose', 'excessive mucus from nostrils', 'constant nasal drip', 'nose leaking', 'mucus nose', 'mucus leakage',
        'dripping sinuses', 'mucus continuously dripping', 'snotty nose', 'stuffy nose with runny discharge','dripping all day long'
    ],
    'sneezing': [
        'sneezes', 'repetitive sneezes', 'unstoppable nasal explosions', 'sneeze', 'chain-sneezing', 'nasal expulsions', 'unable to control sneeze',
        'nasal reflex outbursts', 'convulsive sneezing', 'rapid-fire sneezes', 'machine-gun sneezing', 'surprise sneezes', 'sneezy',
        'tickling in nose triggering sneezes', 'uncontrollable nasal reflex', 'sneeze bursts', 'nasal reflex reactions'
    ],
    'swollen lymph nodes': [
        'swollen glands', 'lymph node swelling', 'enlarged lymph nodes', 'swelling in neck', 'lumps in neck', 'tender lymph nodes', 'painful lymph nodes', 'swelling near jaw',
        'lymphatic swelling', 'lymph node enlargement', 'swollen glands under arms', 'underarm lymph node swelling', 'swollen neck glands', 'increased lymph node size',
        'lymphatic system swelling', 'lumps under the skin', 'swollen lymphatic glands', 'painful lumps in neck', 'inflamed lymph nodes', 'lymph node tenderness', 'neck swelling',
        'uncomfortable lumps in neck', 'tender neck lumps', 'swollen lymph glands in groin', 'swollen lymph nodes in armpit', 'painful swelling in neck', 'inflamed glands',
        'lymph node tenderness under jaw', 'enlarged glands in the throat', 'neck lumps', 'tender swollen glands', 'neck lymphatic swelling',
        'inflamed and tender lymph nodes', 'lymphatic swelling with pain'
    ],
  
   'diarrhea': [
        'loose stools', 'loose motion', 'frequent bowel movements', 'watery stools', 'runny stools', 'loose bowels', 'urgent need to defecate', 'watery bowel movements', 
        'frequent trips to the bathroom', 'diarrhea with cramping', 'abnormal stool consistency', 'watery feces', 'fecal urgency', 'loose bowel movement',
        'digestive distress', 'frequent liquid stools', 'runny bowel movements', 'intense bowel movements', 'diarrhoea',
        'diarrheal episode', 'loose stool rush', 'pale watery stools', 'frequent bowel clearing', 'fluid-filled stools', 'uncontrolled liquid stools', 'loose stool frequency',
        'constantly running to the bathroom', 'liquid-filled intestines', 'abnormally frequent bowel movements', 'severe bowel looseness', 'bowel irregularity',
        'liquid stools'
    ],
    'vomiting': [
        'throwing up', 'puking', 'retching', 'emesis', 'forcefully throwing up', 'heaving', 'sick stomach', 'food coming out', 'food came out',
        'gagging', 'expelling stomach contents', 'stomach expulsion', 'upchucking', 'spitting up', 'retching reflex', 'vomit',
        'forceful expulsion of food', 'involuntary stomach release', 'emetic response', 'feeling of needing to vomit', 'gag reflex triggering', 
        'unpleasant stomach eruption', 'stomach contents expelled forcefully', 'gastrointestinal purge', 'expulsion of gastric contents', 'violent heaving',
        'vomit-induced gagging', 'stomach-purging sensation', 'retching uncontrollably', 'throwing up after eating', 'puking episodes', 'sick and throwing up',
        'puking from irritation', 'regurgitating food', 'empty stomach vomiting', 'morning sickness vomiting', 'emesis due to motion sickness', 'heaving up'
    ],
    'cold': [
        'common cold', 'head cold', 'mild viral infection', 'slight sniffles', 'catching a cold', 'seasonal cold','light upper respiratory infection', 'mild sniffle bug',
        'standard cold virus', 'low-grade nasal virus', 'mild runny-nose ailment', 'basic rhinovirus', 'short-term sniffles', 'routine winter bug', 'easy viral cold',
        'feeling cold'
    ],
    'sweat': [
        'sweating','perspiring heavily', 'sweating buckets', 'dripping perspiration', 'bead-like sweat on skin', 'moisture streaming down face', 
        'constant perspiration','salty perspiration', 'glistening with sweat', 'sweat trickling down spine', 'drenching perspiration',
        'sweat-laden body', 'humid feeling', 'slick skin', 'warm moisture on skin', 'sweat beads forming everywhere', 'bodily moisture overload', 'persistent dampness', 'sweaty palms and forehead',
        'sweat dripping off hairline', 'sweat-soaked sheets', 'nocturnal sweating', 'smelly perspiration', 'standing in a pool of sweat', 'sweat forming under arms', 'shiny perspiring face',
        'sweat-induced chafing', 'slick and slippery feeling', 'permanent dampness'
    ],
    'swelling': [
        'swollen', 'edema', 'swellings', 'fluid retention', 'swollen body part', 'inflamed tissue', 'puffiness', 'swells', 'enlarged tissue area'
    ],
    'tremor': [
        'twitching', 'involuntary movements', 'nervous shaking', 'rhythmic shaking', 'trembling hands', 'uncontrolled muscle movement',
        'shaking limbs', 'twitchy fingers', 'flickering motion', 'trembling body', 'shaky movements', 'muscle spasms', 'jerking', 'shaky hands',
        'shaking from cold', 'nervous tremors', 'trembling sensation', 'shuddering', 'uncontrollable shaking', 'flickering muscles', 'twitching eyes', 'nervous jerks', 'shaky fingers',
        'twitching limbs', 'muscle jerks', 'nervous body shakes', 'involuntary shaking', 'feeling of tremors', 'trembling body parts', 'sporadic body shaking',
        'hand shaking', 'shaky voice', 'rhythmic tremors', 'body quivering', 'body shudders'
    ],
    'chills': [
        'Shivering', 'trembling with cold', 'uncontrollable shaking', 'teeth chattering', 'feeling frosty', 'quivering limbs', 'body shaking from cold',
        'frigid vibrations', 'quaking with chill', 'hair standing on end', 'trembling internally', 'spasmodic shivers', 'cold-induced tremble', 'chilled to the bone',
        'freezing sensation', 'vibrating with cold', 'small uncontrollable shakes', 'persistent shuddering', 'subtle shivers', 'prickly gooseflesh', 'frost-like feeling', 'quivery muscles',
        'rattled by chill', 'shudders running down spine', 'uncontrollable cold tremors', 'shaky fingers and toes', 'rattling teeth', 'jittering from cold', 'frigid trembles',
        'cold-induced shaking', 'numbing cold', 'shiver', 'shivers'
    ],

    'confusion': [
        'disorientation', 'muddled thinking', 'mental fog', 'trouble thinking clearly', 'brain fog', 'cognitive cloudiness', 'puzzled state', 'jumbled thoughts', 'incoherent reasoning', 'tangled mental process',
        'unclear comprehension', 'befuddled mind', 'scrambled logic', 'perplexed state', 'hazy understanding', 'blurred mental picture', 'fuzzy reasoning', 'perplexity', 'baffled intellect',
        'uncertain grasp', 'foggy mental landscape', 'clouded judgment', 'unclear headspace', 'mixed-up thoughts', 'lack of mental clarity', 'distorted perspective', 'murky understanding',
        'minds in knots', 'head scrambled eggs feeling', 'no clear thread of thought', 'haphazard reasoning', 'bewildered stance', 'lost mental bearings', 'mental haze', 'unclear mental signals',
        'vague cognitive process', 'mental static', 'mentally adrift', 'diluted focus', 'no sharpness in mind', 'blinking confusion', 'unsure mental footing', 'perplexed awareness', 
        'reduced mental acuity', 'messy mental white noise'
    ],
  
    'memory loss': [
        'forgetfulness', 'difficulty recalling', 'poor memory', 'memory lapses', 'amnestic episodes', 'short-term memory issues', 'difficulty remembering recent events', 'blanking out on details',
        'slip of the mind', 'fuzzy recollections', 'failing memory', 'losing track of thoughts', 'vacant mental storage', 'holes in memory', 'patchy recollection',
        'vanishing details from mind', 'gaps in remembrance', 'fleeting mental notes', 'mental blanks', 'fragmented memory', 'elusive past events', 'stuttering memory', 'hazy recall',
        'details fading away', 'mental erasures', 'unstable memory bank', 'shaky recollections', 'selective forgetfulness', 'mental blackouts', 'fuzzy mental snapshots', 'misplacing thoughts',
        'memory glitches', 'jumbled recall', 'inability to summon certain facts', 'feeling brain-drained', 'memory going dark', 'fragments of information missing', 'scattering of remembered info',
        'ghost-like recollections', 'losing the thread of events', 'names escaping me', 'scrambled memory patterns', 'drifting mental records', 'unreliable mental archives', 'evaporation of recent info',
        'dimming recollection', 'disintegrating memory', 'thinning retention', 'leaky mental container', 'short-circuited memory', 'mental fade-outs', 'mental sputtering', 'forgetting simple things',
        'intangible memories slipping away', 'memory weakening over time', 'groping for details', 'elusive truths once known', 'mental book pages going blank', 'unstable mental files',
        'dulled memory edges', 'uncertain memory foothold', 'eroded recollections', 'falling out of my mind', 'scattering mental fragments', 'temporary amnesia-like moments', 'no access to recent thoughts',
        'memory wires disconnected', 'stuttering recollection attempts', 'defragmented mental records', 'shaky mental camera', 'fading mental impressions', 'mind like a sieve', 'losing info instantly',
        'rattled mental library', 'concept slip-through', 'flickering data in mind', 'barren mental shelves', 'no retrieval of recent facts', 'thinking it’s on the tip of my tongue but never surfacing',
        'losing track of recent conversations', 'difficulty holding new info', 'memory short-circuits frequently', 'mental vacancy', 'ephemeral recollections', 'passing mental clouds with no retention',
        'drifting away from details', 'no anchor to past events','do not remember anything', 'forget everything', 'forgetting everything'
    ],
  'hallucination': [
    'delusion', 'illusion', 'false perception', 'sensory distortion', 'auditory hallucination', 'illusions', 'delusions',
    'perceptual distortion', 'false sensory experience', 'phantom perception', 'psychotic episode', 'imagined sight', 'imagined sound', 'mind illusion',
    'sensory misperception', 'hallucinatory experience', 'out-of-body experience', 'visual illusion', 'auditory illusion', 'mental delusion', 'altered reality'
],

  'loss of appetite': [
    'decreased appetite', 'reduced appetite', 'appetite loss', 'lack of appetite', 'poor appetite', 'no desire to eat', 'loss of interest in food', 'unwillingness to eat',
    'inability to eat', 'diminished appetite', 'eating less', 'loss of hunger', 'food aversion', 'food intolerance', 'decreased desire to eat', 'lack of hunger',
    'decrease in food intake', 'disinterest in eating', 'feeling full quickly', 'loss of taste for food', 'absence of hunger', 'less hungry',
    'difficulty eating', 'reduced food consumption', 'lack of craving for food', 'feeling satiated quickly', 'loss of appetite', 'eating less',
    'anorexia', 'anorexia nervosa', 'feeling no appetite', 'feeling disinterested in food', 'poor food intake', 'reduced food desire', 'appetite is less'
],

'constipation': [
    'difficulty passing stool', 'infrequent bowel movements', 'hard stools', 'painful bowel movements', 'feeling of incomplete evacuation', 'straining during bowel movement',
    'constipated', 'dry stool', 'difficulty in defecation', 'delayed bowel movements', 'irregular bowel movements', 'hard and dry stool', ' don\'t have any motion',' don\'t have clear stomach',
    'trouble with bowel movements', 'trouble passing stool', 'slow bowel transit', 'stool retention', 'decreased bowel movement frequency', 'bowel sluggishness', 'motion not passing',
    'straining to poop', 'bowel movement difficulty', 'slow bowel function', 'lack of bowel movement', 'intestinal irregularity', 'do not have clear stomach', 'unclear motion', 'unclear stomach',
    'excreta not coming'
],

'flu': [
    'influenza', 'seasonal flu', 'viral flu', 'flu virus', 'common flu', 'flu infection', 'respiratory flu', 
    'viral infection', 'influenza virus', 'contagious flu', 'pandemic flu', 'influenza fever', 'flu epidemic'
],

'infection': [
    'contamination', 'infectious disease', 'germ infection', 'bacterial infection', 'viral infection', 'fungal infection', 'parasite infection', 'microbial infection',
    'pathogen invasion', 'infected area', 'infection outbreak', 'systemic infection', 'local infection', 'wound infection', 'skin infection', 'respiratory infection',
    'urinary tract infection', 'ear infection', 'sinus infection', 'blood infection', 'sepsis', 'foodborne illness', 'infected tissue', 'infection of the bloodstream',
    'infection of the lungs', 'bacterial contamination', 'infectious agent', 'disease-causing infection', 'contagion', 'infection symptoms',
    'infection spread', 'infection risk', 'infectious condition', 'contagious disease'
],

'inflammation': [
    'inflammatory response', 'inflammatory reaction', 'inflammation of tissues', 'inflammation in the body', 'inflamed',
    'internal inflammation', 'inflammatory condition', 'inflammatory disorder', 'inflammation from disease'
],

'cramp': [
    'paining cramp', 'cramped muscle', 'cramping sensation', 'cramping'
],

'bleeding': [
    'blood loss', 'hemorrhage', 'hemorrhaging', 'bloodshed', 'wound bleeding', 'internal bleeding', 'external bleeding', 'bleeding from injury'
    'spurting blood', 'bleeding wound', 'gushing blood','bleeding'
],

'irritation': [
    'allergic irritation', 'irritated feeling'
],

'anxiety': [
    'unease', 'stress', 'fear', 'apprehension', 'nervous tension', 'anxiousness', 'anxiety disorder', 'worry',
    'anticipatory anxiety', 'anxiety attack', 'apprehensive feeling', 'distress', 'emotional unease', 'worrying', 'overthinking', 'mental tension'
],

'depression': [
    'sadness', 'melancholy', 'despair', 'low mood', 'dismay', 'hopelessness', 'discouragement', 'despondency', 'blues', 'dejectedness',
    'feeling down', 'feeling hopeless', 'loss of interest', 'unhappiness', 'mental exhaustion', 'loss of joy', 'major depressive disorder',
    'depressed', 'depressive episode', 'anhedonia', 'negative mood', 'downheartedness', 'so sad'
],

'cancer': [
    'malignant tumor', 'carcinoma', 'neoplasm', 'oncological disease', 'cancerous growth', 'tumor', 'metastatic cancer', 'cancer cells', 'tumor growth',
    'breast cancer', 'lung cancer', 'skin cancer', 'prostate cancer', 'colon cancer', 'leukemia', 'lymphoma', 'sarcoma', 'head and neck cancer',
    'pancreatic cancer', 'bladder cancer', 'stomach cancer', 'cancer diagnosis', 'cancerous tumor', 'fatal cancer', 'chronic cancer', 'advanced cancer',
    'stage 3 cancer', 'cancer treatment', 'chemotherapy', 'radiation therapy', 'cancer stage', 'oncology'
],

'diabetes': [
    'diabetes mellitus', 'high blood sugar', 'high sugar', 'insulin resistance', 'type 0 diabetes', 'type 2 diabetes', 'gestational diabetes', 'sugar diabetes',
    'chronic high blood sugar', 'endocrine disorder', 'metabolic disorder', 'insulin deficiency', 'insulin imbalance', 'glucose intolerance', 'sugar level is high',
    'blood sugar imbalance', 'hyperglycemia', 'diabetic condition', 'diabetic disease', 'diabetic disorder', 'pancreatic disorder', 'non-insulin dependent diabetes',
    'insulin-dependent diabetes', 'pre-diabetes', 'diabetic'
],

'weight loss': [
    'fat loss', 'loss of body weight', 'slimming down', 'losing pounds', 'weight reduction', 'weight management', 'fat burning', 'weight cut', 'weight is decreasing',
    'weight got decreased', 'weight decrease', 'weight is decreased', 'weight went down','lost my weight',
    'body slimming', 'reduction in weight', 'fat shedding', 'calorie burning', 'trimming down', 'losing inches', 'dropping weight', 'healthy weight loss',
    'body fat reduction','dieting', 'fitness weight loss', 'weight loss goals', 'weight going down', 'losing weight', 'loss of weight', 'lost weight',
    'lost a lot of weight','lost weight','lost some weight','weighing less','loosing too much weight','weightloss', 'loosing weight', 'loss of weight',
    'fatty loss', 'shedding pounds', 'slimming down', 'cutting body fat', 'trimming weight', 'dropping excess mass', 'losing inches', 'weight has reduced',
    'reducing body size', 'burning fatness', 'getting leaner', 'calorie deficit', 'cutting weight', 'body recomposition', 'weight is reduced', 'weight has been reduced'
],

'hair loss': [
    'alopecia', 'balding', 'thinning hair', 'hair thinning', 'hair shedding', 'hair fall', 'scalp hair loss', 'bald spots', 'receding hairline', 'loosened hair roots',
    'hairline recession', 'hair breakage', 'excessive hair loss', 'temporary hair loss', 'pattern baldness', 'male pattern baldness', 'female pattern baldness',
    'androgenic alopecia', 'patchy hair loss', 'diffuse hair loss', 'hair loss due to stress', 'postpartum hair loss', 'age-related hair loss', 'genetic hair loss',
    'hair fall disorder', 'alopecia areata', 'hair loss condition', 'scalp thinning', 'hair loss treatment','hairloss', 'lost hairs', 'loosing hairs', 'loosing my hairs',
    'hair lost', 'hair got lost'
],

'blurred vision': [
    'vision impairment', 'unclear vision', 'fuzzy vision', 'distorted vision', 'foggy vision', 'hazy vision', 'blurry eyesight', 'impaired vision', 'cannot see properly',
    'vision distortion', 'clouded vision', 'poor vision', 'vision fuzziness', 'difficulty seeing clearly', 'blurred eyesight', 'visual disturbance',
    'unclear eyesight', 'visual impairment', 'blurry sight', 'sight distortion', 'vision problems', 'temporary blurred vision', 'chronic blurred vision',
    'blurry perception', 'not well visible','difficulty in seeing','difficult to see','hard to see', 'not clearly visible'
],

'numbness': [
    'loss of sensation', 'lack of feeling', 'reduced sensation', 'sensory loss', 'numb sensation', 'feeling of numbness',
    'numb feeling', 'sensory numbness', 'partial numbness', 'temporary numbness', 'persistent numbness', 'numb'
],

'dry mouth': [
    'xerostomia', 'cottonmouth', 'parched mouth', 'thirsty mouth', 'dryness in the mouth', 'lack of saliva', 'reduced saliva production', 'mouth dryness',
    'sticky mouth', 'dryness of the oral cavity', 'uncomfortable dry mouth', 'dry tongue', 'thirsty feeling in the mouth', 'saliva deficiency', 'oral dryness',
    'mouth discomfort', 'dryness in the mouth and throat', 'sore dry mouth', 'dehydrated mouth', 'dryness due to medication', 'mouth feels dry', 'no saliva',
    'mouth is dry'
],

'frequent urination': [
    'urinary frequency', 'increased urination', 'urinary urgency', 'excessive urination', 'frequent trips to the bathroom', 'overactive bladder',
    'need to urinate often', 'urination urgency', 'recurrent urination', 'constant urination', 'frequent need to pee', 'urgent urination', 'pollakiuria',
    'urinary incontinence', 'nighttime urination', 'nocturia', 'constant need to urinate', 'increased frequency of urination','frequent urination'
],

'acne': [
    'pimples', 'pimple', 'blemishes', 'zits', 'whiteheads', 'blackheads', 'clogged pores','skin spots', 
    'clogged follicles', 'sebaceous gland activity'
],

'difficulty swallowing': [
    'dysphagia', 'trouble swallowing', 'swallowing difficulty', 'painful swallowing', 'difficulty with swallowing', 'difficulty in swallowing food',
    'inability to swallow', 'swallowing discomfort', 'choking sensation', 'difficulty swallowing pills', 'food getting stuck', 'hard time swallowing',
    'difficulty in throat swallowing', 'swallowing obstruction', 'swallowing problems', 'gagging while swallowing', 'swallowing trouble',
    'feeling of blockage while swallowing', "can’t swallow food", 'difficulties swallowing'
],

'restlessness': [
    'unease', 'fidgeting', 'inability to relax', 'impatience', 'uneasiness', 'hyperactivity', 'jitteriness', 'inability to stay still', 'unsettledness',
    'fidgety feeling', 'lack of calm', 'restless feeling'
],

'bloating': [
    'abdominal bloating', 'stomach bloating', 'gas buildup', 'swollen belly', 'feeling of fullness', 'abdominal distention',
    'overfull stomach', 'stomach swelling', 'intestinal bloating', 'bloated stomach', 'bloating sensation',
    'gassy stomach', 'bloating after eating', 'digestive bloating', 'feeling bloated', 'bloating in the abdomen', 'gas pain'
],

'gas': [
    'flatulence', 'intestinal gas', 'stomach gas', 'abdominal gas', 'gassy feeling', 'farting', 'passing gas', 'gas buildup', 'GERD',
    'belching', 'burping', 'gas discomfort', 'gas pains', 'digestive gas', 'stomach is full', 'gassy stomach', 'trapped gas',
    'excessive gas', 'gas expulsion', 'intestinal discomfort', 'gas release', 'unwanted gas', 'gas in the stomach', 'passing wind'
],
'acidity': [
    'acid reflux', 'heartburn', 'sour stomach', 'acidic feeling', 'burning in chest', 'burning sensation in throat','heartburning',
    'stomach acid', 'acid burps', 'sour taste in mouth', 'regurgitation', 'upper abdominal burning',
    'acid in throat', 'stomach burning', 'gastric acid', 'acid buildup', 'acidic burping', 'throat burn',
    'reflux sensation', 'chest discomfort after eating', 'acid sensation', 'acidic regurgitation', 'acidic discomfort',
    'burning after meals', 'acid coming up', 'bitter taste in throat'
],

'indigestion': [
    'dyspepsia', 'digestive discomfort', 'fullness after eating', 'nausea after eating', 'acidic stomach','feeling of heaviness', 'difficulty digesting', 'food intolerance',
     'nothing is digested','not digesting', 'food not getting digested', 'indigested food', 'lack of digestion', 'digestion not happening', 'not being digested',
      'digestion problems', 'digestion problem', 'digestive problem', 'digestive problems', 'stomach upset', 'upset stomach', 'stomach is upset'
],

'nosebleed': [
    'epistaxis', 'bleeding from the nose', 'nasal hemorrhage', 'nose bleeding', 'bloody nose', 'hemorrhaging from the nose', 'nose blood flow',
    'spontaneous nosebleed', 'anterior nosebleed', 'posterior nosebleed', 'frequent nosebleeds', 'nosebleed episode', 'bleeding nostrils',
    'blood coming out from the nose', 'nasal bleeding', 'bloody discharge from the nose', 'nasal passage bleeding', 'nosebleed symptoms', 'internal nasal bleeding',
    'nose injury bleeding', 'blood coming out of nose', 'bloody nose'
],
'ear ringing': [
    'tinnitus', 'ringing in the ears', 'ear buzzing', 'ear noise', 'persistent ear sound', 'ear whistling', 'ear humming', 'sounds in the ears',
    'ear roaring', 'ringing sound in the ear', 'constant ringing', 'ear congestion', 'noises in the ear', 'buzzing in the ear', 'hissing in the ear',
    'whistling in the ear', 'high-pitched sound', 'low-pitched ear sound', 'phantom sounds', 'ear sensation', 'auditory disturbance', 'ear rings'
],

'urine issues': [
    'dark-colored urine', 'dark yellow urine', 'brown urine', 'amber-colored urine', 'tea-colored urine', 'concentrated urine', 'urine with strong color',
    'deep yellow urine', 'urine discoloration', 'darkened urine', 'urine with reddish tint', 'dark brown urine', 'urine with high concentration', 'cloudy urine',
    'urine with abnormal color', 'dark urine caused by medication', 'urine with high pigment', 'strong urine color', 'burning while passing urine',
    'urinary issues'
],

'blood in urine': [
    'hematuria', 'urinary blood', 'blood in the urine', 'blood while peeing', 'bleeding while peeing', 'blood with urine', 
   'hemorrhagic urine', 'urinary bleeding', 'presence of blood in urine', 'blood in the bladder','urine has blood','bloody urine', 'red urine',
    'bloody discharge in urine', 'urine with reddish tint','bleeding while peeing','urine has blood', 'blood with urine', 'bloody urine','urine had blood', 'blood in the urine',
    'visible blood in urine', 'microscopic hematuria','blood in the urinary tract'
],

'blood in stool': [
    'hematochezia', 'rectal bleeding', 'bloody stool', 'stool with blood', 'bright red blood in stool', 'blood in the stool', 'blood in the bowel movement',
    'blood-tinged stool', 'bloody feces', 'blood in feces', 'stool with reddish tint', 'blood in the stool sample', 'melena', 'dark tarry stool',
    'fecal blood', 'visible blood in stool', 'blood after bowel movement', 'stool with clots', 'bloody discharge from the rectum', 'abnormal stool color'
],
	
'high blood pressure': [
    'hypertension', 'elevated blood pressure', 'high BP', 'high arterial pressure', 'raised blood pressure', 'increased blood pressure',
    'high systolic pressure', 'high diastolic pressure', 'hypertensive condition', 'higher BP', 'higher blood pressure', 'BP is trending high',
    'BP is trending higher', 'high blood pressure disorder', 'abnormal blood pressure', 'hypertensive crisis', 'BP is getting high',
    'BP is going high', 'BP gone high', 'elevated BP', 'hypertensive state', 'BP is high', 'BP goes high', 'BP is getting high',
    'blood pressure is high', 'high BP', 'BP is coming high', 'BP showing up high', 'BP showing high', 'highest BP', 'BP is showing high',
    'my blood pressure is high', 'feeling pressure is high', 'BP feels high', 'my BP went up suddenly', 'blood pressure went up',
    'blood pressure rising', 'pressure in my arteries is high', 'high heart pressure', 'pressure reading is high', 'BP is above normal',
    'blood pressure is above average', 'feeling headache from high BP', 'feeling dizzy due to high blood pressure', 'feeling flushed from high BP',
    'BP getting higher', 'blood pressure is rising fast', 'pressure in veins is high', 'pressure in arteries rose', 'systolic pressure is high',
    'diastolic pressure is high', 'my blood pressure reads high', 'pressure numbers are high', 'heart pressure high', 'feeling symptoms of high blood pressure',
    'pressure has gone up', 'pressure level is high', 'pressure is dangerously high', 'high blood pressure episode', 'high BP symptoms',
    'rise in blood pressure', 'blood pressure high and causing headache', 'blood pressure high and causing dizziness',
    'pressure is too much', 'BP is too high', 'blood pressure higher than usual', 'pressure above healthy level',
    'blood pressure higher than normal', 'blood pressure is dangerously high', 'high BP making me feel unwell', 'high BP making me feel dizzy',
    'my blood pressure keeps rising', 'my blood pressure is too high', 'BP dangerously rising', 'BP dangerously high',
    'pressure high and causing symptoms', 'BP above baseline', 'blood pressure higher than expected', 'feeling symptoms from high BP',
    'high systolic and diastolic pressure', 'blood pressure rising suddenly', 'pressure spiking', 'pressure going dangerously high',
    'high pressure causing headache', 'feeling flushed because of high blood pressure', 'high BP causing dizziness',
    'BP higher than it should be', 'BP higher than normal range', 'heart pressure above normal', 'arterial pressure high'
],

'low blood pressure': [
    'hypotension', 'low BP', 'decreased blood pressure', 'low arterial pressure', 'reduced blood pressure', 'hypotensive condition',
    'low systolic pressure', 'low diastolic pressure', 'lower BP', 'lower blood pressure', 'BP is getting low', 'BP is going low',
    'BP gone low', 'BP is coming low', 'blood pressure drop', 'low cardiovascular pressure', 'inadequate blood pressure',
    'lowest BP', 'low blood pressure', 'BP is dropping', 'BP dropped', 'BP is low', 'BP showing low', 'BP is showing low',
    'my blood pressure is low', 'feeling dizzy because of low BP', 'BP feels low', 'BP dropped suddenly',
    'blood pressure went down', 'blood pressure falling', 'pressure in my arteries is low', 'low heart pressure',
    'pressure reading is low', 'BP is below normal', 'blood pressure is below average', 'feeling faint due to low BP',
    'lightheaded from low blood pressure', 'feeling weak from low BP', 'BP getting lower', 'blood pressure is dropping fast',
    'pressure in veins is low', 'pressure in arteries dropped', 'systolic pressure is low', 'diastolic pressure is low',
    'my blood pressure reads low', 'pressure numbers are low', 'heart pressure low', 'feeling symptoms of low blood pressure',
    'pressure has gone down', 'pressure level is low', 'pressure is dangerously low', 'low blood pressure episode',
    'low BP symptoms', 'drop in blood pressure', 'blood pressure low and causing dizziness', 'blood pressure low and causing faintness',
    'pressure is not enough', 'my BP is too low', 'blood pressure lower than usual', 'pressure below healthy level',
    'blood pressure lower than normal', 'blood pressure is dangerously low', 'low BP making me feel weak', 'low BP making me feel dizzy',
    'my blood pressure keeps dropping', 'my blood pressure is too low', 'BP dangerously dropping', 'BP dangerously low',
    'pressure low and causing symptoms', 'BP below baseline', 'blood pressure lower than expected', 'feeling symptoms from low BP',
    'low systolic and diastolic pressure', 'blood pressure falling suddenly', 'pressure bottoming out', 'pressure going dangerously low',
    'low pressure causing fainting', 'feeling faint because of low blood pressure', 'low BP causing lightheadedness',
    'BP lower than it should be', 'BP lower than normal range', 'heart pressure below normal', 'arterial pressure low'
],

'excessive thirst': [
    'polydipsia', 'intense thirst', 'uncontrollable thirst', 'extreme thirst', 'constant thirst', 'increased thirst', 'abnormal thirst', 'drinking more water', 'consuming more water',
    'compulsive thirst', 'thirsty all the time', 'unquenchable thirst', 'chronic thirst', 'intense desire to drink', 'frequent thirst', 'dehydration thirst','thirsty feeling',
    'abnormal fluid intake desire', 'thirst without relief', 'excessive fluid consumption', 'thirst due to dehydration', 'thirsty feeling', 'abnormal hydration needs','BP is getting low','BP is low'
],

'dehydration': [
    'fluid loss', 'water depletion', 'lack of hydration', 'electrolyte imbalance', 'insufficient water intake', 'dehydrating',
    'dehydrated state', 'water deficiency', 'reduced fluid levels', 'severe dehydration', 'mild dehydration', 'dehydration symptoms',
    'fluid imbalance', 'low body water', 'loss of body fluids', 'heat exhaustion', 'low hydration', 'hypohydration', 'water drained out'
],

'red eyes': [
    'eye redness', 'bloodshot eyes', 'conjunctival redness', 'inflamed eyes', 'eye irritation', 'eyes with blood vessels',
    'swollen eyes', 'sore eyes', 'tired eyes', 'watery eyes', 'eye inflammation', 'pink eye', 'eye congestion', 'eye discomfort', 'eyes looking inflamed',
    'redness in the eyes', 'burning eyes', 'allergic eyes', 'eyes with a reddish tint'
],

'ear discharge': [
    'otorrhea', 'ear fluid', 'ear drainage', 'pus from the ear', 'ear pus', 'ear infection discharge', 'fluid from the ear', 'ear secretion',
    'yellow ear discharge', 'green ear discharge', 'watery ear discharge', 'bloody ear discharge', 'ear mucus', 'crust in the ear', 'excessive ear fluid',
    'ear leakage', 'ear wax buildup', 'discharge from the ear canal', 'discharge from the middle ear', 'infection-related ear discharge', 'ear discharge after swimming',
    'ear drainage after injury', 'something coming out of ears','pus comes out from inside the ear','pus is coming out of the ear' 'pus from ear','ear pus''pus comes from ear',
    'pus comes from the ear','pus is coming from an ear','pus is coming from left ear','pus in ear','pus in the ear', 'something coming out of ears', 'something coming out of my ears'
],

'balance problem': [
    'vertigo', 'loss of balance', 'balance disorder', 'impaired balance', 'unsteady gait', 'lack of coordination', 'unsteadiness',
    'balance difficulty', 'feeling of instability', 'spatial disorientation', 'postural imbalance', 'equilibrium disturbance', 'feeling off-balance',
    'gait imbalance', 'disequilibrium', 'vestibular dysfunction', 'balance issues', 'vertiginous symptoms', 'coordination problems', 'stumbling', 'feeling lightheaded'
],

'irregular heartbeat': [
    'arrhythmia', 'abnormal heartbeat', 'heart palpitations', 'irregular pulse', 'heart rhythm disorder', 'uneven heartbeat', 'skipped heartbeat',
    'rapid heartbeat', 'slow heartbeat', 'tachycardia', 'bradycardia', 'atrial fibrillation', 'ventricular fibrillation', 'heart flutter', 'irregular heart rhythm',
    'heart irregularities', 'palpitations', 'fluttering heart', 'cardiac arrhythmia', 'dysrhythmia', 'irregular pulse rate', 'heartbeat irregularity','fast heartbeat',
    'irregular heart rate', 'heart pounding','heartbeat is late','heart beat is late','heartbeat is early','heart beat is early','late heart beat','late heartbeat','heartrate is fast','rapid heartrate',
    'pounding heart rate','pounding heartrate','rapid heart rate','rapid heartrate'
],

'fainting': [
    'syncope', 'passing out', 'loss of consciousness', 'blackout', 'going unconscious', 'faint', 'collapse', 'temporary unconsciousness',
    'fainted','feeling lightheaded', 'brief loss of consciousness',
    'head rush', 'staggering', 'loss of awareness', 'unconsciousness', 'momentary blackout', 'unconscious',
    'feeling woozy'
],

'nervousness': [
    'nervous tension', 'nervous energy', 'uneasiness', 'nervous feeling', 'worry', 'uneasy feeling', 'jitters', 'nervous anticipation', 'fearfulness', 'shakiness', 'edginess',
    'fidgeting', 'mental unease', 'trepidation', 'feeling on edge', 'worrying', 'nervous butterflies'
],

'panic attack': [
    'anxiety attack', 'nervous breakdown', 'stress attack', 'overwhelming fear', 'intense fear episode', 'fight-or-flight response', 'panic episode', 'emotional breakdown',
    'sudden panic', 'heart-pounding anxiety', 'fear attack', 'intense panic', 'acute stress response', 'terror attack', 'nervous episode',
    'severe panic', 'acute emotional distress', 'uncontrollable fear', 'chronic panic disorder'
],

'mood swing': [
    'emotional swing', 'mood fluctuation', 'emotional rollercoaster', 'mood shift', 'mood change', 'mood variation', 'mood disorder',
    'rapid mood change', 'emotional instability', 'mood instability', 'mood alteration', 'emotional shift', 'temper fluctuation',
    'emotional lability', 'mood fluctuations', 'unstable mood', 'irregular mood', 'affective swing', 'mood imbalance', 'emotional outbursts',
    'highs and lows', 'emotional extremes','mood is low','mood is very low', 'mood is very bad'
],

'difficulty concentrating': [
    'inability to focus', 'lack of focus', 'poor concentration', 'trouble focusing', 'concentration problems', 'distractibility',
    'difficulty paying attention', 'lack of mental clarity', 'difficulty staying focused', 'inattention', 'short attention span', 'mind wandering',
    'difficulty concentrating on tasks', 'poor attention span', 'difficulty maintaining focus', 'lack of mental focus', 'difficulty with concentration',
    'easily distracted', 'unable to focus', 'attention issues', 'concentration challenges', 'lack of concentration'
],

'lack of motivation': [
    'demotivated', 'low motivation', 'disinterest', 'lack of drive', 'lack of ambition', 'lack of initiative', 'apathy', 'unmotivated', 'no desire to work',
    'loss of drive', 'lack of enthusiasm', 'indifference', 'lack of determination', 'lack of purpose', 'loss of interest', 'lack of energy',
    'procrastination', 'lack of willpower', 'lack of focus', 'lack of passion', 'feeling uninspired', 'demotivation', 'lack of commitment', 'indifferent attitude'
],

'exhaustion': [
    'tiredness', 'weariness', 'drained', 'burnout', 'physical exhaustion', 'mental exhaustion', 'lack of energy',
    'overwhelming tiredness', 'depletion', 'lack of stamina', 'total exhaustion', 'exhausted feeling', 
    'drowsiness', 'wearing out', 'energy depletion','feeling drained', 'exhaustive tiredness', 'loss of energy',
    'sleep-deprived', 'exhausted', 'yawning', 'low energy', 'snoozy', 'droopy eyed', 'barely awake',
    'hard to stay awake', 'sleep craving', 'languid', 'wearied', 'brain fog',
    'bed ready', 'lazy eyed', 'unfocused from tiredness', 'nodding head', 'drifting off', 'slumberous', 'soporific', 'somnolent',
    'rest-seeking', 'near dozing', 'eyes struggling to stay open', 'unable to concentrate', 'dull from tiredness'
],

'fatigue': [
    'fatigue',
],

'sprain': [
    'ligament injury', 'joint sprain', 'ligament strain', 'stretched ligament', 'ligament tear',
    'sprained ligament', 'ligament damage'
],

'strain': [

    'soft tissue strain', 'overexertion', 'overworked muscle'
],

'arthritis': [
    'inflammatory arthritis', 'rheumatoid arthritis', 'osteoarthritis', 'degenerative joint disease',  'rheumatism',  'pain from arthritis',
    'arthralgia', 'chronic arthritis', 'autoimmune arthritis', 'psoriatic arthritis'

],

'gout': [
    'uric acid buildup', 'acute gout', 'chronic gout', 'gout attack', 'gouty inflammation', 'gouty attack',
    'painful gout episode', 'gouty swelling', 'gout in the foot', 'gout in the big toe', 'gouty condition', 'uric acid crystals', 'gouty joint disease'
],

'bone fracture': [
    'broken bone', 'bone break', 'fractured bone', 'cracked bone', 'bone crack', 'fracture', 'crack in my bone','crack in a bone','bone fracture',
    'stress fracture', 'hairline fracture', 'bone splinter','fracture in bone','crack in bone','bone has cracked','cracks in bone', 'bone cracked',
    'fractured limb', 'fractured bone segment', 'broken limb', 'broken bone segment', 'cracked bone injury', 'bone rupture', 'bone fracture symptoms',
    'fractured bone tissue', 'fracture of the bone', 'crack in bone', 'fractured'
],

'back bone issue': [
    'spinal problem', 'back bone pain', 'spinal condition', 'vertebral issue', 'spinal disorder', 'back injury', 'spinal misalignment', 'back bone is paining',
    'disc herniation', 'spinal injury', 'neck and back issues', 'spinal discomfort', 'lumbar pain', 'spinal cord issue', 'slipped disc', 'musculoskeletal disorder',
    'spinal health issue', 'postural problems', 'spondylosis', 'degenerative disc disease', 'spine misalignment', 'spinal deformity', 'spinal arthritis', 'spinal stenosis',
    'backbone issue'
],
'female issue': [
    'women’s health', 'gynecological issue', 'female reproductive health', 'PCOS', 'PCOD', 'endometriosis',
    'fibroids', 'ovarian cysts', 'vaginal infection', 'vaginal discharge', 
    'vaginal dryness', 'prolapsed uterus', 'birth control issues', 'female urinary issues',
    'pregnancy complications', 'white discharge', 'female issues', 'woman issue', 'women issue', 'woman issues',
    'women issues', 'vaginal itching', 'vaginal odor', 'ovulation pain', 'breast tenderness', 'breast lumps',
    'nipple discharge', 'breast pain', 'breast swelling', 'difficulty conceiving', 'itchy vulva', 'burning vulva'
   
],
'menopause': [
    'menopause','short menstrual cycles', 'menopausal','amenorrhea', 'masik dharm'
],

'caesarean section' : [ 'C section', 'cissarin','sea section','scissoring','caesaring', 'caesarean'],

'pregnancy' : ['pregnant','pregnate','childbirth', 'expecting a child', 'carrying a fetus', 'gestating', 'positive HCG test'],

'pediatric symptoms' : ['kid problems','pediatrics','child is unwell', 'child is facing issues', 'children health', 'child health','feeding problems',
                       'cry patterns', 'growth problems', 'refusal to breastfeed' , 'developmental delay', 'bowed legs', 'bedwetting', 'kids problem'
                       ],

'thyroid': [
    'hypothyroidism', 'hyperthyroidism', 'thyroid disorder', 'thyroid imbalance', 'underactive thyroid', 'overactive thyroid', 'goiter', 'thyroid dysfunction',
    'thyroid disease', 'thyroid cancer', 'thyroiditis', 'low thyroid function', 'high thyroid function', 'endocrine disorder', 'thyroid nodules', 'thyroid hormone imbalance',
    'TSH imbalance', 'thyroid problems', 'autoimmune thyroid disease', 'pituitary-thyroid dysfunction', 'thyroid testing'
],

'piles': [
    'hemorrhoids', 'anal piles', 'rectal swelling', 'internal hemorrhoids', 'external hemorrhoids',
    'hemorrhoidal disease', 'rectal discomfort', 'anal itching', 'anal bleeding', 'rectal bleeding', 'chronic hemorrhoids',
    'painful hemorrhoids', 'prolapsed hemorrhoids', 'thrombosed hemorrhoids', 'anal fissures', 'blood clots in hemorrhoids',
    'swollen hemorrhoids', 'anal prolapse', 'inflamed hemorrhoids', 'rectal irritation', 'constipation-related hemorrhoids',
    'itchy anus', 'hemorrhoid treatment', 'hemorrhoid relief'
],

'hearing loss': [
'loss of hearing', 'lost hearing', 'reduced hearing', 'impaired hearing', 'difficulty hearing', 'diminished hearing ability', 'deaf', 'cannot hear','no hearing',
'hearing impairment', 'hearing less', 'less hearing','low hearing','hearing low','hearing very low', 'not hearing', 'unable to hear', 'one ear not listening',
'hearing deficiency', 'blocked hearing', 'muffled hearing', 'ringing in ears', 'ear damage', 'auditory dysfunction', 'ear canal blockage', 'inner ear damage',
'hearing weakness', 'fading hearing', 'loss of sound perception', 'difficulty understanding speech', 'distorted hearing', 'ear drum damage', 'hearing sensitivity reduction',
'hearing clarity reduction', 'speech comprehension difficulty', 'auditory decline', 'inability to detect sound frequencies', 'ear trauma', 'ears not listening',
'hearing impairment due to illness', 'hearing degradation', 'low sound perception', 'high-frequency hearing loss', 'earwax blockage hearing loss', 'acoustic trauma',
'temporary auditory loss', 'chronic hearing damage','hearing decreased','decreased hearing', 'hearing less', 'loss of hearing','hearing loss'
],

'weight gain': [
'increase in weight', 'gain in body mass', 'weight gain', 'excess body weight', 'body mass increase', 'weight is increasing','weight increased','weight is more',
 'caloric surplus', 'fat accumulation', 'body fat increase', 'muscle mass gain', 'excess calorie intake', 'fat storage increase', 'gaining weight', 'gained weight',
'hormone-related fat storage', 'body composition change', 'gained weight', 'weight going up', 'weight fluctuating', 'gaining too much weight','getting fatter','got fat'
],

'weight fluctuation': ["weight's been fluctuating", 'weight has been fluctuating', 'fluctuating weight', 'weight change', 'weigh different', 'change in weight',
 'weight is different', 'weighing change', 'weight has changed','weight fluctuations'],

'skin burning': [
'burning feeling in skin', 'skin irritation', 'skin stinging', 'skin redness', 'skin inflammation', 'burning sensation in skin', 'skin discomfort', 'tingling burn',
'localized skin burn', 'skin heat sensation', 'raw skin feeling', 'skin hypersensitivity', 'sunburn', 'chemical burn', 'skin scorching', 'skin sensitivity to touch',
'prickling skin sensation', 'hot skin feeling', 'burning skin pain', 'skin abrasion burn', 'nerve-related burning', 'itchy burning skin', 'skin damage from burn',
'intense burning sensation', 'surface skin burn', 'skin blistering', 'burned skin surface', 'burning sensation on the skin', 'burning sensation on the skin',
'red inflamed skin', 'skin discomfort from heat', 'skin chafing burn', 'sensitive skin after burn', 'burning sensation in the skin',
'stinging skin pain', 'skin burn from chemicals', 'skin damage sensation', 'skin peeling from burn', 
'lingering skin burn', 'burnt skin tenderness', 'skin hot spot'
],

'itching': [
'skin itching', 'pruritus', 'itchy sensation', 'skin irritation','itchy rash','itching', 'itchy',
'burning itch', 'itching with redness', 'itching from dryness', 'irritated skin itch', 'tickling skin sensation',
'itchy skin bumps', 'itchy welts', 'itchy hives', 'skin crawling sensation', 'itchy blisters', 'itchiness'
],

'injury': [
'injured', 'physical injury', 'bodily harm', 'tissue damage', 'sports injury', 'accidental injury', 'fallen from stairs',
'cut', 'abrasion', 'laceration', 'contusion', 'injuries','injure', 'fell down from stairs','fell down'
],

'jaundice': [
'icterus', 'jaundiced appearance','john dice','johnlist','john list','john diskey','john dries'
],

'sleepy': [
'sleepy', 'falling asleep', 'fallen asleep','feeling sleepy', 'sleep problems'
],

'asthma': ['reactive airway disease', 'hyperresponsive airway disease', 'asthmatic condition', 'asthmas', 'asthama','whistling sound while breathing'],

'pneumonia': ['lung infection','alveolar infection'],

'sugar': ['sugars', 'blood sugar', 'hyperglycemia', 'hypoglycemia'],

'tingling': ['tingling sensation', 'pins and needles', 'prickling sensation', 'buzzing sensation',
              'electrical sensation'],

'difficulty speaking': [
    'trouble speaking', 'speech difficulty', 'slurred speech', 'unclear speech', 'impaired speech',
    'problems with speech', 'inability to speak clearly', 'difficulty forming words', 'trouble articulating words',
    'speech impairment', 'difficulty talking', 'trouble talking', 'loss of speech', 'sudden speech difficulty',
    'speech problems after stroke', 
    'difficulty finding words', 'difficulty with verbal communication', 'stuttering', 'stammering',
    'broken speech', 'halting speech', 'speech delay', 'difficulty producing speech sounds',
    'raspy voice and trouble speaking', 'difficulty speaking when tired', 'trouble talking after seizure',
    'difficulty pronouncing words', 'difficulty speaking under stress', 'slow speech', 'garbled speech',
    'difficulty with fluent speech', 'disorganized speech', 
    'speech changes', 'difficulty initiating speech', 'trouble expressing thoughts verbally',
    'speech loss', 'difficulty speaking with drooping face'
],

'more hungry': [
    'increased hunger', 'excessive hunger', 'extreme hunger', 'constant hunger', 'unusual hunger',
    'frequent hunger', 'intense hunger', 'never feeling full', 'always hungry', 'feeling hungrier than usual',
    'ravenous appetite', 'uncontrollable hunger', 'increased appetite', 'heightened appetite',
    'overeating due to hunger', 'persistent hunger', 'craving food all the time', 'hungry shortly after eating',
    'hunger that doesn’t go away', 'sudden increase in appetite', 'strong desire to eat', 
    'feeling hungry', 'unable to satisfy hunger', 'eating more',
    'urge to eat constantly', 'insatiable hunger', 'always needing to snack', 'hungry despite eating enough',
    'eating frequently due to hunger', 'waking up hungry', 'nighttime hunger', 'excessive food cravings',
    'hunger pangs more often', 'increased hunger after exercise', 'increased hunger from medication',
    'hunger caused by blood sugar drops', 'hunger due to stress', 'hunger from emotional eating','hungry','eager to eat more',
    'more hunger than normal', 'overeating due to being hungrier'
],

'seizures': [
    'seizure', 'seizure episode', 'epileptic episode',
    'convulsions', 'fits', 'fitting episode', 'sudden convulsion', 'uncontrolled shaking',
    'body shaking episode', 'jerking movements', 'loss of consciousness with shaking', 
    'sudden blackout with convulsions', 'electrical storm in the brain', 'shaking episode without warning',
    'sudden onset of convulsions', 'temporary loss of awareness', 'involuntary body movement'
],

'dysentery': [
    'dysentery', 'diarrhea with blood', 'diarrhea with mucus', 'severe intestinal distress'
],
'hiccups': [
    'hiccoughs', 'jerking', 'involuntary hiccups', 'diaphragm spasms', 'gasping', 'hiccuping',
    'jerky breathing', 'hiccup reflex', 'repetitive hiccups'
],

'obesity': [
    'obese', 'high body mass index (BMI)','fatty tissue buildup', 'high levels of body fat', 'weight-related health issues',
    'BMI is higher', 'high BMI', 'BMI excess'
],

'ulcers': [
    'ulcerations', 'raw spots', 'skin ulcers', 'mucosal ulcers', 'internal ulcers',
    'gastric ulcers', 'peptic ulcers', 'duodenal ulcers', 'stomach ulcers', 'mouth ulcers',
    'oral ulcers', 'canker sores', 'pressure ulcers', 'bedsores', 'decubitus ulcers'
],

'brittle nails': [
    'weak nails', 'fragile nails', 'thin nails', 'breaking nails', 'chipped nails', 'flaky nails', 'easily broken nails',
    'damaged nails', 'dry nails', 'nail fragility', 'brittle fingernails', 'brittle toenails', 'nail breakage', 'nail weakness', 
    'nails that crack easily', 'nails prone to breaking'
],

'malaria': [
    'malarial infection', 'malarial fever', 'mosquito-borne disease', 'mosquito-related fever', 'vector-borne parasitic disease', 'protozoan infection'
   
],

'dengue': [
    'dengue fever', 'mosquito-borne illness', 'Aedes mosquito infection', 'mosquito-transmitted disease'
],

'covid': [
    'covid-19', 'coronavirus', 'corona', 'corona virus', 'sars-cov-2 infection', 'pandemic virus', 'covid outbreak'
],

'hiv': [
    'human immunodeficiency virus', 'HIV-positive', 'HIV', 'HIV/AIDS', 'acquired immunodeficiency virus'
],

'typhoid': [
    'typhoid fever', 'enteric fever', 'Salmonella typhi infection', 'waterborne bacterial infection', 'fever from contaminated water'
],

'chickenpox': [
    'varicella', 'varicella infection', 'chicken pox', 'varicella-zoster virus', 'viral exanthem'
],
'kidney issue': [
    'kidney disease', 'acute kidney injury', 'kidney stones', 'renal failure', 'nephritis', 'glomerulonephritis',
    'pyelonephritis', 'urinary tract infection', 'kidney infection', 'hydronephrosis', 'kidney fail',
    'high creatinine', 'low kidney function', 'kidney transplant', 'renal cysts', 'electrolyte imbalance', 'nephropathy'
],

'wound': [
    'laceration', 'abrasion', 'open wound',
    'skin break', 'gash', 'lesion', 'puncture wound', 'tear in skin'
],

'bruises': [
    'contusions', 'black and blue marks', 'skin discoloration', 'hematoma', 'bruising',
    'purple marks', 'banged up', 'bruised skin', 'minor bleeding under skin','bruises',
    'bluish patches','blue marks on skin', 'black marks on skin', 'bruise', 'bruised'
],
'cold intolerance': [
    'sensitivity to cold', 'discomfort in cold temperatures', 'feeling cold easily', 'low tolerance to cold',
    'cold sensitivity', 'hypersensitivity to cold', "can't tolerate cold", 
    'intolerance to cold weather', 'cold discomfort', 'cold hypersensitivity', 'decreased cold tolerance', 'thermoregulatory dysfunction',
    'abnormal cold sensation', 'excessive response to cold', 'shivering easily', 'overly sensitive to temperature drops'
],
'goiter': [
    'neck swelling', 'thyroid swelling', 'thyroid gland enlargement',
    'bulging thyroid', 'neck lump', 'enlarged neck gland', 'neck enlargement',
    'swollen neck gland', 'neck protuberance'
],
'slow reflexes': [
    'delayed reflexes', 'sluggish reflexes', 'reduced reflex speed', 'impaired reflexes', 'slow reaction time', 'delayed response', 'reflex is slow'
    'slow neurological responses', 'poor reflexes', 'delayed nerve response', 'slowed reflex action', 'decreased reflex speed', 'slow reflex',
    'delayed motor response', 'slow sensorimotor reaction', 'reflex sluggishness', 'impaired reaction time', 'slow response time', 'reflexes are slow'
],
'male reproductive issues': [
    'erectile dysfunction', 'impotence', "can’t get an erection", 'can’t maintain erection', 'loss of libido in men',
    'problems getting hard', 'weak erection', 'loss of erection', 'low sperm count', 'male infertility', 'testicular pain', 'pain in testicles',
    'swollen testicles', 'testicle swelling', 'lump in testicle', 'testicular discomfort', 'shrinkage of testicles', 'small testicles',
    'testicles feel different', 'pain during ejaculation', 'painful ejaculation', 'blood in semen', 'reduced semen volume', 'ejaculation problems', 
    'delayed ejaculation', 'premature ejaculation', "can’t ejaculate", 'retrograde ejaculation', 'no semen during orgasm', 'testicular tightness',
    'genital numbness in men', 'scrotal pain', 'pain in scrotum', 'penis pain', 'penis swelling', 'male genital discomfort', 'prostate issues',
    'enlarged prostate', 'prostatitis', 'sexual dysfunction in men', 'male reproductive health concerns'
],
'female reproductive issues': [
    'ovarian pain', 'pain in ovaries', 'female infertility', 'difficulty getting pregnant', 'trouble conceiving',
    'recurrent miscarriages', 'ectopic pregnancy', 'pain during sex for women', 'painful intercourse','low sex drive in women', 
    'loss of libido in women', 'hormonal imbalance in women', 'bleeding after sex', 'vaginal bleeding after intercourse', 
    'female reproductive health concerns', 'female infertility'
],
'dandruff': [
    'flaky scalp', 'scalp flakes', 'white flakes in hair', 'dry scalp flakes', 'itchy scalp flakes', 'scalp shedding',
    'flaking skin on scalp', 'scalp dryness', 'dry scalp', 'peeling scalp skin', 'white flakes on head', 
    'itchy flaky scalp', 'seborrheic flakes', 'scalp irritation with flakes', 'skin flakes on scalp',  'dead skin flakes on head',
    'visible scalp flakes', 'dead skin flakes in hair', 'flaky dandruff', 'scalp scaling', 'mild seborrheic dermatitis'
],

'blister': ['blister','blisters','blistering']



   }

# ------------------------------------------------------------------ #
# ----------------------- Followup Question ------------------------ #
# ------------------------------------------------------------------ #

symptom_followup_questions = {

  "acidity": [

    {
      "hi": "आपको हार्टबर्न या अम्लीय पुन: प्रवाह (acid reflux) कितनी बार होता है?",
      "en": "How often do you experience heartburn or acid reflux?",
      "category": "heartburn",
      "symptom": "acidity",
      "risk_factor": False,    },
     {
      "hi": "क्या आपको पेट में जलन या जलती हुई अनुभूति हो रही है?",
    "en": "Are you experiencing burning sensations in your stomach?",
      "category": "burning_sensation_with_heartburn",
      "symptom": "acidity",
      "risk_factor": False,    },
        {
      "hi": "क्या आपको अन्य कोई लक्षण जैसे कि उल्टी, पाचन में असुविधा या निगलने में कठिनाई महसूस हो रही है?",
    "en": "Do you experience any other symptoms, such as nausea, regurgitation, or difficulty swallowing?",
      "category": "heartburn",
      "symptom": "acidity",
      "risk_factor": False,    },
{
      "hi": "लक्षणों को क्या ट्रिगर करता है या बिगाड़ता है (जैसे कि कुछ खाद्य पदार्थ, लेट जाना, तनाव)?",
      "en": "What triggers or worsens the symptoms (e.g., certain foods, lying down, stress)?",
      "category": "heartburn",
      "symptom": "acidity",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके आहार, वजन, या जीवनशैली में हाल ही में कोई बदलाव हुआ है?",
      "en": "Have you had any changes in your diet, weight, or lifestyle recently?",
      "category": "dietary changes",
      "symptom": "acidity",
      "risk_factor": False,    },
  ],

  "weakness": [
      {
      "hi": "क्या आपको थकान महसूस होती है?",
      "en": "Do you feel fatigue? ", 
      "category": "weakness",
      "symptom": "weakness",
      "risk_factor": False,    },
    {
        "hi": "क्या आप को नसों या मांसपेशियों से जुड़ी कोई पुरानी समस्या है?",
        "en": "Do you have any chronic nerve or muscle-related condition?",
        "category": "limb_weakness_neuro_muscular_history",
        "symptom": None,
        "risk_factor": True
    }
  ],

  "headache": [
    {
      "hi": "क्या आपका सिरदर्द लगातार है या बीच-बीच में आता है?",
      "en": "Is your headache constant or intermittent?",
      "category": "headache_type",
      "symptom": None,
      "risk_factor": False,    },
    
    {
      "hi": "क्या सिरदर्द का कोई विशिष्ट स्थान है?",
      "en": "Is there a specific location where you feel the headache?",
      "category": "location_specific",
      "symptom": "Location-specific headache",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको ध्वनि या रोशनी से संवेदनशीलता है साथ ही सिरदर्द?",
       "en": "Do you have sensitivity to sound or light along with headache?",
      "category": "sensory_sensitivity",
      "symptom": "Sensitivity to sound or light",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको तनाव है साथ ही सिरदर्द?",
     "en": "Are you under stress along with headache?",
      "category": "stress_headache",
      "symptom": "Stress-related headache",
      "risk_factor": False,    },
{
      "hi": "क्या सिरदर्द की तीव्रता बढ़ रही है?",
      "en": "Is the intensity of your headache increasing?",
      "category": "intensity_increase",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या सिरदर्द की शुरुआत अचानक हुई थी या धीरे-धीरे?",
      "en": "Did the headache start suddenly or gradually?",
      "category": "onset",
      "symptom": None,
      "risk_factor": False,    },
  ],
  "nausea": [
       {
      "hi": "क्या आपको पेट में दर्द हो रहा है साथ ही मतली?",
      "en": "Are you experiencing abdominal pain along with nausea?",
      "category": "abdominal_pain_nausea",
      "symptom": "abdominal_pain_nausea",
      "risk_factor": False,    },
 {
      "hi": "क्या आपको उल्टी हो रही है?",
     "en": "Are you vomiting?",
      "category": "vomiting",
      "symptom": "vomiting",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको लगातार मतली महसूस हो रही है?",
      "en": "Are you experiencing constant nausea?",
      "category": "constant_nausea",
      "symptom": None,
      "risk_factor": False,    },
	{
      "hi": "क्या आपको खाने के बाद मतली होती है?",
      "en": "Do you feel nauseous after eating?",
      "category": "postprandial_nausea",
      "symptom": "Postprandial nausea",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको सिरदर्द है साथ ही मतली?",
      "en": "Do you have headaches along with nausea?",
      "category": "headache_nausea",
      "symptom": "Headache",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको कोई चक्कर आ रहे हैं साथ ही मतली?",
      "en": "Are you feeling dizzy along with nausea?",
      "category": "dizziness_nausea",
      "symptom": "Dizziness",
      "risk_factor": False,    },

  ],

 "congestion": [
  {
    "hi": "क्या आपकी नाक बह रही है?",
  "en": "Do you have a runny nose?",
    "category": "runny_nose",
    "symptom": "Runny nose",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको गले में खराश है साथ ही नाक बंद है?",
   "en": "Do you have a sore throat along with nasal congestion?",
    "category": "sore_throat_congestion",
    "symptom": "Sore throat with congestion",
    "risk_factor": False,
  },

  {
    "hi": "क्या आपकी आवाज़ भारी लग रही है?",
  "en": "Does your voice sound congested or muffled?",
    "category": "voice_congestion",
    "symptom": "Voice congestion",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपकी नाक से बदबू आ रही है या गंध नहीं आ रही?",
  "en": "Are you experiencing a bad smell or loss of smell through your nose?",
    "category": "loss_of_smell",
    "symptom": "Loss or change in smell",
    "risk_factor": False,
  },
{
    "hi": "क्या आपकी नाक में दबाव या जकड़न महसूस हो रही है?",
    "en": "Do you feel pressure or tightness in your nasal passages?",
    "category": "nasal_pressure",
    "symptom": "Nasal pressure or tightness",
    "risk_factor": False,
  },

  {
    "hi": "क्या आपको सुबह उठने पर नाक में ज्यादा जकड़न महसूस होती है?",
    "en": "Do you feel more nasal congestion in the mornings?",
    "category": "morning_congestion",
    "symptom": "Morning nasal congestion",
    "risk_factor": False,
  },
],
 
  "dizziness": [
    {
      "hi": "क्या चक्कर आना अचानक शुरू हुआ था या धीरे-धीरे?",
    "en": "Did the dizziness start suddenly or gradually?",
      "category": "dizziness_onset",
      "symptom": None,
      "risk_factor": False,    },
    {
  "hi": "क्या आप चलते वक्त संतुलन खो रहे हैं?",
  "en": "Are you losing your balance while moving?",
  "category": "balance_issues",
  "symptom": "Balance issues",
  "risk_factor": False,    },

{
      "hi": "क्या चक्कर आना चलने या खड़े होने पर बढ़ता है?",
     "en": "Does the dizziness increase when walking or standing?",
      "category": "position_related_dizziness",
      "symptom": "Position-related dizziness",
      "risk_factor": False,    },
    

    {
      "hi": "क्या आपको सिरदर्द हो रहा है साथ में चक्कर आना?",
      "en": "Are you having headaches along with dizziness?",
      "category": "headache_dizziness",
      "symptom": "headache",
      "risk_factor": False,    },
{
      "hi": "क्या चक्कर आने के साथ मतली या उल्टी हो रही है?",
      "en": "Are you experiencing nausea or vomiting along with dizziness?",
      "category": "dizziness_nausea_vomiting",
      "symptom": None,
      "risk_factor": False,    },
    
  ],
  "yellow eyes": [
    {
      "hi": "क्या आपके आंखों का रंग पीला हो गया है?",
      "en": "Have your eyes turned yellow?",
      "category": "jaundice_eye",
      "symptom": "Jaundice in eyes",
      "risk_factor": False,    },
    {
      "hi": "क्या आपकी त्वचा भी पीली हो गई है?",
     "en": "Has your skin also turned yellow?",
      "category": "jaundice_skin",
      "symptom": "Jaundice in skin",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके मूत्र का रंग गहरा हो गया है?",
    "en": "Has the color of your urine become darker?",
      "category": "dark_urine",
      "symptom": "Dark urine",
      "risk_factor": False,    },
    {
"hi": "क्या आपको पेट में दर्द के साथ पीली आँखें हैं?",
  "en": "Do you have abdominal pain along with yellow eyes?",
      "category": "abdominal_pain",
      "symptom": "abdominal pain",
      "risk_factor": False,    },
    {
      "hi": "क्या आपकी आँखों में जलन हो रही है?",
     "en": "Are your eyes feeling itchy along with yellowing?",
      "category": "itchy_eyes",
      "symptom": "Itchy eyes",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको थकान महसूस हो रही है साथ में पीली आँखें?",
      "en": "Are you feeling fatigued along with yellow eyes?",
      "category": "fatigue_jaundice",
      "symptom": "Fatigue with jaundice",
      "risk_factor": False,    },
  ],

  "fever": [
    {
      "hi": "क्या आपका बुखार लगातार है या बीच-बीच में आता है?",
     "en": "Is your fever constant or intermittent?",
      "category": "fever_type",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या आपको ठंड लग रही है?",
      "en": "Are you experiencing any chills?",
      "category": "chills",
      "symptom": "chills",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको रात में पसीना आता है?",
     "en": "Do you experience night sweats?",
      "category": "night_sweats",
      "symptom": "night sweats",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको सिरदर्द है?",
      "en": "Are you experiencing headaches?",
      "category": "headache",
      "symptom": "headache",
      "risk_factor": False,    },
{
      "hi": "क्या आपका तापमान सामान्य से अधिक है?",
      "en": "Is your temperature higher than normal?",
      "category": "high_temperature",
      "symptom": "high temperature",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको भूख कम लग रही है?",
      "en": "Are you experiencing loss of appetite?",
      "category": "loss_of_appetite",
      "symptom": "loss of appetite",
      "risk_factor": False,    },
  ],

  "cough": [
    {
      "hi": "क्या आपकी खांसी सूखी है या बलगम के साथ?",
    "en": "Is your cough dry or with phlegm?",
      "category": "cough_type",
      "symptom": None,
      "risk_factor": False,    },
    {

      "hi": "क्या आपके खांसी के साथ बुखार है?",
     "en": "Do you have a fever along with your cough?",
      "category": "fever",
      "symptom": "fever",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको सांस लेने में कठिनाई हो रही है?",
     "en": "Are you experiencing difficulty breathing?",
      "category": "breathing",
      "symptom": "shortness of breath",
      "risk_factor": False,    },
{
      "hi": "क्या आपको सीने में दर्द है?",
    "en": "Are you experiencing chest pain?",
      "category": "chest_pain",
      "symptom": "chest pain",
      "risk_factor": False,    },
{
      "hi": "क्या आपको गले में खराश है?",
      "en": "Do you have a sore throat?",
      "category": "sore_throat",
      "symptom": "sore throat",
      "risk_factor": False,    },
    {
      "hi": "क्या आपकी खांसी रात में बढ़ जाती है?",
      "en": "Does your cough worsen at night?",
      "category": "time",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या आपकी आवाज़ बदल गई है?",
      "en": "Has your voice changed?",
      "category": "voice_change",
      "symptom": "broken voice",
      "risk_factor": False,    },
    {
      "hi": "क्या आपकी खांसी के साथ तेज सांस लेना शामिल है?",
      "en": "Does your cough include rapid breathing?",
      "category": "rapid_breathing",
      "symptom": "Rapid breathing",
      "risk_factor": False,    },
  ],

  "constipation": [
    {
      "hi": "क्या कब्ज के साथ पेट में दर्द है?",
      "en": "Are you experiencing abdominal pain along with constipation?",
      "category": "abdominal_pain",
      "symptom": "abdominal pain",
      "risk_factor": False,    },
    {
      "hi": "क्या आप नियमित रूप से पानी पीते हैं?",
      "en": "Are you drinking enough water regularly?",
      "category": "hydration",
      "symptom": None,
      "risk_factor": False,    },
   {
  "hi": "क्या आप रोज़ाना फल और सब्ज़ियां खाते हैं?",
  "en": "Do you eat vegetables and fruits daily?",
  "category": "daily_diet_vegetables_fruits",
  "symptom": None,
  "risk_factor": True,
    },
  {
  "hi": "क्या आपको थायरॉयड की समस्या या मधुमेह (डायबिटीज़) है?",
  "en": "Do you have thyroid issues or diabetes?",
  "category": "thyroid_or_diabetes",
  "symptom": None,
  "risk_factor": True,
},
    {
      "hi": "क्या आप नियमित रूप से व्यायाम करते हैं?",
      "en": "Do you exercise regularly?",
      "category": "exercise",
      "symptom": None,
      "risk_factor": False,    },
  ],

  "sore throat": [
{
      "hi": "क्या आपको निगलने में कठिनाई हो रही है?",
      "en": "Are you having difficulty swallowing?",
      "category": "difficulty_swallowing",
      "symptom": "difficulty swallowing",
      "risk_factor": False,    },
    
     {
      "hi": "क्या आपकी आवाज़ में परिवर्तन आया है?",
      "en": "Has there been any change in your voice?",
      "category": "voice_changes",
      "symptom": "broken voice",
      "risk_factor": False,    },
     {
  "hi": "क्या गले में दर्द के साथ बुखार भी है?",
  "en": "Do you have a fever along with a sore throat?",
  "category": "fever",
  "symptom": "fever",
  "risk_factor": False,
},
{
  "hi": "क्या गले में दर्द के साथ बहती नाक भी है?",
  "en": "Do you have a runny nose along with a sore throat?",
  "category": "runny_nose",
  "symptom": "runny nose",
  "risk_factor": False,
},
   {
      "hi": "क्या गले में दर्द के साथ सूजन भी है?",
      "en": "Is there any swelling along with your sore throat?",
      "category": "swelling",
      "symptom": "swelling",
      "risk_factor": False,    },
    {
      "hi": "क्या आपकी गले में दर्द लगातार है या आता-जाता है?",
      "en": "Is your sore throat constant or does it come and go?",
      "category": "intermittent_pain",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या आपको गले में जलन महसूस हो रही है?",
      "en": "Are you experiencing any burning sensation in your throat?",
      "category": "burning_sensation",
      "symptom": "burning throat",
      "risk_factor": False,    },
  ],

  "diarrhea": [
    {
      "hi": "क्या दस्त के साथ पेट में दर्द है?",
      "en": "Do you have abdominal pain along with diarrhea?",
      "category": "abdominal_pain",
      "symptom": "abdominal pain",
      "risk_factor": False,    },   
 {
      "hi": "क्या आपको दस्त लगातार हो रहे हैं या कभी-कभी?",
      "en": "Are you experiencing diarrhea continuously or intermittently?",
      "category": "intermittent_diarrea",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या आपको दस्त के साथ उल्टी भी हो रही है?",
      "en": "Are you also experiencing vomiting along with diarrhea?",
      "category": "vomiting",
      "symptom": "vomiting",
      "risk_factor": False,    },
    {
      "hi": "क्या दस्त के साथ बुखार भी है?",
      "en": "Is there a fever along with diarrhea?",
      "category": "fever",
      "symptom": "fever",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको दस्त के साथ कोई अन्य लक्षण महसूस हो रहे हैं?",
      "en": "Are you experiencing any other symptoms along with diarrhea?",
      "category": "other_symptoms",
      "symptom": None,
      "risk_factor": False,    },
{
      "hi": "क्या आप अपने शरीर से अधिक पानी खो रहे हैं?",
      "en": "Are you losing more water from your body?",
      "category": "dehydration",
      "symptom": None,
      "risk_factor": False,    },
  ],

  "vomiting": [
{
      "hi": "क्या उल्टी के साथ पेट में दर्द है?",
      "en": "Do you have abdominal pain along with vomiting?",
      "category": "abdominal_pain",
      "symptom": "abdominal pain",
      "risk_factor": False,    },    
{
  "hi": "पिछले 24 घंटों में आपको कितनी बार उल्टी हुई?",
  "en": "How many episodes of vomiting did you have in the last 24 hours?",
  "category": "vomiting",
  "symptom": "vomiting",
  "risk_factor": False,
},
 {
      "hi": "क्या उल्टी के साथ बुखार भी है?",
      "en": "Is there a fever along with vomiting?",
      "category": "fever",
      "symptom": "fever",
      "risk_factor": False,    },
  {
  "hi": "क्या उल्टी के कारण आप कुछ भी खा या पी नहीं पा रहे हैं?",
  "en": "Are you unable to eat or drink anything due to vomiting?",
  "category": "vomiting",
  "symptom": "vomiting",
  "risk_factor": False,
},
  ],

  "chills": [
    {
      "hi": "क्या आपके ठंडक के साथ बुखार भी है?",
     "en": "Do you have a fever along with chills?",
      "category": "fever",
      "symptom": "fever",
      "risk_factor": False,    },
    {
      "hi": "क्या ठंडक की अनुभूति लगातार है या आता-जाता है?",
      "en": "Is your feeling of chills constant or intermittent?",
      "category": "intermittent_chills",
      "symptom": "chills",
      "risk_factor": False,    },
    {
      "hi": "क्या ठंडक के साथ कमजोरी महसूस हो रही है?",
      "en": "Are you experiencing any weakness along with chills?",
      "category": "weakness",
      "symptom": "weakness",
      "risk_factor": False,    },
    {
      "hi": "क्या ठंडक की अनुभूति किसी विशेष समय पर अधिक होती है?",
      "en": "Do you feel chills more at any specific time?",
      "category": "time_related_chills",
      "symptom": None,
      "risk_factor": False,    },
  ],

  "swelling": [
 
    {
      "hi": "क्या सूजन के साथ दर्द भी है?",
      "en": "Is there any pain along with swelling?",
      "category": "pain_with_swelling",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या सूजन लगातार है या आता-जाता है?",
      "en": "Is the swelling constant or does it come and go?",
      "category": "intermittent_swelling",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या सूजन के कारण त्वचा में कोई परिवर्तन हो रहा है?",
      "en": "Is there any change in the skin due to swelling?",
      "category": "skin_changes_with_swelling",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या सूजन के साथ त्वचा की लालिमा भी है?",
      "en": "Is there redness of the skin along with swelling?",
      "category": "redness_with_swelling",
      "symptom": "redness",
      "risk_factor": False,    },
  ],

  "infection": [
    {
      "hi": "क्या संक्रमण के कारण आपको त्वचा में लालिमा आ रही है?",
      "en": "Is there any redness in your skin due to the infection?",
      "category": "skin_redness",
      "symptom": "redness",
      "risk_factor": False,    },   
 {
      "hi": "क्या संक्रमण के कारण आपको किसी विशेष हिस्से में दर्द हो रहा है?",
      "en": "Are you experiencing pain in any specific area due to the infection?",
      "category": "localized_pain",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या संक्रमण के साथ सूजन भी है?",
      "en": "Is there any swelling along with the infection?",
      "category": "swelling",
      "symptom": "swelling",
      "risk_factor": False,    },
    {
      "hi": "क्या संक्रमण के कारण आपको कमजोरी महसूस हो रही है?",
      "en": "Are you feeling weak due to the infection?",
      "category": "weakness",
      "symptom": "weakness",
      "risk_factor": False,    },
  ],

  "depression": [
{
      "hi": "क्या आपकी रुचियों में कमी आई है?",
      "en": "Have you lost interest in your usual activities?",
      "category": "loss_of_interest",
      "symptom": None,
      "risk_factor": False,    },    
    {
      "hi": "क्या आपको खुद को नीचा महसूस होता है?",
      "en": "Do you feel worthless?",
      "category": "worthlessness",
      "symptom": None,
      "risk_factor": False,    },

{
      "hi": "क्या आपको उदासी या निराशा महसूस हो रही है?",
      "en": "Are you feeling sad or hopeless?",
      "category": "sadness",
      "symptom": None,
      "risk_factor": False,    },
{
      "hi": "क्या आपकी नींद में कोई समस्या है?",
      "en": "Are you having any problems with your sleep?",
      "category": "sleep_problems",
      "symptom": "insomnia",
      "risk_factor": False,    },

    {
      "hi": "क्या आपको निर्णय लेने में कठिनाई हो रही है?",
      "en": "Are you having difficulty making decisions?",
      "category": "decision_difficulty",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या आपको खुद को चोट पहुँचाने का विचार आता है?",
      "en": "Are you having thoughts of harming yourself?",
      "category": "self_harm_thoughts",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या आपको ऊर्जा की कमी महसूस हो रही है?",
      "en": "Are you feeling a lack of energy?",
      "category": "energy_deficit",
      "symptom": "fatigue",
      "risk_factor": False,    },
  ],

  "diabetes": [
    {
      "hi": "क्या आपको बार-बार पेशाब आ रहा है?",
      "en": "Are you urinating frequently?",
      "category": "frequent_urination",
      "symptom": "urinary frequency",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके घुटनों या पैरों में सुन्नता है?",
      "en": "Are you experiencing numbness in your knees or feet?",
      "category": "numbness",
      "symptom": "numbness",
      "risk_factor": False,    },
{
      "hi": "क्या आपको बहुत भूख लग रही है?",
      "en": "Are you feeling very hungry?",
      "category": "increased_appetite",
      "symptom": "increased appetite",
      "risk_factor": False,    },

    {
     "hi": "क्या आपको अत्यधिक प्यास लग रही है?",
      "en": "Are you feeling excessively thirsty?",
      "category": "excessive_thirst",
      "symptom": "excessive thirst",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके वजन में अचानक कमी आई है?",
      "en": "Have you experienced sudden weight loss?",
      "category": "sudden_weight_loss",
      "symptom": "weight loss",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको ऊँची या नीची रक्तचाप की समस्या है?",
      "en": "Do you have high or low blood pressure?",
      "category": "blood_pressure",
      "symptom": None,
      "risk_factor": False,    },
  ], 

  "allergy": [
    {
      "hi": "क्या आपकी त्वचा में खुजली या लालिमा है?",
      "en": "Do you have itching or redness on your skin?",
      "category": "skin_allergy_symptoms",
      "symptom": "itching",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके आंखों में सूजन या जलन है?",
      "en": "Do you have swelling or irritation in your eyes?",
      "category": "eye_allergy_symptoms",
      "symptom": "itchy eyes",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके लक्षण किसी खास मौसम या वातावरण में अधिक होते हैं?",
      "en": "Do your symptoms worsen in certain seasons or environments?",
      "category": "environmental_allergy_triggers",
      "symptom": None,
      "risk_factor": False,    },
{
      "hi": "क्या आपको किसी विशेष चीज़ से एलर्जी है?",
      "en": "Do you have allergies to any specific substance?",
      "category": "specific_allergy",
      "symptom": None,
      "risk_factor": False,    },
     {
      "hi": "क्या आपको गले में खुजली या सूजन महसूस हो रही है?",
      "en": "Are you feeling itchiness or swelling in your throat?",
      "category": "throat_allergy_symptoms",
      "symptom": None,
      "risk_factor": False,    },   
  ],

 "high blood pressure": [
  {
    "hi": "क्या आप सिरदर्द, चक्कर, छाती में दर्द, या सांस की तकलीफ जैसे लक्षण महसूस कर रहे हैं?",
    "en": "Are you experiencing any symptoms like headaches, dizziness, chest pain, or shortness of breath?",
    "category": "high blood pressure",
    "symptom": None,
    "risk_factor": False,
  },
  
{
    "hi": "आपने आखिरी बार कब अपना रक्तचाप जांचवाया था, और उसके परिणाम क्या थे?",
    "en": "When was the last time you had your blood pressure checked, and what were the results?",
    "category": "high blood pressure",
    "symptom": "high blood pressure",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपके परिवार में उच्च रक्तचाप, हृदय रोग, या स्ट्रोक का इतिहास है?",
    "en": "Do you have a family history of high blood pressure, heart disease, or stroke?",
    "category": "high blood pressure",
    "symptom": None,
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको ऐसी कोई अन्य स्वास्थ्य समस्याएं हैं, जैसे मधुमेह, गुर्दे की बीमारी, या स्लीप एपनिया, जो उच्च रक्तचाप में योगदान कर सकती हैं?",
    "en": "Do you have any other health conditions, such as diabetes, kidney disease, or sleep apnea, that might contribute to high blood pressure?",
    "category": "high blood pressure",
    "symptom": None,
    "risk_factor": False,   },
  {
    "hi": "क्या आपने अपनी जीवनशैली में कोई बदलाव महसूस किया है, जैसे तनाव में वृद्धि, खराब आहार, या व्यायाम की कमी?",
    "en": "Have you noticed any changes in your lifestyle, such as increased stress, poor diet, or lack of exercise?",
    "category": "high blood pressure",
    "symptom": None,
    "risk_factor": False,
  },
  {
    "hi": "क्या आप शराब, कैफीन, या तंबाकू का सेवन करते हैं, और यदि हां, तो कितनी मात्रा में?",
    "en": "Do you consume alcohol, caffeine, or tobacco, and if so, how much?",
    "category": "high blood pressure",
    "symptom": None,
    "risk_factor": False,
  },
  {
    "hi": "क्या आपने हाल ही में वजन बढ़ाया है या अपने आहार या शारीरिक गतिविधि स्तर में बदलाव महसूस किया है?",
    "en": "Have you recently gained weight or experienced changes in your diet or physical activity levels?",
    "category": "high blood pressure",
    "symptom": None,
    "risk_factor": False,
  },
],
    "low blood pressure": [
  {
    "hi": "क्या आप चक्कर, हल्कापन, थकान, या धुंधली दृष्टि जैसे विशिष्ट लक्षण महसूस कर रहे हैं?",
    "en": "Are you experiencing any specific symptoms like dizziness, lightheadedness, fatigue, or blurred vision?",
    "category": "low blood pressure",
    "symptom": None,
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको जल्दी खड़ा होने पर या कुछ समय तक लेटे रहने के बाद हल्का चक्कर या बेहोशी का एहसास होता है?",
   "en": "Do you feel lightheaded or faint when standing up quickly or after lying down for a while?",
    "category": "low blood pressure",
    "symptom": None,
    "risk_factor": False,
  },
  {
    "hi": "क्या आपने हाल ही में कोई बीमारी, संक्रमण, या स्वास्थ्य में कोई बदलाव अनुभव किया है जो आपके रक्तचाप को प्रभावित कर सकता है?",
    "en": "Have you had any recent illnesses, infections, or changes in your health that could affect your blood pressure?",
    "category": "low blood pressure",
    "symptom": None,
    "risk_factor": False, 
 },
  {
    "hi": "क्या आपने हाल ही में अपने आहार, तरल पदार्थों का सेवन, या शारीरिक गतिविधि स्तर में कोई महत्वपूर्ण बदलाव महसूस किया है?",
    "en": "Have you experienced any significant changes in your diet, fluid intake, or activity level recently?",
    "category": "low blood pressure",
    "symptom": None,
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको ऐसी कोई स्वास्थ्य समस्याएं हैं, जैसे हृदय संबंधी समस्याएं, अंतःस्रावी विकार, या निर्जलीकरण, जो निम्न रक्तचाप में योगदान कर सकती हैं?",
    "en": "Do you have any medical conditions, such as heart problems, endocrine disorders, or dehydration, that could contribute to low blood pressure?",
    "category": "low blood pressure",
    "symptom": None,
    "risk_factor": False,
  },
  {
    "hi": "क्या आपने हाल ही में किसी तनाव का अनुभव किया है या खून की महत्वपूर्ण हानि (जैसे चोट या सर्जरी से) हुई है?",
    "en": "Have you been under any recent stress or experienced a significant loss of blood (e.g., from an injury or surgery)?",
    "category": "low blood pressure",
    "symptom": None,
    "risk_factor": False,
  },
],

  "cramp": [
    {
      "hi": "क्या आपको क्रैम्प्स लगातार हो रहे हैं या कभी-कभी?",
      "en": "Are you experiencing cramps continuously or intermittently?",
      "category": "intermittent_cramps",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या क्रैम्प्स किसी विशेष समय पर अधिक होते हैं?",
      "en": "Do your cramps occur more frequently at any specific time?",
      "category": "time_related_cramps",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या क्रैम्प्स के साथ सूजन भी है?",
      "en": "Is there any swelling along with your cramps?",
      "category": "swelling_with_cramps",
      "symptom": "swelling",
      "risk_factor": False,    },
    {
      "hi": "क्या क्रैम्प्स के कारण आपको थकान महसूस हो रही है?",
      "en": "Are you feeling fatigued due to cramps?",
      "category": "fatigue_with_cramps",
      "symptom": "fatigue",
      "risk_factor": False,    },
    {
      "hi": "क्या क्रैम्प्स किसी विशेष गतिविधि के दौरान बढ़ते हैं?",
      "en": "Do your cramps increase during any specific activity?",
      "category": "activity_related_cramps",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या आपको क्रैम्प्स के साथ दर्द में कोई बदलाव महसूस हो रहा है?",
      "en": "Are you noticing any changes in the pain associated with your cramps?",
      "category": "pain_changes",
      "symptom": None,
      "risk_factor": False,    },
  ],

  "irritation": [
    {
      "hi": "क्या आपको त्वचा पर खुजली या जलन महसूस हो रही है?",
      "en": "Are you experiencing itching or burning sensations on your skin?",
      "category": "skin_itching_burning",
      "symptom": "itching",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको आंखों, नाक या गले में जलन हो रही है?",
      "en": "Are you feeling irritation in your eyes, nose, or throat?",
      "category": "localized_irritation",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या आपके शरीर के किसी विशेष हिस्से में जलन महसूस हो रही है?",
      "en": "Are you feeling burning sensations in any specific part of your body?",
      "category": "specific_irritation",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या जलन के साथ सूजन भी है?",
      "en": "Is there any swelling along with the irritation?",
      "category": "swelling_with_irritation",
      "symptom": "swelling",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको किसी विशेष पदार्थ से जलन हो रही है?",
      "en": "Are you experiencing irritation due to any specific substance?",
      "category": "triggered_irritation",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या जलन के कारण आपकी त्वचा लाल हो गई है?",
      "en": "Has the irritation caused any redness on your skin?",
      "category": "redness_with_irritation",
      "symptom": "redness",
      "risk_factor": False,    },
  ],

  "inflammation": [
    {
      "hi": "क्या सूजन के साथ दर्द भी है?",
      "en": "Is there any pain along with the inflammation?",
      "category": "pain_with_inflammation",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या सूजन लगातार है या आता-जाता है?",
      "en": "Is the inflammation constant or does it come and go?",
      "category": "intermittent_inflammation",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या सूजन किसी विशेष समय पर अधिक होती है?",
      "en": "Does the inflammation occur more frequently at any specific time?",
      "category": "time_related_inflammation",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या सूजन के कारण आपको चलने-फिरने में कठिनाई हो रही है?",
      "en": "Are you having difficulty moving due to the inflammation?",
      "category": "movement_difficulty_with_inflammation",
      "symptom": None,
      "risk_factor": False,    },
  ],

  "weight gain": [
    {
      "hi": "क्या आपको वजन तेजी से बढ़ रहा है?",
      "en": "Are you gaining weight rapidly?",
      "category": "rapid_weight_gain",
      "symptom": "weight gain",
      "risk_factor": False,    },
    {
      "hi": "क्या वजन बढ़ने के कारण आपको थकान महसूस हो रही है?",
      "en": "Are you feeling fatigued due to weight gain?",
      "category": "fatigue_with_weight_gain",
      "symptom": "fatigue",
      "risk_factor": False,    },
    {
      "hi": "क्या वजन बढ़ने के साथ आपकी त्वचा पर कोई परिवर्तन आ रहा है?",
      "en": "Are there any changes in your skin due to weight gain?",
      "category": "skin_changes_with_weight_gain",
      "symptom": "skin changes",
      "risk_factor": False,    },
    {
      "hi": "क्या वजन बढ़ने के साथ आपको किसी विशेष हिस्से में दर्द हो रहा है?",
      "en": "Are you experiencing pain in any specific area due to weight gain?",
      "category": "localized_pain_with_weight_gain",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या वजन बढ़ने के साथ आपका मूड भी प्रभावित हो रहा है?",
      "en": "Is your mood being affected along with weight gain?",
      "category": "mood_changes_with_weight_gain",
      "symptom": "depression",
      "risk_factor": False,    },
  ],

   "weight fluctuation": [
{
   "hi": "क्या आपको वजन तेजी से बढ़ रहा है?",
      "en": "Are you gaining weight rapidly?",
      "category": "rapid_weight_gain",
      "symptom": "weight gain",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको थकान महसूस हो रही है?",
      "en": "Are you feeling fatigued due to weight fluctuation?",
      "category": "fatigue_with_weight_gain",
      "symptom": "fatigue",
      "risk_factor": False,    },
    {
      "hi": "क्या आपकी त्वचा पर कोई परिवर्तन आ रहा है?",
      "en": "Are there any changes in your skin due to weight fluctuation?",
      "category": "skin_changes_with_weight_gain",
      "symptom": "skin changes",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको किसी विशेष हिस्से में दर्द हो रहा है?",
      "en": "Are you experiencing pain in any specific area due to weight fluctuation?",
      "category": "localized_pain_with_weight_gain",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या आपका मूड भी प्रभावित हो रहा है?",
      "en": "Is your mood being affected along with weight fluctuation?",
      "category": "mood_changes_with_weight_gain",
      "symptom": "depression",
      "risk_factor": False,    },
],

  "hair loss": [
    {
      "hi": "क्या बालों का झड़ना किसी विशेष हिस्से में ज्यादा हो रहा है?",
      "en": "Is hair loss more prominent in any specific area?",
      "category": "localized_hair_loss",
      "symptom": None,
      "risk_factor": False,    },
   {
      "hi": "क्या बालों का झड़ना के साथ स्कैल्प में खुजली या जलन है?",
      "en": "Is there itching or burning in the scalp along with hair loss?",
      "category": "scalp_itching_burning",
      "symptom": "scalp_itching_burning",
      "risk_factor": False,    },     
   {
  "hi": "क्या आपके परिवार में बाल झड़ने या गंजेपन का इतिहास है?",
  "en": "Do you have a family history of hair loss or baldness?",
  "category": "family_history_hair_loss",
  "symptom": "family_history_hair_loss",
  "risk_factor": True,
},
 {
      "hi": "क्या आपके बालों की ग्रोथ धीमी हो गई है?",
      "en": "Has your hair growth slowed down?",
      "category": "slowed_hair_growth",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या आपके बालों का रंग बदल रहा है?",
      "en": "Are you noticing any changes in your hair color?",
      "category": "hair_color_changes",
      "symptom": "hair color changes",
      "risk_factor": False,    },
	 {
      "hi": "क्या आपको बालों का झड़ना तेजी से हो रहा है?",
      "en": "Are you experiencing rapid hair loss?",
      "category": "rapid_hair_loss",
      "symptom": "hair loss",
      "risk_factor": False,    },
     {
      "hi": "क्या बालों का झड़ना किसी विशेष समय पर अधिक होता है?",
      "en": "Does hair loss occur more frequently at any specific time?",
      "category": "time_related_hair_loss",
      "symptom": None,
      "risk_factor": False,    },
  ],

  "numbness": [
    {
      "hi": "क्या सुन्नता लगातार है या आती-जाती है?",
      "en": "Is the numbness constant or does it come and go?",
      "category": "intermittent_numbness",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या सुन्नता किसी विशेष गतिविधि के दौरान बढ़ती है?",
      "en": "Does your numbness increase during any specific activity?",
      "category": "activity_related_numbness",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या सुन्नता किसी विशेष समय पर अधिक होती है?",
      "en": "Does the numbness occur more frequently at any specific time?",
      "category": "time_related_numbness",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या आपको सुन्नता के साथ कमजोरी भी महसूस हो रही है?",
      "en": "Are you feeling any weakness along with numbness?",
      "category": "weakness_with_numbness",
      "symptom": "weakness",
      "risk_factor": False,    },
  ],

  

  "bloating": [
    {
      "hi": "क्या सूजन के साथ पेट में दर्द भी हो रहा है?",
      "en": "Are you experiencing abdominal pain along with bloating?",
      "category": "abdominal_pain_with_bloating",
      "symptom": "abdominal pain",
      "risk_factor": False,    },
    {
      "hi": "क्या सूजन के कारण आपको सांस लेने में कठिनाई हो रही है?",
      "en": "Is bloating causing difficulty in breathing?",
      "category": "breathing_difficulty_with_bloating",
      "symptom": "shortness of breath",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको सूजन के साथ मतली या उल्टी हो रही है?",
      "en": "Are you experiencing nausea or vomiting along with bloating?",
      "category": "nausea_vomiting_with_bloating",
      "symptom": "nausea",
      "risk_factor": False,    },
    {
      "hi": "क्या सूजन के कारण आपको थकान महसूस हो रही है?",
      "en": "Are you feeling fatigued due to bloating?",
      "category": "fatigue_with_bloating",
      "symptom": "fatigue",
      "risk_factor": False,    },
  ],

  "gas": [
    {
      "hi": "क्या आपको पेट में गैस की अधिकता महसूस हो रही है?",
      "en": "Are you feeling excessive gas in your abdomen?",
      "category": "excessive_gas",
      "symptom": "gas",
      "risk_factor": False,    },
    {
      "hi": "क्या गैस के साथ पेट में दर्द भी हो रहा है?",
      "en": "Are you experiencing abdominal pain along with gas?",
      "category": "abdominal_pain_with_gas",
      "symptom": "abdominal pain",
      "risk_factor": False,    },
     {
      "hi": "क्या गैस के साथ आपका मूड भी प्रभावित हो रहा है?",
      "en": "Is your mood being affected along with gas?",
      "category": "mood_changes_with_gas",
      "symptom": "mood changes",
      "risk_factor": False,    },
    {
      "hi": "क्या गैस के कारण आपको पेट फूलने का अनुभव हो रहा है?",
      "en": "Are you experiencing bloating due to gas?",
      "category": "bloating_with_gas",
      "symptom": "bloating",
      "risk_factor": False,    },
    
    {
      "hi": "क्या गैस के कारण आपकी नींद प्रभावित हो रही है?",
      "en": "Is gas affecting your sleep?",
      "category": "sleep_disturbance_with_gas",
      "symptom": "insomnia",
      "risk_factor": False,    },
  ],

  "indigestion": [
    {
      "hi": "क्या आपको भोजन के बाद पेट में दर्द हो रहा है?",
      "en": "Are you experiencing abdominal pain after eating?",
      "category": "post_meal_abdominal_pain",
      "symptom": "abdominal pain",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको गैस या सूजन महसूस हो रही है?",
      "en": "Are you feeling gas or bloating?",
      "category": "gas_bloating_with_indigestion",
      "symptom": "gas",
      "risk_factor": False,    },
    {
      "hi": "क्या indigestion के साथ आपको उल्टी या दस्त भी हो रहे हैं?",
      "en": "Are you also experiencing vomiting or diarrhea along with indigestion?",
      "category": "vomiting_diarrhea_with_indigestion",
      "symptom": "vomiting",
      "risk_factor": False,    },
    {
      "hi": "क्या indigestion के कारण आपको भोजन निगलने में कठिनाई हो रही है?",
      "en": "Is indigestion causing difficulty in swallowing your food?",
      "category": "swallowing_difficulty_with_indigestion",
      "symptom": "difficulty swallowing",
      "risk_factor": False,    },
    {
      "hi": "क्या indigestion के साथ आपको पेट में भारीपन महसूस हो रहा है?",
      "en": "Are you feeling a heaviness in your abdomen along with indigestion?",
      "category": "heaviness_with_indigestion",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या indigestion के कारण आपकी नींद प्रभावित हो रही है?",
      "en": "Is indigestion affecting your sleep?",
      "category": "sleep_disturbance_with_indigestion",
      "symptom": "insomnia",
      "risk_factor": False,    },
  ],

  "mouth sore": [
    {
      "hi": "क्या आपके मुंह में घाव तेजी से बढ़ रहे हैं?",
      "en": "Are your mouth sores spreading rapidly?",
      "category": "rapid_spread_mouth_sores",
      "symptom": "mouth sores",
      "risk_factor": False,    },
    {
      "hi": "क्या मुंह के घावों के साथ सूजन भी है?",
      "en": "Is there any swelling along with your mouth sores?",
      "category": "swelling_with_mouth_sores",
      "symptom": "swelling",
      "risk_factor": False,    },
    {
      "hi": "क्या मुंह के घाव खाने या पीने में दर्द पैदा करते हैं?",
      "en": "Do your mouth sores cause pain while eating or drinking?",
      "category": "pain_with_mouth_sores",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या आपको मुंह के घावों से रक्तस्राव हो रहा है?",
      "en": "Are your mouth sores bleeding?",
      "category": "bleeding_mouth_sores",
      "symptom": "bleeding",
      "risk_factor": False,    },
    {
      "hi": "क्या मुंह के घावों के साथ आपके दांतों में दर्द है?",
      "en": "Are you experiencing tooth pain along with mouth sores?",
      "category": "tooth_pain_with_mouth_sores",
      "symptom": "tooth pain",
      "risk_factor": False,    },
    {
      "hi": "क्या मुंह के घावों के कारण आपकी बोलने में कठिनाई हो रही है?",
      "en": "Are your mouth sores causing difficulty in speaking?",
      "category": "speech_difficulty_with_mouth_sores",
      "symptom": "difficulty speaking",
      "risk_factor": False,    },
  ],

  "nosebleed": [
    {
      "hi": "क्या नाक से खून बहना बार-बार हो रहा है?",
      "en": "Are you experiencing frequent nosebleeds?",
      "category": "frequent_nosebleeds",
      "symptom": "nosebleeds",
      "risk_factor": False,    },
    {
      "hi": "क्या नाक से खून बहने के साथ दर्द भी हो रहा है?",
      "en": "Are you experiencing pain along with nosebleeds?",
      "category": "pain_with_nosebleeds",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या नाक से खून बहने का कोई विशेष कारण है?",
      "en": "Is there any specific cause for your nosebleeds?",
      "category": "specific_cause_nosebleeds",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या नाक से खून बहने के साथ आपको सूजन भी हो रही है?",
      "en": "Is there any swelling along with your nosebleeds?",
      "category": "swelling_with_nosebleeds",
      "symptom": "swelling",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको नाक से खून बहने के बाद कमजोरी महसूस हो रही है?",
      "en": "Are you feeling weak after nosebleeds?",
      "category": "weakness_with_nosebleeds",
      "symptom": "weakness",
      "risk_factor": False,    },
    {
      "hi": "क्या नाक से खून बहने के साथ आपको सिरदर्द भी हो रहा है?",
      "en": "Are you experiencing headaches along with nosebleeds?",
      "category": "headache_with_nosebleeds",
      "symptom": "headache",
      "risk_factor": False,    },
  ],

  "blood in urine": [
    {
      "hi": "क्या खून की मात्रा बढ़ रही है?",
      "en": "Is the amount of blood in your urine increasing?",
      "category": "increasing_blood_in_urine",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या खून आने के साथ आपको पेशाब में दर्द हो रहा है?",
      "en": "Are you experiencing pain while urinating along with blood in urine?",
      "category": "pain_with_blood_in_urine",
      "symptom": "urinary pain",
      "risk_factor": False,    },
    {
      "hi": "क्या खून आने के साथ आपको कमजोरी भी महसूस हो रही है?",
      "en": "Are you feeling weak along with blood in your urine?",
      "category": "weakness_with_blood_in_urine",
      "symptom": "weakness",
      "risk_factor": False,    },
    {
      "hi": "क्या खून आने के कारण आपकी त्वचा में कोई परिवर्तन आ रहा है?",
      "en": "Is there any change in your skin due to blood in urine?",
      "category": "skin_changes_with_blood_in_urine",
      "symptom": "skin discoloration",
      "risk_factor": False,    },
    {
      "hi": "क्या खून आने के साथ आपको बुखार भी है?",
      "en": "Do you have a fever along with blood in urine?",
      "category": "fever_with_blood_in_urine",
      "symptom": "fever",
      "risk_factor": False,    },
    {
      "hi": "क्या खून आने के साथ आपको पसीना भी आ रहा है?",
      "en": "Are you sweating along with blood in urine?",
      "category": "sweating_with_blood_in_urine",
      "symptom": "sweating",
      "risk_factor": False,    },
  ],

  "blood in stool": [
    {
      "hi": "क्या खून का रंग गहरा है या हल्का?",
      "en": "Is the blood in your stool dark or light-colored?",
      "category": "blood_color_in_stool",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या खून आने के साथ आपको पेट में दर्द हो रहा है?",
      "en": "Are you experiencing abdominal pain along with blood in stool?",
      "category": "abdominal_pain_with_blood_in_stool",
      "symptom": "abdominal pain",
      "risk_factor": False,    },
    {
      "hi": "क्या खून आने के कारण आपको कमजोरी महसूस हो रही है?",
      "en": "Are you feeling weak due to blood in your stool?",
      "category": "weakness_with_blood_in_stool",
      "symptom": "weakness",
      "risk_factor": False,    },
    {
      "hi": "क्या खून आने के साथ आपके मल त्यागने की आदत बदल गई है?",
      "en": "Has your bowel movement pattern changed along with blood in stool?",
      "category": "bowel_movement_changes_with_blood_in_stool",
      "symptom": "constipation",
      "risk_factor": False,    },
    {
      "hi": "क्या खून आने के साथ आपको बुखार भी है?",
      "en": "Do you have a fever along with blood in stool?",
      "category": "fever_with_blood_in_stool",
      "symptom": "fever",
      "risk_factor": False,    },
    {
      "hi": "क्या खून आने के कारण आपकी त्वचा में कोई परिवर्तन आ रहा है?",
      "en": "Is there any change in your skin due to blood in stool?",
      "category": "skin_changes_with_blood_in_stool",
      "symptom": "skin discoloration",
      "risk_factor": False,    },
  ],

  "excessive thirst": [

    {
      "hi": "क्या अत्यधिक प्यास के साथ आपको बार-बार पेशाब आ रहा है?",
      "en": "Are you urinating frequently along with excessive thirst?",
      "category": "frequent_urination_with_thirst",
      "symptom": "frequent urination",
      "risk_factor": False,    },
    {
      "hi": "क्या अत्यधिक प्यास के कारण आप पर्याप्त पानी पी रहे हैं?",
      "en": "Are you drinking enough water due to excessive thirst?",
      "category": "hydration_with_thirst",
      "symptom": "dehydration",
      "risk_factor": False,    },
    {
      "hi": "क्या अत्यधिक प्यास के साथ आपको कमजोरी भी महसूस हो रही है?",
      "en": "Are you feeling weak along with excessive thirst?",
      "category": "weakness_with_thirst",
      "symptom": "weakness",
      "risk_factor": False,    },
    {
      "hi": "क्या अत्यधिक प्यास के साथ आपके शरीर में कोई अन्य परिवर्तन हो रहा है?",
      "en": "Are there any other changes in your body along with excessive thirst?",
      "category": "other_changes_with_thirst",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या आपकी डाइट में कोई विशेष बदलाव हुआ है जिससे आपको अत्यधिक प्यास लग रही है?",
      "en": "Has there been any specific change in your diet causing excessive thirst?",
      "category": "diet_changes_with_thirst",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या आपको अत्यधिक प्यास के साथ वजन कम हो रहा है?",
      "en": "Are you losing weight along with excessive thirst?",
      "category": "weight_loss_with_thirst",
      "symptom": "weight loss",
      "risk_factor": False,    },
  ],

  "dehydration": [
    {
      "hi": "क्या आपको प्यास लगी हुई है?",
      "en": "Are you feeling thirsty?",
      "category": "thirst",
      "symptom": "thirst",
      "risk_factor": False,    },
    {
      "hi": "क्या आपका पेशाब कम आ रहा है और रंग गहरा हो गया है?",
      "en": "Is your urine output reduced and dark-colored?",
      "category": "reduced_dark_urine",
      "symptom": "dark urine",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको सिरदर्द या चक्कर आ रहे हैं?",
      "en": "Are you experiencing headaches or dizziness?",
      "category": "headache_dizziness_with_dehydration",
      "symptom": "headache",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको शरीर में सूजन महसूस हो रही है?",
      "en": "Are you feeling swelling in your body?",
      "category": "swelling_with_dehydration",
      "symptom": "swelling",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको पसीना आ रहा है या त्वचा सूखी हो गई है?",
      "en": "Are you sweating or is your skin dry?",
      "category": "sweating_dry_skin_with_dehydration",
      "symptom": "sweating",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको थकान महसूस हो रही है?",
      "en": "Are you feeling fatigued?",
      "category": "fatigue_with_dehydration",
      "symptom": "fatigue",
      "risk_factor": False,    },
  ],


  "sweat": [
    {
      "hi": "क्या आपको पसीना आना सामान्य से अधिक हो रहा है?",
      "en": "Are you sweating more than usual?",
      "category": "excessive_sweating",
      "symptom": "sweating",
      "risk_factor": False,    },
    {
      "hi": "क्या पसीना आना किसी विशेष समय पर अधिक होता है?",
      "en": "Does sweating occur more frequently at any specific time?",
      "category": "time_related_sweating",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या आपको पसीना आना के कारण किसी विशेष गतिविधि के दौरान कठिनाई हो रही है?",
      "en": "Are you experiencing difficulty during any specific activity due to sweating?",
      "category": "activity_related_sweating",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या पसीना आना के साथ आपको त्वचा में कोई परिवर्तन हो रहा है?",
      "en": "Are you noticing any changes in your skin due to sweating?",
      "category": "skin_changes_with_sweating",
      "symptom": "skin changes",
      "risk_factor": False,    },
  ],

  "cold": [
    {
      "hi": "क्या आपको ठंड लगना सामान्य से अधिक हो रहा है?",
      "en": "Are you feeling cold more than usual?",
      "category": "excessive_cold",
      "symptom": "feeling cold",
      "risk_factor": False,    },
    {
      "hi": "क्या ठंड महसूस होने के साथ आपको दर्द भी हो रहा है?",
      "en": "Are you experiencing pain along with feeling cold?",
      "category": "pain_with_feeling_cold",
      "symptom": "pain",
      "risk_factor": False,    },
    {
      "hi": "क्या ठंड महसूस होने के कारण आपके शरीर में कोई कमजोरी आ रही है?",
      "en": "Is feeling cold causing any weakness in your body?",
      "category": "weakness_with_feeling_cold",
      "symptom": "weakness",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको सांस लेने में कठिनाई हो रही है?",
      "en": "Are you having difficulty breathing?",
      "category": "breathing_difficulty_with_cold",
      "symptom": "breathing difficulty",
      "risk_factor": True
    },
    {
      "hi": "क्या आपको अचानक से ठंड लगना शुरू हुआ?",
      "en": "Did the feeling of cold start suddenly?",
      "category": "sudden_onset_cold",
      "symptom": None,
      "risk_factor": False
    },
  ],


  "red eyes": [
    {
      "hi": "क्या आपकी आँखें लाल हो रही हैं लगातार या कभी-कभी?",
      "en": "Are your eyes becoming red continuously or intermittently?",
      "category": "intermittent_eye_redness",
      "symptom": "eye redness",
      "risk_factor": False,    },
    {
      "hi": "क्या आँखों में लालिमा के साथ सूजन भी हो रही है?",
      "en": "Is there any swelling along with redness in your eyes?",
      "category": "swelling_with_eye_redness",
      "symptom": "swelling",
      "risk_factor": False,    },
    {
      "hi": "क्या आँखों में लालिमा के साथ दर्द भी हो रहा है?",
      "en": "Are you experiencing pain along with redness in your eyes?",
      "category": "pain_with_eye_redness",
      "symptom": "eye pain",
      "risk_factor": False,    },
    {
      "hi": "क्या लालिमा किसी विशेष गतिविधि या समय पर बढ़ती है?",
      "en": "Does redness in your eyes increase during any specific activity or time?",
      "category": "activity_time_related_eye_redness",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या लालिमा के कारण आपकी दृष्टि प्रभावित हो रही है?",
      "en": "Is the redness in your eyes affecting your vision?",
      "category": "vision_impact_with_eye_redness",
      "symptom": "blurred vision",
      "risk_factor": False,    },
    {
      "hi": "क्या आँखों में लालिमा के साथ पानी आना शुरू हो गया है?",
      "en": "Have you started experiencing watering of the eyes along with redness?",
      "category": "watering_with_eye_redness",
      "symptom": "eye tearing",
      "risk_factor": False,    },
  ],

  "hearing loss": [
    {
      "hi": "क्या आपको सुनने में कठिनाई हो रही है लगातार या कभी-कभी?",
      "en": "Are you experiencing difficulty hearing continuously or intermittently?",
      "category": "intermittent_hearing_loss",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या सुनने में कमी किसी विशेष समय या स्थिति में होती है?",
      "en": "Does the hearing loss occur more during any specific time or situation?",
      "category": "time_situation_related_hearing_loss",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या सुनने में कमी के साथ आपको कान में दर्द भी हो रहा है?",
      "en": "Are you experiencing ear pain along with hearing loss?",
      "category": "ear_pain_with_hearing_loss",
      "symptom": "ear pain",
      "risk_factor": False,    },
    {
      "hi": "क्या सुनने में कमी के कारण आपकी दैनिक गतिविधियाँ प्रभावित हो रही हैं?",
      "en": "Are your daily activities being affected due to hearing loss?",
      "category": "daily_activity_impact_with_hearing_loss",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या आपको कान में कोई स्राव या जलन महसूस हो रही है?",
      "en": "Are you feeling any discharge or irritation in your ears?",
      "category": "discharge_irritation_with_hearing_loss",
      "symptom": "ear discharge",
      "risk_factor": False,    },
    {
      "hi": "क्या सुनने में कमी के साथ आपका संतुलन भी प्रभावित हो रहा है?",
      "en": "Is your balance being affected along with hearing loss?",
      "category": "balance_impact_with_hearing_loss",
      "symptom": "balance problems",
      "risk_factor": False,    },
    {
      "hi": "क्या सुनने में कमी के कारण आपको सामाजिक स्थितियों में कठिनाई हो रही है?",
      "en": "Are you facing difficulties in social situations due to hearing loss?",
      "category": "social_difficulty_with_hearing_loss",
      "symptom": None,
      "risk_factor": False,    },
  ],

  "balance problem": [
    {
      "hi": "क्या संतुलन बिगड़ने के साथ चक्कर आना भी हो रहा है?",
      "en": "Are you experiencing dizziness along with balance problems?",
      "category": "dizziness_with_balance_problems",
      "symptom": "dizziness",
      "risk_factor": False,    },
    {
      "hi": "क्या संतुलन बिगड़ने की समस्या किसी विशेष समय या स्थिति में होती है?",
      "en": "Do balance problems occur more during any specific time or situation?",
      "category": "time_situation_related_balance_problems",
      "symptom": None,
      "risk_factor": False,    },
  
    {
      "hi": "क्या संतुलन बिगड़ने के कारण आपकी दैनिक गतिविधियाँ प्रभावित हो रही हैं?",
      "en": "Are your daily activities being affected due to balance problems?",
      "category": "daily_activity_impact_with_balance_problems",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या संतुलन बिगड़ने के कारण आपको चलने-फिरने में कठिनाई हो रही है?",
      "en": "Are you having difficulty walking due to balance problems?",
      "category": "walking_difficulty_with_balance_problems",
      "symptom": None,
      "risk_factor": False,    },
      {
      "hi": "क्या संतुलन बिगड़ने के साथ आपको कोई अन्य लक्षण भी महसूस हो रहे हैं?",
      "en": "Are you experiencing any other symptoms along with balance problems?",
      "category": "other_symptoms_with_balance_problems",
      "symptom": None,
      "risk_factor": False,    },
  ],

  "rapid breathing": [
    {
      "hi": "क्या तेजी से सांस लेने के कारण आपको सांस लेने में कठिनाई हो रही है?",
      "en": "Are you having difficulty breathing due to rapid breathing?",
      "category": "difficulty_breathing_with_rapid_breathing",
      "symptom": "shortness of breath",
      "risk_factor": False,    },
    {
      "hi": "क्या तेजी से सांस लेने के साथ आपका दिल भी तेज धड़क रहा है?",
      "en": "Is your heart beating faster along with rapid breathing?",
      "category": "heart_rate_increase_with_rapid_breathing",
      "symptom": "irregular heartbeat",
      "risk_factor": False,    },
    {
      "hi": "क्या तेजी से सांस लेने के कारण आपको चक्कर आ रहे हैं?",
      "en": "Are you experiencing dizziness due to rapid breathing?",
      "category": "dizziness_with_rapid_breathing",
      "symptom": "dizziness",
      "risk_factor": False,    },
    {
      "hi": "क्या तेजी से सांस लेने के साथ आपको पसीना आ रहा है?",
      "en": "Are you sweating along with rapid breathing?",
      "category": "sweating_with_rapid_breathing",
      "symptom": "sweating",
      "risk_factor": False,    },
    {
      "hi": "क्या तेजी से सांस लेने का कारण कोई विशेष गतिविधि है?",
      "en": "Is there any specific activity causing your rapid breathing?",
      "category": "activity_related_rapid_breathing",
      "symptom": None,
      "risk_factor": False,    },
  ],

  "irregular heartbeat": [
    {
      "hi": "क्या आपके दिल की धड़कन अनियमित हो गई है?",
      "en": "Has your heartbeat become irregular?",
      "category": "irregular_heartbeat",
      "symptom": "irregular heartbeat",
      "risk_factor": False,    },
     {
      "hi": "क्या अनियमित धड़कन के कारण आपको सांस लेने में कठिनाई हो रही है?",
      "en": "Are you having difficulty breathing due to an irregular heartbeat?",
      "category": "breathing_difficulty_with_irregular_heartbeat",
      "symptom": "shortness of breath",
      "risk_factor": False,    },
    {
      "hi": "क्या अनियमित धड़कन के साथ आपको चक्कर आ रहे हैं?",
      "en": "Are you experiencing dizziness along with an irregular heartbeat?",
      "category": "dizziness_with_irregular_heartbeat",
      "symptom": "dizziness",
      "risk_factor": False,    },
    {
      "hi": "क्या अनियमित धड़कन के साथ आपको थकान भी हो रही है?",
      "en": "Are you feeling fatigued along with an irregular heartbeat?",
      "category": "fatigue_with_irregular_heartbeat",
      "symptom": "fatigue",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके दिल की धड़कन तेज हो गई है?",
      "en": "Has your heartbeat become faster?",
      "category": "fast_heartbeat_with_irregular_heartbeat",
      "symptom": "heart palpitations",
      "risk_factor": False,    },
    {
      "hi": "क्या अनियमित धड़कन अचानक शुरू हुई है या धीरे-धीरे?",
      "en": "Did your irregular heartbeat start suddenly or gradually?",
      "category": "sudden_graduate_irregular_heartbeat",
      "symptom": None,
      "risk_factor": False,    },
  ],


  "rash": [
    {
      "hi": "क्या आपके शरीर पर कोई दाने या चकत्ते हैं?",
      "en": "Do you have any bumps or spots on your skin?",
      "category": "bumps_spots_with_skin_rash",
      "symptom": "skin rash",
      "risk_factor": False,    },
    {
      "hi": "क्या त्वचा पर लालिमा या सूजन भी है?",
      "en": "Is there any redness or swelling on your skin along with the rash?",
      "category": "redness_swelling_with_skin_rash",
      "symptom": "redness",
      "risk_factor": False,    },
    {
      "hi": "क्या रैश किसी विशेष स्थान पर ज्यादा हैं?",
      "en": "Are the rashes more concentrated in any specific area?",
      "category": "localized_skin_rash",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या रैश के साथ खुजली या जलन भी हो रही है?",
      "en": "Are you experiencing itching or burning sensations along with the rash?",
      "category": "itching_burning_with_skin_rash",
      "symptom": "itching",
      "risk_factor": False,    },
    {
      "hi": "क्या रैश समय के साथ फैल रहे हैं या स्थिर हैं?",
      "en": "Are the rashes spreading over time or are they static?",
      "category": "spreading_vs_static_skin_rash",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या आपके रैश के कारण आपकी त्वचा में कोई परिवर्तन हो रहा है?",
      "en": "Are there any changes in your skin due to the rash?",
      "category": "skin_changes_with_skin_rash",
      "symptom": "skin discoloration",
      "risk_factor": False,    },
    {
      "hi": "क्या रैश अचानक शुरू हुए हैं या धीरे-धीरे?",
      "en": "Did your rashes start suddenly or gradually?",
      "category": "sudden_graduate_skin_rash",
      "symptom": None,
      "risk_factor": False,    },
  ],

  "itching": [
    {
      "hi": "क्या आपकी खुजली लगातार है या कभी-कभी आती है?",
      "en": "Is the itching continuous or intermittent?",
      "category": "intermittent_skin_itching",
      "symptom": "skin itching",
      "risk_factor": False,    },
    {
      "hi": "क्या खुजली के साथ लालिमा भी है?",
      "en": "Is there any redness along with itching?",
      "category": "redness_with_skin_itching",
      "symptom": "redness",
      "risk_factor": False,    },
    {
      "hi": "क्या खुजली के कारण सूजन हो रही है?",
      "en": "Is itching causing any swelling?",
      "category": "swelling_with_skin_itching",
      "symptom": "swelling",
      "risk_factor": False,    },
    {
      "hi": "क्या खुजली आपको सोने में परेशान कर रही है?",
      "en": "Is itching disturbing your sleep?",
      "category": "sleep_disturbance_with_skin_itching",
      "symptom": "insomnia",
      "risk_factor": False,    },
    {
      "hi": "क्या खुजली के साथ त्वचा में कोई दरार या फफोले हो रहे हैं?",
      "en": "Are there any cracks or blisters along with itching?",
      "category": "cracks_blisters_with_skin_itching",
      "symptom": "skin lesions",
      "risk_factor": False,    },
    {
      "hi": "क्या खुजली के कारण कोई अन्य परिवर्तन हो रहा है?",
      "en": "Are there any other changes due to itching?",
      "category": "skin_changes_with_skin_itching",
      "symptom": "skin discoloration",
      "risk_factor": False,    },
    {
      "hi": "क्या खुजली किसी विशेष समय या वातावरण में बढ़ती है?",
      "en": "Does itching increase during any specific time or environment?",
      "category": "environment_related_skin_itching",
      "symptom": None,
      "risk_factor": False,    },
  ],

  "acne": [
    {
      "hi": "आपके पास आमतौर पर एक्ने कहाँ होते हैं?",
      "en": "Where do you typically get acne?",
      "category": "acne",
      "symptom": "acne location",
      "risk_factor": False,    },
	  {
      "hi": "क्या आपने अपने एक्ने के लिए कोई उपचार किया है?",
      "en": "Have you tried any treatments for your acne?",
      "category": "acne treatments",
      "symptom": "acne treatment",
      "risk_factor": False,    },
    {
      "hi": "आपके पास किस प्रकार का एक्ने है?",
      "en": "What type of acne do you have?",
      "category": "acne",
      "symptom": "acne type",
      "risk_factor": False,    },
    {
      "hi": "आपके एक्ने कितने गंभीर हैं?",
      "en": "How severe is your acne?",
      "category": "acne",
      "symptom": "acne severity",
      "risk_factor": False,    },
    
    {
      "hi": "क्या आप वर्तमान में कोई स्किनकेयर या मेकअप उत्पाद उपयोग कर रहे हैं?",
      "en": "Are you currently using any skincare or makeup products?",
      "category": "skincare",
      "symptom": "skincare use",
      "risk_factor": False,    },
    {
      "hi": "आप कौन सी दवाइयाँ ले रहे हैं?",
      "en": "What medications are you currently taking?",
      "category": "medication",
      "symptom": "medication",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके परिवार में किसी को एक्ने है?",
      "en": "Do you have a family history of acne?",
      "category": "family history",
      "symptom": "family history",
      "risk_factor": True,    },
    {
      "hi": "क्या आपने अपने एक्ने के लिए किसी विशेष कारण का अनुभव किया है?",
      "en": "Have you noticed any specific triggers for your acne?",
      "category": "acne triggers",
      "symptom": "acne triggers",
      "risk_factor": False,    },
  ],

  "insomnia": [
    {
      "hi": "आप आमतौर पर किस समय सोने जाते हैं और किस समय उठते हैं?",
      "en": "What time do you usually go to bed and wake up?",
      "category": "insomnia",
      "symptom": "sleep schedule",
      "risk_factor": False,    },
    {
      "hi": "आपको सोने में सामान्यतः कितना समय लगता है?",
      "en": "How long does it typically take you to fall asleep?",
      "category": "insomnia",
      "symptom": "time to fall asleep",
      "risk_factor": False,    },
    {
      "hi": "क्या आप रात में उठते हैं? अगर हां, तो कितनी बार?",
      "en": "Do you wake up during the night? If so, how often?",
      "category": "insomnia",
      "symptom": "night waking",
      "risk_factor": False,    },
    {
      "hi": "क्या आप जब उठते हैं तो आराम महसूस करते हैं?",
      "en": "Do you feel rested when you wake up?",
      "category": "insomnia",
      "symptom": "restfulness",
      "risk_factor": False,    },
    {
      "hi": "क्या आपने हाल ही में अपनी जीवनशैली में कोई बदलाव अनुभव किया है (जैसे तनाव, आहार, यात्रा)?",
      "en": "Have you experienced any changes in your lifestyle recently (e.g., stress, diet, travel)?",
      "category": "lifestyle",
      "symptom": "lifestyle changes",
      "risk_factor": False,    },
    {
      "hi": "क्या आप कैफीन, निकोटीन, या शराब का सेवन करते हैं, और अगर हां, तो कब?",
      "en": "Do you consume caffeine, nicotine, or alcohol, and if so, when?",
      "category": "substance use",
      "symptom": "substance use",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको कोई अन्य चिकित्सा समस्याएँ हैं (जैसे दर्द, सांस लेने में समस्या, मानसिक स्वास्थ्य समस्याएँ)?",
      "en": "Do you have any other medical conditions (e.g., pain, breathing problems, mental health conditions)?",
      "category": "medical conditions",
      "symptom": "medical conditions",
      "risk_factor": False,    },
    {
      "hi": "क्या आप सोने से पहले कोई गतिविधियाँ या दिनचर्या करते हैं (जैसे स्क्रीन टाइम, व्यायाम, विश्राम)?",
      "en": "Do you engage in any activities or routines before bed (e.g., screen time, exercise, relaxation)?",
      "category": "bedtime routines",
      "symptom": "bedtime routine",
      "risk_factor": False,    },
  ],

  "memory loss": [
  {
  "hi": "क्या आप हाल की घटनाओं को भूल जाते हैं?",
  "en": "Do you forget recent events?",
  "category": "short_term_memory_loss",
  "symptom": "short-term memory loss",
  "risk_factor": False,
},
{
  "hi": "क्या आपकी याददाश्त में कमी समय के साथ और अधिक बढ़ गई है?",
  "en": "Has your memory loss got worsened over time?",
  "category": "progressive_memory_loss",
  "symptom": "worsening memory loss",
  "risk_factor": False,
},  
 {
      "hi": "क्या याददाश्त की कमी समय के साथ बढ़ रही है?",
      "en": "Is the memory loss getting worse over time?",
      "category": "memory loss",
      "symptom": "memory loss progression",
      "risk_factor": False,    },
   {
  "hi": "क्या आपको हाल ही में सिर में चोट, कोई आघात या स्ट्रोक हुआ है?",
  "en": "Have you had any recent head injuries or trauma or stroke?",
  "category": "head_injury_or_stroke",
  "symptom": None,
  "risk_factor": True,
  },
  {
      "hi": "क्या आपको कोई अन्य चिकित्सा समस्याएँ हैं, जैसे उच्च रक्तचाप, मधुमेह, या थायरॉयड की समस्याएँ?",
      "en": "Do you have any other medical conditions, such as high blood pressure, diabetes, or thyroid problems?",
      "category": "medical conditions",
      "symptom": "medical conditions",
      "risk_factor": True,    },
    {
      "hi": "क्या आप किसी अन्य संज्ञानात्मक समस्या का अनुभव कर रहे हैं, जैसे भ्रम या ध्यान केंद्रित करने में कठिनाई?",
      "en": "Are you experiencing any other cognitive problems, such as confusion or difficulty concentrating?",
      "category": "cognitive problems",
      "symptom": "cognitive problems",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके परिवार में किसी को याददाश्त की समस्याएँ या तंत्रिका तंत्र की बीमारियाँ हैं (जैसे अल्जाइमर, डिमेंशिया)?",
      "en": "Do you have any family history of memory problems or neurological conditions (e.g., Alzheimer’s, dementia)?",
      "category": "family history",
      "symptom": "family history",
      "risk_factor": True,    },
    {
      "hi": "क्या आपको हाल ही में किसी मूड परिवर्तन का अनुभव हो रहा है, जैसे अवसाद या चिंता?",
      "en": "Have you been experiencing any mood changes, such as depression or anxiety?",
      "category": "mood changes",
      "symptom": "mood changes",
      "risk_factor": False,    },
     {
      "hi": "आप किस प्रकार की याददाश्त की समस्याओं का सामना कर रहे हैं?",
      "en": "What type of memory problems are you experiencing?",
      "category": "memory loss",
      "symptom": "memory problem type",
      "risk_factor": False,    },
  ],


  "tremor": [
    {
      "hi": "क्या कंपन हमेशा होते हैं या यह आते-जाते हैं?",
      "en": "Are the tremors present all the time or do they come and go?",
      "category": "tremors",
      "symptom": "tremor frequency",
      "risk_factor": False,    },
    {
      "hi": "क्या कंपन आपके शरीर के किसी विशेष हिस्से में होते हैं (जैसे, हाथ, सिर, आवाज)?",
      "en": "Do the tremors occur in specific parts of your body (e.g., hands, head, voice)?",
      "category": "tremors",
      "symptom": "affected body parts",
      "risk_factor": False,    },
    {
      "hi": "क्या कंपन किसी विशेष गतिविधि के साथ और अधिक बढ़ जाते हैं, जैसे कुछ पकड़ने या हिलाने के दौरान?",
      "en": "Do the tremors get worse with certain activities, like holding something or moving?",
      "category": "tremors",
      "symptom": "activity-related worsening",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके परिवार में कंपन या न्यूरोलॉजिकल स्थितियों का इतिहास है (जैसे, पार्किंसंस रोग)?",
      "en": "Do you have a family history of tremors or neurological conditions (e.g., Parkinson’s disease)?",
      "category": "tremors",
      "symptom": "family history of neurological conditions",
      "risk_factor": True,    },
    {
      "hi": "क्या आपने हाल ही में कोई तनाव, चिंता, या मानसिक परिवर्तन अनुभव किए हैं?",
      "en": "Have you recently experienced any stress, anxiety, or emotional changes?",
      "category": "tremors",
      "symptom": "emotional or stress-related changes",
      "risk_factor": False,    },
    {
      "hi": "क्या आप कोई दवाइयाँ ले रहे हैं, जिसमें पर्ची वाली, ओवर-द-काउंटर दवाइयाँ, या सप्लीमेंट्स शामिल हैं?",
      "en": "Are you taking any medications, including prescription, over-the-counter, or supplements?",
      "category": "tremors",
      "symptom": "medication use",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको हाल ही में कोई चोट, संक्रमण, या बीमारी हुई है जो आपके तंत्रिका तंत्र को प्रभावित कर सकती है?",
      "en": "Have you had any recent injuries, infections, or illnesses that might affect your nervous system?",
      "category": "tremors",
      "symptom": "nervous system impact",
      "risk_factor": False,    },
    {
      "hi": "क्या आप शराब पीते हैं या कैफीन का सेवन करते हैं, और यदि हां, तो कितनी मात्रा में और कितनी बार?",
      "en": "Do you drink alcohol or consume caffeine, and if so, how much and how often?",
      "category": "tremors",
      "symptom": "alcohol or caffeine consumption",
      "risk_factor": False,    },
  ],

  "panic attack": [
    {
      "hi": "आपको कितनी बार पैनिक अटैक होते हैं?",
      "en": "How often do you have panic attacks?",
      "category": "panic_attack",
      "symptom": "frequency of panic attacks",
      "risk_factor": False,    },
    {
      "hi": "क्या पैनिक अटैक अचानक होते हैं, या आपको कुछ विशेष उत्तेजक (जैसे, तनावपूर्ण स्थिति, भीड़) का पता चलता है?",
      "en": "Do the panic attacks occur unexpectedly, or do you notice specific triggers (e.g., stressful situations, crowds)?",
      "category": "panic_attack",
      "symptom": "triggers of panic attacks",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको पैनिक अटैक के अलावा भी चिंता या घबराहट महसूस होती है?",
      "en": "Do you feel anxious or nervous even when you're not having a panic attack?",
      "category": "panic_attack",
      "symptom": "general anxiety",
      "risk_factor": False,    },
    {
      "hi": "क्या आपने हाल ही में कोई बड़ा जीवन परिवर्तन या आघातक घटना अनुभव की है?",
      "en": "Have you experienced any major life stressors or traumatic events recently?",
      "category": "panic_attack",
      "symptom": "recent stressors or trauma",
      "risk_factor": False,    },
    {
      "hi": "क्या आप पैनिक अटैक के डर से कुछ स्थानों या स्थितियों से बचते हैं?",
      "en": "Do you avoid certain situations or places because of the fear of having a panic attack?",
      "category": "panic_attack",
      "symptom": "avoidance behaviors",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको किसी अन्य मानसिक स्वास्थ्य समस्याओं का निदान हुआ है, जैसे चिंता, अवसाद, या PTSD?",
      "en": "Have you been diagnosed with any other mental health conditions, such as anxiety, depression, or PTSD?",
      "category": "panic_attack",
      "symptom": "co-occurring mental health conditions",
      "risk_factor": False,    },
    {
      "hi": "क्या आप कोई दवाइयाँ ले रहे हैं, जिसमें ओवर-द-काउंटर या हर्बल सप्लीमेंट्स भी शामिल हैं?",
      "en": "Are you taking any medications, including over-the-counter or herbal supplements?",
      "category": "panic_attack",
      "symptom": "medication use",
      "risk_factor": False,    },

  ],

  "mood swing": [

    {
      "hi": "आपके मूड स्विंग्स कितनी बार होते हैं?",
      "en": "How often do your mood swings occur?",
      "category": "mood_swings",
      "symptom": "frequency of mood swings",
      "risk_factor": False,    },
    {
      "hi": "आप किस प्रकार के मूड परिवर्तनों का अनुभव करते हैं (जैसे, बहुत खुश या बहुत उदास महसूस करना)?",
      "en": "What types of mood changes do you experience (e.g., feeling very happy or very sad)?",
      "category": "mood_swings",
      "symptom": "types of mood changes",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके मूड स्विंग्स कुछ विशेष घटनाओं या परिस्थितियों द्वारा प्रेरित होते हैं?",
      "en": "Do your mood swings seem to be triggered by specific events or situations?",
      "category": "mood_swings",
      "symptom": "triggers of mood swings",
      "risk_factor": False,    },
    {
      "hi": "क्या आप मूड स्विंग्स के बीच चिड़चिड़े, चिंतित, या अवसादित महसूस करते हैं?",
      "en": "Do you feel irritable, anxious, or depressed between mood swings?",
      "category": "mood_swings",
      "symptom": "mood between swings",
      "risk_factor": False,    },
    {
      "hi": "क्या आपने अपने मूड परिवर्तनों में कोई पैटर्न देखा है, जैसे दिन के कुछ विशेष समयों या सप्ताह के दिनों में?",
      "en": "Have you noticed any patterns in your mood changes, such as certain times of the day or during the week?",
      "category": "mood_swings",
      "symptom": "patterns of mood changes",
      "risk_factor": False,    },
    {
      "hi": "क्या आपने हाल ही में कोई बड़ा जीवन परिवर्तन, तनावपूर्ण घटना या आघातक अनुभव किया है?",
      "en": "Have you experienced any major life stressors, changes, or traumatic events recently?",
      "category": "mood_swings",
      "symptom": "recent life stressors or trauma",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके परिवार में मूड विकारों, जैसे बाइपोलर डिसऑर्डर या अवसाद का इतिहास है?",
      "en": "Do you have a family history of mood disorders, such as bipolar disorder or depression?",
      "category": "mood_swings",
      "symptom": "family history of mood disorders",
      "risk_factor": False,    },
    {
      "hi": "क्या आप कोई दवाइयाँ ले रहे हैं, जिसमें ओवर-द-काउंटर दवाइयाँ या हर्बल सप्लीमेंट्स शामिल हैं, जो आपके मूड को प्रभावित कर सकते हैं?",
      "en": "Are you taking any medications, including over-the-counter or herbal supplements, that could affect your mood?",
      "category": "mood_swings",
      "symptom": "medication use affecting mood",
      "risk_factor": False,    },
  ],

  "difficulty concentrating": [
    {
      "hi": "क्या एकाग्रता में कठिनाई स्थायी है या कभी-कभी होती है?",
      "en": "Is the difficulty with concentration constant or does it come and go?",
      "category": "difficulty_concentrating",
      "symptom": "constant vs intermittent concentration difficulty",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको विशिष्ट कार्यों पर ध्यान केंद्रित करने में कठिनाई हो रही है, या यह अधिक सामान्य है?",
      "en": "Do you find it hard to focus on specific tasks, or is it more general?",
      "category": "difficulty_concentrating",
      "symptom": "focus on tasks",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको चीज़ों को याद करने या कार्यों को पूरा करने में समस्या हो रही है?",
      "en": "Do you have trouble remembering things or following through with tasks?",
      "category": "difficulty_concentrating",
      "symptom": "memory and task completion",
      "risk_factor": False,    },
    {
      "hi": "क्या आप अन्य लक्षणों का अनुभव कर रहे हैं, जैसे थकावट, चिड़चिड़ापन, या नींद की समस्याएं?",
      "en": "Are you experiencing any other symptoms, such as fatigue, irritability, or sleep problems?",
      "category": "difficulty_concentrating",
      "symptom": "associated symptoms (fatigue, irritability, sleep problems)",
      "risk_factor": False,    },
    {
      "hi": "क्या आपने हाल ही में कोई महत्वपूर्ण तनाव, चिंता, या भावनात्मक समस्याएं अनुभव की हैं?",
      "en": "Have you recently experienced significant stress, anxiety, or emotional challenges?",
      "category": "difficulty_concentrating",
      "symptom": "stress, anxiety, or emotional challenges",
      "risk_factor": True,    },
    {
      "hi": "क्या आपको मानसिक स्वास्थ्य स्थितियों का कोई इतिहास है, जैसे ADHD, अवसाद, या चिंता?",
      "en": "Do you have a history of mental health conditions, such as ADHD, depression, or anxiety?",
      "category": "difficulty_concentrating",
      "symptom": "mental health history",
      "risk_factor": True,    },
    {
      "hi": "क्या आप वर्तमान में कोई दवाइयाँ या सप्लीमेंट्स ले रहे हैं जो आपके ध्यान को प्रभावित कर सकते हैं?",
      "en": "Are you currently taking any medications or supplements that could affect your focus?",
      "category": "difficulty_concentrating",
      "symptom": "medications affecting concentration",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको कोई मेडिकल स्थितियां हैं, जैसे थायरॉयड समस्या, मधुमेह, या स्लीप एपनिया, जो आपकी एकाग्रता को प्रभावित कर सकती हैं?",
      "en": "Do you have any medical conditions, such as thyroid problems, diabetes, or sleep apnea, that could affect your concentration?",
      "category": "difficulty_concentrating",
      "symptom": "medical conditions affecting concentration",
      "risk_factor": False,    },
    {
      "hi": "क्या आपने अपनी जीवनशैली में कोई परिवर्तन महसूस किया है, जैसे नींद की खराब आदतें, आहार, या व्यायाम स्तर, जो एकाग्रता में कठिनाई का कारण हो सकते हैं?",
      "en": "Have you had any changes in your lifestyle, such as poor sleep habits, diet, or exercise levels, that might be contributing to the difficulty concentrating?",
      "category": "difficulty_concentrating",
      "symptom": "lifestyle changes affecting concentration",
      "risk_factor": False,    },
  ],

  "hallucination": [

    {
      "hi": "आप किस प्रकार की भ्रांतियाँ अनुभव कर रहे हैं (जैसे, आवाजें सुनना, चीज़ें देखना, गंध महसूस करना)?",
      "en": "What type of hallucinations are you experiencing (e.g., hearing voices, seeing things, smelling odors)?",
      "category": "hallucinations",
      "symptom": "type of hallucinations",
      "risk_factor": False,    },
    {
      "hi": "क्या भ्रांतियाँ दिन में, रात में, या दोनों समय होती हैं?",
      "en": "Are the hallucinations occurring during the day, at night, or both?",
      "category": "hallucinations",
      "symptom": "time of hallucinations",
      "risk_factor": False,    },
    {
      "hi": "क्या भ्रांतियाँ आपको वास्तविक लगती हैं, या आप उन्हें झूठी पहचानते हैं?",
      "en": "Do the hallucinations seem real to you, or do you recognize them as being false?",
      "category": "hallucinations",
      "symptom": "real or false perception",
      "risk_factor": False,    },
    {
      "hi": "क्या भ्रांतियाँ किसी विशिष्ट उत्तेजक से जुड़ी हुई हैं, जैसे तनाव, नींद की कमी, या कुछ परिस्थितियाँ?",
      "en": "Are the hallucinations associated with any specific triggers, such as stress, sleep deprivation, or certain situations?",
      "category": "hallucinations",
      "symptom": "triggers for hallucinations",
      "risk_factor": False,    },
    {
      "hi": "क्या आपने अपनी मानसिक स्थिति में कोई परिवर्तन महसूस किया है, जैसे मूड स्विंग्स, चिंता, या अवसाद?",
      "en": "Have you experienced any changes in your mental health, such as mood swings, anxiety, or depression?",
      "category": "hallucinations",
      "symptom": "mental health changes",
      "risk_factor": False,    },
    {
      "hi": "क्या आप कोई दवाइयाँ, ओवर-द-काउंटर दवाइयाँ, या अवैध नशीली दवाएँ ले रहे हैं?",
      "en": "Are you taking any medications, including prescription, over-the-counter, or recreational drugs?",
      "category": "hallucinations",
      "symptom": "medications or drugs",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके पास मानसिक स्वास्थ्य स्थितियों का कोई इतिहास है, जैसे स्किजोफ्रेनिया, बाइपोलर डिसऑर्डर, या प्रमुख अवसाद?",
      "en": "Do you have any history of mental health conditions, such as schizophrenia, bipolar disorder, or major depression?",
      "category": "hallucinations",
      "symptom": "mental health history",
      "risk_factor": True,    },
    {
      "hi": "क्या आपको हाल ही में सिर की चोट, संक्रमण, या तंत्रिका तंत्र से संबंधित कोई समस्या हुई है, जो आपके मस्तिष्क को प्रभावित कर सकती है?",
      "en": "Have you had any recent head injuries, infections, or neurological conditions that might affect your brain?",
      "category": "hallucinations",
      "symptom": "head injuries or neurological conditions",
      "risk_factor": False,    },
  ],

  "lack of motivation": [
    {
      "hi": "क्या प्रेरणा की कमी लगातार है, या यह आती-जाती रहती है?",
      "en": "Is the lack of motivation constant, or does it come and go?",
      "category": "lack_of_motivation",
      "symptom": "consistency of lack of motivation",
      "risk_factor": False,    },
    {
      "hi": "क्या कुछ विशेष गतिविधियाँ या कार्य हैं जिन्हें करने के लिए आपको प्रेरणा की कमी महसूस होती है (जैसे काम, शौक, सामाजिक गतिविधियाँ)?",
      "en": "Are there specific activities or tasks you feel unmotivated to do (e.g., work, hobbies, socializing)?",
      "category": "lack_of_motivation",
      "symptom": "specific activities affected by lack of motivation",
      "risk_factor": False,    },
    {
      "hi": "क्या आपने अपनी ऊर्जा स्तर या ध्यान केंद्रित करने की क्षमता में कोई बदलाव महसूस किया है?",
      "en": "Have you noticed any changes in your energy levels or ability to focus?",
      "category": "lack_of_motivation",
      "symptom": "changes in energy and focus",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको ऐसा महसूस हो रहा है कि आप कार्य शुरू करने में असमर्थ हैं, यहां तक कि वे कार्य जिन्हें आप पहले पसंद करते थे?",
      "en": "Do you feel overwhelmed or unable to start tasks, even ones you used to enjoy?",
      "category": "lack_of_motivation",
      "symptom": "difficulty starting tasks",
      "risk_factor": False,    },
    {
      "hi": "क्या हाल ही में कोई महत्वपूर्ण जीवन परिवर्तन, तनाव, या मानसिक चुनौतियाँ आई हैं?",
      "en": "Have there been any significant life changes, stressors, or emotional challenges recently?",
      "category": "lack_of_motivation",
      "symptom": "life changes or stressors",
      "risk_factor": False,    },
    {
      "hi": "क्या आप अच्छे से सो रहे हैं, या आपकी नींद के पैटर्न में कोई बदलाव आया है (जैसे, अनिद्रा या अत्यधिक सोना)?",
      "en": "Are you sleeping well, or have you experienced any changes in your sleep patterns (e.g., insomnia or excessive sleeping)?",
      "category": "lack_of_motivation",
      "symptom": "changes in sleep patterns",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके पास मानसिक स्वास्थ्य की कोई पूर्ववर्ती स्थिति है, जैसे अवसाद, चिंता, या ADHD?",
      "en": "Do you have a history of mental health conditions, such as depression, anxiety, or ADHD?",
      "category": "lack_of_motivation",
      "symptom": "history of mental health conditions",
      "risk_factor": False,    },
    {
      "hi": "क्या आप कोई दवाइयाँ ले रहे हैं, जिसमें प्रेसक्रिप्शन, ओवर-द-काउंटर, या अवैध नशीली दवाएँ शामिल हैं?",
      "en": "Are you currently taking any medications, including prescription, over-the-counter, or recreational drugs?",
      "category": "lack_of_motivation",
      "symptom": "medications or drugs",
      "risk_factor": False,    },
  ],

  "bone fracture": [
    {
      "hi": "फ्रैक्चर कैसे हुआ (जैसे गिरना, दुर्घटना, खेलों की चोट)?",
      "en": "How did the fracture occur (e.g., fall, accident, sports injury)?",
      "category": "bone_fracture",
      "symptom": "cause of fracture",
      "risk_factor": False,    },
    {
      "hi": "कौन सा हड्डी फ्रैक्चर हुई है, और दर्द कहाँ है?",
      "en": "Which bone is fractured, and where is the pain located?",
      "category": "bone_fracture",
      "symptom": "location and type of fracture",
      "risk_factor": False,    },

   {
  "hi": "क्या आपको फ्रैक्चर के बाद हड्डी में दर्द, सूजन या असामान्य रूप से गर्मी महसूस हो रही है?",
  "en": "After the fracture, are you experiencing pain, swelling, or unusual warmth in the bone?",
  "category": "bone_fracture",
  "symptom": "pain, swelling, or warmth",
  "risk_factor": False,
},
    {
      "hi": "क्या आपको प्रभावित अंग या जोड़ों को हिलाने में कठिनाई हो रही है?",
      "en": "Do you have difficulty moving the affected limb or joint?",
      "category": "bone_fracture",
      "symptom": "difficulty moving affected limb",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके पास पहले कोई फ्रैक्चर या हड्डी की चोटें रही हैं?",
      "en": "Have you had any previous fractures or bone injuries?",
      "category": "bone_fracture",
      "symptom": "history of fractures or bone injuries",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके परिवार में हड्डी संबंधित समस्याएँ या हड्डी की मजबूती को प्रभावित करने वाली स्थितियाँ हैं?",
      "en": "Do you have a family history of bone problems or conditions that affect bone strength?",
      "category": "bone_fracture",
      "symptom": "family history of bone problems",
      "risk_factor": True,    },
  ],

  "bone pain": [
    {
      "hi": "हड्डी का दर्द कहाँ स्थित है?",
      "en": "Where exactly is the bone pain located?",
      "category": "bone_pain",
      "symptom": "location of bone pain",
      "risk_factor": False,    },
    {
      "hi": "क्या हड्डी में दर्द लगातार बना रहता है, या आता-जाता रहता है?",
      "en": "Is the bone pain constant, or does it come and go?",
      "category": "bone_pain",
      "symptom": "nature of bone pain",
      "risk_factor": False,    },
    {
      "hi": "क्या हड्डी का दर्द तेज़, सुस्त, धड़क रहा है या दर्द कर रहा है?",
      "en": "Is the bone pain sharp, dull, throbbing, or aching?",
      "category": "bone_pain",
      "symptom": "type of bone pain",
      "risk_factor": False,    },
    {
      "hi": "क्या हिलने-डुलने, दबाव पड़ने या कुछ गतिविधियों से हड्डी का दर्द बढ़ जाता है?",
      "en": "Does the bone pain get worse with movement, pressure, or certain activities?",
      "category": "bone_pain",
      "symptom": "pain exacerbation",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको हाल ही में कोई चोटें, गिरना या दुर्घटनाएं हुई हैं?",
      "en": "Have you had any recent injuries, falls, or accidents?",
      "category": "bone_pain",
      "symptom": "recent injuries or accidents",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको प्रभावित क्षेत्र के आसपास सूजन, चोट, या लाली महसूस हो रही है?",
      "en": "Are you experiencing any swelling, bruising, or redness around the affected area?",
      "category": "bone_pain",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या आपने प्रभावित अंग या जोड़ों में कमजोरी, सुन्नता, या आंदोलन में कठिनाई महसूस की है?",
      "en": "Have you noticed any weakness, numbness, or difficulty moving the affected limb or joint?",
      "category": "bone_pain",
      "symptom": "weakness or difficulty moving",
      "risk_factor": False,    },
  ],

  "sprain": [
    {
      "hi": "स्ट्रेन कैसे हुआ (जैसे, गिरना, खेल की चोट, दुर्घटना)?",
      "en": "How did the sprain occur (e.g., fall, sports injury, accident)?",
      "category": "sprain",
      "symptom": "mechanism of injury",
      "risk_factor": False,    },
    {
      "hi": "कौन सा जोड़ा या लिगामेंट घायल हुआ है?",
      "en": "Which joint or ligament is injured?",
      "category": "sprain",
      "symptom": "injured joint or ligament",
      "risk_factor": False,    },
    {
      "hi": "क्या लिगामेंट में दर्द लगातार बना रहता है, या यह हिलने-डुलने या दबाव के साथ बदलता रहता है?",
      "en": "Is the ligament pain constant, or does it vary with movement or pressure?",
      "category": "sprain",
      "symptom": "pain variation",
      "risk_factor": False,    },
    {
      "hi": "क्या घायल क्षेत्र के आसपास सूजन, चोट या लाली है?",
      "en": "Is there swelling, bruising, or redness around the injured area?",
      "category": "sprain",
      "symptom": "swelling, bruising, or redness",
      "risk_factor": False,    },
    {
      "hi": "क्या आप प्रभावित जोड़े को हिला सकते हैं, या यह हिलाने में बहुत दर्द होता है?",
      "en": "Can you move the affected joint, or is it too painful tomove?",
      "category": "sprain",
      "symptom": "joint movement",
      "risk_factor": False,    },
    {
  "hi": "क्या चोट के बाद आपको जोड़े में स्थिरता या अस्थिरता का अनुभव हो रहा है?",
  "en": "After the injury, do you feel any instability or weakness in the joint?",
  "category": "sprain",
  "symptom": "joint instability or weakness",
  "risk_factor": False,
},
    {
      "hi": "क्या आपने उसी जोड़े में पहले कभी कोई स्ट्रेन या चोट लगाई है?",
      "en": "Have you had any previous sprains or injuries to the same joint?",
      "category": "sprain",
      "symptom": "previous injuries",
      "risk_factor": False,    },
  ],

"injury": [
  {
    "hi": "क्या चोट के बाद दर्द लगातार बना रहता है, या हिलने-डुलने या विशिष्ट गतिविधियों से यह बढ़ जाता है?",
    "en": "Is the pain after injury constant, or does it worsen with movement or specific activities?",
    "category": "general injury",
    "symptom": "pain variation with movement",
    "risk_factor": False,
  },
  {
    "hi": "क्या आप प्रभावित क्षेत्र को हिला सकते हैं, या यह हिलाने में बहुत दर्दनाक या अस्थिर है?",
    "en": "Can you move the affected area, or is it too painful or unstable to do so?",
    "category": "general injury",
    "symptom": "movement limitation",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपने पहले कभी उसी क्षेत्र में चोट या बार-बार समस्याएँ महसूस की हैं?",
    "en": "Have you had any previous injuries or recurring problems in the same area?",
    "category": "general injury",
    "symptom": "previous injuries",
    "risk_factor": False,
  },
],

  "gout": [

    {
      "hi": "कौन सा जोड़ा प्रभावित है, और क्या वह सूजा हुआ, लाल, या छूने पर गर्म है?",
      "en": "Which joint is affected, and is it swollen, red, or warm to the touch?",
      "category": "gout",
      "symptom": "affected joint and signs",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको पहले कभी इसी तरह के लक्षण हुए थे, या यह गाउट का पहला दौरा है?",
      "en": "Have you had similar symptoms in the past, or is this your first episode of gout?",
      "category": "gout",
      "symptom": "previous episodes",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको प्रभावित जोड़े में विशेष रूप से रात के समय तीव्र दर्द हो रहा है?",
      "en": "Are you experiencing severe pain in the affected joint, especially at night?",
      "category": "gout",
      "symptom": "pain severity and timing",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको उच्च यूरिक एसिड स्तर का इतिहास है, या क्या आपको पहले गाउट का निदान किया गया था?",
      "en": "Do you have a history of high uric acid levels, or have you been diagnosed with gout before?",
      "category": "gout",
      "symptom": "history of uric acid or gout",
      "risk_factor": True,    },
    {
      "hi": "क्या आपने प्यूरीन से भरपूर खाद्य पदार्थों या पेय पदार्थों का सेवन किया है, जैसे लाल मांस, शंख, या शराब, विशेष रूप से बीयर या शराब?",
      "en": "Have you been consuming foods or drinks high in purines, such as red meat, shellfish, or alcohol, especially beer or liquor?",
      "category": "gout",
      "symptom": "dietary triggers",
      "risk_factor": True,    },
    {
      "hi": "क्या आप वर्तमान में कोई दवाइयाँ ले रहे हैं, विशेष रूप से मूत्रवर्धक, एस्पिरिन, या उच्च रक्तचाप या अन्य स्थितियों के लिए दवाइयाँ?",
      "en": "Are you currently taking any medications, particularly diuretics, aspirin, or medications for blood pressure or other conditions?",
      "category": "gout",
      "symptom": "medications",
      "risk_factor": False,    },

  ],

  "sciatica": [
    {
      "hi": "कटिस्नायुशूल का दर्द कहाँ स्थित है (उदाहरण के लिए, पीठ के निचले हिस्से, नितंब, पैर, पैर)?",
      "en": "Where is the sciatica pain located (e.g., lower back, buttocks, legs, feet)?",
      "category": "sciatica",
      "symptom": "location of pain",
      "risk_factor": False,    },
    {
      "hi": "क्या साइटिका का दर्द लगातार बना रहता है, या यह आता-जाता रहता है?",
      "en": "Is the sciatica pain constant, or does it come and go?",
      "category": "sciatica",
      "symptom": "pain pattern",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको एक पैर में या दोनों पैरों में दर्द, सुन्नता, या झुनझुनी महसूस होती है?",
      "en": "Do you experience pain, numbness, or tingling down one leg or both legs?",
      "category": "sciatica",
      "symptom": "unilateral or bilateral symptoms",
      "risk_factor": False,    },
    {
      "hi": "क्या कटिस्नायुशूल का दर्द तेज, जलन वाला या अधिक हल्का दर्द है?",
      "en": "Is the sciatica pain sharp, burning, or more of a dull ache?",
      "category": "sciatica",
      "symptom": "pain type",
      "risk_factor": False,    },
    {
      "hi": "क्या कुछ विशेष गतिविधियाँ या स्थितियाँ जैसे बैठना, खड़ा होना, खांसी या छींकने से दर्द बढ़ता है?",
      "en": "Does anything trigger or worsen the pain, such as sitting, standing, coughing, or sneezing?",
      "category": "sciatica",
      "symptom": "pain triggers",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको कोई अन्य चिकित्सीय स्थिति है, जैसे हर्नियेटेड डिस्क, डीजनरेटिव डिस्क रोग, या स्पाइनल स्टेनोसिस?",
      "en": "Do you have any other medical conditions, such as herniated discs, degenerative disc disease, or spinal stenosis?",
      "category": "sciatica",
      "symptom": "underlying medical conditions",
      "risk_factor": False,    },
    {
      "hi": "क्या आप वर्तमान में कोई दवाइयाँ ले रहे हैं, और क्या आपने साइटिका के दर्द के लिए किसी उपचार (जैसे फिजिकल थेरेपी, विश्राम, दर्द निवारण) की कोशिश की है?",
      "en": "Are you currently taking any medications, and have you tried any treatments (e.g., physical therapy, rest, pain relief) for the sciatica pain?",
      "category": "sciatica",
      "symptom": "medications and treatments",
      "risk_factor": False,    },
  ],
  
  "arthritis": [
    {
      "hi": "कौन से जोड़ों में समस्या है (जैसे घुटने, हाथ, कूल्हे, उंगलियाँ)?",
      "en": "Which joints are affected (e.g., knees, hands, hips, fingers)?",
      "category": "arthritis",
      "symptom": "location of pain",
      "risk_factor": False,    },
    {
      "hi": "क्या दर्द लगातार है, या यह आता-जाता रहता है?",
      "en": "Is the pain constant, or does it come and go?",
      "category": "arthritis",
      "symptom": "pain pattern",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको सुबह के समय जकड़न महसूस होती है, और यदि होती है, तो यह कितनी देर तक रहती है?",
      "en": "Do you experience morning stiffness, and if so, how long does it last?",
      "category": "arthritis",
      "symptom": "morning stiffness",
      "risk_factor": False,    },
    {
      "hi": "क्या आपने प्रभावित जोड़ों में सूजन, लाली, या गर्मी महसूस की है?",
      "en": "Have you noticed any swelling, redness, or warmth in the affected joints?",
      "category": "arthritis",
      "symptom": "joint swelling and inflammation",
      "risk_factor": False,    },
    {
      "hi": "क्या दर्द कुछ गतिविधियों के साथ बेहतर या खराब होता है (जैसे विश्राम, व्यायाम, मौसम में बदलाव)?",
      "en": "Does the pain improve or worsen with certain activities (e.g., rest, exercise, weather changes)?",
      "category": "arthritis",
      "symptom": "activity-related pain changes",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको दैनिक गतिविधियाँ करने में कठिनाई हो रही है, जैसे चलना, टाइप करना, या जार खोलना?",
      "en": "Do you have difficulty performing daily activities, such as walking, typing, or opening jars?",
      "category": "arthritis",
      "symptom": "difficulty with daily activities",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके परिवार में आर्थ्राइटिस या अन्य ऑटोइम्यून बीमारियों का इतिहास है, जैसे रुमेटोइड आर्थ्राइटिस या ल्यूपस?",
      "en": "Do you have a family history of arthritis or other autoimmune conditions, such as rheumatoid arthritis or lupus?",
      "category": "arthritis",
      "symptom": "family history of arthritis",
      "risk_factor": True,    },
    {
      "hi": "क्या आप वर्तमान में कोई दवाइयाँ ले रहे हैं, जिसमें दर्द निवारक, या आपने कोई उपचार (जैसे शारीरिक चिकित्सा, जीवनशैली में बदलाव) किया है?",
      "en": "Are you currently taking any medications, including pain relievers, or have you tried any treatments (e.g., physical therapy, lifestyle changes)?",
      "category": "arthritis",
      "symptom": "medication and treatment history",
      "risk_factor": True,    },
    ],

  "loss of appetite": [
    {
      "hi": "क्या भूख न लगने की समस्या निरंतर है, या यह आती-जाती रहती है?",
      "en": "Is the loss of appetite constant, or does it come and go?",
      "category": "loss_of_appetite",
      "symptom": "pattern",
      "risk_factor": False,    },
    {
      "hi": "क्या आपने अपनी खाने की आदतों में कोई और बदलाव महसूस किया है, जैसे थोड़ी मात्रा में खाने के बाद भी पेट भर जाना या कुछ खास प्रकार के खाद्य पदार्थों से बचना?",
      "en": "Have you noticed any other changes in your eating habits, such as feeling full after eating small amounts or avoiding certain types of food?",
      "category": "loss_of_appetite",
      "symptom": "eating habits",
      "risk_factor": False,    },
    {
      "hi": "क्या आप कोई दवाइयां ले रहे हैं, और क्या वे आपकी भूख पर प्रभाव डाल सकती हैं (जैसे दर्द निवारक, एंटीडिप्रेसेंट्स, या कीमोथेरेपी)?",
      "en": "Are you currently taking any medications, and could they be affecting your appetite (e.g., painkillers, antidepressants, or chemotherapy)?",
      "category": "loss_of_appetite",
      "symptom": "medications",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको कोई शारीरिक स्वास्थ्य समस्याएं हैं, जैसे गैस्ट्रोइंटेस्टाइनल विकार, संक्रमण, थायरॉयड समस्या, या मानसिक स्वास्थ्य समस्याएं (जैसे अवसाद या खाने से संबंधित विकार)?",
      "en": "Do you have any underlying health conditions, such as gastrointestinal disorders, infections, thyroid problems, or mental health conditions (e.g., depression or eating disorders)?",
      "category": "loss_of_appetite",
      "symptom": "underlying health conditions",
      "risk_factor": False,    },
    {
      "hi": "क्या आपने हाल ही में कोई संक्रमण, बुखार, या अन्य बीमारियां अनुभव की हैं जो भूख कम होने का कारण बन सकती हैं?",
      "en": "Have you had any recent infections, fevers, or other illnesses that could be contributing to the loss of appetite?",
      "category": "loss_of_appetite",
      "symptom": "recent illnesses",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको अपनी स्वाद या गंध की भावना में कोई बदलाव महसूस हुआ है, या खाने में कठिनाई हो रही है?",
      "en": "Have you noticed any changes in your sense of taste or smell, or difficulty swallowing food?",
      "category": "loss_of_appetite",
      "symptom": "taste/smell or swallowing",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको खाने से संबंधित कोई एलर्जी, पाचन समस्याएं, या पुरानी बीमारियां हैं जो भूख को प्रभावित कर सकती हैं?",
      "en": "Do you have a history of food allergies, digestive issues, or chronic conditions that might affect your appetite?",
      "category": "loss_of_appetite",
      "symptom": "history of digestive or food-related issues",
      "risk_factor": True,    },
  ],

    "migraine": [
  {
    "hi": "क्या आप दर्द का प्रकार वर्णित कर सकते हैं? (जैसे की धड़कता, पल्सिंग, चुभने वाला)",
    "en": "Can you describe the type of pain (e.g., throbbing, pulsating, stabbing)?",
    "category": "migraine",
    "symptom": "migraine",
    "risk_factor": False,
  },
  {
    "hi": "क्या माइग्रेन से पहले कोई चेतावनी संकेत या लक्षण होते हैं? (जैसे की आरा, दृश्य समस्याएं)",
    "en": "Do you experience any warning signs or symptoms before the migraine (e.g., aura, visual disturbances)?",
    "category": "migraine",
    "symptom": "migraine",
    "risk_factor": False,
  },
  {
    "hi": "क्या कुछ विशिष्ट कारक होते हैं जो आपके माइग्रेन को उत्तेजित करते हैं? (जैसे की तनाव, कुछ खाद्य पदार्थ, नींद की कमी)",
    "en": "Are there specific triggers that seem to bring on your migraines (e.g., stress, certain foods, lack of sleep)?",
    "category": "migraine",
    "symptom": "migraine",
    "risk_factor": False,
  },
  {
    "hi": "आपके माइग्रेन आपके दैनिक जीवन या गतिविधियों को कैसे प्रभावित करते हैं?",
    "en": "How do your migraines affect your daily life or activities?",
    "category": "migraine",
    "symptom": "migraine",
    "risk_factor": False,
  }
],

    "swollen lymph nodes": [
  {
    "hi": "सूजे हुए लिम्फ नोड्स कहां स्थित हैं? (जैसे गर्दन, बगल, कमर)",
    "en": "Where exactly are the swollen lymph nodes located? (e.g., neck, underarms, groin)",
    "category": "swollen lymph nodes",
    "symptom": "swollen lymph nodes",
    "risk_factor": False,
  },
  {
    "hi": "क्या लिम्फ नोड्स दबाने पर दर्दनाक या कोमल हैं?",
    "en": "Are the lymph nodes painful or tender to the touch?",
    "category": "swollen lymph nodes",
    "symptom": "swollen lymph nodes",
    "risk_factor": False,
  },
  {
    "hi": "क्या सूजे हुए लिम्फ नोड्स के आकार या स्थिरता में पहले देखे गए लक्षणों से कोई बदलाव हुआ है?",
    "en": "Have the swollen lymph nodes changed in size or consistency since you first noticed them?",
    "category": "swollen lymph nodes",
    "symptom": "swollen lymph nodes",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको ऐसी कोई बीमारी का इतिहास है जो इम्यून सिस्टम या लिम्फैटिक सिस्टम को प्रभावित करती है? (जैसे ऑटोइम्यून बीमारियां, कैंसर, एचआईवी)",
    "en": "Do you have a history of conditions that affect the immune system or lymphatic system (e.g., autoimmune diseases, cancer, HIV)?",
    "category": "swollen lymph nodes",
    "symptom": None,
    "risk_factor": True,
  },
  {
    "hi": "क्या आपको संक्रमण के संभावित स्रोतों का सामना हुआ है? (जैसे बीमार संपर्क, ऐसी जगहों पर यात्रा जहां एंडेमिक बीमारियां हैं)",
    "en": "Have you been exposed to any potential sources of infection (e.g., sick contacts, travel to areas with endemic diseases)?",
    "category": "swollen lymph nodes",
    "symptom": None,
    "risk_factor": False,
  }
],

    "skin burning": [
  {
    "hi": "क्या जलन का एहसास लगातार है, या यह कभी-कभी होता है?",
    "en": "Is the burning sensation constant, or does it come and go?",
    "category": "skin burning",
    "symptom": "skin burning",
    "risk_factor": False,
  },
  {
    "hi": "आपकी त्वचा के कौन से हिस्से जलन से प्रभावित हैं?",
    "en": "Which areas of your skin are affected by the burning sensation?",
    "category": "skin burning",
    "symptom": "skin burning",
    "risk_factor": False,
  },
  {
    "hi": "क्या जलन के साथ कोई लाली, सूजन, या दाने हैं?",
    "en": "Is the burning accompanied by any redness, swelling, or rashes?",
    "category": "skin burning",
    "symptom": None,
    "risk_factor": False,
  },
  {
    "hi": "क्या आपने हाल ही में कोई नई दवाइयां या उपचार शुरू किया है जो त्वचा की जलन या संवेदनशीलता का कारण बन सकते हैं?",
    "en": "Have you recently started any new medications or treatments that could cause skin irritation or sensitivity?",
    "category": "skin burning",
    "symptom": "skin burning",
    "risk_factor": False,
  }
    ],
"bleeding": [

    {
      "hi": "आप कितनी मात्रा में खून खो रहे हैं?",
      "en": "How much blood are you losing?",
      "category": "bleeding",
      "symptom": "bleeding",
      "risk_factor": False,
    },
    {
      "hi": "क्या खून बहना लगातार है या यह कभी-कभी होता है?",
      "en": "Is the bleeding continuous or intermittent?",
      "category": "bleeding",
      "symptom": "bleeding",
      "risk_factor": False,
    },
],
"anxiety": [
    {
      "hi": "क्या आपकी चिंता का कारण विशेष परिस्थितियाँ, विचार, या घटनाएँ हैं?",
      "en": "What triggers your anxiety (specific situations, thoughts, or events)?",
      "category": "anxiety",
      "symptom": "anxiety",
      "risk_factor": False,
    },
    {
      "hi": "क्या आप अपनी चिंता का कारण कुछ विशेष परिस्थितियों से बचते हैं?",
      "en": "Do you avoid certain situations because of your anxiety?",
      "category": "anxiety",
      "symptom": "anxiety",
      "risk_factor": False,
    },
    {
      "hi": "आप अपनी चिंता से निपटने या उसे प्रबंधित करने के लिए क्या उपाय करते हैं?",
      "en": "How do you cope with or manage your anxiety?",
      "category": "anxiety",
      "symptom": "anxiety",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपके परिवार में चिंता या अन्य मानसिक स्वास्थ्य समस्याओं का इतिहास है?",
      "en": "Do you have a history of anxiety or other mental health conditions in your family?",
      "category": "anxiety",
      "symptom": "anxiety",
      "risk_factor": False,
    }
],
    "cancer": [
    {
      "hi": "क्या आपने कोई अप्रत्याशित वजन घटने का अनुभव किया है?",
      "en": "Have you noticed any unexplained weight loss?",
      "category": "cancer",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको कोई लगातार दर्द या असुविधा महसूस हो रही है?",
      "en": "Do you have any persistent pain or discomfort?",
      "category": "cancer",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने अपनी त्वचा में कोई बदलाव महसूस किया है, जैसे नए मस्से या वृद्धि?",
      "en": "Have you experienced any changes in your skin, such as new moles or growths?",
      "category": "cancer",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आप किसी असामान्य रक्तस्राव या स्राव का अनुभव कर रहे हैं?",
      "en": "Are you experiencing any unusual bleeding or discharge?",
      "category": "cancer",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको निगलने में कोई कठिनाई या लगातार खांसी का अनुभव हुआ है?",
      "en": "Have you had any difficulty swallowing or persistent cough?",
      "category": "cancer",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको आंत्र या मूत्र संबंधी आदतों में कोई बदलाव महसूस हुआ है (जैसे, मल में खून, बार-बार पेशाब आना)?",
      "en": "Do you have any changes in bowel or urinary habits (e.g., blood in stool, frequent urination)?",
      "category": "cancer",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको कोई असामान्य थकान या कमजोरी महसूस हो रही है जो आराम करने से ठीक नहीं होती?",
      "en": "Have you had any unusual fatigue or weakness that does not improve with rest?",
      "category": "cancer",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपके परिवार में कैंसर या आनुवंशिक प्रवृत्तियाँ हैं?",
      "en": "Do you have a family history of cancer or genetic predispositions?",
      "category": "cancer",
      "symptom": "cancer",
      "risk_factor": False,
    }
],
    "weight loss": [
    {
      "hi": "आपने कितनी वजन कम की है, और यह कितने समय में हुआ है?",
      "en": "How much weight have you lost, and over what period of time?",
      "category": "weight loss",
      "symptom": "weight loss",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने अपनी भूख में कोई बदलाव महसूस किया है?",
      "en": "Have you noticed any changes in your appetite?",
      "category": "weight loss",
      "symptom": "weight loss",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको खाने या निगलने में कोई कठिनाई हो रही है?",
      "en": "Are you experiencing any difficulty eating or swallowing?",
      "category": "weight loss",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने हाल ही में कोई बीमारी, संक्रमण या स्वास्थ्य समस्याएँ अनुभव की हैं?",
      "en": "Have you had any recent illnesses, infections, or health conditions?",
      "category": "weight loss",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको थायरॉयड समस्याएँ, डायबिटीज़, या अन्य चयापचय विकारों का इतिहास है?",
      "en": "Do you have a history of thyroid problems, diabetes, or other metabolic disorders?",
      "category": "weight loss",
      "symptom": None,
      "risk_factor": True,
    }
],
    "frequent urination": [
    {
      "hi": "आपको दिन और रात में कितनी बार पेशाब करने की आवश्यकता होती है?",
      "en": "How often do you need to urinate during the day and night?",
      "category": "frequent urination",
      "symptom": "frequent urination",
      "risk_factor": False,
    },
    {
      "hi": "क्या पेशाब करते समय कोई दर्द या असुविधा हो रही है?",
      "en": "Is there any pain or discomfort when urinating?",
      "category": "frequent urination",
      "symptom": "frequent urination",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने पेशाब के रंग, गंध, या रूप में कोई बदलाव देखा है?",
      "en": "Have you noticed any changes in the color, odor, or appearance of your urine?",
      "category": "frequent urination",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको पेशाब करने की अत्यधिक आवश्यकता या तात्कालिकता महसूस हो रही है?",
      "en": "Are you experiencing any urgency or a strong need to urinate?",
      "category": "frequent urination",
      "symptom": "frequent urination",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने हाल ही में कोई मूत्र मार्ग संक्रमण (UTIs) या मूत्राशय की समस्याएं अनुभव की हैं?",
      "en": "Have you had any recent urinary tract infections (UTIs) or bladder issues?",
      "category": "frequent urination",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आप सामान्य से अधिक तरल पदार्थ पी रहे हैं, या आपके आहार में कोई बदलाव हुआ है?",
      "en": "Are you drinking more fluids than usual, or have there been any changes to your diet?",
      "category": "frequent urination",
      "symptom": "frequent urination",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको डायबिटीज़ या गुर्दे या मूत्राशय से संबंधित अन्य चिकित्सा समस्याओं का इतिहास है?",
      "en": "Do you have a history of diabetes or any other medical conditions affecting the kidneys or bladder?",
      "category": "frequent urination",
      "symptom": None,
      "risk_factor": True,
    },
],
    "strain": [
    {
      "hi": "चोट कैसे लगी? (जैसे, अचानक हरकत, उठाना, या व्यायाम)",
      "en": "How did the injury occur? (e.g., sudden movement, lifting, or exercise)",
      "category": "strain",
      "symptom": "strain",
      "risk_factor": False,
    },
    {
      "hi": "शरीर का कौन सा हिस्सा प्रभावित है?",
      "en": "Which part of the body is affected?",
      "category": "strain",
      "symptom": "strain",
      "risk_factor": False,
    },
    {
      "hi": "क्या आप दर्द का वर्णन कर सकते हैं? (तेज, हल्का, धड़कता हुआ, आदि)",
      "en": "Can you describe the pain (sharp, dull, throbbing, etc.)?",
      "category": "strain",
      "symptom": "strain",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने उस क्षेत्र में सूजन, चोट, या लालिमा महसूस की है?",
      "en": "Have you experienced any swelling, bruising, or redness in the area?",
      "category": "strain",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आप प्रभावित मांसपेशी या जोड़ी को हिला सकते हैं, या गति की सीमा सीमित है?",
      "en": "Are you able to move the affected muscle or joint, or is there limited range of motion?",
      "category": "strain",
      "symptom": "strain",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको इस क्षेत्र में पहले कोई चोट या खिंचाव हुआ है?",
      "en": "Have you had any previous injuries or strains in this area?",
      "category": "strain",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने किसी उपचार की कोशिश की है (जैसे, विश्राम, बर्फ, गर्मी, या दवा), और यदि हां, तो क्या उन्होंने मदद की?",
      "en": "Have you tried any treatments (e.g., rest, ice, heat, or medication), and if so, did they help?",
      "category": "strain",
      "symptom": None,
      "risk_factor": False,
    }
],


"fainting": [
    {
      "hi": "आपने आखिरी बार बेहोशी या बेहोशी के निकट अनुभव कब किया था?",
      "en": "When did you last experience fainting or a near-fainting episode?",
      "category": "fainting",
      "symptom": "fainting",
      "risk_factor": False,
    },
    {
      "hi": "क्या बेहोश होने से पहले कोई विशिष्ट उत्तेजक या चेतावनी संकेत थे (जैसे चक्कर आना, मितली)?",
      "en": "Were there any specific triggers or warning signs before you fainted (e.g., dizziness, nausea)?",
      "category": "fainting",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने पूरी तरह से चेतना खो दी थी, या आपको बस हल्का महसूस हो रहा था?",
      "en": "Did you lose consciousness completely, or were you just lightheaded?",
      "category": "fainting",
      "symptom": "fainting",
      "risk_factor": False,
    },
    {
      "hi": "बेहोशी का अनुभव कितना समय चला?",
      "en": "How long did the fainting episode last?",
      "category": "fainting",
      "symptom": "fainting",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने हाल ही में कोई बीमारी, निर्जलीकरण, या दवाओं में बदलाव अनुभव किया है?",
      "en": "Have you had any recent illnesses, dehydration, or changes in medication?",
      "category": "fainting",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आप खड़े थे या कोई विशेष स्थिति में थे जब आप बेहोश हुए?",
      "en": "Were you standing up or in a particular position when you fainted?",
      "category": "fainting",
      "symptom": "fainting",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको हृदय की समस्याओं, मिर्गी, या कम रक्तचाप का इतिहास है?",
      "en": "Do you have a history of heart problems, seizures, or low blood pressure?",
      "category": "fainting",
      "symptom": None,
      "risk_factor": True,
    },
],
  "nervousness": [
    {
      "hi": "आप सामान्यतः कब नर्वस या चिंतित महसूस करते हैं?",
      "en": "When do you typically feel nervous or anxious?",
      "category": "nervousness",
      "symptom": "nervousness",
      "risk_factor": False,
    },
    {
      "hi": "क्या ऐसी कोई विशिष्ट स्थिति या उत्तेजक है जो आपको नर्वस महसूस कराती है?",
      "en": "Are there specific situations or triggers that make you feel nervous?",
      "category": "nervousness",
      "symptom": "nervousness",
      "risk_factor": False,
    },
    {
      "hi": "यह नर्वसनेस की भावना आमतौर पर कितनी देर तक रहती है?",
      "en": "How long do these feelings of nervousness usually last?",
      "category": "nervousness",
      "symptom": "nervousness",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको अपनी नर्वसनेस को नियंत्रित या प्रबंधित करने में कठिनाई होती है?",
      "en": "Do you find it difficult to control or manage your nervousness?",
      "category": "nervousness",
      "symptom": "nervousness",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने हाल ही में अधिक तनाव महसूस किया है?",
      "en": "Have you been under increased stress recently?",
      "category": "nervousness",
      "symptom": None,
      "risk_factor": False,
    },
],
"blurred vision": [
    {
      "hi": "क्या धुंधली दृष्टि एक आंख में है या दोनों आंखों में?",
      "en": "Is the blurred vision in one eye or both eyes?",
      "category": "blurred vision",
      "symptom": "blurred vision",
      "risk_factor": False,
    },
    {
      "hi": "क्या धुंधलापन आता-जाता है, या यह निरंतर है?",
      "en": "Does the blurriness come and go, or is it constant?",
      "category": "blurred vision",
      "symptom": "blurred vision",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको रात के समय या कुछ विशेष रोशनी की परिस्थितियों में देखने में कठिनाई हो रही है?",
      "en": "Are you experiencing any difficulty seeing at night or in certain lighting conditions?",
      "category": "blurred vision",
      "symptom": "blurred vision",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको आंखों से संबंधित कोई पुरानी समस्या है, जैसे मोतियाबिंद, ग्लूकोमा, या मॅक्यूलर डिजेनेरेशन?",
      "en": "Do you have a history of eye conditions, such as cataracts, glaucoma, or macular degeneration?",
      "category": "blurred vision",
      "symptom": None,
      "risk_factor": True,
    },
    {
      "hi": "क्या आप वर्तमान में कोई दवाइयाँ ले रहे हैं या कोई अंतर्निहित स्वास्थ्य समस्याएँ हैं (जैसे, मधुमेह या उच्च रक्तचाप)?",
      "en": "Are you currently taking any medications or have any underlying health conditions (e.g., diabetes or hypertension)?",
      "category": "blurred vision",
      "symptom": None,
      "risk_factor": False,
    }
],
"restlessness": [
    {
      "hi": "क्या कोई विशेष परिस्थितियाँ या उत्तेजक हैं जो आपको अधिक बेचैन महसूस कराते हैं?",
      "en": "Are there specific situations or triggers that make you feel more restless?",
      "category": "restlessness",
      "symptom": "restlessness",
      "risk_factor": False,
    },
    {
      "hi": "यह बेचैनी की भावना आमतौर पर कितनी देर तक रहती है?",
      "en": "How long do these feelings of restlessness usually last?",
      "category": "restlessness",
      "symptom": "restlessness",
      "risk_factor": False,
    },
    {
      "hi": "क्या आप आराम करने या शांत होने में सक्षम हैं, या यह बेचैनी बनी रहती है?",
      "en": "Are you able to relax or calm down, or does the restlessness persist?",
      "category": "restlessness",
      "symptom": "restlessness",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको सोने में या सोकर बने रहने में कठिनाई हो रही है?",
      "en": "Do you have trouble sleeping or staying asleep?",
      "category": "restlessness",
      "symptom": "restlessness",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने हाल ही में अपनी दिनचर्या, आहार, या दवाइयों में कोई बदलाव किया है?",
      "en": "Have you had any changes in your routine, diet, or medications recently?",
      "category": "restlessness",
      "symptom": None,
      "risk_factor": False,
    }
],

"difficulty swallowing": [
    {
      "hi": "क्या निगलने में कठिनाई ठोस पदार्थों, तरल पदार्थों, या दोनों में है?",
      "en": "Is the difficulty with swallowing solids, liquids, or both?",
      "category": "difficulty swallowing",
      "symptom": "difficulty swallowing",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको लगता है कि खाना या तरल पदार्थ आपके गले या सीने में अटक रहे हैं?",
      "en": "Do you feel like food or liquids are getting stuck in your throat or chest?",
      "category": "difficulty swallowing",
      "symptom": "difficulty swallowing",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको एसिड रिफ्लक्स, आहार नलिका की समस्याएं, या तंत्रिका संबंधी स्थितियों का इतिहास है?",
      "en": "Do you have a history of acid reflux, esophageal issues, or neurological conditions?",
      "category": "difficulty swallowing",
      "symptom": None,
      "risk_factor": True,
    }
],
"dry mouth": [
    {
      "hi": "क्या मुंह में सूखापन लगातार है, या यह कभी-कभी होता है?",
      "en": "Is the dryness constant, or does it come and go?",
      "category": "dry mouth",
      "symptom": "dry mouth",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने दिनभर में पर्याप्त मात्रा में तरल पदार्थ पिए हैं?",
      "en": "Have you been drinking enough fluids throughout the day?",
      "category": "dry mouth",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आप वर्तमान में किसी दवा का सेवन कर रहे हैं, जैसे एंटीहिस्टामिन या एंटीडिप्रेसेंट, जो मुंह के सूखने का कारण बन सकती है?",
      "en": "Are you currently taking any medications, such as antihistamines or antidepressants, that could cause dry mouth?",
      "category": "dry mouth",
      "symptom": "dry mouth",
      "risk_factor": False,
    },
    {
      "hi": "क्या आप तंबाकू उत्पादों या शराब का सेवन करते हैं, जो मुंह के सूखने का कारण बन सकते हैं?",
      "en": "Are you using any tobacco products or alcohol, which may contribute to dry mouth?",
      "category": "dry mouth",
      "symptom": "dry mouth",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको कोई अंतर्निहित स्वास्थ्य स्थितियां हैं, जैसे मधुमेह, शोज़ग्रेन सिंड्रोम, या ऑटोइम्यून विकार?",
      "en": "Do you have any underlying health conditions, such as diabetes, Sjögren's syndrome, or autoimmune disorders?",
      "category": "dry mouth",
      "symptom": None,
      "risk_factor": False,
    }
],
"flu": [
    {
      "hi": "क्या आपको बुखार हो रहा है, और अगर हां, तो यह कितने उच्च स्तर का रहा है?",
      "en": "Are you experiencing a fever, and if so, how high has it been?",
      "category": "flu",
      "symptom": "fever",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको खांसी, गले में खराश, या नाक बंद/बहना हो रहा है?",
      "en": "Do you have a cough, sore throat, or runny/stuffy nose?",
      "category": "flu",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आप थका हुआ या कमजोर महसूस कर रहे हैं?",
      "en": "Are you feeling fatigued or weak?",
      "category": "flu",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने हाल ही में किसी ऐसे व्यक्ति के संपर्क में आया है जिसे फ्लू या सर्दी जैसे लक्षण हो?",
      "en": "Have you been in contact with anyone who has recently had the flu or cold-like symptoms?",
      "category": "flu",
      "symptom": "flu",
      "risk_factor": False,
    },
],
"confusion": [
    {
      "hi": "क्या भ्रम लगातार है, या यह आता जाता है?",
      "en": "Is the confusion constant, or does it come and go?",
      "category": "confusion",
      "symptom": "confusion",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको हाल की घटनाओं या विवरणों को याद रखने में समस्या हो रही है?",
      "en": "Are you having trouble remembering recent events or details?",
      "category": "confusion",
      "symptom": "confusion",
      "risk_factor": False,
    },
    {
      "hi": "क्या आप परिचित लोगों और स्थानों को पहचानने में सक्षम हैं?",
      "en": "Are you able to recognize familiar people and places?",
      "category": "confusion",
      "symptom": "confusion",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको किसी चिकित्सीय स्थिति का इतिहास है, जैसे डिमेंशिया, स्ट्रोक, या संक्रमण?",
      "en": "Do you have any history of medical conditions, such as dementia, stroke, or infections?",
      "category": "confusion",
      "symptom": None,
      "risk_factor": True,
    },
    {
      "hi": "क्या आपने हाल ही में कोई नई दवाएं शुरू की हैं या अपने दिनचर्या में कोई बदलाव महसूस किया है?",
      "en": "Have you started any new medications or experienced any changes in your routine recently?",
      "category": "confusion",
      "symptom": "confusion",
      "risk_factor": True,
    }
],
"runny nose": [
    {
      "hi": "क्या बलगम साफ, पीला, या हरा है?",
      "en": "Is the mucus clear, yellow, or green?",
      "category": "runny nose",
      "symptom": "runny nose",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको एलर्जी या अस्थमा का इतिहास है?",
      "en": "Do you have a history of allergies or asthma?",
      "category": "runny nose",
      "symptom": None,
      "risk_factor": True,
    },
    {
      "hi": "क्या आपने हाल ही में यात्रा की है या पर्यावरणीय उत्तेजकों (जैसे धूल, धुंआ, प्रदूषण) से संपर्क किया है?",
      "en": "Have you recently traveled or been in contact with environmental irritants (e.g., dust, smoke, pollution)?",
      "category": "runny nose",
      "symptom": None,
      "risk_factor": False,
    }
],
  "sneezing": [
    {
      "hi": "क्या आप दिन के कुछ विशेष समय पर या कुछ विशेष वातावरण में ज्यादा छींकते हैं?",
      "en": "Do you sneeze more at certain times of day or in specific environments?",
      "category": "sneezing",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने किसी एलर्जी उत्पन्न करने वाले तत्वों (जैसे पराग, धूल, या पालतू जानवरों की रूसी) से संपर्क किया है?",
      "en": "Have you been exposed to any allergens, such as pollen, dust, or pet dander?",
      "category": "sneezing",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने हाल ही में बिमार महसूस किया है या सर्दी या फ्लू के लक्षण थे?",
      "en": "Have you recently been sick or had symptoms of a cold or flu?",
      "category": "sneezing",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको एलर्जी या अस्थमा का इतिहास है?",
      "en": "Do you have a history of allergies or asthma?",
      "category": "sneezing",
      "symptom": None,
      "risk_factor": True,
    },
    {
      "hi": "क्या आपने हाल ही में मजबूत गंध, धुंआ, या रासायनिक उत्तेजकों से संपर्क किया है?",
      "en": "Have you recently been in contact with strong odors, smoke, or chemical irritants?",
      "category": "sneezing",
      "symptom": None,
      "risk_factor": False,
    },
],

"nose pain": [
    {
      "hi": "क्या आपकी नाक में लगातार दर्द या जलन हो रही है?",
      "en": "Are you experiencing persistent pain or burning sensation in your nose?",
      "category": "nose pain",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको नाक छूने या दबाने पर दर्द महसूस होता है?",
      "en": "Do you feel pain when touching or pressing on your nose?",
      "category": "nose pain",
      "symptom": "nose pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपकी नाक में सूजन या लालिमा है?",
      "en": "Is there any swelling or redness in your nose?",
      "category": "nose pain",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको हाल ही में सर्दी, एलर्जी या साइनस की समस्या हुई है?",
      "en": "Have you recently had a cold, allergies, or sinus issues?",
      "category": "nose pain",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपकी नाक से किसी प्रकार का डिस्चार्ज या खून आ रहा है?",
      "en": "Is there any discharge or bleeding from your nose?",
      "category": "nose pain",
      "symptom": None,
      "risk_factor": False,
    },
],

  "hip pain": [
    {
      "hi": "क्या दर्द एक कूल्हे में है या दोनों कूल्हों में?",
      "en": "Is the pain in one hip or both hips?",
      "category": "hip pain",
      "symptom": "hip pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या कूल्हे का दर्द लगातार बना रहता है, या यह आता-जाता रहता है?",
      "en": "Is the hip pain constant, or does it come and go?",
      "category": "hip pain",
      "symptom": "hip pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको हाल ही में कूल्हे में कोई चोट या आघात हुआ है?",
      "en": "Have you had any recent injuries or trauma to your hip?",
      "category": "hip pain",
      "symptom": "hip pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या कूल्हे का दर्द कुछ गतिविधियों, जैसे चलने, झुकने या खड़े होने से बढ़ जाता है?",
      "en": "Does the hip pain worsen with certain movements, such as walking, bending, or standing up?",
      "category": "hip pain",
      "symptom": "hip pain",
      "risk_factor": False,
    },
],
"jaundice": [
  {
    "hi": "क्या आपने अपनी त्वचा या आंखों के पीले होने को महसूस किया है?",
    "en": "Have you noticed the yellowing of your skin or eyes?",
    "category": "jaundice",
    "symptom": "jaundice",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपने अपनी मूत्र या मल के रंग में कोई बदलाव महसूस किया है?",
    "en": "Have you noticed any changes in the color of your urine or stool?",
    "category": "jaundice",
    "symptom": "jaundice",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको पेट में कोई दर्द है, विशेष रूप से दाहिने ऊपरी हिस्से में?",
    "en": "Do you have any pain in your abdomen, especially in the upper right side?",
    "category": "jaundice",
    "symptom": "abdomen pain",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपने हाल ही में वजन घटने या भूख में कमी महसूस की है?",
    "en": "Have you experienced any recent weight loss or loss of appetite?",
    "category": "jaundice",
    "symptom": "weight loss",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको हेपेटाइटिस या किसी संक्रामक रोग से संक्रमित किसी व्यक्ति के संपर्क में आने का कोई इतिहास है?",
    "en": "Have you been exposed to anyone with hepatitis or any infectious diseases?",
    "category": "jaundice",
    "symptom": None,
    "risk_factor": False,
  },
  {
    "hi": "क्या आप शराब का सेवन करते हैं या किसी प्रकार की दवाइयां लेते हैं?",
    "en": "Do you have a history of alcohol use or take any medications?",
    "category": "jaundice",
    "symptom": None,
    "risk_factor": True,
  },
],
"exhaustion": [
  {
    "hi": "क्या थकान लगातार है, या यह आती-जाती रहती है?",
    "en": "Is the exhaustion constant, or does it come and go?",
    "category": "exhaustion",
    "symptom": "exhaustion",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपने अपनी नींद के पैटर्न में कोई बदलाव महसूस किया है (जैसे, सोने में कठिनाई, बहुत अधिक सोना)?",
    "en": "Have you noticed any changes in your sleep patterns (e.g., difficulty sleeping, sleeping too much)?",
    "category": "exhaustion",
    "symptom": None,
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको कोई तनाव, चिंता या भावनात्मक बदलाव महसूस हो रहे हैं?",
    "en": "Do you have any stress, anxiety, or emotional changes?",
    "category": "exhaustion",
    "symptom": None,
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको कोई ज्ञात चिकित्सीय स्थिति है, जैसे एनीमिया, थायरॉयड समस्याएं, या डायबिटीज?",
    "en": "Do you have a history of any medical conditions, such as anemia, thyroid problems, or diabetes?",
    "category": "exhaustion",
    "symptom": None,
    "risk_factor": True,
  },
  {
    "hi": "क्या आपने हाल ही में अपनी आहार, व्यायाम दिनचर्या या जीवनशैली में कोई बदलाव किया है?",
    "en": "Have you made any recent changes to your diet, exercise routine, or lifestyle?",
    "category": "exhaustion",
    "symptom": None,
    "risk_factor": False,
  },
],

"fatigue": [
  {
    "hi": "क्या थकान लगातार बनी रहती है या आती-जाती रहती है?",
    "en": "Is the fatigue constant, or does it come and go?",
    "category": "fatigue",
    "symptom": "fatigue",
    "risk_factor": False,
  },
],

"sleepy": [
  {
    "hi": "क्या आपको सोने में कठिनाई होती है, नींद में रुकावट आती है, या आप बहुत जल्दी उठ जाते हैं?",
    "en": "Do you have trouble falling asleep, staying asleep, or waking up too early?",
    "category": "sleepy",
    "symptom": "insomnia",
    "risk_factor": False,
  },
  {
    "hi": "आप सामान्यतः रात में कितने घंटे सोते हैं?",
    "en": "How many hours of sleep do you usually get per night?",
    "category": "sleepy",
    "symptom": "sleepy",
    "risk_factor": False,
  },
  {
    "hi": "क्या आप खर्राटे लेते हैं या क्या आपको बताया गया है कि सोते समय आपकी सांस रुक जाती है?",
    "en": "Do you snore or have you been told you stop breathing while sleeping?",
    "category": "sleepy",
    "symptom": None,
    "risk_factor": False,
  },
  {
    "hi": "क्या आपने हाल ही में अपनी दिनचर्या या तनाव स्तर में कोई बदलाव महसूस किया है?",
    "en": "Have you experienced any recent changes in your routine or stress levels?",
    "category": "sleepy",
    "symptom": None,
    "risk_factor": False,
  },
  {
    "hi": "क्या आप कोई दवाइयाँ या पदार्थ ले रहे हैं जो आपकी नींद को प्रभावित कर सकते हैं?",
    "en": "Are you taking any medications or substances that could affect your sleep?",
    "category": "sleepy",
    "symptom": "sleepy",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको दिन में अत्यधिक थकान महसूस होती है, भले ही आपने पूरी रात की नींद ली हो?",
    "en": "Do you feel excessively tired during the day, even after a full night of sleep?",
    "category": "sleepy",
    "symptom": "sleepy",
    "risk_factor": False,
  },
],
"back bone issue": [
    {
      "hi": "क्या आपकी पीठ सीधी है या झुकी हुई है?",
      "en": "Is your back straight or bent?",
      "category": "back bone issue",
      "symptom": "back bone issue",
      "risk_factor": False,
    },
    {
      "hi": "क्या आप पीठ दर्द के स्थान और पैटर्न का वर्णन कर सकते हैं?",
      "en": "Can you describe the back pain’s location and pattern?",
      "category": "back bone issue",
      "symptom": "back bone issue",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको पिछली पीठ की चोटें या सर्जरी हुई हैं?",
      "en": "Have you had any previous back injuries or surgeries?",
      "category": "back bone issue",
      "symptom": "back bone issue",
      "risk_factor": False,
    },
    {
      "hi": "क्या कोई चीज़ पीठ दर्द को बेहतर या बदतर बनाती है?",
      "en": "Does anything make the back pain better or worse?",
      "category": "back bone issue",
      "symptom": "back bone issue",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको अन्य चिकित्सा स्थितियों का कोई इतिहास है?",
      "en": "Do you have any history of other medical conditions?",
      "category": "back bone issue",
      "symptom": "back bone issue",
      "risk_factor": True,
    },
],
"female issue": [
    {
      "hi": "क्या आपकी मासिक धर्म चक्र में कोई बदलाव आया है (जैसे, माहवारी छूट जाना, अधिक या दर्दनाक माहवारी)?",
      "en": "Have you had any changes in your menstrual cycle (e.g., missed periods, heavy or painful periods)?",
      "category": "female issue",
      "symptom": "female issue",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपके शरीर में कोई हार्मोनल असंतुलन है?",
      "en": "Is there any hormonal imbalance in your body?",
      "category": "female issue",
      "symptom": "hormonal imbalance",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको मूत्र संबंधी कोई लक्षण हैं, जैसे बार-बार पेशाब आना या पेशाब करते समय दर्द होना?",
      "en": "Do you have any history of urinary symptoms, such as frequent urination or pain while urinating?",
      "category": "female issue",
      "symptom": None,
      "risk_factor": True,
    },
    {
      "hi": "क्या आपको कोई गाइनकोलॉजिकल स्थितियाँ हैं, जैसे कि फाइब्रॉयड्स, एंडोमेट्रियोसिस, या अंडकोषीय सिस्ट?",
      "en": "Do you have any history of gynecological conditions, such as fibroids, endometriosis, or ovarian cysts?",
      "category": "female issue",
      "symptom": "female issue",
      "risk_factor": True,
    },
    {
      "hi": "क्या आपको पॉलीसिस्टिक अंडाशय सिंड्रोम (PCOS) या अन्य हार्मोनल विकार हैं?",
      "en": "Do you have PCOS or other hormonal disorders?",
      "category": "female issue",
      "symptom": "female issue",
      "risk_factor": False,
    },
    {
      "hi": "क्या आप अपनी माहवारी से पहले या दौरान कोई दर्द या ऐंठन महसूस कर रही हैं?",
      "en": "Are you experiencing any pain or cramping before or during your period?",
      "category": "female issue",
      "symptom": "female issue",
      "risk_factor": False,
    },
   {
      "hi": "क्या आपके पेट के निचले हिस्से में किसी प्रकार की गाँठ या सूजन महसूस हो रही है?",
      "en": "Do you feel any lump or swelling in your lower abdomen or pelvis?",
      "category": "pelvic_mass",
      "symptom": "pelvic mass",
      "risk_factor": True,
    },
],
"menopause": [
  {
    "hi": "क्या आपकी माहवारी नियमित रूप से आती है?",
    "en": "Is your menstrual cycle regular?",
    "category": "menstruation",
    "symptom": "irregular periods",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपकी माहवारी के समय असामान्य रंग या गंध होती है?",
    "en": "Is there any unusual color or odor during your period?",
    "category": "menstruation",
    "symptom": "abnormal discharge",
    "risk_factor": True,
  },
],

"thyroid": [
    {
      "hi": "क्या आपके परिवार में किसी को थायरॉयड संबंधित विकारों का इतिहास है?",
      "en": "Do you have a history of thyroid disorders in your family?",
      "category": "thyroid",
      "symptom": "thyroid",
      "risk_factor": True,
    },
    {
      "hi": "क्या आपने अपनी भूख या वजन में कोई बदलाव महसूस किया है?",
      "en": "Have you noticed any changes in your appetite or weight?",
      "category": "thyroid",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने अपनी त्वचा, बालों, या नाखूनों में कोई बदलाव अनुभव किया है?",
      "en": "Have you experienced any changes in your skin, hair, or nails?",
      "category": "thyroid",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आप अपनी मानसिक स्थिति में कोई बदलाव अनुभव कर रहे हैं, जैसे कि अवसाद या चिंता?",
      "en": "Are you experiencing any changes in your mood, such as depression or anxiety?",
      "category": "thyroid",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आप असामान्य रूप से ठंडा या गर्म महसूस कर रहे हैं, या तापमान में बदलाव के प्रति संवेदनशीलता अनुभव कर रहे हैं?",
      "en": "Are you feeling unusually cold or hot, or experiencing sensitivity to temperature changes?",
      "category": "thyroid",
      "symptom": "temperature changes",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने पहले थायरॉयड संबंधित समस्याओं के लिए कोई दवाइयाँ या उपचार लिया है?",
      "en": "Have you been on any medications or treatments for thyroid issues in the past?",
      "category": "thyroid",
      "symptom": "thyroid",
      "risk_factor": False,
    },
],
"piles": [
    {
      "hi": "क्या आपने शौच के दौरान कोई खून बहते हुए देखा है? अगर हां, तो कितना?",
      "en": "Have you noticed any bleeding during bowel movements? If so, how much?",
      "category": "piles",
      "symptom": "piles",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको बैठने या शौच के दौरान कोई दर्द या असहजता महसूस होती है?",
      "en": "Do you experience any pain or discomfort while sitting or during bowel movements?",
      "category": "piles",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपकी शौच की आदतों में कोई बदलाव आया है (जैसे कब्ज, दस्त)?",
      "en": "Have you had any changes in your bowel habits (e.g., constipation, diarrhea)?",
      "category": "piles",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने शौच के दौरान या भारी वस्तुएं उठाते समय कोई जोर लगाया है?",
      "en": "Do you have a history of straining during bowel movements or lifting heavy objects?",
      "category": "piles",
      "symptom": None,
      "risk_factor": True,
    },
    {
      "hi": "क्या आपने गुदा के आसपास कोई गांठ या सूजन महसूस की है?",
      "en": "Have you experienced any lumps or swelling around the anus?",
      "category": "piles",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको कोई पुरानी स्थितियाँ हैं, जैसे कब्ज, यकृत रोग, या गर्भावस्था?",
      "en": "Do you have any history of chronic conditions, such as constipation, liver disease, or pregnancy?",
      "category": "piles",
      "symptom": None,
      "risk_factor": True,
    },
],

  "shortness of breath": [
    {
      "hi": "क्या आपको सांस लेने में कठिनाई हो रही है?",
      "en": "Are you having difficulty breathing?",
      "category": "breathing_difficulty",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या सांस लेने में कठिनाई के साथ दिल की धड़कन तेज हो रही है?",
      "en": "Is your heart rate increasing along with difficulty breathing?",
      "category": "heart_rate_increase",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या सांस लेने में कठिनाई किसी विशेष गतिविधि के दौरान बढ़ती है?",
      "en": "Does your difficulty in breathing increase during any specific activity?",
      "category": "activity_related_difficulty",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या आपको सांस लेने में दर्द भी हो रहा है?",
      "en": "Are you experiencing pain while breathing?",
      "category": "breathing_pain",
      "symptom": None,
      "risk_factor": True,    },

    {
       "hi": "क्या आपके परिवार में किसी को अस्थमा है?",
       "en": "Do you have a family history of asthma?",
       "category": "family_history_asthma",
       "symptom": None,
       "risk_factor": True,    },

        {
            "hi": "क्या हाल ही में आपको संक्रमण या बुखार हुआ है?",
            "en": "Have you had recent infections or fever?",
            "category": "infection",
            "symptom": None,
            "risk_factor": False,
        },
        {
            "hi": "क्या आप धूम्रपान करते हैं या सेकेंडहैंड स्मोक के संपर्क में आए हैं?",
            "en": "Are you a smoker, or have you been exposed to secondhand smoke?",
            "category": "smoking",
            "symptom": "shortness of breath",
            "risk_factor": True,
        },
  ],

    "asthma": [
    {
            "hi": "क्या आप धूम्रपान करते हैं या शराब पीते हैं?",
            "en": "Do you smoke or drink?",
            "category": "smoking_drinking",
            "symptom": None,
            "risk_factor": True,    },
    {
            "hi": "क्या आपके परिवार में किसी को अस्थमा है?",
            "en": "Do you have a family history of asthma?",
            "category": "family_history_asthma",
            "symptom": None,
            "risk_factor": True,    },
    {
        "hi": "क्या आपको सांस लेने पर व्हीजिंग या सीटी की आवाजें आती हैं?",
        "en": "Do you experience wheezing or whistling sounds when you breathe?",
        "category": "wheezing",
        "symptom": None,
        "risk_factor": False,    },
    {
        "hi": "क्या आपकी अस्थमा रात या सुबह जल्दी बढ़ जाती है?",
        "en": "Does your asthma worsen at night or early morning?",
        "category": "night_worsening",
        "symptom": None,
        "risk_factor": False,    },
    {
        "hi": "क्या आपने हाल ही में किसी एलर्जन के संपर्क में आए हैं?",
        "en": "Have you been exposed to any allergens recently?",
        "category": "allergen_exposure",
        "symptom": None,
        "risk_factor": False,    },
    {
        "hi": "क्या आपको किसी प्रकार की एलर्जी प्रतिक्रिया का इतिहास है?",
        "en": "Do you have a history of allergic reactions?",
        "category": "allergy_history",
        "symptom": None,
        "risk_factor": True,
    },
    {
        "hi": "क्या आपने हाल ही में अपने रेस्क्यू इनहेलर का अधिक उपयोग किया है?",
        "en": "Have you been using any rescue inhaler more frequently than usual?",
        "category": "inhaler_usage",
        "symptom": None,
        "risk_factor": False,    },
    ],

    "pneumonia": [
    {
        "hi": "क्या आपको सांस लेने या खांसने पर सीने में दर्द होता है?",
        "en": "Are you experiencing chest pain when breathing or coughing?",
        "category": "chest_pain",
        "symptom": None,
        "risk_factor": False,    },
    {
        "hi": "क्या आपको तेज बुखार के साथ ठंड लगती है?",
        "en": "Do you have a high fever with chills?",
        "category": "fever_chills",
        "symptom": None,
        "risk_factor": False,    },
    {
        "hi": "क्या आप बलगम या म्यूकस खांस रहे हैं?",
        "en": "Are you coughing up phlegm or mucus?",
        "category": "coughing_phlegm",
        "symptom": None,
        "risk_factor": False,    },
    {
        "hi": "क्या आप असामान्य थकान या कमजोरी महसूस कर रहे हैं?",
        "en": "Have you been feeling unusually tired or weak?",
        "category": "fatigue_weakness",
        "symptom": None,
        "risk_factor": False,    },
    {
        "hi": "क्या आपने हाल ही में भूख में कमी या वजन घटने का अनुभव किया है?",
        "en": "Have you noticed any loss of appetite or weight loss recently?",
        "category": "appetite_weight_loss",
        "symptom": None,
        "risk_factor": False,    },
],

  "sugar": [
        {
            "hi": "क्या आप नियमित रूप से अपने ब्लड शुगर लेवल की जांच करते हैं?",
            "en": "Do you regularly monitor your blood sugar levels?",
            "category": "blood_sugar_monitoring",
            "symptom": "sugar monitoring",
            "risk_factor": True,
        },
        {
            "hi": "क्या आपने हाल ही में अपने ब्लड शुगर में किसी भी असामान्य बदलाव का अनुभव किया है?",
            "en": "Have you experienced any unusual changes in your blood sugar levels recently?",
            "category": "blood_sugar_changes",
            "symptom": "sugar changes",
            "risk_factor": False,
        },
        {
            "hi": "क्या आपको अपने ब्लड शुगर के स्तर को नियंत्रित करने के लिए दवाओं का उपयोग करना पड़ता है?",
            "en": "Do you need to take medications to control your blood sugar levels?",
            "category": "blood_sugar_medications",
            "symptom": "sugar",
            "risk_factor": True,
        },
        {
            "hi": "क्या आपके खानपान में कोई विशेष बदलाव आया है ताकि आप अपने ब्लड शुगर को नियंत्रित कर सकें?",
            "en": "Have you made any specific changes to your diet to manage your blood sugar?",
            "category": "blood_sugar_diet_changes",
            "symptom": "diet changes",
            "risk_factor": False,
        },
        {
            "hi": "क्या आप शारीरिक गतिविधि में किसी प्रकार की वृद्धि या कमी देख रहे हैं ताकि आप अपने ब्लड शुगर को नियंत्रित कर सकें?",
            "en": "Are you increasing or decreasing your physical activities to manage your blood sugar levels?",
            "category": "blood_sugar_physical_activity",
            "symptom": None,
            "risk_factor": False,
        },
        {
            "hi": "क्या आपके परिवार में किसी को डायबिटीज़ है?",
            "en": "Do you have a family history of diabetes?",
            "category": "family_history_diabetes",
            "symptom": None,
            "risk_factor": True,
        },
        {
            "hi": "क्या आपको अपने ब्लड शुगर के स्तर में अचानक गिरावट या वृद्धि का अनुभव होता है?",
            "en": "Do you experience sudden drops or spikes in your blood sugar levels?",
            "category": "blood_sugar_fluctuations",
            "symptom": None,
            "risk_factor": False,
        },
        {
            "hi": "क्या आपको अपने ब्लड शुगर के स्तर को नियंत्रित करने के लिए इंसुलिन का उपयोग करना पड़ता है?",
            "en": "Do you need to use insulin to control your blood sugar levels?",
            "category": "insulin_usage",
            "symptom": "sugar",
            "risk_factor": True,
        },

        {
            "hi": "क्या आप अपने ब्लड शुगर के स्तर पर किसी प्रकार के स्ट्रेस या मानसिक दबाव का अनुभव करते हैं?",
            "en": "Do you experience any stress or mental pressure that affects your blood sugar levels?",
            "category": "blood_sugar_stress",
            "symptom": None,
            "risk_factor": False,
        },
    ],

  "waist pain": [
    {
      "hi": "आप दर्द का वर्णन कैसे करेंगे? क्या यह तेज़, मन्द, जलन वाला, या धड़कता हुआ है?",
      "en": "Can you describe the pain? Is it sharp, dull, burning, or throbbing?",
      "category": "waist pain",
      "symptom": "waist pain",
      "risk_factor": False,
    },
    {
      "hi": "दर्द ठीक कहाँ है? क्या यह एक तरफ़, दोनों तरफ़ या किसी और हिस्से तक फैलता है?",
      "en": "Where exactly is the pain located? Is it on one side, both sides, or spreading elsewhere?",
      "category": "waist pain",
      "symptom": "waist pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या कोई गतिविधि, स्थिति या आराम से दर्द बढ़ता या कम होता है?",
      "en": "Does anything make the pain better or worse, like movement, posture, or rest?",
      "category": "waist pain",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने हाल ही में कोई भारी वजन उठाया है या कोई चोट लगी है?",
      "en": "Have you had any recent injuries, heavy lifting, or physical strain?",
      "category": "waist pain",
      "symptom": "injury",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको पहले भी ऐसी कमर में दर्द की समस्या रही है या कोई पुरानी बीमारी है?",
      "en": "Do you have a history of similar pain or any known medical conditions?",
      "category": "waist pain",
      "symptom": "waist pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या आप कोई दवाइयाँ या सप्लीमेंट्स ले रहे हैं?",
      "en": "Are you taking any medications or supplements currently?",
      "category": "waist pain",
      "symptom": "waist pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या इस दर्द से आपकी रोज़मर्रा की गतिविधियाँ या नींद प्रभावित हो रही हैं?",
      "en": "How does the pain affect your daily activities or sleep?",
      "category": "waist pain",
      "symptom": None,
      "risk_factor": False,
    },
  ],

    "pelvic pain": [
    {
      "hi": "आप pelvic में दर्द का वर्णन कैसे करेंगे? क्या यह तेज़, मन्द, जलन वाला, या धड़कता हुआ है?",
      "en": "Can you describe the pelvic pain? Is it sharp, dull, burning, or throbbing?",
      "category": "pelvic pain",
      "symptom": "pelvic pain",
      "risk_factor": False,
    },
    {
      "hi": "दर्द ठीक कहाँ है? क्या यह एक तरफ़, दोनों तरफ़ या किसी और हिस्से तक फैलता है?",
      "en": "Where exactly is the pain located in your pelvic area? Is it on one side, both sides, or spreading elsewhere?",
      "category": "pelvic pain",
      "symptom": "pelvic pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या कोई गतिविधि, स्थिति या आराम से दर्द बढ़ता या कम होता है?",
      "en": "Does anything make the pain better or worse, like movement, posture, or rest?",
      "category": "pelvic pain",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने हाल ही में कोई भारी वजन उठाया है या कोई चोट लगी है?",
      "en": "Have you had any recent injuries, heavy lifting, or physical strain?",
      "category": "pelvic pain",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको पहले भी ऐसी pelvic में दर्द की समस्या रही है या कोई पुरानी बीमारी है?",
      "en": "Do you have a history of similar pelvic pain or any known medical conditions?",
      "category": "pelvic pain",
      "symptom": "pelvic pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या आप कोई दवाइयाँ या सप्लीमेंट्स ले रहे हैं?",
      "en": "Are you taking any medications or supplements currently?",
      "category": "pelvic pain",
      "symptom": "pelvic pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या इस दर्द से आपकी रोज़मर्रा की गतिविधियाँ या नींद प्रभावित हो रही हैं?",
      "en": "How does the pain affect your daily activities or sleep?",
      "category": "pelvic pain",
      "symptom": None,
      "risk_factor": False,
    },
  ],

    "elbow pain": [
    {
      "hi": "आप कोहनी में दर्द का वर्णन कैसे करेंगे? क्या यह तेज़, मन्द, जलन वाला, या धड़कता हुआ है?",
      "en": "Can you describe the elbow pain? Is it sharp, dull, burning, or throbbing?",
      "category": "elbow pain",
      "symptom": "elbow pain",
      "risk_factor": False,
    },
    {
      "hi": "दर्द ठीक कहाँ है? क्या यह एक तरफ़, दोनों तरफ़ या किसी और हिस्से तक फैलता है?",
      "en": "Where exactly is the pain located in your elbow? Is it on one side, both sides, or spreading elsewhere?",
      "category": "elbow pain",
      "symptom": "elbow pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या कोई गतिविधि, स्थिति या आराम से दर्द बढ़ता या कम होता है?",
      "en": "Does anything make the pain better or worse, like movement, posture, or rest?",
      "category": "elbow pain",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने हाल ही में कोई भारी वजन उठाया है या कोई चोट लगी है?",
      "en": "Have you had any recent injuries, heavy lifting, or physical strain?",
      "category": "elbow pain",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको पहले भी ऐसी कोहनी में दर्द की समस्या रही है या कोई पुरानी बीमारी है?",
      "en": "Do you have a history of similar elbow pain or any known medical conditions?",
      "category": "elbow pain",
      "symptom": "elbow pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या आप कोई दवाइयाँ या सप्लीमेंट्स ले रहे हैं?",
      "en": "Are you taking any medications or supplements currently?",
      "category": "elbow pain",
      "symptom": "elbow pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या इस दर्द से आपकी रोज़मर्रा की गतिविधियाँ या नींद प्रभावित हो रही हैं?",
      "en": "How does the pain affect your daily activities or sleep?",
      "category": "elbow pain",
      "symptom": None,
      "risk_factor": False,
    },
  ],

    "calf pain": [
    {
      "hi": "आप बछड़े में दर्द का वर्णन कैसे करेंगे? क्या यह तेज़, मन्द, जलन वाला, या धड़कता हुआ है?",
      "en": "Can you describe the calf pain? Is it sharp, dull, burning, or throbbing?",
      "category": "calf pain",
      "symptom": "calf pain",
      "risk_factor": False,
    },
    {
      "hi": "दर्द ठीक कहाँ है? क्या यह एक तरफ़, दोनों तरफ़ या किसी और हिस्से तक फैलता है?",
      "en": "Where exactly is the pain located in your calf? Is it on one side, both sides, or spreading elsewhere?",
      "category": "calf pain",
      "symptom": "calf pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या कोई गतिविधि, स्थिति या आराम से दर्द बढ़ता या कम होता है?",
      "en": "Does anything make the pain better or worse, like movement, posture, or rest?",
      "category": "calf pain",
      "symptom": "calf pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने हाल ही में कोई भारी वजन उठाया है या कोई चोट लगी है?",
      "en": "Have you had any recent injuries, heavy lifting, or physical strain?",
      "category": "calf pain",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको पहले भी ऐसी बछड़े में दर्द की समस्या रही है या कोई पुरानी बीमारी है?",
      "en": "Do you have a history of similar calf pain or any known medical conditions?",
      "category": "calf pain",
      "symptom": "calf pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या आप कोई दवाइयाँ या सप्लीमेंट्स ले रहे हैं?",
      "en": "Are you taking any medications or supplements currently?",
      "category": "calf pain",
      "symptom": "calf pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या इस दर्द से आपकी रोज़मर्रा की गतिविधियाँ या नींद प्रभावित हो रही हैं?",
      "en": "How does the pain affect your daily activities or sleep?",
      "category": "calf pain",
      "symptom": None,
      "risk_factor": False,
    },
  ],

  "tingling": [
    {
      "hi": "आपको झुनझुनी का अनुभव कहाँ हो रहा है? क्या यह हाथों, पैरों, या शरीर के किसी अन्य हिस्से में है?",
      "en": "Where are you experiencing tingling? Is it in your hands, feet, or elsewhere in your body?",
      "category": "tingling",
      "symptom": "tingling",
      "risk_factor": False,
    },
    {
      "hi": "क्या झुनझुनी के साथ कोई अन्य लक्षण जैसे सुन्नपन, दर्द, या कमजोरी है?",
      "en": "Are you experiencing any other symptoms along with the tingling, like numbness, pain, or weakness?",
      "category": "tingling",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या कोई गतिविधि, स्थिति या आराम से झुनझुनी बढ़ती या कम होती है?",
      "en": "Does any activity, position, or rest make the tingling better or worse?",
      "category": "tingling",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको हाल ही में कोई चोट लगी है या कोई तनावपूर्ण स्थिति का सामना करना पड़ा है?",
      "en": "Have you had any recent injuries or been under physical or emotional stress?",
      "category": "tingling",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको कोई पुरानी बीमारी जैसे डायबिटीज़, न्यूरोलॉजिकल समस्याएँ या तंत्रिका से संबंधित विकार हैं?",
      "en": "Do you have any chronic conditions like diabetes, neurological problems, or nerve-related disorders?",
      "category": "tingling",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आप कोई दवाइयाँ या सप्लीमेंट्स ले रहे हैं?",
      "en": "Are you taking any medications or supplements currently?",
      "category": "tingling",
      "symptom": "tingling",
      "risk_factor": False,
    },
    {
      "hi": "क्या इस झुनझुनी से आपकी रोज़मर्रा की गतिविधियाँ या नींद प्रभावित हो रही हैं?",
      "en": "How does the tingling affect your daily activities or sleep?",
      "category": "tingling",
      "symptom": "tingling",
      "risk_factor": False,
    },
  ],

    "difficulty speaking": [
    {
      "hi": "क्या आपको बोलने में कोई कठिनाई हो रही है? क्या शब्दों को ठीक से बाहर निकालने में समस्या हो रही है?",
      "en": "Are you having difficulty speaking? Is it hard for you to get words out clearly?",
      "category": "difficulty speaking",
      "symptom": "difficulty speaking",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपकी आवाज़ में कोई बदलाव आया है? क्या यह खोई हुई, कमजोर या असामान्य हो गई है?",
      "en": "Has your voice changed in any way? Is it hoarse, weak, or sounding abnormal?",
      "category": "difficulty speaking",
      "symptom": "broken voice",
      "risk_factor": False,
    },
    {
      "hi": "क्या बोलते समय आपकी जुबान फिसलती है या आप शब्दों को ठीक से जोड़ नहीं पा रहे हैं?",
      "en": "Do you find that your tongue slips or that you're unable to form words correctly when speaking?",
      "category": "difficulty speaking",
      "symptom": "difficulty speaking",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको बोलने में किसी तरह का दर्द या असुविधा महसूस हो रही है?",
      "en": "Are you experiencing any pain or discomfort while speaking?",
      "category": "difficulty speaking",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको पहले भी ऐसी समस्या रही है, या यह हाल ही में शुरू हुई है?",
      "en": "Have you had this issue before, or did it start recently?",
      "category": "difficulty speaking",
      "symptom": "difficulty speaking",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको कोई neurological या मस्तिष्क से संबंधित समस्या है, जैसे स्ट्रोक या मस्तिष्क की चोट?",
      "en": "Do you have any neurological or brain-related issues, such as a stroke or brain injury?",
      "category": "difficulty speaking",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या इस कठिनाई से आपकी रोज़मर्रा की बातचीत या अन्य गतिविधियाँ प्रभावित हो रही हैं?",
      "en": "How is this difficulty affecting your daily conversations or other activities?",
      "category": "difficulty speaking",
      "symptom": "difficulty speaking",
      "risk_factor": False,
    },
  ],

    "brittle nails": [
    {
      "hi": "क्या आपकी नाख़ूनों में कोई कमजोरी महसूस हो रही है? क्या वे आसानी से टूट रहे हैं?",
      "en": "Are your nails feeling weak? Are they breaking easily?",
      "category": "brittle nails",
      "symptom": "brittle nails",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपकी नाख़ूनों की बनावट में कोई बदलाव आया है, जैसे वे भुरभुरी या खुरदुरी हो गई हों?",
      "en": "Have you noticed any changes in the texture of your nails, such as them becoming brittle or rough?",
      "category": "brittle nails",
      "symptom": "brittle nails",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपके नाख़ूनों में कोई रंग परिवर्तन हुआ है, जैसे कि वे सफेद, पीले या नीले दिख रहे हों?",
      "en": "Have you noticed any color changes in your nails, such as them appearing white, yellow, or blue?",
      "category": "brittle nails",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपकी नाख़ूनों में कोई दर्द या सूजन हो रही है?",
      "en": "Are you experiencing any pain or swelling around your nails?",
      "category": "brittle nails",
      "symptom": "brittle nails",
      "risk_factor": False,
    },
    {
      "hi": "क्या आप कोई विटामिन या खनिज की कमी से संबंधित समस्याएँ महसूस कर रहे हैं, जैसे आयरन की कमी?",
      "en": "Are you experiencing any issues related to vitamin or mineral deficiencies, such as an iron deficiency?",
      "category": "brittle nails",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आप कोई दवाइयाँ या उपचार ले रहे हैं जो नाख़ूनों पर प्रभाव डाल सकते हैं?",
      "en": "Are you taking any medications or treatments that could be affecting your nails?",
      "category": "brittle nails",
      "symptom": "brittle nails",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपकी नाख़ूनों की समस्या से आपकी रोज़मर्रा की गतिविधियाँ प्रभावित हो रही हैं?",
      "en": "Is your nail condition affecting your daily activities?",
      "category": "brittle nails",
      "symptom": "brittle nails",
      "risk_factor": False,
    },
  ],

    "more hungry": [
    {
      "hi": "क्या आपको हाल ही में भूख में अचानक वृद्धि महसूस हो रही है?",
      "en": "Have you noticed an increase in your hunger recently?",
      "category": "more hungry",
      "symptom": "more hungry",
      "risk_factor": False,
    },
    {
      "hi": "क्या आप पहले से अधिक खाना खा रहे हैं?",
      "en": "Are you eating more than usual?",
      "category": "more hungry",
      "symptom": "more hungry",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको खाने के बाद भी जल्दी फिर से भूख लग रही है?",
      "en": "Do you feel hungry again soon after eating?",
      "category": "more hungry",
      "symptom": "more hungry",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपकी भूख में बदलाव के साथ कोई अन्य लक्षण जैसे थकान, वजन बढ़ना या कमजोरी है?",
      "en": "Are there any other symptoms accompanying the hunger, such as fatigue, weight gain, or weakness?",
      "category": "more hungry",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको किसी खास समय पर या किसी विशिष्ट स्थिति में भूख में वृद्धि हो रही है?",
      "en": "Is your hunger increasing at specific times or under certain conditions?",
      "category": "more hungry",
      "symptom": "more hungry",
      "risk_factor": False,
    },
    {
      "hi": "क्या आप कोई दवाइयाँ या सप्लीमेंट्स ले रहे हैं जो भूख को प्रभावित कर सकते हैं?",
      "en": "Are you taking any medications or supplements that could be affecting your appetite?",
      "category": "more hungry",
      "symptom": "more hungry",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपकी भूख में वृद्धि से आपकी रोज़मर्रा की गतिविधियाँ प्रभावित हो रही हैं?",
      "en": "Is this increased hunger affecting your daily activities?",
      "category": "more hungry",
      "symptom": "more hungry",
      "risk_factor": False,
    },
  ],

    "obesity": [
    {
      "hi": "क्या आपकी शरीर का वजन सामान्य से अधिक बढ़ गया है?",
      "en": "Has your body weight increased significantly above the normal range?",
      "category": "obesity",
      "symptom": "obesity",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको किसी विशेष आहार या जीवनशैली के कारण वजन बढ़ने में समस्या हो रही है?",
      "en": "Have you been experiencing weight gain due to a specific diet or lifestyle?",
      "category": "obesity",
      "symptom": "weight gain",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपका वजन बढ़ने से आपकी शारीरिक गतिविधियाँ या दिनचर्या प्रभावित हो रही है?",
      "en": "Is your weight gain affecting your physical activity or daily routine?",
      "category": "obesity",
      "symptom": "obesity",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको पहले भी वजन बढ़ने की समस्या रही है या यह हाल ही में शुरू हुई है?",
      "en": "Have you had weight gain issues before, or did it start recently?",
      "category": "obesity",
      "symptom": "weight gain",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपके परिवार में कोई और सदस्य भी मोटापे से ग्रस्त है?",
      "en": "Do other members of your family also struggle with obesity?",
      "category": "obesity",
      "symptom": "obesity",
      "risk_factor": True,
    },
    {
      "hi": "क्या आप कोई दवाइयाँ या उपचार ले रहे हैं जो वजन बढ़ाने का कारण बन सकते हैं?",
      "en": "Are you taking any medications or treatments that could be contributing to your weight gain?",
      "category": "obesity",
      "symptom": "obesity",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको कोई अन्य स्वास्थ्य समस्याएँ हैं, जैसे उच्च रक्तचाप, मधुमेह, या उच्च कोलेस्ट्रॉल?",
      "en": "Do you have any other health issues, such as high blood pressure, diabetes, or high cholesterol?",
      "category": "obesity",
      "symptom": None,
      "risk_factor": True,
    },
  ],
  "seizures": [
    {
      "hi": "क्या आपको हाल ही में किसी प्रकार के दौरे (seizure) का अनुभव हुआ है?",
      "en": "Have you experienced any type of seizure recently?",
      "category": "seizures",
      "symptom": "seizures",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने दौरे के दौरान बेहोशी, झटके या शरीर के किसी हिस्से में अकड़न महसूस की?",
      "en": "Did you experience unconsciousness, jerking movements, or stiffness in any part of your body during the seizure?",
      "category": "seizures",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या दौरे के बाद आपको थकान, सिरदर्द या भ्रम का अनुभव हुआ है?",
      "en": "Did you experience fatigue, headache, or confusion after the seizure?",
      "category": "seizures",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको पहले कभी दौरे का अनुभव हुआ है, या यह पहली बार हुआ है?",
      "en": "Have you had seizures before, or is this the first time?",
      "category": "seizures",
      "symptom": "seizures",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपके परिवार में किसी अन्य सदस्य को भी दौरे का इतिहास है?",
      "en": "Do any other members of your family have a history of seizures?",
      "category": "seizures",
      "symptom": "seizures",
      "risk_factor": True,
    },
    {
      "hi": "क्या आप कोई दवाइयाँ या उपचार ले रहे हैं जो दौरे का कारण बन सकते हैं?",
      "en": "Are you taking any medications or treatments that could be contributing to the seizures?",
      "category": "seizures",
      "symptom": "seizures",
      "risk_factor": False,
    },
    {
      "hi": "क्या किसी विशेष स्थिति, जैसे नींद की कमी, तनाव या शराब का सेवन, से दौरे का अनुभव होता है?",
      "en": "Do you experience seizures under specific conditions, such as lack of sleep, stress, or alcohol consumption?",
      "category": "seizures",
      "symptom": None,
      "risk_factor": False,
    },
  ],

    "hiccups": [
    {
      "hi": "क्या आपको हाल ही में बार-बार हिचकी आ रही है?",
      "en": "Have you been experiencing frequent hiccups recently?",
      "category": "hiccups",
      "symptom": "hiccups",
      "risk_factor": False,
    },
    {
      "hi": "क्या हिचकियाँ अचानक शुरू हो रही हैं, या किसी विशेष कारण से हो रही हैं?",
      "en": "Do the hiccups start suddenly, or are they triggered by something specific?",
      "category": "hiccups",
      "symptom": "hiccups",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपकी हिचकियों के दौरान कोई दर्द, असुविधा या ऐंठन महसूस हो रही है?",
      "en": "Are you experiencing any pain, discomfort, or cramping during the hiccups?",
      "category": "hiccups",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या हिचकियाँ कुछ समय बाद खुद ही बंद हो जाती हैं, या लंबे समय तक जारी रहती हैं?",
      "en": "Do the hiccups go away on their own after a while, or do they persist for a long time?",
      "category": "hiccups",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने हाल ही में अधिक भोजन, तीव्र मसालेदार खाना, या शराब का सेवन किया है?",
      "en": "Have you recently eaten large meals, spicy foods, or consumed alcohol?",
      "category": "hiccups",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको हिचकियाँ किसी विशेष स्थिति, जैसे चिंता, तनाव या शारीरिक गतिविधि से होती हैं?",
      "en": "Do your hiccups occur under specific conditions, such as anxiety, stress, or physical activity?",
      "category": "hiccups",
      "symptom": "hiccups",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपकी हिचकियाँ किसी अन्य लक्षण जैसे सिरदर्द, कमजोरी या थकान के साथ हो रही हैं?",
      "en": "Are your hiccups accompanied by any other symptoms such as headache, weakness, or fatigue?",
      "category": "hiccups",
      "symptom": None,
      "risk_factor": False,
    },
  ],

     "ulcers": [
    {
      "hi": "क्या आपको पेट में जलन या दर्द महसूस हो रहा है?",
      "en": "Are you experiencing any burning or pain in your stomach?",
      "category": "ulcers",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको पेट में किसी प्रकार की सूजन या भरा हुआ महसूस हो रहा है?",
      "en": "Do you feel any bloating or fullness in your stomach?",
      "category": "ulcers",
      "symptom": "bloating",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपके पेट में दर्द खाली पेट होने पर बढ़ जाता है?",
      "en": "Does the stomach pain increase when your stomach is empty?",
      "category": "ulcers",
      "symptom": "stomach pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको खाना खाने के बाद दर्द महसूस होता है?",
      "en": "Do you feel pain after eating food?",
      "category": "ulcers",
      "symptom": "ulcers",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको खट्टी डकारें या सीने में जलन महसूस होती है?",
      "en": "Do you experience acid reflux or a burning sensation in your chest?",
      "category": "ulcers",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको किसी प्रकार की नाड़ी तेज़ होने, कमजोरी, या थकान का अनुभव हो रहा है?",
      "en": "Are you experiencing any increased heartbeat, weakness, or fatigue?",
      "category": "ulcers",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको पिछले कुछ समय में अधिक दर्द, उल्टी, या खून की उल्टी महसूस हुई है?",
      "en": "Have you experienced worsening pain, vomiting, or vomiting blood recently?",
      "category": "ulcers",
      "symptom": None,
      "risk_factor": False,
    },
  ],

    "dysentery": [
    {
      "hi": "क्या आपको बार-बार दस्त हो रहे हैं?",
      "en": "Are you experiencing frequent diarrhea?",
      "category": "dysentery",
      "symptom": "dysentery",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपके दस्त में खून या मवाद (pus) शामिल है?",
      "en": "Is there blood or pus in your stool?",
      "category": "dysentery",
      "symptom": "dysentery",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको दस्त के साथ पेट में दर्द या ऐंठन महसूस हो रही है?",
      "en": "Are you experiencing stomach pain or cramping along with diarrhea?",
      "category": "dysentery",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको दस्त के साथ बुखार भी हो रहा है?",
      "en": "Are you also experiencing fever along with the diarrhea?",
      "category": "dysentery",
      "symptom": "fever",
      "risk_factor": False,
    },
    {
      "hi": "क्या दस्त के दौरान आपको कमजोरी या थकान महसूस हो रही है?",
      "en": "Do you feel weakness or fatigue during the diarrhea episodes?",
      "category": "dysentery",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको किसी अन्य व्यक्ति से दस्त या अन्य लक्षणों के फैलने का डर है?",
      "en": "Are you concerned about the possibility of the diarrhea or other symptoms spreading from another person?",
      "category": "dysentery",
      "symptom": "dysentery",
      "risk_factor": True,
    },
    {
      "hi": "क्या आपने हाल ही में पानी या खाद्य पदार्थ खाए हैं जो संक्रमित हो सकते हैं?",
      "en": "Have you recently consumed water or food that could be contaminated?",
      "category": "dysentery",
      "symptom": "dysentery",
      "risk_factor": True,
    },
  ],

    "malaria": [
    {
      "hi": "क्या आपको बुखार हो रहा है?",
      "en": "Are you experiencing a fever?",
      "category": "malaria",
      "symptom": "fever",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको ठंड या कंपकंपी महसूस हो रही है?",
      "en": "Are you experiencing chills or shivering?",
      "category": "malaria",
      "symptom": "chills",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको पसीना ज्यादा आने या थकान महसूस हो रही है?",
      "en": "Are you experiencing excessive sweating or fatigue?",
      "category": "malaria",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको सिरदर्द, मिचली या उल्टी महसूस हो रही है?",
      "en": "Are you experiencing headache, nausea, or vomiting?",
      "category": "malaria",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपके शरीर में दर्द या मांसपेशियों में ऐंठन हो रही है?",
      "en": "Are you experiencing body aches or muscle cramps?",
      "category": "malaria",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको हाल ही में मच्छरों के काटने या संक्रमित क्षेत्र में यात्रा का अनुभव हुआ है?",
      "en": "Have you recently been bitten by mosquitoes or traveled to an area with malaria?",
      "category": "malaria",
      "symptom": "malaria",
      "risk_factor": True,
    },
    {
      "hi": "क्या आपके परिवार में किसी और को मलेरिया का इतिहास है?",
      "en": "Do any other members of your family have a history of malaria?",
      "category": "malaria",
      "symptom": "malaria",
      "risk_factor": True,
    },
  ],

    "dengue": [
    {
      "hi": "क्या आपको अचानक तेज बुखार हो रहा है?",
      "en": "Are you experiencing a sudden high fever?",
      "category": "dengue",
      "symptom": "fever",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको शरीर में दर्द या मांसपेशियों में ऐंठन हो रही है?",
      "en": "Are you experiencing body aches or muscle pain?",
      "category": "dengue",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपके शरीर पर लाल चकत्ते या चिढ़न (rash) हैं?",
      "en": "Are you experiencing any red rashes or itching on your body?",
      "category": "dengue",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको तेज सिरदर्द, आंखों के पीछे दर्द, या थकान महसूस हो रही है?",
      "en": "Are you experiencing severe headache, pain behind the eyes, or fatigue?",
      "category": "dengue",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको उल्टी, मिचली या पेट में दर्द महसूस हो रहा है?",
      "en": "Are you experiencing vomiting, nausea, or abdominal pain?",
      "category": "dengue",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने हाल ही में मच्छरों के काटने का अनुभव किया है?",
      "en": "Have you recently been bitten by mosquitoes?",
      "category": "dengue",
      "symptom": None,
      "risk_factor": True,
    },
    {
      "hi": "क्या आप किसी ऐसे क्षेत्र में गए हैं जहाँ डेंगू का संक्रमण सामान्य है?",
      "en": "Have you traveled to an area where dengue fever is common?",
      "category": "dengue",
      "symptom": "dengue",
      "risk_factor": True,
    },
  ],

    "covid": [
    {
      "hi": "क्या आपको बुखार हो रहा है?",
      "en": "Are you experiencing a fever?",
      "category": "covid",
      "symptom": "fever",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको सूखी खांसी हो रही है?",
      "en": "Are you experiencing a dry cough?",
      "category": "covid",
      "symptom": "dry cough",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको गले में खराश या गले में दर्द महसूस हो रहा है?",
      "en": "Are you experiencing a sore throat or pain in the throat?",
      "category": "covid",
      "symptom": "covid",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको सांस लेने में कठिनाई हो रही है?",
      "en": "Are you having difficulty breathing?",
      "category": "covid",
      "symptom": "difficulty breathing",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको शरीर में दर्द या मांसपेशियों में ऐंठन हो रही है?",
      "en": "Are you experiencing body aches or muscle pain?",
      "category": "covid",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको हाल ही में किसी संक्रमित व्यक्ति के संपर्क में आने का अनुभव हुआ है?",
      "en": "Have you recently been in contact with someone who is infected?",
      "category": "covid",
      "symptom": "covid",
      "risk_factor": True,
    },
    {
      "hi": "क्या आपने हाल ही में यात्रा की है, खासकर ऐसे क्षेत्र में जहाँ COVID-19 का प्रकोप है?",
      "en": "Have you recently traveled, especially to an area with an outbreak of COVID-19?",
      "category": "covid",
      "symptom": "covid",
      "risk_factor": True,
    },
  ],

    "hiv": [
    {
      "hi": "क्या आपको बार-बार बुखार हो रहा है?",
      "en": "Are you experiencing frequent fevers?",
      "category": "hiv",
      "symptom": "hiv",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको शरीर में दर्द या मांसपेशियों में ऐंठन हो रही है?",
      "en": "Are you experiencing body aches or muscle pain?",
      "category": "hiv",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको थकान या कमजोरी महसूस हो रही है?",
      "en": "Are you feeling fatigued or weak?",
      "category": "hiv",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको वजन घटने या भूख में कमी का अनुभव हो रहा है?",
      "en": "Are you experiencing weight loss or a decrease in appetite?",
      "category": "hiv",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको त्वचा पर लाल चकत्ते या संक्रमण महसूस हो रहे हैं?",
      "en": "Are you noticing any rashes or infections on your skin?",
      "category": "hiv",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपके पास HIV के जोखिम वाले कारक हैं, जैसे कि अनसुरक्षित यौन संबंध या संक्रमित रक्त के संपर्क में आना?",
      "en": "Do you have risk factors for HIV, such as unprotected sex or exposure to infected blood?",
      "category": "hiv",
      "symptom": "hiv",
      "risk_factor": True,
    },
    {
      "hi": "क्या आपको हाल ही में किसी के साथ अनसुरक्षित यौन संबंध बनाने का अनुभव हुआ है?",
      "en": "Have you recently had unprotected sex with anyone?",
      "category": "hiv",
      "symptom": "hiv",
      "risk_factor": True,
    },
  ],

    "typhoid": [
    {
      "hi": "क्या आपको लगातार बुखार हो रहा है?",
      "en": "Are you experiencing a persistent fever?",
      "category": "typhoid",
      "symptom": "fever",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको पेट में दर्द या ऐंठन महसूस हो रही है?",
      "en": "Are you experiencing abdominal pain or cramps?",
      "category": "typhoid",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको उल्टी या मिचली महसूस हो रही है?",
      "en": "Are you experiencing nausea or vomiting?",
      "category": "typhoid",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको कब्जियत या दस्त हो रही है?",
      "en": "Are you experiencing constipation or diarrhea?",
      "category": "typhoid",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको शरीर में कमजोरी या थकान महसूस हो रही है?",
      "en": "Are you feeling weak or fatigued?",
      "category": "typhoid",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने हाल ही में संक्रमित जल या खाद्य पदार्थ खाया है?",
      "en": "Have you recently consumed contaminated water or food?",
      "category": "typhoid",
      "symptom": "typhoid",
      "risk_factor": True,
    },
    {
      "hi": "क्या आप ऐसे क्षेत्र में रहे हैं जहां टाइफॉयड का प्रकोप है?",
      "en": "Have you been living in an area with an outbreak of typhoid?",
      "category": "typhoid",
      "symptom": "typhoid",
      "risk_factor": True,
    },
  ],

    "chickenpox": [
    {
      "hi": "क्या आपको शरीर पर दाने या फफोले हो रहे हैं?",
      "en": "Are you developing rashes or blisters on your body?",
      "category": "chickenpox",
      "symptom": "chickenpox",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपके दानों में खुजली या जलन हो रही है?",
      "en": "Are your rashes itching or burning?",
      "category": "chickenpox",
      "symptom": "chickenpox",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको बुखार हो रहा है?",
      "en": "Are you experiencing a fever?",
      "category": "chickenpox",
      "symptom": "fever",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको सिरदर्द, मिचली या थकान महसूस हो रही है?",
      "en": "Are you experiencing headache, nausea, or fatigue?",
      "category": "chickenpox",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपके शरीर पर रैशेज या फफोले धीरे-धीरे फैल रहे हैं?",
      "en": "Are the rashes or blisters spreading slowly across your body?",
      "category": "chickenpox",
      "symptom": None,
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको हाल ही में चिकनपॉक्स के संपर्क में आने का अनुभव हुआ है?",
      "en": "Have you recently been in contact with someone who has chickenpox?",
      "category": "chickenpox",
      "symptom": "chickenpox",
      "risk_factor": True,
    },
    {
      "hi": "क्या आप उन क्षेत्रों में रहे हैं जहां चिकनपॉक्स का प्रकोप है?",
      "en": "Have you been in areas where there is an outbreak of chickenpox?",
      "category": "chickenpox",
      "symptom": "chickenpox",
      "risk_factor": True,
    },
  ],
"kidney issue": [
  {
    "hi": "क्या आपके पेशाब में किसी प्रकार का बदलाव (जैसे रंग, गंध, झाग या मात्रा) हुआ है?",
    "en": "Have you noticed any changes in your urine, such as color, odor, foaminess, or volume?",
    "category": "kidney issue",
    "symptom": "kidney issue",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको पीठ के निचले हिस्से या पसलियों के नीचे दर्द होता है?",
    "en": "Do you experience pain in your lower back or under your ribs?",
    "category": "kidney issue",
    "symptom": "kidney issue",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको पेशाब करने में जलन या दर्द होता है?",
    "en": "Do you feel a burning sensation or pain while urinating?",
    "category": "kidney issue",
    "symptom": None,
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको उच्च रक्तचाप (ब्लड प्रेशर) की समस्या है?",
    "en": "Do you have high blood pressure?",
    "category": "kidney issue",
    "symptom": "high blood pressure",
    "risk_factor": True,
  },
  {
    "hi": "क्या आपके परिवार में किसी को किडनी की बीमारी रही है?",
    "en": "Is there a family history of kidney disease?",
    "category": "kidney issue",
    "symptom": "kidney issue",
    "risk_factor": True,
  },
  {
    "hi": "क्या आपके शरीर में सूजन (जैसे टखनों, पैरों या चेहरे पर) आती है?",
    "en": "Do you experience swelling in your body, such as in your ankles, feet, or face?",
    "category": "kidney issue",
    "symptom": "swelling",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको मधुमेह (डायबिटीज) है या रहा है?",
    "en": "Do you have or have had diabetes?",
    "category": "kidney issue",
    "symptom": "diabetes",
    "risk_factor": True,
  },
],
 "broken voice": [
  {
    "hi": "क्या आपकी आवाज़ भारी, कर्कश या सामान्य से अलग लग रही है?",
    "en": "Does your voice sound hoarse, rough, or different from normal?",
    "category": "broken voice",
    "symptom": "broken voice",
    "risk_factor": False,
  },
  {
    "hi": "क्या बोलते समय आपकी आवाज़ टूटती है या रुक-रुक कर आती है?",
    "en": "Does your voice crack or break while speaking?",
    "category": "broken voice",
    "symptom": "broken voice",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको लंबे समय तक ऊँची आवाज़ में बोलने या चिल्लाने के बाद गले में परेशानी होती है?",
    "en": "Do you feel throat discomfort after speaking loudly or shouting for a long time?",
    "category": "broken voice",
    "symptom": None,
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको धूम्रपान करने की आदत है?",
    "en": "Do you smoke regularly?",
    "category": "broken voice",
    "symptom": "broken voice",
    "risk_factor": True,
  },
  {
    "hi": "क्या आप पेशेवर रूप से बहुत अधिक बोलते हैं, जैसे शिक्षक या गायक?",
    "en": "Do you speak a lot professionally, such as being a teacher or singer?",
    "category": "broken voice",
    "symptom": "broken voice",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपकी आवाज़ में बदलाव 2 सप्ताह से अधिक समय से है?",
    "en": "Has your voice change persisted for more than two weeks?",
    "category": "broken voice",
    "symptom": "broken voice",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपके गले में किसी प्रकार की गांठ या सूजन महसूस होती है?",
    "en": "Do you feel any lump or swelling in your throat?",
    "category": "broken voice",
    "symptom": None,
    "risk_factor": True,
  },
],
 "pregnancy": [
  {
    "hi": "क्या आपके मासिक धर्म (पीरियड्स) रुक गए हैं?",
    "en": "Have your menstrual periods stopped?",
    "category": "pregnancy",
    "symptom": "menstrual period",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको सुबह के समय मतली या उल्टी होती है?",
    "en": "Do you experience nausea or vomiting in the morning?",
    "category": "pregnancy",
    "symptom": None,
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको खाने की पसंद या स्वाद में कोई बदलाव महसूस हो रहा है?",
    "en": "Have you noticed any changes in food preferences or taste?",
    "category": "pregnancy",
    "symptom": None,
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको बार-बार पेशाब करने की इच्छा होती है?",
    "en": "Do you feel the urge to urinate more frequently?",
    "category": "pregnancy",
    "symptom": None,
    "risk_factor": False,
  },
  {
    "hi": "क्या आप गर्भधारण की योजना बना रही हैं या प्रयास कर रही हैं?",
    "en": "Are you planning or trying to conceive?",
    "category": "pregnancy",
    "symptom": None,
    "risk_factor": True,
  },
  {
    "hi": "क्या आपको अचानक थकान या चक्कर जैसा महसूस होता है?",
    "en": "Do you feel sudden fatigue or dizziness?",
    "category": "pregnancy",
    "symptom": None,
    "risk_factor": False,
  },
],
"pediatric symptoms": [
  {
    "hi": "क्या बच्चे को बुखार है या हाल ही में बुखार आया था?",
    "en": "Does the child have a fever or had one recently?",
    "category": "pediatric symptoms",
    "symptom": "fever",
    "risk_factor": False,
  },
  {
    "hi": "क्या बच्चे को खांसी या सांस लेने में दिक्कत हो रही है?",
    "en": "Is the child coughing or having difficulty breathing?",
    "category": "pediatric symptoms",
    "symptom": None,
    "risk_factor": False,
  },
  {
    "hi": "क्या बच्चे को दस्त या उल्टी हो रही है?",
    "en": "Is the child experiencing diarrhea or vomiting?",
    "category": "pediatric symptoms",
    "symptom": None,
    "risk_factor": False,
  },
  {
    "hi": "क्या बच्चे ने सामान्य से कम खाना या पीना शुरू कर दिया है?",
    "en": "Has the child started eating or drinking less than usual?",
    "category": "pediatric symptoms",
    "symptom": None,
    "risk_factor": False,
  },
  {
    "hi": "क्या बच्चे को कोई पुरानी बीमारी (जैसे अस्थमा या मिर्गी) है?",
    "en": "Does the child have any chronic condition like asthma or epilepsy?",
    "category": "pediatric symptoms",
    "symptom": None,
    "risk_factor": True,
  },
  {
    "hi": "क्या बच्चे का व्यवहार असामान्य लग रहा है, जैसे अधिक नींद या बहुत चिड़चिड़ापन?",
    "en": "Is the child's behavior unusual, such as excessive sleepiness or irritability?",
    "category": "pediatric symptoms",
    "symptom": "pediatric symptoms",
    "risk_factor": False,
  },
  {
    "hi": "क्या बच्चे को किसी प्रकार की एलर्जी या दवा से प्रतिक्रिया हुई है?",
    "en": "Has the child had any allergic reactions or medication sensitivities?",
    "category": "pediatric symptoms",
    "symptom": "pediatric symptoms",
    "risk_factor": True,
  },
],

"caesarean section": [
  {
    "hi": "क्या आपकी पिछली डिलीवरी सी-सेक्शन से हुई थी?",
    "en": "Was your previous delivery done via C-section?",
    "category": "caesarean section",
    "symptom": "caesarean section",
    "risk_factor": True,
  },
  {
    "hi": "क्या आपको हाई ब्लड प्रेशर या प्रीक्लेम्प्सिया जैसी कोई समस्या है?",
    "en": "Do you have high blood pressure or conditions like preeclampsia?",
    "category": "caesarean section",
    "symptom": None,
    "risk_factor": True,
  },
  {
    "hi": "क्या आपके प्रसव के दौरान बहुत अधिक दर्द या असामान्य रक्तस्राव हो रहा है?",
    "en": "Are you experiencing excessive pain or abnormal bleeding during labor?",
    "category": "caesarean section",
    "symptom": None,
    "risk_factor": False,
  },
  {
    "hi": "क्या डॉक्टर ने कहा है कि नॉर्मल डिलीवरी संभव नहीं है?",
    "en": "Has your doctor advised that a normal delivery may not be possible?",
    "category": "caesarean section",
    "symptom": "caesarean section",
    "risk_factor": True,
  },
  {
    "hi": "क्या आपको पहले किसी यूटेराइन (गर्भाशय) सर्जरी का इतिहास है?",
    "en": "Do you have a history of uterine surgery?",
    "category": "caesarean section",
    "symptom": None,
    "risk_factor": True,
  },
  {
    "hi": "क्या आपकी डिलीवरी की नियत तारीख से काफी समय गुजर गया है?",
    "en": "Has your due date passed significantly without labor starting?",
    "category": "caesarean section",
    "symptom": None,
    "risk_factor": False,
  },
],

   "urine issues": [
  {
    "hi": "क्या आपको पेशाब करते समय जलन या दर्द होता है?",
    "en": "Do you feel a burning sensation or pain while urinating?",
    "category": "urine issues",
    "symptom": "urine issues",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपकी पेशाब का रंग सामान्य से अलग है (जैसे गहरा पीला, लाल या बदरंग)?",
    "en": "Is the color of your urine different from normal (e.g., dark yellow, red, or cloudy)?",
    "category": "urine issues",
    "symptom": "urine issues",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपकी पेशाब से दुर्गंध आती है?",
    "en": "Does your urine have a strong or unusual odor?",
    "category": "urine issues",
    "symptom": None,
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको पेशाब में खून दिखा है?",
    "en": "Have you noticed blood in your urine?",
    "category": "urine issues",
    "symptom": "blood in urine",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको मधुमेह (डायबिटीज़) है?",
    "en": "Do you have diabetes?",
    "category": "urine issues",
    "symptom": "diabetes",
    "risk_factor": True,
  },
  {
    "hi": "क्या आपने हाल ही में पानी या तरल पदार्थ कम पिया है?",
    "en": "Have you recently been drinking less water or fluids?",
    "category": "urine issues",
    "symptom": None,
    "risk_factor": True,
  },
  {
    "hi": "क्या आपको बार-बार पेशाब आने के साथ-साथ अधूरी पेशाब महसूस होती है?",
    "en": "Do you feel the urge to urinate frequently but pass only a small amount each time?",
    "category": "urine issues",
    "symptom": "urine issues",
    "risk_factor": False,
  },
],

"wound": [
  {
    "hi": "क्या घाव से खून रुक-रुक कर या लगातार बह रहा है?",
    "en": "Is the wound bleeding continuously or off and on?",
    "category": "wound",
    "symptom": "wound",
    "risk_factor": False,
  },
  {
    "hi": "क्या घाव वाली जगह में सूजन, लालिमा या गर्माहट महसूस होती है?",
    "en": "Is the wound area swollen, red, or warm to the touch?",
    "category": "wound",
    "symptom": None,
    "risk_factor": False,
  },
  {
    "hi": "क्या घाव से पीप या दुर्गंध आ रही है?",
    "en": "Is there any pus or foul smell coming from the wound?",
    "category": "wound",
    "symptom": None,
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको डायबिटीज़ या कोई अन्य ऐसी बीमारी है जो घाव भरने में देरी करती है?",
    "en": "Do you have diabetes or any condition that delays wound healing?",
    "category": "wound",
    "symptom": None,
    "risk_factor": True,
  },
  {
    "hi": "क्या आपको घाव हुए 3 दिन से ज्यादा हो गए हैं लेकिन वह भर नहीं रहा?",
    "en": "Has it been more than 3 days since you got the wound and it still hasn't healed?",
    "category": "wound",
    "symptom": "wound",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपने टेटनस का टीका हाल ही में नहीं लगवाया है?",
    "en": "Have you not had a recent tetanus vaccination?",
    "category": "wound",
    "symptom": "medication",
    "risk_factor": True,
  },
  {
    "hi": "क्या घाव किसी गंदे या जंग लगे चीज़ से हुआ था?",
    "en": "Was the wound caused by something dirty or rusty?",
    "category": "wound",
    "symptom": None,
    "risk_factor": True,
  },
],

"body ache": [
  {
    "hi": "क्या आपके पूरे शरीर में दर्द या थकावट महसूस होती है?",
    "en": "Do you feel pain or fatigue throughout your entire body?",
    "category": "body ache",
    "symptom": None,
    "risk_factor": False,
  },
  {
    "hi": "क्या आपकी मांसपेशियाँ या जोड़ दबाने पर दर्द करते हैं?",
    "en": "Do your muscles or joints hurt when pressed?",
    "category": "body ache",
    "symptom": None,
    "risk_factor": False,
  },
  {
    "hi": "क्या दर्द के साथ आपको बुखार, सर्दी या गले में खराश भी है?",
    "en": "Along with body ache, do you also have fever, cold, or sore throat?",
    "category": "body ache",
    "symptom": None,
    "risk_factor": False,
  },
  {
    "hi": "क्या आप हाल ही में किसी वायरल संक्रमण (जैसे फ्लू या डेंगू) से ठीक हुए हैं?",
    "en": "Have you recently recovered from a viral infection like flu or dengue?",
    "category": "body ache",
    "symptom": None,
    "risk_factor": True,
  },
  {
    "hi": "क्या आप लंबे समय तक एक ही मुद्रा में बैठे या खड़े रहते हैं?",
    "en": "Do you sit or stand in the same posture for long periods?",
    "category": "body ache",
    "symptom": None,
    "risk_factor": True,
  },
  {
    "hi": "क्या आपको नींद पूरी नहीं हो पाती या आराम नहीं मिलता?",
    "en": "Are you not getting enough sleep or proper rest?",
    "category": "body ache",
    "symptom": None,
    "risk_factor": True,
  },
  {
    "hi": "क्या दर्द लगातार कई दिनों से बना हुआ है?",
    "en": "Has the pain been persistent for several days?",
    "category": "body ache",
    "symptom": "body ache",
    "risk_factor": False,
  },
],

"bruises": [
  {
    "hi": "क्या आपके शरीर पर बिना किसी चोट के नीले या काले निशान बन जाते हैं?",
    "en": "Do you get blue or black marks (bruises) on your body without any known injury?",
    "category": "bruises",
    "symptom": "bruises",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको बहुत मामूली चोट पर भी आसानी से निशान पड़ जाते हैं?",
    "en": "Do you bruise easily, even from minor bumps or touches?",
    "category": "bruises",
    "symptom": "bruises",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपके शरीर पर कई जगह एक साथ निशान बन रहे हैं?",
    "en": "Are you getting bruises on multiple areas of the body at the same time?",
    "category": "bruises",
    "symptom": None,
    "risk_factor": False,
  },
  {
    "hi": "क्या आप खून पतला करने वाली दवाएं (जैसे एस्पिरिन या वारफरिन) ले रहे हैं?",
    "en": "Are you taking blood thinners such as aspirin or warfarin?",
    "category": "bruises",
    "symptom": None,
    "risk_factor": True,
  },
  {
    "hi": "क्या आपके परिवार में खून से संबंधित कोई बीमारी (जैसे हीमोफीलिया) है?",
    "en": "Is there a family history of blood disorders like hemophilia?",
    "category": "bruises",
    "symptom": None,
    "risk_factor": True,
  },
  {
    "hi": "क्या आपको हाल ही में कमजोरी, थकान या चक्कर जैसा महसूस हो रहा है?",
    "en": "Have you recently been feeling weak, tired, or dizzy?",
    "category": "bruises",
    "symptom": None,
    "risk_factor": False,
  },
  {
    "hi": "क्या आपके शरीर पर बने निशान दर्दनाक या सूजे हुए हैं?",
    "en": "Are the bruises on your body painful or swollen?",
    "category": "bruises",
    "symptom": None,
    "risk_factor": False,
  },
],

	"cold_intolerance": [
  {
    "hi": "क्या आपको सामान्य से अधिक ठंड लगती है, जब दूसरों को सामान्य लगता है?",
    "en": "Do you feel colder than others around you in normal temperatures?",
    "category": "cold intolerance",
    "symptom": "increased sensitivity to cold",
    "risk_factor": False,
  },
  {
    "hi": "क्या ठंडी जगह में रहने से आपके हाथ या पैर सुन्न हो जाते हैं या रंग बदलते हैं?",
    "en": "Do your hands or feet become numb or change color when exposed to cold?",
    "category": "cold intolerance",
    "symptom": "extremity response to cold",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको ठंड में थकान, कमजोरी या मानसिक भ्रम जैसी समस्याएं होती हैं?",
    "en": "Do you experience fatigue, weakness, or mental fog in cold environments?",
    "category": "cold intolerance",
    "symptom": "cold-related fatigue or confusion",
    "risk_factor": False,
  },
{
  "hi": "क्या आप ठंड से बचने के लिए सामान्य से अधिक गर्म कपड़े पहनते हैं?",
  "en": "Do you find yourself needing to wear more layers or warmer clothing than others to stay comfortable in the cold?",
  "category": "cold intolerance",
  "symptom": "excessive need for warmth",
  "risk_factor": False,
},
{
  "hi": "क्या ठंड के कारण आपकी नींद में खलल पड़ता है या आप रात में जाग जाते हैं?",
  "en": "Does cold interfere with your sleep or cause you to wake up during the night?",
  "category": "cold intolerance",
  "symptom": "sleep disruption due to cold",
  "risk_factor": False,
},
  
{
    "hi": "क्या आपके शरीर का तापमान दूसरों की तुलना में जल्दी कम हो जाता है?",
    "en": "Does your body temperature drop more quickly than others in cold conditions?",
    "category": "cold intolerance",
    "symptom": "rapid drop in body temperature",
    "risk_factor": False,
  },
],

"goiter": [
  {
    "hi": "क्या आपकी गर्दन के सामने किसी प्रकार की सूजन या उभार महसूस हो रहा है?",
    "en": "Do you feel any swelling or lump in the front of your neck?",
    "category": "goiter",
    "symptom": "neck swelling or lump",
    "risk_factor":False,
  },
  {
    "hi": "क्या आपको निगलने या सांस लेने में कठिनाई हो रही है?",
    "en": "Are you experiencing difficulty in swallowing or breathing?",
    "category": "goiter",
    "symptom": "difficulty swallowing or breathing",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपकी आवाज़ भारी या कर्कश हो गई है?",
    "en": "Has your voice become hoarse or rough?",
    "category": "goiter",
    "symptom": "hoarseness of voice",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको थकान, ठंड सहन करने में कठिनाई, या वजन बढ़ने जैसी समस्याएं हैं?",
    "en": "Do you experience fatigue, difficulty tolerating cold, or unexplained weight gain?",
    "category": "goiter",
    "symptom": "hypothyroid symptoms",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपके खान-पान में आयोडीन की कमी है या आप ऐसे क्षेत्र में रहते हैं जहाँ आयोडीन की कमी आम है?",
    "en": "Do you have an iodine-deficient diet or live in an area where iodine deficiency is common?",
    "category": "goiter",
    "symptom": "iodine deficiency",
    "risk_factor": True,
  },
  {
    "hi": "क्या आपके परिवार में किसी को थायरॉइड या गले की सूजन से संबंधित समस्या रही है?",
    "en": "Is there a family history of thyroid disorders or neck swelling?",
    "category": "goiter",
    "symptom": "family history",
    "risk_factor": True,
  },
],

"slow reflexes": [
  {
    "hi": "क्या आपको लगता है कि आपकी प्रतिक्रिया गति (रिफ्लेक्स) धीमी हो गई है?",
    "en": "Do you feel that your reaction time or reflexes have become slower?",
    "category": "slow reflexes",
    "symptom": "subjective slowness of reflexes",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपने हाल ही में थकान, सुस्ती या कम ऊर्जा का अनुभव किया है?",
    "en": "Have you recently experienced fatigue, sluggishness, or low energy?",
    "category": "slow reflexes",
    "symptom": "sluggishness or fatigue",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपकी मांसपेशियों की ताकत या गतिविधि में कोई कमी आई है?",
    "en": "Have you noticed any decrease in muscle strength or activity?",
    "category": "slow reflexes",
    "symptom": "muscle weakness",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको थायरॉइड, न्यूरोलॉजिकल या मेटाबॉलिक बीमारी का कोई इतिहास है?",
    "en": "Do you have a history of thyroid, neurological, or metabolic disorders?",
    "category": "slow reflexes",
    "symptom": "underlying medical history",
    "risk_factor": True,
  },
  {
    "hi": "क्या आपने हाल ही में सिर पर चोट या कोई न्यूरोलॉजिकल समस्या का सामना किया है?",
    "en": "Have you recently had a head injury or experienced any neurological issue?",
    "category": "slow reflexes",
    "symptom": "recent head injury or neuro issue",
    "risk_factor": True,
  },
],
"male reproductive issues": [
  {
    "hi": "क्या आपको यौन उत्तेजना या संभोग के दौरान लिंग में तनाव बनाए रखने में कठिनाई होती है?",
    "en": "Do you have difficulty maintaining an erection during sexual activity?",
    "category": "male_reproductive_issues",
    "symptom": "erectile dysfunction",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपकी यौन इच्छा (लिबिडो) में कमी आई है?",
    "en": "Have you noticed a decrease in your sexual desire (libido)?",
    "category": "male_reproductive_issues",
    "symptom": "low libido",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको वीर्य स्खलन में कोई समस्या हो रही है, जैसे जल्दी स्खलन या देरी से स्खलन?",
    "en": "Are you experiencing problems with ejaculation, such as premature or delayed ejaculation?",
    "category": "male_reproductive_issues",
    "symptom": "ejaculation problems",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको अंडकोष या उसके आसपास दर्द, सूजन या गांठ महसूस हो रही है?",
    "en": "Do you feel pain, swelling, or a lump in or around the testicles?",
    "category": "male_reproductive_issues",
    "symptom": "testicular pain or swelling",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको मूत्र मार्ग में जलन, दर्द या बार-बार पेशाब की समस्या है?",
    "en": "Are you experiencing burning, pain, or frequent urination?",
    "category": "male_reproductive_issues",
    "symptom": "urinary symptoms",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको मधुमेह, उच्च रक्तचाप या मोटापे जैसी कोई पुरानी बीमारी है?",
    "en": "Do you have chronic conditions such as diabetes, high blood pressure, or obesity?",
    "category": "male_reproductive_issues",
    "symptom": "chronic diseases",
    "risk_factor": True,
  },
  {
    "hi": "क्या आपके परिवार में किसी को प्रजनन संबंधी समस्याएं रही हैं?",
    "en": "Is there a family history of reproductive issues?",
    "category": "male_reproductive_issues",
    "symptom": "family history",
    "risk_factor": True,
  },
],
	
"female reproductive issues": [
  {
    "hi": "क्या आपकी माहवारी अनियमित है या छूट रही है?",
    "en": "Is your menstrual cycle irregular or missing?",
    "category": "female_reproductive_issues",
    "symptom": "irregular or missed periods",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको माहवारी के दौरान अत्यधिक रक्तस्राव या दर्द होता है?",
    "en": "Do you experience heavy bleeding or severe pain during periods?",
    "category": "female_reproductive_issues",
    "symptom": "heavy or painful periods",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको योनि से असामान्य स्राव, जलन या खुजली होती है?",
    "en": "Are you experiencing abnormal vaginal discharge, burning, or itching?",
    "category": "female_reproductive_issues",
    "symptom": "vaginal discharge or irritation",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको संभोग के दौरान दर्द होता है?",
    "en": "Do you experience pain during sexual intercourse?",
    "category": "female_reproductive_issues",
    "symptom": "painful intercourse",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको अचानक वजन बढ़ने, मुंहासे, या चेहरे/शरीर पर अत्यधिक बालों की समस्या है?",
    "en": "Have you noticed sudden weight gain, acne, or excessive hair growth on the face/body?",
    "category": "female_reproductive_issues",
    "symptom": "PCOS-like symptoms",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको बार-बार गर्भपात का अनुभव हुआ है?",
    "en": "Have you experienced repeated miscarriages?",
    "category": "female_reproductive_issues",
    "symptom": "recurrent miscarriage",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपके परिवार में किसी को प्रजनन संबंधी समस्याएं रही हैं?",
    "en": "Is there a family history of reproductive health issues?",
    "category": "female_reproductive_issues",
    "symptom": "family history",
    "risk_factor": True,
  },
  {
    "hi": "क्या आपने कोई प्रसवपूर्व संक्रमण, पेल्विक सर्जरी, या गर्भाशय से संबंधित कोई समस्या झेली है?",
    "en": "Have you had any infections during pregnancy, pelvic surgeries, or uterine problems?",
    "category": "female_reproductive_issues",
    "symptom": "pregnancy or uterine history",
    "risk_factor": True,
  },
],
"dandruff": [
  {
    "hi": "क्या आपकी खोपड़ी से सफेद या पीले रंग की परतदार रूसी झड़ती है?",
    "en": "Do you notice white or yellowish flaky dandruff falling from your scalp?",
    "category": "dandruff",
    "symptom": "flaky scalp",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपकी खोपड़ी में खुजली होती है?",
    "en": "Do you experience itching on your scalp?",
    "category": "dandruff",
    "symptom": "itchy scalp",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपकी खोपड़ी पर लालपन या जलन महसूस होती है?",
    "en": "Do you feel redness or irritation on your scalp?",
    "category": "dandruff",
    "symptom": "scalp redness or irritation",
    "risk_factor": False,
  },
  {
    "hi": "क्या बाल धोने के बावजूद भी रूसी बार-बार लौट आती है?",
    "en": "Does the dandruff keep returning even after washing your hair?",
    "category": "dandruff",
    "symptom": "persistent dandruff",
    "risk_factor": False,
  },
  {
    "hi": "क्या आप अत्यधिक तेल वाले उत्पाद या हेयर स्टाइलिंग प्रोडक्ट्स का उपयोग करते हैं?",
    "en": "Do you frequently use oily or heavy hair styling products?",
    "category": "dandruff",
    "symptom": "use of oily hair products",
    "risk_factor": True,
  },
  {
    "hi": "क्या आप नियमित रूप से अपने बाल नहीं धोते या साफ नहीं रखते?",
    "en": "Do you not wash or clean your hair regularly?",
    "category": "dandruff",
    "symptom": "poor scalp hygiene",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको एक्जिमा, सोरायसिस या अन्य त्वचा रोगों का इतिहास है?",
    "en": "Do you have a history of eczema, psoriasis, or other skin conditions?",
    "category": "dandruff",
    "symptom": "skin condition history",
    "risk_factor": True,
  },
],

"blister": [
    {
        "hi": "क्या ये छाले जलने, रगड़ या एलर्जी के बाद आए हैं?",
        "en": "Did the blisters appear after a burn, friction, or an allergy?",
        "category": "blisters_cause",
        "symptom": "Blisters due to irritation",
        "risk_factor": False
    },
    {
        "hi": "क्या छाले दर्दनाक या खुजली वाले हैं?",
        "en": "Are the blisters painful or itchy?",
        "category": "blisters_pain_itch",
        "symptom": "Painful or itchy blisters",
        "risk_factor": False
    },

    {
        "hi": "क्या छाले फट गए हैं और तरल पदार्थ निकल रहा है?",
        "en": "Have the blisters burst and are releasing fluid?",
        "category": "blisters_burst",
        "symptom": "Burst blisters with discharge",
        "risk_factor": False
    },

]




}

# ------------------------------------------------------------------ #
# ----------------------- Medicine Name List ----------------------- #
# ------------------------------------------------------------------ #
medications_list = [
    "ibuprofen", "acetaminophen", "paracetamol", "aspirin", "naproxen", "acetylsalicylic acid",
    "diclofenac", "meloxicam", "celecoxib", "indomethacin", "ketorolac", "butalbital", "dolo" ,"dolo 650",
    "algal oil",  "cod liver oil",  "flaxseed oil", "fish oil", "omega 3", "ORS sachets", "ointment",
    "Electral", "Glucon-D", "Prolyte", "Winlyte", "ORS", "eye drops", "ear drops", "eye drop", "ear drop",
    # Antibiotics
    "amoxicillin", "azithromycin", "doxycycline", "ciprofloxacin", "clindamycin", "metronidazole",
    "cephalexin", "amoxicillin-clavulanate", "levofloxacin", "linezolid", "meropenem", "vancomycin",
    "fluconazole", "tetracycline", "rifampin", "sulfamethoxazole-trimethoprim", "nystatin",
    # Cardiovascular
    "lisinopril", "atorvastatin", "simvastatin", "rosuvastatin", "furosemide", "clopidogrel", "warfarin",
    "heparin", "digoxin", "nifedipine", "amlodipine", "atenolol", "tamsulosin", "isosorbide mononitrate",
    "losartan", "metoprolol", "propranolol", "hydralazine", "captopril", "carvedilol", "valsartan",
    "eplerenone", "nicorandil", "ranolazine", "dobutamine", "nitrate", "statin",
    # Diabetes and Endocrine
    "metformin", "insulin", "glimepiride", "glipizide", "glyburide", "sitagliptin", "pioglitazone",
    "liraglutide", "exenatide", "liraglutide", "canagliflozin", "dapagliflozin", "levothyroxine",
    "sodium bicarbonate", "hydrocortisone", "prednisone", "levothyroxine", "desmopressin", "teriparatide",
    # Respiratory / Allergies
    "albuterol", "cetirizine", "loratadine", "fexofenadine", "salbutamol", "montelukast", "levocetirizine",
    "betahistine", "fluticasone", "budesonide", "beclometasone", "theophylline", "ipratropium", "mometasone",
    "salmeterol", "formoterol", "tuscalo", "aminophylline", "naloxone", "dextromethorphan",
    # Mental Health / Neurology
    "sertraline", "citalopram", "escitalopram", "gabapentin", "hydrocodone", "codeine", "tramadol",
    "lorazepam", "diazepam", "clonazepam", "melatonin", "antidepressant", "antianxiety", "clonidine", "aripiprazole",
    "quetiapine", "risperidone", "lithium", "vortioxetine", "duloxetine", "venlafaxine", "bupropion", "mirtazapine",
    "buspirone", "modafinil", "carbamazepine", "topiramate", "lamotrigine", "valproic acid", "levetiracetam",
    "phenytoin", "oxcarbazepine", "zaleplon", "zolpidem", "eszopiclone",
    # Gastrointestinal
    "omeprazole", "pantoprazole", "antacid", "metoclopramide", "ranitidine", "famotidine", "esomeprazole",
    "lansoprazole", "hydrochlorothiazide", "bismuth subsalicylate", "bisacodyl", "docusate", "loperamide", "diphenoxylate",
    "aluminum hydroxide", "sucralfate", "misoprostol", "codeine phosphate",
    # Vitamins and Supplements
    "zinc", "vitamin c", "vitamin d", "multivitamin", "folic acid", "vitamin b12", "vitamin e",
    "iron sulfate", "calcium carbonate", "magnesium oxide", "potassium chloride", "manganese", "iodine",
    "biotin", "collagen", "probiotic", "omega-3", "fish oil","vitamin D",
    # Other
    "prednisone", "hydroxychloroquine", "betahistine", "antibiotic", "antiplatelet", "anticoagulant", "fentanyl",
    "methadone", "buprenorphine", "naloxone", "acetylcysteine", "digoxin", "thiamine", "fluphenazine",
    "morphine", "methocarbamol", "colchicine", "dantrolene", "loperamide", "theophylline", "apixaban",
    "dabigatran", "rivaroxaban", "pantoprazole", "benzonatate", "immunoglobulin", "neostigmine", "levodopa",
    "entacapone", "bromocriptine", "carbidopa", "tizanidine", "probenecid", "allopurinol", "febuxostat",
    "colchicine", "methylprednisolone", "hydrocortisone", "bupropion", "clozapine", "chlorpromazine", "phenelzine",
    "tranylcypromine", "bromocriptine", "tretinoin", "hydroxyzine", "terbinafine", "dapsone", "lidocaine",
    "hydroxyurea", "azathioprine", "cyclophosphamide", "methotrexate", "sulfasalazine", "dimercaprol",
    "dantrolene", "adrenaline", "epinephrine", "tylenol", "xanax", "valium", "ambien", "ativan", "prozac",
    # Dermatology (Skin-related)
    "clotrimazole", "ketoconazole", "hydrocortisone", "tretinoin", "benzoyl peroxide", "clindamycin gel",
    "adapalene", "hydroxychloroquine", "salicylic acid", "calcipotriene", "betamethasone", "mupirocin",
    "fluticasone cream", "permethrin", "coal tar", "finasteride", "isotretinoin", "gentamicin", "pimecrolimus",
    "tacrolimus", "azelaic acid",
    # Musculoskeletal Disorders
    "methocarbamol", "baclofen", "tizanidine", "carisoprodol", "cyclobenzaprine", "diclofenac gel",
    "celecoxib", "indomethacin", "colchicine", "allopurinol", "febuxostat", "naproxen", "hydroxychloroquine",
    "prednisone", "methylprednisolone", "gabapentin", "tramadol", "etoricoxib", "oxcarbazepine", "tizanidine",
    # Immunosuppressants / Immunology
    "methotrexate", "azathioprine", "mycophenolate mofetil", "cyclophosphamide", "tacrolimus", "sirolimus",
    "prednisolone", "bendamustine", "rituximab", "infliximab", "adalimumab", "etanercept", "leflunomide",
    "hydroxychloroquine", "intravenous immunoglobulin", "tofacitinib", "abatacept", "etanercept", "sulfasalazine",
    "cyclosporine", "belimumab",
    # Ophthalmology (Eye-related)
    "latanoprost", "timolol", "brimonidine", "prednisolone acetate", "neomycin-polymyxin-bacitracin", "pilocarpine",
    "dorzolamide", "bimatoprost", "hydroxychloroquine", "tobramycin", "moxifloxacin", "gentamicin drops",
    "sulfacetamide", "cyclopentolate", "hydrocortisone", "levofloxacin ophthalmic", "ketorolac ophthalmic",
    "flurbiprofen", "povidone-iodine", "dexamethasone", "lisinopril", "azithromycin",
    "acetazolamide (for glaucoma)",
    # Urology
    "finasteride", "tamsulosin", "sildenafil", "terazosin", "dutasteride", "vardenafil", "tadalafil", "alfuzosin",
    "oxybutynin", "tolterodine", "mirabegron", "desmopressin", "bethanechol", "dapoxetine", "flomax", "proscar"
    "silodosin", "bupropion", "indomethacin", "methyltestosterone", "tadalafil", "hydroxyurea", "gabapentin",
    "tramadol", "famotidine", "alpha blockers", "calcitonin", "hydrocodone", "morphine",
    # Anti-Viral and Anti-fungal
    "oseltamivir", "zanamivir", "acylovir", "valacyclovir", "ganciclovir", "amphotericin", "fluconazole",
    "terbinafine", "itraconazole", "nystatin", "clotrimazole", "ketoconazole", "miconazole", "fluconazole", "terbinafine",
    "griseofulvin", "miconazole", "nystatin", "terbinafine"
]

trigger_keywords = {
'tooth': {
        'injury': ['injury', 'injured', 'injure', 'knock', 'blow', 'hit'],
        'sensitivity': ['sensitive', 'sensitivity', 'hard', 'gum', 'gums', 'bleeding'],
        'pain': ['pain', 'painful', 'paining', 'ache', 'aching', 'hurt', 'hurting', 'sore', 'throbbing'],
        'broken': ['broken', 'break', 'broke', 'breaks', 'cracked', 'chip', 'chipped', 'fell', 'fall', 'fallen'],
        'decay': ['decay', 'decayed', 'decays', 'cavity', 'cavities', 'cavitated'],
	'tingling': ['tingling', 'tingled', 'pins and needles', 'prickling', 'buzzing','sensation']
    },
'leg': {
        'injury': ['injury', 'injured', 'twist', 'twists','twisted', 'sprain', 'sprained', 'sprains','fracture', 'fractured', 'broke', 'broken', 'fall', 'fell', 'hurt', 'accident'],
        'pain': ['pain', 'paining', 'ache', 'aching', 'throbbing', 'sharp', 'dull', 'cramp', 'cramping', 'stiff', 'stiffness','pains','hurts'],
        'swelling': ['swelling', 'swollen', 'swells', 'swell','bump', 'puffy', 'inflamed', 'bulge'],
        'itching': ['itch', 'itching', 'itches', 'itched', 'itchiness'],
        'weakness': ['weak', 'weakened', 'weakness', 'fatigue', 'tired', 'no strength', 'drained'],
        'numbness': ['numb', 'numbed', 'numbs', 'numbness', 'tingle', 'tingled', 'tingling', 'pins', 'needles'],
	'freeze': ['freeze', 'freezing', 'frozen', 'chilled'],
        'spasm': ['spasm', 'spasms', 'tightness', 'twitch', 'twitching']
    },

'eye': {
        'itching': ['itchy', 'itching', 'itch', 'itches', 'scratchy', 'scratching', 'irritated', 'irritation','itchiness'],
        'redness': ['redness', 'red', 'reddish', 'bloodshot', 'pink', 'inflamed', 'discoloration'],
        'burn': ['burn', 'burning', 'burnt', 'irritation', 'sting', 'stinging'],
        'weakness': ['weak', 'weakness', 'tired eyes', 'eye strain', 'fatigued eyes', 'weakened'],
        'pain': ['pain', 'pains', 'ache', 'aches', 'hurt', 'hurts', 'sore', 'throbbing', 'discomfort'],
        'blurry vision': ['blurry', 'blurred', 'blur', 'blurry vision', 'not clear', 'foggy', 'unclear', 'hazy', 'double vision'],
	    'swelling': ['swollen','swells', 'swell', 'puffy', 'swelling', 'bulging', 'bump']
    },
'hand': {
        'pain': ['pain', 'pains', 'ache', 'aches', 'hurt', 'hurts', 'sore', 'throbbing', 'aching'],
	'weakness': ['weakness', 'weak',  'fatigued', 'can’t grip', 'loss of strength', 'tremble', 'can’t hold'],
        'numbness': ['numb', 'numbed', 'numbs', 'numbness', 'tingle', 'tingling', 'pins', 'needles'],
        'swelling': ['swelling', 'swollen', 'swells', 'swell','bump', 'puffy', 'inflamed', 'bulge'],
        'injury': ['injury', 'injured', 'fracture', 'fractured', 'broke', 'broken', 'wound', 'wounded', 'crack', 'cracked', 'hit', 'hurt', 'twist', 'twisted'],
        'dryness': ['dry', 'dryness', 'cracked', 'rough', 'peeling', 'flaky', 'chapped'],
        'itching': ['itch', 'itches', 'itching', 'itched', 'itchiness', 'scratchy'],
	'freeze': ['freeze', 'freezing', 'frozen', 'chilled']
    },
'arm': {
        'pain': ['pain', 'pains', 'paining', 'ache', 'aches', 'hurt', 'hurts', 'sore', 'throbbing', 'aching'],
        'numbness': ['numb', 'numbed', 'numbs', 'numbness', 'tingle', 'tingling', 'tingles','pins', 'needles', 'numbing'],
        'injury': ['injury', 'injured', 'fracture', 'fractured', 'broke', 'broken', 'fall', 'fell', 'hit', 'knocked', 'bruise', 'bruised', 'sprain'],
        'weakness': ['weak', 'weakened', 'weakness', 'tired', 'fatigue', 'no strength', 'drained'],
	    'spasm': ['spasm', 'spasms', 'cramp', 'tightness', 'twitching'],
	    'itching': ['itch', 'itching', 'itchy', 'itchiness', 'scratchy'],
        'swelling': ['swollen', 'swells', 'swell', 'puffy', 'swelling', 'bulging', 'bump']
    },
'head': {
        'injury': ['injury', 'injured', 'bump', 'hit', 'knock', 'knocked', 'blow', 'fall', 'fell', 'impact', 'strike', 'broken'],
        'pressure': ['pressure', 'tightness', 'heaviness', 'tense', 'tension', 'compressed'],
	'numbness': ['numb', 'numbness', 'no sensation'],
	'itching': ['itch', 'itching', 'scratchy', 'tingle', 'irritation'],
	'pain' : ['pain', 'paining', 'pains', 'hurts','hurting', 'hurt']
	
    },
'back': {
        'pain': ['backache', 'pain', 'pains', 'hurt', 'hurts', 'sore', 'sores', 'ache', 'aches', 'aching'],
	'weakness': ['weakness', 'weak',  'fatigued', 'tired', 'can’t support', 'loss of strength', 'giving way'],
        'stiffness': ['stiff', 'stiffs', 'stiffness', 'tight', 'tense', 'tension', 'rigid', 'locked','tightness'],
        'injury': ['injury', 'injured', 'fall', 'fell', 'lifted', 'twist', 'twists', 'twisted', 'accident', 'pulled', 'strain', 'strained', 'broken'],
        'numbness': ['numb', 'numbed', 'numbness', 'tingle', 'tingling', 'pins', 'needles'],
	'spasm' : ['spasm','spasms','spasmed'],
	'itching': ['itch', 'itching', 'itchy', 'itchiness', 'scratchy'],
        'issue': ['issue', 'issues', 'problem', 'problems', 'condition', 'discomfort']
    },
'chest': {
        'pain': ['pain', 'pains', 'tightness', 'tight', 'pressure', 'hurt', 'hurts', 'ache', 'aches', 'burning', 'burn', 'soreness'],
	'weakness': ['weakness', 'weak',  'fatigued', 'tired', 'heaviness', 'pressure', 'loss of strength'],
        'discomfort': ['discomfort', 'uneasy', 'weird', 'heaviness', 'unusual feeling', 'tight'],
        'breathing': ['shortness of breath', 'difficulty breathing', 'breathing problem', 'tight chest', 'can’t breathe', 'labored breathing', 'breathless'],
        'palpitations': ['palpitations', 'heart racing', 'fluttering', 'pounding', 'fast heartbeat', 'rapid heartbeat'],
	'itching': ['itch', 'itching', 'itchy', 'itchiness', 'scratchy']
    },
'wrist': {
        'pain': ['pain', 'hurt', 'hurts', 'ache', 'aches', 'throbbing', 'burning', 'soreness'],
	'weakness': ['weakness', 'weak', 'fatigued', 'can’t grip', 'loss of strength', 'shaky', 'tremble', 'can’t hold'],
        'swelling': ['swelling', 'swollen', 'swells', 'swell','bump', 'puffy', 'inflamed', 'bulge'],
        'stiffness': ['stiff', 'stiffness', 'tight', 'restricted', 'rigid', 'locked'],
        'numbness': ['numb', 'numbed', 'numbness', 'tingle', 'tingling', 'pins', 'needles'],
        'injury': ['injury', 'injured', 'fall', 'fell', 'fracture', 'fractured', 'twist', 'twisted', 'sprain', 'sprained', 'broke', 'broken']
    },
'throat': {
        'pain': ['sore', 'pain', 'scratchy', 'hurt', 'ache','pains', 'throbbing', 'burning','hurts','hurting','paining'],
        'swelling': ['swelling', 'swollen', 'swells', 'swell','bump', 'puffy', 'inflamed', 'bulge'],
        'difficulty_swallowing': ['difficulty swallowing', 'trouble swallowing', 'painful swallowing','swallowing'],
        'hoarseness': ['hoarse', 'raspy', 'rough voice', 'lost voice','hoarseness'],
        'infection': ['infection', 'fever', 'cold', 'flu', 'strep','infected','infections','infected'],
	'itching': ['itch', 'itching', 'itchy', 'itchiness', 'scratchy']
    },
'stomach': {
        'pain': ['pain', 'ache', 'hurt', 'cramp', 'cramps', 'discomfort', 'throbbing','aches''hurts','hurting','sore','sores','pains'],
	'weakness': ['weakness', 'weak', 'fatigued', 'tired', 'no strength', 'can’t engage', 'loss of core strength'],
        'bloating': ['bloating', 'bloated', 'gas', 'gassy', 'fullness', 'distention'],
        'nausea': ['nausea', 'queasy', 'feeling sick', 'vomit', 'vomiting', 'urge to vomit'],
        'diarrhea': ['diarrhea', 'loose stool', 'watery stool', 'frequent stool', 'runny stool']
    },
'neck': {
        'pain': ['pain', 'pains', 'hurt', 'hurts', 'sore', 'sores', 'ache', 'aches', 'aching','throbbing',],
	'weakness': ['weakness', 'weak', 'fatigued', 'tired', 'can’t hold up', 'loss of strength', 'unstable'],
        'stiffness': ['stiff', 'stiffness', 'tight', 'rigid', 'locked', 'tense', 'tension'],
        'swelling': ['swelling', 'swollen', 'lump', 'bump', 'enlarged', 'inflamed'],
        'injury': ['injury', 'injured', 'whiplash', 'fall', 'fell', 'hit', 'knock', 'twist', 'twisted'],
        'numbness': ['numb', 'numbness', 'numbed', 'tingle', 'tingling', 'pins', 'needles'],
	'itching': ['itch', 'itching', 'scratchy', 'itchiness'],
        'bleeding': ['bleeding', 'blood', 'bleed', 'cut'],
	'spasm': ['spasm', 'spasms', 'cramp', 'tightness', 'twitching']

    },
'knee': {
        'pain': ['pain', 'pains', 'hurt', 'hurts', 'sore', 'sores', 'ache', 'aches', 'aching'],
        'swelling': ['swelling', 'swollen', 'swells', 'swell','bump', 'puffy', 'inflamed', 'bulge'],
        'stiffness': ['stiff', 'stiffness', 'locked', 'tight', 'rigid'],
        'injury': ['injury', 'injured', 'twist', 'twisted', 'fall', 'fell', 'hit', 'sprain', 'sprained', 'fracture', 'fractured'],
        'weakness': ['weak', 'weakness', 'unstable', 'giving way', "can’t stand", 'buckling'],
        'numbness': ['numb', 'numbness', 'numbed', 'tingling', 'tingle', 'pins', 'needles'],
	'freeze': ['freeze', 'freezing', 'frozen', 'chilled'],
	'itching': ['itch', 'itching', 'itchy', 'itchiness', 'scratchy']
    },
'foot': {
        'pain': ['pain', 'ache', 'hurts', 'hurt', 'sore', 'throbbing', 'burning'],
	'weakness': ['weakness', 'weak', 'fatigued', 'tired', 'giving way', 'can’t push off', 'loss of strength'],
        'swelling': ['swelling', 'swollen', 'swells', 'swell','bump', 'puffy', 'inflamed', 'bulge'],
        'numbness': ['numb', 'numbed', 'numbness', 'tingling', 'tingle', 'pins', 'needles'],
        'injury': ['injury', 'injured', 'fall', 'fell', 'twist', 'twisted', 'fracture', 'fractured', 'sprain', 'sprained', 'broke', 'broken'],
        'stiffness': ['stiff', 'stiffness', 'tight', 'rigid', 'locked', 'restricted'],
	'freeze': ['freeze', 'freezing', 'frozen', 'chilled'],
	'spasm': ['spasm', 'spasms', 'cramp', 'tightness', 'twitching'],
	'itching': ['itch', 'itching', 'scratchy', 'itchiness']
    },
'shoulder': {
        'pain': ['pain', 'pains', 'hurt', 'hurts', 'sore', 'sores', 'ache', 'aches', 'aching','throbbing',],
        'stiffness': ['stiff', 'tight', 'frozen', 'freeze', 'locked', 'restricted', 'stiffness'],
        'injury': ['injury', 'injured', 'fall', 'fell', 'twist', 'twisted', 'dislocate', 'dislocated', 'fracture', 'fractured'],
        'numbness': ['numb', 'numbed', 'numbness', 'tingling', 'tingle', 'pins', 'needles'],
        'weakness': ['weak', 'weakness', 'unstable', 'weakened', "can’t lift", 'difficulty lifting'],
	'itching': ['itch', 'itching', 'itchy', 'itchiness', 'scratchy']
    },
'ear': {
        'pain': ['pain', 'pains', 'hurt', 'hurts', 'sore', 'sores', 'ache', 'aches', 'aching','throbbing',],
        'hearing loss': ['hearing loss', "can’t hear", 'muffled', 'low hearing'],
        'ringing': ['ringing', 'buzzing', 'tinnitus', 'noise in ear','rings','ring'],
        'discharge': ['discharge', 'fluid', 'pus', 'leaking', 'drainage','discharges','discharged'],
        'infection': ['infection', 'fever', 'swelling', 'ear infection'],
        'freeze': ['freeze', 'freezing', 'frozen', 'chilled'],
	'bleeding': ['bleeding', 'blood', 'bleed'],
	'itching': ['itch', 'itching', 'itchy', 'scratchy', 'itchiness']
    },
'nails': {
        'discoloration': ['discoloration', 'yellow', 'dark', 'black', 'pale'],
        'pain': ['pain', 'pains', 'hurt', 'hurts', 'sore', 'sores', 'ache', 'aches', 'aching','throbbing',],
        'infection': ['infection', 'pus', 'swelling', 'redness', 'fungus'],
        'brittle': ['brittle', 'crack', 'split', 'break'],
        'growth': ['not growing', 'slow growth', 'deformed', 'misshaped']
    },
'bone': {
    'pain': ['pain', 'pains', 'ache', 'aches', 'aching', 'soreness', 'tender', 'tenderness', 'throbbing', 'sharp', 'dull'],
    'fracture': ['fracture', 'broken', 'break', 'crack', 'snap', 'shattered', 'hairline'],
    'swelling': ['swelling', 'swollen', 'puffy', 'enlarged', 'inflamed'],
    'weakness': ['weakness', 'weak', 'brittle', 'fragile', 'soft', 'thin', 'osteopenia', 'osteoporosis'],
    'injury': ['injury', 'trauma', 'impact', 'blow', 'contusion', 'bruise', 'damage']
},

'joint': {
        'pain': ['pain', 'pains', 'hurt', 'hurts', 'sore', 'sores', 'ache', 'aches', 'aching','throbbing',],
        'swelling': ['swelling', 'swollen', 'swells', 'swell','bump', 'puffy', 'inflamed', 'bulge'],
        'stiffness': ['stiff', 'rigid', 'locked', 'tight'],
        'weakness': ['weak','weakness', 'unstable', 'giving way', "can’t move"],
        'injury': ['injury', 'sprain', 'dislocation', 'fracture', 'strain']
    },
'skin': {
        'rash': [
            'rash', 'red spots', 'bumps', 'patches', 'eruption', 
            'blotchy', 'hives', 'welts', 'raised spots'
        ],
        'itching': [
            'itch', 'itching', 'scratching', 'irritation', 
            'pruritus', 'crawling sensation','itches'
        ],
        'dryness': [
            'dry', 'flaky', 'scaly', 'rough', 'peeling', 
            'cracked', 'tight skin', 'ashy', 'parched','dryness'
        ],
        'discoloration': [
            'dark spots', 'light patches', 'discoloration', 
            'pigmentation', 'blotch', 'uneven skin tone', 
            'white spots', 'hyperpigmentation', 'hypopigmentation',
            'freckles', 'melasma'
        ],
        'swelling': [
            'swollen', 'lump', 'bump', 'puffy', 'inflammation', 'swelling', 'swollen', 'swells', 'swell','bump', 'puffy', 'inflamed',
            'raised area', 'knot', 'engorged', 'bulge'
        ],
        'acne': [
            'pimples', 'acne', 'zits', 'whiteheads', 'blackheads', 
            'breakouts', 'spots', 'pustules', 'cysts', 'nodules'],
        'burn': ['burn', 'sunburn', 'scald', 'blister','burns','burning'],
        'infection': ['infection', 'pus', 'bacterial', 'fungal', 'sores'],
	'bleeding': ['bleeding', 'blood', 'bleed', 'bleeds']
    },


'muscle': {
        'pain': ['pain', 'pains', 'hurt', 'hurts', 'sore', 'sores', 'ache', 'aches', 'aching','throbbing','stiff','stiffness'],
        'weakness': ['weakness', 'weak',  'fatigued', 'loss of strength', 'unable to lift'],
        'spasm': ['spasm', 'spasms', 'tightness', 'twitching','tensed'],
        'injury': ['injury', 'strain', 'pull', 'tear'],
        'swelling': ['swelling', 'swollen', 'swells', 'swell','bump', 'puffy', 'inflamed', 'bulge'],
	'cramps': ['cramp', 'cramps', 'cramping', 'contracting', 'twitch'],
	'itching': ['itch', 'itching', 'itchy', 'itchiness', 'scratchy']
    },
 
'heart': {
        'pain': ['pain', 'pains', 'paining', 'hurt', 'hurts', 'sore', 'sores', 'ache', 'aches', 'aching','throbbing','pressure', 'squeezing','stabbing','cramping', 'stiff', 'tightness',],
        'weakness': ['weakness', 'weak',  'fatigued', 'tired', 'low stamina', 'easily exhausted', 'shortness of breath with effort'],
         'burn': ['burn', 'burning', 'burns', 'burnt'],
        'palpitation': ['flutter', 'palpitations', 'racing', 'fast heartbeat', 'skipped beat', 'pounding','faster', 'fast']
 },

'urinary': {
        'pain': ['pain', 'pains', 'hurt', 'hurts', 'sore', 'sores', 'ache', 'aches', 'aching','throbbing','pressure','cramping', 'stiff', 'tightness'],
        'frequency': ['frequent', 'often', 'urge', 'need to go', 'multiple times'],
        'blood': ['blood', 'bloody', 'red urine', 'hematuria'],
        'difficulty': ['difficulty', 'straining', 'slow stream', 'trouble passing']
    },
'toes': {
        'pain': ['pain', 'pains', 'hurt', 'hurts', 'sore', 'sores', 'ache', 'aches', 'aching','throbbing','pressure', 'squeezing','stabbing','cramping', 'stiff', 'tightness',],
        'swelling': ['swollen', 'puffy', 'inflamed', 'red', 'tender'],
        'injury': ['injury', 'stubbed', 'fracture', 'broken', 'hurt', 'crush','injures','injured']
    },
'nose': {
        'injury': ['injury', 'hit', 'fracture', 'bump', 'hurt','broken','broke'],
        'burning': ['burning', 'stinging', 'irritation', 'hot sensation','burns'],
        'sniffing': ['sniffing', 'sniff', 'smelling', 'inhale', 'breathing in'],
        'pain': ['pain', 'pains', 'hurt', 'hurts', 'sore', 'sores', 'ache', 'aches', 'aching','throbbing','pressure', 'squeezing','stabbing','cramping', 'stiff', 'tightness',],
        'congestion'  : ['congestion', 'blocked', 'clogged', 'stuffy', 'stopped up'],
        'infection': ['infection', 'sinus', 'cold', 'flu', 'sinusitis'],
        'bleed' : ['bleed', 'bleeding', 'nosebleed', 'epistaxis', 'blood','bled','bleeds'],
	'freeze': ['freeze', 'freezing', 'chilled', 'freezed', 'frozen'],
	'itching': ['itch', 'itching', 'itchy', 'itchiness', 'scratchy']
    },
'thigh': {
        'pain': ['pain', 'pains', 'hurt', 'hurts', 'sore', 'sores', 'ache', 'aches', 'aching','throbbing','pressure', 'squeezing','stabbing','cramping', 'stiff', 'tightness'],
        'weakness': ['weakness', "can’t lift", 'weak','fatigue', 'tired', 'no strength', 'drained'],
        'spasm': ['spasm', 'twitch', 'twitching', 'cramp', 'tightness', 'spasms'],
        'injury': ['injury', 'pulled', 'strain', 'torn','injured','injure'],
        'swelling': ['swelling', 'swollen', 'swells', 'swell','bump', 'puffy', 'inflamed', 'bulge'],
	'numbness': ['numb', 'numbness', 'tingling', 'loss of sensation'],
	'itching': ['itch', 'itching', 'itchy', 'scratchy', 'itchiness']
    },
'forehead': {
        'pain': ['pain', 'pains', 'hurt', 'hurts', 'sore', 'sores', 'ache', 'aches', 'aching','throbbing','pressure', 'squeezing','stabbing','cramping', 'stiff', 'tightness',],
        'swelling': ['swelling', 'swollen', 'swells', 'swell','bump', 'puffy', 'inflamed', 'bulge'],
        'injury': ['forehead injury', 'hit forehead', 'forehead bruise'],
        'tingling': ['forehead tingling', 'numb forehead', 'tingly sensation forehead']
    },
'tongue': {
        'pain': ['pain', 'pains', 'hurt', 'hurts', 'sore', 'sores', 'ache', 'aches', 'aching','throbbing','pressure', 'squeezing','stabbing','cramping', 'stiff', 'tightness',],
        'swelling': ['swelling', 'swollen', 'swells', 'swell','bump', 'puffy', 'inflamed', 'bulge'],
        'burning': ['burning ', 'feels hot', 'scalded', 'burns','burn'],
        'ulcers': ['ulcer', 'sore spot', 'ulcers']
    },
'mouth': {
        'pain': ['pain', 'pains', 'paining', 'hurt', 'hurts', 'sore', 'sores', 'ache', 'aches', 'aching','throbbing','pressure', 'squeezing','stabbing','cramping', 'stiff', 'tightness',],
        'ulcer': ['ulcer', 'wound', 'canker', 'blister', 'lesion','ulcers'],
        'dryness': ['dry', 'dryness', 'parched', 'no saliva'],
        'swelling': ['swelling', 'swollen', 'swells', 'swell','bump', 'puffy', 'inflamed', 'bulge'],
        'bleeding': ['bleed', 'bleeding', 'blood in mouth'],
        'bad breath': ['bad breath', 'halitosis', 'foul smell'],
        'numbness': ['numb', 'tingling', 'pins', 'needles','numbness'],
	'itching': ['itch', 'itching', 'itchy', 'itchiness', 'scratchy']
    },
'jaw':{
        'pain': ['pain', 'pains', 'hurt', 'hurts', 'sore', 'sores', 'ache', 'aches', 'aching','throbbing','pressure', 'squeezing','stabbing','cramping', 'stiff', 'tightness',],
        'swelling': ['swelling', 'swollen', 'swells', 'swell','bump', 'puffy', 'inflamed', 'bulge'],
        'injury': ['injury', 'hit', 'bruise'],
    },
'period' : {
      'pain':     ['paining','pains','hurts','hurting','pain','hurt','sore','sores','ache','aches','cramping','cramps','throbbing'],
      'delayed':   ['delayed','delay','delays','delaying','absent','missed','misses','miss'],
      'bleeding': ['bleeds','bleeding','bled','blood','bleed'],
      'default':  ['issue','issues']   # no “default” words here; we’ll ask to confirm
},
'hip': {
    'pain': ['pain', 'ache', 'aches', 'aching', 'soreness', 'throbbing', 'sharp', 'burning', 'dull', 'stabbing'],
    'stiffness': ['stiffness', 'stiff', 'rigid', 'tight', 'limited motion', 'can’t bend', 'hard to move'],
    'swelling': ['swelling', 'swollen', 'puffy', 'inflamed', 'enlarged'],
    'weakness': ['weakness', 'weak', 'unstable', 'giving way', 'can’t bear weight', 'wobbly', 'tired'],
    'injury': ['injury', 'fracture', 'dislocation', 'sprain', 'strain', 'bruise', 'fall', 'trauma'],
    'itching': ['itch', 'itching', 'itchy', 'itchiness', 'scratchy']
},
 'waist': {
        'pain': ['pain', 'pains', 'paining', 'ache', 'aching', 'throbbing', 'sore', 'discomfort', 'soreness'],
        'stiffness': ['stiffness', 'stiff', 'tight', 'limited movement', 'rigid', 'hard to twist', 'cannot bend'],
        'numbness': ['numbness', 'numb', 'tingling', 'loss of sensation'],
        'swelling': ['swollen', 'bump', 'swelling', 'puffy', 'enlarged', 'inflamed', 'inflammation'],
        'injury': ['injury', 'pulled', 'strained', 'hurt', 'broken', 'strain', 'sprain', 'trauma', 'broke', 'fall', 'twisted'],
        'weakness': ['weakness', 'weak', 'unstable', 'tired', 'fatigued', 'can’t support', 'giving way'],
	'itching': ['itchy', 'itching', 'itchiness', 'scratchy']
    },

'pelvic': {
        'pain': ['pain', 'ache', 'aching', 'sharp', 'cramping', 'burning', 'stabbing', 'pressure', 'discomfort'],
        'stiffness': ['stiffness', 'stiff', 'tight', 'rigid', 'restricted', 'hard to move'],
        'swelling': ['swelling', 'swollen', 'puffy', 'inflamed', 'bloating'],
        'weakness': ['weakness', 'weak', 'unstable', 'tired', 'fatigued', 'can’t support', 'giving way'],
        'injury': ['injury', 'fall', 'fracture', 'trauma', 'strain', 'sprain'],
	'numbness': ['numb', 'numbness', 'tingling', 'loss of sensation'],
	'itching': ['itchy', 'itching', 'itchiness', 'scratchy']
    },
'elbow': {
        'pain': ['pain', 'ache', 'aching', 'sharp', 'burning', 'stabbing', 'soreness', 'discomfort', 'throbbing'],
        'stiffness': ['stiffness', 'stiff', 'tight', 'rigid', 'can’t bend', 'limited motion'],
        'swelling': ['swelling', 'swollen', 'puffy', 'inflamed', 'enlarged'],
        'weakness': ['weak', 'unstable', 'fatigued', 'can’t lift', 'loss of strength'],
        'injury': ['injury', 'strain', 'sprain', 'bruise', 'fracture', 'fall', 'hit', 'trauma']
    },
 'calf': {
        'pain': ['pain', 'ache', 'aching', 'soreness', 'cramping', 'sharp', 'burning', 'throbbing'],
        'spasm': ['spasm', 'cramp', 'tightness', 'twitching'],
        'swelling': ['swelling', 'swollen', 'puffy', 'inflamed', 'enlarged'],
        'weakness': ['weakness', 'weak', 'fatigued', 'loss of strength', 'unable to stand', 'unstable'],
        'injury': ['injury', 'strain', 'pull', 'tear', 'bruise', 'broke', 'broken', 'fall']
    },
'face': {
        'pain': ['pain', 'ache', 'throbbing', 'pains', 'paining'],
        'numbness': ['numbness', 'numb', 'tingling', 'loss of sensation', 'no feeling'],
        'swelling': ['swelling', 'swollen', 'swells', 'swell', 'puffy', 'inflammation', 'bump'],
        'drooping': ['drooping', 'droop', 'sagging', 'paralysis', 'uneven smile'],
        'injury': ['bruise', 'cut', 'impact', 'injury', 'trauma'],
	'itching': ['itch', 'itching', 'itchy', 'itchiness', 'scratchy']
    },
'ankle': {
        'pain': ['pain', 'ache', 'hurting', 'paining', 'pains', 'throbbing'],
        'swelling': ['swollen', 'swelling', 'puffy', 'enlarged'],
        'stiffness': ['stiffness', 'stiff', 'immobile', 'hard to move'],
        'injury': ['injury', 'sprain', 'twist', 'hurt', 'fracture', 'break'],
        'weakness': ['weakness', 'weak', 'unstable', 'buckling', 'giving way']
    },
'body': {
        'pain': ['pain', 'pains', 'paining', 'ache', 'whole body pain', 'all over pain', 'ache everywhere','aching'],
        'fatigue': ['tired', 'fatigue', 'exhausted', 'lethargic'],
        'weakness': ['weakness', 'weak', 'low energy', 'sluggish', 'no strength'],
        'stiffness': ['stiffness', 'stiff', 'tight', 'rigid', 'hard to move'],
	'itching': ['itching', 'itchy', 'scratching', 'irritation', 'rash'],
        'swelling': ['swelling', 'puffiness', 'inflammation']
    },
'hair': {
        'hair loss': ['hair fall', 'hair loss', 'balding', 'shedding', 'thinning'],
        'dandruff': ['dandruff', 'flaky scalp', 'scalp flakes', 'dry scalp'],
        'itching': ['itchy scalp', 'itching', 'scalp irritation'],
        'greying': ['greying', 'white hair', 'grey hair', 'premature greying'],
        'dryness': ['dryness', 'dry', 'rough hair', 'brittle hair']
    },
 'finger': {
        'pain': ['pain', 'pains', 'paining', 'hurts', 'ache', 'throbbing', 'sore'],
        'numbness': ['numbness', 'numb', 'tingling', 'no sensation', 'loss of feeling'],
        'swelling': ['swelling', 'swollen', 'puffy', 'inflammation', 'bump'],
        'stiffness': ['stiffness', 'stiff', 'hard to move', 'limited motion'],
        'injury': ['injury', 'injured', 'fracture', 'jammed', 'cut', 'bruise'],
	'freeze': ['freeze', 'freezing', 'frozen', 'chilled'],
	'itching': ['itch', 'itching', 'itchy', 'itchiness', 'scratchy']
    },
'thumb': {
        'pain': ['pain', 'paining', 'pains', 'hurts', 'ache', 'throbbing', 'sore'],
        'swelling': ['swelling','swollen', 'puffy', 'bump'],
        'stiffness': ['stiffness', 'stiff', 'hard to move', 'locked thumb'],
        'numbness': ['numbness', 'numb', 'tingling', 'no sensation'],
        'injury': ['injury', 'injured', 'sprain', 'dislocated', 'jammed', 'fracture']
    },
'palm': {
        'pain': ['pain', 'paining', 'pains', 'hurts', 'sore', 'ache'],
        'numbness': ['numbness', 'numb', 'tingling', 'burning', 'no sensation', 'pins and needles'],
        'swelling': ['swelling', 'swollen', 'puffy', 'bump', 'inflamed'],
        'stiffness': ['stiffness', 'stiff', 'hard to bend', 'tightness'],
        'injury': ['injury', 'injured', 'bruise', 'cut', 'burn', 'blister']
    },
'toe': {
        'pain': ['pain', 'pains', 'paining', 'hurts', 'ache', 'throbbing', 'sore'],
        'numbness': ['numbness', 'numb', 'tingling', 'no sensation', 'loss of feeling'],
        'swelling': ['swelling', 'swollen', 'puffy', 'inflammation', 'bump'],
        'stiffness': ['stiffness', 'stiff', 'hard to move', 'limited motion'],
        'injury': ['injury', 'injured', 'fracture', 'stubbed', 'cut', 'bruise'],
        'freeze': ['freeze', 'freezing', 'frozen', 'chilled']
    },
'heel': {
        'pain': ['pain', 'ache', 'hurting', 'sharp pain', 'burning', 'discomfort'],
        'swelling': ['swelling', 'swollen', 'puffy', 'inflamed'],
        'stiffness': ['stiff', 'stiffness', 'rigid', 'tight'],
        'injury': ['injury', 'fracture', 'bruise', 'hurt', 'crack', 'damage'],
        'numbness': ['numbness', 'numb', 'tingling', 'no sensation', 'pins and needles']
    },
'lip': {
    'pain': ['pain', 'ache', 'hurting', 'sore', 'burning'],
    'swelling': ['swelling', 'swollen', 'puffy', 'inflamed'],
    'dryness': ['dry', 'dryness', 'chapped', 'cracked', 'peeling'],
    'numbness': ['numb', 'numbness', 'tingling', 'no sensation'],
    'ulcers': ['ulcer', 'ulcers', 'blister', 'sores']
},
'cheek': {
    'pain': ['pain', 'ache', 'hurting', 'sore', 'tender'],
    'swelling': ['swelling', 'swollen', 'puffy', 'inflamed', 'enlarged'],
    'numbness': ['numb', 'numbness', 'tingling', 'no sensation', 'pins and needles'],
    'redness': ['red', 'redness', 'flushed', 'discoloration'],
    'injury': ['injury', 'hit', 'bruised', 'fracture', 'wound', 'cut']
},
'chin' :{
    'pain': ['pain', 'ache', 'hurting', 'sore', 'tender'],
    'swelling': ['swelling', 'swollen', 'puffy', 'inflamed', 'enlarged'],
    'numbness': ['numb', 'numbness', 'tingling', 'no sensation', 'pins and needles'],
    'injury': ['injury', 'hit', 'bruise', 'fracture', 'wound', 'cut'],
    'lump': ['lump', 'bump', 'mass', 'growth', 'nodule']
},
'soles' :{
    'pain': ['pain', 'ache', 'hurting', 'sore', 'burning', 'sharp pain'],
    'swelling': ['swelling', 'swollen', 'puffy', 'inflamed'],
    'numbness': ['numb', 'numbness', 'tingling', 'no sensation', 'pins and needles'],
    'cracks': ['crack', 'cracks', 'fissures', 'split skin', 'dry cracks'],
    'itching': ['itching', 'itchy', 'irritation', 'scratchy']
},

      'child' : {
      'pain':     ['paining','pains','hurts','hurting'],
      'bleeding': ['bleeds','bleeding','bled','blood'],
      'default':  ['issue']   # no “default” words here; we’ll ask to confirm
},

    # add ear / skin / etc…
}

body_part_followup_questions = {
   
    'tooth': {
    'injury': [
        {
            'hi': "क्या चोट लगने के बाद दाँत में दर्द है?",
            'en': "Is there pain in the tooth after the injury?",
            'category': 'tooth_injury_pain'
        },
        {
            'hi': "चोट कैसे लगी थी?",
            'en': "How did the injury happen?",
            'category': 'tooth_injury_cause'
        },
        {
            'hi': "क्या चोट लगने के बाद दाँत हिलने लगा है?",
            'en': "Is the tooth loose after the injury?",
            'category': 'tooth_injury_looseness'
        }
    ],
    'sensitivity': [
        {
            'hi': "क्या दाँत या मसूड़े छूने पर संवेदनशील लग रहे हैं?",
            'en': "Are your teeth or gums feeling sensitive to touch?",
            'category': 'tooth_sensitivity'
        },
        {
            'hi': "क्या गर्म या ठंडा खाने पर दर्द होता है?",
            'en': "Do you feel pain when eating or drinking something hot or cold?",
            'category': 'tooth_sensitivity_temp'
        },
        {
            'hi': "क्या मीठा खाने पर भी संवेदनशीलता होती है?",
            'en': "Do you feel sensitivity when eating sweets?",
            'category': 'tooth_sensitivity_sweets'
        }
    ],
    'pain':[
        
            {
      "hi": "क्या आप दांत के दर्द (तीव्र, धड़कते, लगातार या रुक-रुक कर) का वर्णन कर सकते हैं?",
      "en": "Can you describe the tooth pain (sharp, throbbing, constant, or intermittent)?",
      "category": "tooth pain",
      
    },
    {
      "hi": "क्या यह दर्द गर्म, ठंडा, या मीठे खाद्य या पेय पदार्थों से उत्तेजित होता है?",
      "en": "Is the pain triggered by hot, cold, or sweet foods or drinks?",
      "category": "tooth pain",
 
    },
    {
      "hi": "क्या आपने हाल ही में दंत चिकित्सा कार्य या दांत में किसी प्रकार का आघात अनुभव किया है?",
      "en": "Have you had any recent dental work or trauma to the tooth?",
      "category": "tooth pain",

    },
    {
      "hi": "क्या आपको चबाने या काटने में कोई कठिनाई हो रही है?",
      "en": "Are you having difficulty chewing or biting down?",
      "category": "tooth pain",

    },
    {
      "hi": "क्या आपको कीड़े, मसूड़ों की बीमारी, या अन्य दंत समस्याओं का इतिहास है?",
      "en": "Have you had a history of cavities, gum disease, or other dental issues?",
      "category": "tooth pain",

    }
    ],
    'broken': [
          {
    "hi": "क्या आपके दांत में दरार, टूट-फूट, या चिप लगी हुई है?",
    "en": "Do you have a crack, fracture, or chip in your tooth?",
    "category": "broken tooth",

  },
  {
    "hi": "क्या आप चबाते समय दांत में दर्द या संवेदनशीलता महसूस कर रहे हैं?",
    "en": "Do you feel pain or sensitivity in the tooth while chewing?",
    "category": "broken tooth",

  },
  {
    "hi": "क्या आपका टूटा हुआ दांत खाने, पीने या बोलने में परेशानी पैदा कर रहा है?",
    "en": "Is the broken tooth causing difficulty while eating, drinking, or speaking?",
    "category": "broken tooth",

  },
  {
    "hi": "क्या आपने हाल ही में किसी दुर्घटना, गिरावट या कठोर चीज काटने के बाद दांत टूटने का अनुभव किया है?",
    "en": "Did the tooth break after an accident, fall, or biting something hard?",
    "category": "broken tooth",
  },
  {
    "hi": "क्या आपके पास पहले से दांत क्षय (कीड़ा लगना) या कमजोर दांतों का इतिहास है?",
    "en": "Do you have a history of tooth decay or weakened teeth?",
    "category": "broken tooth",

  },
    ],

    'decay':[ 
      {
        "hi": "क्या आपके किसी दांत में काले धब्बे, गड्ढे या छेद दिखाई दे रहे हैं?",
        "en": "Do you see black spots, pits, or holes in any of your teeth?",
        "category": "tooth decay",

      },
      {
        "hi": "क्या आपको मीठे, गर्म या ठंडे खाद्य पदार्थों से दांत में संवेदनशीलता या दर्द होता है?",
        "en": "Do you feel sensitivity or pain in your tooth when eating sweet, hot, or cold foods?",
        "category": "tooth decay",

      },
      {
        "hi": "क्या आपके मुंह से दुर्गंध आती है या कोई खराब स्वाद बना रहता है?",
        "en": "Do you experience bad breath or a persistent unpleasant taste in your mouth?",
        "category": "tooth decay",

      },
      {
        "hi": "क्या आपके मसूड़े सूजे हुए हैं या उनमें से खून आता है?",
        "en": "Are your gums swollen or do they bleed?",
        "category": "tooth decay",

      },
      {
        "hi": "क्या आप नियमित रूप से मीठे खाद्य पदार्थ खाते हैं या दिन में कई बार स्नैक्स लेते हैं?",
        "en": "Do you frequently eat sugary foods or snack multiple times a day?",
        "category": "tooth decay",

      },
    ],
  'tingling': [
            {
                'hi': "क्या आपके दाँतों में झुनझुनाहट के साथ दर्द भी होता है?",
                'en': "Do you experience pain along with tingling in your teeth?",
                'category': 'teeth_tingling_pain'
            },
            {
                'hi': "क्या दाँतों में झुनझुनाहट ठंडा या गर्म खाने पर बढ़ जाती है?",
                'en': "Does the tingling in your teeth worsen with hot or cold foods?",
                'category': 'teeth_tingling_sensitivity'
            },
        ],
    'default': [
        {
            'hi': "क्या आप अपने दाँत की समस्या के बारे में अधिक बता सकते हैं?",
            'en': "Can you describe more about your tooth issue?",
            'category': 'tooth_detail'
        },
    ]
},
	 'leg': {
        'injury': [
            {
    'hi': "कौन सी टांग या टांगे घायल हैं?",
    'en': "Which leg or legs are injured?",
    'category': 'leg_injury_location'
      },
        {
    "hi": "क्या चोट के बाद प्रभावित क्षेत्र में सूजन, रक्तस्राव या नीलेपन की समस्या हो रही है?",
    "en": "After the injury, are you experiencing swelling, bleeding, or bruising in the affected area?",
    "category": "general injury",
  },
        ],
        'pain': [
            {
                'hi': "क्या दर्द चलते समय बढ़ता है या आराम करते समय भी रहता है?",
                'en': "Does the pain increase while walking or is it constant?",
                'category': 'leg_pain_detail'
            },
            {
                "hi": "क्या कोई विशेष चोट या घटना थी जिसके कारण पैर में दर्द हुआ?",
                "en": "Was there any specific injury or event that triggered the leg pain?",
                "category": "leg pain",
                    },
              {
                "hi": "दर्द आपके पैर के किस हिस्से में महसूस हो रहा है? (जांघ, घुटना, बछड़ा, पंजा)",
                "en": "Where exactly in the leg do you feel the pain (thigh, knee, calf, foot)?",
                "category": "leg pain",
                    },
              {
                "hi": "क्या चलने, दौड़ने या खड़े होने से पैर का दर्द बढ़ जाता है?",
              "en": "Does the leg pain get worse with walking, running, or standing?",
                "category": "leg pain",
                    },
              {
                "hi": "क्या आपने पैरों में सूजन, लालिमा या गर्मी महसूस की है?",
                "en": "Have you noticed any swelling, redness, or warmth in the leg?",
                "category": "leg pain",
                    },
              {
                "hi": "क्या आपने पहले अपने पैरों में किसी चोट या समस्या का अनुभव किया है?",
              "en": "Have you had any previous injuries or problems with your legs?",
                "category": "leg pain",
                   },
              {
                "hi": "क्या आप पैर के दर्द का वर्णन कर सकते हैं? (तीव्र, सुस्त, ऐंठन, जलन, आदि)",
                "en": "Can you describe the leg pain? (Sharp, dull, cramping, burning, etc.)",
                "category": "leg pain",
                    },
              {
                "hi": "क्या पैर में दर्द लगातार होता रहता है, या आता-जाता रहता है?",
                "en": "Does the leg pain occur constantly, or does it come and go?",
                "category": "leg pain",
                    },
              {
                "hi": "क्या दर्द पैर के अन्य हिस्सों तक फैलता है (जैसे कि जांघ से पंजे तक)?",
                "en": "Does the pain radiate to other parts of the leg (e.g., from the thigh to the foot)?",
                "category": "leg pain",
                    },
              {
                "hi": "क्या आपको पैरों में कमजोरी, सुन्नता या झुनझुनी महसूस होती है?",
                "en": "Do you feel weakness, numbness, or tingling in the leg?",
                "category": "leg pain",
                    },

        ],
        'swelling': [
            {
                'hi': "क्या सूजन के साथ लालिमा या गर्माहट भी महसूस हो रही है?",
                'en': "Is there any redness or warmth along with the swelling?",
                'category': 'leg_swelling_symptoms'
            }
        ],
	'itching': [
            {
                'hi': "क्या पैरों में खुजली किसी खास समय जैसे रात में ज्यादा होती है?",
                'en': "Does the itching in your legs get worse at certain times like at night?",
                'category': 'leg_itching_timing'
            }
        ],
        'weakness': [
    {
        'hi': "क्या आपको लंबे समय तक खड़े रहने पर पैरों में थकान या कमजोरी महसूस होती है?",
        'en': "Do your legs feel tired or weak after standing for a long time?",
        'category': 'leg_weakness_fatigue_standing'
    },

    {
        'hi': "क्या सीढ़ियाँ चढ़ते समय पैरों में कमजोरी महसूस होती है?",
        'en': "Do your legs feel weak when climbing stairs?",
        'category': 'leg_weakness_stairs'
    },

],
       'freeze': [
            {
                'hi': "क्या ठंड में आपकी टाँगों में ठंडक या झुनझुनी होती है?",
                'en': "Do you feel coldness or tingling in your legs during cold weather?",
                'category': 'leg_freezing_cold_sensitivity'
            }
        ],
	'spasm': [
            {
                'hi': "क्या आपके पैरों में ऐंठन या मरोड़ रात में सोते समय होती है?",
                'en': "Do you experience leg spasms or cramps at night while sleeping?",
                'category': 'leg_spasm_timing'
            }
        ],
        'default': [
            {
                'hi': "कृपया अपनी टांग की समस्या के बारे में और जानकारी दें।",
                'en': "Please describe your leg issue in more detail.",
                'category': 'leg_detail'
            }
        ]
},
'eye': {
    'itching': [
        {
            'hi': "क्या आपकी आँखों में खुजली लगातार हो रही है या कभी-कभी?",
            'en': "Is the itching in your eyes constant or occasional?",
            'category': 'eye_itching_frequency'
        },
        {
            'hi': "क्या खुजली दोनों आँखों में हो रही है या सिर्फ एक में?",
            'en': "Is the itching in both eyes or just one?",
            'category': 'eye_itching_side'
        },
        {
            'hi': "क्या खुजली के साथ आँखों से पानी भी निकल रहा है?",
            'en': "Is there any watering from the eyes along with the itching?",
            'category': 'eye_itching_tearing'
        }
    ],
    'redness': [
        {
            'hi': "क्या आपकी आँखें लाल होने के साथ दर्द भी कर रही हैं?",
            'en': "Are your eyes also painful along with the redness?",
            'category': 'eye_redness_pain'
        },
        {
            'hi': "क्या लालपन पूरी आँख में है या किसी खास हिस्से में?",
            'en': "Is the redness in the entire eye or a specific part?",
            'category': 'eye_redness_area'
        },
        {
            'hi': "क्या आँखों में सूजन या जलन भी है?",
            'en': "Is there any swelling or burning sensation in your eyes?",
            'category': 'eye_redness_swelling'
        }
    ],
    'burn': [
        {
            'hi': "क्या आँखों में जलन के साथ रोशनी सहन नहीं होती?",
            'en': "Do your eyes feel sensitive to light along with the burning?",
            'category': 'eye_burn_light_sensitivity'
        },
        {
            'hi': "क्या आँखों में जलन किसी केमिकल या धूल के संपर्क के बाद शुरू हुई?",
            'en': "Did the burning start after contact with dust or chemicals?",
            'category': 'eye_burn_trigger'
        },
        {
            'hi': "क्या आप जलन के कारण आँखें बार-बार मसलते हैं?",
            'en': "Are you rubbing your eyes frequently because of the burning?",
            'category': 'eye_burn_rubbing'
        }
    ],

    'weakness': [
        {
        'hi': "क्या कम रोशनी में देखने में परेशानी होती है?",
        'en': "Do you have trouble seeing in low light conditions?",
        'category': 'eye_weakness_low_light'
        },
        {
        'hi': "क्या आपको धुंधला दिखता है जब आप दूर या पास की चीजें देखते हैं?",
        'en': "Do things appear blurry when you look at objects far away or up close?",
        'category': 'eye_weakness_blurry_vision'
        },
          {
              'hi': "क्या आपको लंबे समय तक पढ़ने या स्क्रीन देखने पर आँखों में थकान महसूस होती है?",
              'en': "Do your eyes feel tired after reading or using a screen for a long time?",
              'category': 'eye_weakness_fatigue_screen'
          },
          {
              'hi': "क्या आपको पहले चश्मा या लेंस का उपयोग करने की सलाह दी गई है?",
              'en': "Have you ever been advised to use glasses or contact lenses?",
              'category': 'eye_weakness_prescription'
          }
    ],
	
    'blurry_vision': [
        {
            'hi': "क्या धुंधली दृष्टि दूर की चीज़ें देखने में होती है या पास की?",
            'en': "Is your blurry vision affecting distance or near vision?",
            'category': 'eye_blurry_distance_near'
        },
        {
            'hi': "क्या धुंधली दृष्टि पूरे दिन रहती है या किसी विशेष समय पर होती है?",
            'en': "Is your blurry vision constant or does it occur at certain times?",
            'category': 'eye_blurry_timing'
        },
        {
            'hi': "क्या आँखों पर ज़ोर डालने पर धुंधली दृष्टि और बढ़ जाती है?",
            'en': "Does your blurry vision get worse when you strain your eyes?",
            'category': 'eye_blurry_eye_strain'
        }
    ],

    'discharge':[
    {
      "hi": "क्या आँखों में स्राव के कारण आपकी दृष्टि प्रभावित हो रही है?",
      "en": "Is the discharge in your eyes affecting your vision?",
      "category": "vision_impact_with_eye_discharge",   },
    {
      "hi": "क्या स्राव में रंग में कोई परिवर्तन आया है?",
      "en": "Has there been any change in the color of the discharge?",
      "category": "discharge_color_change", },
    ],

  'pain':[
          {
      "hi": "क्या दर्द एक आंख में है या दोनों आंखों में?",
      "en": "Is the pain in one eye or both eyes?",
      "category": "eye pain",
    },
    {
      "hi": "क्या आपको हाल ही में आंखों में चोट या आघात लगा है?",
      "en": "Have you had any recent eye injuries or trauma?",
      "category": "eye pain",

    },
    {
      "hi": "क्या आपको धुंआ, रसायन, या अन्य उत्तेजकों का संपर्क हुआ है?",
      "en": "Have you been exposed to smoke, chemicals, or other irritants?",
      "category": "eye pain",

    },
    {
      "hi": "क्या आपकी आंखें लाल हैं या उनमें सूजन है?",
      "en": "Are your eyes red or swollen?",
      "category": "eye pain",

    },
    {
      "hi": "क्या आपकी दृष्टि धुंधली हो गई है या आपको रोशनी से संवेदनशीलता महसूस होती है?",
      "en": "Has your vision become blurry or are you experiencing sensitivity to light?",
      "category": "eye pain",

    },

  ],
'swelling': [
            {
                'hi': "क्या सूजी हुई आंख में दर्द या गर्माहट महसूस हो रही है?",
                'en': "Is the swollen eye accompanied by pain or warmth?",
                'category': 'eye_swelling_signs'
            }
        ],
    'default': [
        {
            'hi': "कृपया अपनी आँखों की समस्या के बारे में और जानकारी दें।",
            'en': "Please describe your eye issue in more detail.",
            'category': 'eye_detail'
        },
        {
            'hi': "क्या आपकी समस्या दोनों आँखों को प्रभावित कर रही है?",
            'en': "Is the issue affecting both eyes?",
            'category': 'eye_side'
        },
        {
            'hi': "क्या आपको आँखें खोलने या बंद करने में परेशानी हो रही है?",
            'en': "Are you having trouble opening or closing your eyes?",
            'category': 'eye_open_close_difficulty'
        }
    ]
},

'hand': {
        'pain': [
            {
                'hi': "क्या हाथ में दर्द लगातार है या किसी गतिविधि के साथ बढ़ता है?",
                'en': "Is the pain in your hand constant or does it worsen with activity?",
                'category': 'hand_pain_detail'
            },
                {
      "hi": "क्या दर्द एक हाथ में है या दोनों हाथों में?",
      "en": "Is the pain in one hand or both hands?",
      "category": "hand pain",

    },
    {
      "hi": "क्या आपको हाल ही में हाथों में चोट या आघात लगा है?",
      "en": "Have you had any recent injuries or trauma to your hands?",
      "category": "hand pain",

    },
    {
      "hi": "क्या आपको हाथ में सूजन, लाली, या जकड़न का अनुभव हो रहा है?",
      "en": "Are you experiencing any swelling, redness, or stiffness in the hand?",
      "category": "hand pain",

    },
    {
      "hi": "क्या आपको अपनी उंगलियों या हाथों में सुन्नता या झनझनाहट का अनुभव हो रहा है?",
      "en": "Do you have any numbness or tingling in your fingers or hands?",
      "category": "hand pain",

    },
    {
      "hi": "क्या आप उन गतिविधियों में शामिल हैं जो आपके हाथों पर दबाव डालती हैं, जैसे टाइपिंग या उठाना?",
      "en": "Are you involved in activities that put strain on your hands, like typing or lifting?",
      "category": "hand pain",
    },
        ],
	'weakness': [
            {
                'hi': "क्या आप हाथों से चीजें पकड़ने या पकड़ बनाए रखने में परेशानी महसूस करते हैं?",
                'en': "Do you find it difficult to grip or hold objects with your hands?",
                'category': 'hand_weakness_grip'
            },
            {
                'hi': "क्या हाथों में कमजोरी के साथ कांपना या थकावट भी महसूस होती है?",
                'en': "Do your hands feel shaky or tired along with weakness?",
                'category': 'hand_weakness_tremor_fatigue'
            },
        ],
        'numbness': [
            {
                'hi': "क्या झुनझुनी या सुन्नपन उंगलियों तक सीमित है?",
                'en': "Is the numbness or tingling limited to the fingers?",
                'category': 'hand_numbness_area'
            }
        ],
        'swelling': [
            {
                'hi': "क्या सूजन के साथ हाथ गर्म या लाल दिख रहा है?",
                'en': "Is the hand warm or red along with the swelling?",
                'category': 'hand_swelling_symptoms'
            }
        ],
        'dryness':[
              {
    "hi": "क्या आपकी हथेलियाँ रूखी या खुरदरी महसूस होती हैं?",
    "en": "Do your palms feel dry or rough to the touch?",
    "category": "hand dryness",

  },
  {
    "hi": "क्या आपकी त्वचा पर सफेद पपड़ी या झुर्रियां दिखाई देती हैं?",
    "en": "Do you notice flaking or white patches on the skin?",
    "category": "hand dryness",

  },
  {
    "hi": "क्या हाथों की त्वचा में खुजली या जलन होती है?",
    "en": "Do you experience itching or irritation on the hands?",
    "category": "hand dryness",

  },
  {
    "hi": "क्या आप दिन में बार-बार साबुन या सैनिटाइज़र का उपयोग करते हैं?",
    "en": "Do you frequently use soap or hand sanitizer during the day?",
    "category": "hand dryness",


  },
  {
    "hi": "क्या आप ठंडी या शुष्क जलवायु में रहते हैं?",
    "en": "Do you live in a cold or dry climate?",
    "category": "hand dryness",

  },
  {
    "hi": "क्या आपके हाथों की त्वचा पर दरारें या खून आने जैसे लक्षण हैं?",
    "en": "Do you have cracks or bleeding on the skin of your hands?",
    "category": "hand dryness",

  },
  {
    "hi": "क्या आपको एग्ज़िमा या त्वचा से जुड़ी कोई पुरानी समस्या है?",
    "en": "Do you have eczema or any chronic skin condition?",
    "category": "hand dryness",

  },
        ],
        'injury': [
            {
    'hi': "कौन सा हाथ या दोनों हाथ घायल हैं?",
    'en': "Which hand or hands are injured?",
    'category': 'hand_injury_location'
           },
             {
    "hi": "क्या चोट के बाद प्रभावित क्षेत्र में सूजन, रक्तस्राव या नीलेपन की समस्या हो रही है?",
    "en": "After the injury, are you experiencing swelling, bleeding, or bruising in the affected area?",
    "category": "general injury",
  },

        ],
	'freeze': [
            {
                'hi': "क्या ठंड में आपके हाथ सुन्न या ठंडे हो जाते हैं?",
                'en': "Do your hands feel numb or cold in cold weather?",
                'category': 'hand_freezing_cold_sensitivity'
            }
        ],
    'itching': [
            {
                'hi': "क्या हाथों में खुजली के साथ फोड़े या छाले भी हैं?",
                'en': "Is the itching in your hands accompanied by boils or blisters?",
                'category': 'hand_itching_signs'
            }
        ],
        'default': [
            {
                'hi': "कृपया अपने हाथ की समस्या के बारे में और जानकारी दें।",
                'en': "Please describe your hand issue in more detail.",
                'category': 'hand_detail'
            }
        ]
    },

 'arm': {
     'pain': [
            {
                'hi': "क्या आपके हाथ में दर्द लगातार बना रहता है?",
                'en': "Is the pain in your arm persistent?",
                'category': 'arm_pain_detail'
            },
            {
               "hi": "क्या दर्द एक हाथ में है या दोनों हाथों में?",
               "en": "Is the pain in one arm or both arms?",
               "category": "arm pain",

            },
            {
            "hi": "क्या बांह का दर्द तेज़, सुस्त या धड़कता हुआ है?",
            "en": "Is the arm pain sharp, dull, or throbbing?",
            "category": "arm pain",

            },
            {
            "hi": "क्या आपको हाल ही में हाथ में कोई चोट, गिरने या आघात का सामना करना पड़ा है?",
            "en": "Have you had any recent injuries, falls, or trauma to your arm?",
            "category": "arm pain",

            },
            {
            "hi": "क्या आपको अपने हाथ या कंधे को हिलाने में कठिनाई हो रही है?",
            "en": "Do you have difficulty moving your arm or shoulder?",
            "category": "arm pain",

            },
            {
            "hi": "क्या आपको हाथ या हाथों में सुन्नता, झनझनाहट, या कमजोरी का अनुभव हो रहा है?",
            "en": "Are you experiencing any numbness, tingling, or weakness in the arm or hand?",
            "category": "arm pain",

            },
            ],
    'numbness': [
            {
                'hi': "क्या सुन्नपन पूरे हाथ में है या किसी खास हिस्से में?",
                'en': "Is the numbness in your entire arm or a specific part?",
                'category': 'arm_numbness_location'
            }
        ],
    'injury': [
            {
            'hi': "कौन सा बाजू या दोनों बाजू घायल हैं?",
            'en': "Which arm or arms are injured?",
            'category': 'arm_injury_location'
        },
        {
            "hi": "क्या चोट के बाद प्रभावित क्षेत्र में सूजन, रक्तस्राव या नीलेपन की समस्या हो रही है?",
            "en": "After the injury, are you experiencing swelling, bleeding, or bruising in the affected area?",
            "category": "general injury",
        },
            ],
     'weakness': [
            {
                'hi': "क्या हाथ में कमजोरी किसी विशेष क्रिया के बाद महसूस होती है?",
                'en': "Do you feel weakness in your arm after any specific activity?",
                'category': 'arm_weakness_context'
            }
        ],
	 'spasm': [
            {
                'hi': "क्या आपके हाथ में ऐंठन किसी काम के दौरान होती है?",
                'en': "Do you experience arm spasms during any specific activities?",
                'category': 'arm_spasm_activity'
            }
        ],
	 'itching': [
            {
                'hi': "क्या हाथ में खुजली किसी विशेष जगह पर सीमित है या पूरे हाथ में है?",
                'en': "Is the itching in your arm localized or spread across the whole arm?",
                'category': 'arm_itching_extent'
            }
        ],

        'swelling': [
            {
                'hi': "क्या हाथ की सूजन के साथ दर्द या लालपन भी है?",
                'en': "Is the swelling in your arm accompanied by pain or redness?",
                'category': 'arm_swelling_signs'
            }
        ],

        'default': [
            {
                'hi': "कृपया अपने हाथ की समस्या के बारे में अधिक जानकारी दें।",
                'en': "Please describe your arm issue in more detail.",
                'category': 'arm_detail'
            }
        ]
    },
  'head': {
        'injury': [
            {
        "hi": "क्या सिर में चोट के बाद दर्द लगातार बना रहता है, या हिलने-डुलने से यह बढ़ता है?",
        "en": "Is the head pain after the injury constant, or does it worsen with movement?",
        "category": "head_injury_pain_variation",
    },
    {
        "hi": "क्या आपने पहले भी सिर में चोट या बार-बार सिरदर्द की समस्या झेली है?",
        "en": "Have you had previous head injuries or frequent headaches?",
        "category": "head_injury_history",
        "symptom": "previous head injuries",
        "risk_factor": True
    },
        ],
        'pressure': [
            {
                'hi': "क्या सिर में भारीपन लगातार रहता है या कभी-कभी होता है?",
                'en': "Is the pressure in your head constant or does it come and go?",
                'category': 'head_pressure_pattern'
            }
        ],
	 'numbness': [
    {
        'hi': "क्या सिर में सुन्नपन के साथ बोलने या देखने में भी कोई समस्या हो रही है?",
        'en': "Are you experiencing any trouble speaking or seeing along with the numbness in your head?",
        'category': 'head_numbness_neurological_signs'
    }
        ],
 'itching': [
            {
                'hi': "क्या सिर में खुजली के साथ पपड़ी, लालिमा या बाल झड़ना भी हो रहा है?",
                'en': "Is the itching on your head accompanied by flaking, redness, or hair loss?",
                'category': 'head_itching_signs'
            }
        ],
	'pain': [
            {
                'hi': "क्या सिरदर्द अचानक शुरू हुआ या धीरे-धीरे बढ़ा?",
                'en': "Did the head pain start suddenly or develop gradually?",
                'category': 'head_pain_onset'
            }
        ],
        'default': [
            {
                'hi': "कृपया अपने सिर की समस्या के बारे में और जानकारी दें।",
                'en': "Please describe your head issue in more detail.",
                'category': 'head_detail'
            }
        ]
    },  
'back': {
        'pain': [
            {
                'hi': "क्या पीठ का दर्द चलते समय बढ़ता है या आराम करते समय भी होता है?",
                'en': "Does your back pain increase while moving or is it present even at rest?",
                'category': 'back_pain_detail'
            },

       {
            "hi": "क्या आपको लंबे समय तक चलने, खड़े रहने, या बैठने में परेशानी हो रही है?",
            "en": "Are you having difficulty walking, standing, or sitting for long periods?",
            "category": "mobility_impairment",
            "symptom": None,
            "risk_factor": False,
        },
        {
            "hi": "क्या आपके पिछवाड़े या रीढ़ में पहले कोई चोट, गिरना, या दुर्घटना हुई है?",
            "en": "Have you had previous injuries, falls, or accidents involving your back or spine?",
            "category": "history_of_injury",
            "symptom": "injury",
            "risk_factor": False,
        },
        {
            "hi": "क्या आपका पीठ दर्द निचले हिस्से में है या ऊपर?",
            "en": "Is your back pain in the lower or upper back?",
            "category": "pain_location",
            "symptom": None,
            "risk_factor": False,
        },
        ],
	'weakness': [
            {
                'hi': "क्या आपकी पीठ की कमजोरी के कारण लंबे समय तक खड़े रहना मुश्किल होता है?",
                'en': "Does weakness in your back make it difficult to stand for long periods?",
                'category': 'back_weakness_standing'
            },
            {
                'hi': "क्या पीठ की कमजोरी के कारण आपको झुकने या उठने में परेशानी होती है?",
                'en': "Does back weakness make it hard for you to bend or lift?",
                'category': 'back_weakness_bend_lift'
            },
        ],
	'spasm': [
	    {
	      "hi": "पीठ की ऐंठन कहाँ स्थित है (उदाहरण के लिए, निचली पीठ, ऊपरी पीठ, या गर्दन)?",
	      "en": "Where is the back spasm located (e.g., lower back, upper back, or neck)?",
	      "category": "back_spasms",
	      "symptom": "location of spasm",
	      "risk_factor": False,    },
	    {
	      "hi": "क्या पीठ की ऐंठन लगातार बनी रहती है, या वे आती-जाती रहती हैं?",
	      "en": "Are the back spasms constant, or do they come and go?",
	      "category": "back_spasms",
	      "symptom": "spasm pattern",
	      "risk_factor": False,    },
	    {
	      "hi": "पीठ की ऐंठन के दौरान दर्द कितना गंभीर होता है? क्या यह तेज़, सुस्त या ऐंठन वाला होता है?",
	      "en": "How severe is the pain during the back spasms? Is it sharp, dull, or cramping?",
	      "category": "back_spasms",
	      "symptom": "pain severity and type",
	      "risk_factor": False,    },
	    {
	      "hi": "क्या पीठ में ऐंठन कुछ गतिविधियों जैसे उठाने, झुकने या शारीरिक परिश्रम के बाद होती है?",
	      "en": "Do the back spasms occur after certain activities, such as lifting, bending, or physical exertion?",
	      "category": "back_spasms",
	      "symptom": "activity-related spasms",
	      "risk_factor": False,    },
	    {
	      "hi": "क्या आपको हाल ही में कोई चोट लगी है, गिर गया है, या खिंचाव आया है जिसके कारण पीठ में ऐंठन हुई हो?",
	      "en": "Have you had any recent injuries, falls, or strains that might have triggered the back spasms?",
	      "category": "back_spasms",
	      "symptom": "recent injury or strain",
	      "risk_factor": False,    },
	    {
	      "hi": "क्या आपको पीठ से संबंधित कोई पिछला इतिहास है, जैसे हर्नियेटेड डिस्क, गठिया, या डीजनरेटिव डिस्क रोग?",
	      "en": "Do you have a history of back problems, such as herniated discs, arthritis, or degenerative disc disease?",
	      "category": "back_spasms",
	      "symptom": "history of back problems",
	      "risk_factor": False,    },
	    {
	      "hi": "क्या आप वर्तमान में पीठ की ऐंठन के लिए कोई दवा ले रहे हैं या उपचार (जैसे, गर्मी, बर्फ, भौतिक चिकित्सा) का उपयोग कर रहे हैं?",
	      "en": "Are you currently taking any medications or using treatments (e.g., heat, ice, physical therapy) for the back spasms?",
	      "category": "back_spasms",
	      "symptom": "medications and treatments",
	      "risk_factor": False,    },
	  ],
        'stiffness': [
            {
                'hi': "क्या सुबह उठने पर पीठ में ज्यादा जकड़न महसूस होती है?",
                'en': "Do you feel more stiffness in your back after waking up?",
                'category': 'back_stiffness_morning'
            }
        ],
        'injury': [
           {
               'hi': "क्या आप आजकल अपनी पीठ मोड़ पा रहे हैं?",
               'en': "Are you able to bend your back nowadays?",
               'category': 'back_mobility_current'
           }
        ],
        'numbness': [
            {
                'hi': "क्या सुन्नपन पीठ से टांगों तक फैलता है?",
                'en': "Does the numbness in your back extend down to your legs?",
                'category': 'back_numbness_radiation'
            }
        ],
	'itching': [
            {
                'hi': "क्या पीठ की खुजली के साथ लाल चकत्ते या सूखापन भी है?",
                'en': "Is the itching on your back accompanied by rash or dryness?",
                'category': 'back_itching_rash'
            }
        ],
	'issue': [
            {
                'hi': "कृपया अपनी कलाई की समस्या के बारे में और जानकारी दें।",
                'en': "Please describe your back issue in more detail.",
                'category': 'back_detail'
            }
        ]
    },
'chest': {
      'pain': [
      {
                'hi': "क्या छाती में दर्द चलने या सीढ़ियाँ चढ़ने पर बढ़ता है?",
                'en': "Does the chest pain increase when walking or climbing stairs?",
                'category': 'chest_pain_exertion'
            },
      {
      "hi": "क्या छाती का दर्द आपके हाथ, गर्दन या कमर में फैल रहा है?",
      "en": "Is your chest pain radiating to your arms, neck, or back?",
      "category": "radiating_pain",
          },
    {
      "hi": "क्या आपका छाती में दर्द तेज है या स्थिर है?",
     "en": "Is your chest pain sharp or dull?",
      "category": "pain_intensity",
       },
    {
      "hi": "क्या छाती का दर्द अचानक शुरू हुआ था या धीरे-धीरे?",
      "en": "Did the chest pain start suddenly or gradually?",
      "category": "onset",
       },
    {
      "hi": "क्या छाती में दर्द के साथ सांस लेने में कठिनाई हो रही है?",
      "en": "Are you experiencing difficulty breathing along with chest pain?",
      "category": "breathing_difficulty",
      },
    {
      "hi": "क्या छाती का दर्द किसी विशेष गतिविधि के दौरान बढ़ता है?",
     "en": "Does your chest pain increase during any specific activity?",
      "category": "activity_related_pain",
    },
        ],
	'weakness': [
            {
                'hi': "क्या छाती में कमजोरी या भारीपन के कारण आपको सांस लेने में कठिनाई होती है?",
                'en': "Do you experience difficulty breathing due to weakness or heaviness in the chest?",
                'category': 'chest_weakness_breathing_difficulty'
            },
            {
                'hi': "क्या छाती की कमजोरी के कारण आपको सामान्य काम करने में भी थकावट महसूस होती है?",
                'en': "Does chest weakness cause you to feel fatigued even during routine activities?",
                'category': 'chest_weakness_fatigue'
            },
        ],
        'discomfort': [
            {
                'hi': "क्या छाती में असहजता के साथ मतली या पसीना भी आता है?",
                'en': "Do you experience nausea or sweating along with the discomfort?",
                'category': 'chest_discomfort_symptoms'
            }
        ],
        'breathing': [
            {
                'hi': "क्या आपको सांस लेने में कठिनाई हाल ही में शुरू हुई है?",
                'en': "Did the difficulty in breathing start recently?",
                'category': 'chest_breathing_onset'
            }
        ],
        'palpitations': [
            {
                'hi': "क्या दिल की धड़कन तेज होने के साथ चक्कर या बेहोशी महसूस हुई?",
                'en': "Have you felt dizzy or faint along with the rapid heartbeat?",
                'category': 'chest_palpitations_symptoms'
            }
        ],
	'itching': [
            {
                'hi': "क्या छाती में खुजली पसीने के कारण होती है?",
                'en': "Is the itching on your chest related to sweating?",
                'category': 'chest_itching_cause'
            }
        ],
        'default': [
            {
                'hi': "कृपया अपनी छाती की समस्या के बारे में और जानकारी दें।",
                'en': "Please describe your chest issue in more detail.",
                'category': 'chest_detail'
            }
        ]
    },
'wrist': {
        'pain': [
            {
    'hi': "क्या दोनों कलाइयों में दर्द है?",
    'en': "Is the pain in both wrists?",
    'category': 'wrist_pain_location'
            },
          {
      "hi": "क्या आपने हाल ही में कलाई को चोट पहुँचाई है? (गिरना, मुड़ना, सीधा असर)",
     "en": "Have you injured the wrist recently? (e.g., fall, twist, direct blow)",
      "category": "wrist pain",
    },
   {
      "hi": "क्या आपकी कलाई के आसपास सूजन या चोट है?",
      "en": "Is there swelling or bruising around the wrist?",
      "category": "wrist pain",
    },
    {
      "hi": "क्या आपके हाथ या अंगुलियों में सुन्नता या झनझनाहट महसूस हो रही है?",
      "en": "Do you have numbness or tingling in your hand or fingers?",
      "category": "wrist pain",
   },
    {
      "hi": "क्या कलाई में दर्द लगातार या रुक-रुक कर होता है?",
      "en": "Is the wrist pain constant or intermittent?",
      "category": "wrist pain",
   },
    {
      "hi": "क्या आप कलाई के दर्द का वर्णन कर सकते हैं? (तीव्र, सुस्त, दर्द, आदि)",
      "en": "Can you describe the wrist pain? (Sharp, dull, aching, etc.)",
      "category": "wrist pain",
   },
    {
      "hi": "कौन सी गतिविधियाँ कलाई के दर्द को बदतर बना देती हैं?",
      "en": "What activities make the wrist pain worse?",
      "category": "wrist pain",
    },
    {
      "hi": "क्या आराम करने से कलाई का दर्द ठीक हो जाता है या बिगड़ जाता है?",
      "en": "Does the wrist pain improve or worsen with rest?",
      "category": "wrist pain",
   },
        ],
	'weakness': [
            {
                'hi': "क्या कलाई की कमजोरी के कारण आप चीजें ठीक से पकड़ नहीं पाते?",
                'en': "Is it difficult to hold or grip things due to wrist weakness?",
                'category': 'wrist_weakness_grip'
            },
            {
                'hi': "क्या कलाई में कमजोरी के साथ कंपन या थकान भी महसूस होती है?",
                'en': "Do you feel tremors or fatigue in the wrist along with weakness?",
                'category': 'wrist_weakness_tremor_fatigue'
            },
        ],
        'swelling': [
            {
                'hi': "क्या सूजन के साथ कलाई में गर्माहट या लालिमा भी है?",
                'en': "Is there warmth or redness along with the wrist swelling?",
                'category': 'wrist_swelling_signs'
            }
        ],
        'stiffness': [
            {
                'hi': "क्या सुबह उठते समय कलाई में जकड़न होती है?",
                'en': "Do you feel wrist stiffness in the morning?",
                'category': 'wrist_stiffness_time'
            }
        ],
        'numbness': [
            {
                'hi': "क्या झुनझुनी या सुन्नपन उंगलियों तक भी पहुंचता है?",
                'en': "Does the numbness or tingling extend to your fingers?",
                'category': 'wrist_numbness_extent'
            }
        ],
        'injury': [
            {
                'hi': "कलाई में चोट कब और कैसे लगी थी?",
                'en': "How and when did you injure your wrist?",
                'category': 'wrist_injury_time'
            }
        ],
        'default': [
            {
                'hi': "कृपया अपनी कलाई की समस्या के बारे में और जानकारी दें।",
                'en': "Please describe your wrist issue in more detail.",
                'category': 'wrist_detail'
            }
        ]
    },
   'throat': {
        'pain': [
            {
                'hi': "क्या गले में दर्द लगातार बना रहता है या किसी विशेष समय में बढ़ता है?",
                'en': "Is the pain in your throat constant, or does it worsen at a particular time?",
                'category': 'throat_pain_pattern'
            },
            {
      "hi": "क्या आपको निगलने में कठिनाई या निगलते समय दर्द हो रहा है?",
      "en": "Are you experiencing any difficulty swallowing or pain when swallowing?",
      "category": "throat pain",
    },
    {
      "hi": "क्या आपने हाल ही में किसी ऐसे व्यक्ति से संपर्क किया है जिसे गले में दर्द या सर्दी हो?",
      "en": "Have you been exposed to anyone with a sore throat or cold recently?",
      "category": "throat pain",

    },
    {
      "hi": "क्या आप धूम्रपान करते हैं या आपको धुंआ या अन्य उत्तेजकों से संपर्क हुआ है?",
      "en": "Do you smoke or have you been exposed to smoke or other irritants?",
      "category": "throat pain",

    },
    {
      "hi": "क्या आपको बुखार, गले में खराश के साथ जुड़ा हुआ है?",
      "en": "Are you experiencing a fever along with your sore throat?",
      "category": "throat pain",

    },
    {
      "hi": "क्या आपके गले में सूजन या लालिमा है?",
      "en": "Do you have any swelling or redness in your throat?",
      "category": "throat pain",

    },
        ],
        'swelling': [
            {
                'hi': "क्या गले में सूजन के साथ निगलने में भी कठिनाई हो रही है?",
                'en': "Is the swelling in your throat making it difficult to swallow?",
                'category': 'throat_swelling_swallowing'
            }
        ],
        'difficulty_swallowing': [
            {
                'hi': "क्या आपको खाने-पीने में कठिनाई महसूस हो रही है?",
                'en': "Are you having difficulty with eating or drinking?",
                'category': 'throat_swallowing_difficulty'
            }
        ],
        'hoarseness': [
            {
                'hi': "क्या आपकी आवाज में खराश हाल ही में आई है?",
                'en': "Did the hoarseness in your voice start recently?",
                'category': 'throat_hoarseness_onset'
            }
        ],
        'infection': [
            {
                'hi': "क्या आपको बुखार, सर्दी या फ्लू के अन्य लक्षण भी हैं?",
                'en': "Do you also have symptoms like fever, cold, or flu?",
                'category': 'throat_infection_symptoms'
            }
        ],
	'itching': [
            {
                'hi': "क्या गले में खुजली के साथ खांसी या खराश भी है?",
                'en': "Is the throat itching accompanied by cough or soreness?",
                'category': 'throat_itching_symptoms'
            }
        ],
        'default': [
            {
                'hi': "कृपया अपने गले की समस्या के बारे में और जानकारी दें।",
                'en': "Please describe your throat issue in more detail.",
                'category': 'throat_detail'
            }
        ]
    },
   
'stomach': {
    'pain': [
        {
            'hi': "क्या पेट में दर्द खाने के बाद बढ़ता है?",
            'en': "Does the stomach pain increase after eating?",
            'category': 'stomach_pain_after_eating'
        },
        {
            'hi': "क्या दर्द पेट के ऊपरी हिस्से में है या निचले हिस्से में?",
            'en': "Is the pain in the upper part of your abdomen or the lower part?",
            'category': 'stomach_pain_location'
        },
        {
            'hi': "क्या पेट दर्द के साथ ऐंठन या चुभन जैसा महसूस होता है?",
            'en': "Does the stomach pain feel like cramping or stabbing?",
            'category': 'stomach_pain_nature'
        },

        {
      "hi": "क्या आपको अन्य कोई लक्षण जैसे कि उल्टी, दस्त, बुखार आदि महसूस हो रहे हैं?",
     "en": "Do you have any other symptoms, such as nausea, vomiting, diarrhea, or fever?", 
      "category": "digestive symptoms",
   },

{
      "hi": "क्या आप पेट दर्द का वर्णन कर सकते हैं? (तीव्र, सुस्त, ऐंठन, जलन, आदि)",
      "en": "Can you describe the stomach pain? (Sharp, dull, cramping, burning, etc.)",
      "category": "stomach ache",
    },   
{
  "hi": "पेट दर्द वास्तव में कहाँ स्थित है? क्या यह ऊपरी हिस्से में है या निचले हिस्से में?",
  "en": "Where exactly is the stomach pain located? Is it the upper part or lower part?",
  "category": "stomach ache",

}  ,
  {
      "hi": "क्या आपने हाल ही में कोई असामान्य भोजन खाया है या आपके आहार में कोई बदलाव हुआ है?",
      "en": "Have you eaten anything unusual or had any changes in your diet recently?",
      "category": "dietary changes",
    },
    {
      "hi": "क्या आपको पाचन समस्याओं का इतिहास है (जैसे कि अम्लता, IBS, अल्सर आदि)?",
      "en": "Do you have a history of digestive problems (e.g., acid reflux, IBS, ulcers)?",
      "category": "digestive history",
      },
    ],
	'weakness': [
            {
                'hi': "क्या पेट की कमजोरी के कारण उठने या सीधे बैठने में कठिनाई होती है?",
                'en': "Does stomach weakness make it difficult for you to sit up or get out of bed?",
                'category': 'stomach_weakness_mobility'
            },
            {
                'hi': "क्या पेट के हिस्से में ताकत की कमी के कारण आपको कोई विशेष शारीरिक गतिविधियाँ करने में परेशानी होती है?",
                'en': "Does the lack of strength in your abdominal area affect your ability to perform physical activities?",
                'category': 'stomach_weakness_activity_limit'
            },
        ],
    'bloating': [
        {
            'hi': "क्या पेट में सूजन के साथ गैस या बेलचिंग भी होती है?",
            'en': "Do you experience gas or belching along with the bloating?",
            'category': 'stomach_bloating_gas'
        },
        {
            'hi': "क्या सूजन भोजन करने के तुरंत बाद होती है?",
            'en': "Does the bloating occur immediately after eating?",
            'category': 'stomach_bloating_trigger_food'
        },
        {
            'hi': "क्या सूजन के कारण पेट भारी या कड़ा लगता है?",
            'en': "Does your stomach feel heavy or tight due to bloating?",
            'category': 'stomach_bloating_heaviness'
        }
    ],
    'nausea': [
        {
            'hi': "क्या आपको उल्टी के अलावा मिचली भी महसूस हो रही है?",
            'en': "Are you feeling nauseous, in addition to vomiting?",
            'category': 'stomach_nausea_additional_symptoms'
        },
        {
            'hi': "क्या मिचली खास तौर पर किसी गंध या खाने से बढ़ जाती है?",
            'en': "Does the nausea get worse with certain smells or foods?",
            'category': 'stomach_nausea_trigger'
        },
        {
            'hi': "क्या मिचली के साथ चक्कर या थकान भी होती है?",
            'en': "Do you feel dizzy or tired along with the nausea?",
            'category': 'stomach_nausea_dizziness'
        }
    ],
    'diarrhea': [
        {
            'hi': "क्या दस्त के साथ बुखार या कमजोरी भी महसूस हो रही है?",
            'en': "Do you experience fever or weakness along with the diarrhea?",
            'category': 'stomach_diarrhea_additional_symptoms'
        },
        {
            'hi': "क्या मल पानी जैसा है या उसमें कोई बदलाव दिखाई दे रहा है?",
            'en': "Is your stool watery or has it changed in appearance?",
            'category': 'stomach_diarrhea_stool_character'
        },
        {
            'hi': "क्या दस्त के साथ पेट में मरोड़ या ऐंठन भी हो रही है?",
            'en': "Do you have abdominal cramps along with the diarrhea?",
            'category': 'stomach_diarrhea_cramps'
        }
    ],
    'default': [
        {
            'hi': "कृपया अपने पेट की समस्या के बारे में और जानकारी दें।",
            'en': "Please describe your stomach issue in more detail.",
            'category': 'stomach_detail'
        },
        {
            'hi': "क्या यह समस्या खाने-पीने की आदतों से जुड़ी लगती है?",
            'en': "Does this issue seem related to your eating habits?",
            'category': 'stomach_eating_habit_relation'
        },
        {
            'hi': "क्या आप कोई दवा ले रहे हैं जिससे पेट पर असर पड़ रहा हो?",
            'en': "Are you taking any medications that might be affecting your stomach?",
            'category': 'stomach_medication_link'
        }
    ]
},

	
'neck': {
        'pain': [
            {
                'hi': "क्या गर्दन का दर्द सिर या कंधों तक भी फैलता है?",
                'en': "Does the neck pain radiate to your head or shoulders?",
                'category': 'neck_pain_radiation'
            },
            {
      "hi": "क्या आपकी गर्दन में दर्द लगातार है या आता-जाता है?",
      "en": "Is your neck pain constant or does it come and go?",
      "category": "intermittent_neck_pain",
  },
    {
      "hi": "क्या गर्दन का दर्द किसी विशेष गतिविधि के दौरान बढ़ता है?",
      "en": "Does your neck pain increase during any specific activity?",
      "category": "activity_related_neck_pain",
  },
    {
      "hi": "क्या गर्दन के दर्द के कारण आपकी गतिशीलता प्रभावित हो रही है?",
      "en": "Is your mobility being affected due to neck pain?",
      "category": "mobility_impact_with_neck_pain",
    },
    {
      "hi": "क्या गर्दन के दर्द के साथ सिरदर्द भी हो रहा है?",
      "en": "Are you experiencing headaches along with neck pain?",
      "category": "headache_with_neck_pain",
   },
    {
      "hi": "क्या गर्दन में दर्द के साथ कोई सूजन भी है?",
      "en": "Is there any swelling along with neck pain?",
      "category": "swelling_with_neck_pain",
   },
    {
      "hi": "क्या गर्दन का दर्द अचानक शुरू हुआ है या धीरे-धीरे?",
      "en": "Did your neck pain start suddenly or gradually?",
      "category": "sudden_graduate_neck_pain",
   },
        ],
	'weakness': [
            {
                'hi': "क्या गर्दन की कमजोरी के कारण सिर को संभालना मुश्किल होता है?",
                'en': "Does neck weakness make it difficult to hold your head up?",
                'category': 'neck_weakness_head_support'
            },
            {
                'hi': "क्या गर्दन में कमजोरी के साथ थकान या झुकाव महसूस होता है?",
                'en': "Do you feel fatigue or drooping in the neck along with weakness?",
                'category': 'neck_weakness_fatigue_droop'
            },
        ],
        'stiffness': [
            {
                'hi': "क्या सुबह उठते समय गर्दन में जकड़न महसूस होती है?",
                'en': "Do you feel neck stiffness when you wake up in the morning?",
                'category': 'neck_stiffness_morning'
            }
        ],
        'swelling': [
            {
                'hi': "क्या गर्दन की सूजन के साथ बुखार या गिल्टी महसूस हो रही है?",
                'en': "Is there fever or a lump felt along with the neck swelling?",
                'category': 'neck_swelling_lump'
            }
        ],
        'injury': [
            {
        'hi': "क्या गर्दन को हिलाने पर दर्द बढ़ता है?",
        'en': "Does the pain worsen when you move your neck?",
        'category': 'neck_injury_movement_pain'
    },
    {
        'hi': "क्या चोट के बाद से गर्दन में अकड़न या जकड़न महसूस हो रही है?",
        'en': "Do you feel stiffness or tightness in your neck since the injury?",
        'category': 'neck_injury_stiffness'
    },
        ],
        'numbness': [
            {
                'hi': "क्या सुन्नपन गर्दन से कंधों या हाथों तक फैलता है?",
                'en': "Does the numbness spread from your neck to your shoulders or arms?",
                'category': 'neck_numbness_radiation'
            }
        ],
	'itching': [
            {
                'hi': "क्या गर्दन में खुजली के साथ लाल चकत्ते या रैश भी हैं?",
                'en': "Is the itching on your neck accompanied by redness or rash?",
                'category': 'neck_itching_signs'
            }
        ],
        'bleeding': [
            {
                'hi': "क्या गर्दन से खून निकलने से पहले कोई चोट या कट लगा था?",
                'en': "Was there any injury or cut before the bleeding from your neck started?",
                'category': 'neck_bleeding_cause'
            }
        ],
	'spasm': [
            {
                'hi': "क्या गर्दन की ऐंठन अचानक होती है और गर्दन हिलाना मुश्किल हो जाता है?",
                'en': "Do neck spasms happen suddenly and make it hard to move your neck?",
                'category': 'neck_spasm_effect'
            }
        ],
        'default': [
            {
                'hi': "कृपया अपनी गर्दन की समस्या के बारे में और जानकारी दें।",
                'en': "Please describe your neck issue in more detail.",
                'category': 'neck_detail'
            }
        ]
    },
  'knee': {
        'pain': [
            {
                'hi': "क्या घुटने का दर्द चलने या बैठने पर बढ़ता है?",
                'en': "Does the knee pain worsen while walking or sitting?",
                'category': 'knee_pain_activity'
            },
              {
      "hi": "क्या कोई विशेष चोट या घटना थी जिसके कारण घुटने में दर्द हुआ?",
     "en": "Was there any specific injury or event that triggered the knee pain?",
      "category": "knee pain",
    }, 
    {
      "hi": "क्या घुटनों में दर्द लगातार होता रहता है, या आता-जाता रहता है?",
      "en": "Does the knee pain occur constantly, or does it come and go?",
      "category": "knee pain",
  },
    {
      "hi": "क्या घुटने के आसपास सूजन, लाली या गर्मी महसूस हो रही है?",
      "en": "Have you noticed any swelling, redness, or warmth around the knee?",
      "category": "knee pain",
   },
    {
      "hi": "क्या आपको घुटने को मोड़ने या सीधा करने में कोई समस्या हो रही है?",
     "en": "Are you having trouble bending or straightening your knee?",
      "category": "knee pain",
   },
    {
      "hi": "क्या आप घुटने के दर्द का वर्णन कर सकते हैं? (तीव्र, सुस्त, दर्द, आदि)",
      "en": "Can you describe the knee pain? (Sharp, dull, aching, etc.)",
      "category": "knee pain",
    },
    {
      "hi": "दर्द आपके घुटने के किस हिस्से में महसूस हो रहा है? (सामने, पीछे, किनारे)",
      "en": "Where exactly in the knee do you feel the pain (front, back, sides)?",
      "category": "knee pain",
 },
    {
      "hi": "क्या चलने या सीढ़ियाँ चढ़ने जैसी कुछ गतिविधियों से घुटने का दर्द बढ़ जाता है?",
      "en": "Does the knee pain get worse with certain activities, like walking or climbing stairs?",
      "category": "knee pain",
   },
    {
      "hi": "क्या आपको घुटने में अस्थिरता या ऐसा लगता है जैसे घुटना 'गिर' रहा हो?",
      "en": "Do you feel any instability or like your knee is 'giving way'?",
      "category": "knee pain",
   },
        ],
        'swelling': [
            {
                'hi': "क्या सूजन के साथ गर्माहट या लालिमा भी महसूस हो रही है?",
                'en': "Is there warmth or redness along with the swelling?",
                'category': 'knee_swelling_signs'
            }
        ],
        'stiffness': [
            {
                'hi': "क्या सुबह उठने पर घुटने जकड़े हुए महसूस होते हैं?",
                'en': "Do your knees feel stiff when you wake up in the morning?",
                'category': 'knee_stiffness_morning'
            }
        ],
        'injury': [
              {
        'hi': "क्या चोट के बाद चलने में दिक्कत हो रही है?",
        'en': "Are you having difficulty walking after the injury?",
        'category': 'knee_injury_walking_difficulty'
    },
    {
        'hi': "क्या आपके घुटने में सूजन या सूजन के साथ दर्द है?",
        'en': "Is there swelling or pain along with the knee injury?",
        'category': 'knee_injury_swelling_pain'
    },
        ],
        'weakness': [
            {
                'hi': "क्या घुटना कमजोर महसूस होता है या चलते समय लड़खड़ाता है?",
                'en': "Does the knee feel weak or give way while walking?",
                'category': 'knee_weakness_instability'
            }
        ],
	'freeze': [
            {
                'hi': "क्या ठंड में आपके घुटनों में ठंडक या सुन्नपन होता है?",
                'en': "Do your knees feel cold or numb in cold weather?",
                'category': 'knee_freezing_cold_sensitivity'
            }
        ],
	'itching': [
            {
                'hi': "क्या घुटने में खुजली के साथ सूजन या लालपन है?",
                'en': "Is the itching in your knee accompanied by swelling or redness?",
                'category': 'knee_itching_signs'
            }
        ],
        'default': [
            {
                'hi': "कृपया अपने घुटने की समस्या के बारे में और जानकारी दें।",
                'en': "Please describe your knee issue in more detail.",
                'category': 'knee_detail'
            }
        ]
    },
  'foot': {
        'pain': [
            {
                'hi': "क्या पैर में दर्द चलने या खड़े होने पर बढ़ता है?",
                'en': "Does the foot pain increase while walking or standing?",
                'category': 'foot_pain_activity'
            },
            {
      "hi": "क्या दर्द एक पैर में है या दोनों पैरों में?",
      "en": "Is the pain in one foot or both feet?",
      "category": "foot pain",
   
    },
    {
      "hi": "क्या पैर में दर्द लगातार बना रहता है, या यह आता-जाता रहता है?",
      "en": "Is the foot pain constant, or does it come and go?",
      "category": "foot pain",

    },
    {
      "hi": "क्या आपको पैरों में सूजन, लाली, या चोट का अनुभव हो रहा है?",
      "en": "Are you experiencing any swelling, redness, or bruising in the foot?",
      "category": "foot pain",

    },
    {
      "hi": "क्या आपको हाल ही में पैर में कोई चोट या आघात हुआ है?",
      "en": "Have you had any recent injuries or trauma to your foot?",
      "category": "foot pain",

    },
    {
      "hi": "क्या दर्द कुछ गतिविधियों के साथ बढ़ जाता है, जैसे लंबी अवधि तक चलना या खड़ा होना?",
      "en": "Does the pain get worse with certain activities, like walking or standing for long periods?",
      "category": "foot pain",
  
    },
        ],
	'weakness': [
            {
                'hi': "क्या पैर की कमजोरी के कारण आपको चलने में अस्थिरता महसूस होती है?",
                'en': "Does foot weakness make you feel unsteady while walking?",
                'category': 'foot_weakness_unsteady_walking'
            },
            {
                'hi': "क्या पैर की कमजोरी के कारण सीढ़ियाँ चढ़ना या दौड़ना मुश्किल हो जाता है?",
                'en': "Does foot weakness make it difficult to climb stairs or run?",
                'category': 'foot_weakness_stairs_running'
            },
        ],
        'swelling': [
            {
                'hi': "क्या सूजन के साथ पैर में गर्माहट या लालिमा है?",
                'en': "Is there warmth or redness along with the swelling in your foot?",
                'category': 'foot_swelling_signs'
            }
        ],
        'numbness': [
            {
                'hi': "क्या सुन्नपन पूरे पैर में है या सिर्फ उंगलियों तक सीमित है?",
                'en': "Is the numbness throughout your foot or just in the toes?",
                'category': 'foot_numbness_location'
            }
        ],
        'injury': [
            {
    'hi': "क्या दोनों पैरों में चोट लगी है?",
    'en': "Are both feet injured?",
    'category': 'foot_injury_location'
            }
        ],
        'stiffness': [
            {
                'hi': "क्या सुबह उठने पर पैर में जकड़न महसूस होती है?",
                'en': "Do you feel stiffness in your foot when you wake up?",
                'category': 'foot_stiffness_morning'
            }
        ],
	'freeze': [
            {
                'hi': "क्या ठंड में आपके पैर सुन्न या ठंडे हो जाते हैं?",
                'en': "Do your feet feel numb or cold in cold weather?",
                'category': 'feet_freezing_cold_sensitivity'
            }
        ],
	'spasm': [
            {
                'hi': "क्या पैरों में ऐंठन चलते समय या व्यायाम करते समय होती है?",
                'en': "Do you get foot spasms while walking or during exercise?",
                'category': 'foot_spasm_context'
            }
        ],
	'itching': [
            {
                'hi': "क्या पैरों में खुजली किसी खास समय जैसे रात में ज्यादा होती है?",
                'en': "Does the itching in your legs get worse at certain times like at night?",
                'category': 'leg_itching_timing'
            }
        ],
        'default': [
            {
                'hi': "कृपया अपने पैर की समस्या के बारे में और जानकारी दें।",
                'en': "Please describe your foot issue in more detail.",
                'category': 'foot_detail'
            }
        ]
    },
    'shoulder': {
        'pain': [
            {
                'hi': "क्या कंधे का दर्द हाथ उठाने पर बढ़ता है?",
                'en': "Does the shoulder pain increase when you lift your arm?",
                'category': 'shoulder_pain_movement'
            },
                {
      "hi": "क्या कंधे का दर्द तेज़, सुस्त या दर्दभरा है?",
      "en": "Is the shoulder pain sharp, dull, or achy?",
      "category": "shoulder pain",

    },
    {
      "hi": "क्या आपको हाल ही में कंधे में कोई चोट हुआ है?",
      "en": "Have you had any recent injuries to your shoulder?",
      "category": "shoulder pain",

    },
    {
      "hi": "क्या कंधे का दर्द विशिष्ट गतिविधियों या गतिविधियों, जैसे उठाने या पहुंचने से बढ़ जाता है?",
      "en": "Does the shoulder pain worsen with specific movements or activities, such as lifting or reaching?",
      "category": "shoulder pain",

    },
    {
      "hi": "क्या आपने कंधे में सूजन, चोट या गति सीमा में प्रतिबंध महसूस किया है?",
      "en": "Have you noticed any swelling, bruising, or restricted range of motion in the shoulder?",
      "category": "shoulder pain",

    },
        ],
        'stiffness': [
            {
                'hi': "क्या कंधा पूरी तरह घुमाने में परेशानी होती है?",
                'en': "Is it difficult to fully rotate your shoulder?",
                'category': 'shoulder_stiffness_range'
            }
        ],
        'injury': [
           {
    'hi': "क्या दोनों कंधों में चोट लगी है?",
    'en': "Are both shoulders injured?",
    'category': 'shoulder_injury_location'
           }
        ],
        'numbness': [
            {
                'hi': "क्या झुनझुनी या सुन्नपन कंधे से हाथ तक फैलता है?",
                'en': "Does the numbness or tingling extend from your shoulder to your arm?",
                'category': 'shoulder_numbness_extent'
            }
        ],
        'weakness': [
            {
                'hi': "क्या कंधे में कमजोरी के कारण भारी चीजें उठाना मुश्किल है?",
                'en': "Is it hard to lift heavy objects due to shoulder weakness?",
                'category': 'shoulder_weakness_function'
            }
        ],
	'itching': [
            {
                'hi': "क्या कंधे में खुजली के साथ रैश या दर्द है?",
                'en': "Is the itching in your shoulder accompanied by rash or pain?",
                'category': 'shoulder_itching_associated'
            }
        ],
        'default': [
            {
                'hi': "कृपया अपने कंधे की समस्या के बारे में और जानकारी दें।",
                'en': "Please describe your shoulder issue in more detail.",
                'category': 'shoulder_detail'
            }
        ]
    },
'ear': {
    'pain': [
        {
            'hi': "क्या कान में दर्द के साथ बुखार या सुनाई देने में दिक्कत है?",
            'en': "Do you have fever or difficulty hearing along with the ear pain?",
            'category': 'ear_pain_additional_symptoms'
        },
        {
            'hi': "क्या दर्द अचानक शुरू हुआ था या धीरे-धीरे बढ़ा?",
            'en': "Did the pain start suddenly or build up gradually?",
            'category': 'ear_pain_onset'
        },

        {
          "hi": "क्या आपको एक कान में दर्द हो रहा है या दोनों कानों में?",
          "en": "Do you have pain in one ear or both ears?",
          "category": "ear pain",
   },
        {
          "hi": "क्या कान में दर्द सर्दी, साइनस संक्रमण, या ऊपरी श्वसन संक्रमण के बाद शुरू हुआ?",
          "en": "Did the ear pain start after a cold, sinus infection, or upper respiratory infection?",
          "category": "ear pain",
  },

    ],
    'hearing_loss': [
        {
            'hi': "क्या सुनाई देने में समस्या एक कान में है या दोनों में?",
            'en': "Is the hearing loss in one ear or both?",
            'category': 'ear_hearing_loss_side'
        },
        {
            'hi': "क्या सुनाई कम होना अचानक हुआ या धीरे-धीरे?",
            'en': "Did the hearing loss happen suddenly or gradually?",
            'category': 'ear_hearing_loss_onset'
        },
        {
            'hi': "क्या सुनाई देने में बदलाव दिन के समय के अनुसार बदलता है?",
            'en': "Does your hearing change depending on the time of day?",
            'category': 'ear_hearing_loss_variation'
        }
    ],
    'ringing': [
        {
            'hi': "क्या कान में घंटी या गूंजने जैसी आवाज़ लगातार रहती है?",
            'en': "Is the ringing or buzzing in your ear constant?",
            'category': 'ear_ringing_frequency'
        },
        {
            'hi': "क्या यह आवाज़ किसी खास स्थिति में तेज़ हो जाती है, जैसे रात में?",
            'en': "Does the sound get louder in specific situations, like at night?",
            'category': 'ear_ringing_conditions'
        },
        {
            'hi': "क्या इस आवाज़ के साथ चक्कर या संतुलन की समस्या भी होती है?",
            'en': "Do you also experience dizziness or balance issues with the ringing?",
            'category': 'ear_ringing_dizziness'
        }
    ],
    'discharge': [
    {
      "hi": "क्या स्राव के कारण कान में सूजन हो रही है?",
      "en": "Is there any swelling in your ears due to discharge?",
      "category": "swelling_with_ear_discharge",
      "symptom": "swelling",
      "risk_factor": False,    },
    {
      "hi": "क्या स्राव के साथ आपको सुनने में कठिनाई हो रही है?",
      "en": "Are you having difficulty hearing along with ear discharge?",
      "category": "hearing_difficulty_with_ear_discharge",
      "symptom": "hearing loss",
      "risk_factor": False,    },
    ],
    'infection': [
        {
            'hi': "क्या डॉक्टर ने कभी कान के संक्रमण की पुष्टि की है?",
            'en': "Have you ever been diagnosed with an ear infection before?",
            'category': 'ear_infection_history'
        },
        {
            'hi': "क्या संक्रमण के समय दर्द, बुखार या बहाव जैसे लक्षण थे?",
            'en': "Did you have symptoms like pain, fever, or discharge during the infection?",
            'category': 'ear_infection_symptoms'
        },
        {
            'hi': "क्या आपने पहले भी इसी तरह के संक्रमण का अनुभव किया है?",
            'en': "Have you experienced similar infections before?",
            'category': 'ear_infection_recurrence'
        }
    ],
    'freeze': [
            {
                'hi': "क्या ठंड में आपके कान सुन्न या बहुत ठंडे महसूस होते हैं?",
                'en': "Do your ears feel numb or extremely cold in cold weather?",
                'category': 'ear_freezing_cold_sensitivity'
            }
        ],
    'bleeding': [
            {
                'hi': "क्या कान से खून निकलने से पहले चोट लगी थी या किसी चीज़ से कान साफ़ किया था?",
                'en': "Was there any injury or use of an object in the ear before the bleeding started?",
                'category': 'ear_bleeding_cause'
            }
        ],
     'itching': [
            {
                'hi': "क्या कान में खुजली के साथ द्रव या रिसाव हो रहा है?",
                'en': "Is there any fluid or discharge along with the itching in your ear?",
                'category': 'ear_itching_discharge'
            }
        ],
    'default': [
        {
            'hi': "कृपया अपने कान की समस्या के बारे में और जानकारी दें।",
            'en': "Please describe your ear issue in more detail.",
            'category': 'ear_detail'
        },
        {
            'hi': "क्या समस्या कान के अंदर महसूस होती है या बाहरी हिस्से में?",
            'en': "Is the problem felt inside the ear or on the outer part?",
            'category': 'ear_location'
        },
        {
            'hi': "क्या आपकी नींद या रोज़मर्रा के काम इस समस्या से प्रभावित हो रहे हैं?",
            'en': "Is this issue affecting your sleep or daily activities?",
            'category': 'ear_impact'
        }
    ]
},
	
   'nails': {
        'discoloration': [
            {
                'hi': "क्या नाखूनों का रंग हाल ही में बदला है?",
                'en': "Has the color of your nails changed recently?",
                'category': 'nail_discoloration_change'
            }
        ],
        'pain': [
            {
                'hi': "क्या नाखून में दर्द किसी चोट के बाद शुरू हुआ?",
                'en': "Did the nail pain start after any injury?",
                'category': 'nail_pain_injury'
            }
        ],
        'infection': [
            {
                'hi': "क्या नाखून के पास सूजन, मवाद या लालिमा है?",
                'en': "Is there swelling, pus, or redness near the nail?",
                'category': 'nail_infection_signs'
            }
        ],
        'brittle': [
            {
                'hi': "क्या आपके नाखून आसानी से टूट या चटक जाते हैं?",
                'en': "Do your nails crack or break easily?",
                'category': 'nail_brittle_frequency'
            }
        ],
        'growth': [
            {
                'hi': "क्या आपने नाखूनों की वृद्धि में कमी या बदलाव देखा है?",
                'en': "Have you noticed any changes or slowdown in nail growth?",
                'category': 'nail_growth_change'
            }
        ],
        'default': [
            {
                'hi': "कृपया अपने नाखूनों की समस्या के बारे में और जानकारी दें।",
                'en': "Please describe your nail issue in more detail.",
                'category': 'nail_detail'
            }
        ]
    }, 
    'bone': {
        'pain': [
            {
                'hi': "क्या यह हड्डी का दर्द किसी विशेष गतिविधि से जुड़ा है?",
                'en': "Is the bone pain related to any specific activity?",
                'category': 'bone_pain_activity'
            }
        ],
        'fracture': [
            {
                'hi': "क्या आपको एक्स-रे या स्कैन में फ्रैक्चर की पुष्टि हुई है?",
                'en': "Has a fracture been confirmed through an X-ray or scan?",
                'category': 'bone_fracture_diagnosed'
            }
        ],
        'swelling': [
            {
                'hi': "क्या सूजन के साथ दर्द या हड्डी पर दबाव से तकलीफ़ होती है?",
                'en': "Is the swelling painful or tender to touch over the bone?",
                'category': 'bone_swelling_pain'
            }
        ],
        'weakness': [
            {
                'hi': "क्या आपकी हड्डियाँ आसानी से टूट जाती हैं या कमजोर महसूस होती हैं?",
                'en': "Do your bones break easily or feel weak?",
                'category': 'bone_weakness_frequency'
            }
        ],
        'injury': [
            {
                'hi': "हड्डी को चोट कब और कैसे लगी थी?",
                'en': "When and how did you injure the bone?",
                'category': 'bone_injury_time'
            }
        ],
        'default': [
            {
                'hi': "कृपया अपनी हड्डियों की समस्या के बारे में और जानकारी दें।",
                'en': "Please describe your bone issue in more detail.",
                'category': 'bone_detail'
            }
        ]
},
'joint': {
        'pain': [
            {
                'hi': "क्या जोड़ों में दर्द गतिविधि करते समय या मौसम बदलने पर बढ़ता है?",
                'en': "Does the joint pain increase with activity or during weather changes?",
                'category': 'joint_pain_activity_weather'
            },
            
          {
                "hi": "क्या आपके जोड़ों में दर्द लगातार है या आता-जाता है?",
              "en": "Is your joint pain constant or does it come and go?",
                "category": "intermittent_pain",
                "symptom": None,
                "risk_factor": False,    },
              {
                "hi": "क्या किसी विशेष गतिविधि के दौरान जोड़ों में दर्द बढ़ता है?",
                "en": "Does your joint pain increase during any specific activity?",
                "category": "activity_related_pain",
                "symptom": None,
                "risk_factor": False,    },
        ],
        'swelling': [
            {
                'hi': "क्या सूजन के साथ जोड़ में गर्माहट या लालिमा महसूस होती है?",
                'en': "Is there warmth or redness along with the swelling in the joint?",
                'category': 'joint_swelling_signs'
            }
        ],
        'stiffness': [
            {
                'hi': "क्या जोड़ों में जकड़न या कठोरता सुबह उठने पर ज्यादा महसूस होती है?",
                'en': "Does the stiffness or rigidity in your joints feel worse in the morning?",
                'category': 'joint_stiffness_morning'
            }
        ],
        'weakness': [
            {
                'hi': "क्या जोड़ों में कमजोरी के कारण चलते वक्त अस्थिरता महसूस होती है?",
                'en': "Does the weakness in the joint cause instability while walking?",
                'category': 'joint_weakness_instability'
            }
        ],
        'injury': [
               {
        'hi': "क्या चोट के बाद चलने में दिक्कत हो रही है?",
        'en': "Are you having difficulty walking after the injury?",
        'category': 'knee_injury_walking_difficulty'
    },
        ],
        'default': [
            {
                'hi': "कृपया अपने जोड़ों की समस्या के बारे में और जानकारी दें।",
                'en': "Please describe your joint issue in more detail.",
                'category': 'joint_detail'
            }
        ]
    },
 'skin': {
        'rash': [
            {
                'hi': "क्या यह चकत्ते शरीर के किसी खास हिस्से पर हैं?",
                'en': "Is the rash located on a specific part of your body?",
                'category': 'skin_rash_location'
            }
        ],
        'itching': [
            {
                'hi': "क्या खुजली लगातार होती है या समय-समय पर?",
                'en': "Is the itching constant or does it come and go?",
                'category': 'skin_itching_duration'
            }
        ],
        'dryness': [
            {
                'hi': "क्या सूखी त्वचा पर दरारें या खून आना भी होता है?",
                'en': "Is the dry skin cracking or bleeding?",
                'category': 'skin_dryness_severity'
            }
        ],
        'discoloration': [
            {
                'hi': "क्या त्वचा का रंग धीरे-धीरे बदल रहा है या अचानक?",
                'en': "Did the skin discoloration happen gradually or suddenly?",
                'category': 'skin_discoloration_timeline'
            }
        ],
        'swelling': [
            {
                'hi': "क्या सूजन वाली जगह पर दर्द या गर्मी महसूस हो रही है?",
                'en': "Is there pain or warmth at the swollen area on the skin?",
                'category': 'skin_swelling_symptoms'
            }
        ],
        'acne': [
        {
            'hi': "क्या मुहांसों के साथ दर्द या पस भी होता है?",
            'en': "Do the pimples come with pain or pus?",
            'category': 'skin_acne_severity'
        }
],
        'burn': [
            {
                'hi': "क्या जलने के कारण त्वचा में छाले या पपड़ी बन रही है?",
                'en': "Are blisters or scabs forming due to the burn?",
                'category': 'skin_burn_blisters'
            }
        ],
        'infection': [
            {
                'hi': "क्या त्वचा में किसी प्रकार के घाव, मवाद या लालिमा है?",
                'en': "Is there any wound, pus, or redness on the skin?",
                'category': 'skin_infection_signs'
            }
        ],
	 'bleeding': [
            {
                'hi': "क्या त्वचा से खून किसी चोट, फोड़े या दाने की वजह से निकल रहा है?",
                'en': "Is the bleeding from your skin due to an injury, boil, or rash?",
                'category': 'skin_bleeding_cause'
            }
        ],
        'default': [
            {
                'hi': "कृपया अपनी त्वचा की समस्या के बारे में और जानकारी दें।",
                'en': "Please describe your skin issue in more detail.",
                'category': 'skin_detail'
            }
        ]
    },
'muscle': {
        'pain': [
            {
                'hi': "क्या मांसपेशियों में दर्द गतिविधि करने पर बढ़ता है?",
                'en': "Does the muscle pain increase with activity?",
                'category': 'muscle_pain_activity'
            },
            {
              "hi": "क्या आपके मांसपेशियों में दर्द लगातार है या आता-जाता है?",
              "en": "Is your muscle pain constant or does it come and go?",
              "category": "intermittent_pain",
          },
            {
              "hi": "क्या आपके मांसपेशियों में दर्द के साथ सूजन भी है?",
              "en": "Is there any swelling along with your muscle pain?",
              "category": "swelling",
          },
        {
              "hi": "क्या मांसपेशियों में दर्द के साथ कमजोरी भी महसूस हो रही है?",
            "en": "Are you experiencing any weakness along with muscle pain?",
              "category": "weakness",
          },
            {
              "hi": "क्या आपको मांसपेशियों में खिंचाव महसूस हो रहा है?",
              "en": "Are you feeling any muscle cramps?",
              "category": "cramps",
            }, 
        ],
        'weakness': [
            {
                'hi': "क्या मांसपेशियों में कमजोरी के कारण आपको भारी चीज़ें उठाने में परेशानी होती है?",
                'en': "Does muscle weakness make it hard for you to lift heavy objects?",
                'category': 'muscle_weakness_function'
            }
        ],
        'spasm': [
            {
                'hi': "क्या मांसपेशियों में ऐंठन या मरोड़ लगातार हो रही है?",
                'en': "Are the muscle spasms or cramps happening frequently?",
                'category': 'muscle_spasm_frequency'
            }
        ],
        'injury': [
               {
        'hi': "क्या चोट के बाद चलने में दिक्कत हो रही है?",
        'en': "Are you having difficulty walking after the injury?",
        'category': 'knee_injury_walking_difficulty'
    },
        ],
'swelling': [
            {
                'hi': "क्या सूजन के साथ दर्द या गर्माहट महसूस हो रही है?",
                'en': "Is there pain or warmth along with the swelling in the muscle?",
                'category': 'muscle_swelling_signs'
            }
        ],
	    'cramps': [
            {
                'hi': "क्या आपको मांसपेशियों में ऐंठन चलते समय या व्यायाम करते समय होती है?",
                'en': "Do you experience muscle cramps while walking or exercising?",
                'category': 'muscle_cramps_activity_triggered'
            },
            {
                'hi': "क्या मांसपेशियों की ऐंठन रात में सोते समय होती है?",
                'en': "Do your muscle cramps occur during the night while sleeping?",
                'category': 'muscle_cramps_nighttime'
            },
        ],
	'itching': [
            {
                'hi': "क्या मांसपेशियों में खुजली व्यायाम या खिंचाव के बाद होती है?",
                'en': "Does the muscle itching happen after exercise or strain?",
                'category': 'muscle_itching_trigger'
            }
        ],
        'default': [
            {
                'hi': "कृपया अपनी मांसपेशियों की समस्या के बारे में और जानकारी दें।",
                'en': "Please describe your muscle issue in more detail.",
                'category': 'muscle_detail'
            }
        ]
    },

'heart': {
        'pain': [
            {'hi': "क्या दर्द सीने के बीच में है या बाईं तरफ?",
             'en': "Is the pain in the center of the chest or on the left side?",
             'category': 'heart_pain_location'}
            ],
	     'weakness': [
            {
                'hi': "क्या हल्की गतिविधियों से ही थकान या सांस फूलने लगती है?",
                'en': "Do you feel tired or short of breath even with mild activity?",
                'category': 'heart_weakness_exertion'
            },
            {
                'hi': "क्या आपकी सहनशक्ति पहले की तुलना में कम हो गई है?",
                'en': "Has your stamina decreased compared to before?",
                'category': 'heart_weakness_stamina_loss'
            },
        ],
        'palpitation': [
            {'hi': "क्या आपको दिल की धड़कन तेज या अनियमित महसूस हो रही है?",
             'en': "Do you feel your heartbeat is fast or irregular?",
             'category': 'heart_palpitations'}
        ],
      
        'burn': [
            {'hi': "क्या आपको दिल की धड़कन तेज या अनियमित महसूस हो रही है?",
             'en': "Do you feel your heartbeat is fast or irregular?",
             'category': 'heart_palpitations'}
        ],
        'default': [
            {'hi': "कृपया अपने दिल से जुड़ी समस्या के बारे में और बताएं।",
             'en': "Please tell me more about your heart-related issue.",
             'category': 'heart_detail'}
        ]
    },

'urinary': {
        'pain': [
            {'hi': "क्या पेशाब करते समय जलन या दर्द होता है?",
             'en': "Do you experience burning or pain while urinating?",
             'category': 'urinary_pain'}
        ],
        'frequency': [
            {'hi': "दिन में कितनी बार पेशाब करने की जरूरत महसूस होती है?",
             'en': "How many times do you feel the need to urinate in a day?",
             'category': 'urinary_frequency'}
        ],
        'blood': [
            {'hi': "क्या पेशाब में खून दिखा है?",
             'en': "Have you noticed any blood in your urine?",
             'category': 'urinary_blood'}
        ],
        'difficulty': [
            {'hi': "क्या पेशाब करने में कठिनाई या रुकावट हो रही है?",
             'en': "Are you experiencing difficulty or blockage while urinating?",
             'category': 'urinary_difficulty'}
        ],
        'default': [
            {'hi': "कृपया अपनी पेशाब से जुड़ी समस्या के बारे में और जानकारी दें।",
             'en': "Please tell me more about your urinary issue.",
             'category': 'urinary_detail'}
        ]
    },
'toes': {
        'injury': [
            {'hi': "कौन सी उंगली या उंगलियाँ घायल हैं?",
             'en': "Which toe or toes are injured?",
             'category': 'toes_injury_location'}
        ],
        'pain': [
            {'hi': "क्या दर्द चलने पर ज्यादा होता है या आराम करते समय भी रहता है?",
             'en': "Does the pain worsen while walking or is it present even at rest?",
             'category': 'toes_pain_detail'}
        ],
        'swelling': [
            {'hi': "क्या सूजन के साथ लालिमा या गर्माहट भी है?",
             'en': "Is there redness or warmth along with the swelling?",
             'category': 'toes_swelling_symptoms'}
        ],
        'default': [
            {'hi': "कृपया अपनी उंगली की समस्या के बारे में और जानकारी दें।",
             'en': "Please describe your toe issue in more detail.",
             'category': 'toes_detail'}
        ]
    },
 'nose': {
        'injury': [
            {
                'hi': "नाक में चोट कब और कैसे लगी थी?",
                'en': "How and when did you injure your nose?",
                'category': 'nose_injury_time'
            }
        ],
        'burning': [
            {
                'hi': "क्या नाक में जलन लगातार रहती है या कुछ खास चीज़ों से होती है?",
                'en': "Is the burning sensation in your nose constant or triggered by something specific?",
                'category': 'nose_burning_trigger'
            }
        ],
        'sniffing': [
            {
                'hi': "क्या आपको सूंघने में कठिनाई हो रही है?",
                'en': "Are you having trouble smelling things?",
                'category': 'nose_sniffing_difficulty'
            }
        ],
        'pain': [
            {
              "hi": "क्या आपकी नाक में लगातार दर्द या जलन हो रही है?",
              "en": "Are you experiencing persistent pain or burning sensation in your nose?",
              "category": "nose pain",
            },
            {
              "hi": "क्या आपको हाल ही में सर्दी, एलर्जी या साइनस की समस्या हुई है?",
              "en": "Have you recently had a cold, allergies, or sinus issues?",
              "category": "nose pain",
            },     
    ],
        'infection': [
            {
                'hi': "क्या आपको सर्दी, जुकाम या साइनस जैसी समस्या भी है?",
                'en': "Are you also experiencing cold, congestion, or sinus problems?",
                'category': 'nose_infection_symptoms'
            }
        ],
   'congestion': [
            {'hi': "क्या आपकी नाक पूरी तरह से बंद है या आंशिक रूप से?",
             'en': "Is your nose completely blocked or partially blocked?",
             'category': 'nose_congestion'}
        ],
        'bleed': [
            {'hi': "क्या नाक से खून बहना जारी है या रुक गया है?",
             'en': "Is the nosebleed still continuing or has it stopped?",
             'category': 'nose_bleed_status'}
        ],
	 'freeze': [
            {
                'hi': "क्या आपको ठंडे मौसम में नाक में सुन्नपन या ठंडक का अनुभव होता है?",
                'en': "Do you feel numbness or a cold sensation in your nose during cold weather?",
                'category': 'nasal_freezing_cold_sensitivity'
            }
        ],
	 'itching': [
            {
                'hi': "क्या नाक में खुजली के साथ छींकें या बहाव भी हो रहा है?",
                'en': "Is the nose itching accompanied by sneezing or discharge?",
                'category': 'nose_itching_allergy'
            }
        ],
        'default': [
            {
                'hi': "कृपया अपनी नाक की समस्या के बारे में और जानकारी दें।",
                'en': "Please describe your nose issue in more detail.",
                'category': 'nose_detail'
            }
        ]
    },
 'thigh': {
        'pain': [
            {
                'hi': "क्या जांघ में दर्द चलने या दौड़ने से बढ़ता है?",
                'en': "Does the thigh pain worsen when walking or running?",
                'category': 'thigh_pain_activity'
            },
                {
      "hi": "आप थाई में दर्द का वर्णन कैसे करेंगे? क्या यह तेज़, मन्द, जलन वाला, या धड़कता हुआ है?",
      "en": "Can you describe the pain in your thigh? Is it sharp, dull, burning, or throbbing?",
      "category": "thigh pain",
 
    },
    {
      "hi": "दर्द ठीक कहाँ है? क्या यह एक तरफ़, दोनों तरफ़ या किसी और हिस्से तक फैलता है?",
      "en": "Where exactly is the pain located in your thigh? Is it on one side, both sides, or spreading elsewhere?",
      "category": "thigh pain",

    },
    {
      "hi": "क्या कोई गतिविधि, स्थिति या आराम से दर्द बढ़ता या कम होता है?",
      "en": "Does anything make the pain better or worse, like movement, posture, or rest?",
      "category": "thigh pain",

    },
    {
      "hi": "क्या आपने हाल ही में कोई भारी वजन उठाया है या कोई चोट लगी है?",
      "en": "Have you had any recent injuries, heavy lifting, or physical strain?",
      "category": "thigh pain",

    },
    {
      "hi": "क्या आपको पहले भी ऐसी थाई में दर्द की समस्या रही है या कोई पुरानी बीमारी है?",
      "en": "Do you have a history of similar pain or any known medical conditions?",
      "category": "thigh pain",

    },
    {
      "hi": "क्या आप कोई दवाइयाँ या सप्लीमेंट्स ले रहे हैं?",
      "en": "Are you taking any medications or supplements currently?",
      "category": "thigh pain",

    },
    {
      "hi": "क्या इस दर्द से आपकी रोज़मर्रा की गतिविधियाँ या नींद प्रभावित हो रही हैं?",
      "en": "How does the pain affect your daily activities or sleep?",
      "category": "thigh pain",

    },
        ],
        'weakness': [
            {
                'hi': "क्या जांघ की कमजोरी के कारण सीढ़ियाँ चढ़ने में दिक्कत होती है?",
                'en': "Is thigh weakness making it hard to climb stairs?",
                'category': 'thigh_weakness_function'
            }
        ],
        'spasm': [
            {
                'hi': "क्या जांघ में बार-बार मरोड़ या ऐंठन हो रही है?",
                'en': "Are you experiencing frequent cramps or spasms in your thigh?",
                'category': 'thigh_spasm_frequency'
            }
        ],
        'injury': [
            {
                'hi': "क्या जांघ में किसी गतिविधि के दौरान चोट लगी थी?",
                'en': "Did the thigh injury happen during any specific activity?",
                'category': 'thigh_injury_cause'
            }
        ],
        'swelling': [
            {
                'hi': "क्या सूजी हुई जांघ को छूने पर गर्म लगती है?",
                'en': "Does the swollen thigh feel warm to the touch?",
                'category': 'thigh_swelling_signs'
            }
        ],
	 'numbness': [
            {
                'hi': "क्या जांघ का सुन्नपन पूरे पैर तक फैलता है?",
                'en': "Does the numbness in your thigh spread down the leg?",
                'category': 'thigh_numbness_distribution'
            }
        ],
	 'itching': [
            {
                'hi': "क्या जांघ में खुजली के साथ रैश या फफोले भी हैं?",
                'en': "Is the thigh itching accompanied by a rash or blisters?",
                'category': 'thigh_itching_signs'
            }
        ],
        'default': [
            {
                'hi': "कृपया अपनी जांघ की समस्या के बारे में अधिक जानकारी दें।",
                'en': "Please provide more details about your thigh issue.",
                'category': 'thigh_detail'
            }
        ]
    },
 'forehead': {
        'pain': [
            {
                'hi': "क्या माथे का दर्द लगातार बना रहता है या समय-समय पर आता है?",
                'en': "Is the forehead pain constant or does it come and go?",
                'category': 'forehead_pain_pattern'
            }
        ],
        'swelling': [
            {
                'hi': "क्या सूजन के साथ माथे पर लालिमा या गर्माहट है?",
                'en': "Is there redness or warmth along with the forehead swelling?",
                'category': 'forehead_swelling_signs'
            }
        ],
        'injury': [
            {
                'hi': "क्या माथे में चोट किसी गिरावट या टक्कर से लगी थी?",
                'en': "Was the forehead injury caused by a fall or impact?",
                'category': 'forehead_injury_cause'
            }
        ],
        'tingling': [
            {
                'hi': "क्या माथे में झनझनाहट के साथ सुन्नपन भी महसूस होता है?",
                'en': "Do you feel numbness along with the tingling in your forehead?",
                'category': 'forehead_tingling_symptoms'
            }
        ],
        'default': [
            {
                'hi': "कृपया अपनी माथे की समस्या के बारे में और जानकारी दें।",
                'en': "Please describe your forehead issue in more detail.",
                'category': 'forehead_detail'
            }
        ]
    },
 'tongue': {
        'pain': [
            {
                'hi': "क्या जीभ में दर्द खाने या बोलने से बढ़ता है?",
                'en': "Does the tongue pain increase when eating or speaking?",
                'category': 'tongue_pain_activity'
            }
        ],
        'swelling': [
            {
                'hi': "क्या सूजी हुई जीभ के कारण निगलने या साँस लेने में परेशानी हो रही है?",
                'en': "Is the swollen tongue making it hard to swallow or breathe?",
                'category': 'tongue_swelling_difficulty'
            }
        ],
        'burning': [
            {
                'hi': "क्या जीभ में जलन किसी गर्म या मसालेदार चीज़ के सेवन के बाद शुरू हुई?",
                'en': "Did the tongue burning start after eating something hot or spicy?",
                'category': 'tongue_burning_trigger'
            }
        ],
        'numbness': [
            {
                'hi': "क्या जीभ की सुन्नता अचानक शुरू हुई थी?",
                'en': "Did the numbness in your tongue start suddenly?",
                'category': 'tongue_numbness_onset'
            }
        ],
        'ulcers': [
            {
                'hi': "क्या जीभ के छाले खाने-पीने में तकलीफ देते हैं?",
                'en': "Do the tongue ulcers cause discomfort while eating or drinking?",
                'category': 'tongue_ulcers_discomfort'
            }
        ],
        'default': [
            {
                'hi': "कृपया अपनी जीभ की समस्या के बारे में और जानकारी दें।",
                'en': "Please describe your tongue issue in more detail.",
                'category': 'tongue_detail'
            }
        ]
    },
 'mouth': {
        'pain': [
            {
                'hi': "क्या मुँह में दर्द खाना खाते समय बढ़ता है?",
                'en': "Does the mouth pain increase while eating?",
                'category': 'mouth_pain_eating'
            },
                {
      "hi": "क्या आपके मुंह का दर्द तेजी से फैल रहा है",
      "en": "Is your mouth pain spreading rapidly?",
      "category": "rapid_spread_mouth_sores",
  },
    {
      "hi": "क्या आपके मुंह में दर्द के साथ सूजन भी है?",
      "en": "Is there any swelling along with your mouth pain?",
      "category": "swelling_with_mouth_sores",
  },
    {
      "hi": "क्या खाने या पीने के दौरान आपके मुंह में दर्द बढ़ जाता है?",
      "en": "Does your mouth pain increase while eating or drinking?",
      "category": "pain_with_mouth_sores",
   },
{
      "hi": "क्या आपके मुंह से खून बह रहा है?",
      "en": "Is your mouth bleeding?",
      "category": "bleeding_mouth_sores",
   },
    {
      "hi": "क्या आपको मुंह के दर्द के साथ दांत में भी दर्द हो रहा है?",
      "en": "Are you experiencing tooth pain along with mouth pain?",
      "category": "tooth_pain_with_mouth_sores",
   },
    {
      "hi": "क्या मुंह में दर्द के कारण बोलने में कठिनाई हो रही है?",
      "en": "Is the mouth pain causing difficulty in speaking?",
      "category": "speech_difficulty_with_mouth_sores",
  },
        ],
        'ulcer': [
            {
                'hi': "क्या मुँह के छाले लंबे समय से हैं?",
                'en': "Have the mouth ulcers been present for a long time?",
                'category': 'mouth_ulcer_duration'
            }
        ],
        'dryness': [
            {
                'hi': "क्या आपके मुँह में अक्सर सूखापन महसूस होता है?",
                'en': "Do you frequently feel dryness in your mouth?",
                'category': 'mouth_dryness_frequency'
            }
        ],
        'swelling': [
            {
                'hi': "क्या मुँह में सूजन के साथ दर्द या गर्मी भी महसूस हो रही है?",
                'en': "Is there pain or warmth along with the swelling in your mouth?",
                'category': 'mouth_swelling_signs'
            }
        ],
        'bleeding': [
            {
                'hi': "क्या मुँह से खून brushing या खाने के समय आता है?",
                'en': "Does your mouth bleed while brushing or eating?",
                'category': 'mouth_bleeding_trigger'
            }
        ],
        'bad breath': [
            {
                'hi': "क्या आपको लंबे समय से मुँह से दुर्गंध आ रही है?",
                'en': "Have you been experiencing bad breath for a long time?",
                'category': 'mouth_bad_breath_duration'
            }
        ],
        'numbness':[
            {
        'hi': "क्या सुन्नता आपके होंठों, जीभ या मुंह के अंदर किसी विशेष हिस्से में है?",
        'en': "Is the numbness in your lips, tongue, or a specific part inside the mouth?",
        'category': 'mouth_numbness_location'
    },
    {
        'hi': "क्या यह सुन्नता खाने या पीने के बाद महसूस होती है?",
        'en': "Does the numbness occur after eating or drinking?",
        'category': 'mouth_numbness_trigger_food'
    },
    {
        'hi': "क्या मुंह में सुन्नता के साथ जलन, झुनझुनी या कोई अजीब स्वाद भी महसूस होता है?",
        'en': "Do you feel burning, tingling, or an unusual taste along with the numbness in the mouth?",
        'category': 'mouth_numbness_sensation'
    },
        ],
	 'itching': [
            {
                'hi': "क्या मुंह में खुजली के साथ सूजन या जलन भी है?",
                'en': "Is the itching in your mouth accompanied by swelling or burning?",
                'category': 'mouth_itching_reaction'
            }
        ],
        'default': [
            {
                'hi': "कृपया अपने मुँह की समस्या के बारे में और जानकारी दें।",
                'en': "Please describe your mouth issue in more detail.",
                'category': 'mouth_detail'
            }
        ]
    },

'jaw': {
    'pain': [
        {
            'hi': "क्या जबड़े में दर्द चबाने या बोलने पर बढ़ता है?",
            'en': "Does the jaw pain worsen while chewing or speaking?",
            'category': 'jaw_pain_trigger'
        },
        {
      "hi": "क्या आप जबड़े के दर्द (तीव्र, सुस्त, धड़कन या दर्द) का वर्णन कर सकते हैं?",
      "en": "Can you describe the jaw pain (sharp, dull, throbbing, or aching)?",
      "category": "jaw pain",
    },
    {
      "hi": "क्या जबड़े का दर्द लगातार बना रहता है, या यह आता-जाता रहता है?",
      "en": "Is the jaw pain constant, or does it come and go?",
      "category": "jaw pain",
    },
    {
      "hi": "क्या दर्द चबाने, बोलने, या मुँह खोलने से बढ़ जाता है?",
      "en": "Does the pain worsen with chewing, speaking, or opening your mouth wide?",
      "category": "jaw pain",
    },
    {
      "hi": "क्या आपको अपने काटने या जबड़े की गति में कोई कठिनाई हो रही है?",
      "en": "Are you having any difficulty with your bite or jaw movement?",
      "category": "jaw pain",
    },
    {
      "hi": "क्या आप रात में अपने दांतों को पीसते हैं या जबड़े को दबाते हैं?",
      "en": "Do you grind your teeth or clench your jaw, especially at night?",
      "category": "jaw pain",
    },
    ],

    'swelling': [
        {
            'hi': "क्या सूजन के साथ जबड़े में जकड़न या गर्माहट है?",
            'en': "Is there tightness or warmth along with the swelling in the jaw?",
            'category': 'jaw_swelling_signs'
        }
    ],
    'injury': [
        {
            'hi': "क्या जबड़े में चोट किसी दुर्घटना, गिरावट या टक्कर से लगी थी?",
            'en': "Was the jaw injury caused by an accident, fall, or impact?",
            'category': 'jaw_injury_cause'
        }
    ],
    'default': [
        {
            'hi': "कृपया अपने जबड़े की समस्या के बारे में और जानकारी दें।",
            'en': "Please describe your jaw issue in more detail.",
            'category': 'jaw_detail'
        }
    ]
},

'period' : {
    'pain': [
        {
            'hi': "क्या आपकी मासिक धर्म के दौरान दर्द होता है?",
            'en': "Do you experience pain during your menstrual period?",
            'category': 'period_pain'
        },
          {
            "hi": "क्या आपकी माहवारी बहुत कम या हल्की होती है?",
            "en": "Is your menstrual flow very light or scanty?",
            "category": "menstruation",
            "symptom": "light periods",
            "risk_factor": False,
        },
    ],
    'delayed': [
            {
                'hi': "क्या आपकी माहवारी अनियमित रही है या पहले भी देर से आती रही है?",
                'en': "Have your periods been irregular or delayed in the past as well?",
                'category': 'period_delay_history'
            },
        ],
    'bleeding': [
        {
            'hi': "क्या आपकी मासिक धर्म में असामान्य रक्तस्राव होता है?",
            'en': "Do you have abnormal bleeding during your period?",
            'category': 'period_bleeding'
        },
          {
            "hi": "क्या आपकी माहवारी के समय थकान या कमजोरी महसूस होती है?",
            "en": "Do you feel fatigued or weak during your period?",
            "category": "menstruation",
            "symptom": "fatigue during menstruation",
            "risk_factor": False,
        },
        {
            "hi": "क्या आपकी माहवारी सामान्य से अधिक भारी होती है?",
            "en": "Is your menstrual flow heavier than usual?",
            "category": "menstruation",
            "symptom": "heavy menstrual bleeding",
            "risk_factor": False,
        },
    ],
    'default': [
        {
            'hi': "क्या यह आपकी मासिक धर्म से संबंधित समस्या है?",
            'en': "Is this related to your menstrual periods?",
            'category': 'confirm_period',
            'symptom': None
        }
    ]
  },
'hip': {
        'pain': [
            {
                'hi': "क्या कूल्हे में दर्द चलने या खड़े होने पर बढ़ता है?",
                'en': "Does the hip pain increase when walking or standing?",
                'category': 'hip_pain_activity'
            }
        ],
        'stiffness': [
            {
                'hi': "क्या सुबह उठने पर कूल्हे में जकड़न ज्यादा होती है?",
                'en': "Is the hip stiffness worse in the morning?",
                'category': 'hip_stiffness_morning'
            }
        ],
        'swelling': [
            {
                'hi': "क्या कूल्हे की सूजन के साथ गर्माहट या लालिमा भी है?",
                'en': "Is there warmth or redness along with the hip swelling?",
                'category': 'hip_swelling_inflammation'
            }
        ],
        'weakness': [
            {
                'hi': "क्या कूल्हे की कमजोरी के कारण आपको खड़ा होने या चलने में दिक्कत होती है?",
                'en': "Does hip weakness make it hard for you to stand or walk?",
                'category': 'hip_weakness_mobility'
            }
        ],
        'injury': [
            {
                'hi': "क्या हाल ही में कूल्हे में गिरावट या चोट लगी थी?",
                'en': "Did you recently have a fall or injury to the hip?",
                'category': 'hip_injury_recent'
            }
        ],
	'itching': [
            {
                'hi': "क्या कूल्हे में खुजली किसी खास कपड़े या रैश के कारण है?",
                'en': "Is the hip itching due to clothing or a rash?",
                'category': 'hip_itching_cause'
            }
        ],
        'default': [
            {
                'hi': "कृपया अपने कूल्हे की समस्या के बारे में और जानकारी दें।",
                'en': "Please describe your hip issue in more detail.",
                'category': 'hip_detail'
            }
        ]
    },
	
    'waist': {
        'pain': [
            {
                'hi': "क्या कमर का दर्द खड़े होने या चलने से बढ़ता है?",
                'en': "Does the waist pain increase when standing or walking?",
                'category': 'waist_pain_trigger'
            }
        ],
        'stiffness': [
            {
                'hi': "क्या कमर में जकड़न सुबह उठने पर ज़्यादा महसूस होती है?",
                'en': "Is the waist stiffness worse in the morning when you wake up?",
                'category': 'waist_stiffness_time'
            }
        ],
        'numbness': [
            {
                'hi': "क्या कमर का सुन्नपन पैर या जांघों तक फैलता है?",
                'en': "Does the numbness in your waist extend to your legs or thighs?",
                'category': 'waist_numbness_radiation'
            }
        ],
        'swelling': [
            {
                'hi': "क्या कमर की सूजन के साथ लालिमा या गर्मी भी है?",
                'en': "Is there redness or warmth with the swelling in your waist?",
                'category': 'waist_swelling_signs'
            }
        ],
        'injury': [
            {
                'hi': "क्या आपने किसी अचानक गतिविधि के दौरान कमर में चोट महसूस की?",
                'en': "Did the waist injury happen during a sudden movement or activity?",
                'category': 'waist_injury_cause'
            }
        ],
	'weakness': [
            {
        'hi': "क्या कमर की कमजोरी के कारण आपको खड़े होने या चलने में कठिनाई होती है?",
        'en': "Does weakness in your waist make it difficult to stand or walk?",
        'category': 'waist_weakness_function'
            }
        ],
        'itching': [
            {
                'hi': "क्या कमर में खुजली के साथ रैश या जलन भी हो रही है?",
                'en': "Is the itching on your waist accompanied by rash or burning?",
                'category': 'waist_itching_symptoms'
            }
        ],
        'default': [
            {
                'hi': "कृपया अपनी कमर की समस्या के बारे में और जानकारी दें।",
                'en': "Please describe your waist issue in more detail.",
                'category': 'waist_detail'
            }
        ]
    },

    'pelvic': {
        'pain': [
            {
                'hi': "क्या श्रोणि क्षेत्र में दर्द बैठने या पेशाब करते समय बढ़ता है?",
                'en': "Does the pelvic pain increase when sitting or during urination?",
                'category': 'pelvic_pain_triggers'
            }
        ],
        'stiffness': [
            {
                'hi': "क्या आपको श्रोणि क्षेत्र को हिलाने में कठिनाई होती है?",
                'en': "Do you find it difficult to move your pelvic area?",
                'category': 'pelvic_stiffness_mobility'
            }
        ],
        'swelling': [
            {
                'hi': "क्या श्रोणि क्षेत्र में सूजन के साथ गर्माहट या दबाव महसूस हो रहा है?",
                'en': "Is there warmth or a feeling of pressure along with swelling in the pelvic area?",
                'category': 'pelvic_swelling_signs'
            }
        ],
        'weakness': [
            {
                'hi': "क्या श्रोणि की कमजोरी के कारण आपको खड़े होने में परेशानी होती है?",
                'en': "Does pelvic weakness make it hard for you to stand?",
                'category': 'pelvic_weakness_function'
            }
        ],
        'injury': [
            {
                'hi': "क्या हाल ही में आपके श्रोणि क्षेत्र में कोई चोट या गिरावट हुई है?",
                'en': "Did you recently have a fall or injury to your pelvic area?",
                'category': 'pelvic_injury_recent'
            }
        ],
	'numbness': [
            {
                'hi': "क्या पेल्विक क्षेत्र का सुन्नपन पैरों तक फैलता है?",
                'en': "Does the numbness in your pelvic area extend to the legs?",
                'category': 'pelvic_numbness_distribution'
            }
        ],
	'itching': [
            {
                'hi': "क्या पेल्विक क्षेत्र की खुजली के साथ जलन या रिसाव भी है?",
                'en': "Is the itching in the pelvic area accompanied by burning or discharge?",
                'category': 'pelvic_itching_accompanied'
            }
        ],
        'default': [
            {
                'hi': "कृपया अपने श्रोणि क्षेत्र की समस्या के बारे में और जानकारी दें।",
                'en': "Please describe your pelvic issue in more detail.",
                'category': 'pelvic_detail'
            }
        ]
},

    'elbow': {
        'pain': [
            {
                'hi': "क्या कोहनी में दर्द कुछ उठाने या मोड़ने पर बढ़ता है?",
                'en': "Does the elbow pain increase when lifting or bending?",
                'category': 'elbow_pain_movement'
            }
        ],
        'stiffness': [
            {
                'hi': "क्या सुबह उठने पर कोहनी में जकड़न महसूस होती है?",
                'en': "Do you feel stiffness in the elbow after waking up in the morning?",
                'category': 'elbow_stiffness_morning'
            }
        ],
        'swelling': [
            {
                'hi': "क्या कोहनी की सूजन के साथ गर्माहट या लालिमा भी है?",
                'en': "Is there warmth or redness along with swelling in the elbow?",
                'category': 'elbow_swelling_signs'
            }
        ],
        'weakness': [
            {
                'hi': "क्या कोहनी की कमजोरी के कारण आपको चीजें उठाने में दिक्कत होती है?",
                'en': "Is it difficult to lift things due to weakness in your elbow?",
                'category': 'elbow_weakness_function'
            }
        ],
        'injury': [
            {
                'hi': "क्या आपने हाल ही में कोहनी में चोट या गिरावट का अनुभव किया है?",
                'en': "Did you recently experience an injury or fall affecting your elbow?",
                'category': 'elbow_injury_recent'
            }
        ],
        'default': [
            {
                'hi': "कृपया अपनी कोहनी की समस्या के बारे में और जानकारी दें।",
                'en': "Please describe your elbow issue in more detail.",
                'category': 'elbow_detail'
            }
        ]
},

    'calf': {
        'pain': [
            {
                'hi': "क्या बछड़े में दर्द चलने या खड़े होने पर बढ़ता है?",
                'en': "Does the calf pain increase when walking or standing?",
                'category': 'calf_pain_activity'
            }
        ],
        'spasm': [
            {
                'hi': "क्या बछड़े में ऐंठन या मरोड़ अक्सर हो रही है?",
                'en': "Are the calf spasms or cramps happening frequently?",
                'category': 'calf_spasm_frequency'
            }
        ],
        'swelling': [
            {
                'hi': "क्या बछड़े में सूजन के साथ गर्माहट या लालिमा भी है?",
                'en': "Is there warmth or redness along with the swelling in the calf?",
                'category': 'calf_swelling_signs'
            }
        ],
        'weakness': [
            {
                'hi': "क्या बछड़े की कमजोरी के कारण आपको खड़े रहने या चलने में परेशानी होती है?",
                'en': "Does calf weakness make it hard for you to stand or walk?",
                'category': 'calf_weakness_function'
            }
        ],
        'injury': [
            {
                'hi': "क्या बछड़े में हाल ही में कोई चोट या खिंचाव हुआ है?",
                'en': "Did you recently have any injury or strain in your calf?",
                'category': 'calf_injury_recent'
            }
        ],
        'default': [
            {
                'hi': "कृपया अपने बछड़े की समस्या के बारे में और जानकारी दें।",
                'en': "Please describe your calf issue in more detail.",
                'category': 'calf_detail'
            }
        ]
    },
'face': {
        'pain': [
            {
                'hi': "क्या चेहरे का दर्द किसी विशेष स्थान पर केंद्रित है?",
                'en': "Is the facial pain localized to a specific area?",
                'category': 'face_pain_location'
            }
        ],
        'numbness': [
            {
                'hi': "क्या चेहरे का सुन्नपन अचानक शुरू हुआ?",
                'en': "Did the facial numbness start suddenly?",
                'category': 'face_numbness_onset'
            }
        ],
        'swelling': [
            {
               'hi': "क्या चेहरे की सूजन के साथ दर्द भी है?",
               'en': "Is there pain along with the facial swelling?",
               'category': 'face_swelling_signs'
           }

        ],
        'drooping': [
            {
                'hi': "क्या आपके चेहरे का एक हिस्सा झुक गया है या मुस्कान असमान है?",
                'en': "Is one side of your face drooping or is your smile uneven?",
                'category': 'face_drooping_sign'
            }
        ],
        'injury': [
            {
                'hi': "क्या आपको हाल ही में चेहरे पर कोई चोट लगी है?",
                'en': "Have you recently had any injury to your face?",
                'category': 'face_injury_recent'
            }
        ],
	'itching': [
            {
                'hi': "क्या चेहरे में खुजली किसी क्रीम या साबुन के इस्तेमाल के बाद हुई?",
                'en': "Did the facial itching start after using any cream or soap?",
                'category': 'face_itching_trigger'
            }
        ],
        'default': [
            {
                'hi': "कृपया अपने चेहरे की समस्या के बारे में और जानकारी दें।",
                'en': "Please describe your facial issue in more detail.",
                'category': 'face_detail'
            }
        ]
    },
'ankle': {
        'pain': [
            {
                'hi': "क्या टखने में दर्द चलते समय बढ़ता है?",
                'en': "Does ankle pain get worse while walking?",
                'category': 'ankle_pain_activity'
            }
        ],
        'swelling': [
            {
                'hi': "क्या टखने में सूजन के साथ लालिमा या गर्मी महसूस हो रही है?",
                'en': "Is there redness or warmth with the ankle swelling?",
                'category': 'ankle_swelling_signs'
            }
        ],
        'stiffness': [
            {
                'hi': "क्या सुबह उठने पर टखना कड़ा महसूस होता है?",
                'en': "Does your ankle feel stiff in the morning?",
                'category': 'ankle_stiffness_morning'
            }
        ],
        'injury': [
            {
                'hi': "क्या आपने हाल ही में टखना मोड़ लिया या गिर गए?",
                'en': "Did you recently twist your ankle or fall?",
                'category': 'ankle_injury_cause'
            }
        ],
        'weakness': [
            {
                'hi': "क्या आपका टखना चलते समय अचानक मुड़ जाता है या लड़खड़ाता है?",
                'en': "Does your ankle give out or wobble while walking?",
                'category': 'ankle_weakness_instability'
            }
        ],
        'default': [
            {
                'hi': "कृपया अपने टखने की समस्या के बारे में और जानकारी दें।",
                'en': "Please describe your ankle issue in more detail.",
                'category': 'ankle_detail'
            }
        ]
    },
'body': {
        'pain': [
            {
                'hi': "क्या पूरे शरीर में दर्द लगातार बना रहता है?",
                'en': "Is the body-wide pain constant?",
                'category': 'body_pain_duration'
            }
        ],
        'fatigue': [
            {
                'hi': "क्या थकान के साथ नींद भी पूरी नहीं हो रही है?",
                'en': "Are you feeling fatigued even after a full night's sleep?",
                'category': 'body_fatigue_sleep'
            }
        ],
        'weakness': [
            {
                'hi': "क्या कमजोरी के कारण रोज़मर्रा के कामों में दिक्कत हो रही है?",
                'en': "Is the weakness affecting your daily activities?",
                'category': 'body_weakness_function'
            }
        ],
        'stiffness': [
            {
                'hi': "क्या सुबह उठने पर पूरे शरीर में जकड़न महसूस होती है?",
                'en': "Do you feel stiffness throughout your body in the morning?",
                'category': 'body_stiffness_morning'
            }
        ],
	'itching': [
        {
            'hi': "क्या पूरे शरीर में खुजली लगातार हो रही है या रुक-रुक कर?",
            'en': "Is the itching happening constantly or intermittently across the body?",
            'category': 'body_itching_pattern'
        }
    ],
    'swelling': [
        {
            'hi': "क्या शरीर की सूजन किसी विशेष हिस्से में सीमित है या पूरे शरीर में फैली हुई है?",
            'en': "Is the swelling limited to one area or spread across the whole body?",
            'category': 'body_swelling_area'
        }
    ],
        'default': [
            {
                'hi': "कृपया अपने शरीर की समस्या के बारे में और जानकारी दें।",
                'en': "Please describe your body issue in more detail.",
                'category': 'body_detail'
            }
        ]
    },
'hair': {
        'hair loss': [
            {
                'hi': "क्या आपके बाल झड़ने का कोई विशेष कारण है जैसे तनाव या हार्मोन?",
                'en': "Is there a specific reason for your hair loss such as stress or hormones?",
                'category': 'hair_loss_cause'
            }
        ],
        'dandruff': [
            {
                'hi': "क्या सिर में खुजली के साथ-साथ रूसी भी हो रही है?",
                'en': "Is dandruff accompanied by itching on the scalp?",
                'category': 'hair_dandruff_itching'
            }
        ],
        'itching': [
            {
                'hi': "क्या यह खुजली हर समय बनी रहती है या कुछ समय में होती है?",
                'en': "Is the itching constant or does it occur occasionally?",
                'category': 'hair_itching_frequency'
            }
        ],
        'greying': [
            {
                'hi': "क्या बालों का सफेद होना उम्र से पहले शुरू हुआ?",
                'en': "Has the greying of your hair started prematurely?",
                'category': 'hair_greying_age'
            }
        ],
        'dryness': [
            {
                'hi': "क्या आपके बालों में रूखापन मौसम या किसी उत्पाद के कारण है?",
                'en': "Is the dryness in your hair due to weather or any hair products?",
                'category': 'hair_dryness_cause'
            }
        ],
        'default': [
            {
                'hi': "कृपया अपने बालों की समस्या के बारे में और जानकारी दें।",
                'en': "Please describe your hair issue in more detail.",
                'category': 'hair_detail'
            }
        ]
    },
'finger': {
        'pain': [
            {
                'hi': "क्या उंगली का दर्द किसी विशेष गतिविधि के दौरान बढ़ता है?",
                'en': "Does the finger pain increase during any specific activity?",
                'category': 'finger_pain_activity'
            }
        ],
        'numbness': [
            {
                'hi': "क्या उंगली में सुन्नपन लगातार बना रहता है या आता-जाता है?",
                'en': "Is the numbness in the finger constant or does it come and go?",
                'category': 'finger_numbness_pattern'
            }
        ],
        'swelling': [
            {
                'hi': "क्या सूजन के साथ दर्द, गर्माहट या लालिमा भी है?",
                'en': "Is there pain, warmth, or redness along with the swelling?",
                'category': 'finger_swelling_signs'
            }
        ],
        'stiffness': [
            {
                'hi': "क्या सुबह के समय उंगली में जकड़न ज्यादा होती है?",
                'en': "Is the stiffness in your finger worse in the morning?",
                'category': 'finger_stiffness_timing'
            }
        ],
        'injury': [
            {
                'hi': "क्या उंगली में हाल ही में कोई चोट या झटका लगा है?",
                'en': "Did you recently injure or bump your finger?",
                'category': 'finger_injury_event'
            }
        ],
	'freeze': [
            {
                'hi': "क्या ठंड में आपकी उंगलियाँ सुन्न या बहुत ठंडी हो जाती हैं?",
                'en': "Do your fingers feel numb or very cold in cold weather?",
                'category': 'finger_freezing_cold_sensitivity'
            }
        ],
	'itching': [
            {
                'hi': "क्या उंगलियों में खुजली के साथ त्वचा फट रही है या सूजन है?",
                'en': "Is the finger itching accompanied by cracked skin or swelling?",
                'category': 'finger_itching_condition'
            }
        ],
        'default': [
            {
                'hi': "कृपया अपनी उंगली की समस्या के बारे में और जानकारी दें।",
                'en': "Please describe your finger issue in more detail.",
                'category': 'finger_detail'
            }
        ]
    },
'thumb': {
        'pain': [
            {
                'hi': "क्या अंगूठे में दर्द पकड़ने या किसी चीज़ को पकड़ने पर बढ़ता है?",
                'en': "Does thumb pain increase when gripping or holding something?",
                'category': 'thumb_pain_grip'
            }
        ],
        'swelling': [
            {
                'hi': "क्या अंगूठे की सूजन के साथ गर्माहट या लालिमा भी है?",
                'en': "Is there warmth or redness along with the swelling in your thumb?",
                'category': 'thumb_swelling_signs'
            }
        ],
        'stiffness': [
            {
                'hi': "क्या सुबह के समय अंगूठे में जकड़न अधिक होती है?",
                'en': "Is thumb stiffness worse in the morning?",
                'category': 'thumb_stiffness_timing'
            }
        ],
        'numbness': [
            {
                'hi': "क्या अंगूठे में सुन्नपन कभी-कभी होता है या लगातार बना रहता है?",
                'en': "Is the numbness in your thumb occasional or constant?",
                'category': 'thumb_numbness_pattern'
            }
        ],
        'injury': [
            {
                'hi': "क्या हाल ही में अंगूठे में कोई चोट या मोच आई है?",
                'en': "Did you recently injure or sprain your thumb?",
                'category': 'thumb_injury_event'
            }
        ],
        'default': [
            {
                'hi': "कृपया अपने अंगूठे की समस्या के बारे में और जानकारी दें।",
                'en': "Please describe your thumb issue in more detail.",
                'category': 'thumb_detail'
            }
        ]
    },
'palm': {
        'pain': [
            {
                'hi': "क्या हथेली में दर्द किसी चीज़ को पकड़ते समय बढ़ता है?",
                'en': "Does the palm pain increase when gripping something?",
                'category': 'palm_pain_grip'
            }
        ],
        'numbness': [
            {
                'hi': "क्या हथेली में झुनझुनी या सुन्नपन रात के समय ज्यादा होता है?",
                'en': "Is the numbness or tingling in your palm worse at night?",
                'category': 'palm_numbness_timing'
            }
        ],
        'swelling': [
            {
                'hi': "क्या हथेली में सूजन के साथ लालिमा या गर्माहट भी है?",
                'en': "Is there redness or warmth along with swelling in your palm?",
                'category': 'palm_swelling_signs'
            }
        ],
        'stiffness': [
            {
                'hi': "क्या हथेली की जकड़न के कारण उंगलियां मोड़ने में दिक्कत होती है?",
                'en': "Is the palm stiffness making it hard to bend your fingers?",
                'category': 'palm_stiffness_flexibility'
            }
        ],
        'injury': [
            {
                'hi': "क्या आपकी हथेली पर हाल ही में कोई चोट, जलन या कट हुआ है?",
                'en': "Have you recently had a cut, burn, or injury on your palm?",
                'category': 'palm_injury_event'
            }
        ],
        'default': [
            {
                'hi': "कृपया अपनी हथेली की समस्या के बारे में और जानकारी दें।",
                'en': "Please describe your palm issue in more detail.",
                'category': 'palm_detail'
            }
        ]
    },
'toe': {
        'pain': [
            {
                'hi': "क्या पैर की उंगली का दर्द चलने या दौड़ने से बढ़ता है?",
                'en': "Does the toe pain worsen when walking or running?",
                'category': 'toe_pain_activity'
            }
        ],
        'numbness': [
            {
                'hi': "क्या पैर की उंगली में सुन्नपन लगातार रहता है या कभी-कभी होता है?",
                'en': "Is the numbness in the toe constant or occasional?",
                'category': 'toe_numbness_pattern'
            }
        ],
        'swelling': [
            {
                'hi': "क्या सूजन के साथ पैर की उंगली में दर्द या गर्माहट है?",
                'en': "Is there pain or warmth along with the swelling in the toe?",
                'category': 'toe_swelling_signs'
            }
        ],
        'stiffness': [
            {
                'hi': "क्या सुबह के समय पैर की उंगली में जकड़न ज्यादा महसूस होती है?",
                'en': "Is the stiffness in your toe worse in the morning?",
                'category': 'toe_stiffness_timing'
            }
        ],
        'injury': [
            {
                'hi': "क्या हाल ही में पैर की उंगली में चोट लगी थी या टकराई थी?",
                'en': "Did you recently injure or stub your toe?",
                'category': 'toe_injury_event'
            }
        ],
        'freeze': [
            {
                'hi': "क्या ठंड में आपकी पैर की उंगलियाँ सुन्न या बहुत ठंडी हो जाती हैं?",
                'en': "Do your toes feel numb or extremely cold in cold weather?",
                'category': 'toe_freezing_cold_sensitivity'
            }
        ],
        'default': [
            {
                'hi': "कृपया अपनी पैर की उंगली की समस्या के बारे में और जानकारी दें।",
                'en': "Please describe your toe issue in more detail.",
                'category': 'toe_detail'
            }
        ]
    },

'heel': {
        'pain': [
            {
                'hi': "क्या एड़ी में दर्द सुबह उठने पर अधिक होता है?",
                'en': "Is your heel pain worse when you get up in the morning?",
                'category': 'heel_pain_morning'
            }
        ],
        'swelling': [
            {
                'hi': "क्या एड़ी पर सूजन के साथ लालिमा या गर्माहट है?",
                'en': "Is there redness or warmth with the heel swelling?",
                'category': 'heel_swelling_signs'
            }
        ],
        'stiffness': [
            {
                'hi': "क्या एड़ी जकड़ी हुई या चलने में कठिनाई होती है?",
                'en': "Does your heel feel stiff or make walking difficult?",
                'category': 'heel_stiffness_difficulty'
            }
        ],
        'injury': [
            {
                'hi': "क्या हाल ही में आपकी एड़ी में कोई चोट लगी है?",
                'en': "Have you recently injured your heel?",
                'category': 'heel_injury_recent'
            }
        ],
        'numbness': [
            {
                'hi': "क्या एड़ी में सुन्नपन या झनझनाहट महसूस होती है?",
                'en': "Do you feel numbness or tingling in your heel?",
                'category': 'heel_numbness_sensation'
            }
        ],
        'default': [
            {
                'hi': "कृपया अपनी एड़ी की समस्या के बारे में और जानकारी दें।",
                'en': "Please describe your heel issue in more detail.",
                'category': 'heel_detail'
            }
        ]
    },
'lip': {
    'pain': [
        {
            'hi': "क्या होंठों में जलन या तीव्र दर्द हो रहा है?",
            'en': "Are you experiencing burning or sharp pain in the lips?",
            'category': 'lip_pain_burning'
        }
    ],
    'swelling': [
        {
            'hi': "क्या होंठों की सूजन अचानक से हुई या किसी एलर्जी के कारण है?",
            'en': "Did the lip swelling happen suddenly or due to an allergy?",
            'category': 'lip_swelling_allergy'
        }
    ],
    'dryness': [
        {
            'hi': "क्या होंठ लगातार फटते या सूखते रहते हैं?",
            'en': "Are your lips constantly dry or cracking?",
            'category': 'lip_dryness_chronic'
        }
    ],
    'numbness': [
        {
            'hi': "क्या होंठों में सुन्नपन या झनझनाहट महसूस हो रही है?",
            'en': "Do you feel numbness or tingling in your lips?",
            'category': 'lip_numbness_sensation'
        }
    ],
    'ulcers': [
        {
            'hi': "क्या होंठों पर छाले या घाव हैं?",
            'en': "Do you have ulcers or sores on your lips?",
            'category': 'lip_ulcers_visible'
        }
    ],
    'default': [
        {
            'hi': "कृपया अपने होंठों की समस्या के बारे में और जानकारी दें।",
            'en': "Please describe your lip issue in more detail.",
            'category': 'lip_detail'
        }
    ]
},
'cheek': {
    'pain': [
        {
            'hi': "क्या गाल में दर्द लगातार बना रहता है या छूने से बढ़ता है?",
            'en': "Is the cheek pain constant or does it increase when touched?",
            'category': 'cheek_pain_touch_sensitive'
        }
    ],
    'swelling': [
        {
            'hi': "क्या गाल में सूजन के साथ बुखार या गर्माहट भी है?",
            'en': "Is the swelling in the cheek accompanied by fever or warmth?",
            'category': 'cheek_swelling_fever'
        }
    ],
    'numbness': [
        {
            'hi': "क्या गाल में सुन्नपन या झनझनाहट महसूस होती है?",
            'en': "Do you feel numbness or tingling in your cheek?",
            'category': 'cheek_numbness_sensation'
        }
    ],
    'redness': [
        {
            'hi': "क्या गाल में लालिमा अचानक से हुई है या जलन महसूस होती है?",
            'en': "Is the redness in your cheek sudden or does it feel like burning?",
            'category': 'cheek_redness_burning'
        }
    ],
    'injury': [
        {
            'hi': "क्या आपके गाल पर हाल ही में कोई चोट लगी है?",
            'en': "Did you recently suffer any injury to your cheek?",
            'category': 'cheek_injury_recent'
        }
    ],
    'default': [
        {
            'hi': "कृपया अपने गाल की समस्या के बारे में और जानकारी दें।",
            'en': "Please describe your cheek issue in more detail.",
            'category': 'cheek_detail'
        }
    ]
},
'chin': {
    'pain': [
        {
            'hi': "क्या ठोड़ी में दर्द चबाने या बोलने पर बढ़ता है?",
            'en': "Does the chin pain increase while chewing or talking?",
            'category': 'chin_pain_activity'
        }
    ],
    'swelling': [
        {
            'hi': "क्या ठोड़ी की सूजन के साथ बुखार या लालिमा है?",
            'en': "Is the chin swelling accompanied by fever or redness?",
            'category': 'chin_swelling_fever'
        }
    ],
    'numbness': [
        {
            'hi': "क्या ठोड़ी में सुन्नपन या झनझनाहट महसूस हो रही है?",
            'en': "Do you feel numbness or tingling in your chin?",
            'category': 'chin_numbness_sensation'
        }
    ],
    'injury': [
        {
            'hi': "क्या आपने हाल ही में ठोड़ी पर चोट लगाई है?",
            'en': "Did you recently injure your chin?",
            'category': 'chin_injury_recent'
        }
    ],
    'lump': [
        {
            'hi': "क्या आपकी ठोड़ी पर कोई गांठ या उभार है?",
            'en': "Is there a lump or bump on your chin?",
            'category': 'chin_lump_present'
        }
    ],
    'default': [
        {
            'hi': "कृपया अपनी ठोड़ी की समस्या के बारे में और जानकारी दें।",
            'en': "Please describe your chin issue in more detail.",
            'category': 'chin_detail'
        }
    ]
},
'soles': {
    'pain': [
        {
            'hi': "क्या तलवों में दर्द सुबह उठने पर या चलने पर बढ़ता है?",
            'en': "Is the pain in your soles worse in the morning or while walking?",
            'category': 'soles_pain_morning_walk'
        }
    ],
    'swelling': [
        {
            'hi': "क्या तलवों में सूजन के साथ गर्मी या लालिमा भी है?",
            'en': "Is there warmth or redness along with swelling in the soles?",
            'category': 'soles_swelling_inflammation'
        }
    ],
    'numbness': [
        {
            'hi': "क्या आपके तलवे सुन्न हो जाते हैं या उनमें झनझनाहट होती है?",
            'en': "Do your soles feel numb or have a tingling sensation?",
            'category': 'soles_numbness_sensation'
        }
    ],
    'cracks': [
        {
            'hi': "क्या आपके तलवे फट रहे हैं या सूखे हैं?",
            'en': "Are the soles of your feet cracked or dry?",
            'category': 'soles_cracks_dryness'
        }
    ],
    'itching': [
        {
            'hi': "क्या तलवों में खुजली या जलन हो रही है?",
            'en': "Do you have itching or burning in the soles?",
            'category': 'soles_itching_irritation'
        }
    ],
    'default': [
        {
            'hi': "कृपया अपने तलवों की समस्या के बारे में और जानकारी दें।",
            'en': "Please describe your sole-related issue in more detail.",
            'category': 'soles_detail'
        }
    ]
},
'fingertip': {
    'pain': [
        {
            'hi': "क्या उंगली के सिरे में तेज़ या जलन जैसा दर्द है?",
            'en': "Is the pain in your fingertip sharp or burning?",
            'category': 'fingertip_pain_burning'
        }
    ],
    'numbness': [
        {
            'hi': "क्या उंगली के सिरे में सुन्नपन या झनझनाहट महसूस हो रही है?",
            'en': "Do you feel numbness or tingling in your fingertip?",
            'category': 'fingertip_numbness_sensation'
        }
    ],
    'swelling': [
        {
            'hi': "क्या उंगली के सिरे में सूजन के साथ लालिमा या गर्मी है?",
            'en': "Is there swelling along with redness or warmth in the fingertip?",
            'category': 'fingertip_swelling_inflammation'
        }
    ],
    'injury': [
        {
            'hi': "क्या आपकी उंगली के सिरे पर हाल ही में चोट लगी है?",
            'en': "Did you recently injure the tip of your finger?",
            'category': 'fingertip_injury_recent'
        }
    ],
    'discoloration': [
        {
            'hi': "क्या उंगली का सिरा नीला, काला या पीला हो गया है?",
            'en': "Has the fingertip turned blue, black, or pale?",
            'category': 'fingertip_discoloration_color_change'
        }
    ],
    'default': [
        {
            'hi': "कृपया अपनी उंगली के सिरे की समस्या के बारे में और जानकारी दें।",
            'en': "Please describe your fingertip issue in more detail.",
            'category': 'fingertip_detail'
        }
    ]
},

'child' : {
    'pain': [
        {
            'hi': "क्या आपका बच्चा दर्द से रोता है? क्या यह बच्चे के लिए असहनीय है?",
            'en': "Does your child cry with pain? Is it unbearable for the child",
            'category': 'child_pain'
        }
    ],
    'bleeding': [
        {
            'hi': "क्या बच्चे को भारी रक्तस्राव हो रहा है?",
            'en': "Does the child have heavy bleeding?",
            'category': 'child_bleeding'
        }
    ],
    'default': [
        {
            'hi': "क्या आपका बच्चा इन समस्याओं का सामना कर रहा है?",
            'en': "Is your child facing the issues?",
            'category': 'confirm_child',
            'symptom': None
        }
    ]
  },

}

# -----------------------------------------------------------------
# Map lone body parts → default specialists (used if NO symptoms)
# -----------------------------------------------------------------
body_part_to_specialist = {
    'tooth': 'Dentist',
    'teeth': 'Dentist',
    'tooths': 'Dentist',
    'mouth': 'Dentist',
    'tongue': 'Dentist',
    'lip': 'Dentist',
    'lips': 'Dentist',
    'cheek': 'Dentist',
    'cheeks': 'Dentist',
    'chin': 'Dentist',
    'oral': 'Dentist',
    'buccal': 'Dentist',
    'eye': 'Ophthalmologist',
    'eyes': 'Ophthalmologist',
    'ocular': 'Ophthalmologist',
    'ear': 'E N T Specialist',
    'ears': 'E N T Specialist',
    'otologic': 'E N T Specialist',
    'nose': 'E N T Specialist',
    'nasal': 'E N T Specialist',
    'throat': 'E N T Specialist',
    'pharyngeal': 'E N T Specialist',
    'laryngeal': 'E N T Specialist',
    'skin': 'Dermatologist',
    'nail': 'Dermatologist',
    'nails': 'Dermatologist',
    'head': 'Neurologist',
    'forehead': 'Neurologist',
    'cranial': 'Neurologist',
    'trigeminal': 'Neurologist',
    'facial': 'General Practitioner',
    'face' : 'General Practitioner',
    'neck': 'Orthopedic Specialist',
    'back': 'Orthopedic Specialist',
    'spinal': 'Orthopedic Specialist',
    'lumbar': 'Orthopedic Specialist',
    'thoracic': 'Orthopedic Specialist',
    'cervical': 'Orthopedic Specialist',
    'arm': 'Orthopedic Specialist',
    'arms': 'Orthopedic Specialist',
    'hand': 'Orthopedic Specialist',
    'hands': 'Orthopedic Specialist',
    'finger': 'Orthopedic Specialist',
    'fingers': 'Orthopedic Specialist',
    'thumb': 'Orthopedic Specialist',
    'thumbs': 'Orthopedic Specialist',
    'wrist': 'Orthopedic Specialist',
    'wrists': 'Orthopedic Specialist',
    'elbow': 'Orthopedic Specialist',
    'elbows': 'Orthopedic Specialist',
    'shoulder': 'Orthopedic Specialist',
    'shoulders': 'Orthopedic Specialist',
    'leg': 'Orthopedic Specialist',
    'legs': 'Orthopedic Specialist',
    'knee': 'Orthopedic Specialist',
    'knees': 'Orthopedic Specialist',
    'foot': 'Orthopedic Specialist',
    'foots': 'Orthopedic Specialist',  # included typo variant
    'feet': 'Orthopedic Specialist',   # common plural
    'ankle': 'Orthopedic Specialist',
    'ankles': 'Orthopedic Specialist',
    'heel': 'Orthopedic Specialist',
    'heels': 'Orthopedic Specialist',
    'toe': 'Orthopedic Specialist',
    'toes': 'Orthopedic Specialist',
    'palm': 'Orthopedic Specialist',
    'palms': 'Orthopedic Specialist',
    'fingertip': 'Orthopedic Specialist',
    'fingertips': 'Orthopedic Specialist',
    'instep': 'Orthopedic Specialist',
    'calf': 'Orthopedic Specialist',
    'shin': 'Orthopedic Specialist',
    'joint': 'Orthopedic Specialist',
    'joints': 'Orthopedic Specialist',
    'bone': 'Orthopedic Specialist',
    'bones': 'Orthopedic Specialist',
    'chest': 'Pulmonologist',
    'respiratory': 'Pulmonologist',
    'pulmonary': 'Pulmonologist',
    'cardiac': 'Cardiologist',
    'heart': 'Cardiologist',
    'stomach': 'Gastroenterologist',
    'abdomen': 'Gastroenterologist',
    'abdominal': 'Gastroenterologist',
    'gastrointestinal': 'Gastroenterologist',
    'digestive': 'Gastroenterologist',
    'biliary': 'Gastroenterologist',
    'rectal': 'Gastroenterologist',
    'liver': 'Hepatologist',
    'hepatic': 'Hepatologist',
    'renal': 'Nephrologist',
    'urinary': 'Urologist',
    'genital': 'Gynecologist',
    'soles': 'Podiatrist',
    'visceral': 'General Surgeon',
    'peripheral': 'Neurologist',
    'jaw': 'Dentist',
    'period pain':'Gynecologist',
    'period bleeding':'Gynecologist',
    'period issue': 'Gynecologist',
    'period':'Gynecologist',
}

BP_CANON = {
    'teeth':      'tooth',
    'tooth':      'tooth',
    'molars':     'tooth',
    'feet':       'foot',
    'foot':       'foot',
    'eyes':       'eye',
    'eye':        'eye',
    'ears':       'ear',
    'ear':        'ear',
    'toes': 'toes',
     'toe': 'toes',
     'legs':'leg',
    'leg':'leg',
   'shoulders':'shoulder',
   'knees':'knee',
   'lips':'lip',
   'hands':'hand',
   'wrists':'wrist',
   'thighs':'thigh',
   'periods' : 'period',
    'menstrual' : 'period',
    'muscles':'muscle',
    'arms':'arm',
    'palms': 'palm',
    'thumbs': 'thumb',
     'bones': 'bone',
     'sole': 'soles',
     'belly': 'stomach',
     'abdomen':'stomach',
     'abdominal':'stomach',
     'tummy': 'stomach',
     'gut': 'stomach',
     'joints':'joint',
     'ankles':'ankle',
     'hips':'hip',
     'jaws':'jaw',
     'hairs':'hair',
     'nails':'nail',
     'heels':'heel',
     'waists':'waist',
     'fingers':'finger',
     'fingertips':'fingertip',
     'children' : 'child',
     'kid' : 'child',
     'kids' : 'child',
     'baby' : 'child',
     'babies' : 'child',
     'son' : 'child',
     'daughter' : 'child',
     'nephew' : 'child',
     'niece' : 'child',
     'cheeks': 'cheek',
     'palms': 'palm',
     'toes': 'toe',
     'calves':'calf'
      
    # …and so on for all body parts
}

body_parts = [
    'leg','legs', 'eye','eyes', 'hand','hands', 'arm','arms', 'head', 'back', 'chest', 'wrist','wrists', 'throat', 'stomach',
    'neck', 'knee','knees', 'foot','foots', 'shoulder', 'shoulders', 'ear', 'ears','nail' , 'nails', 'bone','bones', 'joint','joints', 'skin','abdomen',
    'mouth', 'nose', 'tooth', 'tooths', 'teeth', 'tongue','lip', 'lips', 'cheek','cheeks', 'chin', 'forehead','thigh', 'thighs',
    'elbow', 'elbows','ankle','ankles', 'heel', 'heels', 'toe', 'toes','finger','fingers', 'thumb', 'thumbs', 'palm','palms', 'soles', 'sole',
    'fingertip', 'fingertips', 'instep', 'calf', 'shin','lumbar', 'thoracic', 'cervical', 'gastrointestinal', 'abdominal', 'rectal', 'genital',
    'urinary', 'respiratory', 'cardiac', 'pulmonary', 'digestive', 'cranial', 'facial', 'face', 'hair', 'hairs',
    'ocular', 'otologic', 'nasal', 'oral', 'buccal', 'lingual', 'pharyngeal', 'laryngeal', 'heart',
    'trigeminal', 'spinal', 'peripheral', 'visceral', 'biliary', 'renal', 'hepatic','period','jaw','hip','waist', 'pelvic','body','child'
] 

symptom_to_specialist = {
    # Nephrologist: Kidney-related symptoms
    'kidney issue': 'Nephrologist',
    'dark urine': 'Urologist',
    'blood in urine': 'Urologist',
    'frequent urination': 'Urologist',

    # Gynecologist: Female-specific, pregnancy, and cesarean symptoms
    'female issue': 'Gynecologist',
    'caesarean section': 'Gynecologist',
    'pregnancy': 'Gynecologist',

    # Dentist: Dental-related symptoms
    'tooth pain': 'Dentist',
    'mouth pain': 'Dentist',
    'dry mouth': 'Dentist',

    # Neurologist: Neurological and brain-related symptoms
    'dizziness': 'Neurologist',
    'weakness': 'General Practitioner',
    'numbness': 'Neurologist',
    'confusion': 'Neurologist',
    'memory loss': 'Neurologist',
    'difficulty speaking': 'Neurologist',
    'seizures': 'Neurologist',
    'tremor': 'Neurologist',
    'balance problem': 'Neurologist',
    'headache': 'General Practitioner',
    'migraine': 'Neurologist',

    # Dermatologist: Skin-related symptoms
    'rash': 'Dermatologist',
    'itching': 'Dermatologist',
    'acne': 'Dermatologist',
    'skin burning': 'Dermatologist',
    'hair loss': 'Dermatologist',

    # Orthopedic Specialist: Musculoskeletal symptoms
    'back spasm': 'Orthopedic Specialist',
    'back pain': 'Orthopedic Specialist',
    'joint pain': 'Orthopedic Specialist',
    'muscle pain': 'Orthopedic Specialist',
    'bone pain': 'Orthopedic Specialist',
    'wrist pain': 'Orthopedic Specialist',
    'sprain': 'Orthopedic Specialist',
    'strain': 'Orthopedic Specialist',
    'arthritis': 'Orthopedic Specialist',
    'gout': 'Orthopedic Specialist',
    'neck pain': 'Orthopedic Specialist',
    'leg pain': 'Orthopedic Specialist',
    'hand pain': 'Orthopedic Specialist',
    'arm pain': 'Orthopedic Specialist',
    'foot pain': 'Orthopedic Specialist',
    'knee pain': 'Orthopedic Specialist',
    'shoulder pain': 'Orthopedic Specialist',
    'hip pain': 'Orthopedic Specialist',
    'waist pain': 'Orthopedic Specialist',
    'thigh pain': 'Orthopedic Specialist',
    'pelvic pain': 'Orthopedic Specialist',
    'elbow pain': 'Orthopedic Specialist',
    'calf pain': 'Orthopedic Specialist',
    'bone fracture': 'Orthopedic Specialist',
    'back bone issue': 'Orthopedic Specialist',
    'jaw pain': 'Orthopedic Specialist',

    # Cardiologist: Heart-related symptoms
    'chest pain': 'Cardiologist',
    'shortness of breath': 'Pulmonologist',
    'rapid breathing': 'Cardiologist',
    'irregular heartbeat': 'Cardiologist',
    'high blood pressure': 'Cardiologist',
    'low blood pressure': 'Cardiologist',
    'fainting': 'Cardiologist',

    # Gastroenterologist: Digestive system symptoms
    'stomach pain': 'Gastroenterologist',
    'constipation': 'Gastroenterologist',
    'diarrhea': 'Gastroenterologist',
    'vomiting': 'Gastroenterologist',
    'bloating': 'Gastroenterologist',
    'gas': 'Gastroenterologist',
    'indigestion': 'Gastroenterologist',
    'acidity': 'Gastroenterologist',
    'blood in stool': 'Gastroenterologist',
    'ulcers': 'Gastroenterologist',
    'dysentery': 'Gastroenterologist',

    # ENT Specialist: Ear, nose, throat symptoms
    'throat pain': 'E N T Specialist',
    'ear pain': 'E N T Specialist',
    'ear ringing': 'E N T Specialist',
    'ear discharge': 'E N T Specialist',
    'hearing loss': 'E N T Specialist',
    'runny nose': 'E N T Specialist',
    'sneezing': 'E N T Specialist',
    'congestion': 'E N T Specialist',
    'nosebleed': 'E N T Specialist',
    'difficulty swallowing': 'E N T Specialist',

    # Pulmonologist: Respiratory symptoms
    'cough': 'General Practitioner',
    'flu': 'General Practitioner',
    'asthma': 'General Practitioner',
    'pneumonia': 'Pulmonologist',
    'covid': 'Pulmonologist',

    # Psychiatrist: Mental health symptoms
    'anxiety': 'General',
    'depression': 'Psychologist',
    'insomnia': 'General Practitioner',
    'restlessness': 'General Practitioner',
    'nervousness': 'General Practitioner',
    'panic attack': 'Psychologist',
    'mood swing': 'Psychologist',
    'difficulty concentrating': 'General Practitioner',
    'hallucination': 'General Practitioner',
    'lack of motivation': 'General Practitioner',

    # Endocrinologist: Metabolic and hormonal symptoms
    'diabetes': 'Endocrinologist',
    'thyroid': 'Endocrinologist',
    'weight loss': 'Endocrinologist',
    'weight gain': 'Endocrinologist',
    'excessive thirst': 'Endocrinologist',
    'dehydration': 'Endocrinologist',
    'sugar': 'Endocrinologist',
    'obesity': 'Endocrinologist',

    # Ophthalmologist: Eye-related symptoms
    'blurred vision': 'Ophthalmologist',
    'eye pain': 'Ophthalmologist',
    'eyes pain' : 'Ophthalmologist',
    'eye discharge': 'Ophthalmologist',
    'eye weakness': 'Ophthalmologist',

    # Rheumatologist: Autoimmune and joint-related symptoms
    'swelling': 'Rheumatologist',
    'cramp': 'Rheumatologist',
    'swollen lymph nodes': 'E N T Specialist',

    # Infectious Disease Specialist: Infectious diseases
    'infection': 'General Practitioner',
    'inflammation': 'General Practitioner',
    'malaria': 'General Practitioner',
    'dengue': 'General Practitioner',
    'typhoid': 'General Practitioner',
    'chickenpox': 'General Practitioner',
    'hiv': 'Virologist',

    # Oncologist: Cancer-related symptoms
    'cancer': 'Oncologist',

    # Hepatologist: Liver-related symptoms
    'jaundice': 'Hepatologist',

    # Pediatrician: Pediatric symptoms
    'pediatric symptoms': 'Pediatrician',

    # General Practitioner: Common and unspecified symptoms
    'fever': 'General Practitioner',
    'cold': 'General Practitioner',
    'loss of appetite': 'General Practitioner',
    'nausea': 'General Practitioner',
    'exhaustion': 'General Practitioner',
    'fatigue': 'General Practitioner',
    'chills': 'General Practitioner',
    'sweat': 'General Practitioner',
    'sleepy': 'General Practitioner',
    'more hungry': 'General Practitioner',
    'hiccups': 'General Practitioner',
    'injury': 'General Practitioner',
    'bleeding': 'General Practitioner',
    'irritation': 'General Practitioner',
    'brittle nails': 'General Practitioner',
    'tingling': 'General Practitioner',
    'piles': 'General Practitioner',
    'broken tooth': 'Dentist',
    'tooth decay': 'Dentist',
    'broken voice': 'E N T Specialist',
    'hand dryness': 'Dermatologist',
    'wound': 'General Practitioner',
    'body ache': 'General Practitioner',
    'bruises': 'General Practitioner',
    'eye weakness': 'Ophthalmologist',
    'leg weakness': 'Neurologist',
    'yellow eyes': 'Hepatologist',
    'red eyes': 'Ophthalmologist',
	
    # Gynecologist
    'female issue': 'Gynecologist',
    'menopause': 'Gynecologist',
}

HINDI_OFFLINE_DICT = {
            "fever": "बुखार",
            "cold": "जुकाम",
            "runny nose": "बहती नाक",
            "sneezing": "छींकना",
            "rash": "दाने",
            "back spasm": "पीठ में ऐंठन",
            "dizziness": "चक्कर आना",
            "weakness": "कमज़ोरी",
            "loss of appetite": "भूख में कमी",
            "cough": "खांसी",
            "muscle pain": "मांसपेशियों में दर्द",
            "joint pain": "जोड़ों में दर्द",
            "chest pain": "छाती में दर्द",
            "back pain": "पीठ दर्द",
            "constipation": "कब्ज",
            "throat pain": "गले में दर्द",
            "diarrhea": "दस्त",
            "flu": "फ़्लू",
            "shortness of breath": "सांस फूलना",
            "rapid breathing": "तेजी से सांस लेना",
            "stomach pain": "पेट दर्द",
            "migraine": "आधा सिर दर्द",
            "skin burning": "त्वचा में जलन",
            "itching": "खुजली",
            "swelling": "सूजन",
            "vomiting": "उल्टी",
            "infection": "संक्रमण",
            "inflammation": "सूजन (inflammation)",
            "cramp": "ऐंठन",
            "bleeding": "खून बहना",
            "irritation": "चिड़चिड़ापन",
            "anxiety": "चिंता",
            "depression": "अवसाद",
            "congestion": "जमाव",
            "nausea": "मतली",
            "swollen lymph nodes": "सूजे हुए लसीका ग्रंथि",
            "insomnia": "अनिद्रा",
            "cancer": "कैंसर",
            "diabetes": "मधुमेह",
            "allergy": "एलर्जी",
            "weight loss": "वजन कम होना",
            "weight gain": "वजन बढ़ना",
            "hair loss": "बाल झड़ना",
            "blurred vision": "धुंधली दृष्टि",
            "ear pain": "कान दर्द",
            "numbness": "सुन्नपन",
            "dry mouth": "मुंह सूखना",
            "frequent urination": "बार-बार पेशाब",
            "acne": "मुँहासे",
            "confusion": "भ्रम",
            "memory loss": "याददाश्त कम होना",
            "difficulty swallowing": "निगलने में कठिनाई",
            "restlessness": "बेचैनी",
            "bloating": "पेट फूला हुआ",
            "gas": "गैस",
            "indigestion": "बदहजमी",
            "heartburn": "सीने में जलन",
            "mouth sore": "मुँह दर्द",
            "nosebleed": "नाक से खून आना",
            "ear ringing": "कानों में घंटी बजना",
            "dark urine": "गहरा मूत्र",
            "blood in urine": "मूत्र में खून",
            "blood in stool": "मल में खून",
            "high blood pressure": "उच्च रक्तचाप",
            "low blood pressure": "निम्न रक्तचाप",
            "excessive thirst": "अत्यधिक प्यास",
            "dehydration": "निर्जलीकरण",
            "sweat": "पसीना आना",
            "eye pain": "आंखों में दर्द",
            "eye discharge": "आंखों से रिसाव",
            "ear discharge": "कान से रिसाव",
            "jaundice": "पीलिया",
            "hearing loss": "श्रवण ह्रास",
            "balance problem": "संतुलन की समस्या",
            "irregular heartbeat": "अनियमित धड़कन",
            "fainting": "बेहोशी",
            "tremor": "कंपकंपी",
            "nervousness": "घबराहट",
            "panic attack": "आतंक का दौरा",
            "mood swing": "मिज़ाज़ में उतार-चढ़ाव",
            "difficulty concentrating": "ध्यान केंद्रित करने में कठिनाई",
            "hallucination": "मतिभ्रम",
            "fatigue": "थकान",
            "lack of motivation": "प्रेरणा की कमी",
            "exhaustion": "अत्यधिक थकान",
            "bone pain": "हड्डियों में दर्द",
            "wrist pain": "कलाई में दर्द",
            "sprain": "मोच",
            "strain": "खिंचाव",
            "arthritis": "गठिया",
            "gout": "गाउट",
            "headache": "सिरदर्द",
            "injury": "चोट",
            "chills": "ठंड लगना",
            "leg pain": "टांग में दर्द",
            "hand pain": "हाथ में दर्द",
            "arm pain": "बांह में दर्द",
            "foot pain": "पैर में दर्द",
            "knee pain": "घुटने में दर्द",
            "shoulder pain": "कंधे में दर्द",
            "hip pain": "कूल्हे में दर्द",
            "jaw pain": "जबड़े में दर्द",
            "tooth pain": "दांत में दर्द",
            "sleepy": "नींद आना",
            "bone fracture": "हड्डी टूटना",
            "back bone issue": "रीढ़ की हड्डी की समस्या",
            "female issue": "महिला संबंधी समस्या",
            "thyroid": "थायरॉयड",
            "piles": "बवासीर",
            "asthma": "अस्थमा",
            "pneumonia": "निमोनिया",
            "sugar": "शुगर (मधुमेह)",
            "eye weakness": "आंखों की कमज़ोरी",
	        "waist pain": "कमर दर्द",
            "urine issues": "पेशाब की समस्याएँ",
		    "caesarean section": "सीज़ेरियन सेक्शन",
            "pregnancy": "गर्भावस्था",
            "pediatric symptoms": "बाल चिकित्सा लक्षण",
            
            # — generic “<body-part> issue” entries —
        "leg issue": "टांग की समस्या",
        "eye issue": "आंख की समस्या",
        "hand issue": "हाथ की समस्या",
        "arm issue": "बांह की समस्या",
        "head issue": "सिर की समस्या",
        "back issue": "पीठ की समस्या",
        "chest issue": "छाती की समस्या",
        "wrist issue": "कलाई की समस्या",
        "throat issue": "गले की समस्या",
        "stomach issue": "पेट की समस्या",
        "neck issue": "गरदन की समस्या",
        "knee issue": "घुटने की समस्या",
        "foot issue": "पांव की समस्या",
        "shoulder issue": "कंधे की समस्या",
        "hip issue": "कूल्हे की समस्या",
        "jaw issue": "जबड़े की समस्या",
        "tooth issue": "दांत की समस्या",
        "thigh issue": "जांघ में समस्या",
        "forehead issue": "माथे की समस्या",
        "tongue issue": "जीभ की समस्या",

        # — specific trigger_keyword combos —
        "tooth injury": "दांत में चोट",
        "tooth sensitivity": "दांत की संवेदनशीलता",
        "leg injury": "टांग में चोट",
        "leg pain": "टांग में दर्द",
        "leg swelling": "टांग में सूजन",
        "eye itching": "आंखों में खुजलाहट",
        "eye redness": "आंखों में लाली",
        "eye burn": "आंखों में जलन",
        "eye blurry vision": "आंखों का धुंधलापन",
        "hand numbness": "हाथ में सुन्नपन",
        "hand swelling": "हाथ में सूजन",
        "arm weakness": "बांह में कमजोरी",
        "head injury": "सर में चोट",
        "back stiffness": "पीठ की जकड़न",
        "chest discomfort": "छाती में असुविधा",
        "throat swelling": "गले में सूजन",
        "stomach bloating": "पेट में फुलाव",
        "stomach nausea": "पेट में मतली",
        "neck stiffness": "गरदन में जकड़न",
        "knee swelling": "घुटने में सूजन",
        "shoulder weakness": "कंधे में कमजोरी",
        "ear ringing": "कान में घंटी बजना",
	      "eye weakness": "आँखों में कमजोरी",
        "nosebleed": "नाक से खून आना",

	#newly added
    "nose pain": "नाक में दर्द",
    "mouth pain": "मुंह में दर्द",
    "weight fluctuation": "वजन में उतार-चढ़ाव",
    "obesity": "मोटापा",
    "more hungry": "अत्यधिक भूख लगना",
    "brittle nails": "नाखूनों का टूटना",
    "difficulty speaking": "बोलने में कठिनाई",
    "ulcers": "छाले",
    "hiccups": "हिचकी",
    "seizures": "दौरे",
    "dysentery": "पेचिश",
    "malaria": "मलेरिया",
    "dengue": "डेंगू",
    "covid": "कोविड",
    "typhoid": "टाइफाइड",
    "chickenpox": "चेचक",
    "kidney issue": "गुर्दे की समस्या",
    "broken tooth": "टूटा हुआ दांत",
    "tooth decay": "दांत सड़ना",
    "broken voice": "टूटी आवाज़",
    "hand dryness": "हाथों का सूखापन",
    "wound": "घाव",
    "body ache": "शरीर में दर्द",
    "bruises": "नील",
    "thigh pain": "जांघ में दर्द",
    "pelvic pain": "पेल्विक दर्द",
    "elbow pain": "कोहनी में दर्द",
    "calf pain": "पिंडली में दर्द",
    "pain" : "दर्द",
    "jaw injury": "जबड़े में चोट",
    "jaw swelling": "जबड़े में सूजन",
    "jaw stiffness": "जबड़े में जकड़न",
    "menopause": "रजोनिवृत्ति",
    "period pain": "पीरियड का दर्द",
    "period bleeding": "पीरियड में रक्तस्राव",
    "period issues": "पीरियड से जुड़ी समस्याएं",
    "abdominal issues": "पेट से जुड़ी समस्याएं",
        }
