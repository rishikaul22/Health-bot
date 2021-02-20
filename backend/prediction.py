import pandas as pd
data = pd.read_csv('Disease Sheet - Sheet1.csv')
info = pd.read_csv('symptom_Description.csv')

string = "please undergo {} after consulting your doctor"

symps = dict()
diagnosis = dict()
for index, row in data.iterrows():
  symptoms = row['Symptoms'].lower()
  disease = row['Diseases']
  list_sym = [symp.lower().strip(' ,.')  for symp in symptoms.split(',')]
  symps[disease] = list_sym
  diagnosis[disease] = string.format(row['Diagnosis'])

def information(disease):
  desc = info[info['Disease']=='Arthritis']['Description']
  return desc

def preprocessing(symptomsList):
  sympList = list()
  for symp in symptomsList:
    symptom = symp["symptom"]
    duration = symp["duration"]
    sympList.append((symptom, duration))
  
  return sympList

def match(userSymptoms):
  matchPercent = dict()
  for disease,symptoms in symps.items():
    total = len(symptoms)
    count = 0
    for (symp,dur) in userSymptoms:
      if symp in symptoms:
        count = count + 1
    if count > 0:
      matchPercent[disease] = (count/total)*100
  return matchPercent
  
# symptoms = [
#   {
#     "symptom": "leg pain",
#     "duration": "2 days",
#   },
#   {
#     "symptom": "weakness",
#     "duration": "1 day"
#   },
#   {
#     "symptom": "cough",
#     "duration": "2 days"
#   },
#   {
#     "symptom": "chest pain",
#     "duration": "1 days"
#   },
#   {
#     "symptom": "headache",
#     "duration": "1 days"
#   }
# ]

def prediction(symptoms, user):

  processedSymptoms = preprocessing(symptoms)

  symptomLen = len(processedSymptoms)

  if symptomLen == 1:
        
    if processedSymptoms[0][0] == "cold":
          
      if user["frequent_cold"] == "yes":
        return {
          "Normal Cold" : "Since you get cold very often, having frequent steam sessions and using nasal decongestants would help. "
        }
      elif user["frequent_cold"] == "no" and processedSymptoms[0][1] <= 4:
        return {
          "Normal Cold" : "Try to have frequent steam sessions and use nasal decongestants for instant relief. If it doesn't subside within 1-2 days, try contacting a doctor."
        }
      else:
        return {
          "Cold" : "Since you do not have cold very often and it has been more than 4 days, its preferrable to visit a doctor"
        }
      
    if processedSymptoms[0][0] == "cough":
      if user["frequent_cough"] == "yes":
            return {
          "Normal Cough" : "Since you get cold very often, having frequent steam sessions and using nasal decongestants would help. "
        }
      elif user["frequent_cough"] == "no" and processedSymptoms[0][1] <= 4:
        return {
          "Normal Cough" : "Try to have frequent steam sessions and use nasal decongestants for instant relief. If it doesn't subside within 1-2 days, try contacting a doctor."
        }
      else:
        return {
          "Cough" : "Since you do not have cold very often and it has been more than 4 days, its preferrable to visit a doctor"
        }
    if processedSymptoms[0][0] == "fever":
      pass
    if processedSymptoms[0][0] == "headache":
      pass
    if processedSymptoms[0][0] == "legpain":
      pass

  elif symptomLen == 2:
    pass

  elif symptomLen == 3:
    pass

  print(processedSymptoms) 
  matches = match(processedSymptoms)
  sorted_tuples = sorted(matches.items(), key=lambda item: item[1], reverse = True)
  sorted_dict = {k: v for k, v in sorted_tuples}
  count = 0
  result = dict()
  for k in sorted_dict:
    res = k + ". For that, " + diagnosis[k]
    result[k] = res
    count += 1
    if count == 3:
        break
  for k, v in result.items():
    print(v)
  return result

## Ambigous Symptoms
# Difficulty in breathing
# muscle pain
# stomach cramps
# back pain
# stomach pain
# neck swelling
# loss of appetite
# muscle weakness
# loss of balance
# fast heart rate
# facial pain
# chest pain
# unable to recognize common things
# difficulty in concentration
# difficulty in speaking
# eye pain
# joint pain
# difficulty in moving joints
# forgetfulness
# inflammed eyes
# poor concentration
# irritability

# Cold, Cough and Fever
# if <= 3 days => viral
# if > 3 days check for fever profile blood test

# cold and cough
# if <= 5 days normal medication
# if > 5 days pneumonia

# cold 
# if frequent cold is yes, normal cold and give common medication
# if frequent cold is no then <= 4 days normal medication
# else > 4 days please visit your doctor

# cough 
# if dry cold is yes, normal cold and give common medication
# if frequent cold is no then <= 4 days normal medication
# else > 4 days please visit your doctor