unique = [
    'pain in breast',
    'stomach pain',
    'stomach ache',
    'redness in eyes',
    'palpitations',
    'burning sensations',
    'burning sensation in joints',
    'burning sensation in big toe',
    'light coloured skin patches ',
    'red coloured skin patches',
    'fast heart rate',
    'muscle weakness',
    'chest pain',
    'frequent urination',
    'hyperactivity',
    'loss of balance',
    'trouble in reading ',
    'difficulty in reading',
    'delayed growth',
    'poor wound healing',
    'neck swelling',
    'pain in breathing',
    'dark urine',
    'dehydration',
    'fainted ',
    'fainting',
    'unable to recognize common things',
    'poor concentration',
    'numbness in hands',
    'numbness in feet ',
    'weakness in hands',
    'weakness in feet',
    'swollen lymph nodes',
    'nausea',
    'cough',
    'a swollen stomach',
    'dark coloured urine',
    'dark coloured stool',
    'unable to understand conversations',
    'fluid discharge',
    'blood discharge',
    'failure to thrive',
    'memory loss',
    'confusion',
    'scaly skin ',
    'scaly areas',
    'trouble in spelling',
    'difficulty in concentration',
    'poor conentration',
    'coughing',
    'constipation',
    'diarrhoea',
    'swelling of nose',
    'painless ulcers on the soles of feet',
    'itchy skin',
    'hair loss',
    'weak bones',
    'memory loss',
    'painful urination',
    'difficulty in speaking',
    'muscle cramps',
    'slow movement',
    'eye pain with nausea',
    'chills ',
    'shivering',
    'jumbled speech',
    'depression',
    'loss of height',
    'skin infection',
    'frequent infection',
    'inflamed eyes',
    'stress',
    'forgetfulness',
    'cough with phlegm ',
    'pus ',
    'wheezing',
    'food intolerance',
    'stiffness',
    'sweating',
    'back pain',
    'headache',
    'nasal congestion',
    'difficulty in moving joints',
    'irritability',
    'tremors',
    'red rings or red ring',
    'confused',
    'itching',
    'vision loss',
    'swelling in breast',
    'blood in stools',
    'green pus discharge from the vagina or penis',
    'hunger or hungry',
    'yellowing of eyes or yellow eyes',
    'brittle nails',
    'abnormal discharge',
    'change in skin colour',
    'dark coloured urine',
    'a red skin rash',
    'dry cough',
    'tiredness',
    'dizziness ',
    'low mood ',
    'depression',
    'redness in nipples ',
    'redness in breast',
    'loss of taste ',
    'loss of smell',
    'loss of eyebrows ',
    'eyelashes',
    'fatigue',
    'stomach cramps',
    'flu like symptoms',
    'anxiety',
    'trembling',
    'bloated stomach ',
    'bloating',
    'inability to express',
    'restlessness',
    'blurred vision',
    'development delays',
    'yellowing of the eyes' ,
    'yellowing of skin',
    'weakness',
    'bone fracture',
    'heavier periods ',
    'spotting',
    'runny nose',
    'vomiting',
    'night sweats',
    'swelling',
    'fatigue',
    'constipation',
    'numbness ',
    'muscle pain',
    'cramping',
    'reduced range of motion',
    'neurological changes',
    'increased thirst',
    'rash with small red dots',
    'skin rashes',
    'sore throat',
    'bloody discharge from the nipples ',
    'blood from nipples',
    'body pain ',
    'back pain',
    'swelling in joints',
    'soar eyes',
    'limited thinking abilities',
    'sleep disorder',
    'lump in breast',
    'difficulty in swallowing ',
    'soreness',
    'facial pain',
    'loose watery stools ',
    'loose motions',
    'weight loss',
    'fever',
    'difficulty in breathing',
    'mood swings',
    'muscle tightness',
    'grey nails',
    'cramps',
    'rash',
    'ulcers'
    'distorted vision',
    'limited social skills',
    'difficulty in socializing',
    'cold',
    'joint pain',
    'loss of appetite'
    'painless swelling',
    'lumps on the face ',
    'lumps on earlobes',
]

# ambigious = [
# - muscle spasms
# - less body stability
# - high heart rate
# - high heart beat
# - pain in face
# - uneasy in the chest
# - unable to speak properly
# - unable to speak well
# - unable to speak normally
# - 

# - pain in the eye
# - eyes paining
# - pain in my joints
# - joints are paining
# - not able to move my joints
# - unable to remember
# - forgetting often
# - heavy eyes
# - swollen eyes
# - inflammation of eyes
# - unable to concentrate
# - unable to focus
# - irritated
# ]

# - intent: take_diet
#   examples: |
#     - i need a diet plan for [Alopecia](disease)
#     - show me a diet plan for [Alopecia](disease)
#     - tell me what should I eat during [Alopecia](disease)
#     - give me diet recommendations for [Alopecia](disease)
#     - what all can i eat during [Malaria](disease)
#     - what food can i eat during [Malaria](disease)
#     - show me diet recommendations for [Malaria](disease)
#     - diet plan for [Dengue](disease)
#     - diet recommendation for [Dengue](disease)
#     - [Dengue](disease) diet recommendations
#     - [Mumps](disease) diet plan
#     - i need a diet plan for [Mumps](disease)
#     - show me a diet plan for [Mumps](disease)
#     - tell me what should I eat during [Jaundice](disease)
#     - give me diet recommendations for [Jaundice](disease)
#     - what all can i eat during [Jaundice](disease)
#     - what food can i eat during [Diarrhoea](disease)
#     - show me diet recommendations for [Diarrhoea](disease)
#     - diet plan for [Diarrhoea](disease)
#     - diet recommendation for [Glaucoma](disease)
#     - [Glaucoma](disease) diet recommendations
#     - [Glaucoma](disease) diet plan