from database.DB_connect import DBConnect
from model.album import Album
from model.track import Track


class DAO():

    @staticmethod
    def getAllNodi():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT distinct a.*
                from Album a 
                join Track t on a.AlbumId = t.AlbumId 
                """

        cursor.execute(query)

        for row in cursor:
            album = Album(**row)
            results.append(album)

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllTracks():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT distinct t.*
                from Track t 
                """

        cursor.execute(query)

        for row in cursor:
            track = Track(**row)
            results.append(track)

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllArchi():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT distinct t1.id1 as id_1, t2.id2 as id_2
                from
                (SELECT distinct a.AlbumId as id1, t.GenreId as g1
                from Album a 
                join Track t on a.AlbumId = t.AlbumId ) t1,
                (SELECT distinct a.AlbumId as id2, t.GenreId as g2
                from Album a 
                join Track t on a.AlbumId = t.AlbumId) t2
                where t1.g1 = t2.g2 and t1.id1 < t2.id2
                """

        cursor.execute(query)

        for row in cursor:
            results.append((row['id_1'], row['id_2']))

        cursor.close()
        conn.close()
        return results



