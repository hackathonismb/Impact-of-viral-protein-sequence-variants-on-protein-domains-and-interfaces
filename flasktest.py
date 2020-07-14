from flask import Flask
from mewtate_struct_impact import mewtate_struct_impact

app = Flask(__name__)

@app.route('/') # I think the arguments could be passed in through the URL...
def example( pdb='6VXX', mutation='EA191H', ):
    result = mewtate_struct_impact( '6VXX', 'EA191H', )
    return result.out

if __name__ == '__main__':
    app.run()
