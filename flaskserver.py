from flask import Flask
import json
# from mewtate_struct_impact import mewtate_struct_impact

app = Flask(__name__)

@app.route('/<pdb>/<mutation>')
def mewtate( pdb, mutation):
    # Commenting out for now
    # result = mewtate_struct_impact( '6VXX', 'EA191H', )
    # return result.out
    # Open and return mock data
    print(pdb,mutation)
    json_file = open('mock/mock.json')
    data = json.load(json_file)
    return data

if __name__ == '__main__':
    app.run(host= '34.86.5.194')
