#! /usr/bin/python3
from repositorio import Repositorio
from nota import Nota

class RepositorioNota(Repositorio):
    '''Consulta y escribe objetos Nota en la BD. '''

    def get_one(self, id_nota):
        '''Recibe un id de nota (número entero). Retorna un objeto Nota. Si no
        lo encuentra, retorna None.'''
        consulta = "SELECT id, texto, etiquetas FROM notas WHERE id = ?"
        result = self.cursor.execute(consulta, [id_nota]).fetchone()

        if result == None:
            return None
        else:
            return Nota(result[1], result[2], result[0])

    def get_all(self):
        '''Retorna todas las notas que haya almacenadas en la BD'''
        consulta = "SELECT id, texto, etiquetas FROM notas"
        result = self.cursor.execute(consulta).fetchall()

        lista_de_notas = []

        for unResultado in result:
            lista_de_notas.append(
                    Nota(unResultado[1], unResultado[2], unResultado[0])
                    )
        return lista_de_notas

    def store(self, nota):
        '''Recibe un objeto nota y lo almacena en la Base de Datos
        En caso de éxito, retorna el id de la nota, número generado por la base
        de datos. En caso de fracaso, retorna 0 (cero).'''
        try:
            query = "INSERT INTO notas (texto, etiquetas) VALUES (?, ?)"
            result = self.cursor.execute(query, [nota.texto, nota.etiquetas])
            nota.id = result.lastrowid

            self.bd.commit()
            return nota.id
        except:
            self.bd.rollback()
            return 0
        
    def delete(self, nota):
        '''Recibe un objeto Nota y lo elimina de la Base de Datos.
        Retorna True si tuvo éxito, False de lo contrario.'''
        try:
            query = "DELETE FROM notas WHERE id = ?"
            self.cursor.execute(query, [nota.id])
            c = self.cursor.rowcount
            if c == 0:
                self.bd.rollback()
                return False
            else:
                self.bd.commit()
                return True
        except:
            self.bd.rollback()
            return False

    def update(self, nota):
        '''Recibe un objeto nota y actualiza sus datos en la base de datos
        (no se puede actualizar el id de la nota, pero sí el resto de sus
        datos). Retorna True si tuvo éxito, False de lo contrario.'''
        try:
            query = "UPDATE notas SET texto = ?, etiquetas = ? WHERE id = ?"
            result = self.cursor.execute(query, [nota.texto, nota.etiquetas,
                                                 nota.id])
            if result.rowcount == 0:
                self.bd.rollback()
                return False
            else:
                self.bd.commit()
                return True
        except:
            self.bd.rollback()
            return False
