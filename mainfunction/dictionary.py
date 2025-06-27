code_patterns = [
    r"#include\s*<\w+>",   # C/C++ header
    r"int\s+\w+\s*=",      # C/C++/Java variable
    r"def\s+\w+\s*\(",     # Python function
    r"public\s+(class|static|void)",  # Java keyword
    r"print\s*\(",         # Python print
    r"System\.out\.print", # Java print
    r"console\.log\s*\(",  # JavaScript print
    r"\w+\s*=\s*new\s+\w+", # Java / C++ new keyword
    r"function\s+\w+\s*\(", # JavaScript function
    r"<\?php",  # PHP code
    r"import\s+\w+",  # Python / Java import 
    r"using\s+\w+\s*;",  # C++ `using` 
    r"using\s+(System|javax)\.",  # C# / Java `using`
    r"\w+\s*:\s*\w+\s*=>",  # Lambda （Python, JavaScript）
    r"if\s*\(.*?\)\s*\{?",  # if （C, C++, Java, JavaScript）
    r"for\s*\(.*?\)\s*\{?",  # for
    r"while\s*\(.*?\)\s*\{?",  # while 
    r"\bSELECT\b.*\bFROM\b",  # sql
    r"\bINSERT INTO\b.*\bVALUES\b",
    r"\bUPDATE\b.*\bSET\b",
    r"\bDELETE FROM\b"
]
emoji_to_word = {
    '😂': '<joy>',
    '😊': '<happy>',
    '😢': '<sad>',
    '😎': '<cool>',
    '😍': '<love>',
    '😭': '<crying>',
    '😡': '<anger>',
    '😱': '<fear>',
    '💀': '<skull>',
    '💩': '<poop>',
    '🙌': '<celebrate>',
    '👍': '<like>',
    '👎': '<thumb_down>',
    '😜': '<playful>',
    '🤔': '<thinking>',
    '😤': '<frustrated>',
    '😬': '<awkward>',
    '🥳': '<party>',
    '🙃': '<Facepalm>',
    '🤣': '<Hilarious>',
    '👋': '<hello>',
    '🤗': '<warmth>',
    '🖕' : '<middle finger>'
    
}#manual add the icon having sentiment

manglish_dict = {
    "ah" :"",
    "lah": "",
    "lor": "",
    "wan": "want",
    "boleh": "can",
    "tak": "not",
    "makan": "eat",
    "taboleh": "cannot",
    "bo jio": "never invite",
    "siao": "crazy",
    "walao": "oh my god",
    "jialat": "terrible",
    "gg": "game over",
    "tot" : "thought",
    "lmao": "laughing hard",
    "b4" : "before",
    "u" : "you",
    "typo" :  "typing mistake",
    "r": "are",
    "tmr": "tomorrow",
    "btw": "by the way",
    "rn": "right now",
    "rmb": "remember",
    "nid": "need",
    "yea": "yeah",
    "yall": "you all",
    "iam" : "i am",
    "ill" : "i will",
    "jk":"just kidding",
    "pls": "please",
    "ikr": "I know, right?",
    "nvm": "never mind",
    "tf" :"the fuck",
    "wth":"what the heck",
    "wtf":"what the fuck",
    "shet" : "shit",
    "mdfk": "mother fucker",
    "tbh":"to be honest",
    "meh": "",
    "liao": "",
    "liaoz": "",
    "hor": "",
    "mah": "",
    "dey": "",
    "bo": "no",
    "kena": "got",
    "canot": "cannot",
    "oso": "also",
    "den": "then",
    "cuz": "because",
    "coz": "because",
    "bc": "because",
    "bcuz": "because",
    "bcos": "because",
    "alr": "already",
    "alrd": "already",
    "zzz": "",
    "wah": "wow",
    "eh": "",
    "yo": "",
    "got": "have",
    "wanna": "want to",
    "gonna": "going to",
    "ain’t": "is not",
    "ain": "is not",
    "omg": "oh my god",
    "hahaha": "",
    "haha": "",
    "hehe": "",
    "lol": "",
    "lols": "",
    "xd": "",
    "rofl": "rolling on the floor laughing",
    "zz": "",
    "ehhh": "",
    "ehh": "",
    "leh": "",
    "loh": "",
    "okie": "okay",
    "okey": "okay",
    "okayy": "okay",
    "kay": "okay",
    "k": "okay",
    "idk": "i don't know",
    "ty": "thank you",
    "fyi": "for your information", 
    "dk": "don't know"
}
variations = {
    "bo jio": ["bojio", "bo jio"],
    "walao": ["walao", "walaoeh", "walao eh", "walaowei","walaoweii"],
    "siao": ["siao", "xiao"],
    "lah": ["lah", "la", ""], 
    "leh": ["leh", "le", ""],
    "lor": ["lor", "lo", ""],
    "wan": ["wan", "want"],
    "gg": ["gg", "GG"], 
}