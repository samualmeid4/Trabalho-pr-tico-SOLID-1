import sqlite3

DB_PATH = "db_solid.sqlite3"


def _get_connection():
    conexao = sqlite3.connect(DB_PATH)
    conexao.execute("PRAGMA foreign_keys = ON;")
    return conexao


class CategoriaRepository:
    def listar(self):
        sql = """
            SELECT id, descricao
            FROM Categoria
            ORDER BY descricao
        """
        conexao = _get_connection()
        try:
            return conexao.cursor().execute(sql).fetchall()
        finally:
            conexao.close()

    def obter_por_id(self, categoria_id):
        sql = """
            SELECT id, descricao
            FROM Categoria
            WHERE id = ?
        """
        conexao = _get_connection()
        try:
            return conexao.cursor().execute(sql, (categoria_id,)).fetchone()
        finally:
            conexao.close()

    def inserir(self, descricao):
        sql = "INSERT INTO Categoria(descricao) VALUES(?)"
        conexao = _get_connection()
        try:
            conexao.cursor().execute(sql, (descricao,))
            conexao.commit()
        finally:
            conexao.close()

    def atualizar(self, categoria_id, descricao):
        sql = """
            UPDATE Categoria
            SET descricao = ?
            WHERE id = ?
        """
        conexao = _get_connection()
        try:
            conexao.cursor().execute(sql, (descricao, categoria_id))
            conexao.commit()
        finally:
            conexao.close()

    def excluir(self, categoria_id):
        sql = "DELETE FROM Categoria WHERE id = ?"
        conexao = _get_connection()
        try:
            conexao.cursor().execute(sql, (categoria_id,))
            conexao.commit()
        finally:
            conexao.close()


class ProdutoRepository:
    def listar_com_categoria(self):
        sql = """
            SELECT  pro.id,
                    pro.descricao,
                    pro.preco_unitario,
                    pro.quantidade_estoque,
                    pro.categoria_id,
                    cat.descricao as categoria
            FROM Produto pro
            INNER JOIN Categoria cat ON cat.id = pro.categoria_id
            ORDER BY pro.descricao
        """
        conexao = _get_connection()
        try:
            return conexao.cursor().execute(sql).fetchall()
        finally:
            conexao.close()

    def obter_por_id(self, produto_id):
        sql = """
            SELECT  pro.id,
                    pro.descricao,
                    pro.preco_unitario,
                    pro.quantidade_estoque,
                    pro.categoria_id,
                    cat.descricao as categoria
            FROM Produto pro
            INNER JOIN Categoria cat ON cat.id = pro.categoria_id
            WHERE pro.id = ?
        """
        conexao = _get_connection()
        try:
            return conexao.cursor().execute(sql, (produto_id,)).fetchone()
        finally:
            conexao.close()

    def inserir(self, descricao, preco_unitario, quantidade_estoque, categoria_id):
        sql = """
            INSERT INTO Produto (
                descricao,
                preco_unitario,
                quantidade_estoque,
                categoria_id
            )
            VALUES(?, ?, ?, ?)
        """
        conexao = _get_connection()
        try:
            conexao.cursor().execute(
                sql,
                (descricao, preco_unitario, quantidade_estoque, categoria_id),
            )
            conexao.commit()
        finally:
            conexao.close()

    def atualizar(self, produto_id, descricao, preco_unitario, quantidade_estoque, categoria_id):
        sql = """
            UPDATE Produto
            SET descricao = ?,
                preco_unitario = ?,
                quantidade_estoque = ?,
                categoria_id = ?
            WHERE id = ?
        """
        conexao = _get_connection()
        try:
            conexao.cursor().execute(
                sql,
                (descricao, preco_unitario, quantidade_estoque, categoria_id, produto_id),
            )
            conexao.commit()
        finally:
            conexao.close()

    def excluir(self, produto_id):
        sql = "DELETE FROM Produto WHERE id = ?"
        conexao = _get_connection()
        try:
            conexao.cursor().execute(sql, (produto_id,))
            conexao.commit()
        finally:
            conexao.close()

    def listar_categorias(self):
        sql = "SELECT id, descricao FROM Categoria ORDER BY descricao"
        conexao = _get_connection()
        try:
            return conexao.cursor().execute(sql).fetchall()
        finally:
            conexao.close()
