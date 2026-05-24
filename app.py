from flask import Flask, render_template_string, request, jsonify
import re
from collections import Counter

app = Flask(__name__)

# Sample penal code data
penal_code_data = {"Section 1": {"keywords": ["Title", "Extent", "Operation", "Code", "India"], "description": "Title and extent of operation of the Code"},
    "Section 2": {"keywords": ["Punishment", "Offences", "Within", "India"], "description": "Punishment of offences committed within India"},
    "Section 3": {"keywords": ["Punishment", "Offences", "Committed", "India", "Beyond", "Territorial", "Jurisdiction"], "description": "Punishment of offences committed beyond India"},
    "Section 4": {"keywords": ["Extension", "Code", "Commission", "Offence", "Indian", "Citizen", "Ship", "Anywhere"], "description": "Extension of Code to extra-territorial offences"},
    "Section 5": {"keywords": ["Certain", "Laws", "Repealed"], "description": "Certain laws not to be affected by this enactment"},
    "Section 6": {"keywords": ["Definitions"], "description": "Definitions in the Code to be understood subject to exceptions"},
    "Section 7": {"keywords": ["Sense", "Reference", "Districts", "Courts"], "description": "Sense of expressions once explained"},
    "Section 8": {"keywords": ["Gender", "Number"], "description": "Gender and number"},
    "Section 9": {"keywords": ["Words", "References", "Acts", "Words"], "description": "Acts of Parliament, how cited"},
    "Section 10": {"keywords": ["Punishment", "Offences", "Committed", "India"], "description": "Punishment of offences committed within India"},
    "Section 11": {"keywords": ["Persons", "Concerned", "Offence"], "description": "Persons concerned in criminal act may be guilty of different offences"},
    "Section 12": {"keywords": ["Punishment", "Offences", "Criminal", "Conspiracy", "Commission"], "description": "Punishment of offences committed beyond, but which by law may be tried within, India"},
    "Section 13": {"keywords": ["Effect", "Abetment", "Offence", "Abettor", "Apprehension", "Trial"], "description": "Effect caused partly by act and partly by omission"},
    "Section 14": {"keywords": ["Abettor", "Instigates", "Engages", "Conspiracy"], "description": "When such an act is criminal by reason of its being done with a criminal knowledge or intention"},
    "Section 15": {"keywords": ["Intention", "Instigation", "Engagement", "Conspiracy"], "description": "Explanation of 'voluntarily'"},
    "Section 16": {"keywords": ["Abettor", "Engages", "Conspiracy", "Intentionally"], "description": "Explanation of 'intentionally'"},
    "Section 17": {"keywords": ["Abettor", "Engages", "Conspiracy", "Concealment"], "description": "Explanation of 'conceal'"},
    "Section 18": {"keywords": ["Abettor", "Engages", "Conspiracy", "Performance"], "description": "Explanation of 'provides'"},
    "Section 19": {"keywords": ["Abettor", "Engages", "Conspiracy", "Criminal", "Offence"], "description": "Explanation of 'gives'"},
    "Section 20": {"keywords": ["Abettor", "Engages", "Conspiracy", "Person", "Engaged"], "description": "Explanation of 'dishonestly'"},
    "Section 21": {"keywords": ["Abettor", "Engages", "Conspiracy", "Offence", "Public"], "description": "Explanation of 'fraudulently'"},
    "Section 22": {"keywords": ["Abettor", "Engages", "Conspiracy", "Offence", "Not", "Committed"], "description": "Explanation of 'knowingly'"},
    "Section 23": {"keywords": ["Abettor", "Engages", "Conspiracy", "Performing", "Act"], "description": "Explanation of 'reason to believe'"},
    "Section 24": {"keywords": ["Abettor", "Engages", "Conspiracy", "Offence", "Caused"], "description": "Act done by a person incapable of judgment by reason of intoxication caused against his will"},
    "Section 25": {"keywords": ["Abettor", "Engages", "Conspiracy", "Performance", "Act", "Impracticable"], "description": "Act done by a person incapable of judgment by reason of intoxication caused voluntarily"},
    "Section 26": {"keywords": ["Abettor", "Engages", "Conspiracy", "Performing", "Act", "Impracticable"], "description": "When an act is an offence by reason of its being done with a criminal knowledge or intention"},
    "Section 27": {"keywords": ["Abettor", "Engages", "Conspiracy", "Performance", "Act", "Intended"], "description": "When an act is a criminal offence by reason of its being done with a criminal knowledge or intention"},
    "Section 28": {"keywords": ["Abettor", "Engages", "Conspiracy", "Act", "Done", "Consequence"], "description": "When an act is a criminal offence by reason of its being done with a criminal knowledge or intention"},
    "Section 29": {"keywords": ["Abettor", "Engages", "Conspiracy", "Performance", "Act", "Consequence", "Criminal"], "description": "When an act is a criminal offence by reason of its being done with a criminal knowledge or intention"},
    "Section 30": {"keywords": ["Abettor", "Engages", "Conspiracy", "Performance", "Act", "Criminal"], "description": "When an act is a criminal offence by reason of its being done with a criminal knowledge or intention"},
    "Section 31": {"keywords": ["Abettor", "Engages", "Conspiracy", "Criminal", "Offence", "Abettor", "Absent"], "description": "When an act is a criminal offence by reason of its being done with a criminal knowledge or intention"},
    "Section 32": {"keywords": ["Abettor", "Engages", "Conspiracy", "Performance", "Act", "Criminal"], "description": "When an act is a criminal offence by reason of its being done with a criminal knowledge or intention"},
    "Section 33": {"keywords": ["Punishment", "Offences", "Persons", "Culpable", "Offence"], "description": "Punishment of offences committed beyond, but which by law may be tried within, India"},
    "Section 34": {"keywords": ["Acts", "Which", "Done", "Aiding"], "description": "Acts done by several persons in furtherance of common intention"},
    "Section 35": {"keywords": ["When", "Independent", "Criminal", "Offences", "Consequence", "Occur", "Offence", "Intended", "Individual"], "description": "When such an act is criminal by reason of its being done with a criminal knowledge or intention"},
    "Section 36": {"keywords": ["Act", "Done", "Criminal", "Consequence", "Probable"], "description": "Effect caused partly by act and partly by omission"},
    "Section 37": {"keywords": ["Effect", "Criminal", "Offence", "Probable", "Consequence"], "description": "Effect caused partly by act and partly by omission"},
    "Section 38": {"keywords": ["Effect", "Criminal", "Offence", "Criminal", "Intention"], "description": "Effect caused partly by act and partly by omission"},
    "Section 39": {"keywords": ["Effect", "Act", "Done", "Criminal", "Intention"], "description": "Effect caused partly by act and partly by omission"},
    "Section 40": {"keywords": ["When", "Effect", "Act", "Done", "Preparation", "Intended", "Commission"], "description": "Effect caused partly by act and partly by omission"},
    "Section 41": {"keywords": ["Special", "Law", "Particular", "Act"], "description": "Special law in force to the exclusion of this Code"},
    "Section 42": {"keywords": ["Punishment", "Offences", "Committed", "India"], "description": "Punishment of offences committed within India"},
    "Section 43": {"keywords": ["Punishment", "Offences", "Committed", "India", "Beyond", "Territorial", "Jurisdiction"], "description": "Punishment of offences committed beyond India"},
    "Section 44": {"keywords": ["Extension", "Code", "Commission", "Offence", "Indian", "Citizen", "Ship", "Anywhere"], "description": "Extension of Code to extra-territorial offences"},
    "Section 45": {"keywords": ["Certain", "Laws", "Repealed"], "description": "Certain laws not to be affected by this enactment"},
    "Section 46": {"keywords": ["Definitions"], "description": "Definitions in the Code to be understood subject to exceptions"},
    "Section 47": {"keywords": ["Sense", "Reference", "Districts", "Courts"], "description": "Sense of expressions once explained"},
    "Section 48": {"keywords": ["Gender", "Number"], "description": "Gender and number"},
    "Section 49": {"keywords": ["Words", "References", "Acts", "Words"], "description": "Acts of Parliament, how cited"},
    "Section 50": {"keywords": ["Punishment", "Offences", "Committed", "India"], "description": "Punishment of offences committed within India"},
    "Section 51": {"keywords": ["Persons", "Concerned", "Offence"], "description": "Persons concerned in criminal act may be guilty of different offences"},
    "Section 52": {"keywords": ["Punishment", "Offences", "Criminal", "Conspiracy", "Commission"], "description": "Punishment of offences committed beyond, but which by law may be tried within, India"},
    "Section 53": {"keywords": ["Effect", "Abetment", "Offence", "Abettor", "Apprehension", "Trial"], "description": "Effect caused partly by act and partly by omission"},
    "Section 54": {"keywords": ["Abettor", "Instigates", "Engages", "Conspiracy"], "description": "When such an act is criminal by reason of its being done with a criminal knowledge or intention"},
    "Section 55": {"keywords": ["Intention", "Instigation", "Engagement", "Conspiracy"], "description": "Explanation of 'voluntarily'"},
    "Section 56": {"keywords": ["Abettor", "Engages", "Conspiracy", "Intentionally"], "description": "Explanation of 'intentionally'"},
    "Section 57": {"keywords": ["Abettor", "Engages", "Conspiracy", "Concealment"], "description": "Explanation of 'conceal'"},
    "Section 58": {"keywords": ["Abettor", "Engages", "Conspiracy", "Performance"], "description": "Explanation of 'provides'"},
    "Section 59": {"keywords": ["Abettor", "Engages", "Conspiracy", "Criminal", "Offence"], "description": "Explanation of 'gives'"},
    "Section 60": {"keywords": ["Abettor", "Engages", "Conspiracy", "Person", "Engaged"], "description": "Explanation of 'dishonestly'"},
    "Section 61": {"keywords": ["Abettor", "Engages", "Conspiracy", "Offence", "Public"], "description": "Explanation of 'fraudulently'"},
    "Section 62": {"keywords": ["Abettor", "Engages", "Conspiracy", "Offence", "Not", "Committed"], "description": "Explanation of 'knowingly'"},
    "Section 63": {"keywords": ["Abettor", "Engages", "Conspiracy", "Performing", "Act"], "description": "Explanation of 'reason to believe'"},
    "Section 64": {"keywords": ["Abettor", "Engages", "Conspiracy", "Offence", "Caused"], "description": "Act done by a person incapable of judgment by reason of intoxication caused against his will"},
    "Section 65": {"keywords": ["Abettor", "Engages", "Conspiracy", "Performance", "Act", "Impracticable"], "description": "Act done by a person incapable of judgment by reason of intoxication caused voluntarily"},
    "Section 66": {"keywords": ["Abettor", "Engages", "Conspiracy", "Performing", "Act", "Impracticable"], "description": "When an act is an offence by reason of its being done with a criminal knowledge or intention"},
    "Section 67": {"keywords": ["Abettor", "Engages", "Conspiracy", "Performance", "Act", "Intended"], "description": "When an act is a criminal offence by reason of its being done with a criminal knowledge or intention"},
    "Section 68": {"keywords": ["Abettor", "Engages", "Conspiracy", "Act", "Done", "Consequence"], "description": "When an act is a criminal offence by reason of its being done with a criminal knowledge or intention"},
    "Section 69": {"keywords": ["Abettor", "Engages", "Conspiracy", "Performance", "Act", "Consequence", "Criminal"], "description": "When an act is a criminal offence by reason of its being done with a criminal knowledge or intention"},
    "Section 70": {"keywords": ["Abettor", "Engages", "Conspiracy", "Performance", "Act", "Criminal"], "description": "When an act is a criminal offence by reason of its being done with a criminal knowledge or intention"},
    "Section 71": {"keywords": ["Abettor", "Engages", "Conspiracy", "Criminal", "Offence", "Abettor", "Absent"], "description": "When an act is a criminal offence by reason of its being done with a criminal knowledge or intention"},
    "Section 72": {"keywords": ["Abettor", "Engages", "Conspiracy", "Performance", "Act", "Criminal"], "description": "When an act is a criminal offence by reason of its being done with a criminal knowledge or intention"},
    "Section 73": {"keywords": ["Punishment", "Offences", "Persons", "Culpable", "Offence"], "description": "Punishment of offences committed beyond, but which by law may be tried within, India"},
    "Section 74": {"keywords": ["Acts", "Which", "Done", "Aiding"], "description": "Acts done by several persons in furtherance of common intention"},
    "Section 75": {"keywords": ["When", "Independent", "Criminal", "Offences", "Consequence", "Occur", "Offence", "Intended", "Individual"], "description": "When such an act is criminal by reason of its being done with a criminal knowledge or intention"},
    "Section 76": {"keywords": ["Act", "Done", "Criminal", "Consequence", "Probable"], "description": "Effect caused partly by act and partly by omission"},
    "Section 77": {"keywords": ["Effect", "Criminal", "Offence", "Probable", "Consequence"], "description": "Effect caused partly by act and partly by omission"},
    "Section 78": {"keywords": ["Effect", "Criminal", "Offence", "Criminal", "Intention"], "description": "Effect caused partly by act and partly by omission"},
    "Section 79": {"keywords": ["Effect", "Act", "Done", "Criminal", "Intention"], "description": "Effect caused partly by act and partly by omission"},
    "Section 80": {"keywords": ["When", "Effect", "Act", "Done", "Preparation", "Intended", "Commission"], "description": "Effect caused partly by act and partly by omission"},
    "Section 81": {"keywords": ["Special", "Law", "Particular", "Act"], "description": "Special law in force to the exclusion of this Code"},
    "Section 82": {"keywords": ["Punishment", "Offences", "Committed", "India"], "description": "Punishment of offences committed within India"},  
    "Section 83": {"keywords": ["Beyond", "Territorial", "Jurisdiction"], "description": "Punishment of offences committed beyond India"},
    "Section 84": {"keywords": ["Extension", "Extra-territorial", "Indian", "Citizenship"], "description": "Extension of Code to extra-territorial offences"},
    "Section 85": {"keywords": ["Certain", "Laws", "Repealed"], "description": "Certain laws not affected by this enactment"},
    "Section 86": {"keywords": ["Definitions"], "description": "Definitions in the Code subject to exceptions"},
    "Section 87": {"keywords": ["Sense", "Expressions", "Explained"], "description": "Sense of expressions once explained"},
    "Section 88": {"keywords": ["Gender", "Number"], "description": "Gender and number"},
    "Section 89": {"keywords": ["Acts", "Parliament", "Cited"], "description": "Acts of Parliament, how cited"},
    "Section 90": {"keywords": ["Punishment", "Offences", "Committed", "India"], "description": "Punishment of offences committed within India"},
    "Section 91": {"keywords": ["Persons", "Concerned", "Offence"], "description": "Persons concerned in criminal act may be guilty of different offences"},
    "Section 92": {"keywords": ["Punishment", "Offences", "Committed", "India"], "description": "Punishment of offences committed within India"},
    "Section 93": {"keywords": ["Effect", "Abetment", "Offence", "Trial"], "description": "Effect caused partly by act and partly by omission"},
    "Section 94": {"keywords": ["Abettor", "Criminal", "Knowledge", "Intention"], "description": "When an act is criminal by reason of its being done with a criminal knowledge or intention"},
    "Section 95": {"keywords": ["Intention", "Instigation", "Engagement", "Conspiracy"], "description": "Explanation of 'voluntarily'"},
    "Section 96": {"keywords": ["Abettor", "Engages", "Conspiracy", "Intentionally"], "description": "Explanation of 'intentionally'"},
    "Section 97": {"keywords": ["Abettor", "Engages", "Conspiracy", "Concealment"], "description": "Explanation of 'conceal'"},
    "Section 98": {"keywords": ["Abettor", "Engages", "Conspiracy", "Performance"], "description": "Explanation of 'provides'"},
    "Section 99": {"keywords": ["Abettor", "Engages", "Conspiracy", "Criminal", "Offence"], "description": "Explanation of 'gives'"},
    "Section 100": {
        "keywords": ["private defence", "body", "death", "harm", "assailant"],
        "description": "When the right of private defence of the body extends to causing death"
    },
    "Section 101": {
        "keywords": ["private defence", "body", "harm", "death", "assailant"],
        "description": "When such right extends to causing any harm other than death"
    },
    "Section 102": {
        "keywords": ["private defence", "body", "commencement", "continuance", "danger"],
        "description": "Commencement and continuance of the right of private defence of the body"
    },
    "Section 103": {
        "keywords": ["private defence", "property", "death", "harm", "wrong-doer"],
        "description": "When the right of private defence of property extends to causing death"
    },
    "Section 104": {
        "keywords": ["private defence", "property", "harm", "death", "theft"],
        "description": "When such right extends to causing any harm other than death"
    },
    "Section 105": {
        "keywords": ["private defence", "property", "commencement", "danger", "theft"],
        "description": "Commencement and continuance of the right of private defence of property"
    },
    "Section 106": {
        "keywords": ["private defence", "assault", "risk", "innocent person"],
        "description": "Right of private defence against deadly assault when there is risk of harm to innocent person"
    },
    "Section 107": {
        "keywords": ["abetment", "instigates", "conspiracy", "illegal omission"],
        "description": "Abetment of a thing"
    },
    "Section 108": {
        "keywords": ["abetment", "offence", "knowledge", "intention", "punishment"],
        "description": "Abettor"
    },
    "Section 109": {
        "keywords": ["punishment", "abetment", "consequence", "offence", "express provision"],
        "description": "Punishment of abetment if the act abetted is committed in consequence and where no express provision is made for its punishment"
    },
    "Section 110": {
        "keywords": ["punishment", "abetment", "different intention", "knowledge"],
        "description": "Punishment of abetment if person abetted does act with different intention from that of abettor"
    },
    "Section 111": {
        "keywords": ["liability", "abetment", "different act done"],
        "description": "Liability of abettor when one act abetted and different act done"
    },
    "Section 112": {
        "keywords": ["liability", "abetment", "cumulative punishment"],
        "description": "Abettor when liable to cumulative punishment for act abetted and for act done"
    },
    "Section 113": {
        "keywords": ["liability", "abetment", "effect caused"],
        "description": "Liability of abettor for an effect caused by the act abetted different from that intended by the abettor"
    },
    "Section 114": {
        "keywords": ["abetment", "present", "offence committed"],
        "description": "Abettor present when offence is committed"
    },
    "Section 115": {
        "keywords": ["abetment", "punishment", "death", "imprisonment for life"],
        "description": "Abetment of offence punishable with death or imprisonment for life.—if offence not committed"
    },
    "Section 116": {
        "keywords": ["abetment", "punishment", "imprisonment"],
        "description": "Abetment of offence punishable with imprisonment—if offence be not committed"
    },
    "Section 117": {
        "keywords": ["abetment", "offence", "public", "more than ten persons"],
        "description": "Abetting commission of offence by the public or by more than ten persons"
    },
    "Section 118": {
        "keywords": ["concealing design", "offence", "death", "imprisonment for life"],
        "description": "Concealing design to commit offence punishable with death or imprisonment for life"
    },
    "Section 119": {
        "keywords": ["concealing design", "public servant", "offence"],
        "description": "Public servant concealing design to commit offence which it is his duty to prevent"
    },
    "Section 120": {
        "keywords": ["concealing design", "offence", "imprisonment"],
        "description": "Concealing design to commit offence punishable with imprisonment"
    },
    "Section 121": {
        "keywords": ["waging war", "abetting", "Government of India"],
        "description": "Waging, or attempting to wage war, or abetting waging of war, against the Government of India"
    },
    "Section 122": {
        "keywords": ["collecting arms", "intention of waging war", "Government of India"],
        "description": "Collecting arms, etc., with intention of waging war against the Government of India"
    },
    "Section 123": {
        "keywords": ["concealing with intent", "waging war", "Government of India"],
        "description": "Concealing with intent to facilitate design to wage war"
    },
    "Section 124": {
        "keywords": ["assaulting", "President", "Governor", "lawful power"],
        "description": "Assaulting President, Governor, etc., with intent to compel or restrain the exercise of any lawful power"
    },
    "Section 125": {
        "keywords": ["waging war", "Asiatic Power", "alliance", "Government of India"],
        "description": "Waging war against any Asiatic Power in alliance with the Government of India"
    },
    "Section 126": {
        "keywords": ["depredation", "territories", "Government of India"],
        "description": "Committing depredation on territories of Power at peace with the Government of India"
    },
    "Section 127": {
        "keywords": ["receiving property", "war", "depredation"],
        "description": "Receiving property taken by war or depredation mentioned in sections 125 and 126"
    },
    "Section 128": {
        "keywords": ["public servant", "prisoner of state", "escape"],
        "description": "Public servant voluntarily allowing prisoner of state or war to escape"
    },
    "Section 129": {
        "keywords": ["public servant", "prisoner of state", "escape"],
        "description": "Public servant negligently suffering such prisoner to escape"
    },
    "Section 130": {
        "keywords": ["aiding escape", "rescuing", "harbouring", "prisoner"],
        "description": "Aiding escape of, rescuing or harbouring such prisoner"
    },
    "Section 131": {
        "keywords": ["abetment", "mutiny", "soldier", "sailor", "airman"],
        "description": "Abetting mutiny, or attempting to seduce a soldier, sailor or airman from his duty"
    },
    "Section 132": {
        "keywords": ["abetment", "mutiny", "soldier", "sailor", "airman"],
        "description": "Abetment of mutiny, if mutiny is committed in consequence thereof"
    },
    "Section 133": {
        "keywords": ["abetment", "assault", "superior officer"],
        "description": "Abetment of assault by soldier, sailor or airman on his superior officer, when in execution of his office"
    },
    "Section 134": {
        "keywords": ["abetment", "assault", "superior officer", "committed"],
        "description": "Abetment of such assault, if the assault committed"
    },
    "Section 135": {
        "keywords": ["abetment", "desertion", "soldier", "sailor", "airman"],
        "description": "Abetment of desertion of soldier, sailor or airman"
    },
    "Section 136": {
        "keywords": ["harbouring", "deserter"],
        "description": "Harbouring deserter"
    },
    "Section 137": {
        "keywords": ["deserter", "merchant vessel", "negligence", "penalty"],
        "description": "Deserter concealed on board merchant vessel through negligence of master"
    },
    "Section 138": {
        "keywords": ["abetment", "insubordination", "soldier", "sailor", "airman"],
        "description": "Abetment of act of insubordination by soldier, sailor or airman"
    },
    "Section 139": {
        "keywords": ["persons subject to Acts", "Army Act", "Navy Act", "Air Force Act"],
        "description": "Persons subject to certain Acts"
    },
    "Section 140": {
        "keywords": ["wearing garb", "carrying token", "soldier", "sailor", "airman"],
        "description": "Wearing garb or carrying token used by soldier, sailor or airman"
    },
    "Section 141": {
        "keywords": ["unlawful assembly", "government", "resist law", "mischief", "criminal force"],
        "description": "Unlawful assembly"
    },
    "Section 142": {
        "keywords": ["member", "unlawful assembly", "awareness"],
        "description": "Being member of unlawful assembly"
    },
    "Section 143": {
        "keywords": ["punishment", "unlawful assembly"],
        "description": "Punishment for unlawful assembly"
    },
    "Section 144": {
        "keywords": ["unlawful assembly", "deadly weapon"],
        "description": "Joining unlawful assembly armed with deadly weapon"
    },
    "Section 145": {
        "keywords": ["unlawful assembly", "disperse"],
        "description": "Joining or continuing in unlawful assembly, knowing it has been commanded to disperse"
    },
    "Section 146": {
        "keywords": ["rioting", "force", "violence", "common object"],
        "description": "Rioting"
    },
    "Section 147": {
        "keywords": ["punishment", "rioting"],
        "description": "Punishment for rioting"
    },
    "Section 148": {
        "keywords": ["rioting", "deadly weapon"],
        "description": "Rioting armed with deadly weapon"
    },
    "Section 149": {
        "keywords": ["unlawful assembly", "common object", "offence"],
        "description": "Every member of unlawful assembly guilty of offence committed in prosecution of common object"
    },
    "Section 150": {
        "keywords": ["hiring", "conniving", "unlawful assembly", "punishable", "member"],
        "description": "Hiring or conniving at hiring of persons to join unlawful assembly"
    },
    "Section 151": {
        "keywords": ["knowingly", "joining", "continuing", "assembly", "commanded", "disperse", "punished", "imprisonment", "fine"],
        "description": "Knowingly joining or continuing in assembly of five or more persons after it has been commanded to disperse"
    },
    "Section 152": {
        "keywords": ["assaulting", "obstructing", "public servant", "suppressing", "riot", "affray", "punished", "imprisonment", "fine"],
        "description": "Assaulting or obstructing public servant when suppressing riot, etc."
    },
    "Section 153": {
        "keywords": ["wantonly", "giving", "provocation", "intent", "cause", "riot", "malignantly", "illegal", "punished", "imprisonment", "fine"],
        "description": "Wantonly giving provocation with intent to cause riot"
    },
    "Section 153A": {
        "keywords": ["promoting", "enmity", "religion", "race", "prejudicial", "maintenance", "harmony", "disharmony", "disturbs", "public tranquillity", "criminal force", "violence"],
        "description": "Promoting enmity between different groups on ground of religion, race, place of birth, residence, language, etc., and doing acts prejudicial to maintenance of harmony"
    },
    "Section 154": {
        "keywords": ["owner", "occupier", "land", "unlawful assembly", "fine", "police station"],
        "description": "Owner or occupier of land on which an unlawful assembly is held"
    },
    "Section 155": {
        "keywords": ["liability", "person", "benefit", "riot", "punishable", "fine"],
        "description": "Liability of person for whose benefit riot is committed"
    },
    "Section 156": {
        "keywords": ["liability", "agent", "manager", "benefit", "riot", "punishable", "fine"],
        "description": "Liability of agent of owner or occupier for whose benefit riot is committed"
    },
    "Section 157": {
        "keywords": ["harbouring", "persons", "hired", "unlawful assembly", "imprisonment", "fine"],
        "description": "Harbouring persons hired for an unlawful assembly"
    },
    "Section 158": {
        "keywords": ["hired", "unlawful assembly", "riot", "punished", "imprisonment", "fine"],
        "description": "Being hired to take part in an unlawful assembly or riot"
    },
    "Section 159": {
        "keywords": ["affray", "fighting", "public place", "disturb", "public peace"],
        "description": "Affray"
    },
    "Section 160": {
        "keywords": ["punishment", "affray", "imprisonment", "fine"],
        "description": "Punishment for committing affray"
    },
    "Section 161": {
        "keywords": ["public servant", "gratification", "legal remuneration", "punished", "imprisonment", "fine"],
        "description": "Public servant taking gratification other than legal remuneration in respect of an official act"
    },
    "Section 162": {
        "keywords": ["gratification", "influence", "public servant", "punished", "imprisonment", "fine"],
        "description": "Taking gratification, in order, by corrupt or illegal means, to influence public servant"
    },
    "Section 163": {
        "keywords": ["gratification", "exercise", "personal influence", "public servant", "punished", "imprisonment", "fine"],
        "description": "Taking gratification, for exercise of personal influence with public servant"
    },
    "Section 164": {
        "keywords": ["abetment", "public servant", "offences", "punished", "imprisonment", "fine"],
        "description": "Punishment for abetment by public servant of offences defined in sections 162 or 163"
    },
    "Section 165": {
        "keywords": ["public servant", "valuable thing", "proceeding", "business", "punished", "imprisonment", "fine"],
        "description": "Public servant obtaining valuable thing, without consideration, from person concerned in proceeding or business transacted by such public servant"
    },
    "Section 165A": {
        "keywords": ["abetment", "offences", "punished", "imprisonment", "fine"],
        "description": "Punishment for abetment of offences defined in section 161 or section 165"
    },
    "Section 166": {
        "keywords": ["public servant", "disobeying", "law", "intent", "injury", "punished", "imprisonment", "fine"],
        "description": "Public servant disobeying law, with intent to cause injury to any person"
    },
    "Section 166B": {
        "keywords": ["non-treatment", "victim", "hospital", "contravenes", "Code of Criminal Procedure", "punished", "imprisonment", "fine"],
        "description": "Punishment for non-treatment of victim"
    },
    "Section 167": {
        "keywords": ["public servant", "framing", "incorrect document", "intent", "injury", "punished", "imprisonment", "fine"],
        "description": "Public servant framing an incorrect document with intent to cause injury"
    },
    "Section 168": {
        "keywords": ["public servant", "unlawfully", "engaging", "trade", "punished", "imprisonment", "fine"],
        "description": "Public servant unlawfully engaging in trade"
    },
    "Section 169": {
        "keywords": ["public servant", "unlawfully", "buying", "bidding", "property", "punished", "imprisonment", "fine"],
        "description": "Public servant unlawfully buying or bidding for property"
    },
    "Section 170": {
        "keywords": ["personating", "public servant", "punished", "imprisonment", "fine"],
        "description": "Personating a public servant"
    },
    "Section 171": {
        "keywords": ["wearing", "garb", "carrying", "token", "fraudulent", "intent", "punished", "imprisonment", "fine"],
        "description": "Wearing garb or carrying token used by public servant with fraudulent intent"
    },
    "Section 171A": {
        "keywords": ["candidate", "electoral right", "definitions", "Chapter IXA"],
        "description": "Candidate and electoral right"
    },
    "Section 171B": {
        "keywords": ["bribery", "elections", "offence", "punishment"],
        "description": "Bribery"
    },
    "Section 171C": {
        "keywords": ["undue influence", "elections", "offence", "punishment"],
        "description": "Undue influence at elections"
    },
    "Section 171D": {
        "keywords": ["personation", "elections", "offence", "punishment"],
        "description": "Personation at elections"
    },
    "Section 171E": {
        "keywords": ["bribery", "elections", "offence", "punishment"],
        "description": "Punishment for bribery"
    },
    "Section 171F": {
        "keywords": ["undue influence", "personation", "elections", "offence", "punishment"],
        "description": "Punishment for undue influence or personation at an election"
    },
    "Section 171G": {
        "keywords": ["false statement", "elections", "offence"],
        "description": "False statement in connection with an election"
    },
    "Section 171H": {
        "keywords": ["illegal payments", "elections", "offence"],
        "description": "Illegal payments in connection with an election"
    },
    "Section 171-I": {
        "keywords": ["failure to keep", "election accounts", "offence"],
        "description": "Failure to keep election accounts"
    },
    "Section 172": {
        "keywords": ["absconding", "avoid", "summons", "proceeding", "offence"],
        "description": "Absconding to avoid service of summons or other proceeding"
    },
    "Section 173": {
        "keywords": ["preventing", "service", "summons", "proceedings", "publication", "offence"],
        "description": "Preventing service of summons or other proceedings, or preventing publication thereof"
    },
    "Section 174": {
        "keywords": ["non-attendance", "obedience", "order", "public servant", "offence"],
        "description": "Non-attendance in obedience to an order from public servant"
    },
    "Section 174A": {
        "keywords": ["non-appearance", "proclamation", "CrPC 1973", "offence"],
        "description": "Non-appearance in response to a proclamation under section 82 of Act 2 of 1974"
    },
    "Section 175": {
        "keywords": ["omission", "produce", "document", "electronic record", "public servant", "offence"],
        "description": "Omission to produce document or electronic record to public servant by person legally bound to produce it"
    },
    "Section 176": {
        "keywords": ["omission", "give", "notice", "information", "public servant", "offence"],
        "description": "Omission to give notice or information to public servant by person legally bound to give it"
    },
    "Section 177": {
        "keywords": ["furnishing", "false information", "public servant", "offence"],
        "description": "Furnishing false information"
    },
    "Section 178": {
        "keywords": ["refusing", "oath", "affirmation", "public servant", "offence"],
        "description": "Refusing oath or affirmation when duly required by public servant to make it"
    },
    "Section 179": {
        "keywords": ["refusing", "answer", "public servant", "offence"],
        "description": "Refusing to answer public servant authorized to question"
    },
    "Section 180": {
        "keywords": ["refusing", "sign", "statement", "public servant", "offence"],
        "description": "Refusing to sign statement"
    },
    "Section 181": {
        "keywords": ["false statement", "oath", "affirmation", "public servant", "offence"],
        "description": "False statement on oath or affirmation to public servant or person authorized to administer an oath or affirmation"
    },
    "Section 182": {
        "keywords": ["false information", "intent", "injury", "public servant", "offence"],
        "description": "False information, with intent to cause public servant to use his lawful power to the injury of another person"
    },
    "Section 183": {
        "keywords": ["resistance", "taking property", "public servant", "offence"],
        "description": "Resistance to the taking of property by the lawful authority of a public servant"
    },
    "Section 184": {
        "keywords": ["obstructing", "sale", "property", "public servant", "offence"],
        "description": "Obstructing sale of property offered for sale by authority of public servant"
    },
    "Section 185": {
        "keywords": ["illegal purchase", "bid", "property", "public servant", "offence"],
        "description": "Illegal purchase or bid for property offered for sale by authority of public servant"
    },
    "Section 186": {
        "keywords": ["obstructing", "public servant", "discharge", "public functions", "offence"],
        "description": "Obstructing public servant in discharge of public functions"
    },
    "Section 187": {
        "keywords": ["omission", "assist", "public servant", "offence"],
        "description": "Omission to assist public servant when bound by law to give assistance"
    },
    "Section 188": {
        "keywords": ["disobedience", "order", "public servant", "offence"],
        "description": "Disobedience to order duly promulgated by public servant"
    },
    "Section 189": {
        "keywords": ["threat", "injury", "public servant", "offence"],
        "description": "Threat of injury to public servant"
    },
    "Section 190": {
        "keywords": ["threat", "induce", "refrain", "applying", "protection", "public servant", "offence"],
        "description": "Threat of injury to induce person to refrain from applying for protection to public servant"
    },
    "Section 191": {
        "keywords": ["giving", "false evidence", "judicial proceeding", "offence"],
        "description": "Giving false evidence"
    },
    "Section 192": {
        "keywords": ["fabricating", "false evidence", "judicial proceeding", "offence"],
        "description": "Fabricating false evidence"
    },
    "Section 193": {
        "keywords": ["punishment", "false evidence", "offence"],
        "description": "Punishment for false evidence"
    },
    "Section 194": {
        "keywords": ["fabricating", "false evidence", "conviction", "capital offence", "offence"],
        "description": "Giving or fabricating false evidence with intent to procure conviction of capital offence"
    },
    "Section 195": {
        "keywords": ["fabricating", "false evidence", "conviction", "offence", "punishment"],
        "description": "Giving or fabricating false evidence with intent to procure conviction of offence punishable with imprisonment for life or imprisonment"
    },
    "Section 196": {
        "keywords": ["using", "evidence", "false", "offence"],
        "description": "Using evidence known to be false"
    },
    "Section 197": {
        "keywords": ["issuing", "signing", "false certificate", "offence"],
        "description": "Issuing or signing false certificate"
    },
    "Section 198": {
        "keywords": ["using", "certificate", "false", "offence"],
        "description": "Using as true a certificate known to be false"
    },
    "Section 199": {
        "keywords": ["false statement", "declaration", "evidence", "offence"],
        "description": "False statement made in declaration which is by law receivable as evidence"
    },
    "Section 200": {
        "keywords": ["using", "declaration", "false", "offence"],
        "description": "Using as true such declaration knowing it to be false"
    },
    "Section 201": {
        "keywords": ["causing", "disappearance", "evidence", "giving", "false information", "screen", "offender", "offence"],
        "description": "Causing disappearance of evidence of offence, or giving false information to screen offender"
    },
    "Section 202": {
        "keywords": ["omission", "give information", "offence", "person bound", "inform"],
        "description": "Intentional omission to give information of offence by person bound to inform"
    },
    "Section 203": {
        "keywords": ["giving", "false information", "offence", "respects", "offence committed"],
        "description": "Giving false information respecting an offence committed"
    },
    "Section 204": {
        "keywords": ["destruction", "document", "electronic record", "evidence", "offence", "prevent", "production"],
        "description": "Destruction of document or electronic record to prevent its production as evidence"
    },
    "Section 205": {
        "keywords": ["false personation", "act", "proceeding", "suit", "prosecution", "offence"],
        "description": "False personation for purpose of act or proceeding in suit or prosecution"
    },
    "Section 206": {
        "keywords": ["fraudulent", "removal", "concealment", "property", "seizure", "forfeited", "execution", "offence"],
        "description": "Fraudulent removal or concealment of property to prevent its seizure as forfeited or in execution"
    },
    "Section 207": {
        "keywords": ["fraudulently", "suffering", "decree", "offence", "sum", "not due"],
        "description": "Fraudulently suffering decree for sum not due"
    },
    "Section 208": {
        "keywords": ["dishonestly", "making", "false claim", "court", "injure", "annoy", "offence"],
        "description": "Dishonestly making false claim in Court"
    },
    "Section 209": {
        "keywords": ["fraudulently", "obtaining", "decree", "sum", "not due", "offence"],
        "description": "Fraudulently obtaining decree for sum not due"
    },
    "Section 210": {
        "keywords": ["false charge", "offence", "intent", "injure", "offence made"],
        "description": "False charge of offence made with intent to injure"
    },
    "Section 211": {
        "keywords": ["harbouring", "offender", "offence", "punishment", "imprisonment"],
        "description": "Harbouring offender"
    },
    "Section 212": {
        "keywords": ["taking", "gift", "screen", "offender", "punishment"],
        "description": "Taking gift, etc., to screen an offender from punishment"
    },
    "Section 213": {
        "keywords": ["offering", "gift", "restoration", "property", "screen", "offender", "punishment"],
        "description": "Offering gift or restoration of property in consideration of screening offender"
    },
    "Section 214": {
        "keywords": ["taking", "gift", "recover", "stolen property", "offence", "punishment"],
        "description": "Taking gift to help to recover stolen property, etc"
    },
    "Section 215": {
        "keywords": ["harbouring", "offender", "escaped", "custody", "apprehension", "ordered", "offence"],
        "description": "Harbouring offender who has escaped from custody or whose apprehension has been ordered"
    },
    "Section 216": {
        "keywords": ["harbouring", "robbers", "dacoits", "offence", "punishment"],
        "description": "Penalty for harbouring robbers or dacoits"
    },
    "Section 217": {
        "keywords": ["public servant", "disobeying", "direction", "law", "intent", "save", "person", "property", "punishment"],
        "description": "Public servant disobeying direction of law with intent to save person from punishment or property from forfeiture"
    },
    "Section 218": {
        "keywords": ["public servant", "framing", "incorrect record", "writing", "intent", "save", "person", "property", "punishment"],
        "description": "Public servant framing incorrect record or writing with intent to save person from punishment or property from forfeiture"
    },
    "Section 219": {
        "keywords": ["public servant", "judicial proceeding", "corruptly", "making report", "false", "order", "decision", "punishment"],
        "description": "Public servant in judicial proceeding corruptly making report, etc., contrary to law"
    },
    "Section 220": {
        "keywords": ["commitment", "trial", "confinement", "authority", "contrary", "law", "punishment"],
        "description": "Commitment for trial or confinement by person having authority who knows that he is acting contrary to law"
    },
    "Section 221": {
        "keywords": ["intentional", "omission", "apprehend", "public servant", "bound", "offence"],
        "description": "Intentional omission to apprehend on the part of public servant bound to apprehend"
    },
    "Section 222": {
        "keywords": ["intentional", "omission", "apprehend", "public servant", "knows", "offence"],
        "description": "Intentional omission to apprehend on the part of public servant, who knows that he ought to apprehend"
    },
    "Section 223": {
        "keywords": ["intentional", "omission", "inform", "public servant", "bound", "offence"],
        "description": "Intentional omission to give information of offence by person bound to inform"
    },
    "Section 224": {
        "keywords": ["intentional", "omission", "inform", "public servant", "knows", "offence"],
        "description": "Intentional omission to give information of offence by person who knows or believes that offence has been committed"
    },
    "Section 225": {
        "keywords": ["resistance", "rescue", "offence", "arrest", "prevent", "apprehension", "offender"],
        "description": "Resistance or obstruction to lawful apprehension of another person"
    },
    "Section 225A": {
        "keywords": ["transit remand", "removal", "accused", "prisoner", "bail"],
        "description": "Omission to apprehend, or sufferance of escape, on part of public servant, in cases not otherwise provided for"
    },
    "Section 225B": {
        "keywords": ["sufferance", "escape", "convicted", "offence", "punishment"],
        "description": "Omission to apprehend, or sufferance of escape, on part of public servant, in cases not otherwise provided for"
    },
    "Section 226": {
        "keywords": ["preventing", "service", "summons", "prevent", "service", "offence"],
        "description": "Preventing service of summons or other proceeding, or preventing publication thereof"
    },
    "Section 227": {
        "keywords": ["attempting", "commit", "offence", "not committed"],
        "description": "Attempting to commit offences punishable with imprisonment for life or other imprisonment"
    },
    "Section 228": {
        "keywords": ["intentional insult", "provocation", "breach", "public peace"],
        "description": "Intentional insult or interruption to public servant sitting in judicial proceeding"
    },
    "Section 229": {
        "keywords": ["personation", "office", "election", "municipality", "offence"],
        "description": "Personation of public servant"
    },
    "Section 230": {
        "keywords": ["personation", "office", "election", "municipality", "offence"],
        "description": "Personation of a person holding an office under Government"
    },
    "Section 231": {
        "keywords": ["personation", "office", "election", "municipality", "offence"],
        "description": "Personation of a juror or assessor"
    },
    "Section 232": {
        "keywords": ["false", "personation", "purpose", "election", "offence"],
        "description": "False personation for purpose of a election"
    },
    "Section 233": {
        "keywords": ["false", "personation", "person", "get", "vantage", "offence"],
        "description": "Making or possessing counterfeit seal, etc., with intent to commit forgery punishable otherwise"
    },
    "Section 234": {
        "keywords": ["whoever", "commits", "rape", "women", "husband", "living", "together", "offence", "punishable", "imprisonment"],
        "description": "Whoever commits rape on a woman who is his wife, living separately"
    },
    "Section 235": {
        "keywords": ["whoever", "commits", "rape", "women", "under", "twelve", "years", "offence", "punishable", "imprisonment"],
        "description": "Whoever commits rape on a woman under twelve years of age"
    },
    "Section 236": {
        "keywords": ["commits", "gang rape", "women", "offence", "punishable", "imprisonment"],
        "description": "Whoever commits gang rape"
    },
    "Section 237": {
        "keywords": ["commits", "gang rape", "women", "woman", "under", "twelve", "years", "offence", "punishable", "imprisonment"],
        "description": "Whoever, being a police officer, commits gang rape"
    },
    "Section 238": {
        "keywords": ["commits", "gang rape", "women", "woman", "under", "twelve", "years", "offence", "punishable", "imprisonment"],
        "description": "Whoever, being a public servant, commits gang rape"
    },
    "Section 239": {
        "keywords": ["commits", "gang rape", "women", "woman", "under", "twelve", "years", "offence", "punishable", "imprisonment"],
        "description": "Whoever, being a member of the armed forces of the Union, commits gang rape"
    },
    "Section 240": {
        "keywords": ["woman", "presumed", "physically", "incapable", "consent", "sexual intercourse"],
        "description": "When a woman is raped by one or more in a group of persons acting in furtherance of their common intention"
    },
    
    "Section 241": {
        "keywords": ["delivery", "Indian coin", "possession", "counterfeit", "knows", "imprisonment", "fine"],
        "description": "Punishes delivery of Indian coin possessed with knowledge that it is counterfeit, with imprisonment up to 10 years and fine"
    },
    "Section 242": {
        "keywords": ["possession", "counterfeit coin", "knows", "imprisonment", "fine"],
        "description": "Punishes possession of counterfeit coin by person who knew it to be counterfeit when he became possessed, with imprisonment up to 3 years and fine"
    },
    "Section 243": {
        "keywords": ["possession", "Indian coin", "counterfeit", "knows", "imprisonment", "fine"],
        "description": "Punishes possession of counterfeit Indian coin by person who knew it to be counterfeit when he became possessed, with imprisonment up to 7 years and fine"
    },
    "Section 244": {
        "keywords": ["person employed", "mint", "coin", "weight", "composition", "imprisonment", "fine"],
        "description": "Punishes person employed in mint causing coin to be different from that fixed by law, with imprisonment up to 7 years and fine"
    },
    "Section 245": {
        "keywords": ["unlawfully", "taking", "coin", "mint", "imprisonment", "fine"],
        "description": "Punishes unlawfully taking coining instrument from mint, with imprisonment up to 7 years and fine"
    },
    "Section 246": {
        "keywords": ["fraudulently", "diminishing", "weight", "altering", "composition", "coin", "imprisonment", "fine"],
        "description": "Punishes fraudulently diminishing weight or altering composition of coin, with imprisonment up to 3 years and fine"
    },
    "Section 247": {
        "keywords": ["fraudulently", "diminishing", "weight", "altering", "composition", "Indian coin", "imprisonment", "fine"],
        "description": "Punishes fraudulently diminishing weight or altering composition of Indian coin, with imprisonment up to 7 years and fine"
    },
    "Section 248": {
        "keywords": ["altering", "appearance", "coin", "intent", "pass", "imprisonment", "fine"],
        "description": "Punishes altering appearance of coin with intent that it shall pass as coin of different description, with imprisonment up to 3 years and fine"
    },
    "Section 249": {
        "keywords": ["altering", "appearance", "Indian coin", "intent", "pass", "imprisonment", "fine"],
        "description": "Punishes altering appearance of Indian coin with intent that it shall pass as coin of different description, with imprisonment up to 7 years and fine"
    },
    "Section 250": {
        "keywords": ["delivery", "coin", "altered", "possession", "knowledge", "imprisonment", "fine"],
        "description": "Punishes delivery of coin possessed with knowledge that it is altered, with imprisonment up to 5 years and fine"
    },
    "Section 251": {
        "keywords": ["delivery", "Indian coin", "altered", "possession", "knowledge", "imprisonment", "fine"],
        "description": "Punishes delivery of Indian coin possessed with knowledge that it is altered, with imprisonment up to 10 years and fine"
    },
    "Section 252": {
        "keywords": ["possession", "coin", "altered", "knows", "imprisonment", "fine"],
        "description": "Punishes possession of coin by person who knew it to be altered when he became possessed, with imprisonment up to 3 years and fine"
    },
    "Section 253": {
        "keywords": ["possession", "Indian coin", "altered", "knows", "imprisonment", "fine"],
        "description": "Punishes possession of Indian coin by person who knew it to be altered when he became possessed, with imprisonment up to 5 years and fine"
    },
    "Section 254": {
        "keywords": ["delivery", "coin", "altered", "possession", "knowledge", "imprisonment", "fine"],
        "description": "Punishes delivery of coin as genuine which is altered and not known to be so when possessed, with imprisonment up to 2 years or fine up to 10 times the value of the coin"
    },
    "Section 255": {
        "keywords": ["counterfeiting", "Government stamp", "process", "imprisonment", "fine"],
        "description": "Punishes counterfeiting or any part of process of counterfeiting Government revenue stamp, with imprisonment for life or imprisonment up to 10 years and fine"
    },
    "Section 256": {
        "keywords": ["possession", "instrument", "material", "counterfeiting", "Government stamp", "imprisonment", "fine"],
        "description": "Punishes possession of instrument or material for purpose of counterfeiting Government revenue stamp, with imprisonment up to 7 years and fine"
    },
    "Section 257": {
        "keywords": ["making", "selling", "instrument", "counterfeiting", "Government stamp", "imprisonment", "fine"],
        "description": "Punishes making, selling, disposing any instrument for purpose of counterfeiting Government revenue stamp, with imprisonment up to 7 years and fine"
    },
    "Section 258": {
        "keywords": ["sale", "counterfeit", "Government stamp", "imprisonment", "fine"],
        "description": "Punishes sale or offer for sale of any counterfeit Government revenue stamp, with imprisonment up to 7 years and fine"
    },
    "Section 259": {
        "keywords": ["possession", "counterfeit", "Government stamp", "use", "dispose", "imprisonment", "fine"],
        "description": "Punishes possession of counterfeit Government revenue stamp to use or dispose as genuine, with imprisonment up to 7 years and fine"
    },
    "Section 260": {
        "keywords": ["using", "Government stamp", "counterfeit", "knowledge", "imprisonment", "fine"],
        "description": "Punishes use as genuine of Government revenue stamp known to be counterfeit, with imprisonment up to 7 years or fine or both"
    },
    "Section 261": {
        "keywords": ["effacing", "writing", "substance", "Government stamp", "document", "imprisonment", "fine"],
        "description": "Punishes fraudulently removing writing or stamp from document bearing Government revenue stamp, with imprisonment up to 3 years, fine, or both"
    },
    "Section 262": {
        "keywords": ["using", "Government stamp", "previously used", "imprisonment", "fine"],
        "description": "Punishes fraudulently reusing Government revenue stamp known to have been already used, with imprisonment up to 2 years, fine, or both"
    },
    "Section 263": {
        "keywords": ["erasure", "mark", "stamp", "used", "imprisonment", "fine"],
        "description": "Punishes fraudulently erasing mark showing Government revenue stamp to have been used, or possessing such stamp, with imprisonment up to 3 years, fine, or both"
    },
    "Section 264": {
        "keywords": ["prohibition", "fictitious", "stamps", "making", "selling", "using", "possessing", "seizure", "forfeiture"],
        "description": "Punishes making, selling, using, possessing fictitious stamps or instruments for making them, seizure and forfeiture of such stamps and instruments"
    },
    "Section 265": {
        "keywords": ["fraudulent", "instrument", "weighing", "imprisonment", "fine"],
        "description": "Punishes fraudulent use of false instrument for weighing with imprisonment up to 1 year, fine, or both"
    },
    "Section 266": {
        "keywords": ["fraudulent", "weight", "measure", "imprisonment", "fine"],
        "description": "Punishes fraudulent use of false weight or measure with imprisonment up to 1 year, fine, or both"
    },
    "Section 267": {
        "keywords": ["possession", "false weight", "measure", "imprisonment", "fine"],
        "description": "Punishes possession of false weight or measure intending it to be fraudulently used, with imprisonment up to 1 year, fine, or both"
    },
    "Section 268": {
        "keywords": ["making", "selling", "false weight", "measure", "imprisonment", "fine"],
        "description": "Punishes making, selling or disposing false weight or measure to be used as true with imprisonment up to 1 year, fine, or both"
    },
    "Section 269": {
        "keywords": ["public nuisance", "act", "illegal omission", "common injury", "danger", "annoyance", "imprisonment", "fine"],
        "description": "Offence of public nuisance by doing any act or illegal omission causing common injury, danger or annoyance to public"
    },
    "Section 270": {
        "keywords": ["negligent act", "infection", "disease", "dangerous to life", "imprisonment", "fine"],
        "description": "Punishes negligent act likely to spread infection of life-threatening disease with imprisonment up to 6 months, fine, or both"
    },
    "Section 271": {
        "keywords": ["malignant act", "infection", "disease", "dangerous to life", "imprisonment", "fine"],
        "description": "Punishes malignant act likely to spread infection of life-threatening disease with imprisonment up to 2 years, fine, or both"
    },
    "Section 272": {
        "keywords": ["disobedience", "quarantine rule", "imprisonment", "fine"],
        "description": "Punishes disobedience to quarantine rules with imprisonment up to 6 months, fine, or both"
    },
    "Section 273": {
        "keywords": ["adulteration", "food", "drink", "sale", "noxious", "imprisonment", "fine"],
        "description": "Punishes adulteration of food or drink to make it noxious, intending to sell it or knowing it is likely to be sold, with imprisonment up to 6 months, fine up to Rs. 1000, or both"
    },
    "Section 274": {
        "keywords": ["adulteration", "drugs", "sale", "lessen efficacy", "change operation", "imprisonment", "fine"],
        "description": "Punishes adulteration of any drug or medical preparation to lessen efficacy or change operation, intending it to be sold or used as unadulterated, with imprisonment up to 6 months, fine up to Rs. 1000, or both"
    },
    "Section 275": {
        "keywords": ["sale", "adulterated drugs", "dispensary", "use", "imprisonment", "fine"],
        "description": "Punishes sale, issuance from dispensary, use by any person, of drug or medical preparation known to be adulterated, with imprisonment up to 6 months, fine up to Rs. 1000, or both"
    },
    "Section 276": {
        "keywords": ["sale", "drug", "different preparation", "imprisonment", "fine"],
        "description": "Punishes knowingly selling, issuing from dispensary, any drug or medical preparation as a different drug or preparation, with imprisonment up to 6 months, fine up to Rs. 1000, or both"
    },
    "Section 277": {
        "keywords": ["fouling", "water", "public spring", "reservoir", "corrupting", "imprisonment", "fine"],
        "description": "Punishes voluntarily corrupting or fouling water of public spring or reservoir to make it less fit for ordinary use, with imprisonment up to 3 months, fine up to Rs. 500, or both"
    },
    "Section 278": {
        "keywords": ["making", "atmosphere", "noxious", "health", "fine"],
        "description": "Punishes voluntarily vitiating atmosphere to make it noxious to public health, with fine up to Rs. 500"
    },
    "Section 279": {
        "keywords": ["rash driving", "riding", "public way", "endangering", "imprisonment", "fine"],
        "description": "Punishes rash or negligent driving or riding on a public road endangering human life or likely to cause hurt or injury, with imprisonment up to 6 months, fine up to Rs. 1000, or both"
    },
    "Section 280": {
        "keywords": ["rash navigation", "vessel", "endangering", "imprisonment", "fine"],
        "description": "Punishes rash or negligent navigation of vessel endangering human life or likely to cause hurt or injury, with imprisonment up to 6 months, fine up to Rs. 1000, or both"
    },
    "Section 281": {
        "keywords": ["exhibition", "false light", "mark", "buoy", "mislead navigators", "imprisonment", "fine"],
        "description": "Punishes exhibition of false light, mark or buoy to mislead navigators, with imprisonment up to 7 years, fine, or both"
    },
    "Section 282": {
        "keywords": ["conveying", "unsafe", "overloaded vessel", "imprisonment", "fine"],
        "description": "Punishes knowingly or negligently conveying person for hire in unsafe or overloaded vessel, with imprisonment up to 6 months, fine up to Rs. 1000, or both"
    },
    "Section 283": {
        "keywords": ["danger", "obstruction", "public way", "navigation line", "fine"],
        "description": "Punishes causing danger, obstruction or injury in any public way or navigation line, with fine up to Rs. 200"
    },
    "Section 284": {
        "keywords": ["negligent conduct", "poisonous substance", "endanger", "hurt", "imprisonment", "fine"],
        "description": "Punishes negligent conduct with poison likely to endanger human life or cause hurt, with imprisonment up to 6 months, fine up to Rs. 1000, or both"
    },
    "Section 285": {
        "keywords": ["negligent conduct", "fire", "combustible matter", "endanger", "hurt", "imprisonment", "fine"],
        "description": "Punishes negligent conduct with fire or combustible substance likely to endanger human life or cause hurt, with imprisonment up to 6 months, fine up to Rs. 1000, or both"
    },
    "Section 286": {
        "keywords": ["negligent conduct", "explosive substance", "endanger", "hurt", "imprisonment", "fine"],
        "description": "Punishes negligent conduct with explosive substance likely to endanger human life or cause hurt, with imprisonment up to 6 months, fine up to Rs. 1000, or both"
    },
    "Section 287": {
        "keywords": ["negligent conduct", "machinery", "endanger", "hurt", "imprisonment", "fine"],
        "description": "Punishes negligent conduct with machinery likely to endanger human life or cause hurt, with imprisonment up to 6 months, fine up to Rs. 1000, or both"
    },
    "Section 288": {
        "keywords": ["negligent conduct", "pulling down", "repairing buildings", "endanger", "imprisonment", "fine"],
        "description": "Punishes negligent omission to take precautions against danger to human life from repair or demolition of buildings, with imprisonment up to 6 months, fine up to Rs. 1000, or both"
    },
    "Section 289": {
        "keywords": ["negligent conduct", "animal", "endanger", "hurt", "imprisonment", "fine"],
        "description": "Punishes negligent omission to take precautions against danger to human life or grievous hurt from any animal, with imprisonment up to 6 months, fine up to Rs. 1000, or both"
    },
    "Section 290": {
        "keywords": ["public nuisance", "fine"],
        "description": "Punishes public nuisance in cases not specially provided with fine up to Rs. 200"
    },
    "Section 291": {
        "keywords": ["continuance", "nuisance", "injunction", "discontinue", "imprisonment", "fine"],
        "description": "Punishes continuance of public nuisance after injunction to discontinue, with simple imprisonment up to 6 months, fine, or both"
    },
    "Section 292": {
        "keywords": ["sale", "obscene books", "distribution", "possession", "publication", "import", "export", "fine"],
        "description": "Punishes sale, distribution, possession, publication, import, export of obscene objects"
    },
    "Section 293": {
        "keywords": ["sale", "obscene objects", "young person", "distribution", "exhibition", "circulation", "fine"],
        "description": "Punishes sale, distribution, exhibition or circulation to persons under 20 years of obscene objects described u/s 292"
    },
    "Section 294": {
        "keywords": ["obscene acts", "songs", "public places", "annoyance", "imprisonment", "fine"],
        "description": "Punishes obscene acts or songs in public places to annoyance of others, with imprisonment up to 3 months, fine, or both"
    },
    "Section 295": {
        "keywords": ["injuring", "defiling", "place of worship", "intent", "insult religion", "destroying", "damaging", "religious object", "imprisonment", "fine"],
        "description": "Punishes destroying, damaging or defiling any place of worship or sacred object to insult religion of any class of persons, with imprisonment up to 2 years, fine, or both"
    },
    "Section 295A": {
        "keywords": ["outrage", "religious feelings", "insulting", "religion", "beliefs", "imprisonment", "fine"],
        "description": "Punishes acts intended to outrage religious feelings of any class by insulting its religion or beliefs with imprisonment up to 3 years, fine, or both"
    },
    "Section 296": {
        "keywords": ["disturbing", "religious assembly", "annoyance", "imprisonment", "fine"],
        "description": "Punishes voluntarily causing disturbance to any assembly engaged in religious worship or ceremonies, with imprisonment up to 1 year, fine, or both"
    },
    "Section 297": {
        "keywords": ["trespassing", "burial places", "wound feelings", "insult religion", "imprisonment", "fine"],
        "description": "Punishes trespass on burial places, etc. with intention to wound feelings or insult religion of any person, with imprisonment up to 1 year, fine, or both"
    },
    "Section 298": {
        "keywords": ["uttering words", "wound religious feelings", "imprisonment", "fine"],
        "description": "Punishes uttering any word or making any sound, gesture or exhibit object intending to wound religious feelings of any person, with imprisonment up to 1 year, fine, or both"
    },
    "Section 299": {
        "keywords": ["culpable homicide", "death", "intention", "knowledge", "imprisonment"],
        "description": "Defines culpable homicide as causing death with intention, knowledge or reason to believe that act is likely to cause death"
    },
    "Section 300": {
        "keywords": ["murder", "death", "life imprisonment", "fine"],
        "description": "Defines murder and provides punishment of death or life imprisonment along with liability to fine"
    },
    "Section 301": {
        "keywords": ["causing death", "intent", "knowledge", "imprisonment"],
        "description": "Provides punishment for causing death by act done with intention or knowledge that it is likely to cause death"
    },
    "Section 302": {
        "keywords": ["punishment", "murder", "death", "life imprisonment", "fine"],
        "description": "Punishes murder with death or life imprisonment, along with fine"
    },
    "Section 303": {
        "keywords": ["death", "abetment", "suicide", "punishment", "death", "imprisonment", "fine"],
        "description": "Punishes abetment of suicide of child or insane person with death or life imprisonment and fine or imprisonment"
    },
    "Section 304": {
        "keywords": ["punishment", "culpable homicide", "imprisonment", "fine"],
        "description": "Provides punishment for culpable homicide not amounting to murder, with imprisonment up to 10 years, fine, or both"
    },
    "Section 304A": {
        "keywords": ["causing death", "rash or negligent act", "imprisonment", "fine"],
        "description": "Punishes causing death by rash or negligent act with imprisonment up to 2 years, fine, or both"
    },
    "Section 305": {
        "keywords": ["abetment", "suicide", "minor", "imprisonment", "fine"],
        "description": "Punishes abetment of suicide of minor or insane person, with imprisonment up to 10 years, fine, or both"
    },
    "Section 306": {
        "keywords": ["abetment", "suicide", "imprisonment", "fine"],
        "description": "Punishes abetment of suicide with imprisonment up to 10 years, fine, or both"
    },
    "Section 307": {
        "keywords": ["attempt to murder", "imprisonment", "fine"],
        "description": "Punishes attempt to murder with imprisonment up to 10 years, fine, or both"
    },
    "Section 308": {
        "keywords": ["attempt to commit", "culpable homicide", "imprisonment", "fine"],
        "description": "Punishes attempt to commit culpable homicide not amounting to murder with imprisonment up to 3 years, fine, or both"
    },
    "Section 309": {
        "keywords": ["attempt to commit", "suicide", "punishment", "fine"],
        "description": "Punishes attempt to commit suicide with imprisonment up to 1 year, fine, or both"
    },
    "Section 310": {
        "keywords": ["abetment", "punishment", "attempt to commit", "suicide", "imprisonment"],
        "description": "Punishes abetment of attempt to commit suicide, with imprisonment up to 1 year, or fine, or both"
    },
    "Section 311": {
        "keywords": ["person under 18 years", "committing", "offence", "imprisonment"],
        "description": "Provides that person under 18 years of age can't be punished with imprisonment if committing offence under this Code"
    },
    "Section 312": {
        "keywords": ["causing miscarriage", "woman", "intent", "imprisonment", "fine"],
        "description": "Punishes causing miscarriage of woman with imprisonment up to 3 years, fine, or both"
    },
    "Section 313": {
        "keywords": ["causing miscarriage", "woman", "quickening", "imprisonment", "fine"],
        "description": "Punishes causing miscarriage of woman with quickening with imprisonment up to 7 years, fine, or both"
    },
    "Section 314": {
        "keywords": ["death of quick child", "quickening", "woman", "intent", "imprisonment", "fine"],
        "description": "Punishes causing death of quick child by act amounting to culpable homicide, with imprisonment up to 10 years, fine, or both"
    },
    "Section 315": {
        "keywords": ["act done", "intent", "prevent child being born alive", "imprisonment", "fine"],
        "description": "Punishes act done with intent to prevent child being born alive or to cause it to die after birth with imprisonment up to 10 years, fine, or both"
    },
    "Section 316": {
        "keywords": ["causing death", "child", "concealment of birth", "imprisonment", "fine"],
        "description": "Punishes causing death of quick child by wilfully neglecting to cause death of any child under 12 years of age whose death is caused by act or omission"
    },
    "Section 317": {
        "keywords": ["exposure", "abandonment", "child under 12 years", "imprisonment", "fine"],
        "description": "Punishes exposure or abandonment of child under 12 years by parent or person having care of it with imprisonment up to 7 years, fine, or both"
    },
    "Section 318": {
        "keywords": ["concealment", "birth by secret disposal", "imprisonment", "fine"],
        "description": "Punishes concealment of birth by secret disposal of dead body with imprisonment up to 2 years, fine, or both"
    },
    "Section 319": {
        "keywords": ["hurt", "cause", "intention", "knowledge", "imprisonment", "fine"],
        "description": "Defines hurt as causing bodily pain, disease or infirmity to any person and prescribes punishment for it"
    },
    "Section 320": {
        "keywords": ["grievous hurt", "intention", "knowledge", "imprisonment"],
        "description": "Defines grievous hurt and prescribes punishment for it, including permanent privation of sight, hearing, etc."
    },
    "Section 321": {
        "keywords": ["voluntarily causing hurt", "punishment", "intention", "knowledge", "imprisonment"],
        "description": "Provides punishment for voluntarily causing hurt, with imprisonment up to 1 year, fine, or both"
    },
    "Section 322": {
        "keywords": ["voluntarily causing grievous hurt", "punishment", "intention", "knowledge", "imprisonment"],
        "description": "Provides punishment for voluntarily causing grievous hurt, with imprisonment up to 7 years, fine, or both"
    },
    "Section 323": {
        "keywords": ["voluntarily causing hurt", "simple hurt", "punishment", "intention", "knowledge", "imprisonment"],
        "description": "Provides punishment for voluntarily causing hurt, with imprisonment up to 1 year, fine, or both"
    },
    "Section 324": {
        "keywords": ["voluntarily causing hurt", "dangerous weapon", "punishment", "intention", "knowledge", "imprisonment"],
        "description": "Provides punishment for voluntarily causing hurt by dangerous weapons or means, with imprisonment up to 3 years, fine, or both"
    },
    "Section 325": {
        "keywords": ["voluntarily causing grievous hurt", "dangerous weapon", "punishment", "intention", "knowledge", "imprisonment"],
        "description": "Provides punishment for voluntarily causing grievous hurt by dangerous weapons or means, with imprisonment up to 7 years, fine, or both"
    },
    "Section 326": {
        "keywords": ["voluntarily causing grievous hurt", "dangerous weapon", "punishment", "intention", "knowledge", "imprisonment"],
        "description": "Provides punishment for voluntarily causing grievous hurt by dangerous weapons or means, with imprisonment up to 10 years, fine, or both"
    },
    "Section 326A": {
        "keywords": ["acid attack", "intention", "knowledge", "imprisonment", "fine"],
        "description": "Punishes acid attack causing permanent or partial damage or deformity to any part of the body with imprisonment up to 7 years, fine, or both"
    },
    "Section 326B": {
        "keywords": ["acid attack", "compensation", "court"],
        "description": "Provides for compensation to victims of acid attacks on orders of the court"
    },
    "Section 327": {
        "keywords": ["voluntarily causing hurt", "endangering life", "imprisonment", "fine"],
        "description": "Punishes voluntarily causing hurt to extort confession or to compel restoration of property or to gratify vicious or other unlawful motives, with imprisonment up to 7 years, fine, or both"
    },
    "Section 328": {
        "keywords": ["causing hurt", "preparation", "sale", "imprisonment", "fine"],
        "description": "Punishes causing hurt by means of poison, etc. with intent to commit offence, with imprisonment up to 10 years, fine, or both"
    },
    "Section 329": {
        "keywords": ["causing grievous hurt", "preparation", "sale", "imprisonment", "fine"],
        "description": "Punishes causing grievous hurt by means of poison, etc. with intent to commit offence, with imprisonment up to life, fine, or both"
    },
    "Section 330": {
        "keywords": ["voluntarily causing hurt", "imprisonment", "fine"],
        "description": "Punishes voluntarily causing hurt to extort confession or to compel restoration of property or to gratify vicious or other unlawful motives, with imprisonment up to 3 years, fine, or both"
    },
    "Section 331": {
        "keywords": ["causing hurt", "grievous hurt", "poisoning", "imprisonment", "fine"],
        "description": "Punishes causing hurt or grievous hurt by poisoning with intent to commit or facilitate offence, with imprisonment up to life, fine, or both"
    },
    "Section 332": {
        "keywords": ["hurt", "voluntarily causing hurt to deter", "public servant", "imprisonment", "fine"],
        "description": "Punishes voluntarily causing hurt to deter public servant from duty or in consequence of the execution of his duty, with imprisonment up to 3 years, fine, or both"
    },
    "Section 333": {
        "keywords": ["grievous hurt", "voluntarily causing grievous hurt to deter", "public servant", "imprisonment", "fine"],
        "description": "Punishes voluntarily causing grievous hurt to deter public servant from duty or in consequence of the execution of his duty, with imprisonment up to 10 years, fine, or both"
    },
    "Section 334": {
        "keywords": ["hurt", "voluntarily causing hurt on provocation", "imprisonment", "fine"],
        "description": "Punishes voluntarily causing hurt on grave and sudden provocation, with imprisonment up to 1 year, fine, or both"
    },
    "Section 335": {
        "keywords": ["grievous hurt", "voluntarily causing grievous hurt on provocation", "imprisonment", "fine"],
        "description": "Punishes voluntarily causing grievous hurt on grave and sudden provocation, with imprisonment up to 4 years, fine, or both"
    },
    "Section 336": {
        "keywords": ["act endangering life", "personal safety of others", "imprisonment", "fine"],
        "description": "Punishes act endangering life or personal safety of others with imprisonment up to 3 months, or fine up to Rs. 250, or both"
    },
    "Section 337": {
        "keywords": ["act endangering life", "personal safety of others", "imprisonment", "fine"],
        "description": "Punishes act endangering life or personal safety of others with imprisonment up to 6 months, or fine up to Rs. 500, or both"
    },
    "Section 338": {
        "keywords": ["act endangering life", "personal safety of others", "imprisonment", "fine"],
        "description": "Punishes act endangering life or personal safety of others with imprisonment up to 2 years, or fine, or both"
    },
    "Section 339": {
        "keywords": ["act endangering safety of others", "using", "dangerous", "imprisonment", "fine"],
        "description": "Punishes act endangering safety of others by using any dangerous weapon or other means, with imprisonment up to 6 months, or fine up to Rs. 500, or both"
    },
    "Section 340": {
        "keywords": ["wrongful confinement", "imprisonment", "fine"],
        "description": "Punishes wrongful confinement with imprisonment up to 1 year, or fine up to Rs. 1000, or both"
    },
    "Section 341": {
        "keywords": ["wrongful restraint", "imprisonment", "fine"],
        "description": "Punishes wrongful restraint with imprisonment up to 1 month, or fine up to Rs. 500, or both"
    },
    "Section 342": {
        "keywords": ["wrongful confinement", "10 days", "imprisonment", "fine"],
        "description": "Punishes wrongful confinement for over 10 days with imprisonment up to 2 years, or fine, or both"
    },
    "Section 343": {
        "keywords": ["wrongful confinement", "3 days", "imprisonment", "fine"],
        "description": "Punishes wrongful confinement for 3 days or more, with imprisonment up to 1 year, or fine up to Rs. 1000, or both"
    },
    "Section 344": {
        "keywords": ["wrongful confinement", "escape", "imprisonment", "fine"],
        "description": "Punishes wrongful confinement for the purpose of compelling restoration of property or discharge of debt with imprisonment up to 3 years, or fine, or both"
    },
    "Section 345": {
        "keywords": ["wrongful confinement", "excess of", "10 days", "imprisonment", "fine"],
        "description": "Punishes wrongful confinement for more than 10 days with excessive cruelty with imprisonment up to 2 years, or fine, or both"
    },
    "Section 346": {
        "keywords": ["wrongful confinement", "over 3 days", "female", "imprisonment", "fine"],
        "description": "Punishes wrongful confinement of a woman for over 3 days with imprisonment up to 2 years, or fine, or both"
    },
    "Section 347": {
        "keywords": ["wrongful confinement", "over 10 days", "certain circumstances", "imprisonment", "fine"],
        "description": "Punishes wrongful confinement for over 10 days under certain circumstances with imprisonment up to 3 years, or fine, or both"
    },
    "Section 348": {
        "keywords": ["wrongful confinement", "death", "imprisonment", "fine"],
        "description": "Punishes wrongful confinement for the purpose of extortion or to commit robbery or wrongfully confining a person who has been abducted, with imprisonment up to 2 years, or fine, or both"
    },
    "Section 349": {
        "keywords": ["punishment", "force", "certain circumstances", "imprisonment", "fine"],
        "description": "Provides punishment for using force for an act in certain circumstances, with imprisonment up to 3 months, or fine up to Rs. 500, or both"
    },
    "Section 350": {
        "keywords": ["use of criminal force", "certain circumstances", "imprisonment", "fine"],
        "description": "Provides punishment for using criminal force in certain circumstances, with imprisonment up to 3 months, or fine up to Rs. 500, or both"
    },
    "Section 351": {
        "keywords": ["assault", "criminal force", "imprisonment", "fine"],
        "description": "Punishes assault with criminal force with imprisonment up to 3 months, or fine up to Rs. 500, or both"
    },
    "Section 352": {
        "keywords": ["assault", "fine"],
        "description": "Punishes assault or criminal force with fine"
    },
    "Section 353": {
        "keywords": ["assault or criminal force to deter public servant", "imprisonment", "fine"],
        "description": "Punishes assault or criminal force to deter public servant from duty, with imprisonment up to 2 years, or fine, or both"
    },
    "Section 354": {
        "keywords": ["assault or criminal force to woman with intent to outrage her modesty", "imprisonment", "fine"],
        "description": "Punishes assault or criminal force to woman with intent to outrage her modesty, with imprisonment up to 2 years, or fine, or both"
    },
    "Section 354A": {
        "keywords": ["sexual harassment", "punishment", "imprisonment", "fine"],
        "description": "Punishes sexual harassment with imprisonment up to 3 years, or fine, or both"
    },
    "Section 354B": {
        "keywords": ["assault or use of criminal force with intent to disrobe woman", "punishment", "imprisonment", "fine"],
        "description": "Punishes assault or use of criminal force with intent to disrobe woman, with imprisonment up to 3 years, or fine, or both"
    },
    "Section 354C": {
        "keywords": ["voyeurism", "imprisonment", "fine"],
        "description": "Punishes voyeurism with imprisonment up to 3 years, or fine, or both"
    },
    "Section 354D": {
        "keywords": ["stalking", "punishment", "imprisonment", "fine"],
        "description": "Punishes stalking with imprisonment up to 3 years, or fine, or both"
    },
    "Section 355": {
        "keywords": ["assault or criminal force with intent to dishonor person", "punishment", "imprisonment", "fine"],
        "description": "Punishes assault or criminal force with intent to dishonor person, otherwise than on grave and sudden provocation, with imprisonment up to 2 years, or fine, or both"
    },
    "Section 356": {
        "keywords": ["assault or criminal force in attempt to commit theft of property", "punishment", "imprisonment", "fine"],
        "description": "Punishes assault or criminal force in attempt to commit theft of property with imprisonment up to 3 years, or fine, or both"
    },
    "Section 357": {
        "keywords": ["assault or criminal force in attempt to commit theft", "fine"],
        "description": "Punishes assault or criminal force in attempt to commit theft with fine"
    },
    "Section 358": {
        "keywords": ["assault", "criminal force in attempt to commit theft of property carried by a person", "punishment", "imprisonment", "fine"],
        "description": "Punishes assault or criminal force in attempt to commit theft of property carried by a person with imprisonment up to 7 years, or fine, or both"
    },
    "Section 359": {
        "keywords": ["kidnapping", "abduction", "punishment", "imprisonment", "fine"],
        "description": "Punishes kidnapping or abduction with imprisonment up to 7 years, or fine, or both"
    },
    "Section 360": {
        "keywords": ["kidnapping", "abduction", "incapable of giving consent", "fine"],
        "description": "Provides for punishment for kidnapping or abduction of person with intent to cause that person to be secretly or wrongfully confined, with fine"
    },
    "Section 361": {
        "keywords": ["kidnapping from lawful guardianship", "fine"],
        "description": "Provides punishment for kidnapping from lawful guardianship with fine"
    },
    "Section 362": {
        "keywords": ["abduction", "enticing", "decoying", "fine"],
        "description": "Punishes abduction by enticing or decoying a person with fine"
    },
    "Section 363": {
        "keywords": ["kidnapping", "fine"],
        "description": "Punishes kidnapping with fine"
    },
    "Section 363A": {
        "keywords": ["making sexual advances", "fine"],
        "description": "Provides for punishment for making sexual advances with fine"
    },
    "Section 364": {
        "keywords": ["kidnapping or abducting in order to murder", "fine"],
        "description": "Punishes kidnapping or abducting in order to murder with fine"
    },
    "Section 364A": {
        "keywords": ["kidnapping for ransom", "murder", "punishment", "imprisonment", "fine"],
        "description": "Punishes kidnapping for ransom, etc. with imprisonment up to life or death, or fine"
    },
    "Section 365": {
        "keywords": ["kidnapping or abducting with intent secretly and wrongfully to confine person", "fine"],
        "description": "Punishes kidnapping or abducting with intent secretly and wrongfully to confine person with fine"
    },
    "Section 365A": {
        "keywords": ["procuration of minor girl", "induce illicit intercourse", "punishment", "imprisonment", "fine"],
        "description": "Punishes procuration of minor girl with imprisonment up to 10 years, or fine, or both"
    },
    "Section 366": {
        "keywords": ["kidnapping", "abducting or inducing woman to compel her marriage", "fine"],
        "description": "Punishes kidnapping, abducting or inducing woman to compel her marriage, etc. with fine"
    },
    "Section 366A": {
        "keywords": ["procuration of minor girl", "fine"],
        "description": "Provides punishment for procuration of minor girl with fine"
    },
    "Section 366B": {
        "keywords": ["importation of girl from foreign country", "fine"],
        "description": "Provides punishment for importation of girl from foreign country with fine"
    },
    "Section 367": {
        "keywords": ["kidnapping or abducting", "fine"],
        "description": "Punishes kidnapping or abducting with fine"
    },
    "Section 368": {
        "keywords": ["wrongfully concealing or keeping in confinement", "kidnapped or abducted person", "fine"],
        "description": "Punishes wrongfully concealing or keeping in confinement kidnapped or abducted person with fine"
    },
    "Section 369": {
        "keywords": ["kidnapping or abducting child under 10 years with intent to steal from its person", "fine"],
        "description": "Punishes kidnapping or abducting child under 10 years with intent to steal from its person with fine"
    },
    "Section 370": {
        "keywords": ["trafficking of person", "exploitation", "punishment", "imprisonment", "fine"],
        "description": "Punishes trafficking of person for exploitation with imprisonment up to 10 years, or fine, or both"
    },
    "Section 370A": {
        "keywords": ["trafficking of minor", "punishment", "imprisonment", "fine"],
        "description": "Punishes trafficking of minor with imprisonment up to 7 years, or fine, or both"
    },
    "Section 371": {
        "keywords": ["habitual dealing in slaves", "punishment", "imprisonment", "fine"],
        "description": "Punishes habitual dealing in slaves with imprisonment up to 10 years, or fine, or both"
    },
    "Section 372": {
        "keywords": ["selling minor for purpose of prostitution", "punishment", "imprisonment", "fine"],
        "description": "Punishes selling minor for the purpose of prostitution, etc. with imprisonment up to 10 years, or fine, or both"
    },
    "Section 373": {
        "keywords": ["buying minor for purpose of prostitution", "punishment", "imprisonment", "fine"],
        "description": "Punishes buying minor for the purpose of prostitution, etc. with imprisonment up to 10 years, or fine, or both"
    },
    "Section 374": {
        "keywords": ["unlawful compulsory labour", "punishment", "imprisonment", "fine"],
        "description": "Punishes unlawful compulsory labour with imprisonment up to 1 year, or fine, or both"
    },
    "Section 375": {
        "keywords": ["rape", "punishment", "imprisonment", "fine"],
        "description": "Defines rape and prescribes punishment for it, including imprisonment for life, and fine or without fine"
    },
    "Section 376": {
        "keywords": ["rape", "punishment", "imprisonment", "fine"],
        "description": "Punishes rape with imprisonment for life, or with imprisonment for a term which may extend to ten years, and shall also be liable to fine, unless the woman raped is his own wife, and is not under twelve years of age, in which cases, he shall be punished with imprisonment of either description for a term which may extend to two years, or with fine, or with both"
    },
    "Section 376A": {
        "keywords": ["causing death or vegetative state of victim", "punishment", "imprisonment", "fine"],
        "description": "Punishes causing death or resulting in a persistent vegetative state of victim in case of rape, with imprisonment for life or with imprisonment of either description for a term which may extend to twenty years, and shall also be liable to fine or without fine"
    },
    "Section 376AB": {
        "keywords": ["rape on woman under twelve years of age", "punishment", "death"],
        "description": "Punishes rape on woman under twelve years of age with death"
    },
    "Section 376B": {
        "keywords": ["intercourse by public servant with woman in his custody", "fine"],
        "description": "Provides for punishment for intercourse by public servant with a woman in his custody with fine"
    },
    "Section 376C": {
        "keywords": ["intercourse by superintendent of jail, remand home, etc.", "fine"],
        "description": "Provides for punishment for intercourse by superintendent of jail, remand home, etc. with fine"
    },
    "Section 376D": {
        "keywords": ["gang rape", "punishment", "imprisonment", "fine"],
        "description": "Punishes gang rape with imprisonment for life, or with imprisonment for a term which shall not be less than twenty years, but which may be for life, which shall mean the remainder of that person’s natural life, and shall also be liable to fine"
    },
    "Section 376DA": {
        "keywords": ["gang rape on woman under sixteen years of age", "punishment", "death"],
        "description": "Punishes gang rape on woman under sixteen years of age with death"
    },
    "Section 376DB": {
        "keywords": ["rape on woman under sixteen years of age", "punishment", "death"],
        "description": "Punishes rape on woman under sixteen years of age with death"
    },
    "Section 376E": {
        "keywords": ["repeated rape", "punishment", "death"],
        "description": "Provides for punishment for repeated rape with death"
    },
    "Section 377": {
        "keywords": ["unnatural offences", "fine", "imprisonment"],
        "description": "Punishes unnatural offences with imprisonment for life, or with imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine"
    },
    "Section 378": {
        "keywords": ["theft", "punishment", "fine"],
        "description": "Punishes theft with imprisonment of either description for a term which may extend to three years, or with fine, or with both"
    },
    "Section 379": {
        "keywords": ["theft", "punishment", "imprisonment", "fine"],
        "description": "Punishes theft with imprisonment of either description for a term which may extend to seven years, or with fine, or with both"
    },
    "Section 380": {
        "keywords": ["theft in dwelling house", "punishment", "imprisonment", "fine"],
        "description": "Punishes theft in dwelling house with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine"
    },
    "Section 381": {
        "keywords": ["theft by clerk or servant", "punishment", "imprisonment", "fine"],
        "description": "Punishes theft by clerk or servant of property in possession of master, with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine"
    },
    "Section 382": {
        "keywords": ["theft after preparation made for causing death, hurt or restraint", "punishment", "imprisonment", "fine"],
        "description": "Punishes theft after preparation made for causing death, hurt or restraint, with imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine"
    },
    "Section 383": {
        "keywords": ["extortion", "punishment", "imprisonment", "fine"],
        "description": "Punishes extortion with imprisonment of either description for a term which may extend to three years, or with fine, or with both"
    },
    "Section 384": {
        "keywords": ["extortion", "punishment", "imprisonment", "fine"],
        "description": "Punishes extortion with imprisonment of either description for a term which may extend to seven years, or with fine, or with both"
    },
    "Section 385": {
        "keywords": ["putting person in fear of injury in order to commit extortion", "punishment", "imprisonment", "fine"],
        "description": "Punishes putting person in fear of injury in order to commit extortion with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine"
    },
    "Section 386": {
        "keywords": ["extortion by putting person in fear of death or grievous hurt", "punishment", "imprisonment", "fine"],
        "description": "Punishes extortion by putting person in fear of death or grievous hurt with imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine"
    },
    "Section 387": {
        "keywords": ["putting person in fear of death or of grievous hurt", "in order to commit extortion", "punishment", "imprisonment", "fine"],
        "description": "Punishes putting person in fear of death or of grievous hurt in order to commit extortion with imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine"
    },
    "Section 388": {
        "keywords": ["extortion by threat of accusation of an offence", "punishment", "imprisonment", "fine"],
        "description": "Punishes extortion by threat of accusation of an offence punishable with death or imprisonment for life, etc. with imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine"
    },
    "Section 389": {
        "keywords": ["putting person in fear of accusation of offence", "punishment", "imprisonment", "fine"],
        "description": "Punishes putting person in fear of accusation of an offence punishable with death or imprisonment for life, etc. with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine"
    },
    "Section 390": {
        "keywords": ["robbery", "punishment", "imprisonment", "fine"],
        "description": "Punishes robbery with imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine"
    },
    "Section 391": {
        "keywords": ["dacoity", "fine"],
        "description": "Punishes dacoity with imprisonment for life, or with imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine"
    },
    "Section 392": {
        "keywords": ["robbery", "punishment", "imprisonment", "fine"],
        "description": "Punishes robbery with imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine"
    },
    "Section 393": {
        "keywords": ["attempt to commit robbery", "punishment", "imprisonment", "fine"],
        "description": "Punishes attempt to commit robbery with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine"
    },
    "Section 394": {
        "keywords": ["voluntarily causing hurt in committing robbery", "punishment", "imprisonment", "fine"],
        "description": "Punishes voluntarily causing hurt in committing robbery with imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine"
    },
    "Section 395": {
        "keywords": ["dacoity with murder", "punishment", "imprisonment", "fine"],
        "description": "Punishes dacoity with murder with imprisonment for life, or with imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine"
    },
    "Section 396": {
        "keywords": ["dacoity with murder of any person", "punishment", "death"],
        "description": "Punishes dacoity with murder of any person with death or with imprisonment for life, and shall also be liable to fine"
    },
    "Section 397": {
        "keywords": ["robbery or dacoity, with attempt to cause death or grievous hurt", "punishment", "imprisonment", "fine"],
        "description": "Punishes robbery or dacoity, with attempt to cause death or grievous hurt, with imprisonment for life, or with imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine"
    },
    "Section 398": {
        "keywords": ["attempt to commit robbery or dacoity", "punishment", "imprisonment", "fine"],
        "description": "Punishes attempt to commit robbery or dacoity, when armed with deadly weapon, with imprisonment for life, or with imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine"
    },
    "Section 399": {
        "keywords": ["making preparation to commit dacoity", "punishment", "imprisonment", "fine"],
        "description": "Punishes making preparation to commit dacoity with imprisonment for life, or with imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine"
    },
    "Section 400": {
        "keywords": ["belonging to gang of dacoits", "punishment", "imprisonment", "fine"],
        "description": "Punishes belonging to a gang of dacoits with imprisonment for life, or with imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine"
    },
    "Section 401": {
        "keywords": ["punishment for belonging to gang of thieves", "punishment", "imprisonment", "fine"],
        "description": "Punishes belonging to a gang of thieves with imprisonment for life, or with imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine"
    },
    "Section 402": {
        "keywords": ["assembling for purpose of committing dacoity", "punishment", "imprisonment", "fine"],
        "description": "Punishes assembling for the purpose of committing dacoity with imprisonment for life, or with imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine"
    },
    "Section 402A": {
        "keywords": ["gang preparing to commit dacoity", "punishment", "imprisonment", "fine"],
        "description": "Punishes gang preparing to commit dacoity with imprisonment for life, or with imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine"
    },
    "Section 403": {
        "keywords": ["dishonest misappropriation of property", "punishment", "imprisonment", "fine"],
        "description": "Punishes dishonest misappropriation of property with imprisonment of either description for a term which may extend to two years, or with fine, or with both"
    },
    "Section 404": {
        "keywords": ["dishonest misappropriation of property possessed by deceased person", "punishment", "imprisonment", "fine"],
        "description": "Punishes dishonest misappropriation of property possessed by deceased person at the time of his death with imprisonment of either description for a term which may extend to three years, or with fine, or with both"
    },
    "Section 405": {
        "keywords": ["criminal breach of trust", "punishment", "imprisonment", "fine"],
        "description": "Punishes criminal breach of trust with imprisonment of either description for a term which may extend to three years, or with fine, or with both"
    },
    "Section 406": {
        "keywords": ["criminal breach of trust by clerk or servant", "punishment", "imprisonment", "fine"],
        "description": "Punishes criminal breach of trust by clerk or servant with imprisonment of either description for a term which may extend to seven years, or with fine, or with both"
    },
    "Section 407": {
        "keywords": ["criminal breach of trust by carrier, etc.", "punishment", "imprisonment", "fine"],
        "description": "Punishes criminal breach of trust by carrier, etc. with imprisonment of either description for a term which may extend to ten years, or with fine, or with both"
    },
    "Section 408": {
        "keywords": ["criminal breach of trust by clerk or servant", "punishment", "imprisonment", "fine"],
        "description": "Punishes criminal breach of trust by clerk or servant with imprisonment of either description for a term which may extend to seven years, or with fine, or with both"
    },
    "Section 409": {
        "keywords": ["criminal breach of trust by public servant, or by banker, merchant or agent", "punishment", "imprisonment", "fine"],
        "description": "Punishes criminal breach of trust by public servant, or by banker, merchant or agent, etc. with imprisonment of either description for a term which may extend to ten years, or with fine, or with both"
    },
    "Section 410": {
        "keywords": ["stolen property", "receiving stolen property knowing it to be stolen", "punishment", "imprisonment", "fine"],
        "description": "Punishes receiving stolen property knowing it to be stolen with imprisonment of either description for a term which may extend to three years, or with fine, or with both"
    },
    "Section 411": {
        "keywords": ["dishonestly receiving stolen property", "punishment", "imprisonment", "fine"],
        "description": "Punishes dishonestly receiving stolen property with imprisonment of either description for a term which may extend to three years, or with fine, or with both"
    },
    "Section 412": {
        "keywords": ["dishonestly receiving property stolen in commission of dacoity", "punishment", "imprisonment", "fine"],
        "description": "Punishes dishonestly receiving property stolen in commission of dacoity with imprisonment of either description for a term which may extend to seven years, or with fine, or with both"
    },
    "Section 413": {
        "keywords": ["habitually dealing in stolen property", "punishment", "imprisonment", "fine"],
        "description": "Punishes habitually dealing in stolen property with imprisonment of either description for a term which may extend to seven years, or with fine, or with both"
    },
    "Section 414": {
        "keywords": ["assisting in concealment of stolen property", "punishment", "imprisonment", "fine"],
        "description": "Punishes assisting in concealment of stolen property with imprisonment of either description for a term which may extend to three years, or with fine, or with both"
    },
    "Section 415": {
        "keywords": ["cheating", "punishment", "imprisonment", "fine"],
        "description": "Punishes cheating with imprisonment of either description for a term which may extend to one year, or with fine, or with both"
    },
    "Section 416": {
        "keywords": ["cheating by personation", "punishment", "imprisonment", "fine"],
        "description": "Punishes cheating by personation with imprisonment of either description for a term which may extend to three years, or with fine, or with both"
    },
    "Section 417": {
        "keywords": ["punishment for cheating", "punishment", "imprisonment", "fine"],
        "description": "Punishes punishment for cheating with imprisonment of either description for a term which may extend to one year, or with fine, or with both"
    },
    "Section 418": {
        "keywords": ["cheating with knowledge that wrongful loss may ensue to person whose interest offender is bound to protect", "punishment", "imprisonment", "fine"],
        "description": "Punishes cheating with knowledge that wrongful loss may ensue to person whose interest offender is bound to protect with imprisonment of either description for a term which may extend to three years, or with fine, or with both"
    },
    "Section 419": {
        "keywords": ["punishment for cheating by personation", "punishment", "imprisonment", "fine"],
        "description": "Punishes punishment for cheating by personation with imprisonment of either description for a term which may extend to three years, or with fine, or with both"
    },
    "Section 420": {
        "keywords": ["cheating and dishonestly inducing delivery of property", "punishment", "imprisonment", "fine"],
        "description": "Punishes cheating and dishonestly inducing delivery of property with imprisonment of either description for a term which may extend to seven years, or with fine, or with both"
    },
    "Section 421": {
        "keywords": ["dishonest or fraudulent removal or concealment of property", "punishment", "imprisonment", "fine"],
        "description": "Punishes dishonest or fraudulent removal or concealment of property with imprisonment of either description for a term which may extend to three years, or with fine, or with both"
    },
    "Section 422": {
        "keywords": ["dishonestly or fraudulently preventing debt being available for creditors", "punishment", "imprisonment", "fine"],
        "description": "Punishes dishonestly or fraudulently preventing debt being available for creditors with imprisonment of either description for a term which may extend to three years, or with fine, or with both"
    },
    "Section 423": {
        "keywords": ["dishonest or fraudulent execution of deed of transfer containing false statement of consideration", "punishment", "imprisonment", "fine"],
        "description": "Punishes dishonest or fraudulent execution of deed of transfer containing false statement of consideration with imprisonment of either description for a term which may extend to three years, or with fine, or with both"
    },
    "Section 424": {
        "keywords": ["dishonest or fraudulent removal or concealment of property to prevent distribution among creditors", "punishment", "imprisonment", "fine"],
        "description": "Punishes dishonest or fraudulent removal or concealment of property to prevent distribution among creditors with imprisonment of either description for a term which may extend to three years, or with fine, or with both"
    },
    "Section 425": {
        "keywords": ["mischief", "punishment", "imprisonment", "fine"],
        "description": "Punishes mischief with imprisonment of either description for a term which may extend to three months, or with fine, or with both"
    },
    "Section 426": {
        "keywords": ["punishment for mischief", "imprisonment", "fine"],
        "description": "Punishes punishment for mischief with imprisonment of either description for a term which may extend to one year, or with fine, or with both"
    },
    "Section 427": {
        "keywords": ["mischief", "punishment", "imprisonment", "fine"],
        "description": "Punishes mischief with imprisonment of either description for a term which may extend to two years, or with fine, or with both"
    },
    "Section 428": {
        "keywords": ["mischief by killing or maiming animal of value of ten rupees", "punishment", "imprisonment", "fine"],
        "description": "Punishes mischief by killing or maiming animal of value of ten rupees with imprisonment of either description for a term which may extend to two years, or with fine, or with both"
    },
    "Section 429": {
        "keywords": ["mischief by killing or maiming cattle, etc., of any value or any animal of the value of fifty rupees", "punishment", "imprisonment", "fine"],
        "description": "Punishes mischief by killing or maiming cattle, etc., of any value or any animal of the value of fifty rupees with imprisonment of either description for a term which may extend to five years, or with fine, or with both"
    },
    "Section 430": {
        "keywords": ["mischief by injury to works of irrigation", "punishment", "imprisonment", "fine"],
        "description": "Punishes mischief by injury to works of irrigation with imprisonment of either description for a term which may extend to ten years, or with fine, or with both"
    },
    "Section 431": {
        "keywords": ["mischief by injury to public road, bridge, river or channel", "punishment", "imprisonment", "fine"],
        "description": "Punishes mischief by injury to public road, bridge, river or channel with imprisonment of either description for a term which may extend to five years, or with fine, or with both"
    },
    "Section 432": {
        "keywords": ["mischief by causing inundation or obstruction to public drainage", "punishment", "imprisonment", "fine"],
        "description": "Punishes mischief by causing inundation or obstruction to public drainage with imprisonment of either description for a term which may extend to five years, or with fine, or with both"
    },
    "Section 433": {
        "keywords": ["punishment for mischief", "imprisonment", "fine"],
        "description": "Punishes punishment for mischief with imprisonment of either description for a term which may extend to two years, or with fine, or with both"
    },
    "Section 434": {
        "keywords": ["mischief by destroying or moving, etc., a landmark fixed by public authority", "punishment", "imprisonment", "fine"],
        "description": "Punishes mischief by destroying or moving, etc., a landmark fixed by public authority with imprisonment of either description for a term which may extend to three years, or with fine, or with both"
    },
    "Section 435": {
        "keywords": ["mischief by fire or explosive substance with intent to cause damage", "punishment", "imprisonment", "fine"],
        "description": "Punishes mischief by fire or explosive substance with intent to cause damage with imprisonment of either description for a term which may extend to ten years, or with fine, or with both"
    },
    "Section 436": {
        "keywords": ["mischief by fire or explosive substance with intent to destroy house, etc.", "punishment", "imprisonment", "fine"],
        "description": "Punishes mischief by fire or explosive substance with intent to destroy house, etc. with imprisonment for life, or with imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine"
    },
    "Section 437": {
        "keywords": ["mischief by destroying or moving, etc., a landmark fixed by public authority", "punishment", "imprisonment", "fine"],
        "description": "Punishes mischief by destroying or moving, etc., a landmark fixed by public authority with imprisonment of either description for a term which may extend to three years, or with fine, or with both"
    },
    "Section 438": {
        "keywords": ["punishment for the mischief described in section 437 committed by fire or any explosive substance", "punishment", "imprisonment", "fine"],
        "description": "Punishes punishment for the mischief described in section 437 committed by fire or any explosive substance with imprisonment for life, or with imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine"
    },
    "Section 439": {
        "keywords": ["criminal trespass", "punishment", "imprisonment", "fine"],
        "description": "Punishes criminal trespass with imprisonment of either description for a term which may extend to three months, or with fine which may extend to five hundred rupees, or with both"
    },
    "Section 440": {
        "keywords": ["punishment for criminal trespass", "punishment", "imprisonment", "fine"],
        "description": "Punishes punishment for criminal trespass with imprisonment of either description for a term which may extend to one year, or with fine which may extend to one thousand rupees, or with both"
    },
    "Section 441": {
        "keywords": ["criminal trespass", "punishment", "imprisonment", "fine"],
        "description": "Punishes criminal trespass with imprisonment of either description for a term which may extend to six months, or with fine which may extend to one thousand rupees, or with both"
    },
    "Section 442": {
        "keywords": ["criminal trespass", "punishment", "imprisonment", "fine"],
        "description": "Punishes criminal trespass with imprisonment of either description for a term which may extend to three months, or with fine which may extend to five hundred rupees, or with both"
    },
    "Section 443": {
        "keywords": ["house-trespass", "punishment", "imprisonment", "fine"],
        "description": "Punishes house-trespass with imprisonment of either description for a term which may extend to one year, or with fine which may extend to one thousand rupees, or with both"
    },
    "Section 444": {
        "keywords": ["house-trespass after preparation for hurt, assault or wrongful restraint", "punishment", "imprisonment", "fine"],
        "description": "Punishes house-trespass after preparation for hurt, assault or wrongful restraint with imprisonment of either description for a term which may extend to three years, or with fine, or with both"
    },
    "Section 445": {
        "keywords": ["house-breaking", "punishment", "imprisonment", "fine"],
        "description": "Punishes house-breaking with imprisonment of either description for a term which may extend to two years, or with fine, or with both"
    },
    "Section 446": {
        "keywords": ["house-breaking by night", "punishment", "imprisonment", "fine"],
        "description": "Punishes house-breaking by night with imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine"
    },
    "Section 447": {
        "keywords": ["punishment for criminal trespass", "punishment", "imprisonment", "fine"],
        "description": "Punishes punishment for criminal trespass with imprisonment of either description for a term which may extend to three months, or with fine which may extend to five hundred rupees, or with both"
    },
    "Section 448": {
        "keywords": ["punishment for house-trespass", "punishment", "imprisonment", "fine"],
        "description": "Punishes punishment for house-trespass with imprisonment of either description for a term which may extend to one year, or with fine which may extend to one thousand rupees, or with both"
    },
    "Section 449": {
        "keywords": ["punishment for house-breaking", "punishment", "imprisonment", "fine"],
        "description": "Punishes punishment for house-breaking with imprisonment of either description for a term which may extend to two years, or with fine, or with both"
    },
    "Section 450": {
        "keywords": ["house-trespass in order to commit offence punishable with imprisonment for life", "punishment", "imprisonment", "fine"],
        "description": "Punishes house-trespass in order to commit offence punishable with imprisonment for life with imprisonment of either description for a term which may extend to two years, or with fine, or with both"
    },
    "Section 451": {
        "keywords": ["house-trespass in order to commit offence punishable with imprisonment", "punishment", "imprisonment", "fine"],
        "description": "Punishes house-trespass in order to commit offence punishable with imprisonment with imprisonment of either description for a term which may extend to two years, or with fine, or with both"
    },
    "Section 452": {
        "keywords": ["house-trespass after preparation for hurt, assault or wrongful restraint", "punishment", "imprisonment", "fine"],
        "description": "Punishes house-trespass after preparation for hurt, assault or wrongful restraint with imprisonment of either description for a term which may extend to three years, or with fine, or with both"
    },
    "Section 453": {
        "keywords": ["punishment for lurking house-trespass or house-breaking", "punishment", "imprisonment", "fine"],
        "description": "Punishes punishment for lurking house-trespass or house-breaking with imprisonment of either description for a term which may extend to two years, or with fine, or with both"
    },
    "Section 454": {
        "keywords": ["lurking house-trespass or house-breaking", "punishment", "imprisonment", "fine"],
        "description": "Punishes lurking house-trespass or house-breaking with imprisonment of either description for a term which may extend to five years, and shall also be liable to fine"
    },
    "Section 455": {
        "keywords": ["lurking house-trespass or house-breaking in order to commit offence punishable with imprisonment", "punishment", "imprisonment", "fine"],
        "description": "Punishes lurking house-trespass or house-breaking in order to commit offence punishable with imprisonment with imprisonment of either description for a term which may extend to five years, and shall also be liable to fine"
    },
    "Section 456": {
        "keywords": ["lurking house-trespass or house-breaking by night in order to commit offence punishable with imprisonment", "punishment", "imprisonment", "fine"],
        "description": "Punishes lurking house-trespass or house-breaking by night in order to commit offence punishable with imprisonment with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine"
    },
    "Section 457": {
        "keywords": ["lurking house-trespass or house-breaking by night in order to commit offence punishable with imprisonment for life", "punishment", "imprisonment", "fine"],
        "description": "Punishes lurking house-trespass or house-breaking by night in order to commit offence punishable with imprisonment for life with imprisonment of either description for a term which may extend to fourteen years, and shall also be liable to fine"
    },
    "Section 458": {
        "keywords": ["lurking house-trespass or house-breaking by night after preparation for hurt, assault or wrongful restraint", "punishment", "imprisonment", "fine"],
        "description": "Punishes lurking house-trespass or house-breaking by night after preparation for hurt, assault or wrongful restraint with imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine"
    },
    "Section 459": {
        "keywords": ["grievous hurt caused whilst committing lurking house-trespass or house-breaking", "punishment", "imprisonment", "fine"],
        "description": "Punishes grievous hurt caused whilst committing lurking house-trespass or house-breaking with imprisonment of either description for a term which may extend to fourteen years, and shall also be liable to fine"
    },
    "Section 460": {
        "keywords": ["all persons jointly concerned in lurking house-trespass or house-breaking by night punishable where death or grievous hurt caused by one of them", "punishment", "imprisonment", "fine"],
        "description": "Punishes all persons jointly concerned in lurking house-trespass or house-breaking by night punishable where death or grievous hurt caused by one of them with imprisonment for life, or with imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine"
    },
    "Section 461": {
        "keywords": ["dishonestly breaking open receptacle containing property", "punishment", "imprisonment", "fine"],
        "description": "Punishes dishonestly breaking open receptacle containing property with imprisonment of either description for a term which may extend to two years, or with fine, or with both"
    },
    "Section 462": {
        "keywords": ["punishment for same offence when committed by person entrusted with custody", "punishment", "imprisonment", "fine"],
        "description": "Punishes punishment for the same offence when committed by person entrusted with custody with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine"
    },
    "Section 463": {
        "keywords": ["forgery", "punishment", "imprisonment", "fine"],
        "description": "Punishes forgery with imprisonment of either description for a term which may extend to two years, or with fine, or with both"
    },
    "Section 464": {
        "keywords": ["making a false document", "punishment", "imprisonment", "fine"],
        "description": "Punishes making a false document with imprisonment of either description for a term which may extend to two years, or with fine, or with both"
    },
    "Section 465": {
        "keywords": ["punishment for forgery", "punishment", "imprisonment", "fine"],
        "description": "Punishes punishment for forgery with imprisonment of either description for a term which may extend to two years, or with fine, or with both"
    },
    "Section 466": {
        "keywords": ["forgery of record of court or of public register, etc.", "punishment", "imprisonment", "fine"],
        "description": "Punishes forgery of record of court or of public register, etc. with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine"
    },
    "Section 467": {
        "keywords": ["forgery of valuable security, will, etc.", "punishment", "imprisonment", "fine"],
        "description": "Punishes forgery of valuable security, will, etc. with imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine"
    },
    "Section 468": {
        "keywords": ["forgery for purpose of cheating", "punishment", "imprisonment", "fine"],
        "description": "Punishes forgery for purpose of cheating with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine"
    },
    "Section 469": {
        "keywords": ["forgery for purpose of harming reputation", "punishment", "imprisonment", "fine"],
        "description": "Punishes forgery for purpose of harming reputation with imprisonment of either description for a term which may extend to three years, and shall also be liable to fine"
    },
    "Section 470": {
        "keywords": ["forged document", "punishment", "imprisonment", "fine"],
        "description": "Punishes forged document with imprisonment of either description for a term which may extend to two years, or with fine, or with both"
    },
    "Section 471": {
        "keywords": ["using as genuine a forged document", "punishment", "imprisonment", "fine"],
        "description": "Punishes using as genuine a forged document with imprisonment of either description for a term which may extend to seven years, or with fine, or with both"
    },
    "Section 472": {
        "keywords": ["making or possessing counterfeit seal, etc., with intent to commit forgery punishable under section 467", "punishment", "imprisonment", "fine"],
        "description": "Punishes making or possessing counterfeit seal, etc., with intent to commit forgery punishable under section 467 with imprisonment of either description for a term which may extend to seven years, or with fine, or with both"
    },
    "Section 473": {
        "keywords": ["making or possessing counterfeit seal, etc., with intent to commit forgery punishable otherwise", "punishment", "imprisonment", "fine"],
        "description": "Punishes making or possessing counterfeit seal, etc., with intent to commit forgery punishable otherwise with imprisonment of either description for a term which may extend to seven years, or with fine, or with both"
    },
    "Section 474": {
        "keywords": ["having possession of document described in section 466 or 467, knowing it to be forged and intending to use it as genuine", "punishment", "imprisonment", "fine"],
        "description": "Punishes having possession of document described in section 466 or 467, knowing it to be forged and intending to use it as genuine with imprisonment of either description for a term which may extend to seven years, or with fine, or with both"
    },
    "Section 475": {
        "keywords": ["counterfeiting device or mark used for authenticating documents described in section 467, or possessing counterfeit marked material", "punishment", "imprisonment", "fine"],
        "description": "Punishes counterfeiting device or mark used for authenticating documents described in section 467, or possessing counterfeit marked material with imprisonment of either description for a term which may extend to three years, or with fine, or with both"
    },
    "Section 476": {
        "keywords": ["counterfeiting device or mark used for authenticating documents other than those described in section 467, or possessing counterfeit marked material", "punishment", "imprisonment", "fine"],
        "description": "Punishes counterfeiting device or mark used for authenticating documents other than those described in section 467, or possessing counterfeit marked material with imprisonment of either description for a term which may extend to three years, or with fine, or with both"
    },
    "Section 477": {
        "keywords": ["fraudulent cancellation, destruction, etc., of will, authority to adopt, or valuable security", "punishment", "imprisonment", "fine"],
        "description": "Punishes fraudulent cancellation, destruction, etc., of will, authority to adopt, or valuable security with imprisonment of either description for a term which may extend to two years, or with fine, or with both"
    },
    "Section 478": {
        "keywords": ["forgeries", "punishment", "imprisonment", "fine"],
        "description": "Punishes forgeries with imprisonment of either description for a term which may extend to three years, or with fine, or with both"
    },
    "Section 479": {
        "keywords": ["selling counterfeit marked material as genuine, etc.", "punishment", "imprisonment", "fine"],
        "description": "Punishes selling counterfeit marked material as genuine, etc. with imprisonment of either description for a term which may extend to three years, or with fine, or with both"
    },
    "Section 480": {
        "keywords": ["using as genuine a forged document", "punishment", "imprisonment", "fine"],
        "description": "Punishes using as genuine a forged document with imprisonment of either description for a term which may extend to seven years, or with fine, or with both"
    },
    "Section 481": {
        "keywords": ["dishonestly using a genuine document as a forged one", "punishment", "imprisonment", "fine"],
        "description": "Punishes dishonestly using a genuine document as a forged one with imprisonment of either description for a term which may extend to three years, or with fine, or with both"
    },
    "Section 482": {
        "keywords": ["punishment for using a false property-mark", "punishment", "imprisonment", "fine"],
        "description": "Punishes punishment for using a false property-mark with imprisonment of either description for a term which may extend to one year, or with fine, or with both"
    },
    "Section 483": {
        "keywords": ["punishment for making use of any such false mark", "punishment", "imprisonment", "fine"],
        "description": "Punishes punishment for making use of any such false mark with imprisonment of either description for a term which may extend to two years, or with fine, or with both"
    },
    "Section 484": {
        "keywords": ["counterfeiting property-mark used by another", "punishment", "imprisonment", "fine"],
        "description": "Punishes counterfeiting property-mark used by another with imprisonment of either description for a term which may extend to one year, or with fine, or with both"
    },
    "Section 485": {
        "keywords": ["making or possession of any instrument for counterfeiting a property-mark", "punishment", "imprisonment", "fine"],
        "description": "Punishes making or possession of any instrument for counterfeiting a property-mark with imprisonment of either description for a term which may extend to two years, or with fine, or with both"
    },
    "Section 486": {
        "keywords": ["selling goods marked with a counterfeit property-mark", "punishment", "imprisonment", "fine"],
        "description": "Punishes selling goods marked with a counterfeit property-mark with imprisonment of either description for a term which may extend to one year, or with fine, or with both"
    },
    "Section 487": {
        "keywords": ["making a false mark upon any receptacle containing goods", "punishment", "imprisonment", "fine"],
        "description": "Punishes making a false mark upon any receptacle containing goods with imprisonment of either description for a term which may extend to two years, or with fine, or with both"
    },
    "Section 488": {
        "keywords": ["making use of any such false mark", "punishment", "imprisonment", "fine"],
        "description": "Punishes making use of any such false mark with imprisonment of either description for a term which may extend to three years, or with fine, or with both"
    },
    "Section 489": {
        "keywords": ["counterfeiting currency-notes or bank-notes", "punishment", "imprisonment", "fine"],
        "description": "Punishes counterfeiting currency-notes or bank-notes with imprisonment of either description for a term which may extend to life, or with fine, or with both"
    },
    "Section 489-A": {
        "keywords": ["selling, buying or using as genuine, forged or counterfeit currency-notes or bank-notes", "punishment", "imprisonment", "fine"],
        "description": "Punishes selling, buying or using as genuine, forged or counterfeit currency-notes or bank-notes with imprisonment for life, or with imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine"
    },
    "Section 489-B": {
        "keywords": ["using as genuine forged or counterfeit currency-notes or bank-notes", "punishment", "imprisonment", "fine"],
        "description": "Punishes using as genuine forged or counterfeit currency-notes or bank-notes with imprisonment of either description for a term which may extend to seven years, or with fine, or with both"
    },
    "Section 489-C": {
        "keywords": ["possession of forged or counterfeit currency-notes or bank-notes", "punishment", "imprisonment", "fine"],
        "description": "Punishes possession of forged or counterfeit currency-notes or bank-notes with imprisonment of either description for a term which may extend to seven years, or with fine, or with both"
    },
    "Section 490": {
        "keywords": ["breach of contract to attend on and supply wants of helpless person", "punishment", "imprisonment", "fine"],
        "description": "Punishes breach of contract to attend on and supply wants of helpless person with imprisonment of either description for a term which may extend to three months, or with fine which may extend to two hundred and fifty rupees, or with both."
    },
    "Section 491": {
        "keywords": ["breach of contract to furnish property for repairs", "punishment", "imprisonment", "fine"],
        "description": "Punishes breach of contract to furnish property for repairs with imprisonment of either description for a term which may extend to three months, or with fine which may extend to two hundred and fifty rupees, or with both."
    },
    "Section 492": {
        "keywords": ["breach of contract to make diversion of property from supply of electric power, water, or light", "punishment", "imprisonment", "fine"],
        "description": "Punishes breach of contract to make diversion of property from supply of electric power, water, or light with imprisonment of either description for a term which may extend to three months, or with fine which may extend to two hundred and fifty rupees, or with both."
    },
    "Section 493": {
        "keywords": ["cohabitation caused by a man deceitfully inducing a belief of lawful marriage", "punishment", "imprisonment", "fine"],
        "description": "Punishes cohabitation caused by a man deceitfully inducing a belief of lawful marriage with imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine."
    },
    "Section 494": {
        "keywords": ["marrying again during lifetime of husband or wife", "punishment", "imprisonment", "fine"],
        "description": "Punishes marrying again during the lifetime of husband or wife with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine."
    },
    "Section 495": {
        "keywords": ["same offence with concealment of former marriage from person with whom subsequent marriage is contracted", "punishment", "imprisonment", "fine"],
        "description": "Punishes the same offence with concealment of former marriage from person with whom subsequent marriage is contracted with imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine."
    },
    "Section 496": {
        "keywords": ["marriage ceremony fraudulently gone through without lawful marriage", "punishment", "imprisonment", "fine"],
        "description": "Punishes marriage ceremony fraudulently gone through without lawful marriage with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine."
    },
    "Section 497": {
        "keywords": ["adultery", "punishment", "imprisonment", "fine"],
        "description": "Punishes adultery with imprisonment of either description for a term which may extend to five years, or with fine, or with both."
    },
    "Section 498": {
        "keywords": ["enticing or taking away or detaining with criminal intent a married woman", "punishment", "imprisonment", "fine"],
        "description": "Punishes enticing or taking away or detaining with criminal intent a married woman with imprisonment of either description for a term which may extend to two years, or with fine, or with both."
    },
    "Section 499": {
        "keywords": ["defamation", "punishment", "imprisonment", "fine"],
        "description": "Punishes defamation with simple imprisonment for a term which may extend to two years, or with fine, or with both."
    },
    "Section 500": {
        "keywords": ["punishment for defamation", "punishment", "imprisonment", "fine"],
        "description": "Punishes punishment for defamation with simple imprisonment for a term which may extend to two years, or with fine, or with both."
    },
    "Section 501": {
        "keywords": ["printing or engraving matter known to be defamatory", "punishment", "imprisonment", "fine"],
        "description": "Punishes printing or engraving matter known to be defamatory with simple imprisonment for a term which may extend to two years, or with fine, or with both."
    },
    "Section 502": {
        "keywords": ["sale of printed or engraved substance containing defamatory matter", "punishment", "imprisonment", "fine"],
        "description": "Punishes sale of printed or engraved substance containing defamatory matter with simple imprisonment for a term which may extend to two years, or with fine, or with both."
    },
    "Section 503": {
        "keywords": ["criminal intimidation", "punishment", "imprisonment", "fine"],
        "description": "Punishes criminal intimidation with imprisonment of either description for a term which may extend to two years, or with fine, or with both."
    },
    "Section 504": {
        "keywords": ["intentional insult with intent to provoke breach of the peace", "punishment", "imprisonment", "fine"],
        "description": "Punishes intentional insult with intent to provoke breach of the peace with imprisonment of either description for a term which may extend to two years, or with fine, or with both."
    },
    "Section 505": {
        "keywords": ["statements conducing to public mischief", "punishment", "imprisonment", "fine"],
        "description": "Punishes statements conducing to public mischief with imprisonment which may extend to three years, or with fine, or with both."
    },
    "Section 506": {
        "keywords": ["punishment for criminal intimidation", "punishment", "imprisonment", "fine"],
        "description": "Punishes punishment for criminal intimidation with imprisonment of either description for a term which may extend to two years, or with fine, or with both."
    },
    "Section 507": {
        "keywords": ["criminal intimidation by an anonymous communication", "punishment", "imprisonment", "fine"],
        "description": "Punishes criminal intimidation by an anonymous communication with imprisonment of either description for a term which may extend to two years, or with fine, or with both."
    },
    "Section 508": {
        "keywords": ["act caused by inducing person to believe that he will be rendered an object of the Divine displeasure", "punishment", "imprisonment", "fine"],
        "description": "Punishes an act caused by inducing person to believe that he will be rendered an object of the Divine displeasure with imprisonment of either description for a term which may extend to one year, or with fine, or with both."
    },
    "Section 509": {
        "keywords": ["word, gesture or act intended to insult the modesty of a woman", "punishment", "imprisonment", "fine"],
        "description": "Punishes word, gesture or act intended to insult the modesty of a woman with imprisonment of either description for a term which may extend to three years, or with fine, or with both."
    },
    "Section 510": {
        "keywords": ["misconduct in public by a drunken person", "punishment", "imprisonment", "fine"],
        "description": "Punishes misconduct in public by a drunken person with imprisonment of either description for a term which may extend to twenty-four hours, or with fine which may extend to ten rupees, or with both."
    },
    "Section 511": {
        "keywords": ["attempt to commit an offence", "punishment", "imprisonment", "fine"],
        "description": "Punishes attempt to commit an offence with punishment provided for the offence."
    },
    "Section 512": {
        "keywords": ["punishment for attempting to commit offences punishable with imprisonment for life or other imprisonment", "punishment", "imprisonment", "fine"],
        "description": "Punishes punishment for attempting to commit offences punishable with imprisonment for life or other imprisonment with imprisonment of either description for a term which may extend to one-half of the longest term provided for the offence, or with such fine as is provided for the offence, or with both."
    }
    # Your penal code data here
}


def detect_ipc_sections(sentence):
    """
    Detect relevant IPC sections based on the provided sentence.
    """
    section_counter = Counter()
    words = re.findall(r'\b\w+\b', sentence)  # Extract words from the sentence
    
    for word in words:
        for section, data in penal_code_data.items():
            description = data["description"]
            if re.search(word, description, re.IGNORECASE):
                section_counter[section] += 1
    
    top_matches = section_counter.most_common(3)
    
    return top_matches

# Test the function
sentence = "someone has made my false document"
top_matches = detect_ipc_sections(sentence)
if top_matches:
    print("Top 3 Matches:")
    for section, count in top_matches:
        description = penal_code_data[section]["description"]
        print(f"{section}")
        print(f"Description: {description}")
else:
    print("No relevant IPC sections found for the sentence.")

    # Your detection logic here

from flask import Flask, render_template,request,jsonify
app= Flask(__name__)

 @app.route('/')
 def index():
    return render_template('index.html')  # Assuming your HTML file is named 'index.html'

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    sentence = data['sentence']
    top_sections = detect_ipc_sections(sentence, penal_code_data)
    # Prepare the sections' descriptions for output
    descriptions = [f"{sec}: {penal_code_data[sec]['description']}" for sec in top_sections]
    return jsonify(descriptions)

if __name__ == '__main__':
    app.run(debug=True)
