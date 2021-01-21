import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
#import dash_table_experiments as dt                                                                                                                                                           
import dash_reusable_components as drc

import math
from base64 import decodestring
import base64
import os
from PIL import Image
from shoezam.shoe_classifier import ShoeClassifier
#IMAGE_STRING_PLACEHOLDER = drc.pil_to_b64(Image.open('image_test.jpg').copy(), enc_format='jpeg')
cwd = os.getcwd()
IMAGE_PIL_PLACEHOLDER = Image.open(cwd + '/image_test.jpg')


#input_image_path = cwd +"/image_test.jpg"
#cnn.find_top_matches(input_image_path)


#from keras.applications.vgg19 import VGG19
#from keras.models import Model
#base_model = VGG19(weights='imagenet')
#layer_name = 'fc2'
#layer_model = Model(inputs=base_model.input, outputs=base_model.get_layer(layer_name).output)

app = dash.Dash()

cnn = ShoeClassifier(subcategory='oxfords')

app.scripts.config.serve_locally = True

app.layout = html.Div([
        # Banner display
        html.Div([
            html.H2(
                'Shoezam: a shoe recommendation app',
                id='title'
            )#,
            #html.Img(
            #    src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo/new-branding/dash-logo-by-plotly-stripe-inverted.png"
            #)
        ],
            className="banner"
        ),
        html.Div(className="container", children=[
            html.Div(className='row', children=[
                html.Div(className='five columns', children=[
                        dcc.Upload(
                            id='upload-image',
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Select an Image')
                            ]),
                            style={
                                'width': '100%',
                                'height': '50px',
                                'lineHeight': '50px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center'
                            },
                            #multiple=True
                            #accept='image/*'
                        ),
                        # The Interactive Image Div contains the dcc Graph
                        # showing the image, as well as the hidden div storing
                        # the true image
                        #html.Div(id='output-image-upload',
                        #    style={
                        #        'width': '100%'}
                        #),
                        html.Div(id='output-image-upload', children=[
                            drc.InteractiveImagePIL(
                                        image_id='interactive-image',
                                        #image=im_pil,
                                        #image=IMAGE_PIL_PLACEHOLDER,
                                        #enc_format=enc_format,
                                        display_mode='fixed',
                                        #dragmode=dragmode,
                                        #verbose=DEBUG
                                )


                            #dcc.Graph(id='interactive-image', style={'height': '80vh'}),
                            #html.Div(
                            #    id='div-storage',
                            #    style={'display': 'none'}
                            #)

                        ]),
                            

                        html.Button(
                            'Redo Search on Selection',
                            id='button-redo-search',
                            style={'margin-right': '10px', 'margin-top': '5px'}
                        ),
                        html.Button(
                            'Undo',
                            id='button-undo',
                            style={'margin-top': '5px'}
                        ),
                        ]
                    ),
                html.Div(
                    className='seven columns',
                    style={'float': 'right'},
                    children=[
                        html.Div(id='output-similar-items',style={'margin-right': '10px', 'margin-left': '10px','margin-top': '5px','display':'inline-block'})
                    ]
                )
            ])
        ]),
    ])



def parse_contents(contents):
    return html.Div([

        # HTML images accept base64 encoded strings in the same format                                                                                                                         
        # that is supplied by the upload                                                                                                                                                       
        html.Img(src=contents,style={'height':200}),
        html.Hr()
        #html.Div('Raw Content'),
        #html.Pre(contents[:100] + '...', style={
        #    'whiteSpace': 'pre-wrap',
        #    'wordBreak': 'break-all'
        #})
    ],style={'height':320})

def display_encoded_image_and_metadata(encoded_image,head,brand,name,price,sale,url):
    width = 200
    return html.Div([

        html.H2(head,style={'height':'40px'}),
        html.H5(name,style={'height':'80px'}),
        html.H6(brand,style={'height':'60px'}),
        html.P("MSRP: {}".format(price)),
        html.Img(src='data:image/jpg;base64,{}'.format(encoded_image.decode()),style={'width':width}),
        html.P("Sale: {}".format(sale)),
        html.A(html.Button('BUY NOW'),href=url),
        html.Hr()
        ],style={'margin-right': '10px', 'margin-left': '10px','margin-top': '5px','display':'inline-block','width':width})

def parse_interactive_image(im_pil):
    return  drc.InteractiveImagePIL(
            image_id='interactive-image',
            image=im_pil,
            #enc_format=enc_format,
            display_mode='fixed',
            #dragmode=dragmode,
            #verbose=DEBUG
        )


@app.callback(Output('output-image-upload', 'children'),
              [Input('upload-image', 'contents')])
def update_output(image_str):
    if not image_str:
        print("no image")
        #im_pil = Image.open(cwd + '/image_test.jpg')
    #else:
    print(image_str[0:100])
    string = image_str.split(';base64,')[-1]
    im_pil = drc.b64_to_pil(string.encode('ascii'))
        #image = image_str.split(',')[1]
        #data = decodestring(image.encode('ascii'))


        ## good...
        #data = decodestring(string.encode('ascii'))
        #with open(cwd +"/image_test.jpg", "wb") as f:
        #    f.write(data)

    return parse_interactive_image(im_pil)


@app.callback(Output('output-similar-items', 'children'),
              [Input('upload-image', 'contents'),
               Input('button-undo','n_clicks'),
               Input('button-redo-search','n_clicks')],
              #[State('interactive-image', 'selectedData')]
              )
def update_similar_items(image_str,undo_clicks,redo_clicks):
    if not image_str:
        print("no images")
        return

    print(image_str[0:100])
    string = image_str.split(';base64,')[-1]
    im_pil = drc.b64_to_pil(string.encode('ascii'))

    # good
    data = decodestring(string.encode('ascii'))
    with open(cwd +"/image_test.jpg", "wb") as f:
        f.write(data)

    # fine but don't want to dl images off internet
    input_image_path = cwd +"/image_test.jpg"
    print('input_image_path = {}'.format(input_image_path))


    #global cnn
    top_match, frugal_match, premium_match = cnn.find_top_matches_by_path(input_image_path)
    #top_match, frugal_match, premium_match = cnn.find_top_matches_by_PIL_image(im_pil)
    similar_image_paths = [top_match['image_path'], frugal_match['image_path'],premium_match['image_path']]
    names = [top_match['name'], frugal_match['name'],premium_match['name']]
    brands = [top_match['brand'], frugal_match['brand'],premium_match['brand']]
    urls = [top_match['url'], frugal_match['url'],premium_match['url']]
    prices = [top_match['msrp'], frugal_match['msrp'],premium_match['msrp']]
    sales = []
    for salep in [top_match['sale'], frugal_match['sale'],premium_match['sale']]:
        if (salep is None) or math.isnan(salep):
            sales.append('None')
        else:
            sales.append(salep)

    heads = ['Match!!!','Frugal','Premium']
    children = []
    for i, (image_filename,head,brand,name,price,sale,url) in enumerate(zip(similar_image_paths,heads,brands,names,prices,sales,urls)):
        encoded_image = base64.b64encode(open(image_filename, 'rb').read())
        children.append(display_encoded_image_and_metadata(encoded_image,head,brand,name,price,sale,url))
    return children

              #[Input('interactive-image', 'children'),
#@app.callback(Output('output-similar-items', 'children'),
#              [Input('output-image-upload', 'children'),
#               Input('button-undo','n_clicks'),
#               Input('button-redo-search','n_clicks')],
#              [State('interactive-image', 'selectedData')]
#                  )
#def update_selection(img, undo_clicks,redo_clicks,selectedData):
#    print("\n\n\n\n\n\n probably able to select data \n\n\n\n\n\n\n")
#    return


#image_filename = 'my-image.png' # replace with your own image

external_css = [
    # Normalize the CSS
    "https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
    # Fonts
    "https://fonts.googleapis.com/css?family=Open+Sans|Roboto"
    "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
    # For production
    "https://cdn.rawgit.com/xhlulu/0acba79000a3fd1e6f552ed82edb8a64/raw/dash_template.css",
    # Custom CSS
    "https://cdn.rawgit.com/xhlulu/dash-image-processing/1d2ec55e/custom_styles.css",
]

for css in external_css:
    app.css.append_css({"external_url": css})
#app.css.append_css({
#    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
#})

if __name__ == '__main__':
    app.run_server(debug=False)
