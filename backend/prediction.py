import pandas as pd
import wikipedia

# data = pd.read_csv(r'C:\\Users\\Khushi\\Desktop\\Frameworks\\Rasa\\HealthBot\\backend\\Disease_Sheet.csv',encoding='utf-8')
# info = pd.read_csv(r'C:\\Users\\Khushi\\Desktop\\Frameworks\\Rasa\\HealthBot\\backend\\symptom_Description.csv')
data = pd.read_csv(r'/Users/rishikaul/Desktop/Health-bot/backend/Disease_Sheet.csv',encoding='utf-8')
info = pd.read_csv(r'/Users/rishikaul/Desktop/Health-bot/backend/symptom_Description.csv')

string = "please undergo {} after consulting your doctor"

# all_symps = set()
# for index, row in data.iterrows():
#   symptoms = row['Symptoms'].lower()
#   disease = row['Diseases']
#   list_sym = symptoms.split(',')
#   for sym in list_sym:
#     all_symps.add(sym.strip(' .').lower())

# for s in all_symps:
#   print(" - " + s)

symps = dict()
diagnosis = dict()
for index, row in data.iterrows():
  symptoms = row['Symptoms'].lower()
  disease = row['Diseases']
  list_sym = [symp.lower().strip(' ,.')  for symp in symptoms.split(',')]
  symps[disease] = list_sym
  diagnosis[disease] = string.format(row['Diagnosis'])

# print(symps)

def get_preventive_measures(disease):
  desc = ""
  for index, row in data.iterrows():
    if row['Diseases'].lower() == disease.lower():
      desc = "Preventive Measures for {} : \n".format(disease.title()) + row['Prevention']

      if desc == "Nothing" or len(desc) == 0 or len(desc) == 1:
        desc = get_diet(disease)
  return desc

def get_home_remedies(disease):
  desc = ""
  for index, row in data.iterrows():
    if row['Diseases'].lower() == disease.lower():
      desc = "Home Remedies for {} : \n".format(disease.title()) + row['Home-Remedies']

      if desc == "Nothing" or len(desc) == 0 or len(desc) == 1:
        desc = get_diet(disease)
  return desc

def get_diet(disease):
  desc = ""
  for index, row in data.iterrows():
    if row['Diseases'].lower() == disease.lower():
      print("HELLO")
      desc = "Diet Tips for {} : \n".format(disease.title()) + row['Diet']
  return desc

def get_symptoms(disease):
  desc = ""
  for index, row in data.iterrows():
    if row['Diseases'].lower() == disease.lower():
      print("HELLO")
      desc = "Symptoms for {} : \n".format(disease.title()) + row['Symptoms']
  return desc

def get_info(disease):
  information = ""
  desc = ""

  for index, row in info.iterrows():
    if row['Disease'].lower() == disease.lower():
      desc = row['Description']
      break

  for index, row in data.iterrows():
    if row['Diseases'].lower() == disease.lower():
      information += disease.title() + "\n\n"

      if desc:
        information += "Description : " + desc + "\n\n"
      else:
        desc = wikipedia.summary(disease)
        information += "Description : " + desc + "\n\n"

      information += "Symptoms : " + row['Symptoms'] + "\n\n"
      information += "Duration : " + row['Duration'] + '\n\n'
      information += "Preventive Measures : " + row['Prevention'] + "\n\n"
      information += "Diet during Disease : " + row['Diet'] + '\n\n'
      information += "Treatment : " + row['Treatment']

      return information
      
  information = wikipedia.summary(disease)

  return information

def preprocessing(symptomsList):
  sympList = list()
  for symp in symptomsList:
    symptom = symp["symptom"].lower()
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

def prediction(symptoms, user):

  processedSymptoms = preprocessing(symptoms)

  symptomLen = len(processedSymptoms)

  if symptomLen == 1:
        
    if processedSymptoms[0][0] == "cold":
          
      if user["frequent_cold"] == "yes":
        return {
          'flag' : 0,
          "Normal Cold" : "Since you get cold very often, having frequent steam sessions and using nasal decongestants would help. "
        }
      elif user["frequent_cold"] == "no" and processedSymptoms[0][1] <= 4:
        return {
          'flag' : 0,
          "Normal Cold" : "Try to have frequent steam sessions and use nasal decongestants for instant relief. If it doesn't subside within 1-2 days, try contacting a doctor."
        }
      else:
        return {
          'flag' : 0,
          "Cold" : "Since you do not have cold very often and it has been more than 4 days, its preferrable to visit a doctor"
        }
      
    if processedSymptoms[0][0] == "cough":
      if user["frequent_cough"] == "yes":
        return {
          'flag' : 0,
          "Normal Cough" : "Since you get cough very often, drinking boiled water and gargling with hot water would help. "
        }
      elif user["frequent_cough"] == "no" and processedSymptoms[0][1] <= 4:
        return {
          'flag' : 0,
          "Normal Cough" : "Try to drink boiled water and gargle with hot water for some relief. If it doesn't subside within 1-2 days, try contacting a doctor."
        }
      else:
        return {
          'flag' : 0,
          "Cough" : "Since you do not get cough very often and it has been more than 4 days, its preferrable to visit a doctor"
        }
    if processedSymptoms[0][0] == "fever":
      if processedSymptoms[0][1] <= 2:
        return {
          'flag' : 0,
          "Fever" : "Having any paracetemol like crocin might give you instant relief. If it doesn't subside today, try contacting a doctor."
        }
      else:
        return {
          'flag' : 0,
          "Fever" : "Since you've had fever for more than 2 days, its preferrable to visit a doctor."
        }
    if processedSymptoms[0][0] == "headache":
      if user["migraine"] == "yes":
        return {
          'flag' : 0,
          "Normal Headache" : "Since you have a past medical history with migraine, having frequent steam sessions and using nasal decongestants would help. "
        }
      elif user["frequent_cough"] == "no" and processedSymptoms[0][1] <= 4:
        return {
          'flag' : 0,
          "Normal Cough" : "Try to have frequent steam sessions and use nasal decongestants for instant relief. If it doesn't subside within 1-2 days, try contacting a doctor."
        }
      else:
        return {
          'flag' : 0,
          "Cough" : "Since you do not have cold very often and it has been more than 4 days, its preferrable to visit a doctor"
        }
    if processedSymptoms[0][0] == "legpain" or processedSymptoms[0][0] == "body pain" or processedSymptoms[0][0] == "bodypain" or processedSymptoms[0][0] == "leg pain":
      return {
        'flag' : 0,
        "Body Ache": "Having any paracetemol like crocin might give you instant relief. If it doesn't subside today, try contacting a doctor."
      }
      
  elif symptomLen == 2:
    processedSymptoms.sort(key = lambda x: x[0])
    # [('cold', 2), ('cough', 3), ('fever', 2)]
    if processedSymptoms[0][0] == "cold" and processedSymptoms[1][0] == "cough":
      if processedSymptoms[0][1] <= 2:
        return {
          'flag' : 0,
          "Cold & Cough": "Since it has been consistent for {} days, you can take normal medications for 1-2 days. If yet not cured you may visit a nearby doctor.".format(processedSymptoms[0][1])
        }
      else:
        return {
          'flag' : 0,
          "Cold & Cough" : "Since it has been for more than 4 days it is advised to contact any nearby doctor for proper diagnosis"
        }
    if processedSymptoms[0][0] == "cold" and processedSymptoms[1][0] == "fever":
      if processedSymptoms[1][1] <= 3:
        return {
          'flag' : 0,
          "Viral": "Since fever has been consistent for {} days along with cold, it seems to be viral. Contact your nearby doctor and medications and treatment.".format(processedSymptoms[1][1])
        }
      else:
        return {
          'flag' : 0,
          "Fever Profile" : "Since fever has been for more than 4 days along with cold it is advised to contact any nearby doctor and take prescription for fever profile blood test"
        }
    if processedSymptoms[0][0] == "cough" and processedSymptoms[1][0] == "fever":
      if processedSymptoms[1][1] <= 3:
        return {
          'flag' : 0,
          "Viral": "Since fever has been consistent for {} days along with cough, it seems to be viral. Contact your nearby doctor and medications and treatment.".format(processedSymptoms[1][1])
        }
      else:
        return {
          'flag' : 0,
          "Fever Profile" : "Since fever has been for more than 4 days along with cough it is advised to contact any nearby doctor and take prescription for fever profile blood test"
        }

  elif symptomLen == 3:
    processedSymptoms.sort(key = lambda x: x[0])

    if processedSymptoms[0][0] == "cold" and processedSymptoms[1][0] == "cough" and processedSymptoms[2][0] == "fever":
      if processedSymptoms[2][1] <= 3:
        return {
          'flag' : 0,
          "Viral": "Since fever has been consistent for {} days, it seems to be viral. Contact your nearby doctor and medications and treatment.".format(processedSymptoms[2][1])
        }
      else:
        return {
          'flag' : 0,
          "Fever Profile" : "Since fever has been for more than 4 days it is advised to contact any nearby doctor and take prescription for fever profile blood test"
        }

  print(processedSymptoms) 
  matches = match(processedSymptoms)
  print(matches)
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
  # for k, v in result.items():
    # print(v)
  res = dict()
  res['dis'] = result
  res['flag'] = 1
  return res

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