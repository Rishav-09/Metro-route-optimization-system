from flask import Flask, render_template, request, jsonify
import heapq

app = Flask(__name__)

# Sample metro graph (expand as needed)

metro_graph = {
    # Red Line (Line 1)
    'Shaheed Sthal': {'Hindon': 1},
    'Hindon': {'Shaheed Sthal': 1, 'Arthala': 1},
    'Arthala': {'Hindon': 1, 'Mohan Nagar': 1},
    'Mohan Nagar': {'Arthala': 1, 'Shyam Park': 1},
    'Shyam Park': {'Mohan Nagar': 1, 'Major Mohit Sharma': 1},
    'Major Mohit Sharma': {'Shyam Park': 1, 'Raj Bagh': 1},
    'Raj Bagh': {'Major Mohit Sharma': 1, 'Shaheed Nagar': 1},
    'Shaheed Nagar': {'Raj Bagh': 1, 'Dilshad Garden': 1},
    'Dilshad Garden': {'Shaheed Nagar': 1, 'Jhil Mil': 1},
    'Jhil Mil': {'Dilshad Garden': 1, 'Mansarovar Park': 1},
    'Mansarovar Park': {'Jhil Mil': 1, 'Shahdara': 1},
    'Shahdara': {'Mansarovar Park': 1, 'Welcome': 1},
    'Welcome': {'Shahdara': 1, 'Seelampur': 1},
    'Seelampur': {'Welcome': 1, 'Shastri Park': 1},
    'Shastri Park': {'Seelampur': 1, 'Kashmere Gate': 1},
    'Kashmere Gate': {'Shastri Park': 1, 'Tis Hazari': 1, 'Civil Lines': 1, 'Lal Qila': 1},
    'Tis Hazari': {'Kashmere Gate': 1, 'Pul Bangash': 1},
    'Pul Bangash': {'Tis Hazari': 1, 'Pratap Nagar': 1},
    'Pratap Nagar': {'Pul Bangash': 1, 'Shastri Nagar': 1},
    'Shastri Nagar': {'Pratap Nagar': 1, 'Inder Lok': 1},
    'Inder Lok': {'Shastri Nagar': 1, 'Kanhiya Nagar': 1},
    'Kanhiya Nagar': {'Inder Lok': 1, 'Keshav Puram': 1},
    'Keshav Puram': {'Kanhiya Nagar': 1, 'Netaji Subhash Place': 1},
    'Netaji Subhash Place': {'Keshav Puram': 1, 'Kohat Enclave': 1},
    'Kohat Enclave': {'Netaji Subhash Place': 1, 'Pitampura': 1},
    'Pitampura': {'Kohat Enclave': 1, 'Rohini East': 1},
    'Rohini East': {'Pitampura': 1, 'Rohini West': 1},
    'Rohini West': {'Rohini East': 1, 'Rithala': 1},
    'Rithala': {'Rohini West': 1},

    # Yellow Line (Line 2)
    'Samaypur Badli': {'Rohini Sector 18': 1},
    'Rohini Sector 18': {'Samaypur Badli': 1, 'Haiderpur': 1},
    'Haiderpur': {'Rohini Sector 18': 1, 'Jahangirpuri': 1},
    'Jahangirpuri': {'Haiderpur': 1, 'Adarsh Nagar': 1},
    'Adarsh Nagar': {'Jahangirpuri': 1, 'Azadpur': 1},
    'Azadpur': {'Adarsh Nagar': 1, 'Model Town': 1, 'Shalimar Bagh': 1},
    'Model Town': {'Azadpur': 1, 'GTB Nagar': 1},
    'GTB Nagar': {'Model Town': 1, 'Vishwavidyalaya': 1},
    'Vishwavidyalaya': {'GTB Nagar': 1, 'Vidhan Sabha': 1},
    'Vidhan Sabha': {'Vishwavidyalaya': 1, 'Civil Lines': 1},
    'Civil Lines': {'Vidhan Sabha': 1, 'Kashmere Gate': 1},
    'Kashmere Gate': {'Civil Lines': 1, 'Chandni Chowk': 1},
    'Chandni Chowk': {'Kashmere Gate': 1, 'Chawri Bazar': 1},
    'Chawri Bazar': {'Chandni Chowk': 1, 'New Delhi': 1},
    'New Delhi': {'Chawri Bazar': 1, 'Rajiv Chowk': 1, 'Shivaji Stadium': 1},
    'Rajiv Chowk': {'New Delhi': 1, 'Patel Chowk': 1, 'Karol Bagh': 1, 'Barakhamba': 1},
    'Patel Chowk': {'Rajiv Chowk': 1, 'Central Secretariat': 1},
    'Central Secretariat': {'Patel Chowk': 1, 'Udyog Bhawan': 1},
    'Udyog Bhawan': {'Central Secretariat': 1, 'Lok Kalyan Marg': 1},
    'Lok Kalyan Marg': {'Udyog Bhawan': 1, 'Jor Bagh': 1},
    'Jor Bagh': {'Lok Kalyan Marg': 1, 'Dilli Haat - INA': 1},
    'Dilli Haat - INA': {'Jor Bagh': 1, 'AIIMS': 1},
    'AIIMS': {'Dilli Haat - INA': 1, 'Green Park': 1},
    'Green Park': {'AIIMS': 1, 'Hauz Khas': 1},
    'Hauz Khas': {'Green Park': 1, 'Malviya Nagar': 1},
    'Malviya Nagar': {'Hauz Khas': 1, 'Saket': 1},
    'Saket': {'Malviya Nagar': 1, 'Qutab Minar': 1},
    'Qutab Minar': {'Saket': 1, 'Chhatarpur': 1},
    'Chhatarpur': {'Qutab Minar': 1, 'Sultanpur': 1},
    'Sultanpur': {'Chhatarpur': 1, 'Ghitorni': 1},
    'Ghitorni': {'Sultanpur': 1, 'Arjangarh': 1},
    'Arjangarh': {'Ghitorni': 1, 'Guru Dronacharya': 1},
    'Guru Dronacharya': {'Arjangarh': 1, 'Sikandarpur': 1},
    'Sikandarpur': {'Guru Dronacharya': 1, 'MG Road': 1},
    'MG Road': {'Sikandarpur': 1, 'IFFCO Chowk': 1},
    'IFFCO Chowk': {'MG Road': 1, 'Huda City Centre': 1},
    'Huda City Centre': {'IFFCO Chowk': 1},

    # Blue Line (Line 3/4)
    'Dwarka Sector 21': {'Dwarka Sector 8': 1},
    'Dwarka Sector 8': {'Dwarka Sector 21': 1, 'Dwarka Sector 9': 1},
    'Dwarka Sector 9': {'Dwarka Sector 8': 1, 'Dwarka Sector 10': 1},
    'Dwarka Sector 10': {'Dwarka Sector 9': 1, 'Dwarka Sector 11': 1},
    'Dwarka Sector 11': {'Dwarka Sector 10': 1, 'Dwarka Sector 12': 1},
    'Dwarka Sector 12': {'Dwarka Sector 11': 1, 'Dwarka Sector 13': 1},
    'Dwarka Sector 13': {'Dwarka Sector 12': 1, 'Dwarka Sector 14': 1},
    'Dwarka Sector 14': {'Dwarka Sector 13': 1, 'Dwarka': 1},
    'Dwarka': {'Dwarka Sector 14': 1, 'Dwarka Mor': 1},
    'Dwarka Mor': {'Dwarka': 1, 'Nawada': 1},
    'Nawada': {'Dwarka Mor': 1, 'Uttam Nagar West': 1},
    'Uttam Nagar West': {'Nawada': 1, 'Uttam Nagar East': 1},
    'Uttam Nagar East': {'Uttam Nagar West': 1, 'Janakpuri West': 1},
    'Janakpuri West': {'Uttam Nagar East': 1, 'Janakpuri East': 1},
    'Janakpuri East': {'Janakpuri West': 1, 'Tilak Nagar': 1},
    'Tilak Nagar': {'Janakpuri East': 1, 'Subhash Nagar': 1},
    'Subhash Nagar': {'Tilak Nagar': 1, 'Tagore Garden': 1},
    'Tagore Garden': {'Subhash Nagar': 1, 'Rajouri Garden': 1},
    'Rajouri Garden': {'Tagore Garden': 1, 'Ramesh Nagar': 1},
    'Ramesh Nagar': {'Rajouri Garden': 1, 'Moti Nagar': 1},
    'Moti Nagar': {'Ramesh Nagar': 1, 'Kirti Nagar': 1},
    'Kirti Nagar': {'Moti Nagar': 1, 'Shadipur': 1},
    'Shadipur': {'Kirti Nagar': 1, 'Patel Nagar': 1},
    'Patel Nagar': {'Shadipur': 1, 'Rajendra Place': 1},
    'Rajendra Place': {'Patel Nagar': 1, 'Karol Bagh': 1},
    'Karol Bagh': {'Rajendra Place': 1, 'Rajiv Chowk': 1},
    'Rajiv Chowk': {'Karol Bagh': 1, 'Barakhamba': 1},
    'Barakhamba': {'Rajiv Chowk': 1, 'Mandi House': 1},
    'Mandi House': {'Barakhamba': 1, 'Supreme Court': 1},
    'Supreme Court': {'Mandi House': 1, 'Indraprastha': 1},
    'Indraprastha': {'Supreme Court': 1, 'Yamuna Bank': 1},
    'Yamuna Bank': {'Indraprastha': 1, 'Akshardham': 1, 'Laxmi Nagar': 1},
    'Akshardham': {'Yamuna Bank': 1, 'Mayur Vihar Phase-1': 1},
    'Mayur Vihar Phase-1': {'Akshardham': 1, 'Mayur Vihar Extension': 1},
    'Mayur Vihar Extension': {'Mayur Vihar Phase-1': 1, 'New Ashok Nagar': 1},
    'New Ashok Nagar': {'Mayur Vihar Extension': 1, 'Noida Sector 15': 1},
    'Noida Sector 15': {'New Ashok Nagar': 1, 'Noida Sector 16': 1},
    'Noida Sector 16': {'Noida Sector 15': 1, 'Noida Sector 18': 1},
    'Noida Sector 18': {'Noida Sector 16': 1, 'Botanical Garden': 1},
    'Botanical Garden': {'Noida Sector 18': 1, 'Golf Course': 1},
    'Golf Course': {'Botanical Garden': 1, 'Noida City Centre': 1},
    'Noida City Centre': {'Golf Course': 1, 'Noida Sector 34': 1},
    'Noida Sector 34': {'Noida City Centre': 1, 'Noida Sector 52': 1},
    'Noida Sector 52': {'Noida Sector 34': 1, 'Noida Sector 61': 1},
    'Noida Sector 61': {'Noida Sector 52': 1, 'Noida Sector 59': 1},
    'Noida Sector 59': {'Noida Sector 61': 1, 'Noida Sector 62': 1},
    'Noida Sector 62': {'Noida Sector 59': 1, 'Noida Electronic City': 1},
    'Noida Electronic City': {'Noida Sector 62': 1},

    # Violet Line (Line 6)
    'Kashmere Gate': {'Lal Qila': 1},
    'Lal Qila': {'Kashmere Gate': 1, 'Jama Masjid': 1},
    'Jama Masjid': {'Lal Qila': 1, 'Delhi Gate': 1},
    'Delhi Gate': {'Jama Masjid': 1, 'ITO': 1},
    'ITO': {'Delhi Gate': 1, 'Mandi House': 1},
    'Mandi House': {'ITO': 1, 'Janpath': 1},
    'Janpath': {'Mandi House': 1, 'Central Secretariat': 1},
    'Central Secretariat': {'Janpath': 1, 'Khan Market': 1},
    'Khan Market': {'Central Secretariat': 1, 'Jawaharlal Nehru Stadium': 1},
    'Jawaharlal Nehru Stadium': {'Khan Market': 1, 'Jangpura': 1},
    'Jangpura': {'Jawaharlal Nehru Stadium': 1, 'Lajpat Nagar': 1},
    'Lajpat Nagar': {'Jangpura': 1, 'Moolchand': 1},
    'Moolchand': {'Lajpat Nagar': 1, 'Kailash Colony': 1},
    'Kailash Colony': {'Moolchand': 1, 'Nehru Place': 1},
    'Nehru Place': {'Kailash Colony': 1, 'Kalkaji Mandir': 1},
    'Kalkaji Mandir': {'Nehru Place': 1, 'Govind Puri': 1},
    'Govind Puri': {'Kalkaji Mandir': 1, 'Harkesh Nagar': 1},
    'Harkesh Nagar': {'Govind Puri': 1, 'Jasola Apollo': 1},
    'Jasola Apollo': {'Harkesh Nagar': 1, 'Sarita Vihar': 1},
    'Sarita Vihar': {'Jasola Apollo': 1, 'Mohan Estate': 1},
    'Mohan Estate': {'Sarita Vihar': 1, 'Tughlakabad': 1},
    'Tughlakabad': {'Mohan Estate': 1, 'Badarpur': 1},
    'Badarpur': {'Tughlakabad': 1, 'Sarai': 1},
    'Sarai': {'Badarpur': 1, 'NHPC Chowk': 1},
    'NHPC Chowk': {'Sarai': 1, 'Mewala Maharajpur': 1},
    'Mewala Maharajpur': {'NHPC Chowk': 1, 'Sector-28': 1},
    'Sector-28': {'Mewala Maharajpur': 1, 'Badkhal Lake': 1},
    'Badkhal Lake': {'Sector-28': 1, 'Faridabad Old': 1},
    'Faridabad Old': {'Badkhal Lake': 1, 'Crown Plaza': 1},
    'Crown Plaza': {'Faridabad Old': 1, 'Neelam Chowk Ajronda': 1},
    'Neelam Chowk Ajronda': {'Crown Plaza': 1, 'Bata Chowk': 1},
    'Bata Chowk': {'Neelam Chowk Ajronda': 1, 'Escorts Mujesar': 1},
    'Escorts Mujesar': {'Bata Chowk': 1, 'Sant Surdas - Sihi': 1},
    'Sant Surdas - Sihi': {'Escorts Mujesar': 1, 'Raja Nahar Singh': 1},
    'Raja Nahar Singh': {'Sant Surdas - Sihi': 1},

    # Pink Line (Line 7)
    'Majlis Park': {'Azadpur': 1},
    'Azadpur': {'Majlis Park': 1, 'Shalimar Bagh': 1},
    'Shalimar Bagh': {'Azadpur': 1, 'Netaji Subhash Place': 1},
    'Netaji Subhash Place': {'Shalimar Bagh': 1, 'Shakurpur': 1},
    'Shakurpur': {'Netaji Subhash Place': 1, 'Punjabi Bagh West': 1},
    'Punjabi Bagh West': {'Shakurpur': 1, 'ESI Hospital': 1},
    'ESI Hospital': {'Punjabi Bagh West': 1, 'Rajouri Garden': 1},
    'Rajouri Garden': {'ESI Hospital': 1, 'Mayapuri': 1},
    'Mayapuri': {'Rajouri Garden': 1, 'Naraina Vihar': 1},
    'Naraina Vihar': {'Mayapuri': 1, 'Delhi Cantonment': 1},
    'Delhi Cantonment': {'Naraina Vihar': 1, 'Durgabai Deshmukh South Campus': 1},
    'Durgabai Deshmukh South Campus': {'Delhi Cantonment': 1, 'Sir Vishweshwaraiah Moti Bagh': 1},
    'Sir Vishweshwaraiah Moti Bagh': {'Durgabai Deshmukh South Campus': 1, 'Bhikaji Cama Place': 1},
    'Bhikaji Cama Place': {'Sir Vishweshwaraiah Moti Bagh': 1, 'Sarojini Nagar': 1},
    'Sarojini Nagar': {'Bhikaji Cama Place': 1, 'INA': 1},
    'INA': {'Sarojini Nagar': 1, 'South Extension': 1},
    'South Extension': {'INA': 1, 'Lajpat Nagar': 1},
    'Lajpat Nagar': {'South Extension': 1, 'Vinobapuri': 1},
    'Vinobapuri': {'Lajpat Nagar': 1, 'Ashram': 1},
    'Ashram': {'Vinobapuri': 1, 'Hazrat Nizamuddin': 1},
    'Hazrat Nizamuddin': {'Ashram': 1, 'Mayur Vihar Phase-1': 1},
    'Mayur Vihar Phase-1': {'Hazrat Nizamuddin': 1, 'Mayur Vihar Pocket 1': 1},
    'Mayur Vihar Pocket 1': {'Mayur Vihar Phase-1': 1, 'Trilokpuri Sanjay Lake': 1},
    'Trilokpuri Sanjay Lake': {'Mayur Vihar Pocket 1': 1, 'East Vinod Nagar - Mayur Vihar-II': 1},
    'East Vinod Nagar - Mayur Vihar-II': {'Trilokpuri Sanjay Lake': 1, 'Mandawali - West Vinod Nagar': 1},
    'Mandawali - West Vinod Nagar': {'East Vinod Nagar - Mayur Vihar-II': 1, 'IP Extension': 1},
    'IP Extension': {'Mandawali - West Vinod Nagar': 1, 'Anand Vihar': 1},
    'Anand Vihar': {'IP Extension': 1, 'Karkarduma': 1},
    'Karkarduma': {'Anand Vihar': 1, 'Karkarduma Court': 1},
    'Karkarduma Court': {'Karkarduma': 1, 'Krishna Nagar': 1},
    'Krishna Nagar': {'Karkarduma Court': 1, 'East Azad Nagar': 1},
    'East Azad Nagar': {'Krishna Nagar': 1, 'Welcome': 1},
    'Welcome': {'East Azad Nagar': 1, 'Jaffrabad': 1},
    'Jaffrabad': {'Welcome': 1, 'Maujpur - Babarpur': 1},
    'Maujpur - Babarpur': {'Jaffrabad': 1, 'Gokulpuri': 1},
    'Gokulpuri': {'Maujpur - Babarpur': 1, 'Johri Enclave': 1},
    'Johri Enclave': {'Gokulpuri': 1, 'Shiv Vihar': 1},
    'Shiv Vihar': {'Johri Enclave': 1},

    # Magenta Line (Line 8)
    'Janakpuri West': {'Dabri Mor': 1},
    'Dabri Mor': {'Janakpuri West': 1, 'Dashrath Puri': 1},
    'Dashrath Puri': {'Dabri Mor': 1, 'Palam': 1},
    'Palam': {'Dashrath Puri': 1, 'Sadar Bazaar Cantonment': 1},
    'Sadar Bazaar Cantonment': {'Palam': 1, 'Terminal 1-IGI Airport': 1},
    'Terminal 1-IGI Airport': {'Sadar Bazaar Cantonment': 1, 'Shankar Vihar': 1},
    'Shankar Vihar': {'Terminal 1-IGI Airport': 1, 'Vasant Vihar': 1},
    'Vasant Vihar': {'Shankar Vihar': 1, 'Munirka': 1},
    'Munirka': {'Vasant Vihar': 1, 'RK Puram': 1},
    'RK Puram': {'Munirka': 1, 'IIT Delhi': 1},
    'IIT Delhi': {'RK Puram': 1, 'Hauz Khas': 1},
    'Hauz Khas': {'IIT Delhi': 1, 'Panchsheel Park': 1},
    'Panchsheel Park': {'Hauz Khas': 1, 'Chirag Delhi': 1},
    'Chirag Delhi': {'Panchsheel Park': 1, 'Greater Kailash': 1},
    'Greater Kailash': {'Chirag Delhi': 1, 'Nehru Enclave': 1},
    'Nehru Enclave': {'Greater Kailash': 1, 'Kalkaji Mandir': 1},
    'Kalkaji Mandir': {'Nehru Enclave': 1, 'Okhla NSIC': 1},
    'Okhla NSIC': {'Kalkaji Mandir': 1, 'Sukhdev Vihar': 1},
    'Sukhdev Vihar': {'Okhla NSIC': 1, 'Jamia Millia Islamia': 1},
    'Jamia Millia Islamia': {'Sukhdev Vihar': 1, 'Okhla Vihar': 1},
    'Okhla Vihar': {'Jamia Millia Islamia': 1, 'Jasola Vihar Shaheen Bagh': 1},
    'Jasola Vihar Shaheen Bagh': {'Okhla Vihar': 1, 'Kalindi Kunj': 1},
    'Kalindi Kunj': {'Jasola Vihar Shaheen Bagh': 1, 'Okhla Bird Sanctuary': 1},
    'Okhla Bird Sanctuary': {'Kalindi Kunj': 1, 'Botanical Garden': 1},
    'Botanical Garden': {'Okhla Bird Sanctuary': 1},

    # Grey Line (Line 9)
    'Dwarka': {'Nangli': 1},
    'Nangli': {'Dwarka': 1, 'Najafgarh': 1},
    'Najafgarh': {'Nangli': 1, 'Dhansa Bus Stand': 1},
    'Dhansa Bus Stand': {'Najafgarh': 1},

    # Airport Express Line
    'New Delhi': {'Shivaji Stadium': 1},
    'Shivaji Stadium': {'New Delhi': 1, 'Dhaula Kuan': 1},
    'Dhaula Kuan': {'Shivaji Stadium': 1, 'Delhi Aerocity': 1},
    'Delhi Aerocity': {'Dhaula Kuan': 1, 'IGI Airport': 1},
    'IGI Airport': {'Delhi Aerocity': 1, 'Dwarka Sector 21': 1},
    'Dwarka Sector 21': {'IGI Airport': 1},

    # Interchange Handling
    'Rajiv Chowk': {
        'Karol Bagh': 1,  # Blue Line
        'Barakhamba': 1,  # Blue Line
        'New Delhi': 1    # Yellow Line
    },
    'Kashmere Gate': {
        'Tis Hazari': 1,  # Red Line
        'Shastri Park': 1,  # Red Line
        'Civil Lines': 1  # Yellow Line
    },
    'Mandi House': {
        'Barakhamba': 1,  # Blue Line
        'ITO': 1,        # Violet Line
        'Janpath': 1     # Violet Line
    },
    'Hauz Khas': {
        'Green Park': 1,  # Yellow Line
        'Panchsheel Park': 1  # Magenta Line
    },
    'Botanical Garden': {
        'Noida Sector 18': 1,  # Blue Line
        'Okhla Bird Sanctuary': 1  # Magenta Line
    }
}

def dijkstra(graph, start, end):
    # Validate stations exist
    if start not in graph or end not in graph:
        return [], float('inf')
    
    distances = {station: float('inf') for station in graph}
    previous = {station: None for station in graph}
    distances[start] = 0
    queue = [(0, start)]

    while queue:
        current_distance, current_station = heapq.heappop(queue)
        if current_station == end:
            break
            
        # Skip if station has no connections
        if current_station not in graph:
            continue
            
        for neighbor, weight in graph[current_station].items():
            # Skip invalid neighbors
            if neighbor not in distances:
                continue
                
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_station
                heapq.heappush(queue, (distance, neighbor))
    
    # Rest of the code remains same

    path = []
    station = end
    while station is not None:
        path.insert(0, station)
        station = previous[station]
    if path and path[0] == start:
        return path, distances[end]
    else:
        return [], float('inf')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stations')
def stations():
    return jsonify(sorted(list(metro_graph.keys())))

@app.route('/route', methods=['POST'])
def route():
    data = request.get_json()
    source = data.get('source')
    destination = data.get('destination')
    if not source or not destination:
        return jsonify({'error': 'Invalid input'}), 400
    path, distance = dijkstra(metro_graph, source, destination)
    if not path:
        return jsonify({'error': 'No route found'}), 404
    return jsonify({'path': path, 'distance': distance})

if __name__ == '__main__':
    app.run(debug=True)
