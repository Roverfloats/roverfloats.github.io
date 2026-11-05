hiragana = {"a":"あ","i":"い","u":"う","e":"え","o":"お",
"ka":"か","ki":"き","ku":"く","ke":"け","ko":"こ",
"ga":"が","gi":"ぎ","gu":"ぐ","ge":"げ","go":"ご",
"sa":"さ","si":"し","su":"す","se":"せ","so":"そ","shi":"し",
"za":"ざ","zi":"じ","zu":"ず","ze":"ぜ","zo":"ぞ","ji":"じ",
"ta":"た","ti":"ち","tu":"つ","te":"て","to":"と","chi":"ち","tsu":"つ",
"da":"だ","di":"ぢ","du":"づ","de":"で","do":"ど","dzu":"づ",
"na":"な","ni":"に","nu":"ぬ","ne":"ね","no":"の",
"ha":"は","hi":"ひ","hu":"ふ","he":"へ","ho":"ほ","fu":"ふ",
"ba":"ば","bi":"び","bu":"ぶ","be":"べ","bo":"ぼ",
"pa":"ぱ","pi":"ぴ","pu":"ぷ","pe":"ぺ","po":"ぽ",
"ma":"ま","mi":"み","mu":"む","me":"め","mo":"も",
"ya":"や","yu":"ゆ","yo":"よ",
"ra":"ら","ri":"り","ru":"る","re":"れ","ro":"ろ",
"wa":"わ","wo":"を",
"n":"ん","ｎ":"ん",
"kya":"きゃ","kyu":"きゅ","kyo":"きょ",
"gya":"ぎゃ","gyu":"ぎゅ","gyo":"ぎょ",
"sya":"しゃ","syu":"しゅ","syo":"しょ","sha":"しゃ","shu":"しゅ","sho":"しょ",
"zya":"じゃ","zyu":"じゅ","zyo":"じょ","jya":"じゃ","jyu":"じゅ","jyo":"じょ","ja":"じゃ","ju":"じゅ","jo":"じょ",
"tya":"ちゃ","tyu":"ちゅ","tyo":"ちょ","cha":"ちゃ","chu":"ちゅ","cho":"ちょ",
"nya":"にゃ","nyu":"にゅ","nyo":"にょ",
"hya":"ひゃ","hyu":"ひゅ","hyo":"ひょ",
"bya":"びゃ","byu":"びゅ","byo":"びょ",
"pya":"ぴゃ","pyu":"ぴゅ","pyo":"ぴょ",
"mya":"みゃ","myu":"みゅ","myo":"みょ",
"rya":"りゃ","ryu":"りゅ","ryo":"りょ",
"vu":"ゔ",
"sakuon":"っ"}

katakana = {"a":"ア","i":"イ","u":"ウ","e":"エ","o":"オ",
"ka":"カ","ki":"キ","ku":"ク","ke":"ケ","ko":"コ",
"ga":"ガ","gi":"ギ","gu":"グ","ge":"ゲ","go":"ゴ",
"sa":"サ","si":"シ","su":"ス","se":"セ","so":"ソ","shi":"シ",
"za":"ザ","zi":"ジ","zu":"ズ","ze":"ゼ","zo":"ゾ","ji":"ジ",
"ta":"タ","ti":"チ","tu":"ツ","te":"テ","to":"ト","chi":"チ","tsu":"ツ",
"da":"ダ","di":"ヂ","du":"ヅ","de":"デ","do":"ド","dzu":"ヅ",
"na":"ナ","ni":"ニ","nu":"ヌ","ne":"ネ","no":"ノ",
"ha":"ハ","hi":"ヒ","hu":"フ","he":"ヘ","ho":"ホ","fu":"フ",
"ba":"バ","bi":"ビ","bu":"ブ","be":"ベ","bo":"ボ",
"pa":"パ","pi":"ピ","pu":"プ","pe":"ペ","po":"ポ",
"ma":"マ","mi":"ミ","mu":"ム","me":"メ","mo":"モ",
"ya":"ヤ","yu":"ユ","yo":"ヨ",
"ra":"ラ","ri":"リ","ru":"ル","re":"レ","ro":"ロ",
"wa":"ワ","wo":"ヲ",
"n":"ン",
"kya":"キャ","kyu":"キュ","kyo":"キョ",
"gya":"ギャ","gyu":"ギュ","gyo":"ギョ",
"sya":"シャ","syu":"シュ","syo":"ショ","sha":"シャ","shu":"シュ","sho":"ショ",
"zya":"ジャ","zyu":"ジュ","zyo":"ジョ","jya":"ジャ","jyu":"ジュ","jyo":"ジョ","ja":"ジャ","ju":"ジュ","jo":"ジョ",
"tya":"チャ","tyu":"チュ","tyo":"チョ","cha":"チャ","chu":"チュ","cho":"チョ",
"nya":"ニャ","nyu":"ニュ","nyo":"ニョ",
"hya":"ヒャ","hyu":"ヒュ","hyo":"ヒョ",
"bya":"ビャ","byu":"ビュ","byo":"ビョ",
"pya":"ピャ","pyu":"ピュ","pyo":"ピョ",
"mya":"ミャ","myu":"ミュ","myo":"ミョ",
"rya":"リャ","ryu":"リュ","ryo":"リョ",
"vu":"ヴ",
"va":"ヴァ","vi":"ヴィ","ve":"ヴェ","vo":"ヴォ",
"wi":"ウィ","we":"ウェ",
"fa":"ファ","fi":"フィ","fe":"フェ", "fo":"フォ",
"che":"チェ",
"dli":"ディ","dlu":"ドゥ",
"tli":"ティ","tlu":"トゥ",
"jle":"ジェ",
"she":"シェ",
"sakuon":"ッ",
"pause":"ー"}

def romajiToJapanese(romaji):
	romaji = romaji.lower()
	currentAlphabet = hiragana
	hiraganaIsCurrent = True
	resultStr = ""
	i=0
	while i < len(romaji):
		if romaji[i] == "*": #switch alphabets
			if hiraganaIsCurrent:
				currentAlphabet = katakana
				hiraganaIsCurrent = False
			else:
				currentAlphabet = hiragana
				hiraganaIsCurrent = True
			i+=1
		elif romaji[i] == " ": #check wa rule
			if (i+3 < len(romaji)):
				if romaji[i:i+4] == " wa ": #ha/wa rule
					resultStr += " %s " % currentAlphabet["ha"]
					i+=4
					continue
			resultStr += " "
			i+=1
		elif i+2 < len(romaji) and romaji[i] == "n" and romaji[i+1:i+2] == "n" and romaji[i+1:i+3] not in currentAlphabet: #n rule
			resultStr += currentAlphabet["sakuon"]
			i+=1
		else:
			checkLen = min(3, len(romaji)-i)
			while checkLen > 0:
				checkStr = romaji[i:i+checkLen]
				if checkStr in currentAlphabet:
					resultStr += currentAlphabet[checkStr]
					i+=checkLen
					if (i < len(romaji)):
						# if romaji[i] == "o" and romaji[i-1:i] == "o" and hiraganaIsCurrent: #oo = ou rule
						# 	resultStr += currentAlphabet["u"]
						# 	i+=1
						# elif romaji[i] == "e" and romaji[i-1:i] == "e" and hiraganaIsCurrent: #ee = ei rule
						# 	resultStr += currentAlphabet["i"]
						# 	i+=1
						if romaji[i] == romaji[i-1:i] and hiraganaIsCurrent == False:
							if romaji[i] == "n":
								break
							elif romaji[i] in ["a", "e", "i", "o", "u"]:
								resultStr += currentAlphabet["pause"]
							else:
								resultStr += currentAlphabet["sakuon"]
							i+=1
					break
				elif checkLen == 1:
					if checkStr == "?" or checkStr == "." or checkStr == "!": #punctuation
						resultStr += "。"
					elif checkStr not in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]: #print any characters that aren't a letter
						resultStr += checkStr
					elif i+1 < len(romaji): #little tsu rule
						if checkStr == romaji[i+1:i+2]:
							resultStr += currentAlphabet["sakuon"]
					i+=1
					break	
				checkLen-=1
	return resultStr
