from html.parser import HTMLParser

import pickle
import spacy
import os

class Parser(HTMLParser):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.conferences = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'class' and value in ['topic-confr', 'topic-confr ']:
                    self.conferences.append(attrs[0][1])
                    self.get_content = True

    def handle_data(self, data):
        if getattr(self, 'get_content', False):
            # print("Content:", type(data))
            del self.get_content
    
    def get_conferences(self):
        return self.conferences

class Model:
    def __init__(self, model_path):
        super().__init__()
        self.class_cat_map = {
            'Class1': 'cs.CV',
            'Class2': 'cs.LG',
            'Class3': 'stat.ML',
            'Class4': 'cs.AI',
            'Class5': 'eess.IV',
            'Class6': 'cs.RO',
            'Class7': 'cs.CL',
            'Class8': 'cs.GR',
            'Class9': 'cs.NE',
            'Class10': 'cs.CR',
            'Class11': 'math.OC',
            'Class12': 'cs.SI',
            'Class13': 'eess.SP',
            'Class14': 'cs.MM',
            'Class15': 'cs.SY',
            'Class16': 'cs.IR',
            'Class17': 'cs.HC',
            'Class18': 'cs.MA',
            'Class19': 'eess.SY',
            'Class20': 'cs.IT',
            'Class21': 'math.IT',
            'Class22': 'stat.AP',
            'Class23': 'stat.ME',
            'Class24': 'cs.DC',
            'Class25': 'cs.CY',
            'Class26': 'math.ST',
            'Class27': 'stat.TH',
            'Class28': 'q-bio.QM',
            'Class29': 'eess.AS',
            'Class30': 'cs.SD',
            'Class31': 'cs.DS',
            'Class32': 'math.NA',
            'Class33': 'cs.CG',
            'Class34': 'cs.NA',
            'Class35': 'q-bio.NC',
            'Class36': 'I.2.6',
            'Class37': 'stat.CO',
            'Class38': 'physics.comp-ph',
            'Class39': 'physics.chem-ph',
            'Class40': '68T07',
            'Class41': '68T45',
            'Class42': 'physics.data-an',
            'Class43': 'cs.SE',
            'Class44': 'cs.NI',
            'Class45': 'cs.GT',
            'Class46': '68T05',
            'Class47': 'cs.DB',
            'Class48': 'math.PR',
            'Class49': 'q-bio.BM',
            'Class50': 'math.DS',
            'Class51': 'cs.CE',
            'Class52': '68U10',
            'Class53': 'cond-mat.dis-nn',
            'Class54': 'quant-ph',
            'Class55': 'cond-mat.stat-mech',
            'Class56': 'cs.LO',
            'Class57': 'cs.AR',
            'Class58': 'cs.PL',
            'Class59': '68T10',
            'Class60': 'q-fin.ST',
            'Class61': 'cs.DM',
            'Class62': '62H30',
            'Class63': 'cs.PF',
            'Class64': 'I.4.6',
            'Class65': 'I.2.10'
        }
        self.category_table = {
            '62H30': 'Mathematical economics',
            '68T05': 'Computer networks',
            '68T07': 'Computer architecture',
            '68T10': 'Software engineering',
            '68T45': 'Computer graphics',
            '68U10': 'Artificial intelligence',
            'I.2.10': 'Mathematical logic',
            'I.2.6': 'Combinatorics',
            'I.4.6': 'Numerical analysis',
            'cond-mat.dis-nn': 'Disordered systems and neural networks',
            'cond-mat.stat-mech': 'Statistical mechanics',
            'cs.AI': 'Artificial intelligence',
            'cs.AR': 'Algebraic combinatorics',
            'cs.CE': 'Computational complexity',
            'cs.CG': 'Computer graphics',
            'cs.CL': 'Computational linguistics',
            'cs.CR': 'Cryptography and security',
            'cs.CV': 'Computer vision',
            'cs.CY': 'Computers and society',
            'cs.DB': 'Databases',
            'cs.DC': 'Digital circuits',
            'cs.DM': 'Discrete mathematics',
            'cs.DS': 'Data structures',
            'cs.GR': 'Graphics',
            'cs.GT': 'Game theory',
            'cs.HC': 'Hardware',
            'cs.IR': 'Information retrieval',
            'cs.IT': 'Information theory',
            'cs.LG': 'Logic',
            'cs.LO': 'Logic in computer science',
            'cs.MA': 'Machine learning',
            'cs.MM': 'Multimedia',
            'cs.NA': 'Natural language processing',
            'cs.NE': 'Networking',
            'cs.NI': 'Numerical analysis',
            'cs.PF': 'Programming languages',
            'cs.PL': 'Programming languages',
            'cs.RO': 'Robotics',
            'cs.SD': 'Scientific computing',
            'cs.SE': 'Software engineering',
            'cs.SI': 'Systems',
            'cs.SY': 'Systems',
            'eess.AS': 'Audio and speech processing',
            'eess.IV': 'Image and video processing',
            'eess.SP': 'Signal processing',
            'eess.SY': 'Systems',
            'math.DS': 'Discrete mathematics',
            'math.IT': 'Information theory',
            'math.NA': 'Numerical analysis',
            'math.OC': 'Optimization and control',
            'math.PR': 'Probability and statistics',
            'math.ST': 'Statistics',
            'physics.chem-ph': 'Chemical physics',
            'physics.comp-ph': 'Computational physics',
            'physics.data-an': 'Data analysis',
            'q-bio.BM': 'Biomedical engineering',
            'q-bio.NC': 'Computational biology',
            'q-bio.QM': 'Quantum biology',
            'q-fin.ST': 'Financial mathematics',
            'quant-ph': 'Quantum physics',
            'stat.AP': 'Applied statistics',
            'stat.CO': 'Computational statistics',
            'stat.ME': 'Mathematical statistics',
            'stat.ML': 'Machine learning',
            'stat.TH': 'Theoretical statistics'
        }
        self.category_links = {
            'cs.AI': 'https://conferencealert.com/artificial-intelligence.php',
            'cs.CV': 'https://conferencealert.com/image-processing.php',
            'cs.NE': 'https://conferencealert.com/networking.php',
            'cs.RO': 'https://conferencealert.com/robotics.php',
        }
        self.nlp = spacy.load("en_core_web_lg")
        self.model = pickle.load(open(model_path, "rb"))

        print("Model loaded")
    
    
    def preprocess(self, text):
        doc = self.nlp(text)
        filtered_tokens = []
        for token in doc:
            if token.is_stop or token.is_punct or token.text == "\n":
                continue
            filtered_tokens.append(token.lemma_)
        
        return " ".join(filtered_tokens)
    
    def get_classes(self, one_hot):
        res = []
        for i in range(len(one_hot)):
            if one_hot[i] == 0: continue
            
            res.append(self.class_cat_map["Class"+str(i+1)])
        
        return res

    def predict(self, title, abstract):
        vector = self.nlp(self.preprocess(title+" "+abstract)).vector
        classes = self.get_classes(self.model.predict([vector])[0])

        cat_link = []
        for c in classes:
            cat_link.append({self.category_table.get(c):self.category_links.get(c, "https://conferencealert.com/robotics.php")})
        
        return cat_link

