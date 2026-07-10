from database.DB_connect import DBConnect
from model.album import Album


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
                SELECT distinct t.TrackId, t.AlbumId 
                from Album a 
                join Track t on a.AlbumId = t.AlbumId 
                """

        cursor.execute(query)

        for row in cursor:
            results.append((row['TrackId'], row['AlbumId']))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllArchi():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT distinct t1.idA1 as id_1, t2.idA2 as id_2
                from
                (SELECT distinct t.TrackId as idT1, t.GenreId as idG1, t.AlbumId as idA1
                from Album a 
                join Track t on a.AlbumId = t.AlbumId) t1,
                (SELECT distinct t.TrackId as idT2, t.GenreId as idG2, t.AlbumId as idA2
                from Album a 
                join Track t on a.AlbumId = t.AlbumId) t2
                where t1.idG1 = t2.idG2 and t1.idA1 < t2.idA2
                """

        cursor.execute(query)

        for row in cursor:
            results.append((row['id_1'], row['id_2']))

        cursor.close()
        conn.close()
        return results




