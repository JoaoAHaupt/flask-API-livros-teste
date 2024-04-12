from flask import Flask, jsonify, request
from livros import livros
app = Flask(__name__)


def salvar_livros_em_arquivo():
    with open('livros.py', 'w', encoding='utf-8') as arquivo:
        arquivo.write("livros = " + str(livros))



@app.route('/livros', methods=['GET'])
def obter_todos_livros():
    return jsonify(livros), 200


@app.route('/livros/<int:id>', methods=['GET'])
def obter_id_livro(id):
    for livro in livros:
        if id == livro.get('id'):
            return jsonify(livro), 200

    return jsonify({'error': 'Livro não encontrado'}), 404


@app.route('/livros/<int:id>', methods=['PUT'])
def editar_livro(id):
    livro_copia = request.get_json()
    for i, livro in enumerate(livros):
        if id == livro.get('id'):
            livros[i].update(livro_copia)
            salvar_livros_em_arquivo()
            return jsonify(livros[i]), 202

    return jsonify({'error': 'Livro não encontrado'}), 404



@app.route('/livros', methods=['POST'])
def incluir_livro_novo():
    ultimo_livro = livros[len(livros) - 1]
    novo_livro = request.get_json()
    novo_livro['id'] = ultimo_livro.get('id') + 1
    livros.append(novo_livro)
    salvar_livros_em_arquivo()
    return jsonify(livros), 201


@app.route('/livros/<int:id>', methods=['DELETE'])
def deletar_livro_id(id):
    for i, livro in enumerate(livros):
        if id == livro.get('id'):
            del livros[i]
            salvar_livros_em_arquivo()
            return jsonify({'accepted': 'Livro deletado'}), 202

    return jsonify({'error': 'Livro não encontrado'}), 404



if __name__ == '__main__':
    app.run(port=5000, host='localhost')
