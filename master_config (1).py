
# ------------------------------------------------------------------ #
# ------------------------- Original symptom ----------------------- #
# ------------------------------------------------------------------ #
# Original symptom list with potential duplicates
symptom_list = [
'fever', 'cold', 'runny nose', 'sneezing', 'rash', 'back spasm', 'dizziness', 'weakness', 'loss of appetite', 'cough', 'muscle pain', 'joint pain',
'chest pain', 'back pain', 'constipation', 'throat pain', 'diarrhea', 'flu', 'shortness of breath', 'rapid breathing', 'stomach pain', 'migraine',
'skin burning', 'itching', 'swelling', 'vomiting', 'infection', 'inflammation', 'cramp', 'bleeding', 'irritation', 'anxiety', 'depression','congestion',
'nausea', 'swollen lymph nodes', 'insomnia', 'cancer', 'diabetes', 'allergy', 'weight loss', 'weight gain', 'hair loss', 'blurred vision', 'ear pain',
'numbness', 'dry mouth', 'frequent urination', 'acne', 'confusion', 'memory loss', 'difficulty swallowing', 'restlessness', 'bloating', 'neck pain',
'gas', 'indigestion', 'acidity', 'mouth sore', 'nosebleed', 'ear ringing', 'dark urine', 'blood in urine', 'blood in stool', 'high blood pressure',
'low blood pressure', 'excessive thirst', 'dehydration', 'skin burning', 'sweat', 'eye pain',  'eye discharge', 'ear discharge', 'jaundice',
'hearing loss', 'balance problem', 'irregular heartbeat', 'fainting', 'tremor', 'nervousness', 'panic attack', 'mood swing', 'difficulty concentrating',
'hallucination', 'lack of motivation', 'exhaustion', 'bone pain', 'wrist pain', 'sprain', 'strain', 'arthritis', 'gout', 'headache', 'injury', 'chills',
'leg pain', 'hand pain', 'arm pain', 'foot pain', 'knee pain', 'shoulder pain', 'hip pain', 'jaw pain', 'tooth pain','sleepy', 'bone fracture','sleepy','back bone issue',
'female issue', 'thyroid', 'piles', 'asthma','pneumonia','sugar',
# weakness symtom
'eye weakness' #'leg weakness'
  #'yellow eyes', 'red eyes'
]

# ------------------------------------------------------------------ #
# ------------------------- Mapping symptom ------------------------ #
# ------------------------------------------------------------------ #
symptom_synonyms = {
  'back spasm': [
        'back is spasming', 'back spasms', 'back spasm', 'spinal contraction', 'muscle cramp in back', 'tight back muscles', 'back tightening', 'muscle spasm in lower back', 'spine spasming',
        'back muscle jerk', 'severe back cramp', 'spine knot', 'muscle twitch in back', 'spinal spasm', 'back stiffening', 'lower back stiffness', 'muscle contraction in back', 'back cramping',
        'muscle twitching in spine', 'sharp back pain', 'sudden back pain', 'painful muscle contraction', 'sharp spasms in back', 'throbbing back pain', 'spine twinge', 'muscle jerking in back',
        'painful back convulsion', 'tense back', 'tightness in back', 'cramping back muscles', 'pulled back muscle', 'twisting back pain', 'cramped spine', 'jerking back muscles', 'painful back tightening',
        'spinal muscle strain', 'back tension', 'muscle knots in back', 'spine tightening pain', 'painful back stiffness', 'spinal muscles seizing', 'back spasm attack', 'muscle discomfort in back',
        'intense back strain', 'stiffened spine', 'spinal muscles hardening', 'acute back spasm', 'back contorting', 'back stiffness attack', 'back muscle tension', 'back pain with spasms', 'spasm in the back',
        'back locked up','back clenched up'
    ],
    'headache': [
        'head pain', 'throbbing headache', 'pounding head', 'splitting headache', 'severe headache', 'migraine-like ache', 'cranial ache', 'head pressure', 'sinus headache', 'tension headache',
        'hammering pain in skull', 'aching brain', 'full-head ache', 'temple-throbbing pain', 'dull ache behind eyes', 'stabbing head sensation', 'skull-crushing pressure', 'nagging ache in head',
        'relentless cranial pounding', 'forehead-tightening discomfort', 'vice-like grip on head', 'pulsating headache', 'dull throb', 'piercing head agony', 'continuous headache hum', 'low-level head strain',
        'top-of-head soreness', 'subcranial ache', 'stabbing darts of pain in scalp', 'brain-squeezing feeling', 'top-heavy ache', 'ear-to-ear head ache', 'all-encompassing head discomfort', 'band-like pressure around head',
        'persistent noggin ache', 'head tenderness', 'scalp-aching feeling', 'sensitive head region', 'brainache', 'mind-throbbing torment', 'front-lobe pressure', 'crown-of-head tension',
        'behind-the-eyes ache', 'skull-tight discomfort', 'never-ending head throb', 'grating ache inside skull', 'sinus-pressured ache', 'temple pounding', 'brain pulsation pain', 'cephalic torment',
        'oppressive ache under cranium', 'subtle persistent ache', 'gnawing head discomfort', 'dull pounding drumbeat in head', 'hammering inside skull walls', 'unyielding head tension', 'rote ache cycling through head',
        'cranium under siege', 'deep-set head pang', 'swirling headache sensation', 'anchor-like pressure in head','pain in head'
    ],
    'migraine': [
        'intense one-sided headache', 'migraine aura', 'pulsating pain in head', 'photophobia-associated headache', 'debilitating headache', 'migraine attack', 'searing half-skull ache', 'throbbing temple migraine',
        'nausea-laced head pain', 'light-sensitive head torture', 'migraine episode', 'crippling one-sided ache', 'sharp lancing head pain', 'skull-splitting half-side ache', 'throbbing migraine pulse', 'debilitating cranial assault',
        'severe sensory headache', 'disabling one-sided throb', 'catastrophic temple pounding', 'migraine-induced nausea', 'half-head agony', 'sharp lancing head pain', 'stabbing head sensation', 'pulsating migraine',
        'tension-triggered migraine', 'blinding headache', 'brain-splitting side ache', 'overwhelming migraine pressure', 'incapacitating headache event', 'shattering unilateral head pain', 'sensitive to slightest sound',
        'migraine meltdown', 'severe sensitivity headache', 'hammering half-head ache', 'aura shimmer leading to pain', 'throbbing unilateral agony', 'needle-like head stab', 'crushing half-skull sensation',
        'crippling light-triggered pain', 'migraine climate inside head', 'tidal wave of head torment', 'migraine crescendo', 'migraine-flare crisis', 'incapacitating halo of pain', 'ear-to-temple throbbing on one side'
    ],
    'allergy': [
        'allergies', 'allergic reaction', 'allergic response', 'hay fever', 'allergic rhinitis', 'pollen sensitivity', 'dust mite allergy', 'food allergy', 'skin allergy', 'seasonal allergies',
        'environmental allergies', 'allergic condition', 'allergic response to pollen', 'sensitive to allergens', 'sneezing due to allergies', 'wheezing from allergic reaction',
        'swollen nasal passages', 'runny nose from allergies', 'sinus congestion from allergies', 'allergic rashes', 'eczema flare-up', 'hives', 'itchy skin from allergens', 'swollen face from allergies',
        'respiratory allergy', 'allergic reactions in skin', 'excessive histamine release', 'redness from allergy', 'swollen throat from allergies', 'asthma attack triggered by allergens', 'increased mucus production',
        'throat irritation due to allergens', 'difficulty breathing from allergies', 'sneezing fits due to pollen', 'allergic asthma', 'seasonal allergic reactions', 'itchy nose', 'nasal discharge from allergies',
        'blocked sinuses', 'itchy throat from allergies', 'dry throat from allergies', 'allergy flare-up', 'anaphylactic reaction', 'anaphylaxis', 'allergic dermatitis', 'rashes from allergens', 'swelling of lips',
        'swollen tongue', 'red eyes from allergies', 'tearing eyes from allergies', 'itchy and watery eyes'
    ],
    'fever': [
        'high temperature', 'elevated body temperature', 'feeling feverish', 'fevering', 'running a fever', 'burning up', 'feeling internally hot', 'having a temperature', 'spiking a fever', 'febrile state',
        'raised core temperature', 'overheated body', 'intense body heat', 'thermal imbalance', 'body overheating', 'raging fever', 'heated condition', 'abnormally warm body', 'pyrexia', 'uncontrolled internal heat',
        'feeling aflame', 'body heat surging', 'hot to the touch', 'internal ignition of warmth', 'body temperature surging', 'excessive warmth inside', 'bodily heat overload', 'intense flush', 'thermometer reading high',
        'scorching internal climate', 'burning sensation from within', 'sweltering body feel', 'thermal elevation', 'heated bloodstream', 'furnace-like feeling', 'feeling like an oven', 'heat radiating under skin',
        'internal fire', 'ignited from the inside', 'excessive internal warmth', 'body boiling over', 'incendiary sensation', 'intense internal glow', 'unrelenting heat', 'blazing warmth','feeling hot',
        'molten interior heat', 'near boiling point', 'incapacitating heat', 'relentless feverishness', 'sizzling body temp', 'flaming sensation', 'constant burning feeling', 'heat wave inside me', 'sweating due to internal heat',
        'red-hot core', 'smoldering embers of warmth', 'furnace-like core', 'pulsating heat', 'unremitting temperature rise', 'searing body condition', 'fire coursing through veins', 'endlessly hot', 'elevated reading on the thermometer',
        'no relief from heat', 'intense internal burning', 'volcanic warmth', 'torched from inside', 'superheated body', 'radical temperature spike', 'roasting sensation', 'tropical internal climate', 'heat-induced misery',
        'stoked internal fires', 'hothouse conditions inside', 'stifling fever fire', 'blazing internal inferno', 'relentless temperature climb', 'fever wave'
    ],
    'cough': [
        'Persistent cough', 'hacking cough', 'dry cough', 'wet cough', 'productive cough (with phlegm)', 'barking cough', 'non-productive cough', 'chronic cough',
        'coughing up mucus/sputum/blood', 'irritating cough', 'scratchy cough', 'whooping cough-like sound', 'continuous throat clearing', 'raspy hacking', 'chesty cough',
        'rattling cough', 'deep-chested cough', 'shallow annoying cough', 'tickling cough', 'lingering throat hack', 'spasm-like coughs', 'throaty expulsions',
        'worrisome coughing fits', 'repetitive cough bursts', 'phlegmy hacking', 'bronchial coughing', 'stubborn cough', 'dry tickling cough', 'persistent throat tickle',
        'strangling cough', 'wheezing cough', 'loud barking cough', 'cracking cough', 'sputum-laden cough', 'cough with gagging', 'spasmodic cough', 'stubborn dry cough',
        'overwhelming coughing sensation', 'sharp, dry cough', 'cough with sharp throat pain', 'violent coughing fits', 'painful coughing episodes', 'coughing after exertion',
        'chronic phlegm cough', 'intense wheezing cough', 'grating cough', 'wet chesty cough', 'gurgling cough'
    ],
    'sore throat': [
        'scratchy throat', 'painful throat', 'burning throat', 'irritated throat', 'swollen throat', 'inflamed throat', 'throat discomfort', 'throat scratchiness',
        'raw throat', 'tight throat', 'feeling of something stuck in throat', 'hoarse throat', 'swollen tonsils', 'throat inflammation', 'red throat', 'sore and swollen throat',
        'gritty throat', 'tender throat', 'raspy throat', 'dry throat', 'throat burning sensation', 'feeling of throat swelling', 'pain on swallowing', 'raw feeling in throat',
        'sore feeling when talking', 'throat soreness', 'painful swallowing', 'constant throat irritation', 'throat muscle soreness', 'tight feeling in throat',
        'throat dryness', 'itchy throat', 'burning sensation in throat', 'scratching feeling in throat', 'tenderness in throat', 'chronic throat discomfort', 'raspiness in voice',
        'feeling like throat is closing', 'constant need to clear throat', 'sore throat with hoarseness', 'dry cough with sore throat', 'sharp throat pain'
    ],
    'stomach pain': [
        'stomach pain', 'stomach ache', 'abdominal pain', 'belly ache', 'intestinal discomfort', 'stomach cramps', 'nauseous stomach pain',
        'sharp stomach pain', 'stomach tenderness', 'sharp abdominal cramps', 'stomach upset', 'abdominal tenderness', 'intestinal bloating', 'tummy pain', 'swollen belly',
        'feeling of fullness', 'feeling heavy in stomach', 'digestive pain', 'stomach spasms', 'soreness in abdomen', 'nausea and stomach ache',
        'gastric pain', 'pain after eating', 'belly discomfort', 'gurgling stomach', 'stomach churning', 'sharp abdominal pain', 'dull abdominal pain',
        'abdominal tightness', 'aching belly', 'painful digestion', 'pain under ribs', 'discomfort after meals',
        'uncomfortable stomach', 'intestinal cramps', 'sharp pain in lower abdomen', 'feeling of indigestion', 'pain around stomach area', 'belly pain', 'pain in the abdomen', 'stomach discomfort',
        'sharp stomach pain', 'dull abdominal pain', 'cramping in the abdomen', 'bloating with pain',
        'gas pain in the abdomen', 'stabbing pain in the belly', 'abdominal cramps', 'sharp pain in the stomach area', 'pain from indigestion', 'pain after eating', 'nauseating abdominal pain',
        'pain from gas buildup', 'pressure in the stomach', 'pain from constipation', 'distended abdomen', 'pain from ulcers', 'pain from bloating', 'pain from food intolerance',
        'sore stomach', 'pain from intestinal issues', 'gastrointestinal pain', 'tenderness in the stomach', 'pain near the navel', 'pain from diarrhea', 'stomach flu pain', 'pain in the lower abdomen',
        'feeling of fullness with pain', 'pain in the upper abdomen', 'stomach cramping', 'sharp abdominal cramps', 'nausea with stomach pain', 'abdominal swelling with pain', 'abdominal pain',
        'chronic stomach pain', 'pain with digestive issues', 'pain from food poisoning', 'pain from gallbladder issues', 'pain from acid reflux','pain in stomach'
    ],
    'weakness': [
        'tiredness', 'extreme tiredness','weariness', 'fatigued feeling', 'lack of energy', 'physical depletion', 'mental fatigue', 'chronic tiredness',
        'drained', 'feeling wiped out', 'feeling run down', 'fatigue','low energy', 'severe fatigue', 'feeling sluggish', 'morning fatigue', 'fatigue after exertion',
        'debilitating tiredness', 'drowsiness', 'chronic fatigue syndrome', 'feeling lethargic', 'mental sluggishness', 'physical tiredness', 'difficulty keeping eyes open',
        'lack of vitality', 'energy depletion', 'feeling drained', 'listlessness', 'burned out', 'exhausted state', 'feeling zoned out', 'tired all the time', 'fatigued state',
       'constant tiredness', 'no motivation', 'fatigued muscles', 'endless tiredness', 'lethargic movements',
        'lacking strength', 'body fatigue',  'feeling disconnected'
    ],
    'nausea': [
        'feeling nauseous', 'upset stomach', 'queasy', 'stomach turning', 'sick feeling', 'feeling like vomiting', 'gagging sensation', 'discomfort in stomach', 'unsettled stomach',
        'vomit-like sensation', 'stomach churn', 'sick to stomach', 'nauseous feeling', 'spinning stomach', 'intense nausea', 'gagging feeling', 'feeling on the verge of throwing up',
        'uneasy stomach', 'feeling faint', 'upset belly', 'dizzy stomach', 'nauseous and dizzy', 'headache and nausea', 'intense queasiness', 'morning sickness feeling',
        'stomach discomfort', 'feeling faint with nausea', 'stomach churn', 'constant nausea', 'puking feeling', 'nausea after eating', 'feeling like you could throw up',
        'stomach upset with nausea', 'unsettled feeling in stomach', 'feeling lightheaded with nausea', 'nausea with dizziness', 'craving nausea', 'nausea from food', 'stomach unease',
        'sick feeling after meals', 'swirling stomach', 'nauseous waves', 'gag reflex activated', 'gurgling stomach with nausea'
    ],
    'dizziness': [
        'Lightheadedness', 'feeling faint', 'woozy sensation', 'spinning feeling', 'off-balance', 'unsteady', 'dizzy spells', 'giddy feeling', 'vertiginous sensation',
        'wobbly feeling', 'swaying in mind', 'head swimming', 'feeling as if room is turning', 'disoriented equilibrium', 'teetering sense', 'tipsy sensation without alcohol',
        'floating head', 'unstable ground feeling', 'swirling environment', 'sense of being on a boat', 'nauseating spin', 'loss of spatial orientation', 'drifting balance',
        'feeling like I might topple', 'wavy floor sensation', 'heady unsteadiness', 'murky equilibrium', 'airy head sensation', 'constant near-tip-over feeling', 'mental wobble',
        'feathery balance', 'gravity shifting under feet', 'dizziness waves', 'rocking sensation', 'seasick feeling on land', 'fuzzy-headed instability', 'inner ear imbalance feeling',
        'wavy-field-of-view sensation', 'lurching environment', 'faltering steadiness', 'delicately balanced but slipping', 'rubbery legs feeling', 'giddy swirl in head',
        'tilting world', 'swaying sensation', 'imbalance feeling', 'shaky equilibrium', 'floating dizziness', 'spinning sensation', 'feeling off-kilter'
    ],

    'shortness of breath': [
        'Shortness of breath', 'breathlessness', 'difficulty breathing', 'feeling air hunger', 'fast breathing', 'shallow breathing', 'gasping for air',
        'labored breathing', 'struggling to breathe', 'tightness in chest while inhaling', 'feeling suffocated', 'cannot catch my breath', 'panting heavily', 'air feeling thin',
        'lungs working overtime', 'chest feels restricted', 'fighting for each breath', 'difficulty in breathing', 'strained respiration', 'feeling smothered', 'desperate for oxygen',
        'winded easily', 'constant puffing', 'breathing feels blocked', 'inhaling with effort', 'forced breathing', 'constant need to gulp air', 'sensation of drowning in open air',
        'chest heaviness on breathing', 'incomplete lung expansion', 'inadequate airflow', 'lungs not filling properly', 'needing to breathe harder', 'stuck in half-breath',
        'breath cut short', 'huffing and puffing', 'shallow panting', 'frantic search for air', 'hyperventilating feeling', 'feeling as if air is too thick', 'minimal air exchange',
        'muscle effort just to breathe', 'chest oppression', 'suffocating sensation even in open space', 'feeling strangled by lack of air', 'restrictive breathing pattern',
        'breathing feels like pushing through a straw', 'air-starved lungs', 'cannot take a deep breath', 'strained oxygen intake', 'feeling like each breath is a struggle',
        'never fully satisfied inhalation', 'gasping between words', 'needy breathing pattern', 'barely pulling in enough air', 'lungs working at half capacity', 'respiratory distress',
        'continuous short-windedness'
    ],
   'rapid breathing': [
         'heavy breathing', 'shallow breathing', 'heart skipping beats'
    ],
    'muscle pain': [
        'muscle ache', 'muscle soreness', 'muscle strain', 'muscle discomfort', 'muscle stiffness', 'muscle tension', 'muscle fatigue', 'muscle injury', 'muscle cramps',
        'muscle spasm', 'muscle pulling', 'muscle tears', 'muscle tightness', 'muscle throbbing', 'aching muscles', 'sore muscles', 'tender muscles', 'painful muscles',
        'muscle inflammation', 'deep muscle pain', 'sharp muscle pain', 'pulling sensation in muscles', 'muscle tenderness', 'delayed onset muscle soreness (DOMS)', 'straining muscle',
        'muscle weakness', 'fatigued muscles', 'muscle stiffness after exercise', 'muscle burning', 'swollen muscles', 'muscle discomfort on movement', 'muscle ache after exertion',
        'overused muscles', 'fatigue-related muscle pain', 'chronic muscle pain', 'localized muscle pain', 'muscle strain from overuse', 'aching from tension in muscles',
        'muscle soreness from heavy lifting', 'muscle discomfort from exercise', 'muscle pain after activity', 'muscle distress', 'inflamed muscle tissue', 'muscle spasm after effort',
        'tensed muscles', 'muscle overextension', 'pain in the calves', 'pain in the upper arms', 'pain in the back muscles','pain in the muscle'
    ],
    'insomnia': [
        'difficulty sleeping', 'trouble sleeping', 'sleeplessness', 'restlessness at night', 'inability to fall asleep', 'waking up during the night', 'frequent wake-ups',
        'early morning wakefulness', 'poor sleep quality', 'sleep deprivation', 'sleep disturbance', 'trouble staying asleep', 'sleep interruptions', 'unable to sleep through the night',
        'insufficient sleep', 'lack of sleep', 'unrefreshing sleep', 'tossing and turning', 'unsettled sleep', 'sleep issues', 'chronic insomnia', 'difficulty achieving deep sleep',
        'waking up too early', 'difficulty with sleep onset', 'difficulty getting comfortable at night', 'sleep anxiety', 'sleeping problems', 'frequent nighttime awakenings', 'irregular sleep cycle',
        'poor sleep habits', 'nighttime restlessness', 'waking in the middle of the night', 'sleep deprivation symptoms', 'daytime sleepiness from poor sleep', 'sleep fragmentation',
        'restless sleep', 'persistent insomnia', 'sleep troubles', 'light sleeping', 'short sleep duration', 'restorative sleep deprivation', 'fatigue from sleeplessness',
        'waking up exhausted', 'sleep cycle disruption', 'sleep onset difficulty', 'insomnia due to stress', 'mental hyperactivity preventing sleep', 'cannot sleep', 'unable to sleep','not able to sleep',
        'unable to fall asleep', 'not able to fall asleep'
    ],
    'rash': [
        'skin rash', 'redness on skin', 'skin irritation', 'skin inflammation', 'skin breakout', 'itchy rash', 'hives', 'blotchy skin', 'skin eruption', 'skin lesions',
        'red bumps on skin', 'inflamed skin', 'patchy rash', 'discolored skin', 'raised rash', 'painful rash', 'rash with blisters', 'dry rash', 'moist rash', 'allergic rash',
        'eczema', 'psoriasis patches', 'contact dermatitis', 'hives breakout', 'heat rash', 'prickly heat', 'scaly rash', 'rash on face', 'body rash', 'rashes on arms',
        'welts on skin', 'itchy patches on skin', 'skin redness', 'chronic skin rash', 'dry, scaly rash', 'blistering rash', 'swollen rash', 'rash with swelling',
        'inflamed, sore rash', 'rash with pus', 'pimple-like rash', 'rash caused by allergic reaction', 'skin irritation with swelling', 'flaky rash', 'raw skin from rash',
        'horrible itching rash', 'rashes from medication', 'painful itching on skin', 'burning sensation from rash'
    ],
    'congestion': [
        'nasal congestion', 'blocked nose', 'stuffy nose', 'clogged nasal passages', 'nasal obstruction', 'sinus congestion', 'sinus blockage', 'stuffy sinuses', 'pressure in sinuses',
        'nasal blockage', 'swollen nasal passages', 'congested sinuses', 'nose congestion', 'nasal stuffiness', 'head congestion',
        'swelling of nasal tissues', 'sinus pressure', 'stuffy feeling in head', 'congestion in sinus cavities', 'nasal stuffy feeling',
        'inflamed nasal passages', 'feeling of a blocked nose', 'swollen nostrils', 'nasal airway blockage', 'heavy feeling in head from congestion', 'sinus drainage blockage',
        'clogged airways', 'full nose', 'stuffy head', 'excess mucus in nose', 'thick mucus in nostrils', 'nasal obstruction from mucus', 'inability to breathe through nose',
        'nasal phlegm buildup', 'blocked airways', 'increased mucus production', 'congested nasal lining', 'swelling in nasal cavity', 'unpleasant nose feeling from congestion',
        'nasal fullness', 'pressure behind the eyes from congestion', 'nasal sinus blockage', 'nasal breathing difficulties'
    ],
    'runny nose': [
        'nasal discharge', 'drippy nose', 'clear runny nose', 'watery nose', 'excessive mucus secretion', 'nose dripping', 'watery nasal discharge', 'runny mucus from nose',
        'frequent nose blowing', 'excessive snot', 'thin nasal discharge', 'clear mucus', 'constant nose drip', 'streaming nose', 'watery runny nose', 'mucus dripping down from nose',
        'nose running uncontrollably', 'sticky nasal discharge', 'clear discharge from nostrils', 'frequent nasal wiping', 'constant nasal leaks', 'draining sinuses',
        'runny nose due to allergies', 'constant nasal secretions', 'wet nose', 'nose discharge', 'sinus leakage', 'flowing nose', 'uncontrolled nasal discharge',
        'persistent runny nose', 'dripping from nostrils', 'clogged but dripping nose', 'excessive mucus from nostrils', 'sniffling from a runny nose', 'constant nasal drip',
        'dripping sinuses', 'runny nose caused by cold', 'mucus continuously dripping', 'snotty nose', 'stuffy nose with runny discharge', 'chronic runny nose', 'dripping all day long'
    ],
    'sneezing': [
        'Sneezing fits', 'frequent sneezing', 'sneezing spells', 'sneezing bouts', 'sneezing attacks', 'sneezing episodes', 'uncontrollable sneezing', 'explosive sneezes',
        'repetitive sneezes', 'unstoppable nasal explosions','serial sneezing', 'sneeze after sneeze', 'chain-sneezing', 'nasal expulsions',
        'nasal reflex outbursts', 'convulsive sneezing', 'rapid-fire sneezes', 'machine-gun sneezing', 'persistent nasal expulsions', 'surprise sneezes',
        'tickling in nose triggering sneezes', 'staccato sneezing', 'sneeze cascades', 'recurrent sneezing', 'violent sneezing', 'spontaneous sneezes', 'sudden sneezing',
        'blasting sneezes', 'paroxysmal sneezing', 'intense sneezing', 'frequent sneezing attacks', 'sneezing with watery eyes', 'sudden fit of sneezing', 'uncontrollable nasal reflex',
        'hayfever sneezing', 'sneeze bursts', 'non-stop sneezing', 'gasping after sneezing', 'nasal reflex reactions', 'irritated sneezing', 'allergic sneezing', 'multiple sneeze cycles'
    ],
    'swollen lymph nodes': [
        'swollen glands', 'lymph node swelling', 'enlarged lymph nodes', 'swelling in neck', 'lumps in neck', 'tender lymph nodes', 'painful lymph nodes', 'swelling near jaw',
        'lymphatic swelling', 'lymph node enlargement', 'swollen glands under arms', 'underarm lymph node swelling', 'swollen neck glands', 'increased lymph node size',
        'lymphatic system swelling', 'lumps under the skin', 'swollen lymphatic glands', 'painful lumps in neck', 'inflamed lymph nodes', 'lymph node tenderness', 'neck swelling',
        'uncomfortable lumps in neck', 'tender neck lumps', 'swollen lymph glands in groin', 'swollen lymph nodes in armpit', 'painful swelling in neck', 'inflamed glands',
        'lymph node tenderness under jaw', 'enlarged glands in the throat', 'neck lumps', 'swollen lymph nodes behind ears', 'tender swollen glands', 'neck lymphatic swelling',
        'swelling in the throat', 'pain in swollen glands', 'pain from swollen lymph nodes', 'inflamed and tender lymph nodes', 'lymphatic swelling with pain'
    ],
  'neck pain': [
    'stiff neck', 'sore neck', 'cervical pain', 'neck ache', 'aching neck', 'neck discomfort', 'pain in the neck','neck stiffness', 'tense neck muscles', 'painful neck movement', 'neck is sore',
    'muscle strain in neck', 'neck muscle soreness', 'tight neck muscles', 'chronic neck pain', 'acute neck pain', 'neck crick', 'neck tension', 'pinched nerve in neck', 'radiating neck pain', 
    'pain at the base of the skull', 'upper spine pain', 'neck injury pain', 'limited neck mobility', 'sharp neck pain', 'dull neck ache', 'neck strain', 'neck throbbing', 'neck is little sore',
    'burning sensation in neck', 'neck inflammation', 'neck tenderness', 'cervical spine discomfort', 'pain when turning head', 'pain along the side of neck', 'pain in back of neck', 'stabbing neck pain',
    'tension in upper neck', 'cervical tension', 'neck muscle fatigue', 'pain in neck muscles','sensation of pressure in neck', 'neck pain from poor posture', 'neck pain from sleeping wrong'
],

    'joint pain': [
        'joint ache', 'joint discomfort', 'joint inflammation', 'joint stiffness', 'joint tenderness', 'pain in joints', 'arthritic pain', 'swollen joint', 'joint soreness',
        'joint irritation', 'musculoskeletal pain', 'painful joints', 'joint stiffness', 'grating joint feeling', 'aching joints', 'joint tightness', 'joint swelling', 'rheumatoid pain', 'stiff joints',
         'painful shoulders', 'pain in elbows', 'wrist joint pain', 'ankle joint pain', 'hip joint pain', 'persistent joint pain', 'severe joint pain', 'uncomfortable joint pressure',
        'popping joints', 'clicking joints', 'cracking joints', 'joint inflammation in fingers', 'inflamed joints','excessive joint pain',
        'joint tenderness', 'joint soreness from strain', 'arthralgia', 'sharp joint pain', 'stabbing joint pain', 'chronic joint ache', 'inflamed elbow joints',
         'joint damage', 'strained joint', 'degenerative joint disease', 'discomfort in joints', 'dull joint ache', 'acute joint pain', 'swollen hands', 'weakening joint flexibility',
        'muscle and joint discomfort', 'continuous joint pain', 'painful back joints', 'arthritic inflammation', 'joint locking', 'joint clicking', 'joint popping', 'joint dislocation'

    ],
   'diarrhea': [
        'loose stools', 'frequent bowel movements', 'watery stools', 'runny stools', 'loose bowels', 'urgent need to defecate', 'watery bowel movements', 'explosive diarrhea',
        'stomach upset with diarrhea', 'frequent trips to the bathroom', 'diarrhea with cramping', 'abnormal stool consistency', 'watery feces', 'fecal urgency', 'loose bowel movement',
        'urgent diarrhea', 'persistent diarrhea', 'morning diarrhea', 'stomach flu diarrhea', 'digestive distress', 'frequent liquid stools', 'runny bowel movements', 'intense bowel movements',
        'diarrheal episode', 'loose stool rush', 'urgent diarrhea attack', 'acute diarrhea', 'chronic diarrhea', 'pale watery stools', 'stomach churn with diarrhea', 'intestinal upset',
        'frequent bowel clearing', 'fluid-filled stools', 'non-stop diarrhea', 'gut infection diarrhea', 'dehydrating diarrhea', 'uncontrolled liquid stools', 'loose stool frequency',
        'constantly running to the bathroom', 'liquid-filled intestines', 'intense gastrointestinal upset', 'abnormally frequent bowel movements', 'severe bowel looseness', 'bowel irregularity',
        'involuntary liquid stools', 'gassy diarrhea', 'splashy diarrhea', 'digestive upset causing liquid stools', 'diarrhea with abdominal pain'
    ],
    'vomiting': [
        'throwing up', 'puking', 'stomach upset', 'retching', 'emesis', 'nausea with vomiting', 'forcefully throwing up', 'heaving', 'vomiting episodes', 'sick stomach',
        'gagging', 'expelling stomach contents', 'stomach expulsion', 'violent vomiting', 'repeated vomiting', 'uncontrollable vomiting', 'upchucking', 'spitting up', 'retching reflex',
        'forceful expulsion of food', 'involuntary stomach release', 'emetic response', 'feeling of needing to vomit', 'gag reflex triggering', 'chronic vomiting', 'severe vomiting',
        'nausea-induced vomiting', 'unpleasant stomach eruption', 'stomach contents expelled forcefully', 'gastrointestinal purge', 'expulsion of gastric contents', 'violent heaving',
        'nauseated vomiting', 'vomit-induced gagging', 'stomach-purging sensation', 'retching uncontrollably', 'throwing up after eating', 'puking episodes', 'sick and throwing up',
        'puking from irritation', 'regurgitating food', 'empty stomach vomiting', 'morning sickness vomiting', 'nausea attacks with vomiting', 'emesis due to motion sickness', 'heaving up'
    ],

    'ear pain': [
        'ear ache', 'pain in the ear', 'ear discomfort', 'ear irritation', 'painful ear', 'throbbing ear ache', 'sharp ear pain', 'dull ear pain', 'stabbing pain in ear', 'ringing ear pain',
        'pressure in ear', 'ear sensitivity', 'intense ear discomfort', 'itchy ear', 'swollen ear', 'ear tenderness', 'ear pulsations', 'persistent ear pain', 'ear infection pain',
        'ear tenderness', 'pain behind ear', 'soreness in ear', 'ear pressure', 'ear inflammation', 'ear ache from cold', 'stuffy ear pain', 'pain in ear canal', 'ear ache when swallowing',
        'painful inner ear', 'hearing sensitivity with pain', 'fluid in ear causing pain', 'acute ear pain', 'chronic ear ache', 'pain after water exposure', 'ear infection causing pain',
        'tender ear lobes', 'painful eardrum', 'painful earful feeling', 'pounding ear pain', 'sharp stabbing ear ache', 'swollen ear canal', 'eardrum sensitivity', 'sharp pressure sensation in ear',
        'soreness in ear cavity', 'clogged ear with pain', 'throbbing sensation in ear', 'ear ache during sleep', 'pain in eardrum', 'ear hurts', 'pain in eardrums'
    ],
    'back pain': [
        'lower back pain', 'upper back pain', 'pain in lower back', 'pain in upper back', 'spinal pain', 'pain in the back', 'back is paining', 'achy back', 'sharp back pain', 'dull back pain', 'severe back pain', 'chronic back pain',
        'stiff back', 'muscle soreness in back', 'pressure in lower back', 'pain between shoulder blades', 'sharp pain in spine', 'pain in back muscles', 'backache from lifting',
        'back discomfort', 'spinal discomfort', 'pain in lumbar region', 'back injury', 'radiating back pain', 'tight back muscles', 'spinal stiffness', 'lower back strain', 'back pain after exercise',
        'muscle strain in the back', 'burning sensation in back', 'intense back pain', 'nagging back pain', 'sharp stabbing pain in lower back', 'back tension', 'sore spine',
        'pinched nerve in back', 'back spasms', 'pain when bending', 'pain while standing up', 'pressure in upper back', 'burning pain in the back', 'pain in the sacral region',
        'pain with back movement', 'back pain when sitting', 'lower back discomfort', 'muscular back pain', 'upper spinal discomfort', 'radiating pain down the back', 'back is sore'
    ],
    'cold': [
        'Common cold', 'head cold', 'mild viral infection', 'slight sniffles', 'catching a cold', 'seasonal cold', 'chest cold', 'light upper respiratory infection', 'mild sniffle bug',
        'standard cold virus', 'low-grade nasal virus', 'mild runny-nose ailment', 'basic rhinovirus', 'everyday cold symptoms', 'short-term sniffles', 'routine winter bug', 'easy viral cold',
        'minor head stuffiness illness', 'typical seasonal illness', 'cold symptoms', 'stuffy nose cold', 'mild sore throat with cold', 'cold with slight fever', 'cough with cold',
        'runny nose cold', 'sneezing with cold', 'mild chest congestion', 'low-grade cold infection', 'itchy throat cold', 'general cold symptoms', 'nasal congestion from cold',
        'watery eyes with cold', 'mild head congestion', 'cold-related fatigue', 'chilly viral infection', 'upper respiratory cold', 'typical cold symptoms', 'stuffy feeling from cold',
        'cough and cold', 'runny nose from cold', 'frequent sneezing cold', 'cold-related chills', 'feeling chilled from cold', 'aching muscles with cold', 'minor fever with cold',
        'slight cold discomfort', 'cold-induced sore throat' ,'feeling cold'
    ],
    'sweat': [
        'sweating', 'excessive sweating', 'unusual sweating', 'profuse sweating', 'drenched in sweat', 'perspiring heavily', 'sweating buckets', 'clammy sweating', 'dripping perspiration',
        'bead-like sweat on skin', 'moisture streaming down face', 'uncontrollable sweating', 'soaked in sweat', 'overactive sweat glands', 'sweaty and damp skin', 'sweat-soaked clothes',
        'constant perspiration', 'sticky sweat', 'salty perspiration', 'glistening with sweat', 'sweat trickling down spine', 'nervous sweating', 'stress-induced sweat', 'drenching perspiration',
        'sweat-laden body', 'humid feeling', 'slick skin', 'warm moisture on skin', 'sweat beads forming everywhere', 'bodily moisture overload', 'persistent dampness', 'sweaty palms and forehead',
        'rivers of sweat', 'sweat dripping off hairline', 'sweat-soaked sheets', 'nocturnal sweating', 'smelly perspiration', 'standing in a pool of sweat', 'sweat forming under arms', 'shiny perspiring face',
        'sweat running down temples', 'sweat-induced chafing', 'slick and slippery feeling', 'sweating like in a steam room', 'permanent dampness', 'sweat stains on clothing'
    ],
    'swelling': [
        'swollen area', 'edema', 'swelling of body part', 'fluid retention', 'swollen body part', 'inflamed tissue', 'swollen limbs', 'puffiness',
        'swollen joints', 'swollen ankle', 'swollen hands', 'swollen feet', 'localized swelling', 'swollen skin', 'swelling in legs', 'swelling due to injury', 'swollen belly',
        'swollen face', 'swollen knees', 'edematous swelling', 'painful swelling', 'swollen extremities', 'swelling from infection', 'swelling from trauma', 'swelling after surgery',
        'swelling of the face', 'swelling under the skin', 'swollen throat', 'swelling with discomfort', 'puffy hands', 'swelling after a fall', 'generalized swelling', 'swelling in eyes',
        'swelling from arthritis', 'swelling around wounds', 'enlarged tissue area', 'swelling from allergic reaction', 'swelling in body cavity', 'swelling around the joints','bruising'
    ],
    'tremor': [
        'shaking', 'shivering', 'twitching', 'involuntary movements', 'nervous shaking', 'muscle tremors', 'rhythmic shaking', 'trembling hands', 'uncontrolled muscle movement',
        'shaking limbs', 'twitchy fingers', 'uncontrolled tremor', 'flickering motion', 'trembling body', 'shaky movements', 'muscle spasms', 'jerking', 'shivering body', 'shaky hands',
        'shaking from cold', 'nervous tremors', 'trembling sensation', 'shuddering', 'uncontrollable shaking', 'flickering muscles', 'twitching eyes', 'nervous jerks', 'shaky fingers',
        'twitching limbs', 'muscle jerks', 'nervous body shakes', 'subtle muscle tremors', 'involuntary shaking', 'feeling of tremors', 'trembling body parts', 'sporadic body shaking',
        'hand shaking', 'shaky voice', 'rhythmic tremors', 'shivering fingers', 'body quivering', 'body shudders', 'shaking from anxiety'
    ],
    'chills': [
        'Shivering', 'trembling with cold', 'goosebumps', 'feeling cold inside', 'uncontrollable shaking', 'teeth chattering', 'feeling frosty', 'quivering limbs', 'body shaking from cold',
        'icy tremors', 'frigid vibrations', 'quaking with chill', 'hair standing on end', 'trembling internally', 'spasmodic shivers', 'cold-induced tremble', 'chilled to the bone',
        'freezing sensation', 'vibrating with cold', 'small uncontrollable shakes', 'persistent shuddering', 'subtle shivers', 'prickly gooseflesh', 'frost-like feeling', 'quivery muscles',
        'rattled by chill', 'shudders running down spine', 'uncontrollable cold tremors', 'shaky fingers and toes', 'rattling teeth', 'jittering from cold', 'frigid trembles',
        'cold-induced shaking', 'body frozen in chills', 'deep chills', 'numbing cold'
    ],

    'eye pain': [
        'ocular pain', 'eye discomfort', 'pain in the eye', 'eye ache', 'sore eye', 'sharp pain in the eye', 'pain around the eyes', 'painful vision', 'pain behind the eye',
        'irritation in the eye', 'burning sensation in the eye', 'dry eye pain', 'stabbing eye pain', 'eye strain', 'pressure in the eye', 'throbbing in the eye',
        'sensitive eyes', 'eye tenderness', 'aching in the eye', 'eye inflammation', 'pulsing pain in the eye', 'intense eye discomfort', 'distorted vision from pain', 'foreign body sensation in the eye',
        'sharp eye ache', 'vision-related pain', 'severe eye pain', 'sharp stabbing pain in the eye', 'pain in the eyeball', 'tired eye pain', 'swollen eye discomfort', 'throbbing behind the eyes',
        'pain from light sensitivity', 'pain after reading', 'pain when blinking', 'gritty feeling in the eyes', 'intense eye pressure', 'pain around the eyelids', 'blurry vision with pain', 'puffy eyes with pain',
        'pain near the cornea', 'stinging pain in the eye', 'pain with redness in the eye', 'ocular discomfort', 'persistent eye pain', 'painful feeling when moving eyes', 'pressure sensation in the eyes',
        'pain from eye strain', 'pain with dry eyes', 'eye irritation', 'eye swelling', 'eye tearing','pain in my eye','pain in my eyes'
    ],
   
    'nose pain': [
        'pain in the nose', 'nasal pain', 'sinus pain', 'stabbing pain in the nose', 'sharp nasal discomfort', 'painful sinus area', 'throbbing pain in the nose', 'blocked nose pain',
        'pain from sinusitis', 'nasal congestion pain', 'pain from cold in the nose', 'swollen nose', 'pressure in the sinuses', 'pain from a cold', 'tenderness in the nose', 'painful nostrils',
        'pain from nasal polyps', 'pain around the nostrils', 'nosebleed-related pain', 'pain with nasal drip', 'stuffy nose pain', 'pain due to allergies', 'burning sensation in the nose',
        'painful nasal congestion', 'aching nose', 'chronic nasal pain', 'pain when breathing through nose', 'nose pressure', 'pain at the bridge of the nose', 'pain in nasal cavity', 'itchy nose with pain',
        'pain from external nose injury', 'pain from sniffles', 'swelling in the nasal area', 'facial pain near the nose', 'pain from sinus congestion', 'painful nasal passages', 'pain in the septum',
        'pain from sniffing'
    ],
    'throat pain': [
        'sore throat', 'pain in the throat', 'scratchy throat', 'throat discomfort', 'painful swallowing', 'irritated throat', 'dry throat pain', 'burning sensation in the throat', 'throat tenderness',
        'throat scratchiness', 'swollen throat', 'pain from tonsillitis', 'strep throat pain', 'pain from a cold', 'inflammation of the throat', 'sore throat with fever', 'pain in the tonsils',
        'pain from acid reflux', 'hoarse throat', 'tight throat pain', 'painful voice box', 'pain in the larynx', 'pain with coughing', 'pain with dry mouth', 'pain with difficulty swallowing',
        'pain in the pharynx', 'pain with swollen glands', 'throat congestion', 'pain after excessive talking', 'pain from dry air', 'pain from smoking', 'throat dryness', 'severe throat discomfort',
        'pain after eating', 'pain from post-nasal drip', 'sore and swollen throat', 'pain from throat infection', 'swollen tonsils with pain', 'tightness in the throat', 'pain from sore mouth',
        'stabbing throat pain', 'pain when swallowing food', 'burning throat pain'
    ],
    'jaw pain': [
        'pain in the jaw', 'jaw discomfort', 'jaw ache', 'pain in the temporomandibular joint', 'TMJ pain', 'painful jaw muscles', 'pain from jaw clenching', 'tooth-related jaw pain',
        'sharp jaw pain', 'throbbing jaw pain', 'jaw tension', 'muscle pain in the jaw', 'pain from grinding teeth', 'jaw stiffness', 'pain in the lower jaw', 'pain from jaw injury', 'pain near the jawline',
        'pain around the mouth area', 'pain when chewing', 'discomfort in the jaw', 'jaw lock', 'jaw popping pain', 'pain around the ear and jaw', 'pain from dental issues', 'pain with jaw movement',
        'swollen jaw area', 'pain in the temporomandibular joint', 'facial pain near the jaw', 'pain from misaligned teeth', 'jaw pain from stress', 'jaw swelling', 'pain when yawning',
        'sharp pain in jaw joint', 'stiffness in jaw', 'dull aching jaw pain', 'pain from jaw trauma', 'pain from wisdom teeth', 'jaw clicking', 'pain in the side of the jaw', 'pain from jaw misalignment',
        'pain after jaw surgery', 'pain during biting', 'jaw discomfort while sleeping'
    ],
    'tooth pain': [
        'toothache', 'dental pain', 'pain in the tooth', 'sharp tooth pain', 'throbbing tooth pain', 'pain from cavity', 'pain from tooth infection', 'pain in the gums', 'sensitive teeth pain',
        'pain from a dental abscess', 'pain when chewing', 'pain from tooth decay', 'pain with tooth sensitivity', 'pain after dental work', 'pain in the tooth root', 'pain from tooth fracture',
        'pain from gum disease', 'tooth pressure', 'pain after eating', 'pain when brushing teeth', 'pain from wisdom teeth', 'pain in the molars', 'pain from misaligned teeth', 'dull tooth pain',
        'pain from tooth eruption', 'pain from a cracked tooth', 'pain with swollen gums', 'constant toothache', 'sharp shooting tooth pain', 'pain from tooth trauma', 'dental discomfort',
        'pain in the tooth nerve', 'pain from filling', 'gum-related tooth pain', 'pain from chipped tooth', 'pain from teeth grinding', 'pain from dental infection', 'pain from plaque buildup',
        'tooth pressure with pain', 'pain from oral sores', 'pain in upper teeth', 'severe tooth pain', 'pain in front teeth'
    ],
    'chest pain': [
        'pain in the chest', 'chest discomfort', 'tightness in chest', 'pressure in the chest', 'sharp chest pain', 'tight chest feeling', 'stabbing chest pain', 'burning chest pain', 'aching chest',
        'chest heaviness', 'pain in the breastbone', 'pain radiating from chest', 'dull chest pain', 'pain from heartburn', 'pain from acid reflux', 'pain in the ribs', 'pain in the upper chest',
        'sharp stabbing pain in chest', 'chest tightness', 'pain under the sternum', 'pain when breathing deeply', 'feeling of chest pressure', 'pain from pulmonary issues', 'heart-related chest pain',
        'sharp pain in the breastbone', 'radiating chest discomfort', 'pain when moving', 'pain from costochondritis', 'pain from muscle strain in chest', 'deep chest discomfort', 'pain from anxiety',
        'dull aching chest pain', 'pain in the upper left chest', 'pain when lying down', 'sore chest', 'pain from trauma to chest', 'persistent chest pain', 'discomfort after exercise',
        'pain in the center of the chest', 'pain from chest cold', 'pain in the chest while breathing', 'sore chest area', 'pain in the left side of the chest', 'pain from coughing', 'pain from deep breathing'
    ],

    'knee pain': [
        'knee discomfort', 'pain in the knee', 'painful knees','joint pain in the knee', 'knee ache', 'sharp knee pain', 'throbbing knee pain', 'stabbing pain in the knee', 'pain in the knee joint',
        'pain from knee injury', 'pain from knee strain', 'knee swelling', 'pain when bending knee', 'pain while walking', 'pain after exercise', 'pain from knee overuse', 'pain with knee movement',
        'pain in the kneecap', 'pain on the outer knee', 'pain on the inner knee', 'pain from ligament injury', 'pain from torn meniscus', 'sharp pain in the knee cap',
        'knee joint inflammation', 'pain when climbing stairs', 'chronic knee pain','pain with swelling', 'pain from running', 'pain from twisting knee', 'pain when standing up', 'knee tenderness', 'pain from patella dislocation',
        'pain with knee instability','pain in knees','joint pain', 'pain from bursitis', 'aching knees','sore knees','pain with osteoarthritis', 'pain from cartilage damage', 'pain after knee surgery', 'pain in the back of the knee', 'pain in my knee', 'pain in my knees'
    ],
    'foot pain': [
        'pain in the foot', 'plantar pain', 'foot discomfort', 'foot ache', 'pain in the heel', 'sharp foot pain', 'throbbing foot pain', 'pain from foot injury', 'pain in the arch',
        'pain from flat feet', 'pain from bunions', 'pain in the toes', 'pain from corns', 'pain from calluses', 'pain from foot fractures', 'pain from wearing tight shoes', 'pain with walking',
        'pain from arthritis in foot', 'swollen foot', 'pain in the sole', 'pain when standing', 'pain from sprained ankle', 'pain from tendinitis', 'sharp pain in the foot arch', 'pain in foot joints',
        'pain in the ball of the foot', 'numbness in foot with pain', 'heel pain', 'pain from Morton’s neuroma', 'pain in foot after exercise', 'pain from overuse', 'pain after running', 'foot cramping pain',
        'pain after standing for long periods', 'pain in the toes after walking', 'sharp heel pain', 'foot pain from nerve issues', 'pain from diabetic neuropathy', 'foot pain from swelling', 'pain after wearing heels',
        'pain in feet', 'feet pain'
    ],
    'ankle pain': [
        'ankle discomfort', 'pain in the ankle', 'twisted ankle pain', 'pain from sprained ankle', 'swollen ankle', 'sharp ankle pain', 'throbbing pain in the ankle', 'pain when walking',
        'pain after ankle injury', 'pain from overuse', 'pain after exercise', 'pain with ankle movement', 'pain with swelling', 'pain from torn ligament', 'pain in the outer ankle', 'pain in the inner ankle',
        'pain in the ankle joint', 'pain from ligament strain', 'pain from ankle fracture', 'ankle tenderness', 'pain with ankle instability', 'pain when standing', 'sharp pain in the ankle',
        'pain in ankle tendon', 'pain after running', 'pain from ankle arthritis', 'pain with twisting', 'pain in ankle after jumping', 'pain in the Achilles tendon', 'stabbing pain in ankle',
        'pain with ankle sprain', 'ankle bruising', 'pain when walking on uneven surfaces', 'pain when bending the foot', 'pain in the heel of the ankle', 'pain during sports activities', 'pain when stretching ankle'
    ],
     'wrist pain': [
        'pain in the wrist', 'wrist discomfort', 'carpal pain', 'wrist ache', 'pain in the wrist joint', 'wrist inflammation', 'swollen wrist', 'stiff wrist pain', 'pain from repetitive strain',
        'tenderness in the wrist', 'sharp wrist pain', 'throbbing wrist pain', 'pain after wrist injury', 'pain from wrist overuse', 'wrist sprain pain', 'pain in the wrist tendons', 'wrist joint stiffness',
        'pain with wrist movement', 'pain during wrist flexion', 'pain in wrist ligaments', 'carpal tunnel syndrome pain', 'pain from arthritis in the wrist', 'pain with wrist rotation', 'pain in the wrist after typing',
        'wrist discomfort from injury', 'pain around wrist bones', 'dull wrist pain', 'pain when lifting objects', 'pain in the wrist after exertion', 'pain from wrist fractures', 'wrist tendonitis pain',
        'pain after hand movements', 'pain in the wrist when gripping', 'pain with wrist extension', 'stiff wrist from overuse', 'sharp sensation in the wrist', 'pain after extended typing', 'pain with wrist bending',
        'swollen joints in the wrist', 'wrist pain with numbness', 'pain around wrist bones after activity', 'pain in the carpal region', 'wrist discomfort with tingling sensation', 'pain after sports activity'
    ],
    'hand pain': [
        'hand discomfort', 'pain in the hand', 'aching hand', 'sharp hand pain', 'throbbing hand pain', 'pain in hand joints', 'pain in the palm of the hand', 'pain in the fingers', 'pain in the knuckles',
        'pain from hand injury', 'swollen hand', 'pain with hand movement', 'hand strain pain', 'numbness in the hand', 'pain after gripping', 'pain in the thumb', 'pain from arthritis in the hand',
        'pain from repetitive motions', 'pain from carpal tunnel syndrome', 'pain from hand overuse', 'hand joint pain', 'pain from hand sprain', 'pain from tendonitis in the hand', 'pain in the wrist with hand use',
        'sharp pain when holding objects', 'burning pain in the hand', 'painful hand cramps', 'dull hand pain', 'pain from hand fracture', 'pain from swelling in the hand', 'joint stiffness in the hand',
        'pain from typing', 'pain after using the hand excessively', 'pain when stretching the hand', 'pain in hand from trauma', 'pain when writing', 'pain with hand dexterity', 'pain in the hand after exercise',
        'muscle pain in the hand', 'pain from cold in the hand', 'pain after lifting objects'
    ],
    'arm pain': [
        'pain in the arm', 'upper limb pain', 'arm discomfort', 'sharp arm pain', 'throbbing arm pain', 'pain in the elbow', 'pain in the shoulder', 'pain in the forearm', 'pain in the biceps',
        'pain from arm injury', 'pain from repetitive arm movement', 'pain from tendonitis in the arm', 'muscle pain in the arm', 'nerve pain in the arm', 'pain from elbow strain', 'pain in the upper arm muscles',
        'pain from arm sprain', 'pain in the wrist and arm', 'stiffness in the arm', 'swollen arm', 'pain when moving the arm', 'burning pain in the arm', 'aching in the arm', 'arm cramping',
        'pain from lifting with the arm', 'pain when raising the arm', 'pain from overuse of the arm', 'pain from arm fracture', 'pain in the arm muscles after exercise', 'pain from muscle strain in the arm',
        'pain from joint inflammation', 'sharp pain in the arm muscles', 'pain in the elbow joint', 'pain in the shoulder joint', 'dull arm pain', 'pain in the forearm when lifting', 'shooting arm pain',
        'nerve-like pain in the arm'
    ],
    'leg pain': [
        'pain in the leg', 'lower limb pain', 'leg discomfort', 'muscle pain in the leg', 'pain in the thigh', 'pain in the calf', 'pain in the knee', 'pain in the shin', 'pain from leg injury',
        'sharp leg pain', 'throbbing leg pain', 'aching leg pain', 'pain in the leg muscles', 'pain in the leg joints', 'pain when walking', 'pain from leg cramps', 'pain after leg exercise',
        'pain after running','pain in my legs','legs are paining','pain in leg', 'pain from overuse', 'pain in the hamstring', 'pain from leg sprain', 'muscle soreness in the leg', 'pain in the calf after activity', 'pain from leg fractures',
        'burning pain in the leg', 'pain from restless legs', 'pain when standing', 'pain in the thigh after sitting', 'pain in the foot and leg', 'pain with leg movement', 'pain from sciatica',
        'leg pain from sitting too long', 'pain when bending the leg', 'pain in the shin muscles', 'swollen leg', 'pain from arthritis in the leg', 'dull pain in the leg', 'sharp pain in the lower leg',
        'pain when walking on uneven ground', 'pain in the lower back and leg'
    ],
    'confusion': [
        'disorientation', 'muddled thinking', 'mental fog', 'trouble thinking clearly', 'brain fog', 'cognitive cloudiness', 'puzzled state', 'jumbled thoughts', 'incoherent reasoning', 'tangled mental process',
        'unclear comprehension', 'befuddled mind', 'scrambled logic', 'perplexed state', 'hazy understanding', 'blurred mental picture', 'fuzzy reasoning', 'perplexity', 'baffled intellect',
        'uncertain grasp', 'foggy mental landscape', 'clouded judgment', 'unclear headspace', 'mixed-up thoughts', 'lack of mental clarity', 'distorted perspective', 'murky understanding',
        'minds in knots', 'head scrambled eggs feeling', 'no clear thread of thought', 'haphazard reasoning', 'bewildered stance', 'lost mental bearings', 'mental haze', 'unclear mental signals',
        'vague cognitive process', 'mental static', 'mentally adrift', 'diluted focus', 'no sharpness in mind', 'blinking confusion', 'unsure mental footing', 'perplexed awareness',
        'reduced mental acuity', 'messy mental white noise'
    ],
    'hip pain': [
        'pain in the hip', 'hip discomfort', 'hip joint pain', 'pain from hip arthritis', 'sharp hip pain', 'throbbing hip pain', 'pain in the hip joint', 'pain in the hip area', 'pain from hip injury',
        'hip inflammation', 'pain from hip strain', 'pain from bursitis in the hip', 'pain when moving the hip', 'pain from overuse of the hip', 'pain in the groin area', 'pain during walking',
        'pain from hip fracture', 'pain after standing for a long time', 'pain from hip surgery', 'pain when lying on the hip', 'pain with hip rotation', 'pain in the side of the hip',
        'pain in the front of the hip', 'pain from sciatica', 'sharp hip joint pain', 'pain from hip flexor strain', 'deep hip pain', 'pain from hip dislocation', 'aching hip pain',
        'pain from muscle strain around the hip'
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
        'drifting away from details', 'no anchor to past events'
    ],
  'hallucination': [
    'delusion', 'illusion', 'false perception', 'sensory distortion', 'visual disturbance', 'auditory hallucination',
    'perceptual distortion', 'false sensory experience', 'phantom perception', 'psychotic episode', 'imagined sight', 'imagined sound', 'mind illusion',
    'sensory misperception', 'hallucinatory experience', 'out-of-body experience', 'visual illusion', 'auditory illusion', 'mental delusion', 'altered reality'
],

  'loss of appetite': [
    'decreased appetite', 'reduced appetite', 'appetite loss', 'lack of appetite', 'poor appetite', 'no desire to eat', 'loss of interest in food', 'unwillingness to eat',
    'inability to eat', 'diminished appetite', 'eating less', 'loss of hunger', 'food aversion', 'food intolerance', 'decreased desire to eat', 'lack of hunger',
    'decrease in food intake', 'disinterest in eating', 'feeling full quickly', 'loss of taste for food', 'sudden loss of appetite', 'absence of hunger', 'nausea with food',
    'difficulty eating', 'reduced food consumption', 'lack of craving for food', 'feeling satiated quickly', 'loss of appetite due to illness', 'loss of appetite from stress',
    'loss of appetite from medication', 'anorexia', 'anorexia nervosa', 'feeling no appetite', 'feeling disinterested in food', 'poor food intake', 'reduced food desire'
],

'constipation': [
    'difficulty passing stool', 'infrequent bowel movements', 'hard stools', 'painful bowel movements', 'feeling of incomplete evacuation', 'straining during bowel movement',
    'constipated', 'dry stool', 'difficulty in defecation', 'delayed bowel movements', 'irregular bowel movements', 'hard and dry stool', 'chronic constipation', 'temporary constipation',
    'trouble with bowel movements', 'trouble passing stool', 'slow bowel transit', 'stool retention', 'decreased bowel movement frequency', 'bowel sluggishness',
    'straining to poop', 'bowel movement difficulty', 'slow bowel function', 'lack of bowel movement', 'intestinal irregularity'
],

'flu': [
    'influenza', 'seasonal flu', 'viral flu', 'flu virus', 'common flu', 'flu infection', 'respiratory flu', 'flu-like symptoms', 'flu illness',
    'acute influenza', 'viral infection', 'cold and flu', 'influenza virus', 'flu sickness', 'contagious flu', 'pandemic flu',
    'swine flu', 'avian flu', 'H0N1 flu', 'influenza strain', 'cough and flu', 'flu symptoms', 'body aches from flu', 'cold flu',
    'influenza fever', 'flu epidemic', 'general flu discomfort', 'influenza outbreak', 'flu season illness', 'sudden flu'
],

'infection': [
    'contamination', 'infectious disease', 'germ infection', 'bacterial infection', 'viral infection', 'fungal infection', 'parasite infection', 'microbial infection',
    'pathogen invasion', 'infected area', 'infection outbreak', 'systemic infection', 'local infection', 'wound infection', 'skin infection', 'respiratory infection',
    'urinary tract infection', 'ear infection', 'sinus infection', 'blood infection', 'sepsis', 'foodborne illness', 'infected tissue', 'infection of the bloodstream',
    'infection of the lungs', 'bacterial contamination', 'inflammation from infection', 'infectious agent', 'disease-causing infection', 'contagion', 'infection symptoms',
    'chronic infection', 'acute infection', 'health infection', 'infection spread', 'infection risk', 'infectious condition', 'contagious disease'
],

'inflammation': [
    'inflammatory response', 'immune response', 'chronic inflammation', 'acute inflammation', 'inflammatory reaction', 'inflammation of tissues', 'inflammation in the body',
    'inflammation of the skin', 'joint inflammation', 'internal inflammation', 'inflammatory condition', 'cellular inflammation', 'inflammatory disorder', 'local inflammation',
    'systemic inflammation', 'inflammation from infection', 'inflammation from injury', 'inflammation from disease', 'autoimmune inflammation', 'inflammation in the joints',
    'stiffness from inflammation', 'inflammation from trauma', 'inflammation due to allergies'
],

'cramp': [
    'paining cramp', 'cramped muscle', 'cramping sensation', 'cramping'
],

'bleeding': [
    'blood loss', 'hemorrhage', 'hemorrhaging', 'bloodshed', 'wound bleeding', 'internal bleeding', 'external bleeding', 'bleeding from injury', 'blood flow',
    'spurting blood', 'bleeding wound', 'gushing blood', 'cut bleeding', 'profuse bleeding', 'minor bleeding', 'heavy bleeding', 'excessive bleeding',
    'periodic bleeding', 'bleeding from incision', 'bleeding from surgery', 'abnormal bleeding', 'uncontrolled bleeding', 'bleeding disorder'
],

'irritation': [
    'annoyance', 'chronic irritation', 'temporary irritation', 'allergic irritation', 'irritated feeling'
],

'anxiety': [
    'worry', 'unease', 'stress', 'fear', 'apprehension', 'nervous tension', 'anxiousness', 'nervous anxiety', 'social anxiety', 'generalized anxiety', 'anxiety disorder', 
    'anticipatory anxiety', 'anxiety attack', 'apprehensive feeling', 'distress', 'emotional unease', 'worrying', 'overthinking', 'mental tension'
],

'depression': [
    'sadness', 'melancholy', 'despair', 'low mood', 'dismay', 'hopelessness', 'discouragement', 'despondency', 'blues', 'dejectedness', 'very sad', 'sad',
    'feeling down', 'feeling hopeless', 'loss of interest', 'unhappiness', 'mental exhaustion', 'loss of joy', 'major depressive disorder',
    'clinical depression', 'chronic depression', 'depressive episode', 'anhedonia', 'negative mood', 'downheartedness'
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
    'insulin-dependent diabetes', 'pre-diabetes', 'diabetic symptoms', 'diabetic complications', 'diabetes management', 'diabetes treatment'
],

'weight loss': [
    'fat loss', 'loss of body weight', 'slimming down', 'losing pounds', 'weight reduction', 'weight management', 'fat burning', 'weight cut',
    'body slimming', 'reduction in weight', 'fat shedding', 'calorie burning', 'trimming down', 'losing inches', 'dropping weight', 'healthy weight loss',
    'body fat reduction', 'weight loss journey', 'sustainable weight loss', 'rapid weight loss', 'gradual weight loss', 'controlled weight loss',
    'dieting', 'fitness weight loss', 'weight loss goals', 'weight going down', 'losing weight', 'loss of weight'
],

'hair loss': [
    'alopecia', 'balding', 'thinning hair', 'hair thinning', 'hair shedding', 'hair fall', 'scalp hair loss', 'bald spots', 'receding hairline',
    'hairline recession', 'hair breakage', 'excessive hair loss', 'temporary hair loss', 'pattern baldness', 'male pattern baldness', 'female pattern baldness',
    'androgenic alopecia', 'patchy hair loss', 'diffuse hair loss', 'hair loss due to stress', 'postpartum hair loss', 'age-related hair loss', 'genetic hair loss',
    'hair fall disorder', 'alopecia areata', 'hair loss condition', 'scalp thinning', 'hair loss treatment'
],

'blurred vision': [
    'vision impairment', 'unclear vision', 'fuzzy vision', 'distorted vision', 'foggy vision', 'hazy vision', 'blurry eyesight', 'impaired vision', 'cannot see properly',
    'vision distortion', 'clouded vision', 'poor vision', 'vision fuzziness', 'difficulty seeing clearly', 'blurred eyesight', 'visual disturbance',
    'unclear eyesight', 'visual impairment', 'blurry sight', 'sight distortion', 'vision problems', 'temporary blurred vision', 'chronic blurred vision',
    'blurry perception'
],

'numbness': [
    'loss of sensation', 'tingling', 'pins and needles', 'lack of feeling', 'reduced sensation', 'sensory loss', 'numb sensation', 'feeling of numbness',
    'numb feeling', 'sensory numbness', 'partial numbness', 'temporary numbness', 'persistent numbness'
],

'dry mouth': [
    'xerostomia', 'cottonmouth', 'parched mouth', 'thirsty mouth', 'dryness in the mouth', 'lack of saliva', 'reduced saliva production', 'mouth dryness',
    'sticky mouth', 'dryness of the oral cavity', 'uncomfortable dry mouth', 'dry tongue', 'thirsty feeling in the mouth', 'saliva deficiency', 'oral dryness',
    'mouth discomfort', 'dryness in the mouth and throat', 'sore dry mouth', 'dehydrated mouth', 'dryness due to medication', 'mouth feels dry', 'no saliva'
],

'frequent urination': [
    'urinary frequency', 'increased urination', 'urinary urgency', 'excessive urination', 'frequent trips to the bathroom', 'overactive bladder',
    'need to urinate often', 'urination urgency', 'recurrent urination', 'constant urination', 'frequent need to pee', 'urgent urination', 'pollakiuria',
    'urinary incontinence', 'nighttime urination', 'nocturia', 'constant need to urinate', 'increased frequency of urination'
],

'acne': [
    'pimples', 'blemishes', 'zits', 'whiteheads', 'blackheads', 'cystic acne', 'teenage acne', 'adult acne', 'pimple outbreaks', 'clogged pores', 'acne vulgaris', 'skin spots', 
    'face pimples', 'hormonal acne', 'acne lesions', 'acne scars', 'clogged follicles', 'sebaceous gland activity', 'oil acne', 'acne on the back', 'acne on the chest'
],

'difficulty swallowing': [
    'dysphagia', 'trouble swallowing', 'swallowing difficulty', 'painful swallowing', 'difficulty with swallowing', 'difficulty in swallowing food',
    'difficulty swallowing liquids', 'inability to swallow', 'swallowing discomfort', 'choking sensation', 'difficulty swallowing pills', 'food getting stuck',
    'difficulty in throat swallowing', 'swallowing obstruction', 'swallowing problems', 'gagging while swallowing', 'swallowing trouble',
    'feeling of blockage while swallowing'
],

'restlessness': [
    'unease', 'fidgeting', 'inability to relax', 'impatience', 'uneasiness', 'hyperactivity', 'jitteriness', 'inability to stay still', 'unsettledness',
    'fidgety feeling', 'lack of calm', 'shaky feeling'
],

'bloating': [
    'abdominal bloating', 'stomach bloating', 'gas buildup', 'swollen belly', 'feeling of fullness', 'abdominal distention',
    'overfull stomach', 'stomach discomfort', 'stomach swelling', 'intestinal bloating', 'bloated stomach', 'feeling puffed up', 'bloating sensation',
    'gassy stomach', 'stomach pressure', 'bloating after eating', 'digestive bloating', 'feeling bloated', 'bloating in the abdomen', 'gas pain',
    'cramping and bloating'
],

'gas': [
    'flatulence', 'intestinal gas', 'stomach gas', 'abdominal gas', 'gassy feeling', 'farting', 'passing gas', 'gas buildup', 'GERD',
    'wind', 'belching', 'burping', 'gas discomfort', 'gas pains', 'digestive gas', 'stomach is full', 'gassy stomach', 'trapped gas',
    'excessive gas', 'gas expulsion', 'intestinal discomfort', 'gas release', 'unwanted gas', 'gas in the stomach', 'passing wind'
],
'acidity': [
    'acid reflux', 'heartburn', 'sour stomach', 'acidic feeling', 'burning in chest', 'burning sensation','heartburning',
    'stomach acid', 'acid burps', 'sour taste in mouth', 'regurgitation', 'indigestion', 'upper abdominal burning',
    'acid in throat', 'stomach burning', 'gastric acid', 'acid buildup', 'acidic burping', 'throat burn',
    'reflux sensation', 'chest discomfort after eating', 'acid sensation', 'acidic regurgitation', 'acidic discomfort',
    'burning after meals', 'acid coming up', 'bitter taste in throat'
],

'indigestion': [
    'dyspepsia', 'digestive discomfort', 'fullness after eating', 'nausea after eating', 'acidic stomach', 'belching', 'feeling of heaviness', 'difficulty digesting', 'food intolerance', 'excessive burping'
],

'mouth sore': [
    'oral ulcer', 'canker sore', 'cold sore', 'blister in the mouth', 'mouth ulcer', 'painful mouth lesion', 'sores in the mouth', 'lesions on the gums',
    'painful spot in the mouth', 'mouth blister', 'mouth irritation', 'gum ulcer', 'sore inside the mouth', 'ulcerated mouth tissue', 'painful mouth spot',
    'burning mouth', 'painful tongue spot', 'sores on the lips', 'swollen mouth tissue', 'open mouth wound', 'oral lesion', 'mouth wound', 'infected mouth area'
],

'nosebleed': [
    'epistaxis', 'bleeding from the nose', 'nasal hemorrhage', 'nose bleeding', 'bloody nose', 'hemorrhaging from the nose', 'nose blood flow',
    'spontaneous nosebleed', 'anterior nosebleed', 'posterior nosebleed', 'frequent nosebleeds', 'nosebleed episode', 'bleeding nostrils',
    'blood coming out from the nose', 'nasal bleeding', 'bloody discharge from the nose', 'nasal passage bleeding', 'nosebleed symptoms', 'internal nasal bleeding',
    'nose injury bleeding'
],
'ear ringing': [
    'tinnitus', 'ringing in the ears', 'ear buzzing', 'ear noise', 'persistent ear sound', 'ear whistling', 'ear humming', 'sounds in the ears',
    'ear roaring', 'ringing sound in the ear', 'constant ringing', 'ear congestion', 'noises in the ear', 'buzzing in the ear', 'hissing in the ear',
    'whistling in the ear', 'high-pitched sound', 'low-pitched ear sound', 'phantom sounds', 'ear sensation', 'auditory disturbance'
],

'dark urine': [
    'dark-colored urine', 'dark yellow urine', 'brown urine', 'amber-colored urine', 'tea-colored urine', 'concentrated urine', 'urine with strong color',
    'deep yellow urine', 'urine discoloration', 'darkened urine', 'urine with reddish tint', 'dark brown urine', 'urine with high concentration', 'cloudy urine',
    'urine with abnormal color', 'dark urine caused by medication', 'urine with blood', 'urine with high pigment', 'strong urine color'
],

'blood in urine': [
    'hematuria', 'urinary blood', 'bloody urine', 'red urine', 'urine with blood', 'blood-tinged urine', 'blood in the urine stream', 'pink urine',
    'urinary tract bleeding', 'blood in the urinary tract', 'hemorrhagic urine', 'urinary bleeding', 'presence of blood in urine', 'blood in the bladder',
    'bloody discharge in urine', 'urine with reddish tint', 'blood in the urine sample', 'bleeding from the kidneys', 'blood in the urine after urination',
    'visible blood in urine', 'microscopic hematuria'
],

'blood in stool': [
    'hematochezia', 'rectal bleeding', 'bloody stool', 'stool with blood', 'bright red blood in stool', 'dark blood in stool', 'blood in the bowel movement',
    'blood-tinged stool', 'bloody feces', 'blood in feces', 'stool with reddish tint', 'blood in the stool sample', 'melena', 'dark tarry stool',
    'fecal blood', 'visible blood in stool', 'blood after bowel movement', 'stool with clots', 'bloody discharge from the rectum', 'abnormal stool color'
],

'high blood pressure': [
    'hypertension', 'elevated blood pressure', 'high BP', 'high arterial pressure', 'raised blood pressure', 'increased blood pressure', 'high systolic pressure',
    'high diastolic pressure', 'chronic hypertension', 'hypertensive condition', 'uncontrolled blood pressure', 'borderline hypertension', 'stage 0 hypertension',
    'stage 1 hypertension', 'persistent high blood pressure', 'high blood pressure disorder', 'abnormal blood pressure', 'hypertensive crisis', 'cardiovascular hypertension',
    'risk of hypertension', 'elevated BP', 'hypertensive state', 'BP is high'
],

'low blood pressure': [
    'hypotension', 'low BP', 'decreased blood pressure', 'low arterial pressure', 'reduced blood pressure', 'hypotensive condition', 'low systolic pressure',
    'low diastolic pressure', 'abnormally low blood pressure', 'postural hypotension', 'orthostatic hypotension', 'chronic hypotension', 'mild hypotension',
    'severe hypotension', 'low blood pressure symptoms', 'blood pressure drop', 'low cardiovascular pressure', 'circulatory hypotension', 'inadequate blood pressure',
    'dizzy blood pressure', 'low blood pressure episode', 'BP is low','low blood pressure'
],

'excessive thirst': [
    'polydipsia', 'intense thirst', 'uncontrollable thirst', 'extreme thirst', 'constant thirst', 'increased thirst', 'abnormal thirst', 'drinking more water', 'consuming more water',
    'compulsive thirst', 'thirsty all the time', 'unquenchable thirst', 'chronic thirst', 'intense desire to drink', 'frequent thirst', 'dehydration thirst','thirsty feeling',
    'abnormal fluid intake desire', 'thirst without relief', 'excessive fluid consumption', 'thirst due to dehydration', 'thirsty feeling', 'abnormal hydration needs'
],

'dehydration': [
    'fluid loss', 'water depletion', 'lack of hydration', 'electrolyte imbalance', 'insufficient water intake', 'dehydrating',
    'dehydrated state', 'water deficiency', 'reduced fluid levels', 'severe dehydration', 'mild dehydration', 'dehydration symptoms',
    'fluid imbalance', 'low body water', 'loss of body fluids', 'heat exhaustion', 'low hydration', 'hypohydration'
],

'red eyes': [
    'eye redness', 'bloodshot eyes', 'conjunctival redness', 'inflamed eyes', 'eye irritation', 'eyes with blood vessels',
    'swollen eyes', 'sore eyes', 'tired eyes', 'watery eyes', 'eye inflammation', 'pink eye', 'eye congestion', 'eye discomfort', 'eyes looking inflamed',
    'redness in the eyes', 'burning eyes', 'allergic eyes', 'eyes with a reddish tint'
],

'eye discharge': [
    'ocular discharge', 'eye mucus', 'eye secretion', 'eye crust', 'sticky eyes', 'eye pus', 'yellow eye discharge', 'clear eye discharge', 'water coming out of eyes',
    'green eye discharge', 'gunky eyes', 'eye drainage', 'teary eyes', 'eye secretion buildup', 'crusty eyes', 'eye fluid', 'excessive tear production',
    'morning eye crust', 'sticky eyelids', 'eye infection discharge', 'pus from the eye', 'watery eye discharge', 'eye discharge after sleep',
    'discharge from the tear duct', 'rheum in the eye','something coming out of eyes'
],

'ear discharge': [
    'otorrhea', 'ear fluid', 'ear drainage', 'pus from the ear', 'ear pus', 'ear infection discharge', 'fluid from the ear', 'ear secretion',
    'yellow ear discharge', 'green ear discharge', 'watery ear discharge', 'bloody ear discharge', 'ear mucus', 'crust in the ear', 'excessive ear fluid',
    'ear leakage', 'ear wax buildup', 'discharge from the ear canal', 'discharge from the middle ear', 'infection-related ear discharge', 'ear discharge after swimming',
    'ear drainage after injury', 'something coming out of ears'
],

'balance problem': [
    'vertigo', 'loss of balance', 'balance disorder', 'impaired balance', 'unsteady gait', 'lack of coordination', 'dizziness and unsteadiness',
    'balance difficulty', 'feeling of instability', 'spatial disorientation', 'postural imbalance', 'equilibrium disturbance', 'feeling off-balance',
    'gait imbalance', 'disequilibrium', 'vestibular dysfunction', 'balance issues', 'vertiginous symptoms', 'coordination problems', 'stumbling', 'feeling lightheaded'
],

'irregular heartbeat': [
    'arrhythmia', 'abnormal heartbeat', 'heart palpitations', 'irregular pulse', 'heart rhythm disorder', 'uneven heartbeat', 'skipped heartbeat',
    'rapid heartbeat', 'slow heartbeat', 'tachycardia', 'bradycardia', 'atrial fibrillation', 'ventricular fibrillation', 'heart flutter', 'irregular heart rhythm',
    'heart irregularities', 'palpitations', 'fluttering heart', 'cardiac arrhythmia', 'dysrhythmia', 'irregular pulse rate', 'heartbeat irregularity',
    'irregular heart rate', 'heart pounding'
],

'fainting': [
    'syncope', 'passing out', 'loss of consciousness', 'blackout', 'going unconscious', 'faint', 'collapse', 'temporary unconsciousness',
    'sudden fainting', 'faint spell', 'dizziness and fainting', 'dizzy spell', 'feeling lightheaded', 'near fainting', 'brief loss of consciousness',
    'head rush', 'staggering', 'fainting episode', 'loss of awareness', 'unconsciousness', 'momentary blackout', 'unconscious',
    'dizzy and lightheaded', 'feeling woozy'
],

'nervousness': [
    'nervous tension', 'nervous energy', 'uneasiness', 'nervous feeling', 'worry', 'uneasy feeling', 'jitters', 'nervous anticipation', 'fearfulness', 'shakiness', 'edginess',
    'fidgeting', 'mental unease', 'trepidation', 'feeling on edge', 'worrying', 'nervous butterflies'
],

'panic attack': [
    'anxiety attack', 'nervous breakdown', 'stress attack', 'overwhelming fear', 'intense fear episode', 'fight-or-flight response', 'panic episode', 'emotional breakdown',
    'sudden panic', 'heart-pounding anxiety', 'fear attack', 'panic episode', 'anxiety episode', 'intense panic', 'acute stress response', 'terror attack', 'nervous episode',
    'severe panic', 'acute emotional distress', 'uncontrollable fear', 'chronic panic disorder'
],

'mood swing': [
    'emotional swing', 'mood fluctuation', 'emotional rollercoaster', 'mood shift', 'mood change', 'mood variation', 'mood disorder',
    'rapid mood change', 'emotional instability', 'mood instability', 'mood alteration', 'emotional shift', 'temper fluctuation',
    'emotional lability', 'mood fluctuations', 'unstable mood', 'irregular mood', 'affective swing', 'mood imbalance', 'emotional outbursts',
    'highs and lows', 'emotional extremes'
],

'difficulty concentrating': [
    'inability to focus', 'lack of focus', 'poor concentration', 'trouble focusing', 'concentration problems', 'distractibility',
    'difficulty paying attention', 'lack of mental clarity', 'difficulty staying focused', 'inattention', 'short attention span', 'mind wandering',
    'difficulty concentrating on tasks', 'poor attention span', 'difficulty maintaining focus', 'lack of mental focus', 'difficulty with concentration',
    'easily distracted', 'unable to focus', 'attention issues', 'concentration challenges'
],

'lack of motivation': [
    'demotivated', 'low motivation', 'disinterest', 'lack of drive', 'lack of ambition', 'lack of initiative', 'apathy', 'unmotivated',
    'loss of drive', 'lack of enthusiasm', 'indifference', 'lack of determination', 'lack of purpose', 'loss of interest', 'lack of energy',
    'procrastination', 'lack of willpower', 'lack of focus', 'lack of passion', 'feeling uninspired', 'demotivation', 'lack of commitment', 'indifferent attitude'
],

'exhaustion': [
    'fatigue', 'tiredness', 'weariness', 'drained', 'burnout', 'physical exhaustion', 'mental exhaustion', 'extreme fatigue', 'lack of energy',
    'overwhelming tiredness', 'complete fatigue', 'depletion', 'lack of stamina', 'total exhaustion', 'exhausted feeling', 'chronic fatigue',
    'fatigued state', 'drowsiness', 'wearing out', 'energy depletion', 'fatigue syndrome', 'feeling drained', 'exhaustive tiredness', 'loss of energy',
    'profound fatigue', 'fatigue and weakness'
],

'sprain': [
    'ligament injury', 'joint sprain', 'ligament strain', 'stretched ligament', 'ligament tear',
    'sprained ligament', 'mild sprain', 'severe sprain', 'ligament damage'
],

'strain': [

    'soft tissue strain', 'overexertion', 'overworked muscle', 'acute strain', 'chronic strain', 'ligament strain'
],

'arthritis': [
    'inflammatory arthritis', 'rheumatoid arthritis', 'osteoarthritis', 'degenerative joint disease',  'rheumatism',  'pain from arthritis',
    'arthralgia', 'chronic arthritis', 'autoimmune arthritis', 'psoriatic arthritis'

],

'gout': [
    'uric acid buildup', 'acute gout', 'chronic gout', 'gout attack', 'joint pain from gout', 'gout flare-up', 'gouty inflammation', 'gouty attack',
    'painful gout episode', 'gouty swelling', 'gout in the foot', 'gout in the big toe', 'gouty condition', 'uric acid crystals', 'gouty joint disease'
],

'shoulder pain': [
    'shoulder discomfort', 'pain in the shoulder', 'shoulder ache', 'sharp shoulder pain', 'dull shoulder pain', 'shoulder stiffness', 'rotator cuff pain',
    'shoulder joint pain', 'pain in the shoulder joint', 'shoulder strain', 'shoulder injury', 'shoulder inflammation', 'pain in the upper arm',
    'muscle pain in the shoulder', 'shoulder tenderness', 'pain when moving the shoulder', 'shoulder sprain', 'pain in the deltoid', 'shoulder dislocation pain',
    'pain in the scapula', 'pain after shoulder surgery', 'shoulder impingement pain', 'frozen shoulder', 'pain from shoulder overuse', 'referred shoulder pain'
],

'bone fracture': [
    'broken bone', 'bone break', 'fractured bone', 'cracked bone', 'bone crack', 'bone injury', 'fracture', 'compound fracture', 'closed fracture',
    'stress fracture', 'hairline fracture', 'complete fracture', 'incomplete fracture', 'displaced fracture', 'non-displaced fracture', 'bone splinter',
    'fractured limb', 'fractured bone segment', 'broken limb', 'broken bone segment', 'cracked bone injury', 'bone rupture', 'bone fracture symptoms',
    'fractured bone tissue', 'fracture of the bone', 'crack in bone'
],

'back bone issue': [
    'spinal problem', 'back bone pain', 'spinal condition', 'vertebral issue', 'spinal disorder', 'back injury', 'spinal misalignment', 'back bone is paining',
    'disc herniation', 'sciatica', 'spinal injury', 'neck and back issues', 'spinal discomfort', 'lumbar pain', 'spinal cord issue', 'slipped disc', 'musculoskeletal disorder',
    'spinal health issue', 'postural problems', 'spondylosis', 'degenerative disc disease', 'spine misalignment', 'spinal deformity', 'spinal arthritis', 'spinal stenosis'
],

'female issue': [
    'women’s health', 'gynecological issue', 'female reproductive health', 'menstrual problems', 'menstrual irregularities', 'PCOS', 'endometriosis', 'fibroids', 'ovarian cysts',
    'vaginal infection', 'vaginal discharge', 'fertility issues', 'menopause', 'pre menopause', 'post menopause', 'infertility', 'vaginal dryness', 'prolapsed uterus',
    'birth control issues', 'female urinary issues', 'pregnancy complications','white discharge','female issue','female issues'
],

'thyroid': [
    'thyroid gland', 'hypothyroidism', 'hyperthyroidism', 'thyroid disorder', 'thyroid imbalance', 'underactive thyroid', 'overactive thyroid', 'goiter', 'thyroid dysfunction',
    'thyroid disease', 'thyroid cancer', 'thyroiditis', 'low thyroid function', 'high thyroid function', 'endocrine disorder', 'thyroid nodules', 'thyroid hormone imbalance',
    'TSH imbalance', 'thyroid condition', 'thyroid problems', 'autoimmune thyroid disease', 'pituitary-thyroid dysfunction', 'thyroid health', 'thyroid testing'
],

'piles': [
    'hemorrhoids', 'anal piles', 'rectal swelling', 'swollen veins', 'internal hemorrhoids', 'external hemorrhoids',
    'hemorrhoidal disease', 'rectal discomfort', 'anal itching', 'anal bleeding', 'rectal bleeding', 'chronic hemorrhoids',
    'painful hemorrhoids', 'prolapsed hemorrhoids', 'thrombosed hemorrhoids', 'anal fissures', 'blood clots in hemorrhoids',
    'swollen hemorrhoids', 'anal prolapse', 'inflamed hemorrhoids', 'rectal irritation', 'constipation-related hemorrhoids',
    'itchy anus', 'hemorrhoid treatment', 'hemorrhoid relief'
],

'vomiting': [
'food throwing up', 'puking', 'stomach upset', 'retching', 'nauseated vomiting', 'projectile vomiting', 'forceful expulsion', 'stomach evacuation',
'regurgitation', 'gag reflex', 'vomit episode', 'bilious vomiting', 'dry heaving', 'stomach upheaval', 'continuous vomiting', 'acidic vomit', 'vomiting bile',
'upset stomach leading to vomiting', 'cyclic vomiting', 'food rejection', 'nausea-induced vomiting', 'vomiting spells', 'recurrent vomiting', 'violent vomiting',
'vomiting after eating', 'motion sickness vomiting', 'morning sickness vomiting', 'dehydration from vomiting', 'vomiting blood', 'gastrointestinal vomiting',
'digestive tract expulsion', 'vomiting sensation', 'persistent nausea', 'induced vomiting', 'uncontrollable vomiting', 'abdominal vomiting', 'stomach spasms causing vomiting',
'vomiting reflex', 'vomiting from food poisoning', 'travel sickness vomiting', 'chronic vomiting episodes', 'sudden vomiting', 'intense vomiting', 'frequent retching',
'vomiting with dizziness', 'vomiting due to illness', 'nervous vomiting', 'vomiting from indigestion', 'bitter vomit taste', 'post-vomit weakness', 'vomiting accompanied by sweating'
],

'hearing loss': [
'loss of hearing', 'partial hearing loss', 'complete hearing loss', 'reduced hearing', 'impaired hearing', 'difficulty hearing', 'diminished hearing ability',
'hearing impairment', 'sensorineural hearing loss', 'conductive hearing loss', 'temporary hearing loss', 'permanent hearing loss', 'age-related hearing loss', 'noise-induced hearing loss',
'hearing deficiency', 'blocked hearing', 'muffled hearing', 'ringing in ears', 'ear damage', 'auditory dysfunction', 'ear canal blockage', 'inner ear damage',
'hearing weakness', 'fading hearing', 'loss of sound perception', 'difficulty understanding speech', 'distorted hearing', 'ear drum damage', 'hearing sensitivity reduction',
'unilateral hearing loss', 'bilateral hearing loss', 'gradual hearing loss', 'sudden hearing loss', 'ear infection-related hearing loss', 'fluid in ear causing hearing loss',
'hearing clarity reduction', 'speech comprehension difficulty', 'auditory decline', 'nerve damage causing hearing loss', 'inability to detect sound frequencies', 'ear trauma',
'hearing impairment due to illness', 'hearing degradation', 'low sound perception', 'high-frequency hearing loss', 'earwax blockage hearing loss', 'acoustic trauma',
'temporary auditory loss', 'chronic hearing damage', 'progressive hearing loss'
],

'bone pain': [
'bone tenderness', 'bone swelling', 'aching bones', 'deep bone pain', 'sharp bone pain', 'bone discomfort', 'persistent bone pain', 'localized bone pain',
'throbbing bone sensation', 'bone sensitivity', 'bone ache during movement', 'chronic bone pain', 'bone bruising', 'bone soreness', 'inflammatory bone pain',
'fracture-related bone pain', 'joint and bone pain', 'dull bone ache', 'piercing bone pain', 'bone pain during rest', 'bone pain under pressure', 'bone stiffness',
'osteopathic pain', 'bone fragility pain', 'bone strain', 'bone inflammation', 'bone pain with swelling', 'tender bone surface', 'aching joints and bones',
'deep-seated bone ache', 'bone discomfort while standing', 'bone pain due to injury', 'radiating bone pain', 'stress fracture pain', 'bone pain from infection',
'cancer-related bone pain', 'bone tenderness to touch', 'nighttime bone pain', 'sensitive bone tissue', 'bone marrow pain', 'bone pain during activity',
'osteoporosis-related bone pain', 'bone pain with movement', 'skeletal pain', 'generalized bone pain', 'acute bone discomfort', 'bone stress pain',
'pressure-induced bone pain', 'intense bone ache', 'stiff bone joints', 'localized skeletal pain'
],

'weight gain': [
'increase in weight', 'gain in body mass', 'unintended weight gain', 'gradual weight gain', 'rapid weight gain', 'excess body weight', 'body mass increase',
'weight fluctuation', 'caloric surplus', 'fat accumulation', 'body fat increase', 'muscle mass gain', 'bloating-related weight gain', 'water retention weight gain',
'unhealthy weight gain', 'sudden weight gain', 'weight gain from overeating', 'hormonal weight gain', 'stress-related weight gain', 'weight gain due to inactivity',
'metabolic weight gain', 'post-pregnancy weight gain', 'age-related weight gain', 'diet-induced weight gain', 'weight gain from medication', 'insulin-related weight gain',
'abdominal weight gain', 'upper body weight gain', 'lower body weight gain', 'excess calorie intake', 'fluid retention weight gain', 'chronic weight gain',
'weight gain around the waist', 'poor diet weight gain', 'sedentary lifestyle weight gain', 'hormone imbalance weight gain', 'slow metabolism weight gain',
'unexplained weight gain', 'overeating-induced weight gain', 'fat storage increase', 'weight gain from sugary foods', 'weight gain due to lack of exercise',
'weight gain with bloating', 'hormone-related fat storage', 'weight gain caused by stress eating', 'body composition change', 'progressive weight gain',
'weight gain due to emotional eating', 'weight gain from poor sleep', 'unbalanced diet weight gain','gained weight', 'weight going up'
],

'skin burning': [
'burning feeling', 'skin irritation', 'skin stinging', 'skin redness', 'skin inflammation', 'burning sensation', 'skin discomfort', 'tingling burn',
'localized skin burn', 'skin heat sensation', 'raw skin feeling', 'skin hypersensitivity', 'sunburn', 'chemical burn', 'skin scorching', 'skin sensitivity to touch',
'prickling skin sensation', 'hot skin feeling', 'burning skin pain', 'skin abrasion burn', 'nerve-related burning', 'itchy burning skin', 'skin damage from burn',
'skin burning after contact', 'intense burning sensation', 'surface skin burn', 'skin blistering', 'persistent skin burn', 'burned skin surface',
'red inflamed skin', 'skin discomfort from heat', 'skin burning from friction', 'skin chafing burn', 'thermal skin burn', 'abrasive skin burn', 'sensitive skin after burn',
'stinging skin pain', 'skin burn from chemicals', 'skin damage sensation', 'skin peeling from burn', 'acute burning feeling', 'skin burn with swelling',
'lingering skin burn', 'burnt skin tenderness', 'skin hot spot', 'irritated skin burn', 'sharp skin burn sensation', 'skin burning rash', 'skin burning itch'
],

'itching': [
'skin itching', 'pruritus', 'itchy sensation', 'persistent itching', 'intense itching', 'localized itching', 'generalized itching', 'skin irritation',
'itchy rash', 'dry skin itching', 'allergic itching', 'itching from insect bites', 'itchy skin patches', 'scalp itching', 'itching sensation under the skin',
'chronic itching', 'temporary itching', 'burning itch', 'itching with redness', 'itching from dryness', 'irritated skin itch', 'tickling skin sensation',
'itchy skin bumps', 'itchy welts', 'itchy hives', 'skin crawling sensation', 'itching from heat rash', 'itchy blisters', 'itching from eczema', 'itching from psoriasis',
'itching with flaking skin', 'itching from fungal infection', 'itching from dermatitis', 'nighttime itching', 'itching due to allergies', 'itching from contact dermatitis',
'itching after sunburn', 'itching from insect stings', 'itching with swelling', 'prickly itching sensation', 'itching from poison ivy', 'itching with dryness',
'itching from skin irritation', 'itching from chemicals', 'itchy mosquito bites', 'itching with inflammation', 'nerve-related itching', 'itching from medication side effects',
'itching due to sweat', 'itching from poor hygiene', 'itchy skin lesions','itching'
],

'injury': [
'injured', 'wound', 'physical injury', 'bodily harm', 'tissue damage', 'acute injury', 'chronic injury', 'sports injury', 'accidental injury',
'soft tissue injury', 'muscle injury', 'joint injury', 'bone injury', 'ligament injury', 'nerve injury', 'head injury', 'spinal injury', 'bruise',
'cut', 'abrasion', 'laceration', 'contusion', 'strain injury', 'sprain injury', 'impact injury', 'blunt force trauma', 'penetrating injury', 'superficial injury',
'deep tissue injury', 'skin injury', 'crush injury', 'internal injury', 'traumatic wound', 'workplace injury', 'repetitive strain injury', 'overuse injury',
'thermal injury', 'chemical injury', 'burn injury', 'frostbite', 'puncture wound', 'tendon injury', 'cartilage injury', 'open wound', 'closed injury',
'localized injury', 'multiple injuries', 'injury with swelling', 'painful injury', 'infected injury'
],

'jaundice': [
'icterus', 'jaundiced appearance',
'hepatic jaundice', 'neonatal jaundice', 'obstructive jaundice', 'hemolytic jaundice', 'liver-related jaundice', 'gallbladder-related jaundice',
'chronic jaundice', 'acute jaundice', 'jaundice-induced fatigue', 'itching with jaundice',
'jaundice rash', 'jaundice-related weakness', 'jaundice-related nausea', 'jaundice-related abdominal pain', 'hepatitis-related jaundice',
'gallstone-related jaundice', 'pre-hepatic jaundice', 'post-hepatic jaundice','biliary jaundice', 'jaundice-related weight loss',
 'jaundice-associated itching', 'systemic jaundice','jaundice in newborns', 'jaundice symptoms'
],

'sleepy': [
'sleeping', 'sleepiness', 'drowsy', 'asleep', 'lethargic', 'groggy', 'sluggish', 'heavy-eyed', 'nodding off', 'fatigued', 'dozing',
'half asleep', 'sleep-deprived', 'exhausted', 'yawning', 'slow-moving', 'low energy', 'ready for bed', 'snoozy', 'sleep-prone', 'droopy eyed', 'barely awake',
'mentally tired', 'physically tired', 'overly relaxed', 'hard to stay awake', 'sleep craving', 'languid', 'wearied', 'brain fog',
'bed ready', 'sleep drawn', 'lazy eyed', 'unfocused from tiredness', 'nodding head', 'drifting off', 'sleepy sensation', 'slumberous', 'soporific', 'somnolent',
'half-awake', 'daytime sleepiness', 'overwhelming fatigue', 'rest-seeking', 'near dozing', 'eyes struggling to stay open', 'unable to concentrate', 'dull from tiredness'
],

'eye weakness': [
'weakness in eyes', 'weak eyes', 'eyes are weak', 'eyes are becoming weak', 'eye is weak', 'tired eyes', 'eye strain', 'blurred vision',
'fatigued eyes', 'heavy eyes', 'difficulty focusing', 'eye muscle weakness', 'strained vision', 'eye discomfort', 'droopy eyelids', 'lack of eye strength',
'vision fatigue', 'eye exhaustion', 'eye tiredness', 'reduced eye stamina', 'difficulty keeping eyes open', 'eye sensitivity', 'failing eye strength',
'eye fatigue after reading', 'poor eye endurance', 'eye weakness from screen use', 'eye weariness', 'visual tiredness', 'eye fragility', 'weak eye muscles',
'prolonged eye strain', 'focus difficulty', 'unstable eye movement', 'eye soreness', 'eye heaviness', 'visual exhaustion', 'difficulty maintaining focus',
'eyes feeling overworked', 'weak visual acuity', 'eye tiredness at night', 'eye discomfort after long tasks', 'loss of eye strength', 'drooping eyes',
'strained eye muscles', 'eye fatigue with headaches', 'difficulty keeping eyes focused', 'eye tension', 'sensitivity to light', 'eye weakness from fatigue'
],


'leg weakness': [
'legs are becoming weak', 'weakness in legs', 'leg is weak', 'legs are weak', 'tired legs', 'wobbly legs', 'unsteady legs', 'shaky legs',
'fatigued legs', 'heavy legs', 'lack of leg strength', 'unstable legs', 'leg muscle weakness', 'difficulty standing', 'difficulty walking', 'leg fatigue',
'legs giving out', 'trembling legs', 'poor leg endurance', 'reduced leg strength', 'weak leg muscles', 'unstable lower limbs', 'leg instability',
'feeling of leg collapse', 'limb weakness', 'leg exhaustion', 'legs feel drained', 'weakness in thigh muscles', 'weakness in calf muscles',
'legs feel powerless', 'numb legs', 'tingling in legs', 'cramping legs', 'difficulty supporting weight', 'legs feel rubbery', 'shaking lower limbs',
'legs feel unstable after exertion', 'difficulty lifting legs', 'leg weakness while climbing stairs', 'leg weakness after standing long',
'legs feel like jelly', 'legs feel heavy and weak', 'poor leg control', 'unstable footing', 'weakness after prolonged standing', 'leg stiffness',
'inability to bear weight on legs', 'sensation of leg failure', 'unresponsive legs'
],

'asthma': ['wheezing', 'reactive airway disease', 'hyperresponsive airway disease', 'asthmatic condition', 'asthmas', 'asthama','whistling sound while breathing'],

'pneumonia': ['lung infection','alveolar infection'],

'sugar': ['sugars', 'glucose', 'blood sugar', 'hyperglycemia', 'hypoglycemia'],
   }

# ------------------------------------------------------------------ #
# ----------------------- Followup Question ------------------------ #
# ------------------------------------------------------------------ #
symptom_followup_questions = {
  "stomach pain": [
    {
      "hi": "पेट दर्द वास्तव में कहाँ स्थित है?",
      "en": "Where exactly is the stomach pain located?",
      "category": "stomach ache",
      "symptom": "stomach ache",
      "risk_factor": False,    },
    {
      "hi": "क्या आप पेट दर्द का वर्णन कर सकते हैं? (तीव्र, सुस्त, ऐंठन, जलन, आदि)",
      "en": "Can you describe the stomach pain? (Sharp, dull, cramping, burning, etc.)",
      "category": "stomach ache",
      "symptom": "stomach ache",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको अन्य कोई लक्षण जैसे कि उल्टी, दस्त, बुखार आदि महसूस हो रहे हैं?",
      "en": "Do you have any other symptoms, such as nausea, vomiting, diarrhea, or fever?",
      "category": "digestive symptoms",
      "symptom": "nausea, vomiting, diarrhea, fever",
      "risk_factor": False,    },
    {
      "hi": "क्या आपने हाल ही में कोई असामान्य भोजन खाया है या आपके आहार में कोई बदलाव हुआ है?",
      "en": "Have you eaten anything unusual or had any changes in your diet recently?",
      "category": "dietary changes",
      "symptom": "dietary changes",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको पाचन समस्याओं का इतिहास है (जैसे कि अम्लता, IBS, अल्सर आदि)?",
      "en": "Do you have a history of digestive problems (e.g., acid reflux, IBS, ulcers)?",
      "category": "digestive history",
      "symptom": "digestive problems",
      "risk_factor": True,    },
  ],
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
      "hi": "लक्षणों को क्या ट्रिगर करता है या बिगाड़ता है (जैसे कि कुछ खाद्य पदार्थ, लेट जाना, तनाव)?",
      "en": "What triggers or worsens the symptoms (e.g., certain foods, lying down, stress)?",
      "category": "heartburn",
      "symptom": "acidity",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको अन्य कोई लक्षण जैसे कि उल्टी, पाचन में असुविधा या निगलने में कठिनाई महसूस हो रही है?",
      "en": "Do you experience any other symptoms, such as nausea, regurgitation, or difficulty swallowing?",
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
      "hi": "क्या आपको नींद की कमी का सामना करना पड़ता है?",
      "en": "Do you face lack of sleep?",
      "category": "lack of sleep",
      "symptom": "sleep deprivation",
      "risk_factor": False,    },
    {
      "hi": "क्या आप खुद को हाइड्रेटेड रखते हैं?",
      "en": "Do you keep yourself hydrated??",
      "category": "dehydration",
      "symptom": "dehydration",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको मांसपेशियों में कमजोरी है?",
      "en": "Do you have muscle weakness?",
      "category": "weakness",
      "symptom": "Weakness",
      "risk_factor": False,    },
    {
      "hi": "क्या आप पौष्टिक भोजन खाते हैं?",
      "en": "Do you eat nutritious food?",
      "category": "weakness",
      "symptom": "Weakness",
      "risk_factor": False,    },
    {
      "hi": "क्या आप प्रतिदिन व्यायाम करते हैं?",
      "en": "Do you exercise daily?",
      "category": "weakness",
      "symptom": "Weakness",
      "risk_factor": False,    },
    {
      "hi": "क्या आप शारीरिक रूप से विकलांग व्यक्ति हैं?",
      "en": "Are you physically challenged person?",
      "category": "weakness",
      "symptom": "Weakness",
      "risk_factor": False,    },
  ],

  "headache": [
    {
      "hi": "क्या आपका सिरदर्द लगातार है या बीच-बीच में आता है?",
      "en": "Is your headache constant or intermittent?",
      "category": "headache_type",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या सिरदर्द की तीव्रता बढ़ रही है?",
      "en": "Is the intensity of your headache increasing?",
      "category": "intensity_increase",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या सिरदर्द के साथ दृष्टि में परिवर्तन है?",
      "en": "Are you experiencing any changes in vision along with headache?",
      "category": "vision_changes",
      "symptom": "Vision changes",
      "risk_factor": False,    },
    {
      "hi": "क्या सिरदर्द की शुरुआत अचानक हुई थी या धीरे-धीरे?",
      "en": "Did the headache start suddenly or gradually?",
      "category": "onset",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या सिरदर्द का कोई विशिष्ट स्थान है?",
      "en": "Is there a specific location where you feel the headache?",
      "category": "location_specific",
      "symptom": "Location-specific headache",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको मिचली हो रही है साथ ही सिरदर्द?",
      "en": "Are you feeling nauseous along with headache?",
      "category": "nausea_headache",
      "symptom": "Nausea",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको ध्वनि या रोशनी से संवेदनशीलता है साथ ही सिरदर्द?",
      "en": "Do you have sensitivity to sound or light along with headache?",
      "category": "sensory_sensitivity",
      "symptom": "Sensitivity to sound or light",
      "risk_factor": False,    },
    {
      "hi": "क्या आपने कोई नया स्टाइलिश हैडबैग या चश्मा पहनना शुरू किया है?",
      "en": "Have you started wearing a new stylish hat or glasses?",
      "category": "external_factors",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या आपको तनाव है साथ ही सिरदर्द?",
      "en": "Are you under stress along with headache?",
      "category": "stress_headache",
      "symptom": "Stress-related headache",
      "risk_factor": False,    },
    {
      "hi": "क्या आपकी नींद में कोई कमी है साथ ही सिरदर्द?",
      "en": "Are you lacking sleep along with headache?",
      "category": "sleep_deprivation",
      "symptom": "Sleep deprivation",
      "risk_factor": False,    },
  ],
  "nausea": [
    {
      "hi": "क्या आपको उल्टी हो रही है?",
      "en": "Are you vomiting?",
      "category": "vomiting",
      "symptom": "Vomiting",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको लगातार मतली महसूस हो रही है?",
      "en": "Are you experiencing constant nausea?",
      "category": "constant_nausea",
      "symptom": "Constant nausea",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको खाने के बाद मतली होती है?",
      "en": "Do you feel nauseous after eating?",
      "category": "postprandial_nausea",
      "symptom": "Postprandial nausea",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको पेट में दर्द हो रहा है साथ ही मतली?",
      "en": "Are you experiencing abdominal pain along with nausea?",
      "category": "abdominal_pain_nausea",
      "symptom": "abdominal_pain_nausea",
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
  "dizziness": [

    {
      "hi": "क्या चक्कर आना अचानक शुरू हुआ था या धीरे-धीरे?",
      "en": "Did the dizziness start suddenly or gradually?",
      "category": "dizziness_onset",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या चक्कर आने के साथ मतली या उल्टी हो रही है?",
      "en": "Are you experiencing nausea or vomiting along with dizziness?",
      "category": "dizziness_nausea_vomiting",
      "symptom": "Nausea or vomiting",
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
      "symptom": "Headache",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको संतुलन बिगड़ रहा है?",
      "en": "Are you losing your balance?",
      "category": "balance_issues",
      "symptom": "Balance issues",
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
      "hi": "क्या आपको थकान महसूस हो रही है साथ में पीली आँखें?",
      "en": "Are you feeling fatigued along with yellow eyes?",
      "category": "fatigue_jaundice",
      "symptom": "Fatigue with jaundice",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके मूत्र का रंग गहरा हो गया है?",
      "en": "Has the color of your urine become darker?",
      "category": "dark_urine",
      "symptom": "Dark urine",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके बवासीर या पेट में दर्द है साथ में पीली आँखें?",
      "en": "Do you have hemorrhoids or abdominal pain along with yellow eyes?",
      "category": "hemorrhoids_abdominal_pain",
      "symptom": "Hemorrhoids or abdominal pain",
      "risk_factor": False,    },
    {
      "hi": "क्या आपकी आँखों में जलन हो रही है?",
      "en": "Are your eyes feeling itchy along with yellowing?",
      "category": "itchy_eyes",
      "symptom": "Itchy eyes",
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
      "symptom": "Chills",
      "risk_factor": False,    },
    {
      "hi": "क्या आपने कोई दवा ली है?",
      "en": "Have you taken any medication?",
      "category": "medications",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या आपको सिरदर्द है?",
      "en": "Are you experiencing headaches?",
      "category": "headache",
      "symptom": "Headache",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको उल्टी जैसा महसूस हो रहा है?",
      "en": "Are you feeling nauseous?",
      "category": "nausea",
      "symptom": "Nausea",
      "risk_factor": False,    },
    {
      "hi": "क्या आपका तापमान सामान्य से अधिक है?",
      "en": "Is your temperature higher than normal?",
      "category": "high_temperature",
      "symptom": "High temperature",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको रात में पसीना आता है?",
      "en": "Do you experience night sweats?",
      "category": "night_sweats",
      "symptom": "Night sweats",
      "risk_factor": False,    },

     
        {
            "hi": "क्या आप बेहोश, चक्कर, या भ्रम में हैं?",
            "en": "Are you feeling faint, dizzy, or confused?",
            "category": "neurological",
            "symptom": "fever",
            "risk_factor": False,
        },
    {
      "hi": "क्या आपको भूख कम लग रही है?",
      "en": "Are you experiencing loss of appetite?",
      "category": "loss_of_appetite",
      "symptom": "Loss of appetite",
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
      "symptom": "Fever",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको सांस लेने में कठिनाई हो रही है?",
      "en": "Are you experiencing difficulty breathing?",
      "category": "breathing",
      "symptom": "Shortness of breath",
      "risk_factor": False,    },
    {
      "hi": "क्या आपकी खांसी रात में बढ़ जाती है?",
      "en": "Does your cough worsen at night?",
      "category": "time",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या आपको सीने में दर्द है?",
      "en": "Are you experiencing chest pain?",
      "category": "chest_pain",
      "symptom": "Chest pain",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको गले में खराश है?",
      "en": "Do you have a sore throat?",
      "category": "sore_throat",
      "symptom": "Sore throat",
      "risk_factor": False,    },
    {
      "hi": "क्या आपकी आवाज़ बदल गई है?",
      "en": "Has your voice changed?",
      "category": "voice_change",
      "symptom": "Hoarseness",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको सांस लेने में सीटी जैसी आवाज़ आती है?",
      "en": "Do you experience wheezing?",
      "category": "wheezing",
      "symptom": "Wheezing",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके खांसी के साथ बलगम में खून है?",
      "en": "Is there blood in your phlegm with your cough?",
      "category": "hemoptysis",
      "symptom": "Hemoptysis",
      "risk_factor": False,    },
    {
      "hi": "क्या आपकी खांसी के साथ तेज सांस लेना शामिल है?",
      "en": "Does your cough include rapid breathing?",
      "category": "rapid_breathing",
      "symptom": "Rapid breathing",
      "risk_factor": False,    },
  ],

  "muscle pain": [
    {
      "hi": "क्या आपके मांसपेशियों में दर्द लगातार है या आता-जाता है?",
      "en": "Is your muscle pain constant or does it come and go?",
      "category": "intermittent_pain",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या मांसपेशियों में दर्द किसी विशेष गतिविधि के दौरान बढ़ता है?",
      "en": "Does your muscle pain increase during any specific activity?",
      "category": "activity_related_pain",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या आपके मांसपेशियों में दर्द के साथ सूजन भी है?",
      "en": "Is there any swelling along with your muscle pain?",
      "category": "swelling",
      "symptom": "swelling",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको मांसपेशियों में खिंचाव महसूस हो रहा है?",
      "en": "Are you feeling any muscle cramps?",
      "category": "cramps",
      "symptom": "cramps",
      "risk_factor": False,    },
    {
      "hi": "क्या मांसपेशियों में दर्द के साथ कमजोरी भी महसूस हो रही है?",
      "en": "Are you experiencing any weakness along with muscle pain?",
      "category": "weakness",
      "symptom": "weakness",
      "risk_factor": False,    },
  ],

  "joint pain": [
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
    {
      "hi": "क्या आपके जोड़ों में सूजन भी है?",
      "en": "Is there any swelling in your joints?",
      "category": "swelling",
      "symptom": "swelling",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको जोड़ों में कठोरता महसूस हो रही है?",
      "en": "Are you experiencing stiffness in your joints?",
      "category": "stiffness",
      "symptom": "stiffness",
      "risk_factor": False,    },
    {
      "hi": "क्या जोड़ों में दर्द के साथ कोई आवाज़ भी सुनाई देती है?",
      "en": "Do you hear any clicking or popping sounds in your joints along with pain?",
      "category": "sounds_with_pain",
      "symptom": None,
      "risk_factor": False,    },
  ],
  "knee pain": [
    {
      "hi": "क्या कोई विशेष चोट या घटना थी जिसके कारण घुटने में दर्द हुआ?",
      "en": "Was there any specific injury or event that triggered the knee pain?",
      "category": "knee pain",
      "symptom": "knee pain",
      "risk_factor": False,    },
    {
      "hi": "क्या आप घुटने के दर्द का वर्णन कर सकते हैं? (तीव्र, सुस्त, दर्द, आदि)",
      "en": "Can you describe the knee pain? (Sharp, dull, aching, etc.)",
      "category": "knee pain",
      "symptom": "knee pain",
      "risk_factor": False,    },
    {
      "hi": "क्या घुटनों में दर्द लगातार होता रहता है, या आता-जाता रहता है?",
      "en": "Does the knee pain occur constantly, or does it come and go?",
      "category": "knee pain",
      "symptom": "knee pain",
      "risk_factor": False,    },
    {
      "hi": "दर्द आपके घुटने के किस हिस्से में महसूस हो रहा है? (सामने, पीछे, किनारे)",
      "en": "Where exactly in the knee do you feel the pain (front, back, sides)?",
      "category": "knee pain",
      "symptom": "knee pain",
      "risk_factor": False,    },
    {
      "hi": "क्या चलने या सीढ़ियाँ चढ़ने जैसी कुछ गतिविधियों से घुटने का दर्द बढ़ जाता है?",
      "en": "Does the knee pain get worse with certain activities, like walking or climbing stairs?",
      "category": "knee pain",
      "symptom": "knee pain",
      "risk_factor": False,    },
    {
      "hi": "क्या घुटने के आसपास सूजन, लाली या गर्मी महसूस हो रही है?",
      "en": "Have you noticed any swelling, redness, or warmth around the knee?",
      "category": "knee pain",
      "symptom": "knee pain",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको घुटने को मोड़ने या सीधा करने में कोई समस्या हो रही है?",
      "en": "Are you having trouble bending or straightening your knee?",
      "category": "knee pain",
      "symptom": "knee pain",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको घुटने में अस्थिरता या ऐसा लगता है जैसे घुटना 'गिर' रहा हो?",
      "en": "Do you feel any instability or like your knee is 'giving way'?",
      "category": "knee pain",
      "symptom": "knee pain",
      "risk_factor": False,    },
  ],
  "wrist pain": [

    {
      "hi": "क्या आप कलाई के दर्द का वर्णन कर सकते हैं? (तीव्र, सुस्त, दर्द, आदि)",
      "en": "Can you describe the wrist pain? (Sharp, dull, aching, etc.)",
      "category": "wrist pain",
      "symptom": "wrist pain",
      "risk_factor": False,    },
    {
      "hi": "कौन सी गतिविधियाँ कलाई के दर्द को बदतर बना देती हैं?",
      "en": "What activities make the wrist pain worse?",
      "category": "wrist pain",
      "symptom": "wrist pain",
      "risk_factor": False,    },
    {
      "hi": "क्या आपकी कलाई के आसपास सूजन या चोट है?",
      "en": "Is there swelling or bruising around the wrist?",
      "category": "wrist pain",
      "symptom": "wrist pain",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके हाथ या अंगुलियों में सुन्नता या झनझनाहट महसूस हो रही है?",
      "en": "Do you have numbness or tingling in your hand or fingers?",
      "category": "wrist pain",
      "symptom": "wrist pain",
      "risk_factor": False,    },
    {
      "hi": "क्या आपने हाल ही में कलाई को चोट पहुँचाई है? (गिरना, मुड़ना, सीधा असर)",
      "en": "Have you injured the wrist recently? (e.g., fall, twist, direct blow)",
      "category": "wrist pain",
      "symptom": "wrist pain",
      "risk_factor": False,    },
    {
      "hi": "क्या आपने हाल ही में कोई पुनरावृत्त गतिविधियाँ या अधिक उपयोग किया है?",
      "en": "Have you had any recent repetitive activities or overuse?",
      "category": "wrist pain",
      "symptom": "wrist pain",
      "risk_factor": False,    },
    {
      "hi": "क्या कलाई में दर्द लगातार या रुक-रुक कर होता है?",
      "en": "Is the wrist pain constant or intermittent?",
      "category": "wrist pain",
      "symptom": "wrist pain",
      "risk_factor": False,    },
    {
      "hi": "क्या आराम करने से कलाई का दर्द ठीक हो जाता है या बिगड़ जाता है?",
      "en": "Does the wrist pain improve or worsen with rest?",
      "category": "wrist pain",
      "symptom": "wrist pain",
      "risk_factor": False,    },
  ],

  "leg pain": [
    {
      "hi": "क्या कोई विशेष चोट या घटना थी जिसके कारण पैर में दर्द हुआ?",
      "en": "Was there any specific injury or event that triggered the leg pain?",
      "category": "leg pain",
      "symptom": "leg pain",
      "risk_factor": False,    },
    {
      "hi": "क्या आप पैर के दर्द का वर्णन कर सकते हैं? (तीव्र, सुस्त, ऐंठन, जलन, आदि)",
      "en": "Can you describe the leg pain? (Sharp, dull, cramping, burning, etc.)",
      "category": "leg pain",
      "symptom": "leg pain",
      "risk_factor": False,    },
    {
      "hi": "क्या पैर में दर्द लगातार होता रहता है, या आता-जाता रहता है?",
      "en": "Does the leg pain occur constantly, or does it come and go?",
      "category": "leg pain",
      "symptom": "leg pain",
      "risk_factor": False,    },
    {
      "hi": "दर्द आपके पैर के किस हिस्से में महसूस हो रहा है? (जांघ, घुटना, बछड़ा, पंजा)",
      "en": "Where exactly in the leg do you feel the pain (thigh, knee, calf, foot)?",
      "category": "leg pain",
      "symptom": "leg pain",
      "risk_factor": False,    },
    {
      "hi": "क्या चलने, दौड़ने या खड़े होने से पैर का दर्द बढ़ जाता है?",
      "en": "Does the leg pain get worse with walking, running, or standing?",
      "category": "leg pain",
      "symptom": "leg pain",
      "risk_factor": False,    },
    {
      "hi": "क्या आपने पैरों में सूजन, लालिमा या गर्मी महसूस की है?",
      "en": "Have you noticed any swelling, redness, or warmth in the leg?",
      "category": "leg pain",
      "symptom": "leg pain",
      "risk_factor": False,    },
    {
      "hi": "क्या दर्द पैर के अन्य हिस्सों तक फैलता है (जैसे कि जांघ से पंजे तक)?",
      "en": "Does the pain radiate to other parts of the leg (e.g., from the thigh to the foot)?",
      "category": "leg pain",
      "symptom": "leg pain",
      "risk_factor": False,    },
    {
      "hi": "क्या आपने पहले अपने पैरों में किसी चोट या समस्या का अनुभव किया है?",
      "en": "Have you had any previous injuries or problems with your legs?",
      "category": "leg pain",
      "symptom": "leg pain",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको पैरों में कमजोरी, सुन्नता या झुनझुनी महसूस होती है?",
      "en": "Do you feel weakness, numbness, or tingling in the leg?",
      "category": "leg pain",
      "symptom": "leg pain",
      "risk_factor": False,    },
  ],

  "chest pain": [
    {
      "hi": "क्या आपका छाती में दर्द तेज है या स्थिर है?",
      "en": "Is your chest pain sharp or dull?",
      "category": "pain_intensity",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या छाती का दर्द अचानक शुरू हुआ था या धीरे-धीरे?",
      "en": "Did the chest pain start suddenly or gradually?",
      "category": "onset",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या छाती में दर्द के साथ सांस लेने में कठिनाई हो रही है?",
      "en": "Are you experiencing difficulty breathing along with chest pain?",
      "category": "breathing_difficulty",
      "symptom": "shortness of breath",
      "risk_factor": False,    },
    {
      "hi": "क्या छाती का दर्द किसी विशेष गतिविधि के दौरान बढ़ता है?",
      "en": "Does your chest pain increase during any specific activity?",
      "category": "activity_related_pain",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या छाती का दर्द आपके हाथ, गर्दन या कमर में फैल रहा है?",
      "en": "Is your chest pain radiating to your arms, neck, or back?",
      "category": "radiating_pain",
      "symptom": None,
      "risk_factor": False,    },
  ],

  "back pain": [
        {
            "hi": "क्या आपका पीठ दर्द निचले हिस्से में है या ऊपर?",
            "en": "Is your back pain in the lower or upper back?",
            "category": "pain_location",
            "symptom": None,
            "risk_factor": False,
        },
        {
            "hi": "क्या पीठ दर्द लगातार है या आता-जाता है?",
            "en": "Is your back pain constant or does it come and go?",
            "category": "intermittent_pain",
            "symptom": None,
            "risk_factor": False,
        },
        {
            "hi": "क्या किसी विशेष गतिविधि के दौरान पीठ दर्द बढ़ता है?",
            "en": "Does your back pain increase during any specific activity?",
            "category": "activity_related_pain",
            "symptom": None,
            "risk_factor": False,
        },
        {
            "hi": "क्या पीठ दर्द के साथ सूजन है?",
            "en": "Is there any swelling along with your back pain?",
            "category": "swelling",
            "symptom": "swelling",
            "risk_factor": False,
        },
        {
            "hi": "क्या पीठ दर्द के साथ कमजोरी महसूस हो रही है?",
            "en": "Are you experiencing any weakness along with back pain?",
            "category": "weakness",
            "symptom": "weakness",
            "risk_factor": False,
        },
      
        {
            "hi": "क्या दर्द तेज/चुभन वाला, मट्टा, या जलन जैसा है?",
            "en": "Is the pain sharp/stabbing, dull, or burning?",
            "category": "pain_quality",
            "symptom": "back pain",
            "risk_factor": False,
        },
        
        {
            "hi": "क्या आपको लंबे समय तक चलने, खड़े रहने, या बैठने में परेशानी हो रही है?",
            "en": "Are you having difficulty walking, standing, or sitting for long periods?",
            "category": "mobility_impairment",
            "symptom": "back pain",
            "risk_factor": False,
        },
        
        {
            "hi": "क्या आपके पिछवाड़े या रीढ़ में पहले कोई चोट, गिरना, या दुर्घटना हुई है?",
            "en": "Have you had previous injuries, falls, or accidents involving your back or spine?",
            "category": "history_of_injury",
            "symptom": "back pain",
            "risk_factor": False,
        },
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
      "hi": "क्या आपकी डाइट में पर्याप्त फाइबर है?",
      "en": "Does your diet include sufficient fiber?",
      "category": "diet_fiber",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या कब्ज की समस्या के साथ कोई अन्य लक्षण हैं?",
      "en": "Are there any other symptoms associated with your constipation?",
      "category": "other_symptoms",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या आप नियमित रूप से व्यायाम करते हैं?",
      "en": "Do you exercise regularly?",
      "category": "exercise",
      "symptom": None,
      "risk_factor": False,    },
  ],

  "sore throat": [
    {
      "hi": "क्या आपकी गले में दर्द लगातार है या आता-जाता है?",
      "en": "Is your sore throat constant or does it come and go?",
      "category": "intermittent_pain",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या आपको निगलने में कठिनाई हो रही है?",
      "en": "Are you having difficulty swallowing?",
      "category": "difficulty_swallowing",
      "symptom": "difficulty swallowing",
      "risk_factor": False,    },
    {
      "hi": "क्या गले में दर्द के साथ सूजन भी है?",
      "en": "Is there any swelling along with your sore throat?",
      "category": "swelling",
      "symptom": "swelling",
      "risk_factor": False,    },
    {
      "hi": "क्या आपकी आवाज़ में परिवर्तन आया है?",
      "en": "Has there been any change in your voice?",
      "category": "voice_changes",
      "symptom": "voice changes",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको गले में जलन महसूस हो रही है?",
      "en": "Are you experiencing any burning sensation in your throat?",
      "category": "burning_sensation",
      "symptom": "burning",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके गले में कोई गड़गड़ाहट है?",
      "en": "Do you have any tickling sensation in your throat?",
      "category": "tickling_sensation",
      "symptom": None,
      "risk_factor": False,    },
  ],

  "diarrhea": [
    {
      "hi": "क्या आपको दस्त लगातार हो रहे हैं या कभी-कभी?",
      "en": "Are you experiencing diarrhea continuously or intermittently?",
      "category": "intermittent_diarrea",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या दस्त के साथ पेट में दर्द है?",
      "en": "Do you have abdominal pain along with diarrhea?",
      "category": "abdominal_pain",
      "symptom": "abdominal pain",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको दस्त के साथ उल्टी भी हो रही है?",
      "en": "Are you also experiencing vomiting along with diarrhea?",
      "category": "vomiting",
      "symptom": "vomiting",
      "risk_factor": False,    },
    {
      "hi": "क्या आप अपने शरीर से अधिक पानी खो रहे हैं?",
      "en": "Are you losing more water from your body?",
      "category": "dehydration",
      "symptom": "dehydration",
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
  ],

  "vomiting": [
    {
      "hi": "क्या उल्टी लगातार हो रही है या कभी-कभी?",
      "en": "Are you vomiting continuously or intermittently?",
      "category": "intermittent_vomiting",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या उल्टी के साथ पेट में दर्द है?",
      "en": "Do you have abdominal pain along with vomiting?",
      "category": "abdominal_pain",
      "symptom": "abdominal pain",
      "risk_factor": False,    },
    {
      "hi": "क्या उल्टी के कारण आपको शरीर से पानी की कमी हो रही है?",
      "en": "Are you losing water from your body due to vomiting?",
      "category": "dehydration",
      "symptom": "dehydration",
      "risk_factor": False,    },
    {
      "hi": "क्या उल्टी के साथ बुखार भी है?",
      "en": "Is there a fever along with vomiting?",
      "category": "fever",
      "symptom": "fever",
      "risk_factor": False,    },
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
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या ठंडक के साथ पसीना आना भी शुरू हो गया है?",
      "en": "Have you started sweating along with chills?",
      "category": "sweating_with_chills",
      "symptom": "sweating",
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
      "hi": "क्या सूजन किसी विशेष हिस्से में है?",
      "en": "Is the swelling in any specific area?",
      "category": "swelling_location",
      "symptom": None,
      "risk_factor": False,    },
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
    {
      "hi": "क्या सूजन के कारण आपको बेचैनी हो रही है?",
      "en": "Are you feeling restless due to swelling?",
      "category": "restlessness_with_swelling",
      "symptom": None,
      "risk_factor": False,    },
  ],

  "infection": [
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
    {
      "hi": "क्या संक्रमण के साथ कोई अन्य लक्षण भी हैं?",
      "en": "Are there any other symptoms along with the infection?",
      "category": "other_symptoms",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या संक्रमण के कारण आपको त्वचा में लालिमा आ रही है?",
      "en": "Is there any redness in your skin due to the infection?",
      "category": "skin_redness",
      "symptom": "redness",
      "risk_factor": False,    },
  ],

  "depression": [
    {
      "hi": "क्या आपको उदासी या निराशा महसूस हो रही है?",
      "en": "Are you feeling sad or hopeless?",
      "category": "sadness",
      "symptom": None,
      "risk_factor": False,    },
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
      "hi": "क्या आपको निर्णय लेने में कठिनाई हो रही है?",
      "en": "Are you having difficulty making decisions?",
      "category": "decision_difficulty",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या आपकी नींद में कोई समस्या है?",
      "en": "Are you having any problems with your sleep?",
      "category": "sleep_problems",
      "symptom": "insomnia",
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
      "hi": "क्या आपको अत्यधिक प्यास लग रही है?",
      "en": "Are you feeling excessively thirsty?",
      "category": "excessive_thirst",
      "symptom": "excessive thirst",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको बहुत भूख लग रही है?",
      "en": "Are you feeling very hungry?",
      "category": "increased_appetite",
      "symptom": "increased appetite",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके वजन में अचानक कमी आई है?",
      "en": "Have you experienced sudden weight loss?",
      "category": "sudden_weight_loss",
      "symptom": "weight loss",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको धुंधली दृष्टि हो रही है?",
      "en": "Are you experiencing blurred vision?",
      "category": "blurred_vision",
      "symptom": "blurred vision",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको ऊँची या नीची रक्तचाप की समस्या है?",
      "en": "Do you have high or low blood pressure?",
      "category": "blood_pressure",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या आपके घुटनों या पैरों में सुन्नता है?",
      "en": "Are you experiencing numbness in your knees or feet?",
      "category": "numbness",
      "symptom": "numbness",
      "risk_factor": False,    },
  ],

  "allergy": [
    {
      "hi": "क्या आपको किसी विशेष चीज़ से एलर्जी है?",
      "en": "Do you have allergies to any specific substance?",
      "category": "specific_allergy",
      "symptom": None,
      "risk_factor": False,    },
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
      "hi": "क्या आपको गले में खुजली या सूजन महसूस हो रही है?",
      "en": "Are you feeling itchiness or swelling in your throat?",
      "category": "throat_allergy_symptoms",
      "symptom": "swelling",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके लक्षण किसी खास मौसम या वातावरण में अधिक होते हैं?",
      "en": "Do your symptoms worsen in certain seasons or environments?",
      "category": "environmental_allergy_triggers",
      "symptom": None,
      "risk_factor": False,    },
  ],

 "high blood pressure": [
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
    "symptom": "high blood pressure",
    "risk_factor": False,
  },
  {
    "hi": "क्या आप सिरदर्द, चक्कर, छाती में दर्द, या सांस की तकलीफ जैसे लक्षण महसूस कर रहे हैं?",
    "en": "Are you experiencing any symptoms like headaches, dizziness, chest pain, or shortness of breath?",
    "category": "high blood pressure",
    "symptom": "high blood pressure",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपने अपनी जीवनशैली में कोई बदलाव महसूस किया है, जैसे तनाव में वृद्धि, खराब आहार, या व्यायाम की कमी?",
    "en": "Have you noticed any changes in your lifestyle, such as increased stress, poor diet, or lack of exercise?",
    "category": "high blood pressure",
    "symptom": "high blood pressure",
    "risk_factor": False,
  },
  {
    "hi": "क्या आप वर्तमान में उच्च रक्तचाप या अन्य स्वास्थ्य समस्याओं के लिए कोई दवाएं ले रहे हैं?",
    "en": "Are you currently taking any medications for high blood pressure or other health conditions?",
    "category": "high blood pressure",
    "symptom": "high blood pressure",
    "risk_factor": False,
  },
  {
    "hi": "क्या आप शराब, कैफीन, या तंबाकू का सेवन करते हैं, और यदि हां, तो कितनी मात्रा में?",
    "en": "Do you consume alcohol, caffeine, or tobacco, and if so, how much?",
    "category": "high blood pressure",
    "symptom": "high blood pressure",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपने हाल ही में वजन बढ़ाया है या अपने आहार या शारीरिक गतिविधि स्तर में बदलाव महसूस किया है?",
    "en": "Have you recently gained weight or experienced changes in your diet or physical activity levels?",
    "category": "high blood pressure",
    "symptom": "high blood pressure",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको ऐसी कोई अन्य स्वास्थ्य समस्याएं हैं, जैसे मधुमेह, गुर्दे की बीमारी, या स्लीप एपनिया, जो उच्च रक्तचाप में योगदान कर सकती हैं?",
    "en": "Do you have any other health conditions, such as diabetes, kidney disease, or sleep apnea, that might contribute to high blood pressure?",
    "category": "high blood pressure",
    "symptom": "high blood pressure",
    "risk_factor": False,
  }
],
    "low blood pressure": [
  {
    "hi": "क्या आप चक्कर, हल्कापन, थकान, या धुंधली दृष्टि जैसे विशिष्ट लक्षण महसूस कर रहे हैं?",
    "en": "Are you experiencing any specific symptoms like dizziness, lightheadedness, fatigue, or blurred vision?",
    "category": "low blood pressure",
    "symptom": "low blood pressure",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको जल्दी खड़ा होने पर या कुछ समय तक लेटे रहने के बाद हल्का चक्कर या बेहोशी का एहसास होता है?",
    "en": "Do you feel lightheaded or faint when standing up quickly or after lying down for a while?",
    "category": "low blood pressure",
    "symptom": "low blood pressure",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपने हाल ही में कोई बीमारी, संक्रमण, या स्वास्थ्य में कोई बदलाव अनुभव किया है जो आपके रक्तचाप को प्रभावित कर सकता है?",
    "en": "Have you had any recent illnesses, infections, or changes in your health that could affect your blood pressure?",
    "category": "low blood pressure",
    "symptom": "low blood pressure",
    "risk_factor": False,
  },
  {
    "hi": "क्या आप वर्तमान में कोई दवाएं ले रहे हैं, जैसे डाययुरेटिक्स, एंटीडिप्रेसेंट्स, या रक्तचाप की दवाएं, जो निम्न रक्तचाप का कारण बन सकती हैं?",
    "en": "Are you currently taking any medications, such as diuretics, antidepressants, or blood pressure medications, that could cause low blood pressure?",
    "category": "low blood pressure",
    "symptom": "low blood pressure",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपने हाल ही में अपने आहार, तरल पदार्थों का सेवन, या शारीरिक गतिविधि स्तर में कोई महत्वपूर्ण बदलाव महसूस किया है?",
    "en": "Have you experienced any significant changes in your diet, fluid intake, or activity level recently?",
    "category": "low blood pressure",
    "symptom": "low blood pressure",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको ऐसी कोई स्वास्थ्य समस्याएं हैं, जैसे हृदय संबंधी समस्याएं, अंतःस्रावी विकार, या निर्जलीकरण, जो निम्न रक्तचाप में योगदान कर सकती हैं?",
    "en": "Do you have any medical conditions, such as heart problems, endocrine disorders, or dehydration, that could contribute to low blood pressure?",
    "category": "low blood pressure",
    "symptom": "low blood pressure",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपने हाल ही में किसी तनाव का अनुभव किया है या खून की महत्वपूर्ण हानि (जैसे चोट या सर्जरी से) हुई है?",
    "en": "Have you been under any recent stress or experienced a significant loss of blood (e.g., from an injury or surgery)?",
    "category": "low blood pressure",
    "symptom": "low blood pressure",
    "risk_factor": False,
  }
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
      "hi": "क्या सूजन किसी विशेष हिस्से में है?",
      "en": "Is the inflammation localized to any specific area?",
      "category": "localized_inflammation",
      "symptom": None,
      "risk_factor": False,    },
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
      "hi": "क्या सूजन के कारण त्वचा में लालिमा या गर्मी महसूस हो रही है?",
      "en": "Is there any redness or warmth in the skin due to inflammation?",
      "category": "skin_changes_with_inflammation",
      "symptom": "redness",
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

  "hair loss": [
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
      "symptom": "itching",
      "risk_factor": False,    },
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
  ],

  "numbness": [
    {
      "hi": "क्या आपको किसी विशेष हिस्से में सुन्नता महसूस हो रही है?",
      "en": "Are you feeling numbness in any specific area?",
      "category": "localized_numbness",
      "symptom": None,
      "risk_factor": False,    },
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
      "hi": "क्या सुन्नता के साथ झुनझुनी भी हो रही है?",
      "en": "Are you experiencing tingling sensations along with numbness?",
      "category": "tingling_with_numbness",
      "symptom": "tingling",
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

  "itchy eye": [
    {
      "hi": "क्या आपकी आँखों में खुजली लगातार है या आती-जाती है?",
      "en": "Is the itchiness in your eyes constant or does it come and go?",
      "category": "intermittent_itchiness",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या आपकी आँखों में लालिमा भी है?",
      "en": "Is there any redness in your eyes along with itchiness?",
      "category": "redness_with_itchy_eyes",
      "symptom": "redness",
      "risk_factor": False,    },
    {
      "hi": "क्या आपकी आँखों में जलन या दर्द है?",
      "en": "Are you experiencing any burning or pain in your eyes?",
      "category": "burning_pain_with_itchy_eyes",
      "symptom": "burning",
      "risk_factor": False,    },
    {
      "hi": "क्या आपकी आँखों से पानी आ रहा है?",
      "en": "Are your eyes watering?",
      "category": "watery_eyes",
      "symptom": "watery eyes",
      "risk_factor": False,    },
    {
      "hi": "क्या आपकी आँखों की खुजली किसी विशेष पदार्थ से संबंधित है?",
      "en": "Is the itchiness in your eyes related to any specific substance?",
      "category": "triggered_itchy_eyes",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या आपकी आँखों में सूजन है?",
      "en": "Is there any swelling in your eyes?",
      "category": "swelling_with_itchy_eyes",
      "symptom": "swelling",
      "risk_factor": False,    },
    {
      "hi": "क्या आपकी आँखों में कोई धुंधलापन है?",
      "en": "Are you experiencing any blurriness in your vision along with itchy eyes?",
      "category": "blurred_vision_with_itchy_eyes",
      "symptom": "blurred vision",
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
      "hi": "क्या गैस के कारण आपको पेट फूलने का अनुभव हो रहा है?",
      "en": "Are you experiencing bloating due to gas?",
      "category": "bloating_with_gas",
      "symptom": "bloating",
      "risk_factor": False,    },
    {
      "hi": "क्या गैस के साथ आपका मूड भी प्रभावित हो रहा है?",
      "en": "Is your mood being affected along with gas?",
      "category": "mood_changes_with_gas",
      "symptom": "depression",
      "risk_factor": False,    },
    {
      "hi": "क्या गैस के कारण आपकी नींद प्रभावित हो रही है?",
      "en": "Is gas affecting your sleep?",
      "category": "sleep_disturbance_with_gas",
      "symptom": "insomnia",
      "risk_factor": False,    },
  ],

  "hiccup": [
    {
      "hi": "क्या आपके सिकुड़न लगातार हो रही है या आती-जाती हैं?",
      "en": "Are your hiccups continuous or intermittent?",
      "category": "intermittent_hiccups",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या सिकुड़न के साथ आपको दर्द भी हो रहा है?",
      "en": "Are you experiencing pain along with hiccups?",
      "category": "pain_with_hiccups",
      "symptom": "chest pain",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको सिकुड़न के दौरान सांस लेने में कठिनाई हो रही है?",
      "en": "Are you having difficulty breathing during hiccups?",
      "category": "breathing_difficulty_with_hiccups",
      "symptom": "shortness of breath",
      "risk_factor": False,    },
    {
      "hi": "क्या सिकुड़न के कारण आपका खाना निगलने में कठिनाई हो रही है?",
      "en": "Are hiccups causing difficulty in swallowing your food?",
      "category": "swallowing_difficulty_with_hiccups",
      "symptom": "difficulty swallowing",
      "risk_factor": False,    },
    {
      "hi": "क्या सिकुड़न के साथ आपके पेट में दर्द हो रहा है?",
      "en": "Are you experiencing abdominal pain along with hiccups?",
      "category": "abdominal_pain_with_hiccups",
      "symptom": "abdominal pain",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके सिकुड़न के कारण आपकी नींद प्रभावित हो रही है?",
      "en": "Are your hiccups affecting your sleep?",
      "category": "sleep_disturbance_with_hiccups",
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
      "symptom": "pain",
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
      "symptom": "chest pain",
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
      "hi": "क्या नाक से खून बहने के कारण आपके आँखों में भी कोई समस्या हो रही है?",
      "en": "Are you experiencing any issues with your eyes due to nosebleeds?",
      "category": "eye_issues_with_nosebleeds",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या नाक से खून बहने के साथ आपको सिरदर्द भी हो रहा है?",
      "en": "Are you experiencing headaches along with nosebleeds?",
      "category": "headache_with_nosebleeds",
      "symptom": "headache",
      "risk_factor": False,    },
  ],

  "ear ringing": [
    {
      "hi": "क्या कानों में बजने वाली आवाजें लगातार हैं या कभी-कभी आती हैं?",
      "en": "Are the ringing sounds in your ears constant or intermittent?",
      "category": "intermittent_ringing",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या कानों में बजने वाली आवाजें तेज हो रही हैं?",
      "en": "Are the ringing sounds in your ears becoming louder?",
      "category": "intensity_increase_ringing",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या कानों में बजने वाली आवाजें आपके सुनने में कठिनाई पैदा कर रही हैं?",
      "en": "Are the ringing sounds in your ears causing difficulty in hearing?",
      "category": "hearing_difficulty_with_ringing",
      "symptom": "hearing loss",
      "risk_factor": False,    },
    {
      "hi": "क्या कानों में बजने वाली आवाजें किसी विशेष समय पर अधिक होती हैं?",
      "en": "Do the ringing sounds in your ears occur more frequently at any specific time?",
      "category": "time_related_ringing",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या कानों में बजने वाली आवाजें किसी विशेष गतिविधि के दौरान बढ़ती हैं?",
      "en": "Do the ringing sounds in your ears increase during any specific activity?",
      "category": "activity_related_ringing",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या आपको कानों में बजने वाली आवाजें सुनने के साथ साथ सूजन या दर्द भी महसूस हो रहा है?",
      "en": "Are you experiencing swelling or pain in your ears along with ringing sounds?",
      "category": "swelling_pain_with_ringing",
      "symptom": "swelling",
      "risk_factor": False,    },
    {
      "hi": "क्या कानों में बजने वाली आवाजें किसी विशेष दवा के सेवन के कारण हो रही हैं?",
      "en": "Are the ringing sounds in your ears caused by taking any specific medication?",
      "category": "medication_related_ringing",
      "symptom": None,
      "risk_factor": False,    },
  ],

  "decreased appetite": [
    {
      "hi": "क्या भूख में कमी के साथ वजन घट रहा है?",
      "en": "Are you losing weight along with decreased appetite?",
      "category": "weight_loss_with_decreased_appetite",
      "symptom": "weight loss",
      "risk_factor": False,    },
    {
      "hi": "क्या भूख में कमी के कारण आपकी ऊर्जा स्तर प्रभावित हो रहा है?",
      "en": "Is your energy level being affected due to decreased appetite?",
      "category": "energy_deficit_with_decreased_appetite",
      "symptom": "fatigue",
      "risk_factor": False,    },
    {
      "hi": "क्या भूख में कमी के साथ पेट में दर्द हो रहा है?",
      "en": "Are you experiencing abdominal pain along with decreased appetite?",
      "category": "abdominal_pain_with_decreased_appetite",
      "symptom": "abdominal pain",
      "risk_factor": False,    },
    {
      "hi": "क्या भूख में कमी के कारण आपको थकान महसूस हो रही है?",
      "en": "Are you feeling fatigued due to decreased appetite?",
      "category": "fatigue_with_decreased_appetite",
      "symptom": "fatigue",
      "risk_factor": False,    },
    {
      "hi": "क्या आपकी डाइट में कोई विशेष परिवर्तन हुआ है?",
      "en": "Has there been any specific change in your diet?",
      "category": "diet_changes",
      "symptom": None,
      "risk_factor": False,    },
  ],

  "increased appetite": [
    {
      "hi": "क्या आपकी भूख में अचानक बढ़ोतरी हो गई है?",
      "en": "Has there been a sudden increase in your appetite?",
      "category": "sudden_increase_appetite",
      "symptom": "increased appetite",
      "risk_factor": False,    },
    {
      "hi": "क्या वजन बढ़ने के साथ आपकी भूख में भी वृद्धि हुई है?",
      "en": "Has your appetite increased along with weight gain?",
      "category": "appetite_increase_with_weight_gain",
      "symptom": "weight gain",
      "risk_factor": False,    },
    {
      "hi": "क्या आपकी भूख में वृद्धि के कारण आपकी डाइट में कोई विशेष बदलाव हुआ है?",
      "en": "Has there been any specific change in your diet due to increased appetite?",
      "category": "diet_changes_with_increased_appetite",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या भूख में वृद्धि के साथ आपको थकान भी महसूस हो रही है?",
      "en": "Are you feeling fatigued along with increased appetite?",
      "category": "fatigue_with_increased_appetite",
      "symptom": "fatigue",
      "risk_factor": False,    },
    {
      "hi": "क्या आपकी भूख में वृद्धि के कारण आपकी नींद प्रभावित हो रही है?",
      "en": "Is your sleep being affected due to increased appetite?",
      "category": "sleep_disturbance_with_increased_appetite",
      "symptom": "insomnia",
      "risk_factor": False,    },
    {
      "hi": "क्या भूख में वृद्धि के साथ आपका मूड भी प्रभावित हो रहा है?",
      "en": "Is your mood being affected along with increased appetite?",
      "category": "mood_changes_with_increased_appetite",
      "symptom": "depression",
      "risk_factor": False,    },
  ],

  "feeling full": [
    {
      "hi": "क्या आपको खाने के तुरंत बाद भरा हुआ महसूस होता है?",
      "en": "Do you feel full immediately after eating?",
      "category": "early_satiety",
      "symptom": "feeling full quickly",
      "risk_factor": False,    },
    {
      "hi": "क्या भरा हुआ महसूस होने के साथ पेट में दर्द भी हो रहा है?",
      "en": "Are you experiencing abdominal pain along with feeling full quickly?",
      "category": "abdominal_pain_with_satiety",
      "symptom": "abdominal pain",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको खाने में कठिनाई हो रही है?",
      "en": "Are you having difficulty eating?",
      "category": "eating_difficulty",
      "symptom": "difficulty swallowing",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके खाने के साथ किसी विशेष प्रकार का दर्द होता है?",
      "en": "Do you experience any specific type of pain while eating?",
      "category": "pain_with_eating",
      "symptom": "pain",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको खाने के बाद वजन बढ़ने की समस्या हो रही है?",
      "en": "Are you having issues with weight gain after eating?",
      "category": "weight_gain_after_eating",
      "symptom": "weight gain",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको खाने के बाद सूजन महसूस हो रही है?",
      "en": "Are you feeling bloated after eating?",
      "category": "bloating_after_eating",
      "symptom": "bloating",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको खाने के बाद थकान महसूस हो रही है?",
      "en": "Are you feeling fatigued after eating?",
      "category": "fatigue_after_eating",
      "symptom": "fatigue",
      "risk_factor": False,    },
  ],

  "dark urine": [
    {
      "hi": "क्या आपका पेशाब गहरा रंग का हो गया है?",
      "en": "Has your urine become dark-colored?",
      "category": "dark_urine",
      "symptom": "dark urine",
      "risk_factor": False,    },
    {
      "hi": "क्या आपका पेशाब सामान्य से अधिक है?",
      "en": "Is your urine output more than usual?",
      "category": "increased_urine_output",
      "symptom": "frequent urination",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको पेशाब के साथ कोई दर्द भी हो रहा है?",
      "en": "Are you experiencing any pain while urinating?",
      "category": "pain_with_dark_urine",
      "symptom": "urinary pain",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके पेशाब में खून की लकीरें आ रही हैं?",
      "en": "Are you noticing blood streaks in your urine?",
      "category": "blood_streaks_in_urine",
      "symptom": "blood in urine",
      "risk_factor": False,    },
    {
      "hi": "क्या गहरे पेशाब के कारण आपकी त्वचा में कोई परिवर्तन आ रहा है?",
      "en": "Is there any change in your skin due to dark urine?",
      "category": "skin_changes_with_dark_urine",
      "symptom": "skin discoloration",
      "risk_factor": False,    },
  ],

  "light colored stool": [
    {
      "hi": "क्या हल्के रंग के मल के साथ आपको पेट में दर्द भी हो रहा है?",
      "en": "Are you experiencing abdominal pain along with light-colored stools?",
      "category": "abdominal_pain_with_light_stools",
      "symptom": "abdominal pain",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके मल में कोई अन्य परिवर्तन आ रहा है?",
      "en": "Are you noticing any other changes in your stool?",
      "category": "other_changes_with_light_stools",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या आपके मल में कोई रक्त है?",
      "en": "Is there any blood in your stool?",
      "category": "blood_in_stool",
      "symptom": "blood in stool",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको मल त्यागने में कठिनाई हो रही है?",
      "en": "Are you having difficulty in passing stool?",
      "category": "difficulty_passing_stool",
      "symptom": "constipation",
      "risk_factor": False,    },
    {
      "hi": "क्या हल्के रंग के मल के साथ आपको उल्टी भी हो रही है?",
      "en": "Are you experiencing vomiting along with light-colored stools?",
      "category": "vomiting_with_light_stools",
      "symptom": "vomiting",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके मल त्यागने के साथ आपको पसीना आ रहा है?",
      "en": "Are you sweating while passing stool?",
      "category": "sweating_with_light_stools",
      "symptom": "sweating",
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

  "delayed healing": [
    {
      "hi": "क्या आपके घाव या चोटों का ठीक होने में समय अधिक लग रहा है?",
      "en": "Are your wounds or injuries taking longer to heal?",
      "category": "delayed_healing",
      "symptom": "delayed healing",
      "risk_factor": False,    },
    {
      "hi": "क्या ठीक होने में देरी के साथ आपको दर्द भी हो रहा है?",
      "en": "Are you experiencing pain along with delayed healing?",
      "category": "pain_with_delayed_healing",
      "symptom": "pain",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके घावों में कोई संक्रमण भी हो रही है?",
      "en": "Are your wounds getting infected while healing?",
      "category": "infection_with_delayed_healing",
      "symptom": "infection",
      "risk_factor": False,    },
    {
      "hi": "क्या ठीक होने में देरी के कारण आपकी त्वचा में कोई परिवर्तन आ रहा है?",
      "en": "Is there any change in your skin due to delayed healing?",
      "category": "skin_changes_with_delayed_healing",
      "symptom": "skin discoloration",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको घावों के ठीक होने में किसी विशेष दवा का सेवन करना पड़ रहा है?",
      "en": "Are you taking any specific medication for delayed healing of wounds?",
      "category": "medication_with_delayed_healing",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या आपके घाव या चोटों के ठीक होने में कोई विशेष कारण है?",
      "en": "Is there any specific reason for the delayed healing of your wounds or injuries?",
      "category": "specific_cause_delayed_healing",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या आपको घावों के ठीक होने के दौरान कमजोरी महसूस हो रही है?",
      "en": "Are you feeling weak during the healing of your wounds?",
      "category": "weakness_with_delayed_healing",
      "symptom": "weakness",
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

  "skin burn": [
    {
      "hi": "क्या आपको त्वचा पर जलन या दर्द महसूस हो रहा है?",
      "en": "Are you feeling burning or pain on your skin?",
      "category": "burning_pain_with_skin_burn",
      "symptom": "burning",
      "risk_factor": False,    },
    {
      "hi": "क्या त्वचा पर जलने के कारण सूजन हो रही है?",
      "en": "Is there any swelling due to the skin burn?",
      "category": "swelling_with_skin_burn",
      "symptom": "swelling",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको त्वचा पर दाने या फफोले हो रहे हैं?",
      "en": "Are you developing blisters or bumps on your skin?",
      "category": "blisters_bumps_with_skin_burn",
      "symptom": "skin lesions",
      "risk_factor": False,    },
    {
      "hi": "क्या त्वचा पर जलने के बाद त्वचा लाल हो गई है?",
      "en": "Has your skin turned red after the burn?",
      "category": "redness_with_skin_burn",
      "symptom": "redness",
      "risk_factor": False,    },
    {
      "hi": "क्या त्वचा पर जलने के कारण आपको दर्द में वृद्धि हो रही है?",
      "en": "Is the pain increasing due to the skin burn?",
      "category": "pain_increase_with_skin_burn",
      "symptom": "pain",
      "risk_factor": False,    },
    {
      "hi": "क्या त्वचा पर जलने के कारण कोई संक्रमण हो गया है?",
      "en": "Has the skin burn led to any infection?",
      "category": "infection_with_skin_burn",
      "symptom": "infection",
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
      "hi": "क्या आपको ठंड महसूस होने के साथ त्वचा में कोई परिवर्तन हो रहा है?",
      "en": "Are you noticing any changes in your skin due to feeling cold?",
      "category": "skin_changes_with_feeling_cold",
      "symptom": "skin discoloration",
      "risk_factor": False,    },
    {
      "hi": "क्या ठंड महसूस होने के कारण आपकी नींद प्रभावित हो रही है?",
      "en": "Is feeling cold affecting your sleep?",
      "category": "sleep_disturbance_with_feeling_cold",
      "symptom": "insomnia",
      "risk_factor": False,    },
    {
      "hi": "क्या ठंड महसूस होने के कारण आपके शरीर में कोई कमजोरी आ रही है?",
      "en": "Is feeling cold causing any weakness in your body?",
      "category": "weakness_with_feeling_cold",
      "symptom": "weakness",
      "risk_factor": False,    },
  ],

  "double vision": [
    {
      "hi": "क्या आपकी दृष्टि दोहरी हो रही है लगातार या कभी-कभी?",
      "en": "Is your vision double continuously or intermittently?",
      "category": "intermittent_double_vision",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या दोहरी दृष्टि के साथ आपको सिरदर्द भी हो रहा है?",
      "en": "Are you experiencing headaches along with double vision?",
      "category": "headache_with_double_vision",
      "symptom": "headache",
      "risk_factor": False,    },
    {
      "hi": "क्या दोहरी दृष्टि किसी विशेष समय या गतिविधि के दौरान बढ़ती है?",
      "en": "Does your double vision increase during any specific time or activity?",
      "category": "activity_related_double_vision",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या दोहरी दृष्टि के साथ आपके आँखों में दर्द भी हो रहा है?",
      "en": "Are you experiencing eye pain along with double vision?",
      "category": "eye_pain_with_double_vision",
      "symptom": "eye pain",
      "risk_factor": False,    },
    {
      "hi": "क्या दोहरी दृष्टि के कारण आपको चलने-फिरने में कठिनाई हो रही है?",
      "en": "Are you having difficulty walking due to double vision?",
      "category": "walking_difficulty_with_double_vision",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या दोहरी दृष्टि अचानक शुरू हुई है या धीरे-धीरे?",
      "en": "Did your double vision start suddenly or gradually?",
      "category": "sudden_graduate_double_vision",
      "symptom": None,
      "risk_factor": False,    },
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

  "eye discharge": [
    {
      "hi": "क्या आपकी आँखों से अधिक मात्रा में स्राव आ रहा है?",
      "en": "Are you experiencing excessive discharge from your eyes?",
      "category": "excessive_eye_discharge",
      "symptom": "eye discharge",
      "risk_factor": False,    },
    {
      "hi": "क्या आँखों में स्राव के साथ सूजन भी है?",
      "en": "Is there any swelling along with discharge in your eyes?",
      "category": "swelling_with_eye_discharge",
      "symptom": "swelling",
      "risk_factor": False,    },
    {
      "hi": "क्या आँखों में स्राव के साथ खुजली या जलन हो रही है?",
      "en": "Are you experiencing itching or burning sensations in your eyes along with discharge?",
      "category": "itching_burning_with_eye_discharge",
      "symptom": "itching",
      "risk_factor": False,    },
    {
      "hi": "क्या आँखों में स्राव के कारण आपकी दृष्टि प्रभावित हो रही है?",
      "en": "Is the discharge in your eyes affecting your vision?",
      "category": "vision_impact_with_eye_discharge",
      "symptom": "blurred vision",
      "risk_factor": False,    },
    {
      "hi": "क्या स्राव में रंग में कोई परिवर्तन आया है?",
      "en": "Has there been any change in the color of the discharge?",
      "category": "discharge_color_change",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या स्राव के कारण आपकी आँखों में सूजन हो रही है?",
      "en": "Is there any swelling in your eyes due to discharge?",
      "category": "swelling_with_eye_discharge",
      "symptom": "swelling",
      "risk_factor": False,    },
  ],

  "ear discharge": [

    {
      "hi": "क्या स्राव के साथ कान में दर्द भी हो रहा है?",
      "en": "Are you experiencing pain in your ears along with discharge?",
      "category": "pain_with_ear_discharge",
      "symptom": "ear pain",
      "risk_factor": False,    },
    {
      "hi": "क्या स्राव का रंग में कोई परिवर्तन आया है?",
      "en": "Has there been any change in the color of the discharge?",
      "category": "discharge_color_change_ear",
      "symptom": None,
      "risk_factor": False,    },
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
    {
      "hi": "क्या स्राव के कारण कान में खुजली हो रही है?",
      "en": "Are you experiencing itching in your ears due to discharge?",
      "category": "itching_with_ear_discharge",
      "symptom": "itching",
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
      "hi": "क्या संतुलन बिगड़ने के साथ आपको कोई अन्य लक्षण भी महसूस हो रहे हैं?",
      "en": "Are you experiencing any other symptoms along with balance problems?",
      "category": "other_symptoms_with_balance_problems",
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
  ],

  "taste change": [
    {
      "hi": "क्या आपके स्वाद में कोई बदलाव आया है?",
      "en": "Have you noticed any changes in your taste?",
      "category": "taste_changes",
      "symptom": "taste changes",
      "risk_factor": False,    },
    {
      "hi": "क्या स्वाद में बदलाव के साथ आप कुछ खास चीज़ों का स्वाद नहीं ले पा रहे हैं?",
      "en": "Are you unable to taste certain specific things along with taste changes?",
      "category": "specific_taste_changes",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या आपको स्वाद में कमी या बढ़ोतरी महसूस हो रही है?",
      "en": "Are you experiencing a decrease or increase in taste?",
      "category": "decrease_increase_taste",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या स्वाद में बदलाव के साथ आपकी भूख प्रभावित हो रही है?",
      "en": "Is your appetite being affected due to taste changes?",
      "category": "appetite_impact_with_taste_changes",
      "symptom": "decreased appetite",
      "risk_factor": False,    },
    {
      "hi": "क्या स्वाद में बदलाव के कारण आपको खाना पसंद नहीं आता?",
      "en": "Are you not liking food due to taste changes?",
      "category": "food_dislike_with_taste_changes",
      "symptom": "decreased appetite",
      "risk_factor": False,    },
    {
      "hi": "क्या स्वाद में बदलाव अचानक शुरू हुआ है या धीरे-धीरे?",
      "en": "Did your taste changes start suddenly or gradually?",
      "category": "sudden_graduate_taste_changes",
      "symptom": None,
      "risk_factor": False,    },
  ],

  "smell change": [
    {
      "hi": "क्या आपकी गंध में कोई बदलाव आया है?",
      "en": "Have you noticed any changes in your sense of smell?",
      "category": "smell_changes",
      "symptom": "smell changes",
      "risk_factor": False,    },
    {
      "hi": "क्या गंध में बदलाव के साथ आपकी भूख प्रभावित हो रही है?",
      "en": "Is your appetite being affected due to changes in smell?",
      "category": "appetite_impact_with_smell_changes",
      "symptom": "decreased appetite",
      "risk_factor": False,    },
    {
      "hi": "क्या गंध में बदलाव के कारण आप कुछ खास चीजों की गंध नहीं ले पा रहे हैं?",
      "en": "Are you unable to detect the smell of certain specific things due to smell changes?",
      "category": "specific_smell_changes",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या गंध में बदलाव अचानक शुरू हुआ है या धीरे-धीरे?",
      "en": "Did your smell changes start suddenly or gradually?",
      "category": "sudden_graduate_smell_changes",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या गंध में बदलाव के साथ आपके मूड में भी कोई परिवर्तन आया है?",
      "en": "Has your mood changed along with smell changes?",
      "category": "mood_changes_with_smell_changes",
      "symptom": "depression",
      "risk_factor": False,    },
    {
      "hi": "क्या गंध में बदलाव के कारण आपको खाने में कोई समस्या हो रही है?",
      "en": "Are you having any issues with eating due to smell changes?",
      "category": "eating_issues_with_smell_changes",
      "symptom": "difficulty swallowing",
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
      "hi": "क्या अनियमित धड़कन के कारण आपको सांस लेने में कठिनाई हो रही है?",
      "en": "Are you having difficulty breathing due to an irregular heartbeat?",
      "category": "breathing_difficulty_with_irregular_heartbeat",
      "symptom": "shortness of breath",
      "risk_factor": False,    },
    {
      "hi": "क्या अनियमित धड़कन अचानक शुरू हुई है या धीरे-धीरे?",
      "en": "Did your irregular heartbeat start suddenly or gradually?",
      "category": "sudden_graduate_irregular_heartbeat",
      "symptom": None,
      "risk_factor": False,    },
  ],

  "neck pain": [
    {
      "hi": "क्या आपकी गर्दन में दर्द लगातार है या आता-जाता है?",
      "en": "Is your neck pain constant or does it come and go?",
      "category": "intermittent_neck_pain",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या गर्दन का दर्द किसी विशेष गतिविधि के दौरान बढ़ता है?",
      "en": "Does your neck pain increase during any specific activity?",
      "category": "activity_related_neck_pain",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या गर्दन के दर्द के साथ सिरदर्द भी हो रहा है?",
      "en": "Are you experiencing headaches along with neck pain?",
      "category": "headache_with_neck_pain",
      "symptom": "headache",
      "risk_factor": False,    },
    {
      "hi": "क्या गर्दन में दर्द के साथ कोई सूजन भी है?",
      "en": "Is there any swelling along with neck pain?",
      "category": "swelling_with_neck_pain",
      "symptom": "swelling",
      "risk_factor": False,    },
    {
      "hi": "क्या गर्दन के दर्द के कारण आपकी गतिशीलता प्रभावित हो रही है?",
      "en": "Is your mobility being affected due to neck pain?",
      "category": "mobility_impact_with_neck_pain",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या गर्दन का दर्द अचानक शुरू हुआ है या धीरे-धीरे?",
      "en": "Did your neck pain start suddenly or gradually?",
      "category": "sudden_graduate_neck_pain",
      "symptom": None,
      "risk_factor": False,    },
  ],

  "muscle spasm": [
    {
      "hi": "क्या आपको मांसपेशियों में अचानक स्पैसम्स महसूस हो रहे हैं?",
      "en": "Are you experiencing sudden muscle spasms?",
      "category": "sudden_muscle_spasms",
      "symptom": "muscle spasms",
      "risk_factor": False,    },
    {
      "hi": "क्या मांसपेशियों में स्पैसम्स लगातार हो रहे हैं या कभी-कभी?",
      "en": "Are muscle spasms occurring continuously or intermittently?",
      "category": "intermittent_muscle_spasms",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या स्पैसम्स के साथ दर्द भी हो रहा है?",
      "en": "Are you experiencing pain along with muscle spasms?",
      "category": "pain_with_muscle_spasms",
      "symptom": "pain",
      "risk_factor": False,    },
    {
      "hi": "क्या मांसपेशियों में स्पैसम्स किसी विशेष गतिविधि के दौरान बढ़ते हैं?",
      "en": "Do muscle spasms increase during any specific activity?",
      "category": "activity_related_muscle_spasms",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या स्पैसम्स के कारण आपकी गतिशीलता प्रभावित हो रही है?",
      "en": "Are your mobility being affected due to muscle spasms?",
      "category": "mobility_impact_with_muscle_spasms",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या मांसपेशियों में स्पैसम्स के साथ सूजन भी हो रही है?",
      "en": "Is there any swelling along with muscle spasms?",
      "category": "swelling_with_muscle_spasms",
      "symptom": "swelling",
      "risk_factor": False,    },

  ],

  "spasm": [
    {
      "hi": "कक्या आप अचानक ऐंठन का अनुभव कर रहे हैं?",
      "en": "Are you experiencing sudden spasms?",
      "category": "sudden_spasms",
      "symptom": "spasms",
      "risk_factor": False,    },
    {
      "hi": "ऐंठन कहाँ स्थित है (जैसे निचली पीठ, ऊपरी पीठ, या गर्दन)?",
      "en": "Where is the spasm located (e.g., lower back, upper back, or neck)?",
      "category": "back_spasms",
      "symptom": "location of spasm",
      "risk_factor": False,    },
    {
      "hi": "क्या ऐंठन लगातार या रुक-रुक कर हो रही है?",
      "en": "Are spasms occurring continuously or intermittently?",
      "category": "intermittent_muscle_spasms",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या आप ऐंठन के साथ दर्द का भी अनुभव कर रहे हैं?",
      "en": "Are you experiencing pain along with spasms?",
      "category": "pain_with_muscle_spasms",
      "symptom": "pain",
      "risk_factor": False,    },
    {
      "hi": "क्या किसी विशिष्ट गतिविधि के दौरान ऐंठन बढ़ जाती है?",
      "en": "Do spasms increase during any specific activity?",
      "category": "activity_related_muscle_spasms",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या ऐंठन के कारण आपकी गतिशीलता प्रभावित हो रही है?",
      "en": "Are your mobility being affected due to spasms?",
      "category": "mobility_impact_with_muscle_spasms",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या ऐंठन के साथ-साथ कोई सूजन भी है?",
      "en": "Is there any swelling along with spasms?",
      "category": "swelling_with_muscle_spasms",
      "symptom": "swelling",
      "risk_factor": False,    },

  ],

  "muscle strain": [

    {
      "hi": "क्या मांसपेशियों में तनाव के साथ दर्द भी हो रहा है?",
      "en": "Are you experiencing pain along with muscle strain?",
      "category": "pain_with_muscle_strain",
      "symptom": "pain",
      "risk_factor": False,    },
    {
      "hi": "क्या मांसपेशियों में तनाव किसी विशेष गतिविधि के दौरान बढ़ता है?",
      "en": "Does muscle strain increase during any specific activity?",
      "category": "activity_related_muscle_strain",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या मांसपेशियों में तनाव के कारण आपकी गतिशीलता प्रभावित हो रही है?",
      "en": "Is your mobility being affected due to muscle strain?",
      "category": "mobility_impact_with_muscle_strain",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या मांसपेशियों में तनाव के साथ सूजन भी हो रही है?",
      "en": "Is there any swelling along with muscle strain?",
      "category": "swelling_with_muscle_strain",
      "symptom": "swelling",
      "risk_factor": False,    },
    {
      "hi": "क्या मांसपेशियों में तनाव अचानक शुरू हुआ है या धीरे-धीरे?",
      "en": "Did your muscle strain start suddenly or gradually?",
      "category": "sudden_graduate_muscle_strain",
      "symptom": None,
      "risk_factor": False,    },
  ],

  "muscle injury": [
    {
      "hi": "क्या मांसपेशी में चोट के साथ दर्द भी हो रहा है?",
      "en": "Are you experiencing pain along with the muscle injury?",
      "category": "pain_with_muscle_injury",
      "symptom": "pain",
      "risk_factor": False,    },
    {
      "hi": "क्या मांसपेशी में चोट के कारण आपकी गतिशीलता प्रभावित हो रही है?",
      "en": "Is your mobility being affected due to the muscle injury?",
      "category": "mobility_impact_with_muscle_injury",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या मांसपेशी में चोट के साथ सूजन भी हो रही है?",
      "en": "Is there any swelling along with the muscle injury?",
      "category": "swelling_with_muscle_injury",
      "symptom": "swelling",
      "risk_factor": False,    },
    {
      "hi": "क्या मांसपेशी में चोट के कारण आपको कमजोरी महसूस हो रही है?",
      "en": "Are you feeling weak due to the muscle injury?",
      "category": "weakness_with_muscle_injury",
      "symptom": "weakness",
      "risk_factor": False,    },
    {
      "hi": "क्या मांसपेशी में चोट अचानक हुई है या किसी दुर्घटना के बाद?",
      "en": "Did your muscle injury occur suddenly or after an accident?",
      "category": "sudden_or_accident_related_muscle_injury",
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



  "mole": [
    {
      "hi": "क्या आपके शरीर पर मौल्स में कोई बदलाव आया है?",
      "en": "Have there been any changes in your moles?",
      "category": "mole_changes",
      "symptom": "moles",
      "risk_factor": False,    },
    {
      "hi": "क्या मौल्स का आकार, रंग या आकृति बदल गई है?",
      "en": "Has the size, color, or shape of your moles changed?",
      "category": "size_color_shape_changes_with_moles",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या मौल्स से खून आ रहा है या दर्द हो रहा है?",
      "en": "Are you experiencing bleeding or pain from your moles?",
      "category": "bleeding_pain_with_moles",
      "symptom": "bleeding",
      "risk_factor": False,    },
    {
      "hi": "क्या मौल्स किसी विशेष समय पर अधिक दिखाई देते हैं?",
      "en": "Do your moles become more noticeable at any specific time?",
      "category": "time_related_moles",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या मौल्स के कारण आपकी त्वचा में कोई अन्य परिवर्तन हो रहा है?",
      "en": "Are there any other changes in your skin due to moles?",
      "category": "skin_changes_with_moles",
      "symptom": "skin discoloration",
      "risk_factor": False,    },
    {
      "hi": "क्या मौल्स अचानक हो गए हैं या धीरे-धीरे?",
      "en": "Did your moles appear suddenly or gradually?",
      "category": "sudden_graduate_moles",
      "symptom": None,
      "risk_factor": False,    },
  ],

  "skin lesion": [
    {
      "hi": "क्या आपको त्वचा पर घाव या गांठें महसूस हो रही हैं?",
      "en": "Are you feeling sores or lumps on your skin?",
      "category": "sores_lumps_with_skin_lesions",
      "symptom": "skin lesions",
      "risk_factor": False,    },
    {
      "hi": "क्या त्वचा पर घावों के साथ सूजन भी है?",
      "en": "Is there any swelling along with sores on your skin?",
      "category": "swelling_with_skin_lesions",
      "symptom": "swelling",
      "risk_factor": False,    },
    {
      "hi": "क्या त्वचा पर घावों के साथ दर्द भी हो रहा है?",
      "en": "Are you experiencing pain along with sores on your skin?",
      "category": "pain_with_skin_lesions",
      "symptom": "pain",
      "risk_factor": False,    },
    {
      "hi": "क्या त्वचा पर घाव धीरे-धीरे बढ़ रहे हैं या स्थिर हैं?",
      "en": "Are the sores on your skin increasing gradually or remaining static?",
      "category": "increasing_vs_static_skin_lesions",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या त्वचा पर घावों का रंग बदल रहा है?",
      "en": "Are the sores on your skin changing in color?",
      "category": "color_changes_with_skin_lesions",
      "symptom": "skin discoloration",
      "risk_factor": False,    },
    {
      "hi": "क्या त्वचा पर घावों के साथ खुजली या जलन हो रही है?",
      "en": "Are you experiencing itching or burning sensations along with sores on your skin?",
      "category": "itching_burning_with_skin_lesions",
      "symptom": "itching",
      "risk_factor": False,    },
    {
      "hi": "क्या त्वचा पर घावों के कारण आपकी त्वचा में कोई अन्य परिवर्तन हो रहा है?",
      "en": "Are there any other changes in your skin due to sores?",
      "category": "other_skin_changes_with_skin_lesions",
      "symptom": None,
      "risk_factor": False,    },
  ],

  "skin lump": [
    {
      "hi": "क्या आपको त्वचा पर गांठें या गांठे महसूस हो रही हैं?",
      "en": "Are you feeling lumps or bumps on your skin?",
      "category": "skin_lumps",
      "symptom": "skin lumps",
      "risk_factor": False,    },
    {
      "hi": "क्या त्वचा पर गांठों के साथ सूजन भी है?",
      "en": "Is there any swelling along with lumps on your skin?",
      "category": "swelling_with_skin_lumps",
      "symptom": "swelling",
      "risk_factor": False,    },
    {
      "hi": "क्या त्वचा पर गांठों के साथ दर्द भी हो रहा है?",
      "en": "Are you experiencing pain along with lumps on your skin?",
      "category": "pain_with_skin_lumps",
      "symptom": "pain",
      "risk_factor": False,    },
    {
      "hi": "क्या त्वचा पर गांठें स्थिर हैं या बढ़ रही हैं?",
      "en": "Are the lumps on your skin static or increasing?",
      "category": "static_increasing_skin_lumps",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या त्वचा पर गांठों का रंग बदल रहा है?",
      "en": "Are the lumps on your skin changing in color?",
      "category": "color_changes_with_skin_lumps",
      "symptom": "skin discoloration",
      "risk_factor": False,    },
    {
      "hi": "क्या त्वचा पर गांठों के साथ खुजली या जलन हो रही है?",
      "en": "Are you experiencing itching or burning sensations along with lumps on your skin?",
      "category": "itching_burning_with_skin_lumps",
      "symptom": "itching",
      "risk_factor": False,    },
    {
      "hi": "क्या त्वचा पर गांठों के कारण आपकी त्वचा में कोई अन्य परिवर्तन हो रहा है?",
      "en": "Are there any other changes in your skin due to lumps?",
      "category": "other_skin_changes_with_skin_lumps",
      "symptom": None,
      "risk_factor": False,    },
  ],

  "skin bump": [
    {
      "hi": "क्या आपको त्वचा पर उभार या गांठें महसूस हो रही हैं?",
      "en": "Are you feeling bumps or lumps on your skin?",
      "category": "skin_bumps",
      "symptom": "skin bumps",
      "risk_factor": False,    },
    {
      "hi": "क्या त्वचा पर उभार के साथ सूजन भी है?",
      "en": "Is there any swelling along with bumps on your skin?",
      "category": "swelling_with_skin_bumps",
      "symptom": "swelling",
      "risk_factor": False,    },
    {
      "hi": "क्या त्वचा पर उभार के साथ दर्द भी हो रहा है?",
      "en": "Are you experiencing pain along with bumps on your skin?",
      "category": "pain_with_skin_bumps",
      "symptom": "pain",
      "risk_factor": False,    },
    {
      "hi": "क्या त्वचा पर उभार धीरे-धीरे बढ़ रहे हैं या स्थिर हैं?",
      "en": "Are the bumps on your skin increasing gradually or remaining static?",
      "category": "increasing_vs_static_skin_bumps",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या त्वचा पर उभार का रंग बदल रहा है?",
      "en": "Are the bumps on your skin changing in color?",
      "category": "color_changes_with_skin_bumps",
      "symptom": "skin discoloration",
      "risk_factor": False,    },
    {
      "hi": "क्या त्वचा पर उभार के साथ खुजली या जलन हो रही है?",
      "en": "Are you experiencing itching or burning sensations along with bumps on your skin?",
      "category": "itching_burning_with_skin_bumps",
      "symptom": "itching",
      "risk_factor": False,    },
    {
      "hi": "क्या त्वचा पर उभार के कारण आपकी त्वचा में कोई अन्य परिवर्तन हो रहा है?",
      "en": "Are there any other changes in your skin due to bumps?",
      "category": "other_skin_changes_with_skin_bumps",
      "symptom": None,
      "risk_factor": False,    },
  ],

  "skin cracking": [
    {
      "hi": "क्या आपकी त्वचा दरार खा रही है?",
      "en": "Is your skin cracking?",
      "category": "skin_cracking",
      "symptom": "skin cracking",
      "risk_factor": False,    },
    {
      "hi": "क्या दरारों के साथ त्वचा में सूजन भी है?",
      "en": "Is there any swelling along with skin cracking?",
      "category": "swelling_with_skin_cracking",
      "symptom": "swelling",
      "risk_factor": False,    },
    {
      "hi": "क्या त्वचा की दरारों के साथ खुजली या जलन हो रही है?",
      "en": "Are you experiencing itching or burning sensations along with skin cracking?",
      "category": "itching_burning_with_skin_cracking",
      "symptom": "itching",
      "risk_factor": False,    },
    {
      "hi": "क्या त्वचा की दरारें किसी विशेष समय पर अधिक होती हैं?",
      "en": "Do your skin cracks occur more frequently at any specific time?",
      "category": "time_related_skin_cracking",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या त्वचा की दरारें स्थिर हैं या बढ़ रही हैं?",
      "en": "Are your skin cracks static or increasing?",
      "category": "increasing_vs_static_skin_cracking",
      "symptom": None,
      "risk_factor": False,    },

    {
      "hi": "क्या त्वचा की दरारें अचानक शुरू हुई हैं या धीरे-धीरे?",
      "en": "Did your skin cracks start suddenly or gradually?",
      "category": "sudden_graduate_skin_cracking",
      "symptom": None,
      "risk_factor": False,    },
  ],

  "itching": [
    {
      "hi": "क्या आपकी त्वचा में खुजली लगातार है या कभी-कभी आती है?",
      "en": "Is the itching on your skin continuous or intermittent?",
      "category": "intermittent_skin_itching",
      "symptom": "skin itching",
      "risk_factor": False,    },
    {
      "hi": "क्या खुजली के साथ त्वचा में लालिमा भी है?",
      "en": "Is there any redness on your skin along with itching?",
      "category": "redness_with_skin_itching",
      "symptom": "redness",
      "risk_factor": False,    },
    {
      "hi": "क्या खुजली के कारण आपको त्वचा में सूजन हो रही है?",
      "en": "Is itching causing any swelling on your skin?",
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
      "en": "Are there any cracks or blisters on your skin along with itching?",
      "category": "cracks_blisters_with_skin_itching",
      "symptom": "skin lesions",
      "risk_factor": False,    },
    {
      "hi": "क्या आपकी त्वचा में खुजली के कारण कोई अन्य परिवर्तन हो रहा है?",
      "en": "Are there any other changes in your skin due to itching?",
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

  "skin pain": [
    {
      "hi": "क्या आपको त्वचा पर दर्द महसूस हो रहा है?",
      "en": "Are you feeling pain on your skin?",
      "category": "skin_pain",
      "symptom": "skin pain",
      "risk_factor": False,    },
    {
      "hi": "क्या त्वचा के दर्द के साथ कोई सूजन भी है?",
      "en": "Is there any swelling along with skin pain?",
      "category": "swelling_with_skin_pain",
      "symptom": "swelling",
      "risk_factor": False,    },
    {
      "hi": "क्या त्वचा के दर्द के कारण आपको चलने-फिरने में कठिनाई हो रही है?",
      "en": "Are you having difficulty walking due to skin pain?",
      "category": "walking_difficulty_with_skin_pain",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या त्वचा के दर्द के साथ कोई दरार या फफोले हो रहे हैं?",
      "en": "Are there any cracks or blisters on your skin along with pain?",
      "category": "cracks_blisters_with_skin_pain",
      "symptom": "skin lesions",
      "risk_factor": False,    },
    {
      "hi": "क्या दर्द के साथ आपकी त्वचा में लालिमा हो गई है?",
      "en": "Has your skin turned red along with the pain?",
      "category": "redness_with_skin_pain",
      "symptom": "redness",
      "risk_factor": False,    },
    {
      "hi": "क्या त्वचा के दर्द के साथ आपको खुजली या जलन भी हो रही है?",
      "en": "Are you experiencing itching or burning sensations along with skin pain?",
      "category": "itching_burning_with_skin_pain",
      "symptom": "itching",
      "risk_factor": False,    },
    {
      "hi": "क्या त्वचा का दर्द अचानक शुरू हुआ है या धीरे-धीरे?",
      "en": "Did the skin pain start suddenly or gradually?",
      "category": "sudden_graduate_skin_pain",
      "symptom": None,
      "risk_factor": False,    },
  ],

  "skin swelling": [
    {
      "hi": "क्या आपकी त्वचा में सूजन हो रही है?",
      "en": "Are you experiencing swelling in your skin?",
      "category": "skin_swelling",
      "symptom": "swelling",
      "risk_factor": False,    },
    {
      "hi": "क्या सूजन के साथ त्वचा में लालिमा भी है?",
      "en": "Is there any redness in your skin along with swelling?",
      "category": "redness_with_skin_swelling",
      "symptom": "redness",
      "risk_factor": False,    },
    {
      "hi": "क्या सूजन के कारण आपको किसी विशेष हिस्से में दर्द हो रहा है?",
      "en": "Is the swelling causing any pain in a specific area?",
      "category": "localized_pain_with_skin_swelling",
      "symptom": "pain",
      "risk_factor": False,    },
    {
      "hi": "क्या सूजन लगातार है या आता-जाता है?",
      "en": "Is the swelling constant or does it come and go?",
      "category": "intermittent_skin_swelling",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या सूजन किसी विशेष समय पर अधिक होती है?",
      "en": "Does the swelling occur more frequently at any specific time?",
      "category": "time_related_skin_swelling",
      "symptom": None,
      "risk_factor": False,    },
    {
      "hi": "क्या सूजन के कारण आपकी त्वचा में कोई परिवर्तन हो रहा है?",
      "en": "Are there any changes in your skin due to swelling?",
      "category": "skin_changes_with_skin_swelling",
      "symptom": "skin discoloration",
      "risk_factor": False,    },
  ],

  "acne": [
    {
      "hi": "आपको कितने समय से एक्ने है?",
      "en": "How long have you had acne?",
      "category": "acne",
      "symptom": "acne duration",
      "risk_factor": False,    },
    {
      "hi": "आपके पास आमतौर पर एक्ने कहाँ होते हैं?",
      "en": "Where do you typically get acne?",
      "category": "acne",
      "symptom": "acne location",
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
      "hi": "क्या आपने अपने एक्ने के लिए कोई उपचार किया है?",
      "en": "Have you tried any treatments for your acne?",
      "category": "acne treatments",
      "symptom": "acne treatment",
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
      "hi": "आप किस प्रकार की याददाश्त की समस्याओं का सामना कर रहे हैं?",
      "en": "What type of memory problems are you experiencing?",
      "category": "memory loss",
      "symptom": "memory problem type",
      "risk_factor": False,    },
    {
      "hi": "क्या याददाश्त की कमी समय के साथ बढ़ रही है?",
      "en": "Is the memory loss getting worse over time?",
      "category": "memory loss",
      "symptom": "memory loss progression",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको हाल ही में कोई सिर की चोट या आघात हुआ है?",
      "en": "Have you had any recent head injuries or trauma?",
      "category": "head injury",
      "symptom": "head injury",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको विशिष्ट विवरण याद करने में परेशानी हो रही है, या यह सामान्य याददाश्त की कमी है?",
      "en": "Do you have trouble recalling specific details, or is it more about general memory loss?",
      "category": "memory loss",
      "symptom": "specific vs general memory loss",
      "risk_factor": False,    },
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
      "hi": "क्या आप कोई दवाइयाँ या सप्लीमेंट्स ले रहे हैं?",
      "en": "Are you taking any medications or supplements?",
      "category": "medications",
      "symptom": "medication use",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको कोई अन्य चिकित्सा समस्याएँ हैं, जैसे उच्च रक्तचाप, मधुमेह, या थायरॉयड की समस्याएँ?",
      "en": "Do you have any other medical conditions, such as high blood pressure, diabetes, or thyroid problems?",
      "category": "medical conditions",
      "symptom": "medical conditions",
      "risk_factor": False,    },
  ],

  "urinary frequency": [
    {
      "hi": "आपको कितनी बार पेशाब करने की आवश्यकता महसूस होती है?",
      "en": "How often do you feel the need to urinate?",
      "category": "urinary frequency",
      "symptom": "urination frequency",
      "risk_factor": False,    },
    {
      "hi": "क्या आप रात में पेशाब करने के लिए उठते हैं (नोक्टुरिया)?",
      "en": "Do you wake up during the night to urinate (nocturia)?",
      "category": "urinary frequency",
      "symptom": "nocturia",
      "risk_factor": False,    },
    {
      "hi": "क्या आप हर बार कितनी मात्रा में पेशाब करते हैं?",
      "en": "How much urine do you pass each time?",
      "category": "urinary frequency",
      "symptom": "urine amount",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको पेशाब करते समय कोई दर्द या असुविधा महसूस हो रही है?",
      "en": "Are you experiencing any pain or discomfort while urinating?",
      "category": "urinary frequency",
      "symptom": "pain during urination",
      "risk_factor": False,    },
    {
      "hi": "क्या आपने अपने मूत्र के रंग या गंध में कोई बदलाव देखा है?",
      "en": "Have you noticed any changes in the color or odor of your urine?",
      "category": "urinary frequency",
      "symptom": "urine color/odor changes",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको पेशाब करने की तीव्र आवश्यकता महसूस होती है लेकिन इसे रोकने में कठिनाई होती है?",
      "en": "Do you have a strong urge to urinate but find it difficult to hold it in?",
      "category": "urinary frequency",
      "symptom": "urgency/difficulty holding urine",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको हाल ही में कोई मूत्राशय संक्रमण (UTI) या अन्य मूत्र संबंधी समस्याएँ हुई हैं?",
      "en": "Have you recently had any urinary tract infections (UTIs) or other urinary problems?",
      "category": "urinary frequency",
      "symptom": "UTI or urinary issues",
      "risk_factor": False,    },
    {
      "hi": "क्या आप बहुत अधिक तरल पदार्थ पीते हैं, खासकर कैफीन, शराब या शर्करा वाले पेय?",
      "en": "Do you drink a lot of fluids, especially caffeine, alcohol, or sugary drinks?",
      "category": "urinary frequency",
      "symptom": "fluid intake habits",
      "risk_factor": False,    },
  ],

  "ear pain": [
    {
      "hi": "आपको कितने समय से कान में दर्द हो रहा है?",
      "en": "How long have you been experiencing ear pain?",
      "category": "ear pain",
      "symptom": "ear pain duration",
      "risk_factor": False,    },
    {
      "hi": "क्या कान में दर्द लगातार बना रहता है, या आता-जाता रहता है?",
      "en": "Is the ear pain constant, or does it come and go?",
      "category": "ear pain",
      "symptom": "pain pattern",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको एक कान में दर्द हो रहा है या दोनों कानों में?",
      "en": "Do you have pain in one ear or both ears?",
      "category": "ear pain",
      "symptom": "ear affected",
      "risk_factor": False,    },
    {
      "hi": "क्या कान में दर्द सर्दी, साइनस संक्रमण, या ऊपरी श्वसन संक्रमण के बाद शुरू हुआ?",
      "en": "Did the ear pain start after a cold, sinus infection, or upper respiratory infection?",
      "category": "ear pain",
      "symptom": "infection history",
      "risk_factor": True,    },
    {
      "hi": "क्या आपको हाल ही में कान में कोई चोट या आघात हुआ है?",
      "en": "Have you had any recent injuries or trauma to the ear?",
      "category": "ear pain",
      "symptom": "ear injury",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके कान से कोई रिसाव या डिस्चार्ज हो रहा है?",
      "en": "Do you have drainage or discharge coming from your ear?",
      "category": "ear pain",
      "symptom": "ear discharge",
      "risk_factor": False,    },
    {
      "hi": "क्या आप हाल ही में जोरदार शोर या पानी (जैसे तैराकी या स्नान) के संपर्क में आए हैं?",
      "en": "Have you recently been exposed to loud noises or water (e.g., swimming or bathing)?",
      "category": "ear pain",
      "symptom": "noise or water exposure",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको बाहरी कान या कान के आस-पास के क्षेत्र को छूने या खींचने पर दर्द हो रहा है?",
      "en": "Are you experiencing any pain when touching or pulling on the outer ear or around the ear area?",
      "category": "ear pain",
      "symptom": "touch pain",
      "risk_factor": False,    },
  ],

  "hypertension": [
    {
      "hi": "क्या आपके परिवार में उच्च रक्तचाप या हृदय रोग का इतिहास है?",
      "en": "Do you have a family history of high blood pressure or heart disease?",
      "category": "hypertension",
      "symptom": "family history",
      "risk_factor": True,    },
    {
      "hi": "क्या आपको किसी अन्य चिकित्सा समस्याओं का निदान हुआ है (जैसे, मधुमेह, गुर्दे की बीमारी)?",
      "en": "Have you been diagnosed with any other medical conditions (e.g., diabetes, kidney disease)?",
      "category": "hypertension",
      "symptom": "other medical conditions",
      "risk_factor": False,    },
    {
      "hi": "क्या आप वर्तमान में कोई दवाइयाँ, ओवर-द-काउंटर दवाइयाँ या सप्लीमेंट्स ले रहे हैं?",
      "en": "Are you currently taking any medications, including over-the-counter drugs or supplements?",
      "category": "hypertension",
      "symptom": "medication use",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको धूम्रपान करने का इतिहास है या अत्यधिक शराब का सेवन करते हैं?",
      "en": "Do you have a history of smoking or excessive alcohol consumption?",
      "category": "hypertension",
      "symptom": "smoking or alcohol use",
      "risk_factor": False,    },
    {
      "hi": "आप अपनी आहार को कैसे वर्णित करेंगे (जैसे, नमक, प्रसंस्कृत खाद्य पदार्थों में अधिक)?",
      "en": "How would you describe your diet (e.g., high in salt, processed foods)?",
      "category": "hypertension",
      "symptom": "diet habits",
      "risk_factor": False,    },
    {
      "hi": "क्या आप नियमित रूप से शारीरिक गतिविधि या व्यायाम करते हैं?",
      "en": "Do you engage in regular physical activity or exercise?",
      "category": "hypertension",
      "symptom": "physical activity",
      "risk_factor": False,    },
    {
      "hi": "आप अपने दैनिक जीवन में कितना तनाव महसूस कर रहे हैं?",
      "en": "How much stress are you experiencing in your daily life?",
      "category": "hypertension",
      "symptom": "stress levels",
      "risk_factor": False,    },
    {
      "hi": "क्या आप नियमित रूप से अपने रक्तचाप की निगरानी करते हैं? यदि हाँ, तो आपके सामान्य रक्तचाप के पठन क्या हैं?",
      "en": "Do you monitor your blood pressure regularly? If so, what are your typical readings?",
      "category": "hypertension",
      "symptom": "blood pressure monitoring",
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

  "delusion": [
    {
      "hi": "आप किस प्रकार की भ्रांतियाँ अनुभव कर रहे हैं (जैसे, संदेहवादी, महानता, विचित्र)?",
      "en": "What kind of delusions are you experiencing (e.g., paranoid, grandiose, bizarre)?",
      "category": "delusions",
      "symptom": "type of delusions",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको लगता है कि दूसरे लोग आपको नुकसान पहुँचाने की कोशिश कर रहे हैं, या कि आपके पास विशेष शक्तियाँ या क्षमताएँ हैं?",
      "en": "Do you believe that others are out to harm you, or that you have special powers or abilities?",
      "category": "delusions",
      "symptom": "paranoia or grandiosity",
      "risk_factor": False,    },
    {
      "hi": "क्या भ्रांतियाँ आपके दैनिक जीवन या रिश्तों को प्रभावित कर रही हैं?",
      "en": "Are the delusions affecting your daily life or relationships?",
      "category": "delusions",
      "symptom": "impact on daily life or relationships",
      "risk_factor": False,    },
    {
      "hi": "क्या आप मानते हैं कि आपके विश्वास वास्तविक नहीं हो सकते, या क्या आप वास्तव में उन्हें सत्य मानते हैं?",
      "en": "Do you recognize that your beliefs may not be real, or do you truly believe them to be true?",
      "category": "delusions",
      "symptom": "recognition of false beliefs",
      "risk_factor": False,    },
    {
      "hi": "क्या आपने हाल ही में कोई महत्वपूर्ण तनाव, जीवन परिवर्तन, या आघातपूर्ण घटनाएँ अनुभव की हैं?",
      "en": "Have you experienced any major stressors, life changes, or traumatic events recently?",
      "category": "delusions",
      "symptom": "recent stressors or trauma",
      "risk_factor": False,    },
    {
      "hi": "क्या आप कोई दवाइयाँ, ओवर-द-काउंटर दवाइयाँ, या अवैध नशीली दवाएँ ले रहे हैं?",
      "en": "Are you currently taking any medications, including prescription, over-the-counter, or recreational drugs?",
      "category": "delusions",
      "symptom": "medications or drugs",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके पास मानसिक स्वास्थ्य स्थितियों का कोई इतिहास है, जैसे स्किजोफ्रेनिया, बाइपोलर डिसऑर्डर, या अवसाद?",
      "en": "Do you have a history of mental health conditions, such as schizophrenia, bipolar disorder, or depression?",
      "category": "delusions",
      "symptom": "mental health history",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको हाल ही में सिर की चोट, संक्रमण, या तंत्रिका तंत्र से संबंधित कोई समस्या हुई है, जो आपके सोचने की क्षमता को प्रभावित कर सकती है?",
      "en": "Have you had any recent head injuries, infections, or neurological conditions that might affect your thinking?",
      "category": "delusions",
      "symptom": "head injuries or neurological conditions",
      "risk_factor": True,    },
    {
      "hi": "क्या आपके परिवार में मानसिक स्वास्थ्य विकारों का कोई इतिहास है, जैसे मानसिक विकृति, स्किजोफ्रेनिया, या बाइपोलर डिसऑर्डर?",
      "en": "Do you have a family history of mental health disorders, such as psychosis, schizophrenia, or bipolar disorder?",
      "category": "delusions",
      "symptom": "family history of mental health disorders",
      "risk_factor": True,    },
  ],

  "paranoia": [
    {
      "hi": "आपके पास लोगों के बारे में क्या विशिष्ट डर या चिंता हैं (जैसे, यह मानना कि लोग आपके खिलाफ साजिश कर रहे हैं या आपकी जासूसी कर रहे हैं)?",
      "en": "What specific fears or concerns do you have about people (e.g., believing others are plotting against you or spying on you)?",
      "category": "paranoia",
      "symptom": "specific fears or concerns",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको लगता है कि लोग जानबूझकर आपको नुकसान पहुँचाने या धोखा देने की कोशिश कर रहे हैं?",
      "en": "Do you feel that people are intentionally trying to harm or deceive you?",
      "category": "paranoia",
      "symptom": "belief of harm or deception",
      "risk_factor": False,    },
    {
      "hi": "क्या यह विचार स्थिर हैं, या क्या वे आते-जाते रहते हैं?",
      "en": "Are these thoughts persistent, or do they come and go?",
      "category": "paranoia",
      "symptom": "persistence of thoughts",
      "risk_factor": False,    },
    {
      "hi": "क्या आपने अपने संदेहपूर्ण विचारों के लिए कोई उत्तेजक देखा है (जैसे, कुछ लोग, परिस्थितियाँ, या स्थान)?",
      "en": "Have you noticed any triggers for your paranoid thoughts (e.g., certain people, situations, or places)?",
      "category": "paranoia",
      "symptom": "triggers for paranoid thoughts",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको दोस्तों, परिवार, या सहकर्मियों पर विश्वास करने में कठिनाई होती है?",
      "en": "Do you have difficulty trusting friends, family, or coworkers?",
      "category": "paranoia",
      "symptom": "difficulty trusting others",
      "risk_factor": False,    },
    {
      "hi": "क्या आप कोई दवाइयाँ, ओवर-द-काउंटर दवाइयाँ, या अवैध नशीली दवाएँ ले रहे हैं?",
      "en": "Are you taking any medications, including prescription, over-the-counter, or recreational drugs?",
      "category": "paranoia",
      "symptom": "medications or drugs",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके परिवार में मानसिक स्वास्थ्य विकारों का कोई इतिहास है, जैसे स्किजोफ्रेनिया, बाइपोलर डिसऑर्डर, या चिंता विकार?",
      "en": "Do you have a family history of mental health conditions, such as schizophrenia, bipolar disorder, or anxiety disorders?",
      "category": "paranoia",
      "symptom": "family history of mental health conditions",
      "risk_factor": True,    },
  ],

  "euphoria": [
    {
      "hi": "इन उत्साही भावनाओं की तीव्रता कितनी है?",
      "en": "How intense are these feelings of euphoria?",
      "category": "euphoria",
      "symptom": "intensity of euphoria",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको लगता है कि यह उत्साह आपके चारों ओर की स्थिति या घटनाओं के मुकाबले अत्यधिक है?",
      "en": "Do you feel that the euphoria is out of proportion to the situation or events around you?",
      "category": "euphoria",
      "symptom": "disproportionate euphoria",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको असामान्य रूप से आत्मविश्वासी, ऊर्जावान, या 'दुनिया के शीर्ष पर' जैसा महसूस हो रहा है?",
      "en": "Do you feel unusually confident, energetic, or 'on top of the world'?",
      "category": "euphoria",
      "symptom": "feeling of being 'on top of the world'",
      "risk_factor": False,    },
    {
      "hi": "क्या आपने अपने उत्साह के लिए कोई पैटर्न या उत्तेजक देखा है (जैसे, कुछ स्थितियाँ, समय का हिस्सा, या गतिविधियाँ)?",
      "en": "Have you noticed any patterns or triggers for your euphoria (e.g., certain situations, times of day, or activities)?",
      "category": "euphoria",
      "symptom": "triggers for euphoria",
      "risk_factor": False,    },
    {
      "hi": "क्या आप कोई दवाइयाँ, ओवर-द-काउंटर दवाइयाँ, या अवैध नशीली दवाएँ ले रहे हैं (जैसे, उत्तेजक या शराब)?",
      "en": "Are you taking any medications, including prescription, over-the-counter, or recreational drugs (e.g., stimulants or alcohol)?",
      "category": "euphoria",
      "symptom": "medications or drugs",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके मानसिक स्वास्थ्य में कोई महत्वपूर्ण परिवर्तन हुए हैं, जैसे अवसाद, चिंता, या चिड़चिड़ापन?",
      "en": "Have you had any significant changes in your mental health, such as periods of depression, anxiety, or irritability?",
      "category": "euphoria",
      "symptom": "changes in mental health (e.g., depression, anxiety)",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके पास मानसिक स्वास्थ्य विकारों का इतिहास है, जैसे बाइपोलर डिसऑर्डर, उन्माद, या नशीली दवाओं का दुरुपयोग?",
      "en": "Do you have a history of mental health conditions, such as bipolar disorder, mania, or substance abuse?",
      "category": "euphoria",
      "symptom": "history of mental health conditions",
      "risk_factor": True,    },
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
      "hi": "क्या आपको चोट लगते समय कोई पॉपिंग या क्रैकिंग की आवाज़ सुनाई दी थी?",
      "en": "Did you hear a popping or cracking sound when the injury occurred?",
      "category": "bone_fracture",
      "symptom": "sound during injury",
      "risk_factor": False,    },
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
      "hi": "क्या आप कोई दवाइयाँ ले रहे हैं, जिसमें कैल्शियम या विटामिन D जैसे सप्लीमेंट शामिल हैं?",
      "en": "Are you currently taking any medications, including supplements like calcium or vitamin D?",
      "category": "bone_fracture",
      "symptom": "current medications or supplements",
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
      "symptom": "swelling, bruising, or redness",
      "risk_factor": False,    },
    {
      "hi": "क्या आपने प्रभावित अंग या जोड़ों में कमजोरी, सुन्नता, या आंदोलन में कठिनाई महसूस की है?",
      "en": "Have you noticed any weakness, numbness, or difficulty moving the affected limb or joint?",
      "category": "bone_pain",
      "symptom": "weakness or difficulty moving",
      "risk_factor": False,    },
    {
      "hi": "क्या आप कोई दवाइयाँ या सप्लीमेंट्स ले रहे हैं, जैसे कि कैल्शियम या विटामिन D?",
      "en": "Are you taking any medications or supplements, including calcium or vitamin D?",
      "category": "bone_pain",
      "symptom": "medications or supplements",
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
      "hi": "क्या चोट लगने के समय कोई पॉपिंग या स्नैपिंग की आवाज आई थी?",
      "en": "Did you hear any popping or snapping sounds when the injury occurred?",
      "category": "sprain",
      "symptom": "popping or snapping sounds",
      "risk_factor": False,    },
    {
      "hi": "क्या आपने उसी जोड़े में पहले कभी कोई स्ट्रेन या चोट लगाई है?",
      "en": "Have you had any previous sprains or injuries to the same joint?",
      "category": "sprain",
      "symptom": "previous injuries",
      "risk_factor": False,    },
    {
      "hi": "क्या आप वर्तमान में कोई दवाइयाँ ले रहे हैं, या आपने चोट पर बर्फ, गर्मी, या अन्य उपचार का उपयोग किया है?",
      "en": "Are you currently taking any medications, or have you used ice, heat, or other treatments on the injury?",
      "category": "sprain",
      "symptom": "treatment used",
      "risk_factor": False,    },
  ],

  "injury": [
    {
      "hi": "लिगामेंट की चोट कैसे हुई (जैसे, खेल, दुर्घटना, गिरना, मुड़ने की गति)?",
      "en": "How did the injury occur (through sports, accident, fall, twisting movement)?",
      "category": "ligament injury",
      "symptom": "mechanism of injury",
      "risk_factor": False,    },
    {
      "hi": "कौन सा जोड़ा या क्षेत्र घायल हुआ है (जैसे, घुटना, टखना, कोहनी)?",
      "en": "Which joint or area is injured (e.g., knee, ankle, elbow)?",
      "category": "ligament injury",
      "symptom": "injured joint or area",
      "risk_factor": False,    },
    {
      "hi": "क्या चोट के समय कोई पॉपिंग या स्नैपिंग की आवाज आई थी?",
      "en": "Did you hear a popping or snapping sound when the injury occurred?",
      "category": "ligament injury",
      "symptom": "popping or snapping sounds",
      "risk_factor": False,    },
    {
      "hi": "क्या चोट के बाद दर्द लगातार बना रहता है, या हिलने-डुलने या विशिष्ट गतिविधियों से यह बढ़ जाता है?",
      "en": "Is the pain after injury constant, or does it worsen with movement or specific activities?",
      "category": "ligament injury",
      "symptom": "pain variation with movement",
      "risk_factor": False,    },
    {
      "hi": "क्या आप प्रभावित जोड़े को हिला सकते हैं, या यह हिलाने में बहुत दर्दनाक या अस्थिर है?",
      "en": "Can you move the affected joint, or is it too painful or unstable to do so?",
      "category": "ligament injury",
      "symptom": "joint movement",
      "risk_factor": False,    },
    {
      "hi": "क्या आपने पहले कभी लिगामेंट की चोट या उसी जोड़े में बार-बार समस्याएँ महसूस की हैं?",
      "en": "Have you had any previous injuries or recurring problems in the same area?",
      "category": "ligament injury",
      "symptom": "previous injuries",
      "risk_factor": False,    },
    {
      "hi": "क्या आप वर्तमान में कोई दवाइयाँ ले रहे हैं, या आपने बर्फ, संपीड़न, या ऊँचाई जैसे उपचार का उपयोग किया है?",
      "en": "Are you currently taking any medications, or have you used any treatments like ice, compression, or elevation?",
      "category": "ligament injury",
      "symptom": "treatment used",
      "risk_factor": False,    },
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

  "herniated disc": [
    {
      "hi": "दर्द कहाँ स्थित है (जैसे निचला पीठ, गर्दन, हाथ, पैर)?",
      "en": "Where is the pain located (e.g., lower back, neck, arms, legs)?",
      "category": "herniated_disc",
      "symptom": "location of pain",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको अपने हाथों या पैरों में दर्द महसूस होता है (जैसे साइटिका प्रकार का दर्द)?",
      "en": "Do you have pain radiating down your arms or legs (e.g., sciatica-type pain)?",
      "category": "herniated_disc",
      "symptom": "radiating pain",
      "risk_factor": False,    },
    {
      "hi": "क्या दर्द लगातार है, या यह आता-जाता रहता है?",
      "en": "Is the pain constant, or does it come and go?",
      "category": "herniated_disc",
      "symptom": "pain pattern",
      "risk_factor": False,    },
    {
      "hi": "क्या दर्द तेज, जलन वाला, या हलका चुभता हुआ है? क्या यह कुछ विशेष गति या स्थिति में बढ़ता है?",
      "en": "Is the pain sharp, burning, or dull? Does it worsen with certain movements or positions?",
      "category": "herniated_disc",
      "symptom": "pain type and triggers",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको हाल ही में कोई चोट, भारी वजन उठाना, या ऐसी गतिविधियाँ हुई हैं जिन्होंने आपकी पीठ या गर्दन को दबाव डाला हो?",
      "en": "Have you had any recent injuries, heavy lifting, or activities that might have strained your back or neck?",
      "category": "herniated_disc",
      "symptom": "recent injuries or strain",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको अपने हाथों, पैरों, हाथों या पैरों में सुन्नता, झुनझुनी या कमजोरी महसूस हो रही है?",
      "en": "Are you experiencing numbness, tingling, or weakness in your arms, legs, hands, or feet?",
      "category": "herniated_disc",
      "symptom": "numbness, tingling, or weakness",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको खड़ा होने, चलने, या कुछ स्थितियों (जैसे झुकना, लंबे समय तक बैठना) में कठिनाई हो रही है?",
      "en": "Do you have difficulty standing, walking, or maintaining certain positions (e.g., bending, sitting for long periods)?",
      "category": "herniated_disc",
      "symptom": "mobility difficulties",
      "risk_factor": False,    },
    {
      "hi": "क्या आप वर्तमान में कोई दवाइयाँ ले रहे हैं, और क्या आपने फिजिकल थेरेपी, विश्राम, या दर्द निवारण जैसे उपचार किए हैं?",
      "en": "Are you currently taking any medications, and have you tried treatments like physical therapy, rest, or pain relief?",
      "category": "herniated_disc",
      "symptom": "medications and treatments",
      "risk_factor": False,    },
  ],

  "back spasm": [
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

  "whiplash": [
    {
      "hi": "आपको कहाँ दर्द महसूस हो रहा है (जैसे गर्दन, कंधे, ऊपरी पीठ)?",
      "en": "Where exactly do you feel pain (e.g., neck, shoulders, upper back)?",
      "category": "whiplash",
      "symptom": "location of pain",
      "risk_factor": False,    },
    {
      "hi": "क्या दर्द लगातार है, या यह आता-जाता रहता है?",
      "en": "Is the pain constant, or does it come and go?",
      "category": "whiplash",
      "symptom": "pain pattern",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको गर्दन या सिर में कठोरता या सीमित गति महसूस हो रही है?",
      "en": "Do you experience stiffness or limited movement in your neck or head?",
      "category": "whiplash",
      "symptom": "stiffness or movement limitation",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको चोट के बाद सिरदर्द, चक्कर, या कानों में घंटी बजने (टिनिटस) का अनुभव हो रहा है?",
      "en": "Have you noticed any headaches, dizziness, or ringing in your ears (tinnitus) since the injury?",
      "category": "whiplash",
      "symptom": "headaches, dizziness, or tinnitus",
      "risk_factor": False,    },
    {
      "hi": "क्या आपने अन्य कोई चोटें खाई हैं, जैसे मस्तिष्क concussion या पीठ की चोटें, साथ में whiplash के?",
      "en": "Have you had any other injuries, such as a concussion or back injuries, along with the whiplash?",
      "category": "whiplash",
      "symptom": "other injuries",
      "risk_factor": False,    },
    {
      "hi": "क्या आपने किसी उपचार का प्रयास किया है (जैसे आराम, बर्फ, हीट, दर्द निवारक), और क्या उससे राहत मिली?",
      "en": "Have you tried any treatments (e.g., rest, ice, heat, pain relievers) to relieve the symptoms, and did they help?",
      "category": "whiplash",
      "symptom": "treatment attempts",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको गर्दन या पीठ से संबंधित कोई इतिहास है, जैसे पिछले whiplash, हर्नियेटेड डिस्क, या गठिया?",
      "en": "Do you have a history of neck or back problems, such as previous whiplash, herniated discs, or arthritis?",
      "category": "whiplash",
      "symptom": "history of neck or back issues",
      "risk_factor": True,    },
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

  "dermatitis": [
    {
      "hi": "आपके शरीर के किस हिस्से में सबसे ज्यादा लक्षण दिखाई दे रहे हैं (जैसे सिर की त्वचा, चेहरा, भौहें, छाती, या पीठ)?",
      "en": "Where on your body do you have the most noticeable symptoms (e.g., scalp, face, eyebrows, chest, or back)?",
      "category": "seborrheic_dermatitis",
      "symptom": "location of symptoms",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको रूसी या खुजलीदार, उबड़-खाबड़ सिर की त्वचा का अनुभव होता है?",
      "en": "Do you experience dandruff or an itchy, flaky scalp?",
      "category": "seborrheic_dermatitis",
      "symptom": "scalp irritation",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको एलर्जी या त्वचा की समस्याओं, जैसे एक्जिमा या सोरायसिस, का इतिहास है?",
      "en": "Do you have a history of allergies or skin conditions, such as eczema or psoriasis?",
      "category": "contact_dermatitis",
      "symptom": "medical history of skin conditions",
      "risk_factor": False,    },
    {
      "hi": "क्या त्वचा की जलन स्थिर रहती है, या यह बीच-बीच में बढ़ जाती है?",
      "en": "Is the skin irritation persistent, or does it flare up intermittently?",
      "category": "seborrheic_dermatitis",
      "symptom": "irritation pattern",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको कोई अन्य स्थितियाँ हैं, जैसे तैलीय त्वचा, फंगल संक्रमण, या अन्य पुरानी त्वचा स्थितियाँ (जैसे सोरायसिस, एक्जिमा)?",
      "en": "Do you have any underlying conditions like oily skin, fungal infections, or other chronic skin conditions (e.g., psoriasis, eczema)?",
      "category": "seborrheic_dermatitis",
      "symptom": "underlying conditions",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको सेबोरेइक डर्मेटाइटिस से जुड़ी कोई अन्य स्थिति, जैसे पार्किंसंस रोग या एचआईवी, का इतिहास है?",
      "en": "Do you have a history of other conditions, such as Parkinson’s disease or HIV, which are associated with seborrheic dermatitis?",
      "category": "seborrheic_dermatitis",
      "symptom": "history of associated conditions",
      "risk_factor": True,    },
    {
      "hi": "क्या आपने सेबोरेइक डर्मेटाइटिस के लिए कोई उपचार किया है, जैसे मेडिकेटेड शैंपू, टॉपिकल क्रीम, या कोर्टिकोस्टेरॉइड्स?",
      "en": "Have you tried any treatments for seborrheic dermatitis, such as medicated shampoos, topical creams, or corticosteroids?",
      "category": "seborrheic_dermatitis",
      "symptom": "treatments tried",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके परिवार में सेबोरेइक डर्मेटाइटिस या अन्य त्वचा विकारों का इतिहास है?",
      "en": "Do you have a family history of seborrheic dermatitis or other skin disorders?",
      "category": "seborrheic_dermatitis",
      "symptom": "family history of seborrheic dermatitis",
      "risk_factor": True,    },
  ],

  "cellulitis": [

    {
      "hi": "सेल्यूलाइटिस सबसे पहले आपके शरीर के किस हिस्से में दिखा (जैसे पैरों, हाथों, चेहरे)?",
      "en": "Where on your body did the cellulitis first appear (e.g., legs, arms, face)?",
      "category": "cellulitis",
      "symptom": "location of cellulitis",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको हाल ही में कट, कीड़े के काटने, या त्वचा में कोई अन्य दरारें हुई हैं जहाँ संक्रमण घुस सकता था?",
      "en": "Have you had any recent cuts, insect bites, or other breaks in the skin where the infection could have entered?",
      "category": "cellulitis",
      "symptom": "skin injury or break",
      "risk_factor": False,    },
    {
      "hi": "क्या संक्रमण का क्षेत्र समय के साथ अधिक सूजा, लाल हुआ, या दर्दनाक हो गया है?",
      "en": "Is the area of infection becoming more swollen, red, or painful over time?",
      "category": "cellulitis",
      "symptom": "infection progression",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको कोई अन्य स्वास्थ्य समस्याएँ हैं, जैसे डायबिटीज, कमजोर इम्यून सिस्टम, या परिसंचरण संबंधी समस्याएँ, जो संक्रमण के जोखिम को बढ़ा सकती हैं?",
      "en": "Do you have any underlying health conditions, such as diabetes, weakened immune system, or circulatory problems, that could increase your risk of infection?",
      "category": "cellulitis",
      "symptom": "underlying health conditions",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको पहले कभी सेल्यूलाइटिस या बार-बार होने वाले त्वचा संक्रमण का सामना हुआ है?",
      "en": "Have you had a history of cellulitis or recurrent skin infections in the past?",
      "category": "cellulitis",
      "symptom": "history of cellulitis",
      "risk_factor": True,    },
    {
      "hi": "क्या आप किसी दवा का सेवन कर रहे हैं, विशेष रूप से स्टेरॉयड या इम्यूनोसप्रेसिव दवाएँ?",
      "en": "Are you currently taking any medications, particularly steroids or immunosuppressive drugs?",
      "category": "cellulitis",
      "symptom": "current medications",
      "risk_factor": False,    },
    {
      "hi": "क्या आसपास के लिम्फ नोड्स में सूजन है, या संक्रमित क्षेत्र के आस-पास की गति सीमा में कोई बदलाव हुआ है?",
      "en": "Do you have any swelling in nearby lymph nodes, or have you noticed any changes in your range of motion around the infected area?",
      "category": "cellulitis",
      "symptom": "swelling or motion limitation",
      "risk_factor": False,    },
    {
      "hi": "क्या आपने किसी ऐसे व्यक्ति से संपर्क किया है जो त्वचा संक्रमण से पीड़ित हो, या क्या आपने किसी ऐसी स्थिति (जैसे असंक्रमित पानी में तैरना) का अनुभव किया है जिससे बैक्टीरिया के संपर्क का जोखिम बढ़ सकता हो?",
      "en": "Have you been in contact with anyone who has a skin infection, or have you been in situations (e.g., swimming in untreated water) that might increase exposure to bacteria?",
      "category": "cellulitis",
      "symptom": "exposure to infection",
      "risk_factor": False,    },
  ],

  "ulcer": [
    {
      "hi": "आपके शरीर पर अल्सर कहां स्थित हैं (जैसे पेट, मुँह, पैर, या पैर के तलवे)?",
      "en": "Where on your body are the ulcers located (e.g., stomach, mouth, legs, or feet)?",
      "category": "ulcer",
      "symptom": "location of ulcer",
      "risk_factor": False,    },
    {
      "hi": "क्या अल्सर से आपको दर्द होता है, और यदि हां, तो दर्द की तीव्रता कितनी है?",
      "en": "Do the ulcers cause you pain, and if so, how severe is the pain?",
      "category": "ulcer",
      "symptom": "pain severity",
      "risk_factor": False,    },
    {
      "hi": "क्या अल्सर खुले हुए हैं और बहाव कर रहे हैं, या क्या उन पर कोई क्रस्ट या स्कैब है?",
      "en": "Are the ulcers open and draining, or do they have a scab or crust over them?",
      "category": "ulcer",
      "symptom": "ulcer appearance",
      "risk_factor": False,    },
    {
      "hi": "क्या आपने अल्सर से रक्तस्राव देखा है, या क्या आपको कोई असामान्य स्राव हुआ है?",
      "en": "Have you noticed any bleeding from the ulcer, or have you had any unusual discharge?",
      "category": "ulcer",
      "symptom": "bleeding or discharge",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको गैस्ट्राइटिस, एसिड रिफ्लक्स, क्रोहन रोग, या वैरिकोज वेन जैसी बीमारियों का इतिहास है?",
      "en": "Do you have a history of conditions like gastritis, acid reflux, Crohn's disease, or varicose veins?",
      "category": "ulcer",
      "symptom": "underlying conditions",
      "risk_factor": True,    },
    {
      "hi": "क्या आपने हाल ही में कोई चोट, संक्रमण, या दवाइयां (जैसे NSAIDs या स्टेरॉयड) ली हैं, जो अल्सर को बढ़ा सकती हैं?",
      "en": "Have you recently had any injuries, infections, or medications (such as NSAIDs or steroids) that could trigger the ulcer?",
      "category": "ulcer",
      "symptom": "triggers",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको धूम्रपान, अत्यधिक शराब सेवन, या ऐसी आहार आदतें हैं जो अल्सर बनने में योगदान कर सकती हैं?",
      "en": "Do you have a history of smoking, excessive alcohol use, or a diet that could contribute to ulcer formation?",
      "category": "ulcer",
      "symptom": "lifestyle factors",
      "risk_factor": True,    },
    {
      "hi": "क्या आप वर्तमान में अल्सर, उच्च रक्तचाप, मधुमेह, या ऑटोइम्यून रोगों के लिए कोई दवाइयां ले रहे हैं?",
      "en": "Are you currently taking any medications for conditions like ulcers, high blood pressure, diabetes, or autoimmune disorders?",
      "category": "ulcer",
      "symptom": "medication history",
      "risk_factor": False,    },
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

  "nail splitting": [
    {
      "hi": "कौन से नाखून प्रभावित हैं (जैसे उंगलियां, पैर, या कोई विशेष नाखून)?",
      "en": "Which nails are affected (e.g., fingers, toes, specific nails)?",
      "category": "nail_splitting",
      "symptom": "affected nails",
      "risk_factor": False,    },
    {
      "hi": "क्या नाखूनों में फटने से दर्द होता है या कोई असुविधा महसूस होती है?",
      "en": "Is the splitting painful, or does it cause any discomfort?",
      "category": "nail_splitting",
      "symptom": "pain or discomfort",
      "risk_factor": False,    },
    {
      "hi": "क्या आपने नाखूनों के रंग, बनावट, या मोटाई में कोई बदलाव महसूस किया है, जैसे कि रंग का बदलना या नाखूनों का कमजोर होना?",
      "en": "Have you noticed any changes in the color, texture, or thickness of your nails, such as discoloration or brittleness?",
      "category": "nail_condition",
      "symptom": "nail discoloration or brittleness",
      "risk_factor": False,    },
    {
      "hi": "क्या आपको नाखूनों को किसी प्रकार का आघात, अधिक हाथ धोने या कठोर रसायनों के संपर्क में आने का इतिहास है (जैसे सफाई उत्पाद, नेल पॉलिश रिमूवर)?",
      "en": "Do you have a history of nail trauma, frequent hand washing, or exposure to harsh chemicals (e.g., cleaning products, nail polish removers)?",
      "category": "external_factors",
      "symptom": "trauma or chemical exposure",
      "risk_factor": False,    },
    {
      "hi": "क्या आप कोई ऐसी दवाइयाँ या सप्लीमेंट ले रहे हैं, जो आपके नाखूनों को प्रभावित कर सकते हैं (जैसे कि कीमोथेरेपी, बायोटिन, या अन्य विटामिन की कमी)?",
      "en": "Are you taking any medications or supplements that might be affecting your nails (e.g., chemotherapy, biotin, or other vitamin deficiencies)?",
      "category": "medications",
      "symptom": "medications or supplements",
      "risk_factor": False,    },
    {
      "hi": "क्या आपके परिवार में नाखूनों या त्वचा की बीमारियों का इतिहास है, जैसे एक्जिमा या फंगल संक्रमण?",
      "en": "Do you have a family history of nail or skin conditions, such as eczema or fungal infections?",
      "category": "family_history",
      "symptom": "family history of skin or nail conditions",
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
    "symptom": "swollen lymph nodes",
    "risk_factor": True,
  },
  {
    "hi": "क्या आपको संक्रमण के संभावित स्रोतों का सामना हुआ है? (जैसे बीमार संपर्क, ऐसी जगहों पर यात्रा जहां एंडेमिक बीमारियां हैं)",
    "en": "Have you been exposed to any potential sources of infection (e.g., sick contacts, travel to areas with endemic diseases)?",
    "category": "swollen lymph nodes",
    "symptom": "swollen lymph nodes",
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
    "symptom": "skin burning",
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
      "hi": "खून कहां से बह रहा है?",
      "en": "Where is the bleeding coming from?",
      "category": "bleeding",
      "symptom": "bleeding",
      "risk_factor": False,
    },
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
    {
      "hi": "क्या आप कोई दवाइयां ले रहे हैं, विशेष रूप से रक्त पतला करने वाली दवाइयां?",
      "en": "Are you taking any medications, particularly blood thinners?",
      "category": "bleeding",
      "symptom": "bleeding",
      "risk_factor": False,
    },
],
"anxiety": [
    {
      "hi": "क्या आपकी चिंता के कारण विशेष परिस्थितियाँ, विचार, या घटनाएँ हैं?",
      "en": "What triggers your anxiety (specific situations, thoughts, or events)?",
      "category": "anxiety",
      "symptom": "anxiety",
      "risk_factor": False,
    },
    {
      "hi": "क्या आप अपनी चिंता के कारण कुछ विशेष परिस्थितियों से बचते हैं?",
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
      "symptom": "cancer",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको कोई लगातार दर्द या असुविधा महसूस हो रही है?",
      "en": "Do you have any persistent pain or discomfort?",
      "category": "cancer",
      "symptom": "cancer",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने अपनी त्वचा में कोई बदलाव महसूस किया है, जैसे नए मस्से या वृद्धि?",
      "en": "Have you experienced any changes in your skin, such as new moles or growths?",
      "category": "cancer",
      "symptom": "cancer",
      "risk_factor": False,
    },
    {
      "hi": "क्या आप किसी असामान्य रक्तस्राव या स्राव का अनुभव कर रहे हैं?",
      "en": "Are you experiencing any unusual bleeding or discharge?",
      "category": "cancer",
      "symptom": "cancer",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको निगलने में कोई कठिनाई या लगातार खांसी का अनुभव हुआ है?",
      "en": "Have you had any difficulty swallowing or persistent cough?",
      "category": "cancer",
      "symptom": "cancer",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको आंत्र या मूत्र संबंधी आदतों में कोई बदलाव महसूस हुआ है (जैसे, मल में खून, बार-बार पेशाब आना)?",
      "en": "Do you have any changes in bowel or urinary habits (e.g., blood in stool, frequent urination)?",
      "category": "cancer",
      "symptom": "cancer",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको कोई असामान्य थकान या कमजोरी महसूस हो रही है जो आराम करने से ठीक नहीं होती?",
      "en": "Have you had any unusual fatigue or weakness that does not improve with rest?",
      "category": "cancer",
      "symptom": "cancer",
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
      "symptom": "weight loss",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने हाल ही में कोई बीमारी, संक्रमण या स्वास्थ्य समस्याएँ अनुभव की हैं?",
      "en": "Have you had any recent illnesses, infections, or health conditions?",
      "category": "weight loss",
      "symptom": "weight loss",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको थायरॉयड समस्याएँ, डायबिटीज़, या अन्य चयापचय विकारों का इतिहास है?",
      "en": "Do you have a history of thyroid problems, diabetes, or other metabolic disorders?",
      "category": "weight loss",
      "symptom": "weight loss",
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
      "symptom": "frequent urination",
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
      "symptom": "frequent urination",
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
      "symptom": "frequent urination",
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
      "symptom": "strain",
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
      "symptom": "strain",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने किसी उपचार की कोशिश की है (जैसे, विश्राम, बर्फ, गर्मी, या दवा), और यदि हां, तो क्या उन्होंने मदद की?",
      "en": "Have you tried any treatments (e.g., rest, ice, heat, or medication), and if so, did they help?",
      "category": "strain",
      "symptom": "strain",
      "risk_factor": False,
    }
],
    "jaw pain": [
    {
      "hi": "क्या आप जबड़े के दर्द (तीव्र, सुस्त, धड़कन या दर्द) का वर्णन कर सकते हैं?",
      "en": "Can you describe the jaw pain (sharp, dull, throbbing, or aching)?",
      "category": "jaw pain",
      "symptom": "jaw pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या जबड़े का दर्द लगातार बना रहता है, या यह आता-जाता रहता है?",
      "en": "Is the jaw pain constant, or does it come and go?",
      "category": "jaw pain",
      "symptom": "jaw pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या दर्द चबाने, बोलने, या मुँह खोलने से बढ़ जाता है?",
      "en": "Does the pain worsen with chewing, speaking, or opening your mouth wide?",
      "category": "jaw pain",
      "symptom": "jaw pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको अपने काटने या जबड़े की गति में कोई कठिनाई हो रही है?",
      "en": "Are you having any difficulty with your bite or jaw movement?",
      "category": "jaw pain",
      "symptom": "jaw pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या आप रात में अपने दांतों को पीसते हैं या जबड़े को दबाते हैं?",
      "en": "Do you grind your teeth or clench your jaw, especially at night?",
      "category": "jaw pain",
      "symptom": "jaw pain",
      "risk_factor": False,
    },
],
    "tooth pain": [
    {
      "hi": "क्या आप दांत के दर्द (तीव्र, धड़कते, लगातार या रुक-रुक कर) का वर्णन कर सकते हैं?",
      "en": "Can you describe the tooth pain (sharp, throbbing, constant, or intermittent)?",
      "category": "tooth pain",
      "symptom": "tooth pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या यह दर्द गर्म, ठंडा, या मीठे खाद्य या पेय पदार्थों से उत्तेजित होता है?",
      "en": "Is the pain triggered by hot, cold, or sweet foods or drinks?",
      "category": "tooth pain",
      "symptom": "tooth pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने हाल ही में दंत चिकित्सा कार्य या दांत में किसी प्रकार का आघात अनुभव किया है?",
      "en": "Have you had any recent dental work or trauma to the tooth?",
      "category": "tooth pain",
      "symptom": "tooth pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको चबाने या काटने में कोई कठिनाई हो रही है?",
      "en": "Are you having difficulty chewing or biting down?",
      "category": "tooth pain",
      "symptom": "tooth pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको कीड़े, मसूड़ों की बीमारी, या अन्य दंत समस्याओं का इतिहास है?",
      "en": "Have you had a history of cavities, gum disease, or other dental issues?",
      "category": "tooth pain",
      "symptom": "tooth pain",
      "risk_factor": True,
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
      "symptom": "fainting",
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
      "symptom": "fainting",
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
      "symptom": "fainting",
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
      "symptom": "nervousness",
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
      "symptom": "blurred vision",
      "risk_factor": True,
    },
    {
      "hi": "क्या आप वर्तमान में कोई दवाइयाँ ले रहे हैं या कोई अंतर्निहित स्वास्थ्य समस्याएँ हैं (जैसे, मधुमेह या उच्च रक्तचाप)?",
      "en": "Are you currently taking any medications or have any underlying health conditions (e.g., diabetes or hypertension)?",
      "category": "blurred vision",
      "symptom": "blurred vision",
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
      "symptom": "restlessness",
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
      "symptom": "difficulty swallowing",
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
      "symptom": "dry mouth",
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
      "symptom": "dry mouth",
      "risk_factor": False,
    }
],
"flu": [
    {
      "hi": "क्या आपको बुखार हो रहा है, और अगर हां, तो यह कितने उच्च स्तर का रहा है?",
      "en": "Are you experiencing a fever, and if so, how high has it been?",
      "category": "flu",
      "symptom": "flu",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको खांसी, गले में खराश, या नाक बंद/बहना हो रहा है?",
      "en": "Do you have a cough, sore throat, or runny/stuffy nose?",
      "category": "flu",
      "symptom": "flu",
      "risk_factor": False,
    },
    {
      "hi": "क्या आप थका हुआ या कमजोर महसूस कर रहे हैं?",
      "en": "Are you feeling fatigued or weak?",
      "category": "flu",
      "symptom": "flu",
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
      "symptom": "confusion",
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
      "symptom": "runny nose",
      "risk_factor": True,
    },
    {
      "hi": "क्या आपने हाल ही में यात्रा की है या पर्यावरणीय उत्तेजकों (जैसे धूल, धुंआ, प्रदूषण) से संपर्क किया है?",
      "en": "Have you recently traveled or been in contact with environmental irritants (e.g., dust, smoke, pollution)?",
      "category": "runny nose",
      "symptom": "runny nose",
      "risk_factor": False,
    }
],
  "sneezing": [
    {
      "hi": "क्या आप दिन के कुछ विशेष समय पर या कुछ विशेष वातावरण में ज्यादा छींकते हैं?",
      "en": "Do you sneeze more at certain times of day or in specific environments?",
      "category": "sneezing",
      "symptom": "sneezing",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने किसी एलर्जी उत्पन्न करने वाले तत्वों (जैसे पराग, धूल, या पालतू जानवरों की रूसी) से संपर्क किया है?",
      "en": "Have you been exposed to any allergens, such as pollen, dust, or pet dander?",
      "category": "sneezing",
      "symptom": "sneezing",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने हाल ही में बिमार महसूस किया है या सर्दी या फ्लू के लक्षण थे?",
      "en": "Have you recently been sick or had symptoms of a cold or flu?",
      "category": "sneezing",
      "symptom": "sneezing",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको एलर्जी या अस्थमा का इतिहास है?",
      "en": "Do you have a history of allergies or asthma?",
      "category": "sneezing",
      "symptom": "sneezing",
      "risk_factor": True,
    },
    {
      "hi": "क्या आपने हाल ही में मजबूत गंध, धुंआ, या रासायनिक उत्तेजकों से संपर्क किया है?",
      "en": "Have you recently been in contact with strong odors, smoke, or chemical irritants?",
      "category": "sneezing",
      "symptom": "sneezing",
      "risk_factor": False,
    }
],

  "throat pain": [
    {
      "hi": "क्या आपको निगलने में कठिनाई या निगलते समय दर्द हो रहा है?",
      "en": "Are you experiencing any difficulty swallowing or pain when swallowing?",
      "category": "throat pain",
      "symptom": "throat pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने हाल ही में किसी ऐसे व्यक्ति से संपर्क किया है जिसे गले में दर्द या सर्दी हो?",
      "en": "Have you been exposed to anyone with a sore throat or cold recently?",
      "category": "throat pain",
      "symptom": "throat pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या आप धूम्रपान करते हैं या आपको धुंआ या अन्य उत्तेजकों से संपर्क हुआ है?",
      "en": "Do you smoke or have you been exposed to smoke or other irritants?",
      "category": "throat pain",
      "symptom": "throat pain",
      "risk_factor": False,
    },
],
  "eye pain": [
    {
      "hi": "क्या दर्द एक आंख में है या दोनों आंखों में?",
      "en": "Is the pain in one eye or both eyes?",
      "category": "eye pain",
      "symptom": "eye pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको हाल ही में आंखों में चोट या आघात लगा है?",
      "en": "Have you had any recent eye injuries or trauma?",
      "category": "eye pain",
      "symptom": "eye pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको आंखों से संबंधित कोई समस्या का इतिहास है, जैसे ग्लूकोमा या सूखी आंखें?",
      "en": "Do you have a history of eye conditions, such as glaucoma or dry eyes?",
      "category": "eye pain",
      "symptom": "eye pain",
      "risk_factor": True,
    },
    {
      "hi": "क्या आपको धुंआ, रसायन, या अन्य उत्तेजकों का संपर्क हुआ है?",
      "en": "Have you been exposed to smoke, chemicals, or other irritants?",
      "category": "eye pain",
      "symptom": "eye pain",
      "risk_factor": False,
    },
],
  "hand pain": [
    {
      "hi": "क्या दर्द एक हाथ में है या दोनों हाथों में?",
      "en": "Is the pain in one hand or both hands?",
      "category": "hand pain",
      "symptom": "hand pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या हाथ में दर्द लगातार बना रहता है, या यह आता-जाता रहता है?",
      "en": "Is the hand pain constant, or does it come and go?",
      "category": "hand pain",
      "symptom": "hand pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको हाल ही में हाथों में चोट या आघात लगा है?",
      "en": "Have you had any recent injuries or trauma to your hands?",
      "category": "hand pain",
      "symptom": "hand pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको हाथ में सूजन, लाली, या जकड़न का अनुभव हो रहा है?",
      "en": "Are you experiencing any swelling, redness, or stiffness in the hand?",
      "category": "hand pain",
      "symptom": "hand pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको अपनी उंगलियों या हाथों में सुन्नता या झनझनाहट का अनुभव हो रहा है?",
      "en": "Do you have any numbness or tingling in your fingers or hands?",
      "category": "hand pain",
      "symptom": "hand pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या आप उन गतिविधियों में शामिल हैं जो आपके हाथों पर दबाव डालती हैं, जैसे टाइपिंग या उठाना?",
      "en": "Are you involved in activities that put strain on your hands, like typing or lifting?",
      "category": "hand pain",
      "symptom": "hand pain",
      "risk_factor": False,
    },
],
  "arm pain": [
    {
      "hi": "क्या दर्द एक हाथ में है या दोनों हाथों में?",
      "en": "Is the pain in one arm or both arms?",
      "category": "arm pain",
      "symptom": "arm pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या बांह का दर्द तेज़, सुस्त या धड़कता हुआ है?",
      "en": "Is the arm pain sharp, dull, or throbbing?",
      "category": "arm pain",
      "symptom": "arm pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको हाल ही में हाथ में कोई चोट, गिरने या आघात का सामना करना पड़ा है?",
      "en": "Have you had any recent injuries, falls, or trauma to your arm?",
      "category": "arm pain",
      "symptom": "arm pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको अपने हाथ या कंधे को हिलाने में कठिनाई हो रही है?",
      "en": "Do you have difficulty moving your arm or shoulder?",
      "category": "arm pain",
      "symptom": "arm pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको हाथ या हाथों में सुन्नता, झनझनाहट, या कमजोरी का अनुभव हो रहा है?",
      "en": "Are you experiencing any numbness, tingling, or weakness in the arm or hand?",
      "category": "arm pain",
      "symptom": "arm pain",
      "risk_factor": False,
    },
],
  "foot pain": [
    {
      "hi": "क्या दर्द एक पैर में है या दोनों पैरों में?",
      "en": "Is the pain in one foot or both feet?",
      "category": "foot pain",
      "symptom": "foot pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या पैर में दर्द लगातार बना रहता है, या यह आता-जाता रहता है?",
      "en": "Is the foot pain constant, or does it come and go?",
      "category": "foot pain",
      "symptom": "foot pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको पैरों में सूजन, लाली, या चोट का अनुभव हो रहा है?",
      "en": "Are you experiencing any swelling, redness, or bruising in the foot?",
      "category": "foot pain",
      "symptom": "foot pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको हाल ही में पैर में कोई चोट या आघात हुआ है?",
      "en": "Have you had any recent injuries or trauma to your foot?",
      "category": "foot pain",
      "symptom": "foot pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या दर्द कुछ गतिविधियों के साथ बढ़ जाता है, जैसे लंबी अवधि तक चलना या खड़ा होना?",
      "en": "Does the pain get worse with certain activities, like walking or standing for long periods?",
      "category": "foot pain",
      "symptom": "foot pain",
      "risk_factor": False,
    },
],
  "shoulder pain": [
    {
      "hi": "क्या दर्द एक कंधे में है या दोनों कंधों में?",
      "en": "Is the pain in one shoulder or both shoulders?",
      "category": "shoulder pain",
      "symptom": "shoulder pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या कंधे का दर्द तेज़, सुस्त या दर्दभरा है?",
      "en": "Is the shoulder pain sharp, dull, or achy?",
      "category": "shoulder pain",
      "symptom": "shoulder pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको हाल ही में कंधे में कोई चोट या आघात हुआ है?",
      "en": "Have you had any recent injuries or trauma to your shoulder?",
      "category": "shoulder pain",
      "symptom": "shoulder pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या कंधे का दर्द विशिष्ट गतिविधियों या गतिविधियों, जैसे उठाने या पहुंचने से बढ़ जाता है?",
      "en": "Does the shoulder pain worsen with specific movements or activities, such as lifting or reaching?",
      "category": "shoulder pain",
      "symptom": "shoulder pain",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने कंधे में सूजन, चोट या गति सीमा में प्रतिबंध महसूस किया है?",
      "en": "Have you noticed any swelling, bruising, or restricted range of motion in the shoulder?",
      "category": "shoulder pain",
      "symptom": "shoulder pain",
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
    "symptom": "jaundice",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपने हाल ही में वजन घटने या भूख में कमी महसूस की है?",
    "en": "Have you experienced any recent weight loss or loss of appetite?",
    "category": "jaundice",
    "symptom": "jaundice",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको हेपेटाइटिस या किसी संक्रामक रोग से संक्रमित किसी व्यक्ति के संपर्क में आने का कोई इतिहास है?",
    "en": "Have you been exposed to anyone with hepatitis or any infectious diseases?",
    "category": "jaundice",
    "symptom": "jaundice",
    "risk_factor": False,
  },
  {
    "hi": "क्या आप शराब का सेवन करते हैं या किसी प्रकार की दवाइयां लेते हैं?",
    "en": "Do you have a history of alcohol use or take any medications?",
    "category": "jaundice",
    "symptom": "jaundice",
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
    "symptom": "exhaustion",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको पूरी रात की नींद या आराम के बाद भी थकान महसूस होती है?",
    "en": "Do you feel fatigued even after a full night’s sleep or rest?",
    "category": "exhaustion",
    "symptom": "exhaustion",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको कोई तनाव, चिंता या भावनात्मक बदलाव महसूस हो रहे हैं?",
    "en": "Do you have any stress, anxiety, or emotional changes?",
    "category": "exhaustion",
    "symptom": "exhaustion",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपको कोई ज्ञात चिकित्सीय स्थिति है, जैसे एनीमिया, थायरॉयड समस्याएं, या डायबिटीज?",
    "en": "Do you have a history of any medical conditions, such as anemia, thyroid problems, or diabetes?",
    "category": "exhaustion",
    "symptom": "exhaustion",
    "risk_factor": True,
  },
  {
    "hi": "क्या आपने हाल ही में अपनी आहार, व्यायाम दिनचर्या या जीवनशैली में कोई बदलाव किया है?",
    "en": "Have you made any recent changes to your diet, exercise routine, or lifestyle?",
    "category": "exhaustion",
    "symptom": "exhaustion",
    "risk_factor": False,
  },
],
"sleepy": [
  {
    "hi": "क्या आपको सोने में कठिनाई होती है, नींद में रुकावट आती है, या आप बहुत जल्दी उठ जाते हैं?",
    "en": "Do you have trouble falling asleep, staying asleep, or waking up too early?",
    "category": "sleepy",
    "symptom": "sleepy",
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
    "symptom": "sleepy",
    "risk_factor": False,
  },
  {
    "hi": "क्या आपने हाल ही में अपनी दिनचर्या या तनाव स्तर में कोई बदलाव महसूस किया है?",
    "en": "Have you experienced any recent changes in your routine or stress levels?",
    "category": "sleepy",
    "symptom": "sleepy",
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
      "hi": "क्या आपको मूत्र संबंधी कोई लक्षण हैं, जैसे बार-बार पेशाब आना या पेशाब करते समय दर्द होना?",
      "en": "Do you have any history of urinary symptoms, such as frequent urination or pain while urinating?",
      "category": "female issue",
      "symptom": "female issue",
      "risk_factor": True,
    },
    {
      "hi": "क्या आपने कोई असामान्य योनि स्राव या गंध महसूस की है?",
      "en": "Have you noticed any unusual vaginal discharge or odors?",
      "category": "female issue",
      "symptom": "female issue",
      "risk_factor": False,
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
      "hi": "क्या आपके शरीर में कोई हार्मोनल असंतुलन है?",
      "en": "Is there any hormonal imbalance in your body?",
      "category": "female issue",
      "symptom": "female issue",
      "risk_factor": False,
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
      "symptom": "thyroid",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने अपनी त्वचा, बालों, या नाखूनों में कोई बदलाव अनुभव किया है?",
      "en": "Have you experienced any changes in your skin, hair, or nails?",
      "category": "thyroid",
      "symptom": "thyroid",
      "risk_factor": False,
    },
    {
      "hi": "क्या आप अपनी मानसिक स्थिति में कोई बदलाव अनुभव कर रहे हैं, जैसे कि अवसाद या चिंता?",
      "en": "Are you experiencing any changes in your mood, such as depression or anxiety?",
      "category": "thyroid",
      "symptom": "thyroid",
      "risk_factor": False,
    },
    {
      "hi": "क्या आप असामान्य रूप से ठंडा या गर्म महसूस कर रहे हैं, या तापमान में बदलाव के प्रति संवेदनशीलता अनुभव कर रहे हैं?",
      "en": "Are you feeling unusually cold or hot, or experiencing sensitivity to temperature changes?",
      "category": "thyroid",
      "symptom": "thyroid",
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
      "symptom": "piles",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपकी शौच की आदतों में कोई बदलाव आया है (जैसे कब्ज, दस्त)?",
      "en": "Have you had any changes in your bowel habits (e.g., constipation, diarrhea)?",
      "category": "piles",
      "symptom": "piles",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपने शौच के दौरान या भारी वस्तुएं उठाते समय कोई जोर लगाया है?",
      "en": "Do you have a history of straining during bowel movements or lifting heavy objects?",
      "category": "piles",
      "symptom": "piles",
      "risk_factor": True,
    },
    {
      "hi": "क्या आपने गुदा के आसपास कोई गांठ या सूजन महसूस की है?",
      "en": "Have you experienced any lumps or swelling around the anus?",
      "category": "piles",
      "symptom": "piles",
      "risk_factor": False,
    },
    {
      "hi": "क्या आपको कोई पुरानी स्थितियाँ हैं, जैसे कब्ज, यकृत रोग, या गर्भावस्था?",
      "en": "Do you have any history of chronic conditions, such as constipation, liver disease, or pregnancy?",
      "category": "piles",
      "symptom": "piles",
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
            "symptom": "shortness of breath",
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

  'sugar': [
        {
            "hi": "क्या आप नियमित रूप से अपने ब्लड शुगर लेवल की जांच करते हैं?",
            "en": "Do you regularly monitor your blood sugar levels?",
            "category": "blood_sugar_monitoring",
            "symptom": "sugar",
            "risk_factor": True,
        },
        {
            "hi": "क्या आपने हाल ही में अपने ब्लड शुगर में किसी भी असामान्य बदलाव का अनुभव किया है?",
            "en": "Have you experienced any unusual changes in your blood sugar levels recently?",
            "category": "blood_sugar_changes",
            "symptom": "sugar",
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
            "symptom": "sugar",
            "risk_factor": False,
        },
        {
            "hi": "क्या आप शारीरिक गतिविधि में किसी प्रकार की वृद्धि या कमी देख रहे हैं ताकि आप अपने ब्लड शुगर को नियंत्रित कर सकें?",
            "en": "Are you increasing or decreasing your physical activities to manage your blood sugar levels?",
            "category": "blood_sugar_physical_activity",
            "symptom": "sugar",
            "risk_factor": False,
        },
        {
            "hi": "क्या आपके परिवार में किसी को डायबिटीज़ है?",
            "en": "Do you have a family history of diabetes?",
            "category": "family_history_diabetes",
            "symptom": "sugar",
            "risk_factor": True,
        },
        {
            "hi": "क्या आपको अपने ब्लड शुगर के स्तर में अचानक गिरावट या वृद्धि का अनुभव होता है?",
            "en": "Do you experience sudden drops or spikes in your blood sugar levels?",
            "category": "blood_sugar_fluctuations",
            "symptom": "sugar",
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
            "symptom": "sugar",
            "risk_factor": False,
        },
    ],
}

# ------------------------------------------------------------------ #
# ----------------------- Medicine Name List ----------------------- #
# ------------------------------------------------------------------ #
medications_list = [
    "ibuprofen", "acetaminophen", "paracetamol", "aspirin", "naproxen", "acetylsalicylic acid",
    "diclofenac", "meloxicam", "celecoxib", "indomethacin", "ketorolac", "butalbital", "dolo" ,"dolo 650",
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
    "biotin", "collagen", "probiotic", "omega-3", "fish oil",
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
    "sulfacetamide", "cyclopentolate", "hydrocortisone eye drops", "levofloxacin ophthalmic", "ketorolac ophthalmic",
    "flurbiprofen", "povidone-iodine", "dexamethasone eye drops", "lisinopril", "azithromycin eye drops",
    "acetazolamide (for glaucoma)",
    # Urology
    "finasteride", "tamsulosin", "sildenafil", "terazosin", "dutasteride", "vardenafil", "tadalafil", "alfuzosin",
    "oxybutynin", "tolterodine", "mirabegron", "desmopressin", "bethanechol", "dapoxetine", "flomax", "proscar",
    "silodosin", "bupropion", "indomethacin", "methyltestosterone", "tadalafil", "hydroxyurea", "gabapentin",
    "tramadol", "famotidine", "alpha blockers", "calcitonin", "hydrocodone", "morphine",
    # Anti-Viral and Anti-fungal
    "oseltamivir", "zanamivir", "acylovir", "valacyclovir", "ganciclovir", "amphotericin", "fluconazole",
    "terbinafine", "itraconazole", "nystatin", "clotrimazole", "ketoconazole", "miconazole", "fluconazole", "terbinafine",
    "griseofulvin", "miconazole", "nystatin", "terbinafine"
]
