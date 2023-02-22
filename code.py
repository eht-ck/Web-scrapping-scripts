from bs4 import BeautifulSoup
import requests
import json
import re as relib 
chap_num=1;
verses = []
def ext(prev,curr,test_case):
    global verses
    global chap_num
    if(prev!=chap_num):
        with open('chapter'+str(prev-1)+'.json', 'w') as f:
            json.dump(verses, f, indent=4)
            print("Successfull chapter", (prev-1))
            verses = []
            chap_num=prev
    
    if(int(prev)>=int(test_case)):
        return True;
    url = 'https://vedabase.io/en/library/sb/1/'+str(prev)+'/'+str(curr)+'/'
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, 'html.parser')
    verse = soup.find('div', {'class': 'r r-title r-verse'}).text.strip()
    verse = verse[7:].replace('.','')    
    devanagari_text = soup.find('div', {'class': 'r r-devanagari'}).text
    dev_english = soup.find('div', {'class': 'r r-lang-en r-verse-text'}).text
    translation=soup.find('div', {'class': 'r r-lang-en r-translation'}).text
    synonyms = [synonym.text.strip() for synonym in soup.find('div', {'class': 'r r-lang-en r-synonyms'}).find_all('a')]
    wrapper_purport = soup.findAll('div', {'class': 'r r-lang-en r-paragraph'})
    purport=""
    for i in wrapper_purport:
        purport=purport+" "+(i.text)
    verse_dict = {
            "verse": verse,
            "devanagari": devanagari_text,
            "english_devnagari":dev_english,
            "verse_Syn": synonyms,
            "translation": translation,
            "purport":purport 
        }
    verses.append(verse_dict)
      
for i in range(1,22):
    url = 'https://vedabase.io/en/library/sb/1/'+str(i)+'/'
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, 'html.parser')
    dls = soup.find_all('dl')
    last=0;
    verse_dict=[];
    for dl in dls:
        dt_a = dl.find('dt').find('a')
        dt_text = dt_a.text.strip() 
        dd_text = dl.find('dd').text.strip()
        verse_num=""
        for k in dt_text:
            if(k.isdigit() or k=='-'):
                verse_num=verse_num+k;
        verse_dict.append(verse_num); 
        
    for j in range(0,len(verse_dict)):
        if(ext(i,verse_dict[j],21)):
            break;