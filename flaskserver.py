from flask import Flask
from flask_cors import CORS
import json
# from mewtate_struct_impact import mewtate_struct_impact

app = Flask(__name__)
CORS(app)


@app.route('/<pdb>/<mutation>')
def mewtate(pdb, mutation):
    # Commenting out for now
    # result = mewtate_struct_impact( '6VXX', 'EA191H', )
    # return result.out
    # Open and return mock data
    print(pdb, mutation)
    json_file = open('mock/mock.json')
    data = json.load(json_file)
    return data


if __name__ == '__main__':
    app.run()
