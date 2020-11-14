import streamlit as st
from io import BytesIO
from PIL import Image, ImageColor
import requests
import PIL
   
@st.cache
def get_rgb(image): # Returns Median Cut Alg. applied version of an image and its RGB data
    
    image_ = image.quantize(colors = 10, method = 0).convert('RGB') #method = 0 for MEDIANCUT ALGORITHM
    rgb = list(image_.getdata())
    return image_, rgb


def getscale(rgb): # Returns a dictionary contains {(r,g,b): Counts/Total}

    d = {}
    for i in rgb:
        if i not in d.keys(): 
            d[i] = 1
        else: 
            d[i] += 1
        
    mostrgb = [(k,v) for k, v in sorted(d.items(), key = lambda x:x[1], reverse = True)]    
    values = [i[1] for i in mostrgb]
    total = sum(values)
    myd = {}
    for rgb, freq in mostrgb:
        p = round(freq/total, 3)
        myd[rgb] = p

    return myd

def get_hex(rgb: dict): # Returns hex codes of RGB data
    rgblist = {'#%02x%02x%02x' %i:i for i in rgb.keys()}
    return '\n'.join(rgblist.keys())

def make(myd): #Returns a new image consists of most occured colours in the image
    l = []
    for k, v in myd.items():
        l.extend([k] * int(700 * v ) * 700)
    
    if len(l) > 700**2: 
        l = l[:700**2]
        
    else:
        cut = 700 - len(l)
        l.extend([list(myd.keys())[-1]] * cut)
    
    im = Image.new('RGB', (700, 700))
    im.putdata(l)
    return(im)
    
st.set_option('deprecation.showfileUploaderEncoding', False)
st.title('_Dominant Colours Finder_')
choice = st.radio(
    label = 'Choose an image from...', 
    options = ('the web', 'local storage'))


if choice == 'the web':
    link = st.text_input('Please enter an image link')
    if link.startswith('https://') or link.startswith('https://'):
        response = requests.get(link)
        file_buffer = BytesIO(response.content)
    if link:
            
        try:     
            image = Image.open(file_buffer)
            st.image(image, width = 700)
            st.success('The uploading is succesful!')
            # st.write(f'Resolution is {image.size[0]}x{image.size[1]}')
    
        except:  
            text = 'This link is not valid or does not contain image in jpg or png format!'
            st.error(text)
            st.stop()
        if image:        
            button = st.button('Get the palette of dominant colours!')
            if button:
                st.image(make(getscale(get_rgb(image)[1])))    
                st.markdown('**_Colours are: _**' + get_hex(getscale(get_rgb(image)[1])))

    

elif choice == 'local storage':
    file_buffer = st.file_uploader(
        label = 'Import your image', type = ['png', 'jpg']
        )
    
    if file_buffer:
        try:        
            image = Image.open(file_buffer)
            st.image(image, width = 700)
            st.success('The uploading is succesful!')
            # st.write(f'Resolution is {image.size[0]}x{image.size[1]}')
        except:
            pass
        
        if image:        
            button = st.button('Get the palette of dominant colours!')
            if button:
                st.image(make(getscale(get_rgb(image)[1])))
                st.markdown('**_Colours are: _**' + get_hex(getscale(get_rgb(image)[1])))
                

                

            