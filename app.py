from flask import Flask, render_template, request, jsonify
import heapq
import math

app = Flask(__name__)

# ---- HTML PAGES ----

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/station')
def station_page():
    return render_template('station.html')

@app.route('/route')
def route_page():
    return render_template('route.html')

# ---- METRO DATA ----

from flask import Flask, render_template, request, jsonify
import heapq
import math

app = Flask(__name__)

# ---- HTML PAGES ----

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/station')
def station_page():
    return render_template('station.html')

@app.route('/route')
def route_page():
    return render_template('route.html')

# ---- METRO DATA ----

metro_graph = {
    "stations": {
        "Shaheed Sthal": {
            "coords": [28.6925, 77.4986],
            "neighbors": ["Hindon"],
            "line": "red"
        },
        "Hindon": {
            "coords": [28.6811, 77.4823],
            "neighbors": ["Shaheed Sthal", "Arthala"],
            "line": "red"
        },
        "Arthala": {
            "coords": [28.6741, 77.4712],
            "neighbors": ["Hindon", "Mohan Nagar"],
            "line": "red"
        },
        "Mohan Nagar": {
            "coords": [28.6579, 77.4474],
            "neighbors": ["Arthala", "Shyam Park"],
            "line": "red"
        },
        "Shyam Park": {
            "coords": [28.6502, 77.4345],
            "neighbors": ["Mohan Nagar", "Major Mohit Sharma"],
            "line": "red"
        },
        "Major Mohit Sharma": {
            "coords": [28.6430, 77.4230],
            "neighbors": ["Shyam Park", "Raj Bagh"],
            "line": "red"
        },
        "Raj Bagh": {
            "coords": [28.6360, 77.4130],
            "neighbors": ["Major Mohit Sharma", "Shaheed Nagar"],
            "line": "red"
        },
        "Shaheed Nagar": {
            "coords": [28.6300, 77.4050],
            "neighbors": ["Raj Bagh", "Dilshad Garden"],
            "line": "red"
        },
        "Dilshad Garden": {
            "coords": [28.6772, 77.3077],
            "neighbors": ["Shaheed Nagar", "Jhil Mil"],
            "line": "red"
        },
        "Jhil Mil": {
            "coords": [28.6815, 77.2995],
            "neighbors": ["Dilshad Garden", "Mansarovar Park"],
            "line": "red"
        },
        "Mansarovar Park": {
            "coords": [28.6848, 77.2927],
            "neighbors": ["Jhil Mil", "Shahdara"],
            "line": "red"
        },
        "Shahdara": {
            "coords": [28.6810, 77.2822],
            "neighbors": ["Mansarovar Park", "Welcome"],
            "line": "red"
        },
        "Welcome": {
            "coords": [28.6781, 77.2670],
            "neighbors": ["Shahdara", "Seelampur", "East Azad Nagar"],
            "line": "red"
        },
        "Seelampur": {
            "coords": [28.6776, 77.2582],
            "neighbors": ["Welcome", "Shastri Park"],
            "line": "red"
        },
        "Shastri Park": {
            "coords": [28.6732, 77.2472],
            "neighbors": ["Seelampur", "Kashmere Gate"],
            "line": "red"
        },
        "Kashmere Gate": {
            "coords": [28.6675, 77.2273],
            "neighbors": ["Shastri Park", "Tis Hazari", "Civil Lines", "Lal Qila"],
            "line": "red"
        },
        "Tis Hazari": {
            "coords": [28.6697, 77.2086],
            "neighbors": ["Kashmere Gate", "Pul Bangash"],
            "line": "red"
        },
        "Pul Bangash": {
            "coords": [28.6740, 77.1980],
            "neighbors": ["Tis Hazari", "Pratap Nagar"],
            "line": "red"
        },
        "Pratap Nagar": {
            "coords": [28.6767, 77.1919],
            "neighbors": ["Pul Bangash", "Shastri Nagar"],
            "line": "red"
        },
        "Shastri Nagar": {
            "coords": [28.6848, 77.1748],
            "neighbors": ["Pratap Nagar", "Inder Lok"],
            "line": "red"
        },
        "Inder Lok": {
            "coords": [28.6870, 77.1637],
            "neighbors": ["Shastri Nagar", "Kanhiya Nagar"],
            "line": "red"
        },
        "Kanhiya Nagar": {
            "coords": [28.6926, 77.1533],
            "neighbors": ["Inder Lok", "Keshav Puram"],
            "line": "red"
        },
        "Keshav Puram": {
            "coords": [28.6959, 77.1426],
            "neighbors": ["Kanhiya Nagar", "Netaji Subhash Place"],
            "line": "red"
        },
        "Netaji Subhash Place": {
            "coords": [28.6981, 77.1349],
            "neighbors": ["Keshav Puram", "Kohat Enclave", "Shalimar Bagh"],
            "line": "red"
        },
        "Kohat Enclave": {
            "coords": [28.6994, 77.1229],
            "neighbors": ["Netaji Subhash Place", "Pitampura"],
            "line": "red"
        },
        "Pitampura": {
            "coords": [28.7038, 77.1160],
            "neighbors": ["Kohat Enclave", "Rohini East"],
            "line": "red"
        },
        "Rohini East": {
            "coords": [28.7137, 77.1037],
            "neighbors": ["Pitampura", "Rohini West"],
            "line": "red"
        },
        "Rohini West": {
            "coords": [28.7237, 77.1011],
            "neighbors": ["Rohini East", "Rithala"],
            "line": "red"
        },
        "Rithala": {
            "coords": [28.7325, 77.1031],
            "neighbors": ["Rohini West"],
            "line": "red"
        },
        "Samaypur Badli": {
            "coords": [28.7512, 77.1347],
            "neighbors": ["Rohini Sector 18"],
            "line": "yellow"
        },
        "Rohini Sector 18": {
            "coords": [28.7427, 77.1324],
            "neighbors": ["Samaypur Badli", "Haiderpur"],
            "line": "yellow"
        },
        "Haiderpur": {
            "coords": [28.7370, 77.1301],
            "neighbors": ["Rohini Sector 18", "Jahangirpuri"],
            "line": "yellow"
        },
        "Jahangirpuri": {
            "coords": [28.7255, 77.1423],
            "neighbors": ["Haiderpur", "Adarsh Nagar"],
            "line": "yellow"
        },
        "Adarsh Nagar": {
            "coords": [28.7152, 77.1518],
            "neighbors": ["Jahangirpuri", "Azadpur"],
            "line": "yellow"
        },
        "Azadpur": {
            "coords": [28.6984, 77.1896],
            "neighbors": ["Adarsh Nagar", "Model Town", "Shalimar Bagh", "Majlis Park"],
            "line": "yellow"
        },
        "Model Town": {
            "coords": [28.7011, 77.1924],
            "neighbors": ["Azadpur", "GTB Nagar"],
            "line": "yellow"
        },
        "GTB Nagar": {
            "coords": [28.7062, 77.1938],
            "neighbors": ["Model Town", "Vishwavidyalaya"],
            "line": "yellow"
        },
        "Vishwavidyalaya": {
            "coords": [28.7140, 77.2135],
            "neighbors": ["GTB Nagar", "Vidhan Sabha"],
            "line": "yellow"
        },
        "Vidhan Sabha": {
            "coords": [28.7180, 77.2201],
            "neighbors": ["Vishwavidyalaya", "Civil Lines"],
            "line": "yellow"
        },
        "Civil Lines": {
            "coords": [28.7232, 77.2262],
            "neighbors": ["Vidhan Sabha", "Kashmere Gate"],
            "line": "yellow"
        },
        "Chandni Chowk": {
            "coords": [28.6562, 77.2278],
            "neighbors": ["Kashmere Gate", "Chawri Bazar"],
            "line": "yellow"
        },
        "Chawri Bazar": {
            "coords": [28.6505, 77.2293],
            "neighbors": ["Chandni Chowk", "New Delhi"],
            "line": "yellow"
        },
        "New Delhi": {
            "coords": [28.6420, 77.2205],
            "neighbors": ["Chawri Bazar", "Rajiv Chowk", "Shivaji Stadium"],
            "line": "yellow"
        },
        "Patel Chowk": {
            "coords": [28.6265, 77.2138],
            "neighbors": ["Rajiv Chowk", "Central Secretariat"],
            "line": "yellow"
        },
        "Central Secretariat": {
            "coords": [28.6143, 77.2167],
            "neighbors": ["Patel Chowk", "Udyog Bhawan", "Janpath"],
            "line": "yellow"
        },
        "Udyog Bhawan": {
            "coords": [28.6061, 77.2129],
            "neighbors": ["Central Secretariat", "Lok Kalyan Marg"],
            "line": "yellow"
        },
        "Lok Kalyan Marg": {
            "coords": [28.5984, 77.2106],
            "neighbors": ["Udyog Bhawan", "Jor Bagh"],
            "line": "yellow"
        },
        "Jor Bagh": {
            "coords": [28.5912, 77.2092],
            "neighbors": ["Lok Kalyan Marg", "Dilli Haat - INA"],
            "line": "yellow"
        },
        "Dilli Haat - INA": {
            "coords": [28.5687, 77.2097],
            "neighbors": ["Jor Bagh", "AIIMS", "INA", "Sarojini Nagar"],
            "line": "yellow"
        },
        "AIIMS": {
            "coords": [28.5672, 77.2107],
            "neighbors": ["Dilli Haat - INA", "Green Park"],
            "line": "yellow"
        },
        "Green Park": {
            "coords": [28.5581, 77.2065],
            "neighbors": ["AIIMS", "Hauz Khas"],
            "line": "yellow"
        },
        "Hauz Khas": {
            "coords": [28.5494, 77.2077],
            "neighbors": ["Green Park", "Malviya Nagar", "IIT Delhi", "Panchsheel Park"],
            "line": "yellow"
        },
        "Malviya Nagar": {
            "coords": [28.5368, 77.2106],
            "neighbors": ["Hauz Khas", "Saket"],
            "line": "yellow"
        },
        "Saket": {
            "coords": [28.5274, 77.2068],
            "neighbors": ["Malviya Nagar", "Qutab Minar"],
            "line": "yellow"
        },
        "Qutab Minar": {
            "coords": [28.5113, 77.1945],
            "neighbors": ["Saket", "Chhatarpur"],
            "line": "yellow"
        },
        "Chhatarpur": {
            "coords": [28.5029, 77.1769],
            "neighbors": ["Qutab Minar", "Sultanpur"],
            "line": "yellow"
        },
        "Sultanpur": {
            "coords": [28.4922, 77.1687],
            "neighbors": ["Chhatarpur", "Ghitorni"],
            "line": "yellow"
        },
        "Ghitorni": {
            "coords": [28.4803, 77.1576],
            "neighbors": ["Sultanpur", "Arjangarh"],
            "line": "yellow"
        },
        "Arjangarh": {
            "coords": [28.4693, 77.1486],
            "neighbors": ["Ghitorni", "Guru Dronacharya"],
            "line": "yellow"
        },
        "Guru Dronacharya": {
            "coords": [28.4577, 77.1404],
            "neighbors": ["Arjangarh", "Sikandarpur"],
            "line": "yellow"
        },
        "Sikandarpur": {
            "coords": [28.4799, 77.0732],
            "neighbors": ["Guru Dronacharya", "MG Road"],
            "line": "yellow"
        },
        "MG Road": {
            "coords": [28.4697, 77.0732],
            "neighbors": ["Sikandarpur", "IFFCO Chowk"],
            "line": "yellow"
        },
        "IFFCO Chowk": {
            "coords": [28.4671, 77.0638],
            "neighbors": ["MG Road", "Huda City Centre"],
            "line": "yellow"
        },
        "Huda City Centre": {
            "coords": [28.4595, 77.0591],
            "neighbors": ["IFFCO Chowk"],
            "line": "yellow"
        },
        "Dwarka Sector 21": {
            "coords": [28.5821, 76.9380],
            "neighbors": ["Dwarka Sector 8", "IGI Airport"],
            "line": "blue"
        },
        "Dwarka Sector 8": {
            "coords": [28.5841, 76.9501],
            "neighbors": ["Dwarka Sector 21", "Dwarka Sector 9"],
            "line": "blue"
        },
        "Dwarka Sector 9": {
            "coords": [28.5861, 76.9622],
            "neighbors": ["Dwarka Sector 8", "Dwarka Sector 10"],
            "line": "blue"
        },
        "Dwarka Sector 10": {
            "coords": [28.5881, 76.9743],
            "neighbors": ["Dwarka Sector 9", "Dwarka Sector 11"],
            "line": "blue"
        },
        "Dwarka Sector 11": {
            "coords": [28.5901, 76.9864],
            "neighbors": ["Dwarka Sector 10", "Dwarka Sector 12"],
            "line": "blue"
        },
        "Dwarka Sector 12": {
            "coords": [28.5922, 76.9985],
            "neighbors": ["Dwarka Sector 11", "Dwarka Sector 13"],
            "line": "blue"
        },
        "Dwarka Sector 13": {
            "coords": [28.5941, 77.0106],
            "neighbors": ["Dwarka Sector 12", "Dwarka Sector 14"],
            "line": "blue"
        },
        "Dwarka Sector 14": {
            "coords": [28.5962, 77.0234],
            "neighbors": ["Dwarka Sector 13", "Dwarka"],
            "line": "blue"
        },
        "Dwarka": {
            "coords": [28.6087, 77.0375],
            "neighbors": ["Dwarka Sector 14", "Dwarka Mor", "Nangli"],
            "line": "blue"
        },
        "Dwarka Mor": {
            "coords": [28.6215, 77.0427],
            "neighbors": ["Dwarka", "Nawada"],
            "line": "blue"
        },
        "Nawada": {
            "coords": [28.6236, 77.0556],
            "neighbors": ["Dwarka Mor", "Uttam Nagar West"],
            "line": "blue"
        },
        "Uttam Nagar West": {
            "coords": [28.6371, 77.0704],
            "neighbors": ["Nawada", "Uttam Nagar East"],
            "line": "blue"
        },
        "Uttam Nagar East": {
            "coords": [28.6390, 77.0792],
            "neighbors": ["Uttam Nagar West", "Janakpuri West"],
            "line": "blue"
        },
        "Janakpuri West": {
            "coords": [28.6411, 77.0902],
            "neighbors": ["Uttam Nagar East", "Janakpuri East", "Dabri Mor"],
            "line": "blue"
        },
        "Janakpuri East": {
            "coords": [28.6428, 77.0983],
            "neighbors": ["Janakpuri West", "Tilak Nagar"],
            "line": "blue"
        },
        "Tilak Nagar": {
            "coords": [28.6467, 77.1035],
            "neighbors": ["Janakpuri East", "Subhash Nagar"],
            "line": "blue"
        },
        "Subhash Nagar": {
            "coords": [28.6467, 77.1035],
            "neighbors": ["Tilak Nagar", "Tagore Garden"],
            "line": "blue"
        },
        "Tagore Garden": {
            "coords": [28.6481, 77.1092],
            "neighbors": ["Subhash Nagar", "Rajouri Garden"],
            "line": "blue"
        },
        "Rajouri Garden": {
            "coords": [28.6492, 77.1173],
            "neighbors": ["Tagore Garden", "Ramesh Nagar", "ESI Hospital"],
            "line": "blue"
        },
        "Ramesh Nagar": {
            "coords": [28.6495, 77.1231],
            "neighbors": ["Rajouri Garden", "Moti Nagar"],
            "line": "blue"
        },
        "Moti Nagar": {
            "coords": [28.6511, 77.1314],
            "neighbors": ["Ramesh Nagar", "Kirti Nagar"],
            "line": "blue"
        },
        "Kirti Nagar": {
            "coords": [28.6519, 77.1407],
            "neighbors": ["Moti Nagar", "Shadipur"],
            "line": "blue"
        },
        "Shadipur": {
            "coords": [28.6512, 77.1538],
            "neighbors": ["Kirti Nagar", "Patel Nagar"],
            "line": "blue"
        },
        "Patel Nagar": {
            "coords": [28.6519, 77.1677],
            "neighbors": ["Shadipur", "Rajendra Place"],
            "line": "blue"
        },
        "Rajendra Place": {
            "coords": [28.6536, 77.1852],
            "neighbors": ["Patel Nagar", "Karol Bagh"],
            "line": "blue"
        },
        "Karol Bagh": {
            "coords": [28.6514, 77.1905],
            "neighbors": ["Rajendra Place", "Rajiv Chowk"],
            "line": "blue"
        },
        "Rajiv Chowk": {
            "coords": [28.6328, 77.2197],
            "neighbors": ["Karol Bagh", "Barakhamba", "New Delhi", "Patel Chowk"],
            "line": "blue"
        },
        "Barakhamba": {
            "coords": [28.6312, 77.2226],
            "neighbors": ["Rajiv Chowk", "Mandi House"],
            "line": "blue"
        },
        "Mandi House": {
            "coords": [28.6282, 77.2410],
            "neighbors": ["Barakhamba", "Supreme Court", "ITO", "Janpath"],
            "line": "blue"
        },
        "Supreme Court": {
            "coords": [28.6189, 77.2427],
            "neighbors": ["Mandi House", "Indraprastha"],
            "line": "blue"
        },
        "Indraprastha": {
            "coords": [28.6189, 77.2427],
            "neighbors": ["Supreme Court", "Yamuna Bank"],
            "line": "blue"
        },
        "Yamuna Bank": {
            "coords": [28.6097, 77.2732],
            "neighbors": ["Indraprastha", "Akshardham", "Laxmi Nagar"],
            "line": "blue"
        },
        "Akshardham": {
            "coords": [28.6132, 77.2772],
            "neighbors": ["Yamuna Bank", "Mayur Vihar Phase-1"],
            "line": "blue"
        },
        "Mayur Vihar Phase-1": {
            "coords": [28.5847, 77.2874],
            "neighbors": ["Akshardham", "Mayur Vihar Extension", "Hazrat Nizamuddin"],
            "line": "blue"
        },
        "Mayur Vihar Extension": {
            "coords": [28.5890, 77.2926],
            "neighbors": ["Mayur Vihar Phase-1", "New Ashok Nagar"],
            "line": "blue"
        },
        "New Ashok Nagar": {
            "coords": [28.5882, 77.3022],
            "neighbors": ["Mayur Vihar Extension", "Noida Sector 15"],
            "line": "blue"
        },
        "Noida Sector 15": {
            "coords": [28.5914, 77.3090],
            "neighbors": ["New Ashok Nagar", "Noida Sector 16"],
            "line": "blue"
        },
        "Noida Sector 16": {
            "coords": [28.5796, 77.3186],
            "neighbors": ["Noida Sector 15", "Noida Sector 18"],
            "line": "blue"
        },
        "Noida Sector 18": {
            "coords": [28.5708, 77.3260],
            "neighbors": ["Noida Sector 16", "Botanical Garden"],
            "line": "blue"
        },
        "Botanical Garden": {
            "coords": [28.5535, 77.3341],
            "neighbors": ["Noida Sector 18", "Golf Course", "Okhla Bird Sanctuary"],
            "line": "blue"
        },
        "Golf Course": {
            "coords": [28.5679, 77.3340],
            "neighbors": ["Botanical Garden", "Noida City Centre"],
            "line": "blue"
        },
        "Noida City Centre": {
            "coords": [28.5748, 77.3536],
            "neighbors": ["Golf Course", "Noida Sector 34"],
            "line": "blue"
        },
        "Noida Sector 34": {
            "coords": [28.5991, 77.3211],
            "neighbors": ["Noida City Centre", "Noida Sector 52"],
            "line": "blue"
        },
        "Noida Sector 52": {
            "coords": [28.6127, 77.3260],
            "neighbors": ["Noida Sector 34", "Noida Sector 61"],
            "line": "blue"
        },
        "Noida Sector 61": {
            "coords": [28.6237, 77.3307],
            "neighbors": ["Noida Sector 52", "Noida Sector 59"],
            "line": "blue"
        },
        "Noida Sector 59": {
            "coords": [28.6282, 77.3427],
            "neighbors": ["Noida Sector 61", "Noida Sector 62"],
            "line": "blue"
        },
        "Noida Sector 62": {
            "coords": [28.6304, 77.3588],
            "neighbors": ["Noida Sector 59", "Noida Electronic City"],
            "line": "blue"
        },
        "Noida Electronic City": {
            "coords": [28.6280, 77.3735],
            "neighbors": ["Noida Sector 62"],
            "line": "blue"
        },
        "Laxmi Nagar": {
            "coords": [28.6316, 77.2771],
            "neighbors": ["Yamuna Bank", "Nirman Vihar"],
            "line": "blue"
        },
        "Nirman Vihar": {
            "coords": [28.6372, 77.2865],
            "neighbors": ["Laxmi Nagar", "Preet Vihar"],
            "line": "blue"
        },
        "Preet Vihar": {
            "coords": [28.6413, 77.2945],
            "neighbors": ["Nirman Vihar", "Karkarduma"],
            "line": "blue"
        },
        "Karkarduma": {
            "coords": [28.6485, 77.3037],
            "neighbors": ["Preet Vihar", "Anand Vihar", "Karkarduma Court"],
            "line": "blue"
        },
        "Anand Vihar": {
            "coords": [28.6470, 77.3160],
            "neighbors": ["Karkarduma", "IP Extension", "Kaushambi"],
            "line": "blue"
        },
        "Kaushambi": {
            "coords": [28.6459, 77.3246],
            "neighbors": ["Anand Vihar", "Vaishali"],
            "line": "blue"
        },
        "Vaishali": {
            "coords": [28.6475, 77.3384],
            "neighbors": ["Kaushambi"],
            "line": "blue"
        },
        "Kashmere Gate": {
            "coords": [28.6675, 77.2273],
            "neighbors": ["Lal Qila", "Shastri Park", "Tis Hazari", "Civil Lines"],
            "line": "violet"
        },
        "Lal Qila": {
            "coords": [28.6561, 77.2306],
            "neighbors": ["Kashmere Gate", "Jama Masjid"],
            "line": "violet"
        },
        "Jama Masjid": {
            "coords": [28.6509, 77.2335],
            "neighbors": ["Lal Qila", "Delhi Gate"],
            "line": "violet"
        },
        "Delhi Gate": {
            "coords": [28.6422, 77.2401],
            "neighbors": ["Jama Masjid", "ITO"],
            "line": "violet"
        },
        "ITO": {
            "coords": [28.6287, 77.2428],
            "neighbors": ["Delhi Gate", "Mandi House"],
            "line": "violet"
        },
        "Janpath": {
            "coords": [28.6245, 77.2193],
            "neighbors": ["Mandi House", "Central Secretariat"],
            "line": "violet"
        },
        "Khan Market": {
            "coords": [28.6063, 77.2263],
            "neighbors": ["Central Secretariat", "Jawaharlal Nehru Stadium"],
            "line": "violet"
        },
        "Jawaharlal Nehru Stadium": {
            "coords": [28.5992, 77.2342],
            "neighbors": ["Khan Market", "Jangpura"],
            "line": "violet"
        },
        "Jangpura": {
            "coords": [28.5878, 77.2400],
            "neighbors": ["Jawaharlal Nehru Stadium", "Lajpat Nagar"],
            "line": "violet"
        },
        "Lajpat Nagar": {
            "coords": [28.5708, 77.2365],
            "neighbors": ["Jangpura", "Moolchand", "South Extension", "Vinobapuri"],
            "line": "violet"
        },
        "Moolchand": {
            "coords": [28.5662, 77.2327],
            "neighbors": ["Lajpat Nagar", "Kailash Colony"],
            "line": "violet"
        },
        "Kailash Colony": {
            "coords": [28.5569, 77.2369],
            "neighbors": ["Moolchand", "Nehru Place"],
            "line": "violet"
        },
        "Nehru Place": {
            "coords": [28.5492, 77.2540],
            "neighbors": ["Kailash Colony", "Kalkaji Mandir"],
            "line": "violet"
        },
        "Kalkaji Mandir": {
            "coords": [28.5518, 77.2610],
            "neighbors": ["Nehru Place", "Govind Puri", "Nehru Enclave", "Okhla NSIC"],
            "line": "violet"
        },
        "Govind Puri": {
            "coords": [28.5443, 77.2650],
            "neighbors": ["Kalkaji Mandir", "Harkesh Nagar"],
            "line": "violet"
        },
        "Harkesh Nagar": {
            "coords": [28.5376, 77.2701],
            "neighbors": ["Govind Puri", "Jasola Apollo"],
            "line": "violet"
        },
        "Jasola Apollo": {
            "coords": [28.5338, 77.2828],
            "neighbors": ["Harkesh Nagar", "Sarita Vihar"],
            "line": "violet"
        },
        "Sarita Vihar": {
            "coords": [28.5312, 77.2911],
            "neighbors": ["Jasola Apollo", "Mohan Estate"],
            "line": "violet"
        },
        "Mohan Estate": {
            "coords": [28.5232, 77.2973],
            "neighbors": ["Sarita Vihar", "Tughlakabad"],
            "line": "violet"
        },
        "Tughlakabad": {
            "coords": [28.5156, 77.3018],
            "neighbors": ["Mohan Estate", "Badarpur"],
            "line": "violet"
        },
        "Badarpur": {
            "coords": [28.5032, 77.3029],
            "neighbors": ["Tughlakabad", "Sarai"],
            "line": "violet"
        },
        "Sarai": {
            "coords": [28.4932, 77.3027],
            "neighbors": ["Badarpur", "NHPC Chowk"],
            "line": "violet"
        },
        "NHPC Chowk": {
            "coords": [28.4802, 77.2995],
            "neighbors": ["Sarai", "Mewala Maharajpur"],
            "line": "violet"
        },
        "Mewala Maharajpur": {
            "coords": [28.4710, 77.3106],
            "neighbors": ["NHPC Chowk", "Sector-28"],
            "line": "violet"
        },
        "Sector-28": {
            "coords": [28.4572, 77.3153],
            "neighbors": ["Mewala Maharajpur", "Badkhal Lake"],
            "line": "violet"
        },
        "Badkhal Lake": {
            "coords": [28.4469, 77.3175],
            "neighbors": ["Sector-28", "Faridabad Old"],
            "line": "violet"
        },
        "Faridabad Old": {
            "coords": [28.4356, 77.3177],
            "neighbors": ["Badkhal Lake", "Crown Plaza"],
            "line": "violet"
        },
        "Crown Plaza": {
            "coords": [28.4278, 77.3143],
            "neighbors": ["Faridabad Old", "Neelam Chowk Ajronda"],
            "line": "violet"
        },
        "Neelam Chowk Ajronda": {
            "coords": [28.4185, 77.3144],
            "neighbors": ["Crown Plaza", "Bata Chowk"],
            "line": "violet"
        },
        "Bata Chowk": {
            "coords": [28.4097, 77.3133],
            "neighbors": ["Neelam Chowk Ajronda", "Escorts Mujesar"],
            "line": "violet"
        },
        "Escorts Mujesar": {
            "coords": [28.3994, 77.3139],
            "neighbors": ["Bata Chowk", "Sant Surdas - Sihi"],
            "line": "violet"
        },
        "Sant Surdas - Sihi": {
            "coords": [28.3865, 77.3143],
            "neighbors": ["Escorts Mujesar", "Raja Nahar Singh"],
            "line": "violet"
        },
        "Raja Nahar Singh": {
            "coords": [28.3766, 77.3144],
            "neighbors": ["Sant Surdas - Sihi"],
            "line": "violet"
        },
                "Majlis Park": {
            "coords": [28.6995, 77.1835],
            "neighbors": ["Azadpur", "Shalimar Bagh"],
            "line": "pink"
        },
        "Shalimar Bagh": {
            "coords": [28.6968, 77.1752],
            "neighbors": ["Majlis Park", "Netaji Subhash Place", "Punjabi Bagh West"],
            "line": "pink"
        },
        "Punjabi Bagh West": {
            "coords": [28.6865, 77.1662],
            "neighbors": ["Shalimar Bagh", "ESI Hospital"],
            "line": "pink"
        },
        "ESI Hospital": {
            "coords": [28.6703, 77.1505],
            "neighbors": ["Punjabi Bagh West", "Rajouri Garden"],
            "line": "pink"
        },
        "Shivaji Park": {
            "coords": [28.6682, 77.1582],
            "neighbors": ["Punjabi Bagh West", "Madipur"],
            "line": "pink"
        },
        "Madipur": {
            "coords": [28.6685, 77.1653],
            "neighbors": ["Shivaji Park", "Paschim Vihar West"],
            "line": "pink"
        },
        "Paschim Vihar West": {
            "coords": [28.6688, 77.1724],
            "neighbors": ["Madipur", "Paschim Vihar East"],
            "line": "pink"
        },
        "Paschim Vihar East": {
            "coords": [28.6691, 77.1795],
            "neighbors": ["Paschim Vihar West", "Peeragarhi"],
            "line": "pink"
        },
        "Peeragarhi": {
            "coords": [28.6694, 77.1866],
            "neighbors": ["Paschim Vihar East", "Udyog Nagar"],
            "line": "pink"
        },
        "Udyog Nagar": {
            "coords": [28.6697, 77.1937],
            "neighbors": ["Peeragarhi", "Surajmal Stadium"],
            "line": "pink"
        },
        "Surajmal Stadium": {
            "coords": [28.6700, 77.2008],
            "neighbors": ["Udyog Nagar", "Nangloi"],
            "line": "pink"
        },
        "Nangloi": {
            "coords": [28.6703, 77.2079],
            "neighbors": ["Surajmal Stadium", "Nangloi Railway Station"],
            "line": "pink"
        },
        "Nangloi Railway Station": {
            "coords": [28.6706, 77.2150],
            "neighbors": ["Nangloi", "Rajdhani Park"],
            "line": "pink"
        },
        "Rajdhani Park": {
            "coords": [28.6709, 77.2221],
            "neighbors": ["Nangloi Railway Station", "Mundka"],
            "line": "pink"
        },
        "Mundka": {
            "coords": [28.6712, 77.2292],
            "neighbors": ["Rajdhani Park", "Mundka Industrial Area"],
            "line": "pink"
        },
        "Mundka Industrial Area": {
            "coords": [28.6715, 77.2363],
            "neighbors": ["Mundka", "Ghevra"],
            "line": "pink"
        },
        "Ghevra": {
            "coords": [28.6718, 77.2434],
            "neighbors": ["Mundka Industrial Area", "Tikri Kalan"],
            "line": "pink"
        },
        "Tikri Kalan": {
            "coords": [28.6721, 77.2505],
            "neighbors": ["Ghevra", "Tikri Border"],
            "line": "pink"
        },
        "Tikri Border": {
            "coords": [28.6724, 77.2576],
            "neighbors": ["Tikri Kalan", "Pandit Shree Ram Sharma"],
            "line": "pink"
        },
        "Pandit Shree Ram Sharma": {
            "coords": [28.6727, 77.2647],
            "neighbors": ["Tikri Border", "Bahadurgarh City"],
            "line": "pink"
        },
        "Bahadurgarh City": {
            "coords": [28.6730, 77.2718],
            "neighbors": ["Pandit Shree Ram Sharma", "Brigadier Hoshiyar Singh"],
            "line": "pink"
        },
        "Brigadier Hoshiyar Singh": {
            "coords": [28.6733, 77.2789],
            "neighbors": ["Bahadurgarh City"],
            "line": "pink"
        },
        "East Azad Nagar": {
            "coords": [28.6736, 77.2860],
            "neighbors": ["Welcome", "Krishna Nagar"],
            "line": "pink"
        },
        "Krishna Nagar": {
            "coords": [28.6739, 77.2931],
            "neighbors": ["East Azad Nagar", "Karkarduma Court"],
            "line": "pink"
        },
        "Karkarduma Court": {
            "coords": [28.6742, 77.3002],
            "neighbors": ["Krishna Nagar", "Karkarduma"],
            "line": "pink"
        },
        "Anand Vihar ISBT": {
            "coords": [28.6745, 77.3073],
            "neighbors": ["Karkarduma", "IP Extension"],
            "line": "pink"
        },
        "IP Extension": {
            "coords": [28.6748, 77.3144],
            "neighbors": ["Anand Vihar ISBT", "Mandawali"],
            "line": "pink"
        },
        "Mandawali": {
            "coords": [28.6751, 77.3215],
            "neighbors": ["IP Extension", "Vinod Nagar East"],
            "line": "pink"
        },
        "Vinod Nagar East": {
            "coords": [28.6754, 77.3286],
            "neighbors": ["Mandawali", "Vinod Nagar"],
            "line": "pink"
        },
        "Vinod Nagar": {
            "coords": [28.6757, 77.3357],
            "neighbors": ["Vinod Nagar East", "Trilokpuri"],
            "line": "pink"
        },
        "Trilokpuri": {
            "coords": [28.6760, 77.3428],
            "neighbors": ["Vinod Nagar", "Mayur Vihar Pocket 1"],
            "line": "pink"
        },
        "Mayur Vihar Pocket 1": {
            "coords": [28.6763, 77.3499],
            "neighbors": ["Trilokpuri", "Mayur Vihar Phase 1"],
            "line": "pink"
        },
        "Sarai Kale Khan": {
            "coords": [28.5832, 77.2615],
            "neighbors": ["Hazrat Nizamuddin", "Ashram"],
            "line": "pink"
        },
        "Ashram": {
            "coords": [28.5765, 77.2632],
            "neighbors": ["Sarai Kale Khan", "Sarai Kale Khan Nizamuddin"],
            "line": "pink"
        },
        "Sarai Kale Khan Nizamuddin": {
            "coords": [28.5698, 77.2649],
            "neighbors": ["Ashram", "Hazrat Nizamuddin"],
            "line": "pink"
        },
        "Hazrat Nizamuddin": {
            "coords": [28.5895, 77.2582],
            "neighbors": ["Sarai Kale Khan Nizamuddin", "Mayur Vihar Phase-1"],
            "line": "pink"
        },
        "IGI Airport": {
            "coords": [28.5563, 77.0820],
            "neighbors": ["Dwarka Sector 21", "Delhi Aerocity"],
            "line": "orange"
        },
        "Delhi Aerocity": {
            "coords": [28.5494, 77.1235],
            "neighbors": ["IGI Airport", "Dhaula Kuan"],
            "line": "orange"
        },
        "Dhaula Kuan": {
            "coords": [28.5923, 77.1604],
            "neighbors": ["Delhi Aerocity", "Shivaji Stadium"],
            "line": "orange"
        },
        "Shivaji Stadium": {
            "coords": [28.6313, 77.2105],
            "neighbors": ["Dhaula Kuan", "New Delhi"],
            "line": "orange"
        },
        "New Delhi": {
            "coords": [28.6420, 77.2205],
            "neighbors": ["Shivaji Stadium", "Chawri Bazar", "Rajiv Chowk"],
            "line": "orange"
        }
    },
    "lines": {
        "red": "#e74c3c",
        "yellow": "#f1c40f",
        "blue": "#3498db",
        "violet": "#8e44ad",
        "pink": "#e84393",
        "orange": "#e67e22",
        "green": "#2ecc71",
        "magenta": "#9b59b6",
        "grey": "#95a5a6",
        "rapid": "#1abc9c"
    }
}

def calculate_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371
    return c * r

def dijkstra(graph, start, end):
    if start not in graph["stations"] or end not in graph["stations"]:
        return [], 0, 0, 0, []
    
    stations = graph["stations"]
    distances = {station: float('inf') for station in stations}
    previous = {station: None for station in stations}
    distances[start] = 0
    queue = [(0, start)]
    visited_nodes = set()
    visited_order = []
    
    while queue:
        current_distance, current_station = heapq.heappop(queue)
        visited_nodes.add(current_station)
        visited_order.append(current_station)
        
        if current_station == end:
            break
            
        for neighbor in stations[current_station]["neighbors"]:
            if neighbor not in stations:
                continue
                
            start_coords = stations[current_station]["coords"]
            neighbor_coords = stations[neighbor]["coords"]
            weight = calculate_distance(start_coords[0], start_coords[1], 
                                      neighbor_coords[0], neighbor_coords[1])
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_station
                heapq.heappush(queue, (distance, neighbor))
    
    path = []
    station = end
    while station is not None:
        path.insert(0, station)
        station = previous[station]
    
    total_distance = distances[end]
    fare = calculate_fare(total_distance)
    
    if path and path[0] == start:
        return path, total_distance, fare, len(visited_nodes), visited_order
    else:
        return [], 0, 0, 0, []

def calculate_fare(distance_km):
    if distance_km <= 2:
        return 10
    elif distance_km <= 5:
        return 15
    elif distance_km <= 10:
        return 25
    elif distance_km <= 15:
        return 35
    elif distance_km <= 25:
        return 45
    else:
        return 60

# ---- API ENDPOINTS ----

@app.route('/stations')
def stations_api():
    return jsonify(sorted(list(metro_graph["stations"].keys())))

@app.route('/lines')
def lines_api():
    return jsonify({line: data["color"] for line, data in metro_graph["lines"].items()})

@app.route('/route', methods=['POST'])
def route_api():
    data = request.get_json()
    source = data.get('source')
    destination = data.get('destination')
    
    if not source or not destination:
        return jsonify({'error': 'Invalid input'}), 400
        
    path, distance, fare, visited, visited_order = dijkstra(metro_graph, source, destination)
    
    if not path:
        return jsonify({'error': 'No route found'}), 404
        
    # Get line information for each station in path
    path_with_lines = []
    for station in path:
        path_with_lines.append({
            "name": station,
            "line": metro_graph["stations"][station]["line"],
            "coords": metro_graph["stations"][station]["coords"]
        })
    
    return jsonify({
        'path': path_with_lines,
        'distance': round(distance, 2),
        'stations_count': len(path),
        'fare': fare,
        'visited': visited,
        'visited_order': visited_order
    })

@app.route('/stations-data')
def stations_data():
    stations = []
    for name, data in metro_graph["stations"].items():
        stations.append({
            "name": name,
            "coords": data["coords"],
            "line": data["line"]
        })
    return jsonify(stations)

if __name__ == '__main__':
    app.run(debug=True)
