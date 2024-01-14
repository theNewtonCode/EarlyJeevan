import requests
from bs4 import BeautifulSoup

def get_first_n_sentences(text, n):
    sentences = text.split('. ')
    return '. '.join(sentences[:n])+".", len(sentences)

def get_early_life_text(name, numsent):
    try:

        url = f'https://en.wikipedia.org/wiki/{name}'
        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')

        early_life_heading = soup.find('span', {'id': 'Early_life_and_education'})
        if early_life_heading is None:
            early_life_heading = soup.find('span', {'id': 'Early_life_2'})
        if early_life_heading is None:
            early_life_heading = soup.find('span', {'id': 'Early_life'})
        if early_life_heading is None:
            early_life_heading = soup.find('span', {'id': 'Career'})
        # if early_life_heading is None:
        #     early_life_heading = soup.find('span', {'id': 'Early_life_and_family'})
        # if early_life_heading is None:
        #     early_life_heading = soup.find('span', {'id': 'Early_and_personal_life'})
        # if early_life_heading is None:
        #     early_life_heading = soup.find('span', {'id': 'Early_life_and_background'})
        if early_life_heading is None:
            early_life_heading = soup.find(lambda tag: tag.name == 'span' and ('Early_life_and' in tag.get('id', '') or 'Early_and' in tag.get('id', '')))
        if early_life_heading is None:
            return "xyz", 0
        next_heading = early_life_heading.find_next('h2')


        early_life_text = ''
        current_element = early_life_heading.parent
        while current_element != next_heading:
            if current_element.name and not current_element.find('img') and (not current_element.has_attr('class') or 'thumbcaption' not in current_element['class']):
                early_life_text += current_element.text + '\n'
            current_element = current_element.next_element


        lines = early_life_text.splitlines()
        filtered_lines = []
        for line in lines:
            if len(line.split()) < 10:
                continue
            main_line = ""
            x = False
            for char in line:
                if char == "[":
                    x = True
                if x==False:
                    main_line+=char
                if char == "]":
                    x = False
            filtered_lines.append(main_line)
        filtered_text = "\n".join(filtered_lines)
        x, y = get_first_n_sentences(filtered_text, numsent)
        return x, y
    except requests.exceptions.HTTPError:
        return "xyz", 0
